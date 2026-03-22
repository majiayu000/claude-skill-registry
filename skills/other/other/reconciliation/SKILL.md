---
name: dr-reconcile
description: Reconcile P&L vs KPI data sources. Validates consistency and identifies discrepancies with variance analysis.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__aggregate_table_data
  - mcp__datarails-finance-os__list_finance_tables
  - Write
  - Read
  - Bash
argument-hint: "--year <YYYY> [--scenario <name>] [--tolerance-pct <#>] [--output <file>]"
---

# P&L vs KPI Reconciliation

Validate consistency between P&L and KPI data sources. Identifies discrepancies and explains variances.

Essential for month-end close and financial validation.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--year <YYYY>` | **REQUIRED** Calendar year to reconcile | — |
| `--scenario <name>` | Scenario to reconcile | `Actuals` |
| `--tolerance-pct <#>` | Acceptable variance threshold | `5.0` |
| `--output <file>` | Output file path | `tmp/Reconciliation_YYYY_TIMESTAMP.xlsx` |

## What It Validates

### Revenue Consistency
- P&L Revenue vs KPI Revenue
- Within tolerance threshold
- Identifies timing differences

### Expense Completeness
- COGS + Operating Expense coverage
- Validation of expense structure
- Missing expense categories

### Data Completeness
- All expected accounts present
- All expected KPI metrics available
- Data quality validation

### Variance Analysis
- Absolute variance amounts
- Percentage variance
- Tolerance compliance
- Root cause identification

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

Excel report with multiple sheets:

1. **Summary** - Pass/fail status, metrics, exception count
2. **Validation Rules** - Detailed results of each check
3. **Exceptions** (if any) - Issues exceeding tolerance
4. **P&L Summary** - Revenue, expenses by account
5. **KPI Summary** - All KPI values for verification

## Examples

### Reconcile current year (default 5% tolerance)
```bash
/dr-reconcile --year 2025
```

### Strict reconciliation (1% tolerance)
```bash
/dr-reconcile --year 2025 --tolerance-pct 1.0
```

### Reconcile specific scenario
```bash
/dr-reconcile --year 2025 --scenario Forecast
```

### Custom output location
```bash
/dr-reconcile --year 2025 --output reports/reconciliation_2025.xlsx
```

## Use Cases

### Month-End Close
Run after data extraction to validate:
```bash
/dr-extract --year 2025
/dr-anomalies-report --severity critical    # Check quality
/dr-reconcile --year 2025 --tolerance-pct 2 # Validate consistency
```

### Financial Review
Reconcile before presentations:
```bash
/dr-reconcile --year 2025 --scenario Actuals
```

### Audit Preparation
Reconcile with strict tolerance:
```bash
/dr-reconcile --year 2025 --tolerance-pct 0.5
```

## Performance

- Year reconciliation: ~30-60 seconds
- Includes 3+ validation checks
- Scalable to large data volumes

## Error Handling

**"Revenue not found"** - Check P&L vs KPI account names in profile

**"Variance exceeds tolerance"** - Review exception sheet for details

**"Incomplete data"** - Run `/dr-extract` to refresh data first

## Related Skills

- `/dr-extract` - Get latest financial data
- `/dr-anomalies-report` - Check data quality
- `/dr-dashboard` - Verify KPI values
- `/dr-insights` - Understand trends driving reconciliation items
