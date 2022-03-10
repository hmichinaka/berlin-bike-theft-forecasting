import streamlit as st
from PIL import Image


def app():

    st.title("cycle_safe(berlin) - helping to keep you and your bike safe")

    st.write("How can we use Machine Learning to mitigate")
    st.write("1. Bike theft risk")
    st.write("2. Bike accident risk")

    image = Image.open('./images/BikeTheft.png')
    st.image(image, caption='bike theft')

    st.markdown("### The Team")

    st.write("Hitoshi Michinaka [Linkedin](https://www.linkedin.com/in/hmichinaka/)")
    st.write("Dominik Abratanski [Linkedin](https://www.linkedin.com/in/dominikabratanski/)")
    st.write("Lukas Hartung [Linkedin](https://www.linkedin.com/in/lukas-h-0438578b/)")
    st.write("Marlon Deus [Linkedin](https://www.linkedin.com/in/marlon-deus-0a37031b4/)")
    st.write("Paul Roberts [Linkedin](https://www.linkedin.com/in/paul-roberts-871a6790/)")
    st.write("Jakob Hohenstein [Linkedin](https://www.linkedin.com/in/jakob-hohenstein-53667914a/)")
