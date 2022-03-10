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
from data.get_data import read_data, get_geojson, round_up

def app():
    st.title('Bike Sharing 2')
    st.write("Bike sharing animation")
    labels = {'value': 'Relative % (Avg. = 0)', 'avg':'% of bikes', 'theft_count':'count'}


    df_hour_mean = read_data('./data/nextbike_location_animation_mean.csv')
    df_hour_mean = round_up(df_hour_mean, 3)

    geojson = get_geojson(0)
    color = 'value'
    df = df_hour_mean

    #Plotting template
    fig = px.choropleth_mapbox(df, geojson=geojson,
                            featureidkey='PLR_ID', locations='PLR_ID',
                            color=color,
                            range_color = [-0.5, 0.5],
                            animation_frame="hour",
                            color_continuous_midpoint = 0,
                            hover_name='PLR_NAME',
                            color_continuous_scale="Edge",
                            mapbox_style="open-street-map",
                            zoom=10, opacity=0.6,
                            center={'lat': 52.52, 'lon': 13.405},
                            labels=labels,
                            )
    fig.update_layout(title='NextBike Dynamic Distribution')
    st.plotly_chart(fig)
