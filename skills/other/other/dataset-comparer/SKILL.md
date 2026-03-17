---
name: dataset-comparer
description: Compare two datasets to find differences, added/removed rows, changed values. Use for data validation, ETL verification, or tracking changes.
---

# Dataset Comparer

Compare two CSV/Excel datasets to identify differences, additions, deletions, and value changes.

## Features

- **Row Comparison**: Find added, removed, and matching rows
- **Value Changes**: Detect changed values in matching rows
- **Column Comparison**: Identify schema differences
- **Statistics**: Summary of differences
- **Diff Reports**: HTML, CSV, and JSON output
- **Flexible Matching**: Compare by key columns or row position

## Quick Start

```python
from dataset_comparer import DatasetComparer

comparer = DatasetComparer()
comparer.load("old_data.csv", "new_data.csv")

# Compare by key column
diff = comparer.compare(key_columns=["id"])

print(f"Added rows: {diff['added_count']}")
print(f"Removed rows: {diff['removed_count']}")
print(f"Changed rows: {diff['changed_count']}")

# Generate report
comparer.generate_report("diff_report.html")
```

## CLI Usage

```bash
# Basic comparison
python dataset_comparer.py --old old.csv --new new.csv

# Compare by key column
python dataset_comparer.py --old old.csv --new new.csv --key id

# Multiple key columns
python dataset_comparer.py --old old.csv --new new.csv --key id,date

# Generate HTML report
python dataset_comparer.py --old old.csv --new new.csv --key id --report diff.html

# Export differences to CSV
python dataset_comparer.py --old old.csv --new new.csv --key id --output diff.csv

# JSON output
python dataset_comparer.py --old old.csv --new new.csv --key id --json

# Ignore specific columns
python dataset_comparer.py --old old.csv --new new.csv --key id --ignore updated_at,modified_date

# Compare only specific columns
python dataset_comparer.py --old old.csv --new new.csv --key id --columns name,email,status
```

## API Reference

### DatasetComparer Class

```python
class DatasetComparer:
    def __init__(self)

    # Data loading
    def load(self, old_path: str, new_path: str) -> 'DatasetComparer'
    def load_dataframes(self, old_df: pd.DataFrame,
                       new_df: pd.DataFrame) -> 'DatasetComparer'

    # Comparison
    def compare(self, key_columns: list = None,
               ignore_columns: list = None,
               compare_columns: list = None) -> dict

    # Detailed results
    def get_added_rows(self) -> pd.DataFrame
    def get_removed_rows(self) -> pd.DataFrame
    def get_changed_rows(self) -> pd.DataFrame
    def get_unchanged_rows(self) -> pd.DataFrame

    # Schema comparison
    def compare_schema(self) -> dict

    # Reports
    def generate_report(self, output: str, format: str = "html") -> str
    def to_dataframe(self) -> pd.DataFrame
    def summary(self) -> str
```

## Comparison Methods

### Key-Based Comparison

Compare rows by matching key columns (like primary keys):

```python
diff = comparer.compare(key_columns=["customer_id"])

# Multiple keys for composite matching
diff = comparer.compare(key_columns=["order_id", "product_id"])
```

### Position-Based Comparison

Compare rows by their position (row number):

```python
diff = comparer.compare()  # No keys = positional comparison
```

## Output Format

### Comparison Result

```python
{
    "summary": {
        "old_rows": 1000,
        "new_rows": 1050,
        "added_count": 75,
        "removed_count": 25,
        "changed_count": 50,
        "unchanged_count": 900,
        "total_differences": 150
    },
    "schema_changes": {
        "added_columns": ["new_field"],
        "removed_columns": ["old_field"],
        "type_changes": [
            {"column": "amount", "old_type": "int64", "new_type": "float64"}
        ]
    },
    "key_columns": ["id"],
    "compared_columns": ["name", "email", "status"],
    "ignored_columns": ["updated_at"]
}
```

### Changed Row Details

```python
changes = comparer.get_changed_rows()

# Returns DataFrame with columns:
# _key: Key value(s) for the row
# _column: Column that changed
# _old_value: Original value
# _new_value: New value
```

## Schema Comparison

Compare column structure:

```python
schema = comparer.compare_schema()

# Returns:
{
    "old_columns": ["id", "name", "old_field"],
    "new_columns": ["id", "name", "new_field"],
    "common_columns": ["id", "name"],
    "added_columns": ["new_field"],
    "removed_columns": ["old_field"],
    "type_changes": [
        {"column": "price", "old_type": "int64", "new_type": "float64"}
    ],
    "old_row_count": 1000,
    "new_row_count": 1050
}
```

## Filtering Options

### Ignore Columns

Skip certain columns during comparison:

```python
diff = comparer.compare(
    key_columns=["id"],
    ignore_columns=["updated_at", "modified_by", "timestamp"]
)
```

### Compare Specific Columns

Only compare selected columns:

```python
diff = comparer.compare(
    key_columns=["id"],
    compare_columns=["name", "email", "status"]  # Only these columns
)
```

## Report Formats

### HTML Report

```python
comparer.generate_report("diff_report.html", format="html")
```

Features:
- Summary statistics
- Interactive tables
- Color-coded changes (green=added, red=removed, yellow=changed)
- Schema comparison section

### CSV Export

```python
comparer.generate_report("diff_report.csv", format="csv")
```

Includes all differences in tabular format.

### JSON Output

```python
comparer.generate_report("diff_report.json", format="json")
```

Complete diff data in JSON format.

## Example Workflows

### Data Migration Validation

```python
comparer = DatasetComparer()
comparer.load("source_data.csv", "migrated_data.csv")

diff = comparer.compare(key_columns=["id"])

if diff["summary"]["total_differences"] == 0:
    print("Migration successful - no differences!")
else:
    print(f"Found {diff['summary']['total_differences']} differences")
    comparer.generate_report("migration_issues.html")
```

### ETL Pipeline Verification

```python
comparer = DatasetComparer()
comparer.load("yesterday.csv", "today.csv")

diff = comparer.compare(
    key_columns=["transaction_id"],
    ignore_columns=["processing_timestamp"]
)

# Check for unexpected changes
changed = comparer.get_changed_rows()
if len(changed) > 0:
    print("Warning: Historical records changed!")
    print(changed)
```

### Incremental Update Detection

```python
comparer = DatasetComparer()
comparer.load("last_sync.csv", "current.csv")

diff = comparer.compare(key_columns=["customer_id"])

# Get new records for processing
new_records = comparer.get_added_rows()
print(f"New records to process: {len(new_records)}")

# Get deleted records
deleted = comparer.get_removed_rows()
print(f"Records to deactivate: {len(deleted)}")
```

### Schema Change Detection

```python
comparer = DatasetComparer()
comparer.load("v1_export.csv", "v2_export.csv")

schema = comparer.compare_schema()

if schema["added_columns"]:
    print(f"New columns: {schema['added_columns']}")

if schema["removed_columns"]:
    print(f"Removed columns: {schema['removed_columns']}")

if schema["type_changes"]:
    for change in schema["type_changes"]:
        print(f"Type change: {change['column']} "
              f"({change['old_type']} -> {change['new_type']})")
```

## Large Dataset Tips

For very large datasets:

```python
# Compare in chunks
comparer = DatasetComparer()
comparer.load("large_old.csv", "large_new.csv")

# Use key column for efficient matching
diff = comparer.compare(key_columns=["id"])

# Export only differences (not full data)
comparer.generate_report("diff_only.csv", format="csv")
```

## Dependencies

- pandas>=2.0.0
- numpy>=1.24.0
