---
name: document-xlsx
description: Create, edit, and analyze Excel spreadsheets with formulas, formatting, charts, pivot tables, and data validation. Supports xlsx, exceljs, openpyxl, and pandas for comprehensive spreadsheet workflows in Node.js and Python.
---

# Document XLSX Skill — Quick Reference

This skill enables creation, editing, and analysis of Excel spreadsheets programmatically. Claude should apply these patterns when users need to generate data reports, financial models, automate Excel workflows, or process spreadsheet data.

**Modern Best Practices (Dec 2025)**:
- Treat spreadsheets as software: clear inputs/outputs, auditability, and versioning.
- Protect data integrity: control totals, validation, and traceability to sources.
- Accessibility and readability matter (labels, contrast, not color-only meaning).
- Ship with a review loop and an owner (avoid “mystery models”).

---

## Quick Reference

| Task | Tool/Library | Language | When to Use |
|------|--------------|----------|-------------|
| Create XLSX | exceljs | Node.js | Reports, data exports |
| Create XLSX | openpyxl | Python | Formatted workbooks |
| Data analysis | pandas | Python | DataFrame to Excel |
| Read XLSX | xlsx (SheetJS) | Node.js | Parse spreadsheets |
| Charts | openpyxl | Python | Embedded visualizations |
| Styling | exceljs/openpyxl | Both | Conditional formatting |

## When to Use This Skill

Claude should invoke this skill when a user requests:

- Generate Excel reports from data
- Create spreadsheets with formulas and formatting
- Add charts and pivot tables
- Parse and extract data from Excel files
- Implement conditional formatting
- Create data validation rules
- Automate Excel-based workflows

---

## Core Operations

### Create Spreadsheet (Node.js - exceljs)

```typescript
import ExcelJS from 'exceljs';

const workbook = new ExcelJS.Workbook();
const sheet = workbook.addWorksheet('Sales Report');

// Headers with styling
sheet.columns = [
  { header: 'Product', key: 'product', width: 20 },
  { header: 'Quantity', key: 'qty', width: 12 },
  { header: 'Price', key: 'price', width: 12 },
  { header: 'Total', key: 'total', width: 15 },
];

// Style header row
sheet.getRow(1).font = { bold: true };
sheet.getRow(1).fill = {
  type: 'pattern',
  pattern: 'solid',
  fgColor: { argb: 'FF4472C4' }
};

// Add data
const data = [
  { product: 'Widget A', qty: 100, price: 10 },
  { product: 'Widget B', qty: 50, price: 25 },
];

data.forEach((item, index) => {
  const row = sheet.addRow({
    product: item.product,
    qty: item.qty,
    price: item.price,
    total: { formula: `B${index + 2}*C${index + 2}` }
  });
});

// Add totals row
const lastRow = sheet.rowCount + 1;
sheet.addRow({
  product: 'TOTAL',
  total: { formula: `SUM(D2:D${lastRow - 1})` }
});

// Currency formatting
sheet.getColumn('price').numFmt = '$#,##0.00';
sheet.getColumn('total').numFmt = '$#,##0.00';

await workbook.xlsx.writeFile('report.xlsx');
```

### Create Spreadsheet (Python - openpyxl)

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Fill, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference

wb = Workbook()
ws = wb.active
ws.title = 'Sales Report'

# Headers
headers = ['Product', 'Quantity', 'Price', 'Total']
for col, header in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=header)
    cell.font = Font(bold=True, color='FFFFFF')
    cell.fill = PatternFill(start_color='4472C4', fill_type='solid')

# Data
data = [
    ('Widget A', 100, 10),
    ('Widget B', 50, 25),
    ('Widget C', 75, 15),
]

for row_idx, (product, qty, price) in enumerate(data, 2):
    ws.cell(row=row_idx, column=1, value=product)
    ws.cell(row=row_idx, column=2, value=qty)
    ws.cell(row=row_idx, column=3, value=price)
    ws.cell(row=row_idx, column=4, value=f'=B{row_idx}*C{row_idx}')

# Totals row
total_row = len(data) + 2
ws.cell(row=total_row, column=1, value='TOTAL')
ws.cell(row=total_row, column=4, value=f'=SUM(D2:D{total_row-1})')

# Number formatting
for row in range(2, total_row + 1):
    ws.cell(row=row, column=3).number_format = '$#,##0.00'
    ws.cell(row=row, column=4).number_format = '$#,##0.00'

wb.save('report.xlsx')
```

### Read and Analyze (Python - pandas)

```python
import pandas as pd

# Read Excel file
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# Analysis
summary = df.groupby('Category').agg({
    'Sales': 'sum',
    'Quantity': 'mean'
}).round(2)

# Write to Excel with formatting
with pd.ExcelWriter('analysis.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Raw Data', index=False)
    summary.to_excel(writer, sheet_name='Summary')

    # Auto-adjust column widths
    for sheet in writer.sheets.values():
        for column in sheet.columns:
            max_length = max(len(str(cell.value)) for cell in column)
            sheet.column_dimensions[column[0].column_letter].width = max_length + 2
```

### Add Charts (Python)

```python
from openpyxl.chart import BarChart, Reference

chart = BarChart()
chart.title = 'Sales by Product'
chart.x_axis.title = 'Product'
chart.y_axis.title = 'Sales'

# Data range
data = Reference(ws, min_col=4, min_row=1, max_row=len(data)+1, max_col=4)
categories = Reference(ws, min_col=1, min_row=2, max_row=len(data)+1)

chart.add_data(data, titles_from_data=True)
chart.set_categories(categories)
chart.shape = 4

ws.add_chart(chart, 'F2')
```

### Conditional Formatting

```python
from openpyxl.formatting.rule import ColorScaleRule, FormulaRule
from openpyxl.styles import PatternFill

# Color scale (heatmap)
ws.conditional_formatting.add(
    'D2:D100',
    ColorScaleRule(
        start_type='min', start_color='FF0000',
        end_type='max', end_color='00FF00'
    )
)

# Highlight cells above threshold
red_fill = PatternFill(start_color='FFCCCC', fill_type='solid')
ws.conditional_formatting.add(
    'D2:D100',
    FormulaRule(formula=['D2>1000'], fill=red_fill)
)
```

---

## Common Formulas Reference

| Purpose | Formula | Example |
|---------|---------|---------|
| Sum | `=SUM(range)` | `=SUM(A1:A10)` |
| Average | `=AVERAGE(range)` | `=AVERAGE(B2:B100)` |
| Count | `=COUNT(range)` | `=COUNT(C:C)` |
| Conditional sum | `=SUMIF(range,criteria,sum_range)` | `=SUMIF(A:A,"Widget",B:B)` |
| Lookup | `=VLOOKUP(value,range,col,FALSE)` | `=VLOOKUP(A2,Data!A:C,3,FALSE)` |
| If | `=IF(condition,true,false)` | `=IF(B2>100,"High","Low")` |
| Percentage | `=value/total` | `=B2/SUM(B:B)` |

---

## Decision Tree

```text
Excel Task: [What do you need?]
    ├─ Create new spreadsheet?
    │   ├─ Simple data export → pandas to_excel()
    │   ├─ Formatted report → exceljs or openpyxl
    │   └─ With charts → openpyxl charts module
    │
    ├─ Read/analyze existing?
    │   ├─ Data analysis → pandas read_excel()
    │   ├─ Preserve formatting → openpyxl load_workbook()
    │   └─ Fast parsing → xlsx (SheetJS)
    │
    ├─ Modify existing?
    │   ├─ Add data → openpyxl (preserves formatting)
    │   └─ Update formulas → openpyxl
    │
    └─ Complex features?
        ├─ Pivot tables → openpyxl or xlwings
        ├─ Data validation → openpyxl DataValidation
        └─ Macros → xlwings (Python-Excel bridge)
```

---

## Do / Avoid (Dec 2025)

### Do

- Separate Inputs / Calculations / Outputs (tabs or clear sections).
- Keep assumptions explicit (value + unit + source + date).
- Add control totals and reconciliation checks for imported data.

### Avoid

- Hardcoded constants inside formulas without a documented assumption.
- Hidden rows/columns that change results without documentation.
- Sharing sheets with customer PII or secrets.

## What Good Looks Like

- Structure: clear Inputs/Assumptions, Calculations, and Outputs separation (tabs or sections).
- Integrity: no `#REF!`, broken named ranges, or hardcoded constants hidden in formulas.
- Traceability: every key output ties back to labeled inputs (units + source + date).
- Checks: control totals, reconciliations, and error flags that fail loudly.
- Review: independent review pass using `templates/spreadsheet-model-review-checklist.md`.

## Optional: AI / Automation

Use only when explicitly requested and policy-compliant.

- Generate first-pass formulas/charts; humans verify correctness and edge cases.
- Draft documentation tabs (assumptions, glossary); do not invent source data.

## Navigation

**Resources**
- [resources/excel-formulas.md](resources/excel-formulas.md) — Formula reference and patterns
- [resources/excel-formatting.md](resources/excel-formatting.md) — Styling, conditional formatting
- [resources/excel-charts.md](resources/excel-charts.md) — Chart types and customization
- [data/sources.json](data/sources.json) — Library documentation links

**Templates**
- [templates/financial-report.md](templates/financial-report.md) — Financial statement template
- [templates/data-dashboard.md](templates/data-dashboard.md) — Dashboard with charts
- [templates/spreadsheet-model-review-checklist.md](templates/spreadsheet-model-review-checklist.md) — Model QA checklist (assumptions, formulas, traceability)

**Related Skills**
- [../document-pdf/SKILL.md](../document-pdf/SKILL.md) — PDF generation from data
- [../ai-ml-data-science/SKILL.md](../ai-ml-data-science/SKILL.md) — Data analysis patterns
- [../data-sql-optimization/SKILL.md](../data-sql-optimization/SKILL.md) — Database to Excel workflows
