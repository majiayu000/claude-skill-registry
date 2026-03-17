---
name: excel-handler
description: 读取、写入和操作Excel文件（.xlsx、.xls）。创建电子表格、读取数据并导出为各种格式。
metadata:
  short-description: 读写Excel文件
source:
  repository: https://github.com/python-excel/xlrd
  license: BSD
---

# Excel Handler Tool

## Description
Read, write, and manipulate Excel spreadsheets with support for formulas, styling, and data export.

## Trigger
- `/excel` command
- User requests Excel file operations
- User needs to read or create spreadsheets

## Usage

```bash
# Read Excel to JSON
python scripts/excel_handler.py read --input data.xlsx --output data.json

# Create Excel from JSON/CSV
python scripts/excel_handler.py create --input data.json --output report.xlsx

# Convert Excel to CSV
python scripts/excel_handler.py convert --input data.xlsx --output data.csv

# Merge multiple Excel files
python scripts/excel_handler.py merge --inputs file1.xlsx,file2.xlsx --output merged.xlsx
```

## Tags
`excel`, `spreadsheet`, `xlsx`, `csv`, `data`

## Compatibility
- Codex: ✅
- Claude Code: ✅
