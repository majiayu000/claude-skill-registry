---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: excel-automation
description: ">"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: spreadsheet
tags:
  - excel
  - automation
  - macro
  - workflow
department: All

# AI Model Compatibility
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

# MCP Tools Integration
mcp:
  server: office-mcp
  tools:
    - read_xlsx
    - create_xlsx
    - apply_formula
    - pivot_table

# Skill Capabilities
capabilities:
  - automation
  - data_processing
  - reporting

# Language Support
languages:
  - en
  - zh
---

# Excel Automation Skill

## Overview

This skill enables advanced Excel automation using **xlwings** - a library that can interact with live Excel instances. Unlike openpyxl (file-only), xlwings can control Excel in real-time, execute VBA, update dashboards, and automate complex workflows.

## How to Use

1. Describe the Excel automation task you need
2. Specify if you need live Excel interaction or file processing
3. I'll generate xlwings code and execute it

**Example prompts:**
- "Update this live Excel dashboard with new data"
- "Run this VBA macro and get the results"
- "Create an Excel add-in for data validation"
- "Automate monthly report generation with live charts"

## Domain Knowledge

### xlwings vs openpyxl

| Feature | xlwings | openpyxl |
|---------|---------|----------|
| Requires Excel | Yes | No |
| Live interaction | Yes | No |
| VBA execution | Yes | No |
| Speed (large files) | Fast | Slow |
| Server deployment | Limited | Easy |

### xlwings Fundamentals

```python
import xlwings as xw

# Connect to active Excel workbook
wb = xw.Book.caller()  # From Excel add-in
wb = xw.books.active   # Active workbook

# Open specific file
wb = xw.Book('path/to/file.xlsx')

# Create new workbook
wb = xw.Book()

# Get sheet
sheet = wb.sheets['Sheet1']
sheet = wb.sheets[0]
```

### Working with Ranges

#### Reading and Writing
```python
# Single cell
sheet['A1'].value = 'Hello'
value = sheet['A1'].value

# Range
sheet['A1:C3'].value = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
data = sheet['A1:C3'].value  # Returns list of lists

# Named range
sheet['MyRange'].value = 'Named data'

# Expand range (detect data boundaries)
sheet['A1'].expand().value  # All connected data
sheet['A1'].expand('table').value  # Table format
```

#### Dynamic Ranges
```python
# Current region (like Ctrl+Shift+End)
data = sheet['A1'].current_region.value

# Used range
used = sheet.used_range.value

# Last row with data
last_row = sheet['A1'].end('down').row

# Resize range
rng = sheet['A1'].resize(10, 5)  # 10 rows, 5 columns
```

### Formatting
```python
# Font
sheet['A1'].font.bold = True
sheet['A1'].font.size = 14
sheet['A1'].font.color = (255, 0, 0)  # RGB red

# Fill
sheet['A1'].color = (255, 255, 0)  # Yellow background

# Number format
sheet['B1'].number_format = '$#,##0.00'

# Column width
sheet['A:A'].column_width = 20

# Row height
sheet['1:1'].row_height = 30

# Autofit
sheet['A:D'].autofit()
```

### Excel Features

#### Charts
```python
# Add chart
chart = sheet.charts.add(left=100, top=100, width=400, height=250)
chart.set_source_data(sheet['A1:B10'])
chart.chart_type = 'column_clustered'
chart.name = 'Sales Chart'

# Modify existing chart
chart = sheet.charts['Sales Chart']
chart.chart_type = 'line'
```

#### Tables
```python
# Create Excel Table
rng = sheet['A1'].expand()
table = sheet.tables.add(source=rng, name='SalesTable')

# Refresh table
table.refresh()

# Access table data
table_data = table.data_body_range.value
```

#### Pictures
```python
# Add picture
sheet.pictures.add('logo.png', left=10, top=10, width=100, height=50)

# Update picture from matplotlib
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
sheet.pictures.add(fig, name='MyPlot', update=True)
```

### VBA Integration
```python
# Run VBA macro
wb.macro('MacroName')()

# With arguments
wb.macro('MyMacro')('arg1', 'arg2')

# Get return value
result = wb.macro('CalculateTotal')(100, 200)

# Access VBA module
vb_code = wb.api.VBProject.VBComponents('Module1').CodeModule.Lines(1, 10)
```

### User Defined Functions (UDFs)
```python
# Define a UDF (in Python file)
import xlwings as xw

@xw.func
def my_sum(x, y):
    """Add two numbers"""
    return x + y

@xw.func
@xw.arg('data', ndim=2)
def my_array_func(data):
    """Process array data"""
    import numpy as np
    return np.sum(data)

# These become Excel functions: =my_sum(A1, B1)
```

### Application Control
```python
# Excel application settings
app = xw.apps.active
app.screen_updating = False  # Speed up
app.calculation = 'manual'   # Manual calc
app.display_alerts = False   # Suppress dialogs

# Perform operations...

# Restore
app.screen_updating = True
app.calculation = 'automatic'
app.display_alerts = True
```

## Best Practices

1. **Disable Screen Updating**: For batch operations
2. **Use Arrays**: Read/write entire ranges, not cell-by-cell
3. **Manual Calculation**: Turn off auto-calc during data loading
4. **Close Connections**: Properly close workbooks when done
5. **Error Handling**: Handle Excel not being installed

## Common Patterns

### Performance Optimization
```python
import xlwings as xw

def batch_update(data, workbook_path):
    app = xw.App(visible=False)
    try:
        app.screen_updating = False
        app.calculation = 'manual'
        
        wb = app.books.open(workbook_path)
        sheet = wb.sheets['Data']
        
        # Write all data at once
        sheet['A1'].value = data
        
        app.calculation = 'automatic'
        wb.save()
    finally:
        wb.close()
        app.quit()
```

### Dashboard Update
```python
def update_dashboard(data_dict):
    wb = xw.books.active
    
    # Update data sheet
    data_sheet = wb.sheets['Data']
    for name, values in data_dict.items():
        data_sheet[name].value = values
    
    # Refresh all charts
    dashboard = wb.sheets['Dashboard']
    for chart in dashboard.charts:
        chart.refresh()
    
    # Update timestamp
    from datetime import datetime
    dashboard['A1'].value = f'Last Updated: {datetime.now()}'
```

### Report Generator
```python
def generate_monthly_report(month, data):
    template = xw.Book('template.xlsx')
    
    # Fill data
    sheet = template.sheets['Report']
    sheet['B2'].value = month
    sheet['A5'].value = data
    
    # Run calculations
    template.app.calculate()
    
    # Export to PDF
    sheet.api.ExportAsFixedFormat(0, f'report_{month}.pdf')
    
    template.save(f'report_{month}.xlsx')
```

## Examples

### Example 1: Live Dashboard Update
```python
import xlwings as xw
import pandas as pd
from datetime import datetime

# Connect to running Excel
wb = xw.books.active
dashboard = wb.sheets['Dashboard']
data_sheet = wb.sheets['Data']

# Fetch new data (simulated)
new_data = pd.DataFrame({
    'Date': pd.date_range('2024-01-01', periods=30),
    'Sales': [1000 + i*50 for i in range(30)],
    'Costs': [600 + i*30 for i in range(30)]
})

# Update data sheet
data_sheet['A1'].value = new_data

# Calculate profit
data_sheet['D1'].value = 'Profit'
data_sheet['D2'].value = '=B2-C2'
data_sheet['D2'].expand('down').value = data_sheet['D2'].formula

# Update KPIs on dashboard
dashboard['B2'].value = new_data['Sales'].sum()
dashboard['B3'].value = new_data['Costs'].sum()
dashboard['B4'].value = new_data['Sales'].sum() - new_data['Costs'].sum()
dashboard['A1'].value = f'Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}'

# Refresh charts
for chart in dashboard.charts:
    chart.api.Refresh()

print("Dashboard updated!")
```

### Example 2: Batch Processing Multiple Files
```python
import xlwings as xw
from pathlib import Path

def process_sales_files(folder_path, output_path):
    """Consolidate multiple Excel files into one summary."""
    
    app = xw.App(visible=False)
    app.screen_updating = False
    
    try:
        # Create summary workbook
        summary_wb = xw.Book()
        summary_sheet = summary_wb.sheets[0]
        summary_sheet.name = 'Consolidated'
        
        headers = ['File', 'Total Sales', 'Total Units', 'Avg Price']
        summary_sheet['A1'].value = headers
        
        row = 2
        for file in Path(folder_path).glob('*.xlsx'):
            wb = app.books.open(str(file))
            data_sheet = wb.sheets['Sales']
            
            # Extract summary
            total_sales = data_sheet['B:B'].api.SpecialCells(11).Value  # xlCellTypeConstants
            total_units = data_sheet['C:C'].api.SpecialCells(11).Value
            
            # Calculate and write
            summary_sheet[f'A{row}'].value = file.name
            summary_sheet[f'B{row}'].value = sum(total_sales) if isinstance(total_sales, (list, tuple)) else total_sales
            summary_sheet[f'C{row}'].value = sum(total_units) if isinstance(total_units, (list, tuple)) else total_units
            summary_sheet[f'D{row}'].value = f'=B{row}/C{row}'
            
            wb.close()
            row += 1
        
        # Format summary
        summary_sheet['A1:D1'].font.bold = True
        summary_sheet['B:D'].number_format = '$#,##0.00'
        summary_sheet['A:D'].autofit()
        
        summary_wb.save(output_path)
        
    finally:
        app.quit()
    
    print(f"Consolidated {row-2} files to {output_path}")

# Usage
process_sales_files('/path/to/sales/', 'consolidated_sales.xlsx')
```

### Example 3: Excel Add-in with UDFs
```python
# myudfs.py - Place in xlwings project

import xlwings as xw
import numpy as np

@xw.func
@xw.arg('data', pd.DataFrame, index=False, header=False)
@xw.ret(expand='table')
def GROWTH_RATE(data):
    """Calculate period-over-period growth rate"""
    values = data.iloc[:, 0].values
    growth = np.diff(values) / values[:-1] * 100
    return [['Growth %']] + [[g] for g in growth]

@xw.func
@xw.arg('range1', np.array, ndim=2)
@xw.arg('range2', np.array, ndim=2)
def CORRELATION(range1, range2):
    """Calculate correlation between two ranges"""
    return np.corrcoef(range1.flatten(), range2.flatten())[0, 1]

@xw.func
def SENTIMENT(text):
    """Basic sentiment analysis (placeholder)"""
    positive = ['good', 'great', 'excellent', 'amazing']
    negative = ['bad', 'poor', 'terrible', 'awful']
    
    text_lower = text.lower()
    pos_count = sum(word in text_lower for word in positive)
    neg_count = sum(word in text_lower for word in negative)
    
    if pos_count > neg_count:
        return 'Positive'
    elif neg_count > pos_count:
        return 'Negative'
    return 'Neutral'
```

## Limitations

- Requires Excel to be installed
- Limited support on macOS for some features
- Not suitable for server-side processing
- VBA features require trust settings
- Performance varies with Excel version

## Installation

```bash
pip install xlwings

# For add-in functionality
xlwings addin install
```

## Resources

- [xlwings Documentation](https://docs.xlwings.org/)
- [GitHub Repository](https://github.com/xlwings/xlwings)
- [UDF Tutorial](https://docs.xlwings.org/en/stable/udfs.html)
- [Excel VBA Reference](https://docs.microsoft.com/en-us/office/vba/api/overview/excel)
