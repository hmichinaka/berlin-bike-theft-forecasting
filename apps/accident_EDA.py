import streamlit as st
from PIL import Image

def app():
    st.title('Exploratory analysis of bike accidents in Berlin')
    st.write('between 2018 and 2020')
    st.markdown('#### `40% of accidents` reported in Berlin involved bicycles.')
    st.markdown('#### On average `14 accidents` are reported per day.')


    image1 = Image.open('./images/accident_kind.png')
    st.image(image1)
    image2 = Image.open('./images/accident_district.png')
    st.image(image2)
    image3 = Image.open('./images/accident_months.png')
    st.image(image3)
    image4 = Image.open('./images/accident_weekday.png')
    st.image(image4)
    image5 = Image.open('./images/accident_hours.png')
    st.image(image5)

    st.caption('The data has been obtained from [daten.berlin.de](https://daten.berlin.de/kategorie/verkehr)')
