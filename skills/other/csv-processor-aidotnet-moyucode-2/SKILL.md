---
name: csv-processor
description: 读取、写入、转换和分析CSV文件，支持过滤、排序、聚合和格式转换。
metadata:
  short-description: 处理CSV文件
source:
  repository: https://github.com/pandas-dev/pandas
  license: BSD-3-Clause
---

# CSV Processor Tool

## Description
Process CSV files with powerful data manipulation capabilities including filtering, sorting, aggregation, and format conversion.

## Trigger
- `/csv` command
- User needs to process CSV data
- User wants to transform or analyze tabular data

## Usage

```bash
# Read and display CSV
python scripts/csv_processor.py read data.csv

# Filter rows
python scripts/csv_processor.py filter data.csv --column "status" --value "active"

# Sort by column
python scripts/csv_processor.py sort data.csv --by "date" --desc

# Convert to JSON
python scripts/csv_processor.py convert data.csv --format json --output data.json

# Aggregate data
python scripts/csv_processor.py aggregate data.csv --group "category" --sum "amount"
```

## Tags
`csv`, `data`, `transform`, `analysis`, `pandas`

## Compatibility
- Codex: ✅
- Claude Code: ✅
