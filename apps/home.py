import streamlit as st
#from PIL import Image


def app():

    st.title("cycle_safe(berlin) - helping to keep you and your bike safe")

    st.write("We offer the following visualized dashboards:")
    st.write("- Bike Traffic: Bike distribution map gives you an idea about bike traffic throughout the day")    
    st.write("- Bike Accident: Cluster analysis shows you where the accident hot spots are")    
    st.write("- Bike Theft: Data analysis and forecasting thefts by districts might save your bike")

    st.image("./images/BikeTheft.png")

    st.markdown("### The Team")
    st.image("./images/team.jpg")    
    
    st.markdown("##### Hitoshi Michinaka [Linkedin](https://www.linkedin.com/in/hmichinaka/)")
    st.markdown("##### Dominik Abratanski [Linkedin](https://www.linkedin.com/in/dominikabratanski/)")
    st.markdown("##### Lukas Hartung [Linkedin](https://www.linkedin.com/in/lukas-h-0438578b/)")
    st.markdown("##### Marlon Deus [Linkedin](https://www.linkedin.com/in/marlon-deus-0a37031b4/)")
    st.markdown("##### Paul Roberts [Linkedin](https://www.linkedin.com/in/paul-roberts-871a6790/)")
    st.markdown("##### Jakob Hohenstein [Linkedin](https://www.linkedin.com/in/jakob-hohenstein-53667914a/)")
