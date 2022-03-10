#imports
import streamlit as st
import pandas as pd
import geopandas as gpd
from streamlit_folium import folium_static
import pickle
import numpy as np

def app():
    st.title('1. Accidents - Yearly')
    st.markdown("#### Yearly bike accident counts between 01.01.2018 and 31.12.2020")

    file = open('./pickle/map_yearly_accident.pkl', 'rb')
    accidents_yearly = pickle.load(file)
    file.close()
    st.plotly_chart(accidents_yearly)

    st.markdown("#### Bike accidents in Berlin by year")
    df = pd.DataFrame(np.array(
        [["8,459", "8,384", "6,701"],
        ["5,192", "5,005", "5,109"]]),
        columns=['2018', '2019', '2020'])
    df.rename(index={0:'Traffic accident without bike', 1:'Traffic accident with bike'}, inplace=True)
    st.table(df)

#    #@st.cache(suppress_st_warning=True)
#    st.title('1 Accidents by Area')
#    st.write("Bike accidents by area.")
#    # load dataframes
#    cluster_gdf = pd.read_pickle('./raw_data/cluster_gdf.pickle')
#    final_df = pd.read_pickle('./raw_data/greenlane_df.pickle')
#
#    #grouping final_df
#    completed = final_df.coordinates[final_df.status == 'completed']
#    under_construction = final_df.coordinates[final_df.status == 'under construction']
#    in_planning = final_df.coordinates[final_df.status == 'in planning']
#    intended = final_df.coordinates[final_df.status == 'intended']
#
#    # creating map
#    m = folium.Map(location=[52.52000, 13.4050],tiles='openstreetmap', zoom_start=12)
#
#    # adding accident clusters to map
#    folium.features.GeoJson(cluster_gdf,
#                            style_function= lambda x: {'fillColor': 'red', 'color': 'red'},
#                            tooltip=folium.GeoJsonTooltip(fields= ['count'],aliases=["Accident count: "],labels=True)).add_to(m)
#
#    # adding Greenlanes to map
#    folium.PolyLine(locations=completed, color='green', weight=7, opacity=0.7, tooltip='completed').add_to(m)
#    folium.PolyLine(locations=under_construction, color='yellow', weight=7, opacity=0.7, tooltip='under construction').add_to(m)
#    folium.PolyLine(locations=in_planning, color='orange', weight=7, opacity=0.7, tooltip='in planning').add_to(m)
#    folium.PolyLine(locations=intended, color='red', weight=7, opacity=0.7, tooltip='intended').add_to(m)
#
#    # display map
#    folium_static(m)
#
