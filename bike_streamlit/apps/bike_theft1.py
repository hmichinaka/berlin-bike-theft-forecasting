import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from folium.plugins import HeatMap
import geopandas as gpd
from pyproj import Proj, transform
from shapely.geometry import Point, Polygon
import json
import plotly.express as px
import streamlit as st
from data.get_data import read_data, get_geojson, round_int

def app():
    st.title('Bike Theft 1')
    st.write("Bike theft by area")
    #Parameters
    geojson = get_geojson(0)
    color = 'theft_count'
    df_theft = read_data('./data/theft_counts.csv')
    df_theft = round_int(df_theft)
    df = df_theft

    #Plotting template
    labels = {'value': 'Relative % (Avg. = 0)', 'avg':'% of bikes', 'theft_count':'count'}
    fig = px.choropleth_mapbox(df, geojson=geojson,
                            featureidkey='PLR_ID', locations='PLR_ID',
                            color=color,
                            range_color = [0, 200],
                            color_continuous_midpoint = 0,
                            hover_name='PLR_NAME',
                            color_continuous_scale="OrRd",
                            mapbox_style="open-street-map",
                            zoom=10, opacity=0.6,
                            center={'lat': 52.52, 'lon': 13.405},
                            labels=labels,
                            )
    fig.update_layout(title='Bike Theft Total Counts')
    st.plotly_chart(fig)
