import plotly.express as px
import streamlit as st
from apps.get_data import read_data, get_geojson, round_up
import pickle
import streamlit as st
import pandas as pd
import geopandas as gpd
from streamlit_folium import folium_static
import numpy as np

def app():
    
    st.title('1. Accidents - Yearly')
    st.write("Yearly bike accident counts between 01.01.2018 and 31.12.2020 (3 years)")

    file = open('./pickle/map_yearly_accident.pkl', 'rb')
    accidents_yearly = pickle.load(file)
    file.close()
    st.plotly_chart(accidents_yearly)

    st.write("Data Source: Amt für Statistik Berlin-Brandenburg")
    df = pd.DataFrame(np.array(
        [[8459, 8384, 6701],
        [5192, 5005, 5109]]),
        columns=['2018', '2019', '2020'])
    df.rename(index={0:'Traffic accident without bike', 1:'Traffic accident with bike'}, inplace=True)
    st.table(df)

###############
    st.title('1. Accidents - Hourly')
    st.write("Animated hourly bike accidents between 01.01.2018 and 31.12.2020 (3 years)")

#    file = open('./pickle/map_hourly_accident.pkl', 'rb')
#    object_file = pickle.load(file)
#    file.close()
#    st.plotly_chart(object_file)

    df_accident_hour = read_data('./data/accident_animation_min.csv')
    df_accident_hour = round_up(df_accident_hour, 3)
    df_accident_hour['hour'] = df_accident_hour['hour'].astype('int16')

    labels = {'value': 'Relative % (avg. = 0)', 'avg':'% of bikes', 'theft_count':'count', 'hourly_accident':'Relative % (min. = 0)'}

    fig = px.choropleth_mapbox(df_accident_hour, geojson=get_geojson(1),
                               featureidkey='PLR_ID', locations='PLR_ID',
                               color='hourly_accident',
                               range_color = [0, 500],
                               animation_frame="hour",
                               color_continuous_midpoint = 0,
                               hover_name='PLR_NAME',
                               color_continuous_scale="OrRd",
                               mapbox_style="open-street-map",
                               zoom=9, opacity=0.8,
                               center={'lat': 52.52, 'lon': 13.405},
                               labels=labels,
                              )
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

    st.write("- Relative ratio of bike accidents in each area")
    st.write("- 100 = average, 0 = zero accident")
    st.write("Data Source: Amt für Statistik Berlin-Brandenburg")
###############
    st.title('2 Locations - Area')
    st.write("Sharing bike locations by area between 24.02.2022 and 09.03.2022 (14 days)")

    file = open('./pickle/map_avg_location.pkl', 'rb')
    object_file = pickle.load(file)
    file.close()
    st.plotly_chart(object_file)

    st.write("- Total number of available NextBike (approx. 2200 bikes) over the period")
    st.write("Data Source: NextBike live location API")    

###############
    st.title('2 Locations - Hourly')
    st.write("Animated hourly sharing bike loactions between 24.02.2022 - 09.03.2022 (14 days)")


    df_hour_mean = read_data('./data/nextbike_location_animation_mean.csv')
    df_hour_mean = round_up(df_hour_mean, 3)
    df_hour_mean['hour'] = df_hour_mean['hour'].astype('int16')

    labels = {'value': 'Relative % (avg. = 0)', 'avg':'% of bikes', 'theft_count':'count', 'hourly_accident':'Relative % (min. = 0)'}

    fig = px.choropleth_mapbox(df_hour_mean, geojson=get_geojson(0),
                               featureidkey='PLR_ID', locations='PLR_ID',
                               color='value',
                               range_color = [-0.5, 0.5],
                               animation_frame="hour",
                               color_continuous_midpoint = 0,
                               hover_name='PLR_NAME',
                               color_continuous_scale="RdBu_r",
                               mapbox_style="open-street-map",
                               zoom=10, opacity=0.8,
                               center={'lat': 52.52, 'lon': 13.405},
                               labels=labels,
                              )
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

    st.write("- Relative ratio of parked NextBike in each area")
    st.write("- 0 = average number of NextBike")
    st.write("Data Source: NextBike live location API")
    
