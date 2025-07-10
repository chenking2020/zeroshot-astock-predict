import sys, os

sys.path.append(os.path.dirname((os.path.abspath(__file__))))

from statsmodels.tsa.arima.model import ARIMA

import pandas as pd

predict_days = 10

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def predict(code, prices):
    predictor = ARIMA(prices["close"], order=(5, 1, 0)).fit()
    predictions = predictor.forecast(steps=predict_days)
    return predictions.iloc[-predict_days:].values.tolist()
