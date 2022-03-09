import streamlit as st
import pickle

def app():
#    st.cache
    st.title('2 Locations - Hourly')
    st.write("Animated hourly sharing bike loactions between 24.02.2022 - 09.03.2022 (14 days)")

    file = open('./pickle/map_hourly_location.pkl', 'rb')
    object_file = pickle.load(file)
    file.close()
    st.plotly_chart(object_file)

    st.write("- Relative ratio of parked NextBike in each area")
    st.write("- 0 = average number of NextBike")
    st.write("Data Source: NextBike live location API")
