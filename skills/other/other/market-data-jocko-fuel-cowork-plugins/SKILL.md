---
name: market-data
description: Pull Circana retail POS analytics for a product category
user-invocable: true
---

You are helping the sales team analyze Circana retail POS market data. This data lives in Snowflake (`PROD_JOCKOFUEL_DWH.SIGMAWRITE`) and covers 324M+ records across 62 retailers and 110 weeks.

### Step 1: Understand the Request

Ask the user what they want to analyze:
- **Category**: Which product segment? (e.g., RTD Energy, Protein Powder, Bars)
- **Retailer**: Specific retailer or total MULO?
- **Time period**: Latest 4 weeks, 12 weeks, 52 weeks, or custom?
- **Metric focus**: Dollar sales, unit sales, market share, velocity, distribution?

### Step 2: Route the Analysis

Based on the request, delegate to the appropriate agent:
- **Market share and trends** → `market-analyst` agent
- **Competitive positioning** → `buyer-strategist` agent
- **Data quality concerns** → `data-validator` agent
- **Data freshness check** → `freshness-monitor` agent

Use the `market-router` agent if the intent is ambiguous.

### Step 3: Check Data Freshness

Before running analysis, verify data currency via `freshness-monitor`. If data is older than 14 days, warn the user about staleness.

### Step 4: Present Results

Format results for the sales context:
- Key metrics with period-over-period comparisons
- Jocko Fuel performance vs category and top competitors
- Retailer-specific insights where relevant
- Actionable takeaways for sales conversations

### Step 5: Follow-Up

Offer:
- **Deeper dive** on a specific retailer or competitor
- **Buyer presentation** — `/jf-market-intel:buyer-presentation`
- **Export** data for a deck or spreadsheet

### Error Handling

- If Snowflake connection fails, inform the user and suggest checking VPN/credentials
- If the requested segment doesn't exist, show available segments from `SEGMENTATION_LOGIC.md`
