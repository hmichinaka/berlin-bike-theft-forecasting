import streamlit as st
import pandas as pd
import numpy as np
from data.create_data import create_table

def app():
    st.title('Home')
    #st.title('Berlin Bike Accident and Theft Predictor ')

    st.write("cycle_safe(berlin) - Information to help you to cycle safely")

    st.write("1. What is the risk of my bike being stolen in Berlin, and how to to avoid it")
    st.write("2. Which are the most dangerous roads and intersection in Berlin")

    st.write("How can we use Machine Learning to mitigate these risks?")

    st.write("Data was aquired from 3 sources")
    st.write("  [Nextbike](https://www.nextbike.de/en/berlin/)")
    st.write("  Berlin Accident Data")
    st.write("  Bike Theft Data")

    st.markdown("### Sample Data")
    #df = create_table()
    #st.write(df)

    st.write('Navigate to `Visualisation` pages to visualize the data')
