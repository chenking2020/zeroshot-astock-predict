import sys, os
import requests
import time
import json
import pandas as pd


sys.path.append(os.path.dirname((os.path.abspath(__file__))))


def get_stock_hisdata(code, start_time_str="20250601", end_time_str="20250701"):

    req_url = "https://q.stock.sohu.com/hisHq?code=cn_{}&start={}&end={}&stat=1&period=d&crt=json".format(
        code, start_time_str, end_time_str
    )
    query_req = requests.get(req_url)
    time.sleep(0.2)
    query_text = query_req.text.strip()
    # print(all_stock_info["code"])
    # print(query_text)
    query_json = json.loads(query_text)
    # query_json = json.loads(query_text)
    if len(query_json) == 0:
        return None
    query_json = query_json[0]
    if "hq" not in query_json:
        return None
    query_data_list = query_json["hq"]
    batch_data = list()
    for query_row in query_data_list:
        if len(query_row) < 9:
            continue
        if float(query_row[2]) < 0.0001:
            continue

        batch_data.append(
            (
                query_row[0],
                float(query_row[1]),
                float(query_row[6]),
                float(query_row[5]),
                float(query_row[2]),
                query_row[4],
                float(query_row[7]),
            )
        )

    result_data = pd.DataFrame(
        batch_data,
        columns=["date", "open", "high", "low", "close", "pct_change", "volume"],
    )
    return result_data


if __name__ == "__main__":

    code = "zs_000001"  # 如果是获取指数，zs_000001代表上证、zs_399001代表深证、zs_399006代表创业板、zs_000680代表科创板，普通股票直接股票代码，如600001
    start_time_str = "20250601"
    end_time_str = "20250701"
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-start_time":
            start_time_str = sys.argv[i + 1]
        elif sys.argv[i] == "-end_time":
            end_time_str = sys.argv[i + 1]
        elif sys.argv[i] == "-code":
            code = sys.argv[i + 1]
        else:
            continue
    print("获取{}从{}到{}的历史数据...".format(code, start_time_str, end_time_str))
    his_data = get_stock_hisdata(code, start_time_str, end_time_str)
    print(his_data)
