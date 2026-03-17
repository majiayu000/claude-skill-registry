---
name: scenario-model
description: Build financial what-if scenarios using current data as baseline
user-invocable: true
---

You are helping the finance team build financial what-if scenarios.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__get_pnl_summary`).

Follow these steps:

### Step 1: Establish Baseline

Pull current financial data to use as the baseline:
- Use `mcp__snowflake__get_pnl_summary` for the most recent period
- Use `mcp__snowflake__get_unit_economics` for per-unit metrics
- Use `mcp__snowflake__get_channel_revenue` for channel mix

Present the baseline to the user.

### Step 2: Define Scenarios

Ask the user what they want to model. Common scenarios:
- **Price change** — "What if we raise DTC prices by 10%?"
- **Volume change** — "What if Amazon volume grows 20%?"
- **Cost change** — "What if COGS increases by 5%?"
- **Channel mix** — "What if wholesale grows to 30% of revenue?"
- **New product launch** — "What if we add a new SKU at $X price point?"

Let the user define 1-3 scenarios to compare.

### Step 3: Model Each Scenario

For each scenario, calculate the impact on:
- Revenue (by channel and total)
- COGS and gross margin
- Contribution margin per unit
- Total contribution
- Break-even implications

Delegate complex modeling to the `scenario-generator` and `scenario-evaluator` agents.

### Step 4: Compare Scenarios

Present a comparison table:
- Baseline vs each scenario
- Key metric changes (revenue, margin %, contribution)
- Risk factors for each scenario
- Sensitivity analysis (which assumptions matter most)

### Step 5: Recommendation

Based on the analysis:
- Identify the highest-impact scenario
- Note key assumptions and risks
- Suggest what additional data would improve confidence

### Step 6: Follow-Up

Offer:
- **Refine a scenario** with adjusted assumptions
- **P&L report** — `/jf-financial-analyst:pnl-report`
- **Demand forecast** — `/jf-financial-analyst:forecast-demand`

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking the HORIZON_SNOWFLAKE_TOKEN
- If baseline data is incomplete, note which assumptions must be user-provided vs data-driven
