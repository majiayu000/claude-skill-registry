---
name: a-share-etf
description: A股ETF分析/行业ETF对比/ETF筛选与持仓。当用户说"ETF"、"指数基金"、"行业ETF"、"宽基ETF"、"ETF推荐"、"XX行业有什么ETF"、"ETF规模"、"场内基金"、"ETF溢价"、"LOF"、"ETF对比"、"ETF持仓"、"ETF分析"、"沪深300ETF"、"中证500ETF"、"创业板ETF"、"科创50ETF"时触发。MUST USE when user asks about ETF analysis, ETF comparison, ETF screening, ETF holdings, or any exchange-traded fund related queries for A-share market. 基于 akshare ETF数据分析ETF行情、规模变化、溢折价、行业覆盖、持仓分析。支持研报风格（formal）和快速解读风格（brief）。
---

# A股ETF分析助手

## 数据源

```bash
SCRIPTS="$SKILLS_ROOT/cn-stock-data/scripts"

# ETF实时行情（akshare）
python -c "import akshare as ak; df=ak.fund_etf_spot_em(); print(df.head(10).to_json(orient='records', force_ascii=False))"

# ETF历史行情
python -c "import akshare as ak; df=ak.fund_etf_hist_em(symbol='510300', period='daily', start_date='20260101', end_date='20260315'); print(df.to_json(orient='records', force_ascii=False))"

# 跟踪指数行情
python "$SCRIPTS/cn_stock_data.py" kline --code [指数代码] --freq daily --start [日期]
```

补充：通过 web 搜索获取 ETF 持仓明细、基金规模变化、申购赎回情况。

## Workflow

1. **确定分析模式**：单只ETF分析 / 行业ETF对比 / 宽基ETF对比 / ETF规模趋势
2. **数据获取**：ETF行情 + 跟踪指数行情 + 规模数据
3. **分析维度**：跟踪误差、费率、规模、流动性、溢折价
4. **对比分析**：同类ETF横向对比（跟踪同一指数的不同ETF）
5. **输出**：根据 style 参数选择 formal（研报风格）或 brief（快速解读）

## 关键规则

1. ETF规模越大流动性越好，优先推荐规模 >10亿 的产品
2. 跟踪误差是ETF质量的核心指标，年化跟踪误差 <2% 为优秀
3. 溢价率过高时买入有风险（T+1日可能折价回归），提醒用户注意
4. 区分 ETF（场内交易）和 ETF联接基金（场外申赎），不要混淆
5. 费率对比需包含管理费+托管费，低费率长期影响显著
6. 跨境ETF/QDII-ETF 有额度限制，溢价可能持续较久，需特别说明

## 输出格式

### formal（研报风格）
- 标题 + 摘要
- 基本信息表格（代码、名称、跟踪指数、规模、费率、管理人）
- 行情走势分析（附关键价格数据）
- 跟踪误差与溢折价分析
- 同类对比表格
- 投资建议与风险提示

### brief（快速解读）
- 一句话结论
- 核心数据（规模/费率/溢折价）
- 关键风险点

## 参考资料

详见 [references/etf-guide.md](references/etf-guide.md)：ETF分类、核心ETF清单、选择指标、溢折价分析、行业轮动策略。
