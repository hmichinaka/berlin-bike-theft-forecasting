#imports
import streamlit as st
import pandas as pd
import folium
import geopandas as gpd
from streamlit_folium import folium_static
import pickle
import geopandas

def app():
    #@st.cache(suppress_st_warning=True)
    st.title('1.1 Bike Accident')
    st.write("Bike accidents by area.")
    # load dataframes
    cluster_gdf = pd.read_pickle('./raw_data/cluster_gdf.pickle')
    final_df = pd.read_pickle('./raw_data/greenlane_df.pickle')

    #grouping final_df
    completed = final_df.coordinates[final_df.status == 'completed']
    under_construction = final_df.coordinates[final_df.status == 'under construction']
    in_planning = final_df.coordinates[final_df.status == 'in planning']
    intended = final_df.coordinates[final_df.status == 'intended']

    # creating map
    m = folium.Map(location=[52.52000, 13.4050],tiles='openstreetmap', zoom_start=12)

    # adding accident clusters to map
    folium.features.GeoJson(cluster_gdf,
                            style_function= lambda x: {'fillColor': 'red', 'color': 'red'},
                            tooltip=folium.GeoJsonTooltip(fields= ['count'],aliases=["Accident count: "],labels=True)).add_to(m)

    # adding Greenlanes to map
    folium.PolyLine(locations=completed, color='green', weight=7, opacity=0.7, tooltip='completed').add_to(m)
    folium.PolyLine(locations=under_construction, color='yellow', weight=7, opacity=0.7, tooltip='under construction').add_to(m)
    folium.PolyLine(locations=in_planning, color='orange', weight=7, opacity=0.7, tooltip='in planning').add_to(m)
    folium.PolyLine(locations=intended, color='red', weight=7, opacity=0.7, tooltip='intended').add_to(m)

    # display map
    folium_static(m)
