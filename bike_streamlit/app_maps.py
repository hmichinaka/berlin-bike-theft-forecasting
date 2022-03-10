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


import config
import logging
import requests
import datetime
import glob
import shapely.wkt
import math
import folium

#_________Functions____________________

def clean_plr(df):
#After reading csv file, cleaning PLR_ID into correct str format
    df['PLR_ID'] = df['PLR_ID'].apply(int)
    df['PLR_ID'] = df['PLR_ID'].apply(lambda x: "0" + str(x) if len(str(x))== 7 else x)
    df.rename(columns={'PLR_ID':'id'}, inplace=True)
    return df

def read_data(path):
    #Read csv and clean PLR_ID
    df = pd.read_csv(path)
    df = clean_plr(df)

    #Merge it to LOR DataFrame
    _df = gdf_plr.merge(df, how='left', on="id")
    df = _df
    df.fillna(0, inplace=True)
    df.rename(columns={'PLR_ID':'id'}, inplace=True)
    return df

#Read LOR file
#path_to_daza_plr = "../raw_data/LOR_shpfiles/lor_plr.shp"
path_to_daza_plr = "data/LOR_shpfiles/lor_plr.shp"
gdf_plr = gpd.read_file(path_to_daza_plr)
gdf_plr = clean_plr(gdf_plr)

#Read CSV file
#df_location = read_data('../data/nextbike_location_change.csv')
#df_accident = read_data('../data/accident_counts.csv')
#df_theft = read_data('../data/theft_counts.csv')
df_location = read_data('data/nextbike_location_change.csv')
df_accident = read_data('data/accident_counts.csv')
df_theft = read_data('data/theft_counts.csv')


#bike_counts_path="data/bike_counts_streamlit.csv"

#UTM to WGS84 conversion in order to make GeoJSON#
#convert polygon

def read_geojson():
    #Read GeoJSON
    f = open('data/plr.geojson')
    geojson = json.load(f)
    return geojson

def get_geojson(area):
    #0: Limited area for bike sharing locaiton, 1: Full area for others
    geojson = read_geojson()
    #Inject id for mapping (somehow we need to do it after loading the geojson)

    if area == 1:
        for k in range(len(geojson['features'])):
            geojson['features'][k]['id'] = gdf_plr.iloc[k, 0]

    elif area == 0:
        for k in range(len(geojson['features'])):
            n = str(gdf_plr.iloc[k, 0])[:3]
            if  n != '032' and n != '033' and n != '034' and n != '035' and n != '042'and \
                n != '051' and n != '052' and n != '053' and n != '054' and n != '062' and \
                n != '063' and n != '064' and n != '075' and n != '076' and n != '082' and \
                n != '083' and n != '084' and n != '091' and n != '092' and n != '093' and \
                n != '094' and n != '095' and n != '115' and n != '101' and n != '102' and \
                n != '103' and n != '111' and n != '112' and n != '113' and n != '114' and \
                n != '104' and n != '121' and n != '122' and n != '124' and n != '125' and n != '126':
                geojson['features'][k]['id'] = gdf_plr.iloc[k, 0]
    else:
        return print('Failed. Please enter 0 or 1')
    return geojson
#--------------------------------------
#Intro text


'''
# Berlin Bike Accident and Theft Predictor

Our project aims to answer two specifc concerns for Berlin cyclists

1. What is the risk of my bike being stolen in Berlin, and how to to avoid it
2. Bike safety as a cyclist - which are the most dangerous roads and intersection in Berlin

How can we use Machine Learning to mitigate these risks.

Data was aquired from 3 sources
    [Nextbike](https://www.nextbike.de/en/berlin/)
    Berlin Accident Data
    Bike Theft Data

'''




#Mapping
#---------------------------------------
'''
1.1  Bike Sharing Location Distribution
---------------------------------------

'''

geojson = get_geojson(0)

#Change color= '0'-'23'/'avg'/'weekday'/'weekend'
fig = px.choropleth_mapbox(df_location, geojson=geojson, locations='id', color='7',
                           color_continuous_scale="Reds",
                           mapbox_style="open-street-map",
                           zoom=10, opacity=0.6,center={'lat': 52.52, 'lon': 13.405},
                           labels={'NextBike Distribution'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)

#-----------------------------------------------
#3.2  Bike Accident
'''
1.2  Bike Accident Location Distribution
---------------------------------------

'''

geojson = get_geojson(1)

#Change color= '2018'/'2019'/'2020'
fig = px.choropleth_mapbox(df_accident, geojson=geojson, locations='id', color='2019',
                           color_continuous_scale="Reds",
                           range_color=(0, 100),
                           mapbox_style="open-street-map",
                           zoom=10, opacity=0.6,center={'lat': 52.52, 'lon': 13.405},
                           labels={'Number of Bike Accident'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)


#-----------------------------------------------
#3.3  Bike Theft
'''
1.3 Bike Theft Location Distribution
------------------------------------------

'''

geojson = get_geojson(1)

fig = px.choropleth_mapbox(df_theft, geojson=geojson, locations='id', color='theft_count',
                           color_continuous_scale="Reds",
                           range_color=(0, 200),
                           mapbox_style="open-street-map",
                           zoom=10, opacity=0.6,center={'lat': 52.52, 'lon': 13.405},
                           labels={'Number of Bike Theft'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)
