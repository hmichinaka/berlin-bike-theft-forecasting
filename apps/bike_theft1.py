import streamlit as st
from apps.theft_data import bikes_stolen_365, theft_frequency, mean_estimated_value
import pickle

def app():
    st.title('3 Bike Thefts Berlin - Facts')

    freq = theft_frequency()
    st.write(f"Every {freq} minutes a bike got reported as being stolen in Berlin in the last 365 days.")
    total_stolen = bikes_stolen_365()
    st.write(f"In total {total_stolen} bikes got reported as being stolen in Berlin in the last 365 days.")
    mean_value = mean_estimated_value()
    st.write(f"The mean value of bikes, that got reported as being stolen in the last 365 days was {mean_value} Euro.")

    st.markdown('##')
    st.write("Total bike theft counts by area between 01.01.2021 and 02.03.2022 (14 months)")

    file = open('./pickle/map_total_theft.pkl', 'rb')
    object_file = pickle.load(file)
    file.close()
    st.plotly_chart(object_file)

    st.write("Data Source: Polizei Berlin")
