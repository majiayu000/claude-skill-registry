---
name: ar-aging
description: Generate an accounts receivable aging report
user-invocable: true
---

You are helping the finance team review accounts receivable aging.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__query`).

Follow these steps:

### Step 1: Determine Scope

Ask the user:
- **Channel filter**: Wholesale, DTC, Amazon, or all?
- **Aging buckets**: Standard (0-30, 31-60, 61-90, 90+) or custom?
- **Minimum balance**: Filter out small balances? (default: show all)

### Step 2: Discover AR Data

Use `mcp__snowflake__search_tables` with query "receivable" or "invoice" to find AR-related tables.

Then use `mcp__snowflake__describe_table` to understand the table structure.

### Step 3: Query AR Aging

Use `mcp__snowflake__query` to build an aging report. Group outstanding invoices by aging bucket:
- **Current (0-30 days)**
- **31-60 days**
- **61-90 days**
- **91+ days**

### Step 4: Present Results

Format as a standard AR aging report:
- Total outstanding by aging bucket
- Top 10 customers by outstanding balance
- Concentration risk (% of AR in 90+ bucket)
- Weighted average days outstanding

### Step 5: Highlight Risks

Flag:
- Accounts with balances in the 90+ bucket
- Large balances that have moved between buckets
- Customers with a pattern of late payment

### Step 6: Follow-Up

Offer:
- **P&L report** — `/jf-financial-analyst:pnl-report`
- **Unit economics** — `/jf-financial-analyst:unit-economics`
- Drill into a specific customer's payment history

### Error Handling

- If Snowflake MCP is unavailable, inform the user and suggest checking the HORIZON_SNOWFLAKE_TOKEN
- If AR data tables are not found, inform the user that AR data may not yet be available in Snowflake
- If table structure is unfamiliar, use `mcp__snowflake__describe_table` to understand available columns
