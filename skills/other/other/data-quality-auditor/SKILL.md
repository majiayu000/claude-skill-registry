---
name: data-quality-auditor
description: Assess data quality with checks for missing values, duplicates, type issues, and inconsistencies. Use for data validation, ETL pipelines, or dataset documentation.
---

# Data Quality Auditor

Comprehensive data quality assessment for CSV/Excel datasets.

## Features

- **Completeness**: Missing values analysis
- **Uniqueness**: Duplicate detection
- **Validity**: Type validation and constraints
- **Consistency**: Pattern and format checks
- **Quality Score**: Overall data quality metric
- **Reports**: Detailed HTML/JSON reports

## Quick Start

```python
from data_quality_auditor import DataQualityAuditor

auditor = DataQualityAuditor()
auditor.load_csv("customers.csv")

# Run full audit
report = auditor.audit()
print(f"Quality Score: {report['quality_score']}/100")

# Check specific issues
missing = auditor.check_missing()
duplicates = auditor.check_duplicates()
```

## CLI Usage

```bash
# Full audit
python data_quality_auditor.py --input data.csv

# Generate HTML report
python data_quality_auditor.py --input data.csv --report report.html

# Check specific aspects
python data_quality_auditor.py --input data.csv --missing
python data_quality_auditor.py --input data.csv --duplicates
python data_quality_auditor.py --input data.csv --types

# JSON output
python data_quality_auditor.py --input data.csv --json

# Validate against rules
python data_quality_auditor.py --input data.csv --rules rules.json
```

## API Reference

### DataQualityAuditor Class

```python
class DataQualityAuditor:
    def __init__(self)

    # Data loading
    def load_csv(self, filepath: str, **kwargs) -> 'DataQualityAuditor'
    def load_dataframe(self, df: pd.DataFrame) -> 'DataQualityAuditor'

    # Full audit
    def audit(self) -> dict
    def quality_score(self) -> float

    # Individual checks
    def check_missing(self) -> dict
    def check_duplicates(self, subset: list = None) -> dict
    def check_types(self) -> dict
    def check_uniqueness(self) -> dict
    def check_patterns(self, column: str, pattern: str) -> dict

    # Validation
    def validate_column(self, column: str, rules: dict) -> dict
    def validate_dataset(self, rules: dict) -> dict

    # Reports
    def generate_report(self, output: str, format: str = "html") -> str
    def summary(self) -> str
```

## Quality Checks

### Missing Values
```python
missing = auditor.check_missing()
# Returns:
{
    "total_cells": 10000,
    "missing_cells": 150,
    "missing_percent": 1.5,
    "by_column": {
        "email": {"count": 50, "percent": 5.0},
        "phone": {"count": 100, "percent": 10.0}
    },
    "rows_with_missing": 120
}
```

### Duplicates
```python
dups = auditor.check_duplicates()
# Returns:
{
    "total_rows": 1000,
    "duplicate_rows": 25,
    "duplicate_percent": 2.5,
    "duplicate_groups": [...],
    "by_columns": {
        "email": {"duplicates": 15},
        "phone": {"duplicates": 20}
    }
}
```

### Type Validation
```python
types = auditor.check_types()
# Returns:
{
    "columns": {
        "age": {
            "detected_type": "int64",
            "unique_values": 75,
            "sample_values": [25, 30, 45],
            "issues": []
        },
        "date": {
            "detected_type": "object",
            "unique_values": 365,
            "sample_values": ["2023-01-01", "invalid"],
            "issues": ["Mixed date formats detected"]
        }
    }
}
```

## Validation Rules

Define custom validation rules:

```json
{
    "columns": {
        "email": {
            "required": true,
            "unique": true,
            "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        "age": {
            "type": "integer",
            "min": 0,
            "max": 120
        },
        "status": {
            "allowed_values": ["active", "inactive", "pending"]
        },
        "created_at": {
            "type": "date",
            "format": "%Y-%m-%d"
        }
    }
}
```

```python
results = auditor.validate_dataset(rules)
```

## Quality Score

The quality score (0-100) is calculated from:
- **Completeness** (30%): Missing value ratio
- **Uniqueness** (25%): Duplicate row ratio
- **Validity** (25%): Type and constraint compliance
- **Consistency** (20%): Format and pattern adherence

```python
score = auditor.quality_score()
# 85.5
```

## Output Formats

### Audit Report
```python
{
    "file": "data.csv",
    "rows": 1000,
    "columns": 15,
    "quality_score": 85.5,
    "completeness": {
        "score": 92.0,
        "missing_cells": 800,
        "details": {...}
    },
    "uniqueness": {
        "score": 97.5,
        "duplicate_rows": 25,
        "details": {...}
    },
    "validity": {
        "score": 78.0,
        "type_issues": [...],
        "details": {...}
    },
    "consistency": {
        "score": 80.0,
        "pattern_issues": [...],
        "details": {...}
    },
    "recommendations": [
        "Column 'phone' has 10% missing values",
        "25 duplicate rows detected",
        "Column 'date' has inconsistent formats"
    ]
}
```

## Example Workflows

### Pre-Import Validation
```python
auditor = DataQualityAuditor()
auditor.load_csv("import_data.csv")

report = auditor.audit()
if report['quality_score'] < 80:
    print("Data quality below threshold!")
    for rec in report['recommendations']:
        print(f"  - {rec}")
    exit(1)
```

### ETL Pipeline Check
```python
auditor = DataQualityAuditor()
auditor.load_dataframe(transformed_df)

# Check critical columns
email_check = auditor.validate_column("email", {
    "required": True,
    "unique": True,
    "pattern": r"^[\w.+-]+@[\w-]+\.[\w.-]+$"
})

if email_check['issues']:
    raise ValueError(f"Email validation failed: {email_check['issues']}")
```

### Generate Documentation
```python
auditor = DataQualityAuditor()
auditor.load_csv("dataset.csv")

# Generate comprehensive report
auditor.generate_report("quality_report.html", format="html")

# Or get summary text
print(auditor.summary())
```

## Dependencies

- pandas>=2.0.0
- numpy>=1.24.0
