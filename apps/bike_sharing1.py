import streamlit as st
import pickle

def app():
#    st.cache
    st.title('2 Locations - Area')
    st.write("Sharing bike locations by area between 24.02.2022 and 09.03.2022 (14 days)")

    file = open('./pickle/map_avg_location.pkl', 'rb')
    object_file = pickle.load(file)
    file.close()
    st.plotly_chart(object_file)

    st.write("- Total number of available NextBike (approx. 2200 bikes) over the period")
    st.write("Data Source: NextBike live location API")
