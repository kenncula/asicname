import matplotlib.dates as dates
from datetime import datetime
import plotly.graph_objects as go



def generate_plots(data):
  fig = go.Figure()
  
  for key,value in data:
    zipped_data = [list(a) for a in zip(*value)]
    x_calculations = zipped_data[0]
    y_calculations = zipped_data[1]

    fig.add_trace(go.Scatter(x=x_calculations,y=y_calculations, name='Probe #'+str(key), mode='lines+markers'))

  fig.update_layout(
    title="Latency Over Time of RIPE Atlas Probes",
    xaxis_title="Time (UTC)",
    yaxis_title="Latency (ms)",
    font=dict(
      family="Courier New, monospace",
      size=18,
      color="Blue"
    )
  )
  fig.show()

