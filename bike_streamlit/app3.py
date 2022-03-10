
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import folium
from folium.plugins import HeatMap
import config
import logging
import requests
import datetime
import glob
import geopandas as gpd
from pyproj import Proj, transform
from shapely.geometry import Point, Polygon
import os
from streamlit_folium import folium_static

import shapely
from shapely import wkt
# for now use old settings
st.set_option('deprecation.showPyplotGlobalUse', False)

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


def clean_plr(df):
#After reading csv file, cleaning PLR_ID into correct str format
    df['PLR_ID'] = df['PLR_ID'].apply(int)
    df['PLR_ID'] = df['PLR_ID'].apply(lambda x: "0" + str(x) if len(str(x))== 7 else x)
    return df


def read_csv2(path):
    #Read csv and clean PLR_ID
    df = pd.read_csv(path)
    df = clean_plr(df)

    #Drop geometry column and added from shapefile
    df.drop(columns=['geometry', 'PLR_NAME'], inplace=True)

    #Merge it to LOR DataFrame
    _df = gdf_plr.merge(df, how='left', on="PLR_ID")
    df = _df
    df.fillna(0, inplace=True)
    return df

def read_csv(path):
    df = pd.read_csv(path)
    #fill
    df.fillna(0, inplace=True)
    #clean
    df['PLR_ID'] = df['PLR_ID'].apply(int)
    df['PLR_ID'] = df['PLR_ID'].apply(lambda x: "0" + str(x) if len(str(x))== 7 else x)

    return df
#@st.cache

#File paths
bike_counts_path="data/bike_counts_streamlit.csv"
bike_counts_hour_path="data/nextbike_hour.csv"
accident_counts_path="data/accident_counts_streamlit.csv"

#Read Shape files
#path_to_daza_plr = "data/LOR_shpfiles/lor_plr.shp"
#path_to_daza_plr = os.path.join("data/LOR_shpfiles/", "lor_plr.shp")
#gdf_plr = gpd.read_file(path_to_daza_plr)
#gdf_plr = clean_plr(gdf_plr)


#Read bike data
bike_counts = read_csv(bike_counts_path)
bike_counts_hour = read_csv(bike_counts_hour_path)

#Convert bike counts to geopandas
df=bike_counts
geometry = df['geometry'].map(shapely.wkt.loads)
dfa = df.drop('geometry', axis=1)
bike_counts_gpd = gpd.GeoDataFrame(dfa, crs="EPSG:4326", geometry=geometry)

#Convert bike counts hour to geopandas
df=bike_counts_hour
geometry = df['geometry'].map(shapely.wkt.loads)
dfa = df.drop('geometry', axis=1)
bike_counts_hour_gpd = gpd.GeoDataFrame(dfa, crs="EPSG:4326", geometry=geometry)


#Plot bike counts
bike_counts_gpd.plot("bike_count", legend=True, cmap = 'OrRd')
plt.show()
st.pyplot()

hr=12

st.title("Select time for bike data visualisation")
st.subheader("Choose hour or weekday/weekend")
time_options=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','weekday','weekend']
time1=st.select_slider("Choose a time", options=time_options)
st.write("you chose ", hr, ' hour')
#hr = st.slider('What time are you interested in (hr)?', 0, 23, 12)
#st.write("you chose ", hr, ' hour')

#Plot bike counts by hr

#bike_counts_hour_gpd.plot(time1, legend=True)
bike_counts_hour_gpd.plot(time1, legend=False, cmap = 'OrRd', scheme='fisher_jenks')
plt.show()
st.pyplot()

#bike_counts = read_csv('data/bike_counts_streamlit.csv')
#accident_counts2018 = read_csv('data/accident_counts2018_streamlit.csv')
#accident_counts2019 = read_csv('data/accident_counts2019_streamlit.csv')
#accident_counts2020 = read_csv('data/accident_counts2020_streamlit.csv')

#Display dataframe
#str_df = accident_counts2020.astype(str)
#st.dataframe(str_df)
#st.write(str_df.head())

#accident_counts2020.plot("accident_count", legend=True)
#gdf_ac = gpd.read_file('data/accident_counts2020_streamlit.csv')
#st.pyplot()

#accident_counts2020['geometry'] = accident_counts2020['geometry'].apply(wkt.loads)
#df1 = gpd.GeoDataFrame(accident_counts2020, geometry = 'geometry')





#Mapping based on Area of PLR using GeoplotAccessor
#accident_counts2020.plot("accident_count", legend=True);

# accidentcount explore
#accident_counts2020.explore("accident_count", legend=True, cmap = 'OrRd', scheme='fisher_jenks')
