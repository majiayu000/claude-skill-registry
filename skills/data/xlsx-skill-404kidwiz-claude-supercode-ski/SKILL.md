---
name: xlsx
description: Expert in automating Excel workflows using Node.js (ExcelJS, SheetJS) and Python (pandas, openpyxl).
---

# XLSX Skill

## Purpose
Provides expertise in creating, reading, modifying, and automating Excel spreadsheet workflows. Specializes in programmatic spreadsheet manipulation using ExcelJS, SheetJS, pandas, and openpyxl for data processing, reporting, and automation.

## When to Use
- Creating Excel reports programmatically
- Reading and parsing XLSX files
- Modifying existing spreadsheets while preserving formatting
- Automating repetitive Excel tasks
- Converting between CSV and XLSX formats
- Building Excel templates with formulas
- Extracting data from complex spreadsheets
- Generating formatted financial or data reports

## Quick Start
**Invoke this skill when:**
- Creating Excel reports programmatically
- Reading and parsing XLSX files
- Modifying existing spreadsheets while preserving formatting
- Automating repetitive Excel tasks
- Converting between CSV and XLSX formats

**Do NOT invoke when:**
- Creating Google Sheets → different API
- Building Excel add-ins → use appropriate .NET/JS skill
- Data analysis without Excel output → use data-analyst
- CSV-only operations → use csv-data-wrangler

## Decision Framework
```
Excel Task?
├── Node.js Environment → ExcelJS (full-featured) or SheetJS (parsing)
├── Python Environment → openpyxl (Excel) or pandas (data + Excel)
├── Heavy Data Processing → pandas with openpyxl engine
├── Complex Formatting → ExcelJS or openpyxl
├── Template-Based → Fill existing templates with data
└── Large Files → Streaming readers (ExcelJS streaming, pandas chunks)
```

## Core Workflows

### 1. Excel Report Generation (Node.js)
1. Initialize ExcelJS workbook
2. Create worksheets with appropriate names
3. Define columns with headers and widths
4. Add data rows from source
5. Apply styling (fonts, borders, fills)
6. Add formulas for calculations
7. Set print area and page setup
8. Write to file buffer or stream

### 2. Spreadsheet Data Extraction (Python)
1. Load workbook with openpyxl or pandas
2. Identify data ranges and headers
3. Handle merged cells and formatting
4. Extract data into structured format
5. Validate and clean extracted data
6. Handle multiple sheets if needed
7. Convert to desired output format

### 3. Template-Based Reporting
1. Create master template with formatting and formulas
2. Load template workbook
3. Identify data insertion points
4. Insert data while preserving formulas
5. Update any date/reference cells
6. Recalculate formulas if needed
7. Save as new file (preserve template)

## Best Practices
- Use streaming mode for large files to manage memory
- Preserve existing styles when modifying files
- Validate data types before writing to cells
- Handle merged cells explicitly
- Use named ranges for maintainability
- Test with actual Excel application, not just libraries

## Anti-Patterns
- **Loading huge files in memory** → Use streaming readers
- **Hardcoding cell references** → Use named ranges or dynamic lookup
- **Ignoring data types** → Explicitly set number, date, text types
- **Overwriting formulas** → Check cell types before writing
- **Missing error handling** → Handle corrupted/password-protected files
