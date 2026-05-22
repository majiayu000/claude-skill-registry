---
name: xlsx
description: "Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. When Claude needs to work with spreadsheets (.xlsx, .xlsm, .csv, .tsv, etc) for: (1) Creating new spreadsheets with formulas and formatting, (2) Reading or analyzing data, (3) Modify existing spreadsheets while preserving formulas, (4) Data analysis and visualization in spreadsheets, or (5) Recalculating formulas"
---

# XLSX Spreadsheet Processing

## Requirements for Outputs

### All Excel Files
- **Zero Formula Errors**: Every file must have ZERO formula errors (#REF!, #DIV/0!, etc.)
- **Preserve Existing Templates**: Match existing format when modifying files

### Financial Models

**Color Coding:**
- Blue text: Hardcoded inputs
- Black text: Formulas and calculations
- Green text: Links from other worksheets
- Red text: External file links
- Yellow background: Key assumptions

**Number Formatting:**
- Years: Text strings ("2024" not "2,024")
- Currency: $#,##0 with units in headers
- Zeros: Format as "-"
- Percentages: 0.0% format
- Negatives: Use parentheses (123)

## Reading and Analyzing

```python
import pandas as pd

# Read Excel
df = pd.read_excel('file.xlsx')
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)

# Analyze
df.head()
df.info()
df.describe()
```

## Creating/Editing with openpyxl

```python
from openpyxl import Workbook, load_workbook

# Create new
wb = Workbook()
sheet = wb.active
sheet['A1'] = 'Hello'
sheet['B2'] = '=SUM(A1:A10)'  # Use formulas!
wb.save('output.xlsx')

# Edit existing
wb = load_workbook('existing.xlsx')
sheet = wb.active
sheet['A1'] = 'New Value'
wb.save('modified.xlsx')
```

## CRITICAL: Use Formulas

**Wrong:** Calculate in Python, hardcode result
```python
total = df['Sales'].sum()
sheet['B10'] = total  # BAD!
```

**Correct:** Use Excel formulas
```python
sheet['B10'] = '=SUM(B2:B9)'  # GOOD!
```

## Recalculating Formulas

```bash
python recalc.py <excel_file> [timeout_seconds]
```

The script:
- Sets up LibreOffice macro on first run
- Recalculates all formulas
- Scans for errors
- Returns JSON with error details

## Library Selection

- **pandas**: Data analysis, bulk operations, simple export
- **openpyxl**: Complex formatting, formulas, Excel features
