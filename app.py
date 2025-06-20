from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
from flask import Flask, render_template, request, g, jsonify
from io import BytesIO
from dotenv import load_dotenv
import requests
import graphUrl 
import base64
import os
import sqlite3
import json
import traceback

# Configure application 
app = Flask(__name__)
DATABASE = 'database.db'

# Templates are reloaded automatically when they change, without needing to restart the server (STILL NEEDS TO HIT REFRESH PAGE).
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Session is cleared when user closes the web. 
app.config['SESSION_PERMANENT'] = False


# python -c "import secrets; print(secrets.token_hex(16))"
load_dotenv()
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# app.debug = True
# toolbar = DebugToolbarExtension(app)

# Database connection helper: Using Flask’s g object ensures you reuse the same connection within a single request
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        # This line allows you to access rows as dictionaries
        g.db.row_factory = sqlite3.Row
    return g.db

# Initialize the Database
def init_db():
    db = get_db()
    cursor = db.cursor()
    db.commit()

#region: Utility Functions not connected to any route
# Use to get location's city name and state name.
# Function GETS Lat and Long from user input via route()
def fetchAPI_points(latitude: float, longitude: float) -> dict:
    # can modify to request user's input of lat and lon.
    # latitude: float  = 47.402094608175815
    # longitude: float = -121.41549110412599
    fetch_url_points: str = f"https://api.weather.gov/points/{latitude},{longitude}"
    response = requests.get(fetch_url_points)

    if response.status_code == 200:
        points_json = response.json()
        return points_json
    
    else:
        print(f"Failed to retrieve data: {response.status_code}")

# Use to get location's elevation and forecast "detailedForecast"-(hover in page) and "shortForecast"-(shown in page)
# Function calls fetchAPI_points 
def fetchAPI_forecastdata(latitude: float, longitude: float) -> dict:

    points_json = fetchAPI_points(latitude, longitude)
    response = requests.get(points_json["properties"]["forecast"])

    if response.status_code == 200:
        forecastdata_json = response.json()
        return forecastdata_json
    
    else:
        print(f"fetchAPI_forecastdata failed to retrieve data: {response.status_code}")

# NO LONGER IN USE - use to get location's hourly forecast (expansive raw data)
def fetchAPI_forecastGridData() -> dict:

    points_json = fetchAPI_points()

    response = requests.get(points_json["properties"]["forecastGridData"])

    if response.status_code == 200:
        forecastGridData_json = response.json()

        return forecastGridData_json
    else:
        print(f"fetchAPI_forecashhourlydata failed to retrieve data: {response.status_code}")

# Encode image from RAM to base64 (ASCII Text) -- Require for displaying image in HTML.
def encode_image_to_base64(img_io):
    # Ensure that the input coming in will have the pointer starting at the front of the allocated memory. 
    img_io.seek(0)
    # Binary image data (bytes) → Base64-encoded data (bytes) → Base64-encoded string (str).
    base64_img = base64.b64encode(img_io.getvalue()).decode('ascii')
    # Return a string neccesary to display the image as PNG in html.
    return f'data:image/png;base64,{base64_img}'

#endregion: Utility Functions

#region: Custom Jinja filler functions
# Custom Jinja filler to reformat ISOtime to 12hr PM/AM time
@app.template_filter('ISO_time_reformat')
def format_time(iso_time: str):
    datetime_obj = datetime.fromisoformat(iso_time)
    # Return only hour and AM/PM - ex: 12PM, 6AM, etc... 
    return datetime_obj.strftime('%I%p').lstrip('0')

# Custom Jinja filler to convert numerical meter to feet
@app.template_filter('meter_to_feet')
def format_elevation(meter):
    feet = meter * 3.28084
    return int(feet)

# Tells browsers to never cache response (meaning that request to the server is always made)    
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#endregion: Custom Jinja filler functions

# Clean Up After Each Request: It’s important to close the database connection after each request to avoid resource leaks. You can do this by registering a teardown function.
@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()



def refresh_forecastdata():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT latitude, longitude FROM forecasts")
    rows = cursor.fetchall()
    if not rows:
        return 
    else:
        for latitude, longitude in rows:
            # Request the forecast data and the plot using the latitude and longitude.
            points:              dict = fetchAPI_points(latitude, longitude)
            forecastdata:        dict = fetchAPI_forecastdata(latitude, longitude)
            detailedForecastPlot: BytesIO = graphUrl.getDetailedForecast(latitude, longitude)
            img_base64 = encode_image_to_base64(detailedForecastPlot)

            # DB is setup so that lat and long is a unique composite. This will replace the entry if lat and long from POST method is the same as in the db. It will insert a new entry if lat and long is different.
            cursor.execute('''INSERT OR REPLACE INTO forecasts (latitude, longitude, location, elevation, forecastdata_periods, detailedForecastPlot_Image, last_updated) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (
                            latitude,
                            longitude,
                            json.dumps(points.get("properties", {}).get("relativeLocation", {}).get("properties", {})),
                            json.dumps(forecastdata.get("properties", {}).get("elevation", {"unitCode": "", "value": 0})),
                            json.dumps(forecastdata.get("properties", {}).get("periods", [])),
                            img_base64,
                            datetime.now().isoformat(),
                        ))
        db.commit()

@app.route("/api/delete_forecast", methods=["POST"])
def delete_forecast():
    db = get_db()
    cursor = db.cursor()

    # Parse the incoming request's body as JSON and return a python dict.
    data = request.get_json()
    # Get the id associated with the delete button that the user clicked on. 
    id = data.get('id')
    print(f"Received ID: {id}") # Add this line
    print(f"Type of ID: {type(id)}") # Add this line

    if id is None:
        return jsonify({"error": "Missing forecast ID"}), 400  # Return an error response
    try:
        # Delete the forecast from database by the id
        print(f"Executing SQL: DELETE FROM forecasts WHERE id = ? with ID: {id}") # Add this line
        cursor.execute("DELETE FROM forecasts WHERE id = ?", (id,)) # Note the comma for a single-element tuple
        db.commit()

        return jsonify({"message": f"Forecast {id} deleted successfully"}), 200
    
    except Exception as e:
        db.rollback()
        # --- IMPORTANT CHANGE HERE ---
        print("An error occurred during forecast deletion:")
        traceback.print_exc() # This will print the full traceback to your server console
        # --- END IMPORTANT CHANGE ---
        return jsonify({"error": str(e)}), 500


@app.route("/api/forecast", methods=["POST"])
def get_forecast():
    db = get_db()
    cursor = db.cursor()

    # Parses the incoming request's body as JSON and returns a Python dictionary.
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    points: dict = fetchAPI_points(latitude, longitude)
    forecastdata: dict = fetchAPI_forecastdata(latitude, longitude)
    detailedForecastPlot: BytesIO = graphUrl.getDetailedForecast(latitude, longitude)
    img_base64 = encode_image_to_base64(detailedForecastPlot)

    cursor.execute('''INSERT OR REPLACE INTO forecasts (latitude, longitude, location, elevation, forecastdata_periods, detailedForecastPlot_Image, last_updated) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (
                            latitude,
                            longitude,
                            json.dumps(points.get("properties", {}).get("relativeLocation", {}).get("properties", {})),
                            json.dumps(forecastdata.get("properties", {}).get("elevation", {"unitCode": "", "value": 0})),
                            json.dumps(forecastdata.get("properties", {}).get("periods", [])),
                            img_base64,
                            datetime.now().isoformat(),
                        ))
    db.commit()
    
    cursor.execute("SELECT * FROM forecasts WHERE latitude = ? AND longitude = ?", (latitude, longitude))
    # fetchone() returns a tuple or a dict (..., ..., ...) | fetchall() returns a list of rows [(..., ..., ...), (...), (...)]
    row = cursor.fetchone()
    forecast = {
            "id" : row[0],
            "latitude" : row[1],
            "longitude" : row[2],
            "location" : json.loads(row[3]), # Convert JSON string to dict
            "elevation" : json.loads(row[4]), # Convert JSON string to dict
            "forecastdata_periods" : json.loads(row[5]), # Convert JSON string to dict
            "detailedForecastPlot_Image" : row[6],
            }
    
    return jsonify(forecast)


@app.route("/", methods=["GET", "POST"])
def index():
     # Ensure active connection is available 
    # Get a local cursor object for this request
    db = get_db()
    cursor = db.cursor()

    if request.method == "POST":

        # For now assume that the user will always input in a valid coordinate - latitude | longitude
        latitude = request.form.get('latitude', '').strip()
        longitude = request.form.get('longitude', '').strip()


        # Request the forecast data and the plot using the latitude and longitude.
        points:              dict = fetchAPI_points(latitude, longitude)
        forecastdata:        dict = fetchAPI_forecastdata(latitude, longitude)
        detailedForecastPlot: BytesIO = graphUrl.getDetailedForecast(latitude, longitude)
        img_base64 = encode_image_to_base64(detailedForecastPlot)

        # DB is setup so that lat and long is a unique composite. This will replace the entry if lat and long from POST method is the same as in the db. It will insert a new entry if lat and long is different.
        cursor.execute('''INSERT OR REPLACE INTO forecasts (latitude, longitude, location, elevation, forecastdata_periods, detailedForecastPlot_Image, last_updated) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (
                        latitude,
                        longitude,
                        json.dumps(points.get("properties", {}).get("relativeLocation", {}).get("properties", {})),
                        json.dumps(forecastdata.get("properties", {}).get("elevation", {"unitCode": "", "value": 0})),
                        json.dumps(forecastdata.get("properties", {}).get("periods", [])),
                        img_base64,
                        datetime.now().isoformat(),
                    ))
        db.commit()


    # Refresh the database.
    refresh_forecastdata()

    # Retrieve forecast entries from the database.
    cursor.execute("SELECT * FROM forecasts")
    # If db is not empty then refresh the data before building the rows.
    rows = cursor.fetchall()

    # Initiate an empty list (this will hold the list of dictionarys - forecasts from db)
    if rows:
        forecasts = []
        for row in rows:
            forecasts.append({
                "id" : row[0],
                "latitude" : row[1],
                "longitude" : row[2],
                "location" : json.loads(row[3]), # Convert JSON string to dict
                "elevation" : json.loads(row[4]), # Convert JSON string to dict
                "forecastdata_periods" : json.loads(row[5]), # Convert JSON string to dict
                "detailedForecastPlot_Image" : row[6],
                })
    else:
        forecasts = None
    
    return render_template("index.html", forecasts = forecasts)


if __name__ == '__main__':
    app.run(debug=True)

# cmd: flask run
