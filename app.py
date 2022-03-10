import streamlit as st
from multiapp import MultiApp
from apps import home, data_stats # import your app modules here
from apps import new_app, app_tweets, bike_accident1, bike_accident2, bike_accident3, bike_sharing1, bike_sharing2, bike_theft1, bike_theft2, under_the_hood, presentation
# import your app modules here

app = MultiApp()


# Add all your application here
#@st.cache(suppress_st_warning=True)
app.add_app("Home", home.app)
app.add_app("1 Accidents - Yearly", bike_accident1.app)
app.add_app("1 Accidents - Hourly", bike_accident2.app)
app.add_app("1 Accidents - Clusters", bike_accident3.app)
app.add_app("2 Locations - Area", bike_sharing1.app)
app.add_app("2 Locations - Hourly ", bike_sharing2.app)
app.add_app("3 Thefts - Facts", bike_theft1.app)
app.add_app("3 Thefts - Prediction", bike_theft2.app)
app.add_app("4 Under the hood", under_the_hood.app)
app.add_app("Data Sources", data_stats.app)
app.add_app("Tweets about bikes in Berlin", app_tweets.app)
app.add_app("Spare Page", new_app.app)

app.add_app("Presentation", presentation.app)

# The main app
app.run()
