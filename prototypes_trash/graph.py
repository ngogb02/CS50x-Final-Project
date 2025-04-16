import requests
from dateutil.parser import parse
from app import format_time
import plotly.express as px
import pandas as pd


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

def fetchAPI_forecastGridData() -> dict:

    points_json = fetchAPI_points()

    response = requests.get(points_json["properties"]["forecastGridData"])

    if response.status_code == 200:
        forecastGridData_json = response.json()

        return forecastGridData_json
    else:
        print(f"fetchAPI_forecashhourlydata failed to retrieve data: {response.status_code}")

forecastGridData_json = fetchAPI_forecastGridData()

snowfallAmount_json = forecastGridData_json["properties"]["snowfallAmount"]

print(f"1: {snowfallAmount_json["values"][0]}")
print(f"2: {snowfallAmount_json["values"][0]["validTime"]}")

timeline_list = []
timelineDate_list = []
snowfall_list = []

# Loop through snowfallAmount.values 
# Each item is a key-value, where the value is a dict that contains 2 keys and 2 values (validTime, value)
for item in snowfallAmount_json["values"]:
    for key, value in item.items():
        if key == 'validTime': #validTime = ISO-8601 Format (ex: "2025-04-14T23:00:00+00:00/PT1H")
            timeStart, timeEnd = value.split("/")
            parsed_timeStart = parse(timeStart)
            print(f"3: {parsed_timeStart}")

            # Func format_time is from app.py (self-made). Takes str iso_time format and spits out time format 12hr AM/PM str
            formatted_parsed_timeStart = format_time(str(parsed_timeStart))
            print(f"4: {format_time(str(parsed_timeStart))}")
            
            timeline_list.append(formatted_parsed_timeStart)

            timelineDate_list.append(parsed_timeStart.strftime("%#I%p-%#d"))
        else:
            snowfall_list.append(value)

# print(timeline_list)
# print(snowfall_list)
# print(len(timeline_list))
# print(len(snowfall_list))

# data= { 
#     'timeline_list' : ['11PM-1', '12AM-2', '6AM-3', '12PM-4', '6PM-5', '12AM-6', '6AM-7', '12PM-8', '6PM-9', '12AM-10', '6AM-11', '12PM-12', '6PM-13', '12AM-14', '6AM-15', '12PM-16', '6PM-17', '12AM-18', '6AM-19', '12PM-20', '6PM', '12AM', '6AM', '12PM', '6PM', '12AM', '6AM', '12PM', '6PM'],
#     'snowfall_list' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20.320000302791623, 20.320000302791623, 0, 2.540000037849048, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# }

# data = { 
#     'timeline_list': timeline_list,
#     'snowfall_list': snowfall_list,
# }


# # Convert to a DataFrame (optional, enhances readability)
# df = pd.DataFrame(data)

# # Create a bar chart using Plotly Express
# fig = px.bar(df, x='timeline_list', y='snowfall_list',
#              title='Snowfall Over Time',
#              labels={'Timeline': 'Time', 'Snowfall': 'Snowfall (cm)'},
#              text='snowfall_list')  # Adds labels to the bars

# # Show the plot
# fig.show()



        
        
        





            
                    





