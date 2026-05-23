---
name: hk-stock-analysis
description: Comprehensive Hong Kong stock analysis covering H-shares, Red Chips, local HK stocks, AH premium analysis, Stock Connect flows, and HK market characteristics (T+0, no price limits, short selling). Use when user asks about 港股分析, Hong Kong listed stocks, H shares, or needs analysis considering HK market features.
---

# 港股分析 (Hong Kong Stock Analysis)

## Overview

Perform comprehensive analysis of Hong Kong listed stocks with consideration of unique market characteristics including T+0 trading, no price limits, short selling mechanism, and cross-border capital flows via Stock Connect.

## Market Characteristics

### Trading Rules
- **T+0 Trading**: Can buy and sell same day (no T+1 restriction)
- **No Price Limits**: No daily limit up/down (unlike A-shares)
- **Short Selling**: Allowed for designated securities
- **Settlement**: T+2
- **Trading Hours**:
  - Morning: 9:30-12:00
  - Afternoon: 13:00-16:00
  - Pre-opening: 9:00-9:30
- **Lot Size**: Varies by stock (often 100, 200, 400, 500, 1000, 2000)
- **Currency**: HKD (some stocks trade in USD/RMB)

### Stock Categories

**H-Shares (H股)**
- Mainland companies listed in HK
- Examples: 中国平安(02318), 工商银行(01398)
- Subject to CSRC approval

**Red Chips (红筹股)**
- HK-incorporated companies controlled by mainland entities
- Examples: 中国移动(00941), 中海油(00883)

**Local HK Stocks (本地股)**
- HK-headquartered companies
- Examples: 长实集团(01113), 新鸿基地产(00016)

**Chinese Concept Stocks (中概股)**
- Chinese companies listed via VIE structure
- Examples: 阿里巴巴(09988), 腾讯控股(00700)

### Key Indices
- 恒生指数 (HSI) - Hang Seng Index
- 恒生科技指数 (HSTECH) - Hang Seng Tech Index
- 恒生中国企业指数 (HSCEI) - H-share Index
- 恒生国企指数

## Data Sources

**Primary Sources:**
- 港交所披露易 (HKEX) - hkexnews.hk
- 阿斯达克财经 (AAStocks) - aastocks.com
- 经济通 (ET Net) - etnet.com.hk
- 富途牛牛 (Futu) - futunn.com
- 雪球港股 (Xueqiu) - xueqiu.com

**Search Strategy:**
- Use HK stock code with .HK suffix
- Search: "[股票名称] 港股 财务数据"
- For AH premium: "[公司名称] AH溢价"
- For southbound: "[股票代码] 南向资金"

## Analysis Framework

### 1. Basic Information
```
股票代码: [Code].HK
股票名称: [Name]
股票类型: H股/红筹/本地股/中概股
所属行业: [Industry]
市值: [Market Cap in HKD/USD]
每手股数: [Lot Size]
是否港股通标的: 是/否
```

### 2. AH Premium Analysis (For Dual-Listed)

**AH溢价指标:**
```
A股价格: ¥XX.XX
H股价格: HK$XX.XX
当前汇率: 1 HKD = XX CNY
AH溢价率: XX% (A股相对H股溢价/折价)
历史溢价区间: XX% - XX%
当前分位: XX%
```

**溢价分析要点:**
- 溢价率 > 30%: A股高估或H股低估
- 溢价率 < 0%: H股高估或A股低估
- 关注溢价收敛机会
- 考虑汇率波动影响

### 3. Fundamental Analysis

**Financial Metrics (Based on HK Accounting Standards):**
- 营业收入 (Revenue)
- 股东应占溢利 (Profit Attributable to Shareholders)
- 每股盈利 EPS
- 每股派息 DPS
- 派息比率 (Payout Ratio)
- 股息率 (Dividend Yield)
- 市盈率 P/E
- 市净率 P/B

**港股特色指标:**
- 每股净资产 (NAV per share)
- 折让率 (Discount to NAV) - for property stocks
- 内含价值 (EV) - for insurance stocks
- 重估净资产 (Revalued NAV)

### 4. Technical Analysis

**价格分析:**
- 当前价格
- 52周高低
- 与均线关系 (10/20/50/200日)
- 支撑位/压力位

**港股特有考虑:**
- 无涨跌停，波动可能较大
- 关注成交量变化 (港股流动性差异大)
- 做空比率 (Short Interest)
- 沽空金额/成交金额比

**指标:**
- MACD
- RSI
- 布林带
- 成交量分析

### 5. Capital Flow Analysis

**南向资金 (Southbound Capital):**
```
港股通持股: XXX万股
占已发行股本: X.XX%
近期变化: 增持/减持
南向资金净买入 (近5日): XXX亿港元
```

**机构持仓:**
- 基金持仓比例
- 大股东增减持
- 回购情况

**沽空数据:**
- 沽空股数
- 沽空金额
- 沽空比率
- 借货利率

### 6. Liquidity Analysis

**流动性指标:**
- 日均成交额 (20日)
- 换手率
- 买卖价差 (Bid-Ask Spread)
- 每手金额

**流动性风险评估:**
- 低流动性警示 (日均成交<1000万港元)
- 大额交易冲击成本估算

## Output Format

### 分析报告模板

```markdown
# [股票名称] ([股票代码].HK) 港股分析报告

## 基本信息
| 指标 | 数值 |
|-----|------|
| 当前价格 | HK$XX.XX |
| 涨跌幅 | X.XX% |
| 市值 | XX亿港元 |
| 每手股数 | XXX股 |
| 每手金额 | HK$XXXX |
| 股票类型 | H股/红筹/本地股 |
| 港股通标的 | 是/否 |

## AH溢价分析 (如适用)
| 指标 | 数值 |
|-----|------|
| A股价格 | ¥XX.XX |
| H股价格 | HK$XX.XX |
| 当前溢价率 | XX% |
| 历史平均溢价 | XX% |
| 投资建议 | 偏好A/偏好H/中性 |

## 财务分析

### 核心指标
| 指标 | 最新值 | 同比变化 |
|-----|-------|---------|
| 营收 | | |
| 归母净利 | | |
| EPS | | |
| 股息率 | | |
| ROE | | |

### 估值水平
| 指标 | 当前 | 历史均值 | 同业对比 |
|-----|------|---------|---------|
| PE | | | |
| PB | | | |
| 股息率 | | | |

## 技术分析

### 趋势判断
- 短期:
- 中期:
- 长期:

### 关键价位
- 压力位: HK$XX.XX
- 支撑位: HK$XX.XX
- 52周高: HK$XX.XX
- 52周低: HK$XX.XX

## 资金与流动性

### 南向资金
- 港股通持股: XXX万股 (X.XX%)
- 近期变化:

### 沽空数据
- 沽空比率: X.XX%
- 沽空趋势:

### 流动性评估
- 日均成交额: XXX万港元
- 流动性评级: 优/良/中/差

## 风险提示
1. [港股特有风险: 流动性、汇率等]
2. [公司特定风险]
3. [行业/政策风险]

## 投资建议
- 操作建议: 买入/持有/观望/卖出
- 目标价: HK$XX.XX
- 止损价: HK$XX.XX
- 适合投资者: [描述]

## 免责声明
本分析仅供参考，不构成投资建议。港股市场无涨跌停限制，波动风险较大。
```

## Special Analysis Types

### AH股套利分析
For dual-listed stocks:
- Current premium/discount
- Historical premium range
- Convergence opportunity assessment
- Consider: currency risk, trading cost, settlement difference

### 港股通标的筛选
Criteria for southbound eligible stocks:
- Index constituents
- Market cap requirements
- Liquidity requirements

### 高息股分析
Hong Kong dividend stocks:
- Dividend yield sustainability
- Payout ratio trends
- Currency of dividend (HKD/USD/RMB)
- Withholding tax considerations

### 老千股识别
Warning signs for potential "penny stock traps":
- 频繁供股/配股 (frequent rights issues)
- 大比例合股后再拆股
- 关联交易频繁
- 业绩长期亏损但不退市
- 成交极度稀少

## Example Queries

- "分析腾讯控股"
- "00700 基本面怎么样"
- "比亚迪AH溢价多少，买哪个合适"
- "港股高息股推荐"
- "恒生科技指数成分股分析"
- "这只港股流动性怎么样"
- "港股通净买入最多的股票"
