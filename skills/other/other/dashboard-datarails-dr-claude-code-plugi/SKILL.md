---
name: dr-dashboard
description: Generate executive KPI dashboard with real-time metrics. Creates Excel dashboards and PowerPoint one-pagers.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__aggregate_table_data
  - Write
  - Read
  - Bash
argument-hint: "[--period <YYYY-MM>] [--output-xlsx <file>] [--output-pptx <file>]"
---

# Executive KPI Dashboard

Generate real-time KPI monitoring dashboards for executive teams.

Creates both Excel dashboards (for analysis) and PowerPoint one-pagers (for meetings).

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--period <YYYY-MM>` | Month to dashboard for | Current month |
| `--output-xlsx <file>` | Excel output path | `tmp/Executive_Dashboard_TIMESTAMP.xlsx` |
| `--output-pptx <file>` | PowerPoint output path | `tmp/Dashboard_OnePager_TIMESTAMP.pptx` |

## Key Metrics Included

**Growth & Revenue**:
- ARR (Annual Recurring Revenue)
- Revenue
- MoM/QoQ growth rates

**Health & Efficiency**:
- Churn rate (%)
- LTV (Lifetime Value)
- CAC (Customer Acquisition Cost)

**Operational**:
- Burn rate (monthly)
- Runway (months of cash)
- Burn multiple

**Custom Metrics**: Any KPI in your data (adapts to profile)

## Datarails Brand Styling

When generating Excel or PowerPoint files, apply Datarails brand styling:

**Font:** Poppins (fall back to Calibri if unavailable). Weights: 400 regular, 600 semibold, 700 bold.

**Colors:**
| Role | Hex | Use |
|------|-----|-----|
| Navy | `0C142B` | Header/banner background |
| Main text | `333333` | Primary text |
| Secondary | `6D6E6F` | Muted/subtitle text |
| Border | `9EA1AA` | Cell borders |
| Section bg | `F2F2FB` | Section header / row header background (lavender) |
| Input bg | `EAEAFF` | Editable/input cell background |
| Input text | `4646CE` | Editable cell text (indigo) |
| Favorable | `2ECC71` | Positive variance / good KPI delta |
| Unfavorable | `E74C3C` | Negative variance / bad KPI delta |
| Chart 1 | `0C142B` | Actuals (navy) |
| Chart 2 | `F93576` | Budget (hot pink) |
| Chart 3 | `00B4D8` | Teal |
| Chart 4 | `FFA30F` | Amber |

**Excel layout:**
- Content starts at column B (column A is a narrow gutter)
- Rows 1-6: header banner with navy background, white title text, white subtitle
- Gridlines OFF. Freeze panes at B7.
- Footer as last row with generation date
- Every cell must have font, fill, alignment, and number format set

**Number formats:** `_(* #,##0_);_(* (#,##0);_(* "-"_);_(@_)` (default), `$#,##0` (dollars), `$#,##0.0,,"M"` (millions), `0.0%` (percent)

**Variance coloring:** Any cell showing a delta/change: green (`2ECC71`) if favorable, red (`E74C3C`) if unfavorable. Apply automatically based on value sign and metric context.

**PowerPoint:** Navy (`0C142B`) background, 16:9 widescreen, Poppins font, white text, amber (`FFA30F`) accent lines, card backgrounds `001F37`.

## Output

### Excel Dashboard
- Summary sheet with top KPIs
- All Metrics sheet with complete list
- Current values
- Status indicators (✅ or ⚠️)

### PowerPoint One-Pager
- Single professional slide
- Top metrics in boxes
- Color-coded for quick scanning
- Generated timestamp
- Perfect for executive team syncs

## Examples

### Generate current month dashboard
```bash
/dr-dashboard
```

Output:
```
📊 Generating dashboard for 2026-02...
  📈 Fetching KPI metrics...
  📊 Calculating trends...
  📋 Generating Excel dashboard...
  🎯 Generating PowerPoint one-pager...

✅ Dashboard generated successfully

==================================================
EXECUTIVE DASHBOARD
==================================================
Period: 2026-02
Metrics: 7

Outputs:
  Excel: tmp/Executive_Dashboard_2026-02-03_143022.xlsx
  PowerPoint: tmp/Dashboard_OnePager_2026-02-03_143022.pptx
==================================================
```

### Specific month
```bash
/dr-dashboard --period 2025-12
```

### With custom locations
```bash
/dr-dashboard \
  --output-xlsx reports/dashboard.xlsx \
  --output-pptx reports/dashboard.pptx
```

## Use Cases

### Daily Executive Sync
```bash
/dr-dashboard  # Use PowerPoint for standup
```

### Weekly Team Update
```bash
# Share Excel for details, PowerPoint for overview
/dr-dashboard
```

### Monthly Board Package
```bash
# Generate for month-end
/dr-dashboard --period 2026-01
```

### Investor Demo
```bash
# Professional one-pager
/dr-dashboard --output-pptx investors_dashboard.pptx
```

## Performance

- Generation: <2 minutes
- Real-time KPI data
- Scales to 100+ metrics
- Efficient aggregation

## Color Coding

- ✅ **Green** - Positive metrics (high revenue, low churn)
- ⚠️ **Yellow** - Needs attention (rising burn, declining growth)
- 🔴 **Red** - Critical (low runway, high churn)

## Features

**Excel Dashboard**:
- Sortable data
- Easy drill-down
- Print-friendly
- Shareable format

**PowerPoint One-Pager**:
- Executive-ready
- Meeting-ready (1 slide)
- Branded template
- Easy to share

## Automated Updates

Schedule weekly updates:
```bash
# Every Monday at 8 AM
0 8 * * 1 /dr-dashboard \
  --output-pptx reports/weekly_dashboard.pptx
```

## Integration

Works with:
- `/dr-insights` - Understand why metrics changed
- `/dr-reconcile` - Validate KPI accuracy
- `/dr-anomalies-report` - Check data quality
- `/dr-extract` - Get latest data

## Related Skills

- `/dr-insights` - Detailed trend analysis
- `/dr-reconcile` - Validate KPI accuracy
- `/dr-anomalies-report` - Check data quality
- `/dr-forecast-variance` - Forecast vs actual
