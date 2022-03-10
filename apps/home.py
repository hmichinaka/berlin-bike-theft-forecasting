import streamlit as st
from PIL import Image


def app():

    st.title("cycle_safe(berlin) - helping to keep you and your bike safe")

    st.markdown("##### How can we use Machine Learning to mitigate")
    st.markdown("##### 1. Bike theft risk")
    st.markdown("##### 2. Bike accident risk")

    image = Image.open('./images/BikeTheft.png')
    st.image(image, caption='bike theft')

    st.markdown("### The Team")

    st.markdown("##### Hitoshi Michinaka [Linkedin](https://www.linkedin.com/in/hmichinaka/)")
    st.markdown("##### Dominik Abratanski [Linkedin](https://www.linkedin.com/in/dominikabratanski/)")
    st.markdown("##### Lukas Hartung [Linkedin](https://www.linkedin.com/in/lukas-h-0438578b/)")
    st.markdown("##### Marlon Deus [Linkedin](https://www.linkedin.com/in/marlon-deus-0a37031b4/)")
    st.markdown("##### Paul Roberts [Linkedin](https://www.linkedin.com/in/paul-roberts-871a6790/)")
    st.markdown("##### Jakob Hohenstein [Linkedin](https://www.linkedin.com/in/jakob-hohenstein-53667914a/)")
