import requests
from dateutil.parser import parse
from app import format_time
# import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


# def fetchAPI_points() -> dict:
#     # can modify to request user's input of lat and lon.
#     latitude: float  = 47.402094608175815
#     longitude: float = -121.41549110412599
#     fetch_url_points: str = f"https://api.weather.gov/points/{latitude},{longitude}"

#     response = requests.get(fetch_url_points)
#     print(f"fetchAPI_points response: {response}")

#     if response.status_code == 200:
#         points_json = response.json()

#         return points_json
#     else:
#         print(f"Failed to retrieve data: {response.status_code}")

# def fetchAPI_forecastGridData() -> dict:

#     points_json = fetchAPI_points()

#     response = requests.get(points_json["properties"]["forecastGridData"])

#     if response.status_code == 200:
#         forecastGridData_json = response.json()

#         return forecastGridData_json
#     else:
#         print(f"fetchAPI_forecashhourlydata failed to retrieve data: {response.status_code}")

# forecastGridData_json = fetchAPI_forecastGridData()

# snowfallAmount_json = forecastGridData_json["properties"]["snowfallAmount"]

# snowfallAmount_json["values"][0]

# # print(snowfallAmount_json["values"][0])

# # print(snowfallAmount_json["values"][0]["validTime"])

# timeline_list = []
# snowfall_list = []

# for item in snowfallAmount_json["values"]:
#     for key, value in item.items():
#         # print(f"key: {key}")
#         # print(f"value: {value}")
#         if key == 'validTime':
#             timeStart, timeEnd = value.split("/")
#             # print(f"timeStart: {timeStart}")
#             # print(f"timeEnd: {timeEnd}")

#             parsed_timeStart = parse(timeStart)
#             # print(f"partsed_timeStart: {format_time(str(parsed_timeStart))}")

#             formatted_parsed_timeStart = format_time(str(parsed_timeStart))
            
#             timeline_list.append(formatted_parsed_timeStart)
#         else:
#             snowfall_list.append(value)

# print(timeline_list)
# print(snowfall_list)
# print(len(timeline_list))
# print(len(snowfall_list))

data= { 
    'timeline_list' : ['11PM', '12AM', '6AM', '12PM', '6PM', '12AM', '6AM', '12PM', '6PM', '12AM', '6AM', '12PM', '6PM', '12AM', '6AM', '12PM', '6PM', '12AM', '6AM', '12PM', '6PM', '12AM', '6AM', '12PM', '6PM', '12AM', '6AM', '12PM', '6PM'],
    'snowfall_list' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20.320000302791623, 20.320000302791623, 0, 2.540000037849048, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}

# Convert to a DataFrame (optional, enhances readability)
df = pd.DataFrame(data)

# Create a bar chart using Plotly Express
fig = px.bar(df, x='timeline_list', y='snowfall_list',
             title='Snowfall Over Time',
             labels={'Timeline': 'Time', 'Snowfall': 'Snowfall (cm)'},
             text='snowfall_list')  # Adds labels to the bars

# Show the plot
fig.show()



        
        
        





            
                    





