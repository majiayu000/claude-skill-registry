---
name: executive-summary
description: Generate a consolidated KPI executive summary with narrative
user-invocable: true
---

You are helping executive leadership get a consolidated view of business performance.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__get_consolidated_kpis`).

Follow these steps:

### Step 1: Gather Parameters

Ask the user for:
- **Period**: What time window? (mtd, qtd, ytd, or last_30d — default: last_30d)

### Step 2: Pull Consolidated KPIs

Use `mcp__snowflake__get_consolidated_kpis` with the user's period parameter.

### Step 3: Build Executive Narrative

Present the data as an executive summary with:

**Performance Headline**
- One-sentence summary of overall business health
- Key metric: total revenue and growth rate

**Revenue & Growth**
- Total revenue for the period
- Period-over-period growth rate
- Revenue by channel with channel mix percentages
- Top performing and underperforming channels

**Profitability**
- Gross margin % and trend
- Key cost drivers
- Unit economics highlights

**Operational Health**
- Fulfillment SLA compliance
- Inventory coverage status
- Exception rate

**Strategic Outlook**
- Key risks and opportunities
- Items requiring executive attention

Delegate narrative construction to the `narrative-builder` agent for polished prose.

### Step 4: Follow-Up

Offer:
- **Investor metrics package** — `/jf-executive-suite:investor-metrics`
- **Build a presentation deck** — `/jf-executive-suite:build-deck`
- **Strategic scenario modeling** — `/jf-executive-suite:scenario-model`
- **Portfolio project status** — `/jf-executive-suite:portfolio-status`

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking the HORIZON_SNOWFLAKE_TOKEN
- If KPI data is partial, build the summary from available data and note gaps
