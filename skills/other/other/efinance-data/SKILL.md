---
name: efinance-data
description: "efinance 中国金融市场数据获取工具，封装 A 股行情、资金流向、龙虎榜、十大股东、业绩报表、基金净值持仓、可转债、期货等数据接口。当用户需要获取 A 股实时行情、个股资金流、主力动向、龙虎榜、十大股东变动、业绩数据、基金净值或持仓、可转债或期货行情时使用此 skill。也适用于需要中国金融市场数据来支撑投研分析、个股研究、行业对比、资产配置等场景。与 akshare-finance 互补，efinance 在资金流分层（主力/大单/超大单）和实时行情字段丰富度上更有优势。"
---

# efinance 中国金融市场数据工具

## 定位

efinance-data 是一个**数据获取工具层 skill**，为投研分析类 skill 提供底层数据支撑。它封装了 efinance 库的核心接口，覆盖 A 股、基金、可转债、期货四大品类。

数据来源为东方财富等公开财经网站，完全免费，无需注册或 API Key。

## 何时使用

- 用户要查某只股票的实时行情、历史K线
- 用户要看个股资金流向（主力净流入、大单、超大单）
- 用户要查龙虎榜、十大股东、业绩报表
- 用户要获取基金净值、重仓股、行业分布
- 用户需要可转债行情或期货行情
- 其他投研 skill 需要数据输入时，作为数据源调用

## 依赖

```bash
pip install efinance pandas
```

运行脚本前确认依赖已安装。如果 `import efinance` 报错，先执行上述安装命令。

## 脚本一览

所有脚本位于本 skill 的 `scripts/` 目录，输出均为 JSON 格式。

| 脚本 | 用途 | 核心命令 |
|------|------|---------|
| `stock_data.py` | 股票数据 | realtime / history / info / holders / bill / billboard / performance |
| `fund_data.py` | 基金数据 | history / position / industry / manager / period / info / codes |
| `bond_data.py` | 可转债数据 | realtime / history / info / all_info / bill |
| `futures_data.py` | 期货数据 | realtime / history / info |

## 股票数据 (stock_data.py)

### 实时行情

```bash
# 全市场 A 股实时行情（5800+ 只）
python stock_data.py realtime

# 指定股票
python stock_data.py realtime --code 000001,600519,000858
```

返回字段：代码、名称、最新价、涨跌幅、换手率、动态市盈率、总市值、流通市值等。

### 历史K线

```bash
# 日线（默认）
python stock_data.py history --code 600519

# 周线 / 月线
python stock_data.py history --code 600519 --period weekly
python stock_data.py history --code 600519 --period monthly

# 分钟级
python stock_data.py history --code 600519 --period 5min

# 指定时间范围
python stock_data.py history --code 600519 --start 20250101 --end 20251231
```

支持周期：daily / weekly / monthly / 5min / 15min / 30min / 60min

### 个股基本信息

```bash
python stock_data.py info --code 000001
```

返回：净利润、总市值、流通市值、所处行业、市盈率(动)、市净率、ROE、毛利率、净利率。

### 十大股东

```bash
python stock_data.py holders --code 000001
```

返回：股东名称、持股数、持股比例、增减、变动率。

### 资金流向

```bash
# 最近30天资金流
python stock_data.py bill --code 000001

# 最近60天
python stock_data.py bill --code 000001 --days 60

# 当日分时资金流
python stock_data.py today_bill --code 000001
```

返回字段包括：主力净流入、小单净流入、中单净流入、大单净流入、超大单净流入，以及各项占比。这是 efinance 相对其他数据源的核心优势——资金流分层非常细致。

### 龙虎榜

```bash
python stock_data.py billboard
```

返回：上榜股票、上榜日期、龙虎榜净买额、买入额、卖出额、上榜原因、机构买卖解读。

### 业绩报表

```bash
python stock_data.py performance
```

返回全市场最新业绩：营收、净利润、同比增长、每股收益、ROE、毛利率等。

### 其他

```bash
# 股东人数
python stock_data.py holder_number --code 000001

# 所属板块
python stock_data.py board --code 000001

# 逐笔成交
python stock_data.py deals --code 000001

# 最新IPO信息
python stock_data.py ipo
```

## 基金数据 (fund_data.py)

```bash
# 基金净值历史
python fund_data.py history --code 005827

# 批量获取多只基金
python fund_data.py history_multi --code 005827,110011,161725

# 基金重仓股
python fund_data.py position --code 005827

# 基金行业分布
python fund_data.py industry --code 005827

# 基金经理
python fund_data.py manager --code 005827

# 阶段涨幅（近1月/3月/1年等）
python fund_data.py period --code 005827

# 基金基本信息
python fund_data.py info --code 005827

# 基金代码列表
python fund_data.py codes
```

## 可转债数据 (bond_data.py)

```bash
# 可转债实时行情
python bond_data.py realtime

# 历史K线
python bond_data.py history --code 123456

# 全部可转债基本信息
python bond_data.py all_info

# 单只基本信息
python bond_data.py info --code 123456

# 资金流向
python bond_data.py bill --code 123456
```

注意：可转债实时行情接口偶尔因上游数据源问题返回错误，建议加 try/except 处理。

## 期货数据 (futures_data.py)

```bash
# 期货实时行情
python futures_data.py realtime

# 历史K线
python futures_data.py history --code 棕榈油2509

# 期货品种信息
python futures_data.py info
```

## 与 akshare-finance 的关系

两个 skill 互补使用：

| 数据需求 | 优先用 | 原因 |
|---------|-------|------|
| 资金流向（主力/大单分层） | efinance-data | 分层更细致 |
| 实时行情（含PE/市值） | efinance-data | 一次返回字段更全 |
| 龙虎榜（含解读） | efinance-data | 包含机构买卖成功率解读 |
| 财务三表（资产负债/利润/现金流） | akshare-finance | efinance 无此接口 |
| 北向资金 / 融资融券 | akshare-finance | efinance 无此接口 |
| 宏观经济（GDP/CPI/PMI） | akshare-finance | efinance 无此接口 |
| 估值指标详细历史 | akshare-finance | PE/PB 历史序列 |

当一个数据源出错时，可尝试用另一个获取相同数据作为备用。

## 注意事项

1. **数据来源**：公开财经网站（东方财富等），仅限学术研究和个人使用
2. **请求频率**：避免高频循环调用，建议间隔 0.5-1 秒
3. **交易时间外**：实时行情在非交易时段返回上一交易日数据
4. **数据延迟**：免费数据可能有 15 分钟延迟，不适用于实盘交易
5. **接口稳定性**：基于网页爬虫，上游网站改版可能导致接口暂时不可用

更多 API 细节见 `references/api_reference.md`。
