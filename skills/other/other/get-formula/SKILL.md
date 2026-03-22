---
name: dr-get-formula
description: Generate Excel workbooks with DR.GET formulas that pull live financial data from Datarails. Creates P&L templates, budget models, and variance reports with validated dimension values.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_finance_tables
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__get_field_distinct_values
  - mcp__datarails-finance-os__get_sample_records
  - mcp__datarails-finance-os__get_records_by_filter
  - mcp__datarails-finance-os__aggregate_table_data
  - Write
  - Read
  - Bash
argument-hint: "[--type summary|detail|budget|variance] [--year <YYYY>] [--output <file>]"
---

# DR.GET Formula Workbook Generator

Generate Excel workbooks containing DR.GET formulas that pull live financial data from Datarails when opened with the Datarails Excel Add-in.

**DR.GET** is a custom Excel function that bridges Datarails' centralized financial database and Excel-based models. Formulas auto-refresh when the workbook is opened with the add-in active.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--type <type>` | Report type: `summary`, `detail`, `budget`, `variance` | `summary` |
| `--year <YYYY>` | Calendar year for date headers | Current year |
| `--output <file>` | Output file path | `tmp/DR_GET_<type>_<YEAR>.xlsx` |

## Client Profile System

This skill uses **client profiles** to adapt to different Datarails environments. Each client has different table IDs, field names, account hierarchies, and dimension values.

### Profile Location
Profiles are stored at: `config/client-profiles/<env>.json`

### First-Time Setup
If no profile exists for the target environment:
1. Inform the user: "No profile found for this environment. Run `/dr-learn` first to configure."
2. Guide them to run `/dr-learn --env <env>`

### Required Profile Fields
```json
{
  "tables": {
    "financials": { "id": "<table_id>" }
  },
  "field_mappings": {
    "amount": "Amount",
    "date": "Reporting Date",
    "scenario": "Scenario",
    "account_l0": "DR_ACC_L0",
    "account_l1_5": "DR_ACC_L1.5",
    "account_l2": "DR_ACC_L2",
    "report_field": "Report_Field",
    "scenario_cycle": "Scenario Cycle",
    "planning_scenario": "Planning Scenario"
  },
  "account_hierarchy": {
    "pnl_filter": "P&L"
  }
}
```

---

## DR.GET Syntax Reference

```
=DR.GET(Value, "[Dimension1]", CellRef1, "[Dimension2]", CellRef2, ...)
```

### Syntax Rules

| Rule | Detail |
|------|--------|
| **Function name** | Always `Value` (no brackets, no quotes) |
| **Dimension names** | In square brackets inside double quotes: `"[Reporting Date]"` |
| **Dimension values** | Always **cell references**, never hardcoded strings |
| **Pair structure** | Every dimension is a `"[DimensionName]", CellRef` pair |
| **Cell references** | Use `$A$1` (absolute), `$A1` (mixed), or `A1` (relative) as appropriate |

### Date Dimension

`[Reporting Date]` requires **Excel serial date numbers** (end-of-month), NOT text strings.

**How to calculate EOM serial dates:**
```python
from datetime import date
EXCEL_EPOCH = date(1899, 12, 30)
# January 2026 EOM = Jan 31, 2026
serial = (date(2026, 1, 31) - EXCEL_EPOCH).days  # = 46053
```

Store the serial number as the cell value and apply `'MMM-YY'` number format so it displays as "Jan-26" while DR.GET reads the numeric serial.

### Common Mistakes to Avoid

| Mistake | Correct Approach |
|---------|-----------------|
| Hardcoding values in DR.GET: `"Actuals"` | Always reference a cell: `$B$1` |
| Using text month: `"January 2026"` | Use EOM serial number: `46053` |
| Using `[Account]` or `[Month]` | Use actual field names from profile |
| Using Report_Field without scoping | Always include `[DR_ACC_L2]` alongside `[Report_Field]` |
| Inventing or guessing dimension values | Validate against actual distinct values first |
| Using `Scenario="Budget"` | Use `Scenario="Forecast"` + `Scenario Cycle` + `Planning Scenario` |
| Wrapping DR.GET in IFERROR/IF/other functions | DR.GET must be bare: `=DR.GET(...)` only |
| Adding fallback values for missing data | Let DR.GET return empty/0 — users need to see gaps |
| Pointing to cells that don't contain data | Every cell reference must point to an actual parameter or header cell |

### CRITICAL: DR.GET Formulas Must Be Simple

**NEVER** wrap DR.GET formulas in any other Excel function. Write them as bare formulas only.

```
WRONG:  =IFERROR(DR.GET(Value, "[Scenario]", $B$1, ...), 0)
WRONG:  =IF(DR.GET(Value, ...) > 0, DR.GET(Value, ...), "")
WRONG:  =ROUND(DR.GET(Value, ...), 2)
RIGHT:  =DR.GET(Value, "[Scenario]", $B$1, "[DR_ACC_L1.5]", $A6, "[Reporting Date]", B$5)
```

**Why:** The Datarails Add-in manages DR.GET formulas. Wrapping them in other functions breaks the add-in's ability to refresh, track, and drill down on them. If data is missing, the cell should show 0 or empty — this is valuable information that users need to see, not mask.

**Cell references must be intentional.** Every cell reference in a DR.GET formula must point to a specific cell that contains a validated parameter value (scenario name, account name, date serial). Never generate references to empty cells or cells outside the data layout.

---

## Workflow

### Phase 1: Setup

#### Step 1: Verify Authentication
```
If any tool call fails with a connection error, guide the user to connect via Connectors UI.
```

#### Step 2: Load Client Profile
```
Read: config/client-profiles/<env>.json

If profile exists:
  - Load table IDs and field mappings
  - Extract field names for: account_l1_5, account_l2, report_field, scenario, date, etc.
  - Continue to Phase 2

If profile does NOT exist:
  - Inform user: "No profile found. Run '/dr-learn' first."
  - Stop execution
```

### Phase 2: Dimension Discovery & Validation

**CRITICAL: Every value used in a DR.GET formula must be validated against the live Datarails table.**

#### Step 3: Discover Account Hierarchy

Use the financials table ID from the profile.

```
# Get distinct values for the account dimensions we'll use
get_field_distinct_values(table_id, field_name=<account_l1_5_field>)
get_field_distinct_values(table_id, field_name=<account_l2_field>)
```

If `get_field_distinct_values` returns a 409 error (known broken endpoint), fall back to:
```
# Fetch sample records and extract unique values
get_sample_records(table_id, n=20)
# Or use aggregation to discover values:
aggregate_table_data(table_id, dimensions=[<account_l1_5_field>], metrics=[{"field": "Amount", "agg": "SUM"}])
```

#### Step 4: Discover Scenario Values

```
get_field_distinct_values(table_id, field_name=<scenario_field>)
get_field_distinct_values(table_id, field_name=<scenario_cycle_field>)
get_field_distinct_values(table_id, field_name=<planning_scenario_field>)
```

#### Step 5: Map Parent-Child Relationships (for detail reports)

For `--type detail`, discover which child values belong to which parent:
```
# For each L1.5 value, find which L2 values belong to it
aggregate_table_data(
  table_id,
  dimensions=[<account_l1_5_field>, <account_l2_field>],
  metrics=[{"field": "Amount", "agg": "COUNT"}],
  filters=[{"name": <scenario_field>, "values": ["Actuals"], "is_excluded": false}]
)
```

For Report_Field detail, also map L2 → Report_Field relationships.

#### Step 6: Build Validated Value Registry

Store all discovered values in a dict structure:
```python
registry = {
    "account_l1_5": ["Revenues", "COGS", ...],  # from live API
    "account_l2": {"Revenues": ["Income"], "S&M": ["Marketing", "Sales", ...], ...},
    "report_fields": {"Sales": ["Events", "Payroll & Benefits", ...], ...},
    "scenarios": ["Actuals", "Forecast"],
    "scenario_cycles": ["0+12", "1+11", ...],
    "planning_scenarios": ["Actuals", "Bottom up", "Budget", ...]
}
```

**Every value in the workbook MUST come from this registry. Never hardcode or guess values.**

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

### Phase 3: Workbook Generation

#### Step 7: Generate Excel with openpyxl

Use Bash to run a Python script (inline or from file) that generates the workbook using openpyxl.

**Workbook Structure by Report Type:**

##### `--type summary` (Summary P&L)
- **Parameter cells** (Row 1-3): Scenario, Scenario Cycle, Planning Scenario
- **Date headers** (Row 5): EOM serial dates formatted as MMM-YY
- **P&L rows** (Row 6+): One row per L1.5 value (from registry)
- **Calculated rows**: Gross Profit, Total OpEx, Operating Income, Net Income
- **Two sheets**: Actuals, Budget

##### `--type detail` (Departmental Detail)
- Same parameter/date structure as summary
- Rows grouped by L1.5 parent with L2 children indented
- Subtotal rows per L1.5 group

##### `--type budget` (Budget Template)
- Scenario pre-set to Forecast
- Scenario Cycle defaults to 0+12
- Planning Scenario defaults to Bottom up
- All L1.5 line items with monthly columns

##### `--type variance` (Actuals vs Budget)
- Two formula blocks: Actuals and Budget
- Variance columns (Actual - Budget) as Excel formulas (not DR.GET)
- Variance % columns

#### DR.GET Formula Construction

**Every DR.GET formula must be a bare `=DR.GET(...)` call. No IFERROR, no IF, no ROUND, no wrapping of any kind.**

**Actuals formula pattern:**
```python
f'=DR.GET(Value, "[{l1_5_field}]", $A{{row}}, "[{scenario_field}]", $B$1, "[{date_field}]", {{col}}$5)'
```

**Budget formula pattern:**
```python
f'=DR.GET(Value, "[{l1_5_field}]", $A{{row}}, "[{scenario_field}]", $B$1, "[{cycle_field}]", $B$2, "[{planning_field}]", $B$3, "[{date_field}]", {{col}}$5)'
```

**Detail formula (with L2 scoping):**
```python
f'=DR.GET(Value, "[{report_field}]", $A{{row}}, "[{l2_field}]", $B{{row}}, "[{scenario_field}]", $D$2, "[{date_field}]", {{col}}$5)'
```

**Cell reference map** — each reference in the formula must point to:
- `$A{row}` → the account/line item label in column A of that row
- `$B$1` → the Scenario parameter cell (e.g., "Actuals")
- `$B$2` → the Scenario Cycle parameter cell (e.g., "0+12")
- `$B$3` → the Planning Scenario parameter cell (e.g., "Bottom up")
- `{col}$5` → the date header in row 5 of that column (EOM serial number)
- `$B{row}` → the L2 scoping value in column B of that row (detail reports)

If a reference doesn't map to one of these known locations, it is wrong. Do not invent references.

#### Excel Formatting

```python
# Date headers: serial number with MMM-YY format
cell.value = serial_number
cell.number_format = 'MMM-YY'

# Financial cells: number format
cell.number_format = '#,##0'

# Parameter cells: clear labels
ws['A1'] = 'Scenario:'
ws['B1'] = 'Actuals'  # validated value from registry

# Calculated rows: Excel formulas (NOT DR.GET)
# Gross Profit = Revenue - COGS
ws.cell(row=gp_row, column=col).value = f'={get_column_letter(col)}{rev_row}-{get_column_letter(col)}{cogs_row}'
```

#### Calculated Lines (No DR.GET)

These P&L lines are always Excel formulas referencing other rows:

| Line | Formula Pattern |
|------|----------------|
| Gross Profit | `= Revenue_row - COGS_row` |
| Total OpEx | `= SUM(opex_line_rows)` |
| Operating Income | `= Gross_Profit_row - Total_OpEx_row` |
| Net Income | `= Operating_Income_row - Finance_row - Tax_row` |

### Phase 4: Save & Report

#### Step 8: Save Output

Save to `tmp/DR_GET_<type>_<YEAR>.xlsx` or the user-specified `--output` path.

#### Step 9: Report to User

Report what was generated:
- Number of validated dimension values used
- Number of DR.GET formulas written
- Number of calculated rows
- Output file path
- Reminder: "Open this workbook with the Datarails Excel Add-in active to refresh formulas."

---

## Examples

### Summary P&L with Actuals
```bash
/dr-get-formula --type summary --year 2026
```

### Detailed departmental breakdown
```bash
/dr-get-formula --type detail --year 2026
```

### Budget template
```bash
/dr-get-formula --type budget --year 2026
```

### Actuals vs Budget variance
```bash
/dr-get-formula --type variance --year 2026
```

### Custom output location
```bash
/dr-get-formula --type summary --year 2026 --output tmp/PnL_Template_2026.xlsx
```

---

## Troubleshooting

**"Not authenticated" error**
- Connect via Connectors UI ("+" > Connectors > Datarails > Connect)

**"No profile found" error**
- Run `/dr-learn` to create a client profile first

**DR.GET formulas return 0 or errors when opened in Excel**
- Verify the Datarails Excel Add-in is active
- Check that dimension values match exactly (case-sensitive, exact spelling)
- Re-run the skill to re-validate values against live data

**`get_field_distinct_values` returns 409**
- Known API issue. The skill falls back to aggregation or sample records for value discovery.

**Missing dimension values**
- The live data may not contain all expected categories
- Check with `/dr-query` to investigate the table directly

**Date headers show numbers instead of month names**
- The serial numbers are correct; apply `MMM-YY` number format in Excel
- The generated workbook should already have this format applied
