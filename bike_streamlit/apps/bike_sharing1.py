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


from data.get_data import read_data, get_geojson


def app():
    st.cache
    st.title('Bike Sharing 1')
    st.write("Bike sharing by area")


    #st.title("Hello world!")  # add a title
    #st.write(df_location)  # visualize my dataframe in the Streamlit app
    #tester
    #df = pd.read_csv("./data/accident_counts.csv")  # read a CSV file inside the 'data" folder next to 'app.py'
    # df = pd.read_excel(...)  # will work for Excel files

    #Parameters
    df_location = read_data('./data/nextbike_location_change_mean.csv')
    geojson = get_geojson(0)
    color = 'avg'
    df = df_location
    max_val = df_location['avg'].max()

    #Plotting template
    labels = {'value': 'Relative % (Avg. = 0)', 'avg':'% of bikes', 'theft_count':'count'}
    fig = px.choropleth_mapbox(df, geojson=geojson,
                            featureidkey='PLR_ID', locations='PLR_ID',
                            color=color,
                            range_color = [0, max_val],
                            color_continuous_midpoint = 0,
                            hover_name='PLR_NAME',
                            color_continuous_scale="OrRd",
                            mapbox_style="open-street-map",
                            zoom=10, opacity=0.6,
                            center={'lat': 52.52, 'lon': 13.405},
                            labels=labels,
                            )
    fig.update_layout(title='NextBike Average Distribution')
    #fig.show()
    st.plotly_chart(fig)
