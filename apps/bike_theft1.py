import streamlit as st
from apps.theft_data import bikes_stolen_365, theft_frequency, mean_estimated_value, get_last_date
import pickle

def app():
    st.title('3 Bike Thefts Berlin - Facts')

    last_date = get_last_date()

    freq = theft_frequency()
    st.markdown(f"##### `Every {freq} minutes` a bike got reported as being stolen in Berlin in the last 365 days.")
    total_stolen = bikes_stolen_365()
    st.markdown(f"##### In total `{total_stolen:,} bikes` got reported as being stolen in Berlin in the last 365 days.")
    mean_value = mean_estimated_value()
    st.markdown(f"##### The `mean value` of bikes, that got reported as being stolen in the last 365 days was **{mean_value} Euro**.")

    st.markdown('##')
    st.markdown(f"##### Number of stolen bikes by 'Kiez' between 01.01.2021 and today")

    file = open('./pickle/map_total_theft.pkl', 'rb')
    object_file = pickle.load(file)
    file.close()
    st.plotly_chart(object_file)


    st.markdown("**Data Source bike thefts**:")
    st.markdown("[Polizei Berlin](https://www.internetwache-polizei-berlin.de/vdb/Fahrraddiebstahl.csv)")
    st.markdown("[Creative Commons Licence CC BY 3.0 DE](https://creativecommons.org/licenses/by/3.0/de/)")
    st.markdown("Dataset from Polizei Berlin that shows reported bike thefts starting from 01.01.2021 and is updated daily.\
        Thefts for which the time of crime cannot be limited to 3 days are excluded. \
            For the mean value break-ins into basements are excluded.")

    st.markdown("**Data Source Lebensweltlich orientierte Räume (LOR) in Berlin**:")
    st.markdown("[Amt für Statistik Berlin-Brandenburg](https://www.stadtentwicklung.berlin.de/planen/basisdaten_stadtentwicklung/lor/de/download.shtml)")
    st.markdown("[Creative Commons Licence CC BY 3.0 DE](https://creativecommons.org/licenses/by/3.0/de/)")
    st.markdown("The LOR-data was transfered into GEOJSON.")
