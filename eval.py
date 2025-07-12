import sys, os
import time
import importlib
import pandas as pd


sys.path.append(os.path.dirname((os.path.abspath(__file__))))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":

    # module_name = "chronos_bolt_model"
    module_name = "arima"

    for i in range(len(sys.argv)):
        if sys.argv[i] == "-module_name":
            module_name = sys.argv[i + 1]
        else:
            continue
    try:
        model = importlib.import_module(module_name)
    except ImportError as e:
        print("不支持的预测模型{}，请检查模型输入是否正确。".format(module_name))
        sys.exit(1)

    squared_errors = []
    for filename in os.listdir(os.path.join(BASE_DIR, "data/eval")):
        if filename.endswith(".csv"):
            filepath = os.path.join(BASE_DIR, "data/eval", filename)
            df = pd.read_csv(filepath, encoding="utf-8")
            pre_values = model.predict(filename.split(".")[0], df.iloc[:-10, :])
            true_values = df.iloc[-10:, :]["close"].values.tolist()
            if len(pre_values) != len(true_values):
                print("预测结果和真实值长度不一致，无法计算误差。")
                continue
            for i in range(len(pre_values)):
                error = pre_values[i] - true_values[i]
                squared_errors.append(error**2)
    mse = sum(squared_errors) / len(squared_errors)
    rmse = mse**0.5
    print("根均方误差(RMSE):", rmse)
