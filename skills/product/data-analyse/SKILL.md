---
name: data-analyse
description: Product management data analysis skill for defining metrics, building funnels/cohorts, diagnosing growth/retention, designing experiments, and translating insights into product actions. Use for tasks like metric trees, event taxonomy, dashboard requirements, SQL-style analysis plans, and decision memos.
---

# data-analyse

Use this skill for PM 视角的数据分析：把问题变成可量化指标与可执行动作。

## Outputs (choose what the task needs)

- Metric tree / North Star Metric decomposition
- Event taxonomy（埋点口径：事件名/属性/触发时机/去重规则）
- Analysis plan（要回答的问题、需要哪些数据、SQL/口径）
- Funnel / cohort definitions（留存、转化、激活）
- Experiment plan（假设、指标、样本量、guardrails）
- Insight → action memo（结论、证据、建议、风险）

## Workflow

1) Clarify the decision
- 业务问题是什么？要做哪个决策？“做/不做/怎么做”。
- 时间窗口：今天要结论，还是一周内可迭代？

2) Define metrics and guardrails
- North Star Metric + supporting metrics.
- Guardrails：错误率、退款/投诉、延迟、合规等。
- 明确口径：分母/分子、去重、时间窗、过滤条件。

3) Define data collection (events + properties)
- 事件命名一致、可组合。
- 属性尽量有限且可枚举；避免高基数字段（如 user_id 作为属性）。
- 明确客户端/服务端各自负责哪些事件。

4) Choose analysis methods
- Funnel：识别掉点（按渠道/人群/版本分群）。
- Cohort：留存与复购（D1/D7/D30）。
- Segmentation：新老用户、付费/非付费、不同入口。
- Causal thinking：区分相关与因果，避免幸存者偏差。

5) Recommend actions
- 针对最大掉点给 1–3 个高性价比改动。
- 每个改动配：预期影响、实现成本、风险与验证方式。

6) Experiment design (if needed)
- 先写假设：如果 X 改为 Y，会让指标 Z 提升，因为 ...
- 定义主指标、辅助指标、guardrails。
- 明确随机化单位（用户/会话/企业）和实验周期。

## Templates

### 埋点条目
- Event: `event_name`
- When: 触发时机
- Props: key/type/allowed values
- Dedup: 去重规则
- Owner: client/server

### Insight memo
- Question:
- Data:
- Findings:
- Interpretation:
- Recommendation:
- Risks:
- Next measurement:

