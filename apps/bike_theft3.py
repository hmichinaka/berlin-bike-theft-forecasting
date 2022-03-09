import streamlit as st
import plotly.express as px

def app():
    '''Bike Theft EDA'''
    st.title('3 Thefts - EDA')
    st.write("Bike theft EDA")

#1. Stats about bike theft:
#a. Total bikes reported as stolen in the last 365 days ---> bikes_stolen_365() function from theft_data.py
#b. Frequency at which bikes get stolen (e.g. every X minutes a bike was stolen) in the last 365 days ---> theft_frequency() function from theft_data.py
#c. Mean value of stolen bikes (all time) ----> mean_estimated_value() function from theft_data.py


#2. Map showing historical bike theft by LOR  ---> from Hitoshi


#3. Line chart showing bike theft by hour ---> hourly_count_stolen_bikes() function from theft_data.py
