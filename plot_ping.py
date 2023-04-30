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

import matplotlib.dates as dates
from datetime import datetime
import plotly.graph_objects as go


def generate_plots(data, geo_lookup, country_map):
    fig = go.Figure()

    for key, value in data:
        zipped_data = [list(a) for a in zip(*value)]
        x_calculations = zipped_data[0]
        y_calculations = zipped_data[1]
        _, _, country = geo_lookup[key]

        fig.add_trace(
            go.Scatter(x=x_calculations,
                       y=y_calculations,
                       name='Probe #' + str(key) + ' (' + country + ')',
                       mode='lines+markers',
                       line=dict(color=country_map[key])))

    fig.update_layout(title="Latency Over Time of RIPE Atlas Probes",
                      xaxis_title="Time (UTC)",
                      yaxis_title="Latency",
                      font=dict(family="Courier New, monospace",
                                size=18,
                                color="Blue"))
    fig.show()


import pandas as pd
import plotly.express as px


def geo_plot(data, geo_lookup, animate=True):
    """
    Big creds to this person who helped me with the animation issue :
    https://stackoverflow.com/questions/60366358/animate-a-plotly-map-with-a-sliding-date-bar
    """
    #we create a dataframe here with cols for time, probe#, lat, lon, latency
    #it will be in the shape of a nested dict with title : {row#: data}

    time = {}
    probe = {}
    lat = {}
    lon = {}
    latency = {}

    start_index = 0

    for key, value in data:
        zipped_data = [list(a) for a in zip(*value)]
        #some sort of location look-up
        # coords = geo_lookup[key]
        # lat_temp = coords[0]
        # long_temp = coords[1]

        #probe id
        probe_ids = zipped_data[0]
        #latency
        y_calculations = zipped_data[1]

        # if len(x_calculations) != len(y_calculations):
        #     TypeError("the time and latency values are not of the same length")
        for i in range(0, len(y_calculations)):
            dict_idx = i + start_index

            probe_id = probe_ids[i]
            coords = geo_lookup[probe_id]
            lat_temp = coords[0]
            long_temp = coords[1]

            time[dict_idx] = key
            probe[dict_idx] = probe_id
            lat[dict_idx] = lat_temp
            lon[dict_idx] = long_temp
            latency[dict_idx] = y_calculations[i]
        start_index = len(y_calculations) + start_index
    #should I populate the time frames with

    df = pd.DataFrame({
        'time': time,
        'probe': probe,
        'lat': lat,
        'lon': lon,
        'latency': latency
    })
    print(df)
    if animate:
        fig = px.scatter_mapbox(df,
                                hover_name=df['probe'],
                                lat=df['lat'],
                                lon=df['lon'],
                                color=df['latency'],
                                range_color=[0, 200],
                                animation_group="probe",
                                animation_frame="time",
                                color_continuous_scale='Portland',
                                zoom=0)
        fig.update_layout(mapbox_style="carto-darkmatter",
                          mapbox_center_lon=180)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_traces(
            mode='markers',
            marker=dict(size=10),
            showlegend=False,
            hovertemplate='Latitude: %{lat}<br>Longitude: %{lon}')
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1
        fig.layout.updatemenus[0].buttons[0].args[1]["transition"][
            "duration"] = 1
        #fig.layout.coloraxis.showscale = True
        fig.layout.sliders[0].pad.t = 10
        fig.layout.updatemenus[0].pad.t = 10

    else:
        fig = px.scatter_mapbox(df,
                                hover_name=df['probe'],
                                lat=df['lat'],
                                lon=df['lon'],
                                color=df['latency'],
                                range_color=[0, 175],
                                color_continuous_scale='Portland',
                                zoom=0)
        fig.update_layout(mapbox_style="carto-darkmatter",
                          mapbox_center_lon=180)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    config = dict({'scrollZoom': True})
    fig.show(config=config)
  


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