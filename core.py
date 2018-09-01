import pandas as pd # pip install pandas
import numpy as np

# Rendering
%matplotlib inline
import matplotlib # pip install matplotlib
import matplotlib.pyplot as plt

import plotly # pip install plotly
import plotly.graph_objs as go
plotly.offline.init_notebook_mode(connected=True)

import folium # pip install folium
from folium import plugins

import ipywidgets as widgets
from datetime import datetime
from IPython.display import display

def load_and_clean(data_file, fare_file):
    types={'hack_license': str, 'hack_license': str, 'pickup_datetime': str}
    indexes = ['medallion', 'hack_license', 'vendor_id', 'pickup_datetime']
    data = pd.read_csv(data_file, nrows=nrows, dtype=types, parse_dates=["pickup_datetime", "dropoff_datetime"]) \
        .rename(columns=lambda x: x.strip()).set_index(indexes)
    fare = pd.read_csv(fare_file, nrows=nrows, dtype=types, parse_dates=[" pickup_datetime"]) \
        .rename(columns=lambda x: x.strip()).set_index(indexes)

    print(data.index.is_unique)
    print(fare.index.is_unique)

    full = data.join(fare, how="inner", lsuffix="_left", rsuffix="_right")