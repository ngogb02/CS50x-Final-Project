from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
from flask import Flask, render_template
import requests

# Configure application 
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# app.config['SECRET_KEY'] = 'your_secret_key'
# app.debug = True
# toolbar = DebugToolbarExtension(app)

# Utility function (not connected to a route)
def fetchAPI_points() -> dict:
    # can modify to request user's input of lat and lon.
    latitude: float  = 47.402094608175815
    longitude: float = -121.41549110412599
    fetch_url_points: str = f"https://api.weather.gov/points/{latitude},{longitude}"
    response = requests.get(fetch_url_points)

    if response.status_code == 200:
        points_json = response.json()
        return points_json
    
    else:
        print(f"Failed to retrieve data: {response.status_code}")

def fetchAPI_forecastdata() -> dict:

    points_json = fetchAPI_points()
    response = requests.get(points_json["properties"]["forecast"])

    if response.status_code == 200:
        forecastdata_json = response.json()
        return forecastdata_json
    
    else:
        print(f"fetchAPI_forecastdata failed to retrieve data: {response.status_code}")

def fetchAPI_forecastGridData() -> dict:
    points_json = fetchAPI_points()

    response = requests.get(points_json["properties"]["forecastGridData"])

    if response.status_code == 200:
        forecastGridData_json = response.json()

        return forecastGridData_json
    else:
        print(f"fetchAPI_forecashhourlydata failed to retrieve data: {response.status_code}")

# Custom Jinja filler to reformat ISOtime to 12hr PM/AM time
@app.template_filter('ISO_time_reformat')
def format_time(iso_time: str):
    datetime_obj = datetime.fromisoformat(iso_time)
    # Return only hour and AM/PM - ex: 12PM, 6AM, etc... 
    return datetime_obj.strftime('%I%p').lstrip('0')

@app.template_filter('meter_to_feet')
def format_elevation(meter):
    feet = meter * 3.28084
    return int(feet)
    

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    points:            dict = fetchAPI_points()
    forecastdata:      dict = fetchAPI_forecastdata()
    forecastgrid_data: dict = fetchAPI_forecastGridData()

    return render_template("index.html", 
                           forecastdata_periods = forecastdata["properties"]["periods"], 
                           elevation            = forecastdata["properties"]["elevation"], 
                           location             = points["properties"]["relativeLocation"]["properties"]
                           )

if __name__ == '__main__':
    app.run(debug=True)
