---
name: working-with-spreadsheets
description: |
  Creates and edits Excel spreadsheets with formulas, formatting, and financial modeling standards.
  Use when working with .xlsx files, financial models, data analysis, or formula-heavy spreadsheets.
  Covers formula recalculation, color coding standards, and common pitfalls.
---

# Working with Spreadsheets

## Quick Start

```python
from openpyxl import Workbook

wb = Workbook()
sheet = wb.active
sheet['A1'] = 'Revenue'
sheet['B1'] = 1000
sheet['B2'] = '=B1*1.1'  # Use formulas, not hardcoded values!
wb.save('output.xlsx')
```

## Critical Rule: Use Formulas, Not Hardcoded Values

**Always use Excel formulas instead of calculating in Python.**

```python
# WRONG - Hardcoding calculated values
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes 5000

# CORRECT - Using Excel formulas
sheet['B10'] = '=SUM(B2:B9)'
```

## Financial Model Color Coding Standards

| Color | RGB | Usage |
|-------|-----|-------|
| **Blue text** | 0,0,255 | Hardcoded inputs, scenario values |
| **Black text** | 0,0,0 | ALL formulas and calculations |
| **Green text** | 0,128,0 | Links from other worksheets |
| **Red text** | 255,0,0 | External links to other files |
| **Yellow background** | 255,255,0 | Key assumptions needing attention |

```python
from openpyxl.styles import Font

# Input cell (user changeable)
sheet['B5'].font = Font(color='0000FF')  # Blue

# Formula cell
sheet['C5'] = '=B5*1.1'
sheet['C5'].font = Font(color='000000')  # Black

# Cross-sheet link
sheet['D5'] = "=Sheet2!A1"
sheet['D5'].font = Font(color='008000')  # Green
```

## Number Formatting Standards

```python
# Currency with thousands separator
sheet['B5'].number_format = '$#,##0'

# Zeros display as dash
sheet['B5'].number_format = '$#,##0;($#,##0);-'

# Percentages with one decimal
sheet['C5'].number_format = '0.0%'

# Valuation multiples
sheet['D5'].number_format = '0.0x'

# Years as text (not 2,024)
sheet['A1'] = '2024'  # String, not number
```

## Library Selection

| Task | Library | Example |
|------|---------|---------|
| Data analysis | pandas | `df = pd.read_excel('file.xlsx')` |
| Formulas & formatting | openpyxl | `sheet['A1'] = '=SUM(B:B)'` |
| Large files (read) | openpyxl | `load_workbook('file.xlsx', read_only=True)` |
| Large files (write) | openpyxl | `Workbook(write_only=True)` |

## Reading Excel Files

```python
import pandas as pd
from openpyxl import load_workbook

# pandas - data analysis
df = pd.read_excel('file.xlsx')
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # Dict of DataFrames

# openpyxl - preserve formulas
wb = load_workbook('file.xlsx')
sheet = wb.active
print(sheet['A1'].value)  # Returns formula string

# openpyxl - get calculated values (WARNING: loses formulas on save!)
wb = load_workbook('file.xlsx', data_only=True)
```

## Creating Excel Files

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active
sheet.title = 'Model'

# Headers
sheet['A1'] = 'Metric'
sheet['B1'] = '2024'
sheet['A1'].font = Font(bold=True)

# Data with formulas
sheet['A2'] = 'Revenue'
sheet['B2'] = 1000000
sheet['B2'].font = Font(color='0000FF')  # Blue = input

sheet['A3'] = 'Growth'
sheet['B3'] = '=B2*0.1'
sheet['B3'].font = Font(color='000000')  # Black = formula

# Formatting
sheet['B2'].number_format = '$#,##0'
sheet.column_dimensions['A'].width = 20

wb.save('model.xlsx')
```

## Editing Existing Files

```python
from openpyxl import load_workbook

wb = load_workbook('existing.xlsx')
sheet = wb['Data']  # Or wb.active

# Modify cells
sheet['A1'] = 'Updated Value'
sheet.insert_rows(2)
sheet.delete_cols(3)

# Add new sheet
new_sheet = wb.create_sheet('Analysis')
new_sheet['A1'] = '=Data!B5'  # Cross-sheet reference

wb.save('modified.xlsx')
```

## Formula Recalculation

**openpyxl writes formulas but doesn't calculate values.** Use LibreOffice to recalculate:

```bash
# Recalculate and check for errors
python recalc.py output.xlsx
```

The script returns JSON:
```json
{
  "status": "success",  // or "errors_found"
  "total_errors": 0,
  "total_formulas": 42,
  "error_summary": {
    "#REF!": {"count": 2, "locations": ["Sheet1!B5", "Sheet1!C10"]}
  }
}
```

## Formula Verification Checklist

### Before Building
- [ ] Test 2-3 sample references first
- [ ] Confirm column mapping (column 64 = BL, not BK)
- [ ] Remember: DataFrame row 5 = Excel row 6 (1-indexed)

### Common Pitfalls
- [ ] Check for NaN with `pd.notna()` before using values
- [ ] FY data often in columns 50+ (far right)
- [ ] Search ALL occurrences, not just first match
- [ ] Check denominators before division (#DIV/0!)
- [ ] Verify cross-sheet references use correct format (`Sheet1!A1`)

### After Building
- [ ] Run `recalc.py` and fix any errors
- [ ] Verify #REF!, #DIV/0!, #VALUE!, #NAME? = 0

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| #REF! | Invalid cell reference | Check deleted rows/columns |
| #DIV/0! | Division by zero | Add IF check: `=IF(B5=0,0,A5/B5)` |
| #VALUE! | Wrong data type | Check cell contains expected type |
| #NAME? | Unknown function | Check spelling, quotes around text |

## Verification

Run: `python scripts/verify.py`

## Related Skills

- `building-nextjs-apps` - Frontend for spreadsheet uploads
- `scaffolding-fastapi-dapr` - API for spreadsheet processing
