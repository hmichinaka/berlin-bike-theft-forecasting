# URL Download
import csv
import io
import urllib.request
import requests

import pandas as pd
import numpy as np


# Read in data from the Berlin Polizei URL
def load_data():
    url = "https://www.internetwache-polizei-berlin.de/vdb/Fahrraddiebstahl.csv"
    download = requests.get(url)
    decoded_content = download.content.decode('ISO-8859-1')
    file = decoded_content.splitlines()

    cr = csv.DictReader(file, delimiter=',')
    my_list = list(cr)
    df  = pd.DataFrame(my_list)
    return df

###################################
###  Clean data ######

#dict to translate from German to English
eng_col_names = {
    "ANGELEGT_AM": "date_reported",
    "TATZEIT_ANFANG_DATUM": "date_theft_start",
    "TATZEIT_ANFANG_STUNDE": "hour_theft_start",
    "TATZEIT_ENDE_DATUM": "date_theft_end",
    "TATZEIT_ENDE_STUNDE": "hour_theft_end",
    "LOR": "LOR",
    "SCHADENSHOEHE": "estimated_value",
    "VERSUCH": "attempt",
    "ART_DES_FAHRRADS": "type_bike", 
    "DELIKT": "theft_type",
    "ERFASSUNGSGRUND": "theft_type_detail"    
}

# define function for renaming the categories
def rename_type_bike(x): 
    if x == "Herrenfahrrad": 
        return "man's bike"
    if x == "Damenfahrrad":
        return "woman's bike"
    if x == "Fahrrad":
        return "bike"
    if x == "Kinderfahrrad":
        return "child's bike"
    else: 
        return "other bike"

# dictionary for "attempt"
attempt_dict = {
    "Ja": "Yes", 
    "Nein": "No", 
    "Unbekannt": "Unknown"
}

# Concatenates translation of column and category names, 
#  conversion of dtypes, drop duplicates and create 
#  higher regional levels from LOR
def clean_theft_data(d):
    """returns a clean dataframe"""
    #translate columns to English
    d.rename(columns= eng_col_names, inplace=True)
    
    #translate bike type to English
    d["type_bike"] = d["type_bike"].apply(rename_type_bike)
    
    #translate attempt type to English
    d["attempt"] = d["attempt"].map(attempt_dict)
    
    # convert the date columns to format='%d.%m.%Y
    d["date_reported"] = pd.to_datetime(d["date_reported"], format='%d.%m.%Y')
    d["date_theft_start"] = pd.to_datetime(d["date_theft_start"], format='%d.%m.%Y')
    d["date_theft_end"] = pd.to_datetime(d["date_theft_end"], format='%d.%m.%Y')
    
    # convert the time columns to int
    d["hour_theft_start"] = d["hour_theft_start"].astype(int)
    d["hour_theft_end"] = d["hour_theft_end"].astype(int)
    
    #convert value column to float
    d["estimated_value"] = d["estimated_value"].astype(float)
    
    #drop duplicates
    d = d.drop_duplicates()
    
    # BZR (first six numbers)
    d["BZR"] = d["LOR"].str[:6]
    
    # PGR (first four numbers)
    d["PGR"] = d["LOR"].str[:4]
    
    # Bezirk (first four numbers)
    d["Bezirk"] = d["LOR"].str[:2]
    
    return d

# Group by bezirk and sum up
def pivot_theft_data(d):
    d = d.pivot_table(index = "date_theft_start", columns = "Bezirk", values = "type_bike", aggfunc= "count")
    d.fillna(value = 0, inplace=True)
    return d


# Calculate percentage theft by Bezirk
def perc_split_bezirk(d):
    """returns df showing % split of bikes stolen over the last 2 weeks per Bezirk in Berlin"""
    d = d[-15:]
    d.loc['perc_split']= d.sum()
    d = d.div(d.sum(axis=1), axis=0)
    d = d.iloc[-1]
    return pd.DataFrame(d)


# Create the dataframe for the modelling
def create_modelling_dataframe():
    df = load_data()
    clean_theft_data(df)
    pivot_theft_data(df)

    # 




