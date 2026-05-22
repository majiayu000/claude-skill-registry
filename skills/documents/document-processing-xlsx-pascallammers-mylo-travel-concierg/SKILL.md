---
name: document-processing-xlsx
description: Process, parse, create, and manipulate Excel spreadsheets (.xlsx, .xls) using libraries like xlsx, exceljs, or SheetJS for data import/export and spreadsheet automation. Use when reading Excel files for data import, generating Excel reports, exporting data to spreadsheets, parsing bulk uploads, creating financial reports, manipulating workbooks and worksheets, or building data export features.
---

# Document Processing - Excel Files

## When to use this skill

- Reading Excel files for data import and processing
- Generating Excel reports and spreadsheets
- Exporting application data to Excel format
- Parsing bulk data uploads from spreadsheets
- Creating financial reports and statements
- Manipulating workbooks, worksheets, and cells
- Building CSV to Excel converters
- Creating templates for data entry
- Extracting data from uploaded spreadsheets
- Generating dynamic Excel reports with formulas
- Handling large dataset imports from Excel
- Building data export and reporting features

## When to use this skill

- Creating, parsing Excel spreadsheets.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Creating, parsing Excel spreadsheets.

## Example
\`\`\`typescript
import * as XLSX from 'xlsx';

const ws = XLSX.utils.aoa_to_sheet([[1, 2], [3, 4]]);
const wb = XLSX.utils.book_new();
XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
\`\`\`

## Resources
- [SheetJS](https://docs.sheetjs.com/)
