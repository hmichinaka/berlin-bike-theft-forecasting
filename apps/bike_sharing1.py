import streamlit as st
import pickle

def app():
#    st.cache
    st.title('Locations - Area')
    st.markdown("#### Shared bike locations by area between 24.02.2022 and 09.03.2022")

    file = open('./pickle/map_avg_location.pkl', 'rb')
    object_file = pickle.load(file)
    file.close()
    st.plotly_chart(object_file)

    st.markdown("###### Total number of available NextBike (approx. 2200 bikes) over the period.")
