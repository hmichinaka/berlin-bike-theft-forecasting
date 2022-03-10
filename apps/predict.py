from webbrowser import get
import joblib
import numpy as np
import pandas as pd
import datetime
import plotly.express as px
from apps.theft_data import *

import warnings
warnings.filterwarnings("ignore")

# load model from joblib file
def load_joblib_model():
    """Read in the fitted model from the locally saved joblib.file
    """
    model = joblib.load("data/model.joblib")
    return model


# read in X_array for prediction
def get_pred_array():
    """"Create the input array X to predict for the next day
    """
    # read in newest dataset from the URL
    df = create_modelling_dataframe()
    # only keep last 31 days
    df = df[-31:]
    #create input array
    X_input = np.expand_dims(df, axis = 0)
    pred_date =  df.index[-1] +  datetime.timedelta(days = 1)

    return X_input, pred_date.date()

def predict_next_day():
    """Given an input array X of shape (1, 31, 2) predict a total value
    for the next day.
    Output: Predicted value and date the prediction refers to"""
    X_input, pred_date = get_pred_array()

    # load model and predict
    model = load_joblib_model()
    y_pred = model.predict(X_input)
    d = {"date_reported": pred_date,
         "total": round(y_pred[0][0], 0)}
    return pd.DataFrame(d, index = [0])

def pred_ts_chart():
    """Create dataframe necessary to show a time series chart (total of reported stolen
    bikes in the last 31 days plus prediction for day 32)"""
    # read in data for the last 31 days and date of prediction
    X_input, pred_date = get_pred_array()

    # we only need the "total" column of X_input
    X_input = X_input[0][:,0]
    X_input = pd.Series(X_input)

    # get the predicted value for day 32 and the corresponding date
    pred_df = predict_next_day()

    # create empty dataframe starting 31 days before prediction date to prediction date
    chart_df = pd.DataFrame({'date':pd.date_range(start = pred_df["date_reported"][0] - datetime.timedelta(days=31), end = pred_df["date_reported"][0])})

    # concatenate the values from X_input to the empty dataframe
    chart_df = pd.concat([chart_df, X_input], axis = 1)
    chart_df.rename(columns={0:"total"}, inplace=True)

    # add the predicted value as the last value
    chart_df.iloc[-1, 1] = pred_df["total"][0]

    fig = px.line(chart_df, x="date", y="total", title= f"Reported stolen bikes in Berlin in the last 31 days and prediction for {pred_date} (red line)")
    fig.add_scattergl(x=chart_df["date"].where(chart_df["date"] >=chart_df.iloc[-2,0]), y=chart_df["total"], line={"color": "red"},
                  showlegend=False)

    return fig

def prediction_by_Bezirk():
    """Allocates the predicted total for the next day on the 12 Bezirke
    based on the mean percentage split for the last 14 days.
    """
    # load data, clean it and group by Bezirke
    df = load_data()
    df= clean_theft_data(df)
    df = pivot_theft_data(df)

    # create dataframe with the mean percentage split of the last 14 days
    df= perc_split_bezirk(df)

    # call the prediction for the next day and assign it as a new column to the dataframe
    df["pred_total"] = predict_next_day().iloc[0,1]

    # create dataframe with just the split up values
    df  = pd.DataFrame(round(df["perc_split"] * df["pred_total"], 0)).rename(columns={0: "Prediction_total"})

    return df

if __name__ == "__main__":
    #print(predict_next_day())
    pred_ts_chart()
