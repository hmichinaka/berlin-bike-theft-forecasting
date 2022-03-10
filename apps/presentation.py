import plotly.express as px
import streamlit as st
from apps.get_data import read_data, get_geojson, round_up
import pickle
import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
from streamlit_folium import folium_static
from dataclasses import dataclass
from apps.predict import pred_ts_chart, prediction_by_Bezirk, predict_next_day
import json


def app():
#####HOME######
    st.title("cycle_safe(berlin) - helping to keep you and your bike safe")

    st.write("We offers you the following information in the visualized dashboard:")
    st.write("- Bike Traffic: Check out our mobility map when people use Bike Sharing service from 3 mil. of data points ")    
    #bike distribution and mobility throout a day
    st.write("- Bike Accident: Check our cluster analysis for the places where accidents happen often")    
    st.write("- Bike Theft: Experimental Bike Theft Forecasting by using a neural network model")    
    
#    st.write("How can we use Machine Learning to mitigate")
#    st.write("1. Bike theft risk")
#    st.write("2. Bike accident risk")
    st.image("./images/BikeTheft.jpg")

    st.markdown("### The Team")
    st.image("./images/team.jpg")

    st.write("Hitoshi Michinaka [Linkedin](https://www.linkedin.com/in/hmichinaka/)")
    st.write("Dominik Abratanski [Linkedin](https://www.linkedin.com/in/dominikabratanski/)")
    st.write("Lukas Hartung [Linkedin](https://www.linkedin.com/in/lukas-h-0438578b/)")
    st.write("Marlon Deus [Linkedin](https://www.linkedin.com/in/marlon-deus-0a37031b4/)")
    st.write("Paul Roberts [Linkedin](https://www.linkedin.com/in/paul-roberts-871a6790/)")
    st.write("Jakob Hohenstein [Linkedin](https://www.linkedin.com/in/jakob-hohenstein-53667914a/)")
#################  
    st.title('1.1 Locations - Area')
    st.write("Sharing bike locations by area between 24.02.2022 and 09.03.2022 (14 days)")

    file = open('./pickle/map_avg_location.pkl', 'rb')
    object_file = pickle.load(file)
    file.close()
    st.plotly_chart(object_file)

    st.write("- Total number of available NextBike (approx. 2200 bikes) over the period")
    st.write("Data Source: NextBike live location API")    

###############
    st.title('1.2 Locations - Hourly')
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
    
###################
    st.title('2.1 Accidents - Yearly')
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
    st.title('2.2 Accidents - Hourly')
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
#################
    st.title('3.1 Thefts - Area')
    st.write("Total bike theft counts by area between 01.01.2021 and 02.03.2022 (14 months)")

    file = open('./pickle/map_total_theft.pkl', 'rb')
    object_file = pickle.load(file)
    file.close()
    st.plotly_chart(object_file)

    st.write("Data Source: Polizei Berlin")
##############
    st.title('3.2 Thefts - Prediction')
    st.write("Bike theft prediction / Time Series - Machine Learning model")

#1. Line chart showing last 31 days + predicted number of stolen bikes for tomorrow
# ---> pred_ts_chart() function from predict.py

    fig = pred_ts_chart()
    st.plotly_chart(fig)
    st.write("Data Source: Polizei Berlin")


#2. Map showing predicted number of bikes stolen per Bezirk for tomorrow (build it from the provided df)
# ---> prediction_by_Bezirk() function from predict.py

    pred_date = predict_next_day()["date_reported"][0]
    st.title(f"Predicted number of stolen bikes on {pred_date:%d.%m.%Y} by Bezirk")


    f = open('raw_data/bezirksgrenzen.geojson')
    geojson_berlin = json.load(f)
    for k in range(len(geojson_berlin['features'])):
        geojson_berlin['features'][k]['Bezirk'] = str(geojson_berlin['features'][k]['properties']['Gemeinde_schluessel'])

    df = prediction_by_Bezirk()
    df.reset_index(inplace=True)
    df['Prediction_total'] = df['Prediction_total'].apply(lambda x: round(x, 2))
    df['Bezirk'] = df['Bezirk'].apply(lambda x: '0' + str(x))
    d = {'001':'Mitte', '002':'Friedrichshain-Kreuzberg', '003':'Pankow',
                         '004':'Charlottenburg-Wilmersdorf','005':'Spandau','006':'Steglitz-Zehlendorf',
                         '007':'Tempelhof-Schöneberg','008':'Neukölln', '009':'Treptow-Köpenick',
                         '010':'Marzahn-Hellersdorf','011':'Lichtenberg','012':'Reinickendorf'}
    df['Bezirk_name'] = df['Bezirk'].map(d)

    fig = px.choropleth_mapbox(df, geojson=geojson_berlin,
                               featureidkey='Bezirk', locations='Bezirk',
                               color='Prediction_total',
                               range_color = [0, 10],
                               #hover_name='Bezirk_name',
                               color_continuous_scale="OrRd",
                               mapbox_style="open-street-map",
                               zoom=8.5, opacity=0.8,
                               center={'lat': 52.52, 'lon': 13.405},

                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

    
    
