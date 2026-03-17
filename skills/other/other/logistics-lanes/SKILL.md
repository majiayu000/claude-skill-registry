---
name: logistics-lanes
description: Analyze carrier performance and shipping lane efficiency
user-invocable: true
---

You are helping the operations team analyze carrier performance and shipping lane efficiency.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__query`).

Follow these steps:

### Step 1: Determine Analysis Focus

Ask the user what they want to analyze:
- **Carrier comparison** — performance across carriers (UPS, FedEx, USPS, etc.)
- **Lane analysis** — origin-to-destination shipping lane performance
- **Cost efficiency** — cost per package by carrier/lane
- **Transit time** — delivery speed by carrier and region

### Step 2: Discover and Query Data

Use `mcp__snowflake__search_tables` to find shipment and carrier tables.

Then use `mcp__snowflake__query` to pull carrier performance data. Also use `mcp__snowflake__get_cost_breakdown` with category "fulfillment" for cost context.

### Step 3: Analyze Performance

Present analysis based on the focus area:

**Carrier Comparison:**
- On-time delivery rate by carrier
- Average transit time by carrier
- Cost per shipment by carrier
- Exception rate by carrier

**Lane Analysis:**
- Top shipping lanes by volume
- Fastest/slowest lanes
- Lanes with highest exception rates
- Regional delivery performance

**Cost Efficiency:**
- Cost per package by carrier and service level
- Weight-based cost analysis
- Zone-based shipping cost trends
- Opportunities for carrier negotiation

### Step 4: Recommendations

Based on the analysis, suggest:
- Carrier allocation changes to optimize cost/speed tradeoffs
- Lanes that should switch carriers
- Volume thresholds for rate negotiations
- Service level adjustments by region

### Step 5: Follow-Up

Offer:
- **Shipping margin analysis** — `/jf-operations-center:shipping-margin`
- **Fulfillment status** — `/jf-operations-center:fulfillment-status`
- **Ops dashboard** — `/jf-operations-center:ops-dashboard`

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking the HORIZON_SNOWFLAKE_TOKEN
- If carrier data is limited, note which data points are available and which are not
- If table structure is unfamiliar, use `mcp__snowflake__describe_table` to understand available columns
