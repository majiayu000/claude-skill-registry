---
name: a-share-insider
description: A股股东/高管增减持分析/内部人交易追踪。当用户说"增减持"、"减持"、"增持"、"大股东"、"高管买卖"、"insider"、"insider trading"、"XX的股东在减持吗"、"谁在增持"、"重要股东"、"举牌"、"解禁"、"股东增减持"、"高管增减持"、"大股东减持"、"内部人交易"时触发。MUST USE when user asks about insider trading, shareholder/executive buy/sell activities, share increase/decrease by major holders, or lock-up expiry impact. 基于 akshare 增减持数据和 cn-stock-data 行情数据，分析重要股东和高管的增减持行为、规模、动机和市场影响。支持研报风格（formal）和快速解读风格（brief）。不适用于基金持仓（用 a-share-fund-holding）或龙虎榜（用 a-share-dragon-tiger）。
---

# A股股东/高管增减持分析助手

## 数据源

```bash
SCRIPTS="$SKILLS_ROOT/cn-stock-data/scripts"

# 股东增减持数据（通过 akshare）
python -c "import akshare as ak; df=ak.stock_inner_trade_xq(); print(df.head(20).to_json(orient='records', force_ascii=False))"

# 十大股东（通过 efinance）
python -c "import efinance as ef; df=ef.stock.get_top10_stock_holder_info(stock_code='600519'); print(df.to_json(orient='records', force_ascii=False))"

# 个股行情
python "$SCRIPTS/cn_stock_data.py" quote --code [CODE]

# K线（看增减持前后走势）
python "$SCRIPTS/cn_stock_data.py" kline --code [CODE] --freq daily --start [日期]
```

补充：通过 web 搜索获取减持预告公告、解禁计划等。

## Workflow

### Step 1: 确定分析模式

根据用户意图分类：
- **个股增减持追踪**：某只股票的股东/高管增减持明细
- **全市场增减持统计**：近期增减持活跃个股概览
- **大股东行为分析**：特定股东（控股股东/机构）的持股变动

### Step 2: 数据获取

获取增减持明细 + 十大股东 + 个股行情 + 近期K线。多只股票时并行获取。

### Step 3: 行为分析

- **主体识别**：控股股东 / 5%+大股东 / 董监高 / 核心员工
- **规模评估**：减持/增持股数占总股本比例
- **方式判断**：集中竞价 / 大宗交易 / 协议转让
- **时间窗口**：是否在解禁后、业绩发布前后、股价高低点

> 详见 [references/insider-guide.md](references/insider-guide.md) 中的主体分类、减持限制和信号解读。

### Step 4: 信号研判

- **持续减持** = 潜在利空，关注减持节奏和剩余持股比例
- **高管增持** = 信心信号，尤其是自有资金增持
- **大股东举牌（≥5%）** = 战略布局，可能触发要约收购义务
- **回购** = 公司层面看好，注意区分注销式回购 vs 股权激励回购
- 结合行情走势、公告内容综合判断，避免单一信号定性

### Step 5: 输出

| 维度 | formal | brief |
|------|--------|-------|
| 输出格式 | 完整增减持分析报告 | 快速要点 |
| 主体分析 | 逐笔详细分析（金额/比例/方式） | 仅标注关键主体和方向 |
| 统计 | 增减持汇总+持股变动表 | 仅净增减方向和规模 |
| 结论 | 客观陈述（"控股股东累计减持X%"） | 可加简要判断 |

默认风格：brief。用户要求"详细分析"/"出报告"时用 formal。

## 关键规则

1. **预披露要求**：大股东/5%以上股东减持需提前15个交易日预披露
2. **窗口期禁令**：高管在定期报告前30日、业绩预告前10日不得买卖
3. **区分计划与完成**：明确标注"计划减持"（预告）vs"已完成减持"（实际执行）
4. **锁定期**：IPO后通常12-36个月锁定期，定增6-18个月，到期≠立即减持
5. **不做交易建议**：只陈述增减持事实和信号含义，不建议"跟随买入/卖出"
6. **数据时效**：增减持公告可能滞后，分析时注明数据截止日期
