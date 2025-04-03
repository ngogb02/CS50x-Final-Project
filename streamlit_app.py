import streamlit as st
import requests

# Utility function (not connected to a route)
def fetchAPI_points() -> dict:
    # can modify to request user's input of lat and lon.
    latitude: float  = 47.402094608175815
    longitude: float = -121.41549110412599
    fetch_url_points: str = f"https://api.weather.gov/points/{latitude},{longitude}"

    response = requests.get(fetch_url_points)
    print(f"fetchAPI_points response: {response}")

    if response.status_code == 200:
        points_json = response.json()

        return points_json
    else:
        print(f"Failed to retrieve data: {response.status_code}")

def fetchAPI_forecastdata() -> dict:
    points_json = fetchAPI_points()

    response = requests.get(points_json["properties"]["forecast"])
    print(f"fetchAPI_forecastdata response: {response}")

    if response.status_code == 200:
        forecastdata_json = response.json()

        return forecastdata_json
    else:
        print(f"fetchAPI_forecastdata failed to retrieve data: {response.status_code}")

st.title("Streamlit Debugger for Flask Data")

# Fetch and display first JSON
data1 = fetchAPI_points()
st.subheader("Points API JSON Data")
st.json(data1, expanded=False)

# Fetch and display second JSON
data2 = fetchAPI_forecastdata()
st.subheader("Forecast API JSON Data")
st.json(data2, expanded=False)

# terminal cmd: streamlit run streamlit_app.py


