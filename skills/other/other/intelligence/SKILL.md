---
name: dr-intelligence
description: Generate comprehensive FP&A intelligence workbooks with auto-detected insights, recommendations, and professional Excel formatting. The most powerful financial analysis skill.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__generate_intelligence_workbook
  - Read
argument-hint: "--year <YYYY> [--output <file>]"
---

# FP&A Intelligence Workbook

Generate comprehensive FP&A intelligence workbooks with auto-detected insights, recommendations, and professional Excel formatting.

This is the **most powerful** financial analysis skill - it answers real business questions, not just data dumps.

## What Makes This Different

| Traditional Report | Intelligence Workbook |
|-------------------|----------------------|
| Shows data | Answers questions |
| Lists numbers | Explains "why" |
| Static tables | Highlights anomalies |
| Manual analysis | Insights auto-surfaced |
| Data dump | Recommendations included |

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--year <YYYY>` | **REQUIRED** Calendar year | -- |
| `--output <file>` | Output file path | `tmp/FPA_Intelligence_Workbook_YYYY_TIMESTAMP.xlsx` |

## Workflow

### Step 1: Verify Connection

If any Datarails tool call fails with an authentication or connection error, tell the user:

> The Datarails connector isn't connected. Click the **"+"** button next to the prompt, select **Connectors**, find **Datarails**, and click **Connect**.

Then STOP — do not retry until the user has reconnected.

### Step 2: Generate Workbook via MCP Tool

Call the `generate_intelligence_workbook` MCP tool with the parsed arguments:

```
Use: generate_intelligence_workbook
Arguments:
  year: <parsed year, REQUIRED>
  output_path: <parsed output, or omit for default>
```

The tool handles:
- Loading the client profile for the environment
- Fetching P&L data via aggregation (~5s per query)
- Fetching KPI, vendor, and cost center data
- Auto-substituting failed aggregation fields using profile alternatives
- Calculating insights and recommendations
- Generating 10-sheet Excel workbook with professional formatting

### Step 3: Report Results

Present the generation summary to the user:
- Output file path
- Year analyzed
- Any errors or warnings

## 10 Sheets Generated

1. **Insights Dashboard** - Top 5 findings with severity, key metrics with trends, recommendations
2. **Expense Deep Dive** - Top 20 expense accounts with % of total, MoM change
3. **Variance Waterfall** - What changed vs prior period and why
4. **Trend Analysis** - 12-month trends with growth rates
5. **Anomaly Report** - Auto-detected outliers with severity scores
6. **Vendor Analysis** - Top 20 vendors, concentration risk flags
7. **SaaS Metrics** - ARR waterfall, unit economics, efficiency ratios
8. **Sales Performance** - Rep leaderboard, cohort analysis
9. **Cost Center P&L** - Department-level detail
10. **Raw Data** - Pivot-ready dataset for your own analysis

## Auto-Generated Insights

The workbook automatically detects and surfaces:

| Insight Type | Detection Rule | Severity |
|--------------|----------------|----------|
| OpEx exceeds Revenue | OpEx/Revenue > 1.0 | CRITICAL |
| High expense growth | MoM change > 20% | WARNING |
| Vendor concentration | Single vendor > 10% of spend | INFO |
| Negative margins | Gross profit < 0 | CRITICAL |
| Unusual variance | > 3 std deviations | CRITICAL |

## Processing Time

- **With aggregation (typical):** ~30 seconds
- **With pagination fallback:** ~10 minutes for 50K+ rows

## Why This Matters

This workbook answers the **Top 10 Business Questions**:

1. **Where is the money going?** - Top 20 expense drivers
2. **What changed vs last month?** - MoM variance waterfall
3. **Which cost centers are over budget?** - Variance by department
4. **Are we efficient?** - OpEx as % of Revenue, Gross Margin
5. **What's unusual?** - Auto-detected anomalies
6. **Who are our biggest vendors?** - Top 10 vendor spend
7. **How are sales reps performing?** - Win rates, ARR by rep
8. **What's our burn situation?** - Runway, burn multiple
9. **What should we investigate?** - Exception report
10. **What actions to take?** - Automated recommendations

## Troubleshooting

### "profile_not_found" error
Run `/dr-learn` first to create a profile.

### "missing_dependency" error
The MCP server is hosted remotely — this error should not occur. If it does, contact support.

### Takes too long
- With aggregation: should complete in ~30 seconds
- Run `/dr-test` to check which fields support aggregation

### Missing data in sheets
- Check if profile has correct field mappings
- Run `/dr-learn` to refresh profile

## Related Skills

- `/dr-extract` - Basic data extraction (simpler, faster)
- `/dr-insights` - Executive PowerPoint + Excel combo
- `/dr-anomalies-report` - Focused on data quality issues
- `/dr-reconcile` - P&L vs KPI validation
