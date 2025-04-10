import plotly.graph_objects as go
from datetime import datetime, timedelta

# Your data
timeline_list = ['11PM', '12AM', '6AM', '12PM', '6PM', '12AM', '6AM', '12PM',
                 '6PM', '12AM', '6AM', '12PM', '6PM', '12AM', '6AM', '12PM',
                 '6PM', '12AM', '6AM', '12PM', '6PM', '12AM', '6AM', '12PM',
                 '6PM', '12AM', '6AM', '12PM', '6PM']
snowfall_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20.320000302791623, 20.320000302791623,
                 0, 2.540000037849048, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

print(snowfall_list)
print(len(snowfall_list))

new_snowfall_list = [value / 6 for value in snowfall_list for _ in range(6)]
print(new_snowfall_list)
print(len(new_snowfall_list))

# Starting time from your original timeline_list (e.g., "11PM")
start_time = timeline_list[0]
# Convert the starting time to a datetime object.
# "%I%p" specifies hour (12-hour clock) and the AM/PM marker.
start_dt = datetime.strptime(start_time, "%I%p")

# Define the desired length for the new timeline list.
desired_length = 174

# Generate the new timeline list by adding 1 hour per iteration.
new_timeline_list = []
for i in range(desired_length):
    # Format the time string. We use lstrip("0") to remove any leading zero.
    formatted_time = start_dt.strftime("%I%p").lstrip("0")
    new_timeline_list.append(formatted_time)
    # Increment the datetime object by 1 hour.
    start_dt += timedelta(hours=1)

print(new_timeline_list)
print(len(new_timeline_list))

# Create numeric indices for the x-axis
x_indices = list(range(len(new_timeline_list)))

# Create the bar chart with numeric x-values
fig = go.Figure(
    data=go.Bar(
        x=x_indices,
        y=new_snowfall_list,
        text=new_snowfall_list,
        textposition='auto',
        marker_color='lightsalmon'
    )
)

# Update layout to force every tick to show and to “zoom out” the x-axis
fig.update_layout(
    title="Snowfall Forecast",
    xaxis=dict(
        title='Time',
        tickmode='array',                 # Use an explicit list of tick positions
        tickvals=x_indices,               # A tick at every numeric index
        ticktext=new_timeline_list,           # Replace numeric ticks with your time labels
        range=[-0.5, len(new_timeline_list)-0.5],  # Set the range to show every bar
        # tickangle=-45,                    # Rotate labels to help them fit
        tickfont=dict(size=7),            # Use smaller font so labels don’t crowd
        automargin=True                   # Let Plotly adjust margins as needed
    ),
    yaxis=dict(title='Snowfall (cm)'),
    width=1550,   # Increase width so all ticks are visible without panning/zooming
    height=400,
    margin=dict(l=50, r=50, t=50, b=150)
)

fig.show()
