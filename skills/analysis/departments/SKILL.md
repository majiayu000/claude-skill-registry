---
name: dr-departments
description: Analyze P&L and performance by department. Creates departmental reports and comparative analysis with Excel and PowerPoint outputs.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__aggregate_table_data
  - Write
  - Read
  - Bash
argument-hint: "--year <YYYY> [--department <name>] [--output-xlsx <file>] [--output-pptx <file>]"
---

# Department Analytics

Analyze departmental P&L performance and resource allocation.

Creates detailed departmental reports for team leads and management reviews.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--year <YYYY>` | **REQUIRED** Calendar year | — |
| `--department <name>` | Specific department (optional) | All departments |
| `--output-xlsx <file>` | Excel output path | `tmp/Department_Analysis_YYYY_TIMESTAMP.xlsx` |
| `--output-pptx <file>` | PowerPoint output path | `tmp/Department_Review_YYYY_TIMESTAMP.pptx` |

## Department Metrics

### Revenue & Expense
- Department revenue
- Expense breakdown
- Net contribution

### Performance
- Budget vs actual
- Variance analysis
- Year-over-year comparison

### Efficiency
- Per-employee metrics
- Cost per unit
- Productivity indicators

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

### Excel Department Pack
- Summary by department
- Detailed P&L per department
- Variance analysis
- Comparison charts

### PowerPoint Department Review
- One slide per department
- Key metrics highlight
- Budget performance
- Comparison to average

## Examples

### Analyze all departments
```bash
/dr-departments --year 2025
```

### Specific department review
```bash
/dr-departments --year 2025 --department Engineering
```

### Custom output
```bash
/dr-departments --year 2025 \
  --output-xlsx reports/depts_2025.xlsx \
  --output-pptx reports/dept_review.pptx
```

## Use Cases

### Monthly Department Reviews
```bash
# Share with department heads
/dr-departments --year 2025
```

### Department Head Meetings
```bash
# Individual department analysis for team
/dr-departments --year 2025 --department Marketing
```

### Executive Dashboard
```bash
# Department comparison for leadership
/dr-departments --year 2025
```

### Budget Planning
```bash
# Department historical analysis
/dr-departments --year 2024
/dr-departments --year 2025
# Use for next year planning
```

## Performance

- Analysis: 1-2 minutes
- Scales to all departments
- Professional output

## Department Metrics Included

**Financial**:
- Revenue
- Expenses
- Net contribution

**Operational**:
- Headcount
- Per-employee metrics
- Productivity

**Performance**:
- Budget variance
- Trend analysis
- YoY comparison

## Features

**Excel Report**:
- Summary by department
- Per-department P&L sheets
- Sortable data
- Print-friendly

**PowerPoint Review**:
- One slide per dept
- Key metrics
- Trend indicators
- Professional layout

## Integration

Works with:
- `/dr-insights` - Context for trends
- `/dr-dashboard` - Department KPIs
- `/dr-reconcile` - Validation
- `/dr-extract` - Data sourcing

## Related Skills

- `/dr-insights` - Trend analysis
- `/dr-dashboard` - KPI monitoring
- `/dr-reconcile` - Data validation
- `/dr-extract` - Data extraction
