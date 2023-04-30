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
