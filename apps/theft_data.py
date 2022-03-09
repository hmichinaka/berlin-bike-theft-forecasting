# URL Download
import csv
import io
from venv import create
import requests
import datetime
import pandas as pd
import numpy as np
import plotly.express as px

# Read in data from the Berlin Polizei URL
def load_data():
    """Read in the most recent bike theft data from Polizei Berlin and return
    a pandas dataframe """
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
def translate_col_names(d):
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
    d.rename(columns= eng_col_names, inplace=True)

# define function for renaming the categories
def rename_type_bike(x):
    """translation of the categories of variable "type_bike".
    """
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
    """Takes in the pd Dataframe created in load_data() and
    returns a clean dataframe"""
    #translate columns to English
    translate_col_names(d)

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
    """Groups dataframe by Bezirk and returns sum of thefts for
    each Bezirk and day (date_reported)"""
    d = d.pivot_table(index = "date_reported", columns = "Bezirk", values = "type_bike", aggfunc= "count")
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


# Calculate rolling average
def calculate_rolling_average(df, window_size):
    """Calculate rolling average over the last window_size days.
    Fills missing values with mean of the last window_size days"""
    fill_value = df["total"][-window_size:].mean()
    df["total_moving_average"] = df["total"].rolling(window = window_size, center = False).mean().fillna(fill_value)

# Calculate the total number of reported stolen bikes in the last 365 days
def bikes_stolen_365():
    """returns total bikes reported stolen in the last 365 days in Berlin"""
    df = load_data()
    df = clean_theft_data(df)
    df = pivot_theft_data(df)
    df['Total'] = df.sum(axis=1)
    df = pd.DataFrame(df["Total"])
    df =df[-365:]
    total_stolen_365=df.sum().values[0]
    return int(total_stolen_365)

# Calculates "Every XX minutes a bike is reported as stolen in Berlin"
def theft_frequency():
    """returns frequency (in minutes) of bikes being reported as
    stolen in Berlin in the last 365 days"""
    minutes_day=1440
    minutes_year=1440*365
    return round(minutes_year/bikes_stolen_365())


# Create the dataframe for the modelling
def create_modelling_dataframe():
    """Read in most recent dataset from URL, clean it, group it
    and return dataframe for model creation
    """
    # load data
    df = load_data()
    # clean data
    df= clean_theft_data(df)
    # group data by Bezirk and date_reported and sum up
    df = pivot_theft_data(df)

    # add "total column"
    df["total"] = df.sum(axis = 1)

    # cut-off the last three days
    # df.drop(df.tail(3).index,inplace=True)

    # calculate rolling average
    calculate_rolling_average(df, window_size = 3)

    # select relevant columns for modelling
    cols_list =  ["total", "total_moving_average"]
    df = df[cols_list]

    return df

# calculates the mean estimated value of all reported stolen bikes
def mean_estimated_value():
    """Returns the mean of "estimated value" of all stolen bikes.
    "Kellereinbruch" is filtered out
    """
    df = load_data()
    df= clean_theft_data(df)
    start_date = datetime.datetime.today() - datetime.timedelta(365)
    cond = np.logical_and(df["theft_type"] != "Keller- und Bodeneinbruch", df["date_reported"] >= start_date)
    df = df[cond]
    return f"The mean estimated value of a reported stolen bike is {round(df.estimated_value.mean())} Euro"


def hourly_count_stolen_bikes():
    """Creates a line plot of the number of stolen bikes by hour_theft_start
    """

    df = load_data()
    df = clean_theft_data(df)

    count_per_hour = df.groupby("hour_theft_start").count()
    count_per_hour = count_per_hour[["date_reported"]].reset_index()
    count_per_hour["count_stolen"] = count_per_hour["date_reported"]
    fig = px.line(count_per_hour, x='hour_theft_start', y='count_stolen',
                title='Berlin: Hourly count of stolen bikes from 2021-01-01',
                labels={"hour_theft_start": "Assumed hour of theft", "count_stolen": "Number of stolen bikes"})

    return fig
