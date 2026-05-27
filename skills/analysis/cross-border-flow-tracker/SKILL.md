---
name: cross-border-flow-tracker
description: Track and analyze cross-border capital flows between mainland China and Hong Kong via Stock Connect (沪港通/深港通). Monitor northbound (北向资金) and southbound (南向资金) flows, identify trending stocks, and analyze institutional positioning. Use when user asks about 北向资金, 南向资金, 外资动向, Stock Connect flows, or cross-border investment trends.
---

# 跨境资金流向追踪 (Cross-Border Flow Tracker)

## Overview

Monitor and analyze capital flows between mainland China and Hong Kong through Stock Connect programs. Track northbound capital (北向资金 - foreign money into A-shares) and southbound capital (南向资金 - mainland money into HK stocks) to identify investment trends and institutional positioning.

## Stock Connect Overview

### Northbound (北向) - Into A-Shares
- **沪股通 (Shanghai Connect)**: Access Shanghai stocks
- **深股通 (Shenzhen Connect)**: Access Shenzhen stocks
- Daily quota: 520 billion RMB each way
- Eligible stocks: Major index constituents, large/mid caps

### Southbound (南向) - Into HK Stocks
- **港股通(沪) via Shanghai**: Access HK stocks
- **港股通(深) via Shenzhen**: Access HK stocks
- Daily quota: 420 billion RMB each way
- Eligible stocks: HSI/HSCEI constituents, large caps

## Data Sources

**Real-time & Daily Data:**
- 东方财富 - 北向资金 (eastmoney.com)
- 同花顺 - 资金流向 (10jqka.com.cn)
- 港交所 (HKEX) - 互联互通数据
- Wind资讯 (wind.com.cn)

**Search Strategy:**
- "北向资金今日流入" - Daily northbound flow
- "北向资金持股 [股票名称]" - Individual stock holdings
- "南向资金净买入" - Southbound net purchases
- "沪深港通 资金流向" - Overall Stock Connect flows

## Analysis Framework

### 1. Daily Flow Summary

```markdown
## 今日跨境资金流向

### 北向资金 (Northbound)
| 指标 | 数值 |
|-----|------|
| 沪股通净流入 | ¥XX.XX亿 |
| 深股通净流入 | ¥XX.XX亿 |
| 北向合计净流入 | ¥XX.XX亿 |
| 本周累计 | ¥XX.XX亿 |
| 本月累计 | ¥XX.XX亿 |
| 年初至今 | ¥XX.XX亿 |

### 南向资金 (Southbound)
| 指标 | 数值 |
|-----|------|
| 港股通(沪)净流入 | HK$XX.XX亿 |
| 港股通(深)净流入 | HK$XX.XX亿 |
| 南向合计净流入 | HK$XX.XX亿 |
| 本周累计 | HK$XX.XX亿 |
| 本月累计 | HK$XX.XX亿 |
```

### 2. Northbound Stock Holdings Analysis

**Top Holdings Changes:**
```markdown
### 北向资金持股变动 Top 10

#### 增持榜
| 股票 | 持股数量 | 变动数量 | 变动比例 | 持股市值 |
|-----|---------|---------|---------|---------|
| | | +XXX万股 | +X.XX% | ¥XX亿 |

#### 减持榜
| 股票 | 持股数量 | 变动数量 | 变动比例 | 持股市值 |
|-----|---------|---------|---------|---------|
| | | -XXX万股 | -X.XX% | ¥XX亿 |
```

**Individual Stock Query:**
```markdown
### [股票名称] 北向资金持仓分析

| 指标 | 数值 |
|-----|------|
| 北向持股数量 | XXX万股 |
| 占流通股比例 | X.XX% |
| 持股市值 | ¥XX.XX亿 |
| 近5日变动 | +/-XXX万股 |
| 近20日变动 | +/-XXX万股 |
| 近60日变动 | +/-XXX万股 |

#### 持股趋势
[描述近期增减持趋势和可能原因]
```

### 3. Southbound Stock Analysis

**Top Southbound Holdings:**
```markdown
### 南向资金持股 Top 20

| 排名 | 股票 | 持股数量 | 占比 | 持股市值 | 5日变动 |
|-----|-----|---------|-----|---------|--------|
| 1 | 腾讯控股 | XX亿股 | X.X% | XXXX亿 | +/-X% |
| 2 | ... | | | | |
```

### 4. Flow Trend Analysis

**Weekly/Monthly Patterns:**
- Identify consistent buying/selling patterns
- Correlate with market movements
- Identify sector preferences

**Seasonal Patterns:**
- MSCI rebalancing periods (Feb, May, Aug, Nov)
- Index reconstitution impacts
- Holiday effects (Chinese New Year, Golden Week)

### 5. Sector Flow Analysis

```markdown
### 北向资金行业配置

| 行业 | 持仓市值 | 占比 | 周变动 | 月变动 |
|-----|---------|-----|-------|-------|
| 食品饮料 | ¥XXXX亿 | XX% | +X% | +X% |
| 电力设备 | ¥XXXX亿 | XX% | -X% | +X% |
| 银行 | ¥XXXX亿 | XX% | +X% | -X% |
| 医药生物 | ¥XXXX亿 | XX% | +X% | +X% |
| ... | | | | |
```

## Signal Interpretation

### Bullish Signals (看多信号)
- 北向资金连续大幅净流入 (>50亿/日持续3天以上)
- 核心资产获持续加仓
- 外资持股比例创新高
- 流入与A股上涨同步

### Bearish Signals (看空信号)
- 北向资金持续净流出
- 重仓股被大幅减持
- 流出伴随指数下跌
- 外资对某行业系统性减仓

### Divergence Signals (背离信号)
- 市场下跌但北向持续流入 (可能底部)
- 市场上涨但北向持续流出 (可能顶部)
- 单只股票北向大买但股价不涨

## Output Templates

### Daily Report
```markdown
# 跨境资金日报 [日期]

## 市场概览
[今日A股/港股表现简述]

## 北向资金
- 今日净流入: ¥XX.XX亿
- 市场解读: [分析流入/流出原因]

### 重点增持
1. [股票1] +XX万股，[可能原因]
2. [股票2] +XX万股，[可能原因]

### 重点减持
1. [股票1] -XX万股，[可能原因]

## 南向资金
- 今日净流入: HK$XX.XX亿
- 重点标的: [列出主要买入股票]

## 后市展望
[基于资金流向的短期市场判断]
```

### Individual Stock Report
```markdown
# [股票名称] 外资持仓分析

## 北向持仓概览
[基本持仓数据表格]

## 持仓趋势
[图表描述或趋势分析]

## 与股价关系
[北向增减持与股价走势的相关性分析]

## 机构观点
[如有，列出相关外资机构的评级]

## 投资建议
[基于外资动向的操作建议]
```

## Example Queries

**日常查询:**
- "今天北向资金流向如何"
- "北向资金最近买了什么"
- "南向资金净买入排行"
- "本周外资流入最多的股票"

**个股查询:**
- "贵州茅台北向资金持仓多少"
- "宁德时代外资持股变化"
- "腾讯南向资金持仓情况"

**趋势分析:**
- "北向资金近期偏好什么行业"
- "外资连续加仓的股票有哪些"
- "北向资金持股比例最高的股票"

**信号分析:**
- "北向资金和大盘有背离吗"
- "哪些股票外资在悄悄建仓"
- "MSCI调整对北向资金影响"
