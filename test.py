import pandas as pd
import plotly.express as px

# Provided data
timeline_list = [
  "11PM-1", "12AM-2", "6AM-2", "12PM-2", "6PM-2", 
  "12AM-3", "6AM-3", "12PM-3", "6PM-3", "12AM-4", 
  "6AM-4", "12PM-4", "6PM-4", "12AM-5", "6AM-5", 
  "12PM-5", "6PM-5", "12AM-6", "6AM-6", "12PM-6", 
  "6PM-6", "12AM-7", "6AM-7", "12PM-7", "6PM-7", 
  "12AM-8", "6AM-8", "12PM-8", "6PM-8"
]

snowfall_list = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
    20.320000302791623, 20.320000302791623,
    0, 2.540000037849048, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0
]

# Create a DataFrame with an additional column for the cleaned time labels
df = pd.DataFrame({
    "Timeline": timeline_list,
    "Snowfall": snowfall_list
})
# Create custom labels that only include the time, stripping the "-#"
df["TimeOnly"] = df["Timeline"].apply(lambda x: x.split('-')[0])

# Create the Plotly Express line chart
fig = px.line(df, x="Timeline", y="Snowfall", title="Snowfall Timeline", markers=True)

# Update the x-axis:
# - Use the original "Timeline" values for positioning (tickvals)
# - Use the cleaned labels ("TimeOnly") for display (ticktext)
fig.update_xaxes(
    tickmode='array',
    tickvals=df["Timeline"],
    ticktext=df["TimeOnly"]
)

# Display the plot
fig.show()
