---
name: dr-audit
description: Generate SOX compliance audit reports with evidence packages. Creates professional PDF audit reports and Excel evidence workbooks.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__aggregate_table_data
  - Write
  - Read
  - Bash
argument-hint: "--year <YYYY> --quarter <Q#> [--output-pdf <file>] [--output-xlsx <file>]"
---

# SOX Compliance Audit

Generate professional SOX compliance audit reports with evidence packages.

Creates both PDF audit reports (for management) and Excel evidence workbooks (for audit trail).

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--year <YYYY>` | **REQUIRED** Calendar year | — |
| `--quarter <Q#>` | **REQUIRED** Quarter: Q1, Q2, Q3, Q4 | — |
| `--output-pdf <file>` | PDF output path | `tmp/Audit_Report_YYYY_QX_DATE.pdf` |
| `--output-xlsx <file>` | Excel evidence path | `tmp/Audit_Evidence_YYYY_QX_DATE.xlsx` |

## Control Testing

Performs comprehensive audit of key financial controls:

- **Data Completeness**: All expected periods present
- **Data Integrity**: No duplicate transactions
- **Access Control**: Authorized user access only
- **Change Management**: All changes documented
- **Reconciliation**: P&L vs KPI alignment

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

### PDF Audit Report
- Executive summary
- Control test results
- Exception findings
- Recommendations
- Management response section
- Control descriptions (appendix)

### Excel Evidence Package
- Control summary with status
- Detailed test results
- Exception log (if any)
- Supporting schedules
- Audit trail documentation

## Examples

### Q4 2025 Annual Audit
```bash
/dr-audit --year 2025 --quarter Q4
```

### Mid-year audit
```bash
/dr-audit --year 2025 --quarter Q2
```

### Custom output locations
```bash
/dr-audit --year 2025 --quarter Q4 \
  --output-pdf audits/audit_q4_2025.pdf \
  --output-xlsx audits/evidence_q4_2025.xlsx
```

## Use Cases

### Annual SOX Audit
```bash
# Run comprehensive audit for year-end
/dr-audit --year 2025 --quarter Q4
```

### Quarterly Board Review
```bash
# Regular compliance check
/dr-audit --year 2025 --quarter Q3
```

### Management Certification
```bash
# Support management's SOX 404 certification
/dr-audit --year 2025 --quarter Q4
```

### External Auditor Support
```bash
# Provide auditors with report and evidence
/dr-audit --year 2025 --quarter Q4
```

## Performance

- Audit execution: ~1-2 minutes
- Comprehensive control testing
- Professional report generation
- Complete evidence package

## Control Framework

Based on COSO framework for financial reporting:

- **Control Environment**: Access controls, segregation
- **Risk Assessment**: Data quality, system integrity
- **Control Activities**: Reconciliation, validation
- **Information & Communication**: Documentation, trails
- **Monitoring**: Regular compliance checks

## Report Contents

### Executive Summary
- Audit scope and period
- Control test summary
- Overall assessment
- Key findings

### Detailed Findings
- Exceptions identified
- Severity assessment
- Management response area

### Control Descriptions
- Each control's objective
- Test performed
- Evidence collected
- Status conclusion

### Management Response
- Area for management to address findings
- Remediation timeline
- Owner assignment

## Evidence Package

### Control Testing Sheet
- Control ID and name
- Objective tested
- Result (pass/fail)
- Evidence gathered

### Exception Log
- Finding description
- Severity level
- Supporting evidence
- Recommended action

### Supporting Schedules
- Transaction samples
- Reconciliation details
- System logs
- Access reports

## Recommendations

Professional audit recommendations:
- Continue monthly reconciliation procedures
- Perform quarterly access reviews
- Maintain data change documentation
- Execute annual comprehensive audit

## Integration

Works with:
- `/dr-anomalies-report` - Data quality validation
- `/dr-reconcile` - Consistency checking
- `/dr-extract` - Data extraction
- `/dr-dashboard` - Control monitoring

## Related Skills

- `/dr-reconcile` - Ongoing reconciliation
- `/dr-anomalies-report` - Data quality
- `/dr-extract` - Data sourcing
- `/dr-dashboard` - KPI monitoring
