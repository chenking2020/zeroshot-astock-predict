import sys, os

sys.path.append(os.path.dirname((os.path.abspath(__file__))))

from autogluon.timeseries import TimeSeriesPredictor, TimeSeriesDataFrame

import pandas as pd

predictor = None

predict_days = 10

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def zeroshot_train():
    global predictor

    traindf = None

    for filename in os.listdir(os.path.join(BASE_DIR, "data/chronos-bolt-traindata")):
        if filename.endswith(".csv"):
            filepath = os.path.join(BASE_DIR, "data/chronos-bolt-traindata", filename)
            df = pd.read_csv(filepath, encoding="utf-8")
            df = df[["date", "close"]]
            df.insert(loc=0, column="code", value=[filename.split(".")[0]] * len(df))
            df = df.rename(
                columns={"code": "item_id", "date": "timestamp", "close": "target"}
            )
            if traindf is None:
                traindf = df
            else:
                traindf = pd.concat([traindf, df], ignore_index=True)

    traindf = TimeSeriesDataFrame(traindf)
    predictor = TimeSeriesPredictor(
        prediction_length=predict_days,
        log_to_file=False,
        freq="D",
        path=os.path.join(BASE_DIR, "models/chronos-bolt-ftbase"),
    ).fit(
        traindf,
        hyperparameters={
            "Chronos": {
                "model_path": os.path.join(BASE_DIR, "models/chronos-bolt-base"),
                # "fine_tune": True,
                # "fine_tune_batch_size": 32,
                # "fine_tune_steps": 5000,
            },
        },
    )
    print("训练完成！")


def predict(code, prices):
    global predictor
    if predictor is None:
        model_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "models/chronos-bolt-ftbase"
        )
        predictor = TimeSeriesPredictor(
            prediction_length=predict_days,
            log_to_file=False,
            path=model_path,
        ).load(model_path)
    testdf = prices[["date", "close"]]
    testdf.insert(loc=0, column="code", value=[code] * len(testdf))
    testdf = testdf.rename(
        columns={"code": "item_id", "date": "timestamp", "close": "target"}
    )
    testdf = TimeSeriesDataFrame(testdf)
    predictions = predictor.predict(testdf)
    return predictions["mean"].values.tolist()


if __name__ == "__main__":
    zeroshot_train()
