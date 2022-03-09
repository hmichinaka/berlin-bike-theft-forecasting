import streamlit as st
import pickle

def app():
    st.title('3 Thefts - Area')
    st.write("Total bike theft counts by area between 01.01.2021 and 02.03.2022 (14 months)")

    file = open('./pickle/map_total_theft.pkl', 'rb')
    object_file = pickle.load(file)
    file.close()
    st.plotly_chart(object_file)

    st.write("Data Source: Polizei Berlin")
