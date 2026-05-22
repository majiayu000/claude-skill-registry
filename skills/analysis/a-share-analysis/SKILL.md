---
name: a-share-analysis
description: Comprehensive China A-share stock analysis covering fundamental analysis, technical analysis, policy impact assessment, and market-specific features (T+1 trading, price limits, northbound capital flow). Use when user asks about A股分析, Chinese mainland stocks, Shanghai/Shenzhen listed stocks, or needs analysis considering China market characteristics.
---

# A股分析 (China A-Share Analysis)

## Overview

Perform comprehensive analysis of China A-share stocks (Shanghai and Shenzhen exchanges) with consideration of unique market characteristics including T+1 trading rules, price limits, policy impacts, and capital flow dynamics.

## Market Characteristics

### Trading Rules
- **T+1 Settlement**: Stocks bought today can only be sold the next trading day
- **Price Limits**:
  - Main board: ±10% daily limit
  - ChiNext (创业板) & STAR Market (科创板): ±20% daily limit
  - ST stocks: ±5% daily limit
  - New IPO: No limit for first 5 trading days (ChiNext/STAR)
- **Trading Hours**: 9:30-11:30, 13:00-15:00 (Beijing Time)
- **Call Auction**: 9:15-9:25 (opening), 14:57-15:00 (closing)

### Market Segments
- **Shanghai Main Board (沪市主板)**: 60xxxx - Large caps, SOEs
- **Shenzhen Main Board (深市主板)**: 00xxxx - Medium to large caps
- **ChiNext (创业板)**: 30xxxx - Growth/tech companies, ±20% limit
- **STAR Market (科创板)**: 688xxx - Innovation/tech, ±20% limit
- **Beijing Stock Exchange (北交所)**: 8xxxxx - SMEs

## Data Sources

Use web search to gather data from:

**Primary Sources:**
- 东方财富 (East Money) - eastmoney.com
- 同花顺 (10jqka) - 10jqka.com.cn
- 新浪财经 (Sina Finance) - finance.sina.com.cn
- 雪球 (Xueqiu) - xueqiu.com
- 巨潮资讯 (cninfo) - cninfo.com.cn (official filings)

**Search Strategy:**
- Use stock code or name + specific data needed
- Search in Chinese for better results: "[股票名称] 财务数据 2024"
- For northbound data: "[股票代码] 北向资金持股"
- For policy news: "[行业] 政策 最新"

## Analysis Framework

### 1. Basic Information
```
股票代码: [Code]
股票名称: [Name]
所属板块: [Board]
所属行业: [Industry]
市值: [Market Cap]
流通市值: [Float Market Cap]
```

### 2. Fundamental Analysis

**Financial Metrics:**
- 营业收入 (Revenue) - YoY growth
- 归母净利润 (Net Profit) - YoY growth
- 扣非净利润 (Non-GAAP Net Profit)
- 毛利率 (Gross Margin)
- 净利率 (Net Margin)
- ROE (净资产收益率)
- 资产负债率 (Debt Ratio)
- 经营现金流 (Operating Cash Flow)

**Valuation Metrics:**
- 市盈率 P/E (TTM & Forward)
- 市净率 P/B
- 市销率 P/S
- PEG比率
- Compare to industry average and historical range

**Quality Indicators:**
- 商誉占比 (Goodwill ratio)
- 应收账款周转 (Receivables turnover)
- 存货周转 (Inventory turnover)
- 研发投入占比 (R&D ratio)

### 3. Technical Analysis

**Price Action:**
- 当前价格 vs 涨跌停价
- 与均线关系 (5/10/20/60/120/250日)
- 支撑位/压力位
- 量价关系

**Indicators:**
- MACD (金叉/死叉)
- KDJ (超买/超卖)
- RSI
- 布林带位置

**Special Considerations:**
- 涨停板打开次数
- 连板天数 (for momentum)
- 封单量 (limit order volume)

### 4. Capital Flow Analysis

**北向资金 (Northbound Capital):**
- 持股数量变化
- 持股比例
- 近期增减仓情况
- 是否为陆股通标的

**主力资金 (Institutional Flow):**
- 主力净流入/流出
- 超大单/大单/中单/小单分布
- 近5日/10日资金流向

**股东分析:**
- 十大股东变化
- 十大流通股东
- 股东户数变化
- 机构持仓比例

### 5. Policy & News Analysis

**政策影响:**
- 行业政策利好/利空
- 监管政策变化
- 国家战略相关性 (新质生产力、自主可控等)

**公司动态:**
- 重大事项公告
- 股权激励/员工持股
- 回购/增减持
- 并购重组

**市场情绪:**
- 两融余额变化
- 龙虎榜信息
- 机构评级

## Output Format

### 分析报告模板

```markdown
# [股票名称] ([股票代码]) 分析报告

## 基本信息
| 指标 | 数值 |
|-----|------|
| 当前价格 | ¥XX.XX |
| 涨跌幅 | X.XX% |
| 市值 | XXX亿 |
| 流通市值 | XXX亿 |
| 所属行业 | XXX |
| 所属概念 | XXX |

## 财务分析

### 核心指标
| 指标 | 最新值 | 同比 | 行业平均 |
|-----|-------|------|---------|
| 营收 | | | |
| 净利润 | | | |
| 毛利率 | | | |
| ROE | | | |

### 估值分析
| 指标 | 当前 | 历史分位 | 行业平均 |
|-----|------|---------|---------|
| PE(TTM) | | | |
| PB | | | |
| PS | | | |

## 技术分析

### 趋势判断
- 短期趋势 (5-20日):
- 中期趋势 (20-60日):
- 长期趋势 (60日以上):

### 关键价位
- 压力位: ¥XX.XX, ¥XX.XX
- 支撑位: ¥XX.XX, ¥XX.XX
- 涨停价: ¥XX.XX
- 跌停价: ¥XX.XX

## 资金分析

### 北向资金
- 持股数量: XXX万股
- 持股比例: X.XX%
- 近期变化: 增持/减持 XXX万股

### 主力动向
- 5日主力净流入: XXX万
- 20日主力净流入: XXX万

## 风险提示
1. [风险1]
2. [风险2]
3. [风险3]

## 投资建议
- 操作建议: 买入/持有/观望/卖出
- 建议仓位: X成
- 目标价位: ¥XX.XX - ¥XX.XX
- 止损价位: ¥XX.XX

## 免责声明
本分析仅供参考，不构成投资建议。股市有风险，投资需谨慎。
```

## Special Analysis Types

### 涨停板分析
When stock hits price limit:
- 封单量/流通市值比
- 涨停原因 (利好消息、板块联动、游资炒作)
- 开板次数
- 连板可能性分析

### 龙虎榜分析
For stocks appearing on Dragon Tiger List:
- 买卖前五席位
- 机构 vs 游资
- 知名游资席位 (华泰证券深圳益田路等)
- 买卖差额

### 股东户数分析
- 户数增减趋势
- 户均持股变化
- 筹码集中度

## Example Queries

- "分析一下贵州茅台"
- "600519 财务分析"
- "宁德时代技术面怎么看"
- "比亚迪北向资金情况"
- "科创板XX公司值得投资吗"
- "这只股票涨停了，能追吗"
