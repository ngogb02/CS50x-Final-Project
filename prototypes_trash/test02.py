import plotly.graph_objects as go

# Your timeline list
# timeline_list = ['11PM-1', '12AM-2', '6AM-3', '12PM-4', '6PM-5', '12AM-6', '6AM-7', '12PM-8',
#                  '6PM-9', '12AM', '6AM', '12PM', '6PM', '12AM', '6AM', '12PM',
#                  '6PM', '12AM', '6AM', '12PM', '6PM', '12AM', '6AM', '12PM',
#                  '6PM', '12AM', '6AM', '12PM', '6PM']

timeline_list = [
    '11PM-1', '12AM-2', '6AM-3', '12PM-4', '6PM-5', '12AM-6', '6AM-7', '12PM-8',
    '6PM-9', '12AM-10', '6AM-11', '12PM-12', '6PM-13', '12AM-14', '6AM-15', '12PM-16',
    '6PM-17', '12AM-18', '6AM-19', '12PM-20', '6PM-21', '12AM-22', '6AM-23', '12PM-24',
    '6PM-25', '12AM-26', '6AM-27', '12PM-28', '6PM-29'
]

# Example data for plotting
data_values = [10, 15, 20, 25, 30, 12, 18, 22, 28, 14, 19, 24, 29, 13, 17, 23, 27, 
               11, 16, 21, 26, 10, 15, 20, 25, 30, 14, 19, 24]

# Create the figure
fig = go.Figure()

# Add a line plot with the custom x-axis
fig.add_trace(go.Scatter(x=timeline_list, y=data_values, mode='lines+markers'))

# Set x-axis as categorical
fig.update_layout(
    xaxis=dict(type='category', title='Timeline'),
    yaxis=dict(title='Values'),
    title='Custom Timeline Plot'
)

# Show the plot
fig.show()
