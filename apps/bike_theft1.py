import streamlit as st
from apps.theft_data import bikes_stolen_365, theft_frequency, mean_estimated_value, get_last_date
import pickle

def app():
    st.title('Bike Thefts Berlin - Facts')

    last_date = get_last_date()

    freq = theft_frequency()
    st.markdown(f"##### `Every {freq} minutes` a bike got reported stolen in Berlin in the last 365 days.")
    total_stolen = bikes_stolen_365()
    st.markdown(f"##### In total `{total_stolen:,} bikes` got reported stolen in Berlin in the last 365 days.")
    mean_value = mean_estimated_value()
    st.markdown(f"##### The `mean value` of bikes, that got reported stolen in the last 365 days was `{mean_value} €`.")

    st.markdown('##')
    st.markdown(f"##### Number of stolen bikes by 'Kiez' between 01.01.2021 and today")

    file = open('./pickle/map_total_theft.pkl', 'rb')
    object_file = pickle.load(file)
    file.close()
    st.plotly_chart(object_file)
