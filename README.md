# zeroshot-astock-predict
汇集ARIMA、时序大模型、视觉大模型等主流或前沿零样本无训练股价预测算法，并在实际数据测试对比下，寻找适合A股的最佳预测模型

## 快速开始

**1. 拉取代码**

git clone本开源代码

**2. 安装Python依赖包**

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/  -r requirements.txt
```
**3. 下载模型**

如果使用chronos_bolt_model模型去预测，则需要下载原始模型文件，下载后的文件夹存放在models中，即models/chronos-bolt-base，现在地址在HuggingFace中的[chronos-bolt-base](https://huggingface.co/amazon/chronos-bolt-base)

**4. 执行预测**

```bash
python predict.py -code cn_600517 -data_file_path /path/cn_600517.csv -module_name chronos_bolt_model
```

其中，

code为股票代码，如果普通个股，为cn_+普通数字股票代码，如cn_600517；如果是获取指数，zs_000001代表上证、zs_399001代表深证、zs_399006代表创业板、zs_000680代表科创板。如果如果不传入该参数，默认为上证指数zs_000001

data_file_path为股票历史数据所在的文件绝对路径，默认为本开源代码提供的测试样例

module_name预测模型名称，默认为arima，具体支持模型见下面说明

如果没有数据，本开源项目提供股票数据获取脚本

```bash
python stock_hisdata_get.py -code cn_600517 -start_time_str 20240601 -end_time_str 20250701
```

其中，code上述已说明，start_time_str和end_time_str分别为开始时间和结束时间。

## 支持模型

**1. arima**

ARIMA（Autoregressive Integrated Moving Average）是一种广泛应用于时间序列预测的统计模型，其基本原理结合了自回归（AR）、差分（I）和移动平均（MA）三个核心概念。自回归（AR）部分通过历史观测值的线性组合来捕捉序列的自相关性；差分（I）处理非平稳性问题，通过对原始序列进行差分转换使其变为平稳序列；移动平均（MA）则利用过去预测误差的线性组合来提高预测精度。ARIMA 模型的参数 (p,d,q) 分别对应自回归阶数、差分阶数和移动平均阶数，通过这三个参数的合理选择，模型能够适应不同特性的时间序列数据，从而实现对未来值的有效预测。

p,d,q值的确认，由于股票数据为非平均，因此差分阶数d选取1，其他p、q值采用搜索评价取最优，经过对比当p、q值为6时，效果最好。各值评价结果如下：

p| q |  RMSE
-|-|-|
0 | 0 | 14.61
1 | 0 | 14.68
0 | 1 | 14.68
1 | 1 | 14.66
2 | 2 | 14.15
3 | 3 | 14.03
4 | 4 | 16.28
5 | 5 | 13.64
**6** | **6** | **11.64**
7 | 7 | 14.18
8 | 8 | 13.57
9 | 9 | 14.48

**2. chronos_bolt_model**

Chronos-Bolt-Base 是基于 T5 架构的时间序列预测模型。它在近 1000 亿个时间序列观测数据上进行训练，通过将历史时间序列上下文分块输入编码器，解码器直接生成分位数预测，相比原始 Chronos 模型快 250 倍，内存效率高 20 倍。该模型零样本预测能力出色，在 27 个数据集上优于常用统计模型和深度学习模型，且预测精度比原始 Chronos（Large）模型更高。

本开源项目提供零样本训练好的模型，可以直接使用预测，由于零样本训练只是推导时间频率和暂存模型，因此可以不用进行零样本训练，如果想要尝试，准备好训练文件数据，文件和预测文件格式一致，放在data/chronos-bolt-traindata下，执行如下命令：

```bash
python chronos_bolt_model.py
```
如果有算力的小伙伴想要微调，可以将如下代码块中的注释拿掉，并调整参数，一般情况下经过微调的效果更佳。

```bash
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
```

## 模型效果评测对比

模型评测集选取包括主要指数和典型的个股一共225个数据，涵盖不同行业、市值和市盈率，评测指标有：

**RMSE：Root Mean Squared Error，均方根误差，是衡量预测值与实际值之间差异的常用指标，计算方式是均方误差（MSE）的平方根，其值越小表示模型预测精度越高。**

**趋势准确率ACC：预测整体的涨跌趋势，结果一共有涨或跌两种，涨或跌的判断用线性回归拟合后的斜率来判断**

**评测结果如下（按照RMSE升序排列）**

模型名称| RMSE |  趋势准确率ACC
-|-|-|
ARIMA | 11.64  | 待评测
chronos_bolt_model | 15.24 | 待评测


## Star历史

[![Star History Chart](https://api.star-history.com/svg?repos=chenking2020/zeroshot-astock-predict&type=Date)](https://star-history.com/#chenking2020/zeroshot-astock-predict&Date)