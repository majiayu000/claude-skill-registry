---
name: dr-anomalies-report
description: Generate comprehensive anomaly detection report with Excel deliverables. Discovers data quality issues without requiring configuration.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_finance_tables
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__profile_numeric_fields
  - mcp__datarails-finance-os__profile_categorical_fields
  - mcp__datarails-finance-os__detect_anomalies
  - mcp__datarails-finance-os__get_records_by_filter
  - Write
  - Read
  - Bash
argument-hint: "[--table-id <id>] [--severity <level>] [--output <file>]"
---

# Anomaly Detection Report

Generate comprehensive data quality assessment report with automated anomaly detection.

This skill automatically discovers your data structure and detects issues without requiring pre-configuration. Works with any Datarails Finance OS table.

## Design Principles

**General-Purpose**:
- ✅ No hardcoded table IDs or field names
- ✅ Adapts to any client structure
- ✅ Works with and without client profiles
- ✅ Falls back to discovery mode if profile missing

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--table-id <id>` | Specific table to analyze | Uses profile or discovers automatically |
| `--severity <level>` | Filter results: critical, high, medium, low | All |
| `--output <file>` | Output filename | `tmp/Anomaly_Report_TIMESTAMP.xlsx` |

## What It Reports

### Summary Sheet
- **Data Quality Score** (0-100)
- Health status indicator
- Anomaly count by severity
- Key metrics

### Critical Findings Sheet
- Anomalies requiring immediate attention
- Sample records for investigation
- Field-specific details
- Recommended actions

### High Priority Sheet
- Issues to address this week
- Full descriptions
- Count and context

### Analysis Sheets
- **Numeric Analysis**: Min, max, mean, std dev for numeric fields
- **Categorical Analysis**: Distinct values, cardinality, frequency
- **Sample Records**: Actual data samples for top anomalies

## Workflow

**Phase 1: Discovery**
1. Verify connection (if tools fail, guide user to Connectors UI)
2. If no `--table-id`, discover tables or use profile
3. Load table schema

**Phase 2: Anomaly Detection**
1. Run `detect_anomalies` - Automated data quality checks
2. Profile numeric fields - Statistics and outliers
3. Profile categorical fields - Cardinality and frequencies
4. Fetch sample records - Get actual data for investigation

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

**Phase 3: Report Generation**
1. Categorize findings by severity
2. Generate Excel workbook with multiple sheets
3. Apply professional formatting
4. Calculate data quality score

**Phase 4: Summary**
1. Display key findings
2. Show health status
3. Guide next steps

## Examples

### Analyze default financials table
```bash
/dr-anomalies-report
```

Output:
```
🔍 Discovering financials table...
✓ Found financials table: TABLE_ID

📊 Analyzing table TABLE_ID...
  🔬 Running anomaly detection...
  📈 Profiling numeric fields...
  📝 Profiling categorical fields...
  🔍 Fetching sample records...
  📊 Summarizing results...
  📄 Generating Excel report...

✅ Report generated: tmp/Anomaly_Report_2026-02-03_143022.xlsx

==================================================
ANOMALY DETECTION SUMMARY
==================================================
Table: TABLE_ID
Total Anomalies: 45
Data Quality Score: 87/100

By Severity:
  Critical: 2
  High: 8
  Medium: 23
  Low: 12

Report: tmp/Anomaly_Report_2026-02-03_143022.xlsx
==================================================
```

### Analyze specific table for critical issues only
```bash
/dr-anomalies-report --table-id TABLE_ID --severity critical
```

### Save to custom location
```bash
/dr-anomalies-report --env app --output tmp/Quality_Check_Feb_2026.xlsx
```

## Data Quality Score

Score ranges from 0-100:
- **90-100** ✅ **Excellent** - Minimal issues, data is reliable
- **80-90** 🟢 **Good** - Minor issues, generally usable
- **70-80** 🟡 **Fair** - Moderate issues, needs attention
- **70** 🟠 **Poor** - Significant issues, requires action
- **<70** 🔴 **Critical** - Major issues, immediate action required

Calculation:
```
Score = 100 - (critical×10 + high×5 + medium×2 + low×0.5)
Clamped to 0-100 range
```

## Adaptive Behavior

### With Client Profile
- Uses table IDs from `config/client-profiles/<env>.json`
- Uses discovered field names and mappings
- Applies business rules from profile notes

### Without Client Profile
- Lists available tables
- Automatically discovers table schema
- Infers field purposes from names and data types
- Uses general data quality rules

### Fallback Discovery
If profile incomplete or unavailable:
1. List all Finance OS tables
2. Identify likely data tables (those with numeric fields)
3. Get full schema
4. Discover field purposes automatically
5. Run analysis

## Use Cases

### Monthly Data Quality Check
```bash
/dr-anomalies-report --env app --output tmp/DQ_Check_$(date +%Y-%m).xlsx
```

### Pre-Month-End Close Validation
```bash
/dr-anomalies-report --severity critical
```
*Alerts on critical issues that could affect close*

### Department Data Audit
```bash
/dr-anomalies-report --table-id 12345 --severity high
```
*Checks specific department data for issues*

### Exploratory Analysis
```bash
/dr-anomalies-report --table-id unknown_table_id
```
*Discovers what's in an unfamiliar table*

## Output Files

Reports are saved to: `tmp/Anomaly_Report_YYYY-MM-DD_HHMMSS.xlsx`

Each report includes:
- Professional formatting with colors
- Severity-based highlighting
- Embedded sample data
- Statistical analysis
- Investigation queries

## Troubleshooting

**"Not authenticated" error**
- Connect via Connectors UI ("+" > Connectors > Datarails > Connect)

**"No tables found" error**
- Check that authentication succeeded
- Verify you have access to Finance OS

**"Table not found" error**
- Verify table ID is correct
- Run `/dr-tables` to see available tables

**"Incomplete profile" error**
- Run `/dr-learn` to refresh profile
- Or specify `--table-id` to override

## Related Skills

- `/dr-tables` - List and explore available tables
- `/dr-learn` - Discover and create client profiles
- `/dr-extract` - Extract validated financial data
- `/dr-reconcile` - Compare P&L vs KPI data

## Performance

- Small tables (< 10K rows): ~30 seconds
- Medium tables (10-100K rows): ~1-2 minutes
- Large tables (100K+ rows): ~5-10 minutes

Scaling handled automatically via pagination and efficient MCP tools.
