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


def app():
    st.title('Bike Theft 2')
    st.write("Bike theft Time Series - Machine Leaerning model")
