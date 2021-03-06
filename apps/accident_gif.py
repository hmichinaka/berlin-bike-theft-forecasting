import streamlit as st
import base64

def app():
  """### gif from local file"""
  file_ = open("./images/accident_gif1000.gif", "rb")
  contents = file_.read()
  data_url = base64.b64encode(contents).decode("utf-8")
  file_.close()
  
  st.title('Accidents - Hourly (GIF)')
  st.markdown("#### Animated hourly bike accidents between 01.01.2018 and 31.12.2020")
    
  st.markdown(
      f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
      unsafe_allow_html=True,
  )
