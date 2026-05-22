---
name: Spreadsheet Builder
slug: spreadsheet-builder
description: Create Excel and CSV files with formulas, formatting, charts, and data analysis
category: document-creation
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "create spreadsheet"
  - "generate excel"
  - "make csv file"
  - "build xlsx"
  - "create workbook"
tags:
  - excel
  - csv
  - spreadsheet
  - data
  - xlsx
  - analysis
---

# Spreadsheet Builder

The Spreadsheet Builder skill enables creation of professional Excel (.xlsx) and CSV files with advanced formatting, formulas, charts, and data analysis features. Using libraries like `exceljs` and `xlsx`, this skill handles everything from simple data exports to complex financial models and dashboards.

Generate data reports, financial statements, inventory lists, analysis dashboards, and any tabular data visualization. Support for multiple sheets, cell styling, conditional formatting, formulas, pivot tables, and charts makes this a comprehensive solution for spreadsheet automation.

## Core Workflows

### Workflow 1: Create Basic Excel Workbook
**Purpose:** Build a simple Excel file with formatted data

**Steps:**
1. Import `exceljs` and create Workbook instance
2. Add worksheet with a name
3. Define columns with headers and widths
4. Add data rows
5. Apply basic formatting (fonts, colors, alignment)
6. Set column widths and row heights
7. Write to .xlsx file

**Implementation:**
```javascript
const ExcelJS = require('exceljs');

async function createBasicWorkbook(data, outputPath) {
  const workbook = new ExcelJS.Workbook();
  const worksheet = workbook.addWorksheet('Sales Data');

  // Define columns
  worksheet.columns = [
    { header: 'Date', key: 'date', width: 12 },
    { header: 'Product', key: 'product', width: 25 },
    { header: 'Quantity', key: 'quantity', width: 10 },
    { header: 'Price', key: 'price', width: 12 },
    { header: 'Total', key: 'total', width: 12 }
  ];

  // Style header row
  worksheet.getRow(1).font = { bold: true, size: 12 };
  worksheet.getRow(1).fill = {
    type: 'pattern',
    pattern: 'solid',
    fgColor: { argb: 'FF4472C4' }
  };
  worksheet.getRow(1).font = { color: { argb: 'FFFFFFFF' }, bold: true };

  // Add data
  data.forEach(row => {
    worksheet.addRow(row);
  });

  // Format currency columns
  worksheet.getColumn('price').numFmt = '$#,##0.00';
  worksheet.getColumn('total').numFmt = '$#,##0.00';

  await workbook.xlsx.writeFile(outputPath);
}
```

### Workflow 2: Add Formulas and Calculations
**Purpose:** Create spreadsheets with automatic calculations and formulas

**Steps:**
1. Create workbook and worksheet
2. Add data columns
3. Insert formula cells (SUM, AVERAGE, IF, VLOOKUP, etc.)
4. Use cell references for dynamic calculations
5. Add conditional formulas
6. Create calculated columns
7. Add totals and subtotals

**Implementation:**
```javascript
async function createWithFormulas(data, outputPath) {
  const workbook = new ExcelJS.Workbook();
  const worksheet = workbook.addWorksheet('Financial Report');

  worksheet.columns = [
    { header: 'Month', key: 'month', width: 12 },
    { header: 'Revenue', key: 'revenue', width: 15 },
    { header: 'Expenses', key: 'expenses', width: 15 },
    { header: 'Profit', key: 'profit', width: 15 },
    { header: 'Margin %', key: 'margin', width: 12 }
  ];

  // Add data rows
  data.forEach((row, index) => {
    const rowIndex = index + 2; // Account for header row
    worksheet.addRow({
      month: row.month,
      revenue: row.revenue,
      expenses: row.expenses,
      profit: { formula: `B${rowIndex}-C${rowIndex}` }, // Revenue - Expenses
      margin: { formula: `D${rowIndex}/B${rowIndex}` }  // Profit / Revenue
    });
  });

  // Add totals row
  const lastRow = data.length + 2;
  worksheet.addRow({
    month: 'TOTAL',
    revenue: { formula: `SUM(B2:B${lastRow - 1})` },
    expenses: { formula: `SUM(C2:C${lastRow - 1})` },
    profit: { formula: `SUM(D2:D${lastRow - 1})` },
    margin: { formula: `D${lastRow}/B${lastRow}` }
  });

  // Format totals row
  worksheet.getRow(lastRow).font = { bold: true };
  worksheet.getRow(lastRow).fill = {
    type: 'pattern',
    pattern: 'solid',
    fgColor: { argb: 'FFE7E6E6' }
  };

  // Number formatting
  worksheet.getColumn('revenue').numFmt = '$#,##0.00';
  worksheet.getColumn('expenses').numFmt = '$#,##0.00';
  worksheet.getColumn('profit').numFmt = '$#,##0.00';
  worksheet.getColumn('margin').numFmt = '0.00%';

  await workbook.xlsx.writeFile(outputPath);
}
```

### Workflow 3: Apply Conditional Formatting
**Purpose:** Highlight cells based on rules and thresholds

**Steps:**
1. Create workbook with data
2. Define conditional formatting rules
3. Apply color scales for value ranges
4. Use data bars for visual comparison
5. Add icon sets for status indicators
6. Highlight top/bottom values
7. Apply custom formula-based rules

**Implementation:**
```javascript
async function addConditionalFormatting(data, outputPath) {
  const workbook = new ExcelJS.Workbook();
  const worksheet = workbook.addWorksheet('Performance');

  // Add data...
  worksheet.columns = [
    { header: 'Employee', key: 'name', width: 20 },
    { header: 'Sales', key: 'sales', width: 15 },
    { header: 'Target', key: 'target', width: 15 },
    { header: 'Performance', key: 'performance', width: 15 }
  ];

  data.forEach(row => worksheet.addRow(row));

  // Color scale: Green (high) to Red (low)
  worksheet.addConditionalFormatting({
    ref: 'B2:B100',
    rules: [
      {
        type: 'colorScale',
        cfvo: [
          { type: 'min' },
          { type: 'percentile', value: 50 },
          { type: 'max' }
        ],
        color: [
          { argb: 'FFF8696B' }, // Red
          { argb: 'FFFFEB84' }, // Yellow
          { argb: 'FF63BE7B' }  // Green
        ]
      }
    ]
  });

  // Data bars for performance column
  worksheet.addConditionalFormatting({
    ref: 'D2:D100',
    rules: [
      {
        type: 'dataBar',
        minLength: 0,
        maxLength: 100,
        color: { argb: 'FF638EC6' }
      }
    ]
  });

  // Highlight values above target
  worksheet.addConditionalFormatting({
    ref: 'B2:B100',
    rules: [
      {
        type: 'expression',
        formulae: ['B2>C2'], // Sales > Target
        style: {
          fill: {
            type: 'pattern',
            pattern: 'solid',
            bgColor: { argb: 'FFC6EFCE' }
          }
        }
      }
    ]
  });

  await workbook.xlsx.writeFile(outputPath);
}
```

### Workflow 4: Create Charts and Visualizations
**Purpose:** Add charts to visualize data trends and comparisons

**Steps:**
1. Create workbook with data
2. Add data worksheet
3. Create chart worksheet or embed in data sheet
4. Define chart type (bar, line, pie, scatter, etc.)
5. Set data ranges for series
6. Configure chart title, axes, legend
7. Apply styling and colors
8. Position chart on worksheet

**Implementation:**
```javascript
async function createWithChart(data, outputPath) {
  const workbook = new ExcelJS.Workbook();
  const worksheet = workbook.addWorksheet('Sales');

  // Add data
  worksheet.columns = [
    { header: 'Month', key: 'month', width: 12 },
    { header: 'Sales', key: 'sales', width: 15 }
  ];

  data.forEach(row => worksheet.addRow(row));

  // Create chart (Note: exceljs has limited chart support, consider using xlsx-chart)
  // For full chart support, you may need to use Excel templates or officegen library

  // Alternative: Add chart using worksheet image
  // Or use a charting library to generate image, then embed

  await workbook.xlsx.writeFile(outputPath);
}

// For advanced charts, consider using officegen or generating chart images
```

### Workflow 5: Multi-Sheet Workbook with Links
**Purpose:** Create complex workbooks with multiple related sheets

**Steps:**
1. Create workbook
2. Add multiple worksheets (Summary, Details, Raw Data, etc.)
3. Create cross-sheet formulas and references
4. Add hyperlinks between sheets
5. Protect sheets with passwords
6. Hide/show sheets as needed
7. Set active sheet and freeze panes

**Implementation:**
```javascript
async function createMultiSheetWorkbook(data, outputPath) {
  const workbook = new ExcelJS.Workbook();

  // Summary sheet
  const summary = workbook.addWorksheet('Summary');
  summary.columns = [
    { header: 'Metric', key: 'metric', width: 25 },
    { header: 'Value', key: 'value', width: 15 }
  ];

  summary.addRow({ metric: 'Total Sales', value: { formula: "SUM(Details!B:B)" } });
  summary.addRow({ metric: 'Average Order', value: { formula: "AVERAGE(Details!B:B)" } });
  summary.addRow({ metric: 'Total Orders', value: { formula: "COUNTA(Details!A:A)-1" } });

  // Details sheet
  const details = workbook.addWorksheet('Details');
  details.columns = [
    { header: 'Order ID', key: 'id', width: 12 },
    { header: 'Amount', key: 'amount', width: 15 },
    { header: 'Date', key: 'date', width: 12 }
  ];

  data.forEach(row => details.addRow(row));

  // Freeze header row
  details.views = [
    { state: 'frozen', xSplit: 0, ySplit: 1 }
  ];

  // Add hyperlink from summary to details
  summary.getCell('A1').value = {
    text: 'View Details',
    hyperlink: '#Details!A1',
    tooltip: 'Jump to Details sheet'
  };
  summary.getCell('A1').font = { color: { argb: 'FF0000FF' }, underline: true };

  // Set Summary as active sheet
  summary.state = 'visible';
  details.state = 'visible';

  await workbook.xlsx.writeFile(outputPath);
}
```

### Workflow 6: Export to CSV
**Purpose:** Create simple CSV files for data exchange

**Steps:**
1. Format data as array of objects or arrays
2. Define headers if needed
3. Convert to CSV format
4. Handle special characters and quotes
5. Set delimiter (comma, semicolon, tab)
6. Write to file with proper encoding

**Implementation:**
```javascript
const fs = require('fs');

function createCSV(data, outputPath, options = {}) {
  const delimiter = options.delimiter || ',';
  const headers = options.headers || Object.keys(data[0]);

  // Create header row
  let csv = headers.join(delimiter) + '\n';

  // Add data rows
  data.forEach(row => {
    const values = headers.map(header => {
      let value = row[header] || '';
      // Escape quotes and wrap in quotes if contains delimiter or newline
      if (typeof value === 'string' && (value.includes(delimiter) || value.includes('\n') || value.includes('"'))) {
        value = '"' + value.replace(/"/g, '""') + '"';
      }
      return value;
    });
    csv += values.join(delimiter) + '\n';
  });

  fs.writeFileSync(outputPath, csv, 'utf8');
}
```

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Create Excel workbook | "create excel file with [data]" |
| Generate CSV | "export [data] to csv" |
| Add formulas | "add formulas to spreadsheet" |
| Apply formatting | "format excel cells [style]" |
| Create chart | "add chart to workbook" |
| Multi-sheet workbook | "create workbook with [sheets]" |
| Conditional formatting | "apply conditional formatting" |
| Freeze panes | "freeze header row" |
| Protect sheet | "password protect [sheet]" |

## Best Practices

- **Data Validation:** Validate data types before writing to cells
- **Number Formatting:** Apply appropriate number formats (currency, percentage, date)
- **Column Widths:** Set widths based on content for readability
- **Freeze Panes:** Freeze header rows for scrollable data
- **Named Ranges:** Use named ranges for formulas in complex workbooks
- **Templates:** Create templates for repeated report types
- **Memory Management:** Use streaming for very large datasets (>100k rows)
- **Error Handling:** Wrap formula creation in try-catch for invalid references
- **CSV Encoding:** Use UTF-8 BOM for international characters
- **Performance:** Batch cell operations rather than individual cell writes
- **Testing:** Verify formulas calculate correctly after file creation
- **Documentation:** Comment complex formulas within cells

## Common Patterns

**Inventory Report:**
```javascript
worksheet.columns = [
  { header: 'SKU', key: 'sku', width: 15 },
  { header: 'Product', key: 'product', width: 30 },
  { header: 'Quantity', key: 'qty', width: 12 },
  { header: 'Unit Price', key: 'price', width: 15 },
  { header: 'Total Value', key: 'value', width: 15 }
];

data.forEach((item, idx) => {
  const row = idx + 2;
  worksheet.addRow({
    sku: item.sku,
    product: item.product,
    qty: item.qty,
    price: item.price,
    value: { formula: `C${row}*D${row}` }
  });
});
```

**Financial Dashboard:**
```javascript
// Summary sheet with KPIs
summary.addRow({ metric: 'Revenue', value: { formula: "SUM(Data!B:B)" } });
summary.addRow({ metric: 'Expenses', value: { formula: "SUM(Data!C:C)" } });
summary.addRow({ metric: 'Net Profit', value: { formula: "B2-B3" } });
summary.addRow({ metric: 'Profit Margin', value: { formula: "B4/B2" } });
summary.getColumn('value').numFmt = '$#,##0.00';
```

## Dependencies

Install required packages:
```bash
npm install exceljs
npm install xlsx      # Alternative library
npm install csv-writer # For CSV generation
```

## Error Handling

- **Invalid Formulas:** Validate formula syntax before assignment
- **Cell References:** Ensure referenced cells exist
- **File Permissions:** Handle write errors gracefully
- **Memory Limits:** Use streaming mode for files >50MB
- **Data Types:** Coerce data to appropriate types (number, string, date)
- **Encoding Issues:** Ensure UTF-8 encoding for international characters

## Performance Tips

- Use `worksheet.addRows()` instead of multiple `addRow()` calls
- Set column properties before adding data
- Avoid reading cells unnecessarily
- Use streaming write for large datasets
- Batch style operations
- Pre-calculate values instead of formulas when possible for static data

## Advanced Features

**Streaming Large Files:**
```javascript
const workbook = new ExcelJS.stream.xlsx.WorkbookWriter({ filename: outputPath });
const worksheet = workbook.addWorksheet('Large Data');
// Add data in chunks
worksheet.commit();
workbook.commit();
```

**Data Validation:**
```javascript
worksheet.getCell('A2').dataValidation = {
  type: 'list',
  allowBlank: true,
  formulae: ['"Option1,Option2,Option3"']
};
```

**Protection:**
```javascript
await worksheet.protect('password', {
  selectLockedCells: true,
  selectUnlockedCells: true
});
```