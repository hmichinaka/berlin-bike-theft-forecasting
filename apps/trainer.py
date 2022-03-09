import joblib
from tensorflow.keras import callbacks
from termcolor import colored
from apps.theft_data import *
from apps.theft_modelling import *

import warnings
warnings.filterwarnings("ignore")

def save_model_locally(model):
    """Save the model into a .joblib format"""
    joblib.dump(model, 'model.joblib')
    print(colored("model.joblib saved locally", "green"))



if __name__ == "__main__":

    # call in dataframe for modelling
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


    # saved fitted model to a joblib file
    save_model_locally(model)
