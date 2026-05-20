---
name: investor-metrics
description: Build an investor-ready metrics package with KPIs and financial summary
user-invocable: true
---

You are helping executive leadership prepare an investor-ready metrics package.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__get_consolidated_kpis`).

Follow these steps:

### Step 1: Gather Parameters

Ask the user:
- **Period**: What reporting period? (monthly, quarterly, annual)
- **Audience**: Existing investors, prospective investors, or board?
- **Focus areas**: Any specific metrics to emphasize?

### Step 2: Pull Financial Data

Gather comprehensive data:
- `mcp__snowflake__get_consolidated_kpis` — headline KPIs
- `mcp__snowflake__get_pnl_summary` — P&L detail
- `mcp__snowflake__get_channel_revenue` — channel breakdown
- `mcp__snowflake__get_unit_economics` — unit economics

### Step 3: Build Investor Package

Delegate to the `financial-modeler` agent to structure the metrics package:

**Section 1: Business Overview**
- Total revenue and growth rate
- Channel mix and diversification
- Customer metrics (if available)

**Section 2: Financial Performance**
- P&L summary (revenue, COGS, gross margin, EBITDA)
- Gross margin % and trend
- Unit economics by channel
- Revenue per customer metrics

**Section 3: Growth Metrics**
- Revenue growth rate (MoM, QoQ, YoY)
- Channel growth rates
- New customer acquisition (if available)
- Expansion revenue (if available)

**Section 4: Operational Efficiency**
- Fulfillment cost as % of revenue
- Customer acquisition cost (if available)
- LTV/CAC ratio (if available)

**Section 5: Forward Look**
- Revenue trajectory and guidance
- Key growth initiatives
- Risks and mitigations

### Step 4: Quality Check

Use the `data-validator` agent to verify:
- Numbers are internally consistent
- Growth rates are correctly calculated
- No data anomalies that would raise investor questions

### Step 5: Follow-Up

Offer:
- **Build a presentation deck** — `/jf-executive-suite:build-deck`
- **Scenario modeling** — `/jf-executive-suite:scenario-model`
- **Executive summary** — `/jf-executive-suite:executive-summary`

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking the HORIZON_SNOWFLAKE_TOKEN
- If certain metrics are unavailable, note gaps and suggest manual data entry
- Flag any data quality concerns before presenting to investors
