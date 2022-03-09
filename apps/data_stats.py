import streamlit as st
import numpy as np
import pandas as pd
from apps.create_data import create_table

def app():
    st.title('Data Stats')

    st.write("This is a sample data stats in the mutliapp.")
    st.write("... to know how to use it.")

    st.markdown("### Plot Data")
    # app.py, run with 'streamlit run app.py'


    df = pd.read_csv("./data/accident_counts.csv")  # read a CSV file inside the 'data" folder next to 'app.py'
    # df = pd.read_excel(...)  # will work for Excel files

    st.title("Hello world!")  # add a title
    st.write(df)  # visualize my dataframe in the Streamlit app

    #Deleted for data testing
    #df = create_table()
    #st.line_chart(df)
