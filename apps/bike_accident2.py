import plotly.express as px
import streamlit as st
from apps.get_data import read_data, get_geojson, round_up
import pickle

def app():
#    st.cache
    st.title('Accidents - Hourly')
    st.markdown("#### Animated hourly bike accidents between 01.01.2018 and 31.12.2020")

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
#    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

    st.write("- Relative ratio of bike accidents in each area")
    st.write("- 100 = average, 0 = zero accident")
