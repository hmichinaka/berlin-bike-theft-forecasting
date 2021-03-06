import streamlit as st
import base64

def app():
  """### gif from local file"""
  file_ = open("./images/location_gif1000.gif", "rb")
  contents = file_.read()
  data_url = base64.b64encode(contents).decode("utf-8")
  file_.close()
  
  st.title('Locations - Hourly (GIF)')
  st.markdown("#### Animated hourly shared bike loactions between 24.02.2022 - 09.03.2022")
  
  st.markdown(
      f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
      unsafe_allow_html=True,
  )
