from turtle import st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from folium.plugins import HeatMap
import config
import logging
import requests
import datetime
import glob
import geopandas
from pyproj import Proj, transform
from shapely.geometry import Point, Polygon
from streamlit as st

#Load csv files
bike_counts = pd.read_csv(f'data/bike_counts_streamlit.csv')
accident_counts = pd.read_csv(f'data/accident_counts_streamlit.csv')

#Create button to change the map
if st.button('Show Accident Counts'):
    accident_counts.explore("accident_count", legend=True, cmap = 'OrRd', scheme='fisher_jenks')
else:
    bike_counts.explore("bike_count", legend=True, cmap = 'OrRd', scheme='fisher_jenks')

if st.button('Show Bike Counts'):
    bike_counts.explore("bike_count", legend=True, cmap = 'OrRd', scheme='fisher_jenks')
else:
    accident_counts.explore("accident_count", legend=True, cmap = 'OrRd', scheme='fisher_jenks')
