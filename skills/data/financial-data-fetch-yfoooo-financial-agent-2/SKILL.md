---
name: financial-data-fetch
description: 获取中国A股和ETF市场数据。使用场景：(1) 查询股票历史数据，(2) 获取ETF净值走势，(3) 指定时间范围的数据提取。支持通过股票代码和天数参数获取OHLCV（开盘价、最高价、最低价、收盘价、成交量）数据。
license: MIT
allowed-tools:
  - fetch_stock_data
  - fetch_etf_data
metadata:
  version: "1.0.0"
  author: "YFOOOO"
  data_source: "AKShare"
---

# Financial Data Fetch Skill

统一的金融数据获取接口，支持中国A股和ETF市场数据查询。

## Overview

本 Skill 提供两个核心功能：
1. **股票数据获取** - 获取A股历史OHLCV数据
2. **ETF数据获取** - 获取ETF净值和成交量数据

所有数据来源于 AKShare，经过标准化处理，返回 pandas DataFrame 格式。

## Quick Start

### 1. 确定数据类型

根据用户需求判断是查询股票还是ETF：
- 股票代码通常为6位数字（如 `000001` 平安银行）
- ETF代码通常为6位数字（如 `510300` 沪深300ETF）

### 2. 提取参数

从用户查询中提取：
- **symbol**: 股票/ETF代码（6位数字）
- **days**: 数据天数（默认30天，最大365天）

### 3. 调用工具

- 股票数据 → 使用 `fetch_stock_data`
- ETF数据 → 使用 `fetch_etf_data`

## Data Types

### Stock Data (A股)

**Tool**: `fetch_stock_data`

**Parameters**:
- `symbol` (str, required): 股票代码（6位数字，如 "000001"）
- `days` (int, optional): 数据天数，默认30天

**Returns**: pandas DataFrame with columns:
- `日期` (date): 交易日期
- `开盘` (float): 开盘价
- `收盘` (float): 收盘价
- `最高` (float): 最高价
- `最低` (float): 最低价
- `成交量` (int): 成交量
- `成交额` (float): 成交额
- `涨跌幅` (float): 涨跌幅（%）

**Example**:
```python
result = fetch_stock_data(symbol="000001", days=30)
# 返回平安银行最近30天的日K线数据
```

### ETF Data

**Tool**: `fetch_etf_data`

**Parameters**:
- `symbol` (str, required): ETF代码（6位数字，如 "510300"）
- `days` (int, optional): 数据天数，默认30天

**Returns**: pandas DataFrame with columns:
- `日期` (date): 交易日期
- `开盘` (float): 开盘价
- `收盘` (float): 收盘价
- `最高` (float): 最高价
- `最低` (float): 最低价
- `成交量` (int): 成交量

**Example**:
```python
result = fetch_etf_data(symbol="510300", days=60)
# 返回沪深300ETF最近60天的数据
```

## Error Handling

### 1. 代码不存在
如果股票/ETF代码不存在，返回明确错误信息：
```
错误：股票代码 'XXXXXX' 不存在或已退市
```

### 2. 网络超时
自动重试3次，每次间隔2秒：
```
重试 1/3: 网络请求超时，正在重试...
```

### 3. 数据为空
如果查询结果为空（如停牌），提示用户调整参数：
```
警告：未获取到数据，可能原因：
- 股票代码错误
- 查询时间范围内无交易数据
- 股票已退市或长期停牌
```

### 4. 参数验证
- `symbol` 必须为6位数字
- `days` 必须在 [1, 365] 范围内

## Decision Tree

```
用户查询
    ├─ 包含"股票"、"A股"关键字？
    │   └─ 是 → 使用 fetch_stock_data
    │
    ├─ 包含"ETF"、"基金"关键字？
    │   └─ 是 → 使用 fetch_etf_data
    │
    └─ 仅提供代码？
        ├─ 检查代码是否为6位数字
        ├─ 默认使用 fetch_stock_data
        └─ 如果失败，尝试 fetch_etf_data
```

## Performance Notes

- **响应时间**: 通常 < 3秒
- **数据更新**: 实时同步交易所数据（有15分钟延迟）
- **并发限制**: 建议单次查询，避免频繁请求

## References

详细 API 文档和数据源说明见：
- [AKShare API 文档](references/akshare_api.md)
- [数据格式说明](references/data_schema.md)

## Script Implementation

数据获取逻辑实现在：
- `scripts/fetch_stock.py` - 股票数据获取
- `scripts/fetch_etf.py` - ETF数据获取

这些脚本复用项目中的 `core/data_fetcher.py` 模块，确保代码一致性。
