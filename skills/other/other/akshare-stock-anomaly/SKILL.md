---
name: akshare-stock-anomaly
description: 用于基于AkShare数据的股票异常检测场景。适用于金融工作中的基础任务单元。
---

# AkShare A股单股票异常行为识别 Skill

## 数据来源

本 Skill 使用 **AkShare** 提供的 A 股行情数据接口进行异常行为识别，核心数据源为：

- `ak.stock_zh_a_hist`：获取单只 A 股的历史行情数据（开盘、收盘、最高、最低、成交量、成交额、振幅、涨跌幅、涨跌额、换手率等）。

说明：
- 默认基于日频后复权（`adjust="qfq"`）历史数据进行分析。
- 若目标股票停牌、退市、无足够历史数据，模型输出可能为空或不稳定。
- 本 Skill 依赖公开市场行情数据，不直接使用逐笔成交、盘口、席位或账户级数据，因此识别结果属于**行情驱动的异常行为代理识别**。

## 功能

本 Skill 针对**单只 A 股股票**进行异常行为识别，并输出异常标签、异常分数和明细说明。当前支持以下识别能力：

1. **异常涨跌幅识别**
   - 基于滚动窗口收益率分布，识别显著偏离常态的单日涨跌。

2. **异常成交量识别**
   - 基于成交量滚动均值与标准差，识别放量或缩量异常。

3. **异常振幅识别**
   - 识别单日振幅显著高于历史常态的交易日。

4. **异常换手识别**
   - 对有换手率字段的数据进行滚动异常检测。

5. **连续异动识别**
   - 识别短期内连续多日大涨、大跌或持续放量的异常模式。

6. **综合风险标签输出**
   - 将异常行为聚合为标签，例如：
     - `price_spike_up`
     - `price_spike_down`
     - `volume_spike`
     - `amplitude_spike`
     - `turnover_spike`
     - `consecutive_abnormal_move`
     - `behavior_watchlist`

7. **结果导出**
   - 输出 JSON 结果，便于被其他策略、风控流程或自动化任务调用。

## 使用示例

### 1. 安装依赖

```bash
pip install akshare pandas numpy
```

### 2. 执行识别

```bash
python script/detect_abnormal_behavior.py --symbol 600519 --start 20230101 --end 20260301
```

### 3. 指定滚动窗口和 z-score 阈值

```bash
python script/detect_abnormal_behavior.py \
  --symbol 000001 \
  --start 20220101 \
  --end 20260301 \
  --window 20 \
  --z-threshold 2.5
```

### 4. 输出示例

```json
{
  "symbol": "000001",
  "last_date": "2026-02-28",
  "risk_score": 74.0,
  "labels": [
    "price_spike_down",
    "volume_spike",
    "consecutive_abnormal_move",
    "behavior_watchlist"
  ],
  "latest_metrics": {
    "pct_change": -6.12,
    "volume_zscore": 3.41,
    "amplitude": 8.55,
    "amplitude_zscore": 2.98,
    "turnover": 5.21,
    "turnover_zscore": 2.21
  },
  "explanations": [
    "最新交易日涨跌幅显著偏离近20日分布",
    "最新交易日成交量显著高于近20日均值",
    "最近3个交易日存在连续异常波动"
  ]
}
```

## 交易说明

1. 本 Skill 面向**研究、监控、风控预警**场景，不构成投资建议。
2. “异常行为”仅表示该股票近期交易特征偏离其历史常态，不等同于违法违规、操纵市场或内幕交易判断。
3. A 股存在涨跌停、停牌、复牌、除权除息、ST 风险警示等制度因素，可能导致统计指标出现结构性跳变。
4. 对低流动性股票、上市时间较短股票、长期停牌后复牌股票，异常标签可能更敏感。
5. 建议将本 Skill 与以下信息联合使用：
   - 公司公告
   - 财务信息
   - 行业事件
   - 龙虎榜/资金流
   - 新闻舆情
6. 若用于实盘风控，建议增加：
   - 最低成交额过滤
   - ST / *ST 过滤
   - 上市天数过滤
   - 财务与合规风险过滤
   - 多周期共振确认

## License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
