---
name: dr-extract
description: Extract validated financial data from Datarails Finance OS to Excel. Creates workbooks with P&L, Balance Sheet, KPIs (including ARR), and validation checks.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__extract_financials
  - Read
argument-hint: "[--output <file>] [--scenario <name>] [--year <YYYY>]"
---

# Datarails Financial Data Extraction

Extract validated financial data from Finance OS to Excel workbooks with:
- **P&L Data**: Revenue, COGS, Operating Expenses by month
- **KPI Data**: ARR, Net New ARR, Churn, LTV, Revenue by quarter
- **Validation**: Cross-checks between P&L and KPI tables

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--output <file>` | Output filename | `tmp/Financial_Extract_YYYY.xlsx` |
| `--scenario <name>` | Primary scenario | `Actuals` |
| `--year <YYYY>` | Calendar year to extract | Current year |

## Workflow

### Step 1: Verify Connection

If any Datarails tool call fails with an authentication or connection error, tell the user:

> The Datarails connector isn't connected. Click the **"+"** button next to the prompt, select **Connectors**, find **Datarails**, and click **Connect**.

Then STOP — do not retry until the user has reconnected.

### Step 2: Run Extraction via MCP Tool

Call the `extract_financials` MCP tool with the parsed arguments:

```
Use: extract_financials
Arguments:
  year: <parsed year, default current year>
  scenario: <parsed scenario, default "Actuals">
  output_path: <parsed output, or omit for default>
```

The tool handles:
- Loading the client profile for the environment
- Pagination (500 rows per request) with auto token refresh
- Client-side aggregation
- Excel generation with openpyxl

### Step 3: Report Results

Present the extraction summary to the user:
- Output file path
- Year and scenario extracted
- Any errors or warnings

## Expected Output

The tool generates an Excel workbook with:
1. **Summary sheet**: Key totals and metrics
2. **P&L sheet**: Monthly breakdown by account category
3. **KPIs sheet**: Quarterly KPI values
4. **Validation sheet**: Cross-checks and profile info

Output location: `tmp/` folder (configurable via `--output`)

## Troubleshooting

### "profile_not_found" error
Run `/dr-learn` first to create a profile.

### "missing_dependency" error
The MCP server is hosted remotely — this error should not occur. If it does, contact support.

### Token expires during extraction
The script auto-refreshes tokens every 20K rows. If you still get 401 errors:
1. Reconnect via Connectors UI ("+" > Connectors > Datarails)

### Missing months in data
Check `System_Year` filter value - must be a **string** ("2025"), not integer.

## Related Skills

- Connect via Connectors UI first
- `/dr-learn` - Create/update client profile
- `/dr-tables` - Explore available tables
- `/dr-query` - Investigate specific records
