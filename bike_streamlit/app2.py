import streamlit as st
import datetime
import requests
import pandas as pd
import os
import numpy as np
#folium
from streamlit_folium import folium_static
import folium
#import geopandas
import matplotlib.pyplot as plt

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
bike_counts = pd.read_csv(f'data/bike_counts_streamlit.csv')
accident_counts = pd.read_csv(f'data/accident_counts_streamlit.csv')


##geopandas demo
#Plot geopandas example
df = pd.DataFrame(
    {'City': ['Buenos Aires', 'Brasilia', 'Santiago', 'Bogota', 'Caracas'],
     'Country': ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Venezuela'],
     'Latitude': [-34.58, -15.78, -33.45, 4.60, 10.48],
     'Longitude': [-58.66, -47.91, -70.66, -74.08, -66.86]})
gdf = geopandas.GeoDataFrame(
    df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))
st.write(gdf.head())
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
ax = world[world.continent == 'South America'].plot(
    color='white', edgecolor='black')
gdf.plot(ax=ax, color='red')
st.pyplot()

# Plotly demo

@st.cache
def get_plotly_data():

    #z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')
    #z_data = pd.read_csv('/data/mt_bruno_elevation.csv')
    z_path = os.path.join("data", "mt_bruno_elevation.csv")
    z_data = pd.read_csv(z_path)
    z = z_data.values
    sh_0, sh_1 = z.shape
    x, y = np.linspace(0, 1, sh_0), np.linspace(0, 1, sh_1)
    return x, y, z

import plotly.graph_objects as go

x, y, z = get_plotly_data()

fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
fig.update_layout(title='Mt Bruno', autosize=False, width=800, height=800, margin=dict(l=40, r=40, b=40, t=40))
'''This is a plotly demo'''
st.plotly_chart(fig)


# folium demo

m = folium.Map(location=[47, 1], zoom_start=6)

geojson_path = os.path.join("data", "departements.json")
cities_path = os.path.join("data", "lewagon_cities.csv")

for _, city in pd.read_csv(cities_path).iterrows():

    folium.Marker(
        location=[city.lat, city.lon],
        popup=city.city,
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)

def color_function(feat):
    return "red" if int(feat["properties"]["code"][:1]) < 5 else "blue"

folium.GeoJson(
    geojson_path,
    name="geojson",
    style_function=lambda feat: {
        "weight": 1,
        "color": "black",
        "opacity": 0.25,
        "fillColor": color_function(feat),
        "fillOpacity": 0.25,
    },
    highlight_function=lambda feat: {
        "fillColor": color_function(feat),
        "fillOpacity": .5,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['code', 'nom'],
        aliases=['Code', 'Name'],
        localize=True
    ),
).add_to(m)

folium_static(m)



#------------------------------------



pickup_date = st.date_input('pickup datetime', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
pickup_time = st.time_input('pickup datetime', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
pickup_datetime = f'{pickup_date} {pickup_time}'
pickup_longitude = st.number_input('pickup longitude', value=40.7614327)
pickup_latitude = st.number_input('pickup latitude', value=-73.9798156)
dropoff_longitude = st.number_input('dropoff longitude', value=40.6413111)
dropoff_latitude = st.number_input('dropoff latitude', value=-73.7803331)
passenger_count = st.number_input('passenger_count', min_value=1, max_value=8, step=1, value=1)

# enter here the address of your flask api
url = 'https://taxifare.lewagon.ai/predict'

params = dict(
    pickup_datetime=pickup_datetime,
    pickup_longitude=pickup_longitude,
    pickup_latitude=pickup_latitude,
    dropoff_longitude=dropoff_longitude,
    dropoff_latitude=dropoff_latitude,
    passenger_count=passenger_count)

response = requests.get(url, params=params)

prediction = response.json()

pred = prediction['fare']

pred
