---
name: nixtla-schema-mapper
description: Analyzes data sources and generates Nixtla-compatible schema transformations. Infers column mappings, creates transformation modules for CSV/SQL/Parquet/dbt sources, generates schema contracts, and validates data quality. Activates when user needs data transformation, schema mapping, column inference, or Nixtla format conversion.
allowed-tools: "Read,Write,Glob,Grep,Edit"
version: "1.1.0"
license: MIT
---

# Nixtla Schema Mapper

Transform data sources to Nixtla-compatible schema (`unique_id`, `ds`, `y`).

## Overview

This skill automates data transformation:

- **Column inference**: Detects timestamp, target, and ID columns
- **Code generation**: Python modules for CSV/SQL/Parquet/dbt
- **Schema contracts**: Documentation with validation rules
- **Quality checks**: Validates transformed data

## Prerequisites

**Required**:
- Python 3.8+
- `pandas`

**Optional**:
- `pyarrow`: For Parquet support
- `sqlalchemy`: For SQL sources
- `dbt-core`: For dbt models

**Installation**:
```bash
pip install pandas pyarrow sqlalchemy
```

## Instructions

### Step 1: Identify Data Source

Supported formats:
- CSV/Parquet files
- SQL tables or queries
- dbt models

### Step 2: Analyze Schema

```bash
python {baseDir}/scripts/analyze_schema.py --input data/sales.csv
```

**Output**:
```
Detected columns:
  Timestamp: 'date' (datetime64)
  Target: 'sales' (float64)
  Series ID: 'store_id' (object)
  Exogenous: price, promotion
```

### Step 3: Generate Transformation

```bash
python {baseDir}/scripts/generate_transform.py \
    --input data/sales.csv \
    --id_col store_id \
    --date_col date \
    --target_col sales \
    --output data/transform/to_nixtla_schema.py
```

### Step 4: Create Schema Contract

```bash
python {baseDir}/scripts/create_contract.py \
    --mapping mapping.json \
    --output NIXTLA_SCHEMA_CONTRACT.md
```

### Step 5: Validate Transformation

```bash
python data/transform/to_nixtla_schema.py
```

## Output

- **data/transform/to_nixtla_schema.py**: Transformation module
- **NIXTLA_SCHEMA_CONTRACT.md**: Schema documentation
- **nixtla_data.csv**: Transformed data (optional)

## Error Handling

1. **Error**: `No timestamp column detected`
   **Solution**: Specify manually with `--date_col`

2. **Error**: `Multiple target candidates`
   **Solution**: Specify manually with `--target_col`

3. **Error**: `Date parsing failed`
   **Solution**: Specify format with `--date_format "%Y-%m-%d"`

4. **Error**: `Non-numeric target column`
   **Solution**: Check for string values, use `pd.to_numeric(errors='coerce')`

## Examples

### Example 1: CSV Transformation

```bash
python {baseDir}/scripts/generate_transform.py \
    --input sales.csv \
    --id_col product_id \
    --date_col timestamp \
    --target_col revenue
```

**Generated code**:
```python
def to_nixtla_schema(path="sales.csv"):
    df = pd.read_csv(path)
    df = df.rename(columns={
        'product_id': 'unique_id',
        'timestamp': 'ds',
        'revenue': 'y'
    })
    df['ds'] = pd.to_datetime(df['ds'])
    return df[['unique_id', 'ds', 'y']]
```

### Example 2: SQL Source

```bash
python {baseDir}/scripts/generate_transform.py \
    --sql "SELECT * FROM daily_sales" \
    --connection postgresql://localhost/db \
    --id_col store_id \
    --date_col sale_date \
    --target_col amount
```

## Resources

- Scripts: `{baseDir}/scripts/`
- Templates: `{baseDir}/assets/templates/`
- Nixtla Schema Docs: https://nixtla.github.io/statsforecast/

**Related Skills**:
- `nixtla-timegpt-lab`: Use transformed data for forecasting
- `nixtla-experiment-architect`: Reference in experiments
