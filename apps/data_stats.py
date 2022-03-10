import streamlit as st
import numpy as np
import pandas as pd
from apps.create_data import create_table

def app():
    st.title('Data Sources')

    st.markdown("**Data Source bike thefts**:")
    st.markdown("[Polizei Berlin](https://www.internetwache-polizei-berlin.de/vdb/Fahrraddiebstahl.csv)  \n \
        [Creative Commons Licence CC BY 3.0 DE](https://creativecommons.org/licenses/by/3.0/de/)")
    st.markdown("Dataset from Polizei Berlin that shows reported bike thefts starting from 01.01.2021 and is updated daily.\
        Thefts for which the time of crime cannot be limited to 3 days are excluded. \
            For the mean value break-ins into basements are excluded.")

    st.markdown("**Data Source Lebensweltlich orientierte Räume (LOR) in Berlin**:")
    st.markdown("[Amt für Statistik Berlin-Brandenburg](https://www.stadtentwicklung.berlin.de/planen/basisdaten_stadtentwicklung/lor/de/download.shtml)  \n \
        [Creative Commons Licence CC BY 3.0 DE](https://creativecommons.org/licenses/by/3.0/de/)")
    st.markdown("The LOR-data was transfered into GEOJSON.")

    st.markdown("**Data source accidents**:")
    st.markdown("Road accidents 2018: [Amt für Statistik Berlin-Brandenburg](https://daten.berlin.de/datensaetze/strassenverkehrsunf%C3%A4lle-nach-unfallort-berlin-2018)  \n \
        [Creative Commons Licence CC BY 3.0 DE](https://creativecommons.org/licenses/by/3.0/de/)")
    st.markdown("Road accidents 2019: [Amt für Statistik Berlin-Brandenburg](https://daten.berlin.de/datensaetze/strassenverkehrsunf%C3%A4lle-nach-unfallort-berlin-2019)  \n \
        [Creative Commons Licence CC BY 3.0 DE](https://creativecommons.org/licenses/by/3.0/de/)")
    st.markdown("Road accidents 2020: [Amt für Statistik Berlin-Brandenburg](https://daten.berlin.de/datensaetze/strassenverkehrsunf%C3%A4lle-nach-unfallort-berlin-2020)  \n \
        [Creative Commons Licence CC BY 3.0 DE](https://creativecommons.org/licenses/by/3.0/de/)")
    st.markdown("Accidents not involving bikes were excluded.")

    st.markdown("**Data Source Bezirke**:")
    st.markdown("Geoportal Berlin / [Bezirke](https://daten.odis-berlin.de/de/dataset/bezirksgrenzen/)")

    st.markdown("**Data source Nextbike**:")
    st.markdown("[Nextbike API](https://sharedmobility.github.io/Nextbike.html)")


    st.markdown("**Data source GreenLane**:")
    st.markdown("infravelo.de / [API](https://www.infravelo.de/api/)")
