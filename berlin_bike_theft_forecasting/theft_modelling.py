from venv import create
import importlib

import numpy as np
from keras.layers import Dense, LSTM, Dropout
from tensorflow.keras import Sequential, callbacks
from berlin_bike_theft_forecasting.theft_data import create_modelling_dataframe

def create_opt_model():
    """
    Creates the finetuned model selected in B_Theft_Modelling
    Outputs models, that needs to be compiled and fit"""
    model = Sequential()
    # first LSTM layer
    model.add(LSTM(units = 70, activation = "tanh", return_sequences = True))
    model.add(Dropout(0.2))
    # second LSTM layer
    model.add(LSTM(units= 30, activation= "tanh", return_sequences= False))
    model.add(Dropout(0.2))

    # output layer to predict one value
    model.add(Dense(1, activation= "linear"))
    return model

def get_X_y(dataset, window_size, future_horizon):
    """Creates arrays to be fed into the RNN model
    Input: dataframe after create_modelling_dataframe, window_size and future_horizon
    Output: Arrays for X and y
    """
    X = []
    y = []

    for i in range(0, dataset.shape[0] - window_size - future_horizon):
        X.append(dataset[i: i + window_size])
        y.append(dataset[i + window_size: i + window_size + future_horizon])

    X = np.array(X)
    y = np.array(y)

    # expand dimensions
    X = np.expand_dims(X, 2)
    return X, y

if __name__ == "__main__":
    # import data
    df = create_modelling_dataframe()

    # instantiate model
    model = create_opt_model()

    # create X and y arrays
    X, y = get_X_y(df, window_size=31, future_horizon=1)

    # compile model
    model.compile(loss = "mse",
                  optimizer = "adam",
                  metrics = "mean_absolute_percentage_error")

    # fit model
    es = callbacks.EarlyStopping(patience = 5, restore_best_weights=True)
    model.fit(X, y, batch_size = 8,
              epochs = 300, verbose = 0,
              callbacks = [es], validation_split = 0.2)
