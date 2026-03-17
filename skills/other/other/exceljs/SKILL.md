---
name: exceljs
description: 在Node.js中读取、操作和写入Excel电子表格（XLSX）。完全支持样式、公式、图表和大文件流式处理。
metadata:
  short-description: Excel电子表格操作
source:
  repository: https://github.com/exceljs/exceljs
  license: MIT
  stars: 14k+
---

# ExcelJS Tool

## Description
Read, manipulate, and write Excel spreadsheets with full formatting support.

## Source
- Repository: [exceljs/exceljs](https://github.com/exceljs/exceljs)
- License: MIT

## Installation

```bash
npm install exceljs
```

## Usage Examples

### Create Excel File

```typescript
import ExcelJS from 'exceljs';

async function createReport() {
  const workbook = new ExcelJS.Workbook();
  workbook.creator = 'My App';
  workbook.created = new Date();
  
  const sheet = workbook.addWorksheet('Sales Report');
  
  // Define columns
  sheet.columns = [
    { header: 'ID', key: 'id', width: 10 },
    { header: 'Product', key: 'product', width: 30 },
    { header: 'Quantity', key: 'quantity', width: 15 },
    { header: 'Price', key: 'price', width: 15 },
    { header: 'Total', key: 'total', width: 15 },
  ];
  
  // Add data
  const data = [
    { id: 1, product: 'Widget A', quantity: 100, price: 9.99 },
    { id: 2, product: 'Widget B', quantity: 50, price: 19.99 },
    { id: 3, product: 'Widget C', quantity: 75, price: 14.99 },
  ];
  
  data.forEach(item => {
    sheet.addRow({
      ...item,
      total: { formula: `C${sheet.rowCount + 1}*D${sheet.rowCount + 1}` },
    });
  });
  
  await workbook.xlsx.writeFile('report.xlsx');
}
```

### Style Cells

```typescript
async function createStyledReport() {
  const workbook = new ExcelJS.Workbook();
  const sheet = workbook.addWorksheet('Styled');
  
  // Header row with styling
  const headerRow = sheet.addRow(['Name', 'Email', 'Status']);
  headerRow.eachCell(cell => {
    cell.fill = {
      type: 'pattern',
      pattern: 'solid',
      fgColor: { argb: '4F46E5' },
    };
    cell.font = { color: { argb: 'FFFFFF' }, bold: true };
    cell.alignment = { horizontal: 'center' };
    cell.border = {
      top: { style: 'thin' },
      bottom: { style: 'thin' },
    };
  });
  
  // Data rows
  const users = [
    { name: 'John', email: 'john@example.com', status: 'Active' },
    { name: 'Jane', email: 'jane@example.com', status: 'Inactive' },
  ];
  
  users.forEach(user => {
    const row = sheet.addRow([user.name, user.email, user.status]);
    
    // Conditional formatting
    const statusCell = row.getCell(3);
    statusCell.fill = {
      type: 'pattern',
      pattern: 'solid',
      fgColor: { argb: user.status === 'Active' ? '22C55E' : 'EF4444' },
    };
  });
  
  await workbook.xlsx.writeFile('styled-report.xlsx');
}
```

### Read Excel File

```typescript
async function readExcel(filePath: string) {
  const workbook = new ExcelJS.Workbook();
  await workbook.xlsx.readFile(filePath);
  
  const sheet = workbook.getWorksheet('Sheet1');
  const data: any[] = [];
  
  sheet?.eachRow((row, rowNumber) => {
    if (rowNumber === 1) return; // Skip header
    
    data.push({
      id: row.getCell(1).value,
      name: row.getCell(2).value,
      email: row.getCell(3).value,
    });
  });
  
  return data;
}
```

### Stream Large Files

```typescript
async function streamLargeExcel(data: any[], outputPath: string) {
  const workbook = new ExcelJS.stream.xlsx.WorkbookWriter({
    filename: outputPath,
    useStyles: true,
  });
  
  const sheet = workbook.addWorksheet('Data');
  sheet.columns = [
    { header: 'ID', key: 'id' },
    { header: 'Value', key: 'value' },
  ];
  
  // Stream rows (memory efficient)
  for (const item of data) {
    sheet.addRow(item).commit();
  }
  
  await workbook.commit();
}
```

## Tags
`excel`, `spreadsheet`, `xlsx`, `report`, `data-export`

## Compatibility
- Codex: ✅
- Claude Code: ✅
