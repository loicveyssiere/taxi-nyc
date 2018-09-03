import pandas as pd # pip install pandas
import numpy as np

# Rendering
import matplotlib # pip install matplotlib
import matplotlib.pyplot as plt

import plotly # pip install plotly
import plotly.graph_objs as go
plotly.offline.init_notebook_mode(connected=True)

import folium # pip install folium
from folium import plugins

import ipywidgets as widgets

def load_and_clean(data_file, fare_file, nrows=None):
    types={'hack_license': str, 'hack_license': str, 'pickup_datetime': str}
    indexes = ['medallion', 'hack_license', 'vendor_id', 'pickup_datetime']
    data = pd.read_csv(data_file, nrows=nrows, dtype=types, parse_dates=["pickup_datetime", "dropoff_datetime"]) \
        .rename(columns=lambda x: x.strip()).set_index(indexes)
    fare = pd.read_csv(fare_file, nrows=nrows, dtype=types, parse_dates=[" pickup_datetime"]) \
        .rename(columns=lambda x: x.strip()).set_index(indexes)

    if (data.index.is_unique and fare.index.is_unique):
        print("The indexing is unique, the join operation is possible")
        full = data.join(fare, how="inner", lsuffix="_left", rsuffix="_right")
        for i, v in enumerate(indexes):
            full[v] = full.index.get_level_values(v)
        print("Data loading and cleaning completed")
        return full
    else:
        return None

def plot_time_series(low, high, low_label="LOW", high_label="HIGH", title="Time Series"):
    trace_high = go.Scatter(
    x=high.index,
    y=high,
    name = high_label,
    line = dict(color = '#17BECF'),
    opacity = 0.8)

    trace_low = go.Scatter(
        x=low.index,
        y=low,
        name = low_label,
        line = dict(color = '#7F7F7F'),
        opacity = 0.8)

    data = [trace_high,trace_low]

    layout = dict(
        title=title,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='day',
                         step='day',
                         stepmode='backward'),
                    dict(count=7,
                         label='week',
                         step='day',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible = True
            ),
            type='date'
        )
    )

    fig = dict(data=data, layout=layout)
    plotly.offline.iplot(fig, filename=title)

def resample_on_subset(full, subset, resampling, function):
    col = subset.copy()
    col.append("pickup_datetime")
    return full[col].reset_index(drop=True).set_index(["pickup_datetime"]).resample(resampling).apply(function)

def heatmap(df, lat_col='latitude', lon_col='longitude', zoom_start=11, \
                heat_map_weights_col=None, \
                heat_map_weights_normalize=True, heat_map_radius=15):

    ## center map in the middle of points center in
    middle_lat = df[lat_col].median()
    middle_lon = df[lon_col].median()

    curr_map = folium.Map(location=[middle_lat, middle_lon],
                          zoom_start=zoom_start)

    # convert to (n, 2) or (n, 3) matrix format
    if heat_map_weights_col is None:
        cols_to_pull = [lat_col, lon_col]
    else:
        cols_to_pull = [lat_col, lon_col, heat_map_weights_col]

    stations = df[cols_to_pull].values
    curr_map.add_child(plugins.HeatMap(stations, radius=heat_map_radius))

    return curr_map

def scatter_on_groups_2D(groups, x_selection, y_selection, group_names=None):
    i = 0
    data = []
    for name, group in groups:
        if (group_names != None):
            display_name = group_names[i]
        else:
            display_name = name
        data.append(go.Scatter(
            x = group[x_selection],
            y = group[y_selection],
            mode = 'markers',
            name = display_name,
            hoverinfo='none'
        ))
        i+=1

    layout = go.Layout(
        xaxis= dict(
            title= x_selection,
            ticklen= 5,
            zeroline= False,
            gridwidth= 2,
        ),
        yaxis=dict(
            title= y_selection,
            ticklen= 5,
            gridwidth= 2,
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.iplot(fig, filename='basic-scatter')

def scatter_on_groups_3D(groups, x_selection, y_selection, z_selection, group_names=None):
    data = []
    i = 0
    for name, group in groups:
        if (group_names != None):
            display_name = group_names[i]
        else:
            display_name = name
        data.append(go.Scatter3d(
            x=group[x_selection],
            y=group[y_selection],
            z=group[z_selection],
            mode='markers',
            name=display_name,
            hoverinfo='none',
            marker=dict(
                size=5,
                opacity=0.5
            )
        ))
        i+=1

    layout = go.Layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=20
        ), 
        scene = dict(
        xaxis = dict(
            title=x_selection),
        yaxis = dict(
            title=y_selection),
        zaxis = dict(
            title=z_selection),),
    )
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.iplot(fig, filename='simple-3d-scatter')