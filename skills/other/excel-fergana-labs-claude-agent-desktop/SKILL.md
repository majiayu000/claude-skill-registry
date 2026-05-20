---
name: excel
description: Create, read, edit, and analyze Microsoft Excel spreadsheets (.xlsx files). Use for spreadsheet data, calculations, formulas, charts, and tabular data analysis.
allowed-tools: Read, Write, Bash
---

# Excel Spreadsheet Tool

This skill enables working with Microsoft Excel spreadsheets using Node.js tools.

## Capabilities

- **Read** data from existing Excel files and extract tabular data
- **Create** new workbooks with multiple worksheets
- **Write** data to cells and ranges
- **Apply** formulas and calculations (SUM, AVERAGE, etc.)
- **Format** cells with colors, borders, fonts, and auto-sizing
- **Analyze** data with column statistics (sum, average, min, max)
- **Update** specific cells in existing spreadsheets

## When to Use

Invoke this skill when the user:
- Mentions Excel files, spreadsheets, .xlsx files, or tabular data
- Asks to create, read, or modify spreadsheet data
- Needs to perform calculations, formulas, or data analysis
- Wants to format data in rows and columns
- Asks about data visualization or charts

## How to Use

The Excel tool is implemented at `src/tools/excel-tool.ts`. Invoke using the Bash tool:

### Reading a Spreadsheet
```bash
ts-node src/tools/excel-tool.ts read "/path/to/file.xlsx" "SheetName"
```

### Creating a Spreadsheet
```bash
ts-node src/tools/excel-tool.ts create "/path/to/new.xlsx" '[{"name":"Sheet1","data":[["A1","B1"],["A2","B2"]],"headers":["Column1","Column2"]}]'
```

### Getting Column Statistics
```bash
ts-node src/tools/excel-tool.ts stats "/path/to/file.xlsx" "Sheet1" "A"
```

## JSON Structure for Creating Spreadsheets

```json
[
  {
    "name": "Sheet1",
    "headers": ["Name", "Value", "Total"],
    "data": [
      ["Item 1", 100, 200],
      ["Item 2", 150, 300]
    ],
    "formulas": [
      {"cell": "C3", "formula": "SUM(B2:B3)"}
    ]
  }
]
```

## Implementation

Uses the `exceljs` npm library for comprehensive Excel file manipulation.
