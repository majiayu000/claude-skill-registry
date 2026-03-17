---
name: pivot-table-generator
description: Generate pivot tables from CSV/Excel with aggregations, filters, and automatic chart creation.
---

# Pivot Table Generator

Create pivot tables with aggregations and visualizations.

## Features

- **Multiple Aggregations**: Sum, mean, count, min, max
- **Filtering**: Filter data before pivoting
- **Grouping**: Multi-level row/column grouping
- **Charts**: Auto-generate pivot charts
- **Export**: Excel, CSV, HTML output

## CLI Usage

```bash
python pivot_table_generator.py --data sales.csv --rows region --columns product --values amount --agg sum
```

## Dependencies

- pandas>=2.0.0
- numpy>=1.24.0
- matplotlib>=3.7.0
- openpyxl>=3.1.0
