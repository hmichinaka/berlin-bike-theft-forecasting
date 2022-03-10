import streamlit as st
import pandas as pd
import geopandas as gpd
from streamlit_folium import folium_static
import pickle
import numpy as np

def app():
    st.title('1. Accidents - Yearly')
    st.write("Yearly bike accident counts between 01.01.2018 and 31.12.2020 (3 years)")

    file = open('./pickle/map_yearly_accident.pkl', 'rb')
    accidents_yearly = pickle.load(file)
    file.close()
    st.plotly_chart(accidents_yearly)

    st.write("Data Source: Amt für Statistik Berlin-Brandenburg")
    df = pd.DataFrame(np.array(
        [[8459, 8384, 6701],
        [5192, 5005, 5109]]),
        columns=['2018', '2019', '2020'])
    df.rename(index={0:'Traffic accident without bike', 1:'Traffic accident with bike'}, inplace=True)
    st.table(df)

