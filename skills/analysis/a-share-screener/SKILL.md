---
name: a-share-screener
description: Screen and filter A-share stocks based on fundamental metrics, technical indicators, capital flow, and custom criteria. Support multiple screening strategies including value investing, growth investing, momentum trading, and dividend hunting. Use when user wants to find stocks meeting specific criteria like "低PE高ROE股票", "北向资金加仓股", "突破年线的股票".
---

# A股选股器 (A-Share Stock Screener)

## Overview

Screen A-share stocks using various criteria including fundamental metrics, technical indicators, capital flow patterns, and combined strategies. Support preset screening strategies and custom filter combinations.

## Screening Categories

### 1. Fundamental Screening (基本面选股)

**Value Metrics (价值指标):**
| Metric | Chinese | Typical Criteria |
|--------|---------|-----------------|
| P/E Ratio | 市盈率 | < 15 (value), < 行业均值 |
| P/B Ratio | 市净率 | < 1.5, < 行业均值 |
| P/S Ratio | 市销率 | < 2 |
| PEG Ratio | PEG | < 1 (被低估) |
| Dividend Yield | 股息率 | > 3% |
| EV/EBITDA | | < 10 |

**Quality Metrics (质量指标):**
| Metric | Chinese | Typical Criteria |
|--------|---------|-----------------|
| ROE | 净资产收益率 | > 15% |
| ROA | 总资产收益率 | > 5% |
| Gross Margin | 毛利率 | > 30% |
| Net Margin | 净利率 | > 10% |
| Operating Cash Flow | 经营现金流 | > 净利润 |

**Growth Metrics (成长指标):**
| Metric | Chinese | Typical Criteria |
|--------|---------|-----------------|
| Revenue Growth | 营收增速 | > 20% YoY |
| Profit Growth | 利润增速 | > 20% YoY |
| EPS Growth | 每股收益增速 | > 15% |
| 3Y CAGR | 三年复合增长率 | > 15% |

**Financial Health (财务健康):**
| Metric | Chinese | Typical Criteria |
|--------|---------|-----------------|
| Debt Ratio | 资产负债率 | < 60% |
| Current Ratio | 流动比率 | > 1.5 |
| Quick Ratio | 速动比率 | > 1 |
| Interest Coverage | 利息保障倍数 | > 3 |
| Cash/Debt | 货币资金/有息负债 | > 1 |

### 2. Technical Screening (技术面选股)

**Trend Filters (趋势筛选):**
| Criteria | Chinese | Description |
|----------|---------|-------------|
| Above MA200 | 站上年线 | 价格 > 200日均线 |
| Above MA60 | 站上季线 | 价格 > 60日均线 |
| Golden Cross | 金叉 | 短期均线上穿长期均线 |
| Death Cross | 死叉 | 短期均线下穿长期均线 |
| New High | 创新高 | 52周/历史新高 |
| Breakout | 突破 | 突破关键阻力位 |

**Momentum Filters (动量筛选):**
| Criteria | Chinese | Description |
|----------|---------|-------------|
| RSI | RSI指标 | RSI > 50 (上涨趋势) |
| MACD | MACD | MACD > 0 或金叉 |
| Volume Surge | 放量 | 成交量 > 5日均量 x 2 |
| Price Range | 振幅 | 近期振幅筛选 |

**Pattern Filters (形态筛选):**
- 连续涨停
- 涨停后缩量整理
- 底部放量
- W底形态
- 头肩底形态

### 3. Capital Flow Screening (资金面选股)

**Northbound Capital (北向资金):**
| Criteria | Chinese | Description |
|----------|---------|-------------|
| NB Holdings | 北向持仓 | 北向持股比例 > X% |
| NB Increasing | 北向加仓 | 近N日北向净买入 |
| NB Heavy | 北向重仓 | 北向持股市值前100 |

**Institutional Flow (主力资金):**
| Criteria | Chinese | Description |
|----------|---------|-------------|
| Main Inflow | 主力净流入 | 近N日主力净流入 > X亿 |
| Big Order Net | 大单净买 | 大单净买入额 > X亿 |
| Dragon Tiger | 龙虎榜 | 近期上榜 |

**Shareholder Analysis (股东分析):**
| Criteria | Chinese | Description |
|----------|---------|-------------|
| Holder Decrease | 股东户数减少 | 筹码集中 |
| Institution Increase | 机构增持 | 机构持仓增加 |
| Buyback | 回购 | 公司回购股票 |

### 4. Market Segment Screening (板块筛选)

**By Board (按板块):**
- 沪市主板 (60开头)
- 深市主板 (00开头)
- 创业板 (30开头)
- 科创板 (688开头)
- 北交所 (8开头)

**By Index (按指数):**
- 沪深300成分股
- 中证500成分股
- 创业板50成分股
- 科创50成分股
- MSCI中国成分股

**By Industry (按行业):**
- 申万一级/二级/三级行业
- 同花顺行业分类
- Wind行业分类

**By Concept (按概念):**
- 热门概念板块
- 政策受益概念
- 国企改革、专精特新等

## Preset Screening Strategies

### Strategy 1: 价值投资选股
```
筛选条件:
- PE < 15 AND PE > 0
- PB < 2
- ROE > 12%
- 资产负债率 < 60%
- 股息率 > 2%
- 市值 > 100亿
```

### Strategy 2: 成长股选股
```
筛选条件:
- 营收增速 > 20%
- 净利润增速 > 25%
- ROE > 15%
- 毛利率 > 30%
- PEG < 1.5
- 经营现金流 > 0
```

### Strategy 3: 白马股选股
```
筛选条件:
- 沪深300成分股
- ROE > 15% (连续3年)
- 净利润增速 > 10%
- 资产负债率 < 70%
- 北向持股比例 > 2%
```

### Strategy 4: 高股息选股
```
筛选条件:
- 股息率 > 4%
- 连续分红年数 > 5年
- 分红率 > 30%
- ROE > 10%
- 资产负债率 < 60%
```

### Strategy 5: 北向资金重仓
```
筛选条件:
- 北向持股比例 > 5%
- 近20日北向净买入 > 0
- 市值 > 200亿
- PE < 30
```

### Strategy 6: 技术突破选股
```
筛选条件:
- 今日收盘 > 20日均线
- 今日收盘 > 60日均线
- 5日均线 > 20日均线
- 成交量 > 5日均量
- MACD > 0
```

### Strategy 7: 超跌反弹选股
```
筛选条件:
- 近20日跌幅 > 15%
- RSI < 30
- 市净率 < 行业平均
- ROE > 8%
- 股东户数近期减少
```

### Strategy 8: 涨停板战法
```
筛选条件:
- 今日涨停或近3日有涨停
- 换手率 < 15%
- 市值 < 200亿
- 非ST股票
- 成交额 > 1亿
```

## Output Format

### Screening Results Template
```markdown
# 选股结果: [策略名称]

## 筛选条件
| 条件 | 设置值 |
|-----|-------|
| [条件1] | [值] |
| [条件2] | [值] |
| ... | ... |

## 筛选结果 (共X只)

| 代码 | 名称 | 行业 | 市值 | PE | PB | ROE | 股息率 | 涨跌幅 |
|-----|------|-----|------|----|----|-----|-------|-------|
| 600519 | 贵州茅台 | 白酒 | XXXX亿 | XX | XX | XX% | X.X% | X.XX% |
| ... | | | | | | | | |

## 重点关注 (Top 5)

### 1. [股票名称] ([代码])
- **入选理由:** [符合条件的关键指标]
- **亮点:** [投资亮点]
- **风险:** [主要风险点]

### 2. [股票名称] ([代码])
...

## 筛选说明
[对本次筛选结果的整体评价和投资建议]
```

### Comparison Template
```markdown
# 选股对比: [股票列表]

## 基本面对比
| 指标 | [股票1] | [股票2] | [股票3] | 优选 |
|-----|---------|---------|---------|------|
| PE | | | | |
| PB | | | | |
| ROE | | | | |
| 增速 | | | | |
| 股息率 | | | | |

## 技术面对比
| 指标 | [股票1] | [股票2] | [股票3] | 优选 |
|-----|---------|---------|---------|------|
| 趋势 | | | | |
| 位置 | | | | |
| 动量 | | | | |

## 综合评分
| 股票 | 基本面 | 技术面 | 资金面 | 综合 |
|-----|-------|-------|-------|------|
| | X/10 | X/10 | X/10 | X/10 |

## 投资建议
[综合分析后的投资建议]
```

## Data Sources

**Use web search to query:**
- 东方财富选股器: "东方财富 选股 [条件]"
- 同花顺i问财: "i问财 [自然语言条件]"
- 雪球选股: "雪球 筛选 [条件]"

**Natural Language Queries:**
- "PE低于15 ROE大于15的股票"
- "北向资金连续5日加仓的股票"
- "创业板 近期突破年线的股票"
- "高股息 低估值 的银行股"

## Example Queries

**基本面选股:**
- "帮我找低估值高分红的股票"
- "ROE大于20%的消费股有哪些"
- "筛选PEG小于1的成长股"
- "资产负债率低于50%的科技股"

**技术面选股:**
- "找出突破年线的股票"
- "最近金叉的蓝筹股"
- "创新高的股票有哪些"
- "超跌反弹的候选股票"

**资金面选股:**
- "北向资金重仓的股票"
- "主力连续流入的股票"
- "股东户数持续减少的股票"
- "近期龙虎榜机构买入的股票"

**组合筛选:**
- "给我一个价值投资选股结果"
- "用白马股策略筛选"
- "找高股息低波动的股票做防守"
- "用CANSLIM方法选股"

**自定义筛选:**
- "PE<20, ROE>15%, 市值>100亿, 北向持股>3%"
- "创业板, 近一年涨幅<-30%, PB<3"
