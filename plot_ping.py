import matplotlib.dates as dates
from datetime import datetime
import plotly.graph_objects as go
from probe_dashboard import create_dash_page
import requests
import flag
import pycountry

prefix = 'https://atlas.ripe.net/api/v2/'

def generate_plots(data):
  fig = go.Figure()
  sorted_data = {key:data[key] for key in sorted(data.keys())}

  for key,value in sorted_data.items():
    zipped_data = [list(a) for a in zip(*value)]
    x_calculations = zipped_data[0]
    y_calculations = zipped_data[1]
    l = len(x_calculations)
    probe = requests.get(prefix + '/probes/' + str(key)).json()
    print("PLOTTING Probe ID " + str(probe['id']))
    if probe['asn_v4'] == 14593 or probe['asn_v6'] == 14593:
      fig.add_trace(go.Scatter(
        x=x_calculations,
        y=y_calculations,
        name='Probe #'+str(key), 
        mode='lines+markers', 
        hovertemplate=
        '<b>Latency</b>: %{y:.2f} ms'+
        '<br><b>Time</b>: %{x} UTC<br>'+
        '%{text}<extra></extra>',
        text = ['<b>Probe ID</b>: ' + str(probe['id']) + '<br><b>Description</b>: ' + str(probe['description']) + '<br><b>Country</b>: '+ pycountry.countries.get(alpha_2=probe['country_code']).name + ' ' + str(flag.flag(probe['country_code'])) for i in range(l)]
        ))
    else:
      print("SKIPPING Probe ID " + str(probe['id']) + " with ASN ID of " + str(probe['asn_v4']) +'/' +str(probe['asn_v6']))

  fig.update_layout(
    title="Latency Over Time of RIPE Atlas Starlink Probes",
    xaxis_title="Time (UTC)",
    yaxis_title="Latency (ms)",
    font=dict(
      family="Courier New, monospace",
      size=18,
      color="Blue"
    ),
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    )
  )
  fig.show()

