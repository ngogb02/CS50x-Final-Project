from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for
from io import BytesIO
from dotenv import load_dotenv
import requests
import graphUrl 
import base64
import os
import secrets

# Configure application 
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# python -c "import secrets; print(secrets.token_hex(16))"
load_dotenv()
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# app.config['SECRET_KEY'] = 'your_secret_key'
# app.debug = True
# toolbar = DebugToolbarExtension(app)

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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # For now assume that the user will always input in a valid coordinate - latitude | longitude
        latitude = float(request.form.get('latitude', '').strip())
        longitude = float(request.form.get('longitude', '').strip())


        # Request the forecast data and the plot using the latitude and longitude.
        points:              dict = fetchAPI_points(latitude, longitude)
        forecastdata:        dict = fetchAPI_forecastdata(latitude, longitude)
        detailedForecastPlot: BytesIO = graphUrl.getDetailedForecast(latitude, longitude)
        img_base64 = encode_image_to_base64(detailedForecastPlot)

        
        # Build a forecast dictionary.
        forecast = {
            "latitude" : latitude,
            "longitude": longitude,
            "forecastdata_periods" : forecastdata.get("properties", {}).get("periods", []),
            "elevation" : forecastdata.get("properties", {}).get("elevation", {"unitCode": "", "value": 0}),
            "location" : points.get("properties, {}").get("relativeLocation", {}).get("properties", {}),
            "detailedForecastPlot" : img_base64,
        }

        # Append the forecast dictionary to the session-stored list
        # Check if there's already a list of forecasts stored in the session. If not, create an empty list.
        # Update the session with the latest forecast after appending the new forecast.
        forecasts: list = session.get("forecasts", [])
        forecasts.append(forecast)
        session["forecasts"] = forecasts

        # Redirect to GET to display the forecast[s].
        return redirect(url_for("index"))
    
    forecasts = session.get("forecasts", [])
    return render_template("index.html", forecasts=forecasts)


if __name__ == '__main__':
    app.run(debug=True)

# cmd: flask run
