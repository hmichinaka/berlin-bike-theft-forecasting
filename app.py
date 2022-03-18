import streamlit as st
from multiapp import MultiApp
from apps import home, data_stats, location_gif #presentation # import your app modules here
from apps import app_tweets, bike_accident1, bike_accident2, bike_accident3, bike_sharing1, bike_sharing2, bike_theft1, bike_theft2, under_the_hood
from apps import accident_gif, accident_EDA

app = MultiApp()


# Add all your application here
#@st.cache(suppress_st_warning=True)
app.add_app("Home", home.app)
app.add_app("Locations - Area", bike_sharing1.app)
app.add_app("Locations - Hourly ", bike_sharing2.app)
app.add_app("Locations - Hourly (GIF)", location_gif.app)

app.add_app("Accidents - EDA", accident_EDA.app)
app.add_app("Accidents - Yearly", bike_accident1.app)
app.add_app("Accidents - Hourly", bike_accident2.app)
app.add_app("Accidents - Hourly (GIF)", accident_gif.app)
app.add_app("Accidents - Clusters", bike_accident3.app)

app.add_app("Thefts - Facts", bike_theft1.app)
app.add_app("Thefts - Prediction", bike_theft2.app)
#app.add_app("4 Under the hood", under_the_hood.app)
app.add_app("Berlin bike tweets", app_tweets.app)
#app.add_app("Spare Page", new_app.app)
app.add_app("Data Sources", data_stats.app)
#app.add_app("Presentation", presentation.app)

# The main app
app.run()
