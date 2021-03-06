import streamlit as st
from dataclasses import dataclass
from apps.predict import pred_ts_chart, prediction_by_Bezirk, predict_next_day
import plotly.express as px
import json


def app():
    '''Bike Theft Forecast'''
    st.title('Thefts - Prediction')

    pred_date = predict_next_day()["date_reported"][0]
#1. Line chart showing last 31 days + predicted number of stolen bikes for tomorrow
# ---> pred_ts_chart() function from predict.py

    st.markdown(f"##### Number of reported stolen bikes in Berlin in the last 31 days and prediction for {pred_date:%d.%m.%Y} (red line)")

    fig = pred_ts_chart()
    st.plotly_chart(fig)



#2. Map showing predicted number of bikes stolen per Bezirk for tomorrow (build it from the provided df)
# ---> prediction_by_Bezirk() function from predict.py


    st.markdown(f"##### Predicted number of stolen bikes on {pred_date:%d.%m.%Y} by Bezirk")


    f = open('raw_data/bezirksgrenzen.geojson')
    geojson_berlin = json.load(f)
    for k in range(len(geojson_berlin['features'])):
        geojson_berlin['features'][k]['Bezirk'] = str(geojson_berlin['features'][k]['properties']['Gemeinde_schluessel'])

    df = prediction_by_Bezirk()
    df.reset_index(inplace=True)
    df['Predicted_theft'] = df['Prediction_total'].apply(lambda x: round(x, 2))
    df['Bezirk'] = df['Bezirk'].apply(lambda x: '0' + str(x))
    d = {'001':'Mitte', '002':'Friedrichshain-Kreuzberg', '003':'Pankow',
                         '004':'Charlottenburg-Wilmersdorf','005':'Spandau','006':'Steglitz-Zehlendorf',
                         '007':'Tempelhof-Schöneberg','008':'Neukölln', '009':'Treptow-Köpenick',
                         '010':'Marzahn-Hellersdorf','011':'Lichtenberg','012':'Reinickendorf'}
    df['Bezirk_name'] = df['Bezirk'].map(d)

    fig = px.choropleth_mapbox(df, geojson=geojson_berlin,
                               featureidkey='Bezirk', locations='Bezirk',
                               color='Predicted_theft',
                               range_color = [0, 10],
                               hover_name='Bezirk_name',
                               hover_data={"Bezirk":False, 'Predicted_theft':True},
                               color_continuous_scale="OrRd",
                               mapbox_style="open-street-map",
                               zoom=8.5, opacity=0.8,
                               center={'lat': 52.52, 'lon': 13.405},

                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

    st.write("##")
    st.markdown("#### Machine Learning Model")
    st.markdown("##### [Recurrent Neural Network](https://www.tensorflow.org/guide/keras/rnn) with 2 LSTM-layers \
        [Long Term Short Memory](https://www.tensorflow.org/api_docs/python/tf/keras/layers/LSTM)")
    st.markdown("###### Bike theft predicted values compared to actual values")
    st.image("./images/prediction vs. actual.png")
