import plotly.express as px
from apps.get_data import read_data, get_geojson, round_up
import streamlit as st
import pickle

def app():
#    st.cache
    st.title('Locations - Hourly')
    st.markdown("#### Animated hourly shared bike loactions between 24.02.2022 - 09.03.2022")

#    file = open('./pickle/map_hourly_location.pkl', 'rb')
#    object_file = pickle.load(file)
#    file.close()
#    st.plotly_chart(object_file)

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
#    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

    st.write("- Relative ratio of parked NextBikes in each area")
    st.write("- 0 = average number of NextBikes in each area")
