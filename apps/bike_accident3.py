import streamlit as st
import pandas as pd
import folium
import geopandas as gpd
from streamlit_folium import folium_static
import pickle

def app():
    st.title('1. Accidents - Clusters')
    st.write("Cluster analysis over the bike accidents between 01.01.2018 and 31.12.2020 (3 years).")

    # load dataframes
#    cluster_gdf = pd.read_pickle('./pickle/cluster_gdf.pickle')
#    final_df = pd.read_pickle('./pickle/greenlane_df.pickle')

    file1 = open('./pickle/cluster_gdf.pickle', 'rb')
    cluster_gdf = pickle.load(file1)
    file1.close()

    file2 = open('./pickle/greenlane_df.pickle', 'rb')
    cluster_gdf = pickle.load(file2)
    file2.close()
    
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
