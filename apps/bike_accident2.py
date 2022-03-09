import streamlit as st
import pickle

def app():
#    st.cache
    st.title('1. Accidents - Hourly')
    st.write("Animated hourly bike accidents between 01.01.2018 and 31.12.2020 (3 years)")

    file = open('./pickle/map_hourly_accident.pkl', 'rb')
    object_file = pickle.load(file)
    file.close()
    st.plotly_chart(object_file)

    st.write("- Relative ratio of bike accidents in each area")
    st.write("- 100 = average, 0 = zero accident")
    st.write("Data Source: Amt für Statistik Berlin-Brandenburg")
