import matplotlib.dates as dates
from datetime import datetime
import plotly.graph_objects as go
from probe_dashboard import create_dash_page
import requests
import flag
import pycountry
import dash
from dash.exceptions import PreventUpdate
from dash import dcc, html
from dash.dependencies import Input, Output
import webbrowser

prefix = 'https://atlas.ripe.net/api/v2/'
app = dash.Dash(__name__)

def make_figure(data, probes, latency_type):
  print("\n\n ~~ PLOTTING " + latency_type.upper() + " LATENCY ~~ \n")
  fig = go.Figure()
  sorted_data = {key:data[key] for key in sorted(data.keys())}

  for key,value in sorted_data.items():
    zipped_data = [list(a) for a in zip(*value)]
    x_calculations = zipped_data[0]
    y_calculations = zipped_data[1]
    l = len(x_calculations)
    probe = probes[key]
    urls = ['https://atlas.ripe.net/probes/' + str(key) +'/' for i in range(l)]
    print("PLOTTING Probe ID " + str(probe['id']))
    if probe['asn_v4'] == 14593 or probe['asn_v6'] == 14593:
      fig.add_trace(go.Scatter(
        x=x_calculations,
        y=y_calculations,
        name='Probe #'+str(key), 
        mode='lines+markers', 
        hovertemplate=
        '<b>' + latency_type.capitalize()+' Latency</b>: %{y:.2f} ms'+
        '<br><b>Time</b>: %{x} UTC<br>'+
        '%{text}<extra></extra>',
        text = ['<b>Probe ID</b>: ' + str(probe['id']) + '<br><b>Description</b>: ' + str(probe['description']) + '<br><b>Country</b>: '+ pycountry.countries.get(alpha_2=probe['country_code']).name + ' ' + str(flag.flag(probe['country_code'])) + "<br> <b>CLICK POINT FOR MORE INFO</b>" for i in range(l)],
        customdata= urls
        ))
    else:
      print("SKIPPING Probe ID " + str(probe['id']) + " with ASN ID of " + str(probe['asn_v4']) +'/' +str(probe['asn_v6']))

  fig.update_layout(
    title=latency_type.capitalize() + " Latency Over Time of RIPE Atlas Starlink Probes",
    xaxis_title="Time (UTC)",
    yaxis_title=latency_type.capitalize() + " Latency (ms)",
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
  fig.update_traces(
    marker={'size':10}
  )
  return fig

def generate_plots(data_sets):
  avg_data = data_sets[0]
  min_data = data_sets[1]
  max_data = data_sets[2]

  probes = {}
  print("\n\n ~~ FETCHING PROBE INFO ~~ \n")
  for key,value in avg_data.items():
    print("FETCHING info for Probe ID " + str(key))
    probes[key] = requests.get(prefix + '/probes/' + str(key)).json()
  
  avg_fig = make_figure(avg_data, probes, "average")
  min_fig = make_figure(min_data, probes, "minimum")
  max_fig = make_figure(max_data, probes, "maximum")

  

  app.layout = html.Div(
    [
      dcc.Graph(
        id="avg-graph",
        style={'width': '90vw', 'height': '90vh'},
        figure=avg_fig
      ),
      dcc.Graph(
        id="min-graph",
        style={'width': '90vw', 'height': '90vh'},
        figure=min_fig
      ),
      dcc.Graph(
        id="max-graph",
        style={'width': '90vw', 'height': '90vh'},
        figure=max_fig
      ),
    ]
  )

  app.run()

@app.callback(
  Output('avg-graph', 'figure'), 
  [Input('avg-graph', 'clickData')])
def avg_open_url(clickData):
  if clickData != None:
    url = clickData['points'][0]['customdata']
    webbrowser.open_new_tab(url)
  else:
    raise PreventUpdate

@app.callback(
  Output('min-graph', 'figure'), 
  [Input('min-graph', 'clickData')])
def min_open_url(clickData):
  if clickData != None:
    url = clickData['points'][0]['customdata']
    webbrowser.open_new_tab(url)
  else:
    raise PreventUpdate

@app.callback(
  Output('max-graph', 'figure'), 
  [Input('max-graph', 'clickData')])
def max_open_url(clickData):
  if clickData != None:
    url = clickData['points'][0]['customdata']
    webbrowser.open_new_tab(url)
  else:
    raise PreventUpdate