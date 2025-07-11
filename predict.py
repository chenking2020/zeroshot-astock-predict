import sys, os
import time
import importlib
import pandas as pd


sys.path.append(os.path.dirname((os.path.abspath(__file__))))

if __name__ == "__main__":

    code = "cn_601066"
    data_file_path = "cn_601066.csv"
    module_name = "chronos_bolt_model"

    for i in range(len(sys.argv)):
        if sys.argv[i] == "-data_file_path":
            data_file_path = sys.argv[i + 1]
        elif sys.argv[i] == "-module_name":
            module_name = sys.argv[i + 1]
        elif sys.argv[i] == "-code":
            code = sys.argv[i + 1]
        else:
            continue
    try:
        model = importlib.import_module(module_name)
    except ImportError as e:
        print("不支持的预测模型{}，请检查模型输入是否正确。".format(module_name))
        sys.exit(1)

    try:
        df = pd.read_csv(data_file_path, encoding="utf-8")
    except FileNotFoundError as e:
        print("数据文件{}不存在，请检查文件路径是否正确。".format(data_file_path))
        sys.exit(1)

    pre_result = model.predict(code, df)
    print("预测结果：")
    print(pre_result)
