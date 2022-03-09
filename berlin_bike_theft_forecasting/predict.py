from webbrowser import get
import joblib
import numpy as np
import pandas as pd
import datetime
from berlin_bike_theft_forecasting.theft_data import create_modelling_dataframe

# load model from joblib file
def load_joblib_model():
    """Read in the fitted model from the locally saved joblib.file
    """
    model = joblib.load("model.joblib")
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
    return pd.DataFrame(d, index = [0]).set_index("date_reported")

if __name__ == "__main__":
    print(predict_next_day())
