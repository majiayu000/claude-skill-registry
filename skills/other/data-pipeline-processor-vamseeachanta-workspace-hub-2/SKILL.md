---
name: data-pipeline-processor
description: Process data files through transformation pipelines with validation, cleaning, and export. Use for CSV/Excel/JSON data processing, encoding handling, batch operations, and data transformation workflows.
version: 1.1.0
category: development
related_skills:
  - yaml-workflow-executor
  - engineering-report-generator
  - parallel-file-processor
---

# Data Pipeline Processor

> Version: 1.1.0
> Category: Development
> Last Updated: 2026-01-02

Process data files through transformation pipelines with validation, encoding detection, and multi-format export capabilities.

## Quick Start

```python
import pandas as pd
from pathlib import Path

# Simple pipeline: Load -> Transform -> Export
df = pd.read_csv("data/raw/source.csv")

# Transform
df = df[df['value'] > 0]  # Filter
df['date'] = pd.to_datetime(df['date'])  # Convert types
df = df.sort_values('date')  # Sort

# Export
Path("data/processed").mkdir(parents=True, exist_ok=True)
df.to_csv("data/processed/cleaned.csv", index=False)

print(f"Processed {len(df)} rows")
```

## When to Use

- Processing CSV/Excel/JSON files with validation
- Data cleaning and transformation workflows
- Batch file processing with aggregation
- Handling encoding issues (UTF-8, Latin-1 fallback)
- ETL (Extract, Transform, Load) operations
- Data quality checks and reporting

## Core Pattern

```
Input (CSV/Excel/JSON) -> Validate -> Transform -> Analyze -> Export
```

## Implementation

### Data Reader with Encoding Detection

```python
import pandas as pd
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import logging
import chardet

logger = logging.getLogger(__name__)


class DataReader:
    """Read data files with automatic encoding detection."""

    SUPPORTED_FORMATS = ['csv', 'xlsx', 'xls', 'json', 'parquet']

    def __init__(self, encoding_fallback: List[str] = None):
        """
        Initialize data reader.

        Args:
            encoding_fallback: List of encodings to try in order
        """
        self.encoding_fallback = encoding_fallback or ['utf-8', 'latin-1', 'cp1252']

    def read(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Read data file with automatic format and encoding detection.

        Args:
            file_path: Path to data file
            **kwargs: Additional arguments for pandas readers

        Returns:
            DataFrame with loaded data
        """
        path = Path(file_path)
        suffix = path.suffix.lower().lstrip('.')

        if suffix == 'csv':
            return self._read_csv(path, **kwargs)
        elif suffix in ['xlsx', 'xls']:
            return self._read_excel(path, **kwargs)
        elif suffix == 'json':
            return pd.read_json(path, **kwargs)
        elif suffix == 'parquet':
            return pd.read_parquet(path, **kwargs)
        else:
            raise ValueError(f"Unsupported format: {suffix}")

    def _read_csv(self, path: Path, **kwargs) -> pd.DataFrame:
        """Read CSV with encoding fallback."""
        # Try to detect encoding
        with open(path, 'rb') as f:
            raw = f.read(10000)
            detected = chardet.detect(raw)
            detected_encoding = detected.get('encoding', 'utf-8')

        # Try detected encoding first, then fallbacks
        encodings_to_try = [detected_encoding] + self.encoding_fallback

        for encoding in encodings_to_try:
            try:
                df = pd.read_csv(path, encoding=encoding, **kwargs)
                logger.info(f"Successfully read {path} with encoding: {encoding}")
                return df
            except UnicodeDecodeError:
                continue

        raise ValueError(f"Could not decode {path} with any encoding")

    def _read_excel(self, path: Path, **kwargs) -> pd.DataFrame:
        """Read Excel file."""
        return pd.read_excel(path, **kwargs)
```

### Data Validator

```python
from dataclasses import dataclass, field
from typing import Callable, List, Dict, Any


@dataclass
class ValidationResult:
    """Result of data validation."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)


class DataValidator:
    """Validate data against configurable rules."""

    def __init__(self):
        self.rules: List[Callable] = []

    def add_rule(self, rule: Callable[[pd.DataFrame], ValidationResult]):
        """Add a validation rule."""
        self.rules.append(rule)

    def validate(self, df: pd.DataFrame) -> ValidationResult:
        """Run all validation rules."""
        all_errors = []
        all_warnings = []
        all_stats = {}

        for rule in self.rules:
            result = rule(df)
            all_errors.extend(result.errors)
            all_warnings.extend(result.warnings)
            all_stats.update(result.stats)

        return ValidationResult(
            is_valid=len(all_errors) == 0,
            errors=all_errors,
            warnings=all_warnings,
            stats=all_stats
        )


# Common validation rules
def required_columns_rule(required: List[str]) -> Callable:
    """Validate required columns exist."""
    def rule(df: pd.DataFrame) -> ValidationResult:
        missing = [col for col in required if col not in df.columns]
        return ValidationResult(
            is_valid=len(missing) == 0,
            errors=[f"Missing required column: {col}" for col in missing],
            stats={'columns_found': len(df.columns)}
        )
    return rule


def no_duplicates_rule(subset: List[str] = None) -> Callable:
    """Validate no duplicate rows."""
    def rule(df: pd.DataFrame) -> ValidationResult:
        duplicates = df.duplicated(subset=subset).sum()
        return ValidationResult(
            is_valid=duplicates == 0,
            warnings=[f"Found {duplicates} duplicate rows"] if duplicates > 0 else [],
            stats={'duplicate_count': duplicates}
        )
    return rule


def non_null_rule(columns: List[str]) -> Callable:
    """Validate specified columns have no null values."""
    def rule(df: pd.DataFrame) -> ValidationResult:
        errors = []
        stats = {}
        for col in columns:
            if col in df.columns:
                null_count = df[col].isnull().sum()
                stats[f'{col}_nulls'] = null_count
                if null_count > 0:
                    errors.append(f"Column '{col}' has {null_count} null values")
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            stats=stats
        )
    return rule
```

### Data Transformer

```python
class DataTransformer:
    """Apply transformations to data."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def rename_columns(self, mapping: Dict[str, str]) -> 'DataTransformer':
        """Rename columns."""
        self.df = self.df.rename(columns=mapping)
        return self

    def filter_rows(self, expression: str) -> 'DataTransformer':
        """Filter rows using query expression."""
        self.df = self.df.query(expression)
        return self

    def select_columns(self, columns: List[str]) -> 'DataTransformer':
        """Select specific columns."""
        self.df = self.df[columns]
        return self

    def drop_columns(self, columns: List[str]) -> 'DataTransformer':
        """Drop specified columns."""
        self.df = self.df.drop(columns=columns, errors='ignore')
        return self

    def fill_nulls(self, value: Any = None, method: str = None) -> 'DataTransformer':
        """Fill null values."""
        if method:
            self.df = self.df.fillna(method=method)
        else:
            self.df = self.df.fillna(value)
        return self

    def convert_types(self, type_mapping: Dict[str, str]) -> 'DataTransformer':
        """Convert column types."""
        for col, dtype in type_mapping.items():
            if col in self.df.columns:
                if dtype == 'datetime':
                    self.df[col] = pd.to_datetime(self.df[col])
                elif dtype == 'numeric':
                    self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                else:
                    self.df[col] = self.df[col].astype(dtype)
        return self

    def add_column(self, name: str, expression: Callable) -> 'DataTransformer':
        """Add computed column."""
        self.df[name] = expression(self.df)
        return self

    def aggregate(self, group_by: List[str], agg_spec: Dict[str, Any]) -> 'DataTransformer':
        """Aggregate data by groups."""
        self.df = self.df.groupby(group_by).agg(agg_spec).reset_index()
        return self

    def sort(self, by: List[str], ascending: bool = True) -> 'DataTransformer':
        """Sort data."""
        self.df = self.df.sort_values(by=by, ascending=ascending)
        return self

    def get_result(self) -> pd.DataFrame:
        """Get transformed DataFrame."""
        return self.df
```

### Data Exporter

```python
class DataExporter:
    """Export data to various formats."""

    @staticmethod
    def to_csv(df: pd.DataFrame, path: str, **kwargs) -> str:
        """Export to CSV."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False, **kwargs)
        return path

    @staticmethod
    def to_excel(df: pd.DataFrame, path: str, sheet_name: str = 'Sheet1', **kwargs) -> str:
        """Export to Excel."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(path, sheet_name=sheet_name, index=False, **kwargs)
        return path

    @staticmethod
    def to_json(df: pd.DataFrame, path: str, orient: str = 'records', **kwargs) -> str:
        """Export to JSON."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        df.to_json(path, orient=orient, **kwargs)
        return path

    @staticmethod
    def to_parquet(df: pd.DataFrame, path: str, **kwargs) -> str:
        """Export to Parquet."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path, **kwargs)
        return path
```

### Pipeline Orchestrator

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class PipelineConfig:
    """Configuration for data pipeline."""
    input_path: str
    output_path: str
    input_options: Dict[str, Any] = field(default_factory=dict)
    validation: Dict[str, Any] = field(default_factory=dict)
    transformations: List[Dict[str, Any]] = field(default_factory=list)
    output_format: str = 'csv'
    output_options: Dict[str, Any] = field(default_factory=dict)


class DataPipeline:
    """Orchestrate data processing pipeline."""

    def __init__(self, config: PipelineConfig):
        self.config = config
        self.reader = DataReader()
        self.validator = DataValidator()
        self.exporter = DataExporter()

    def _setup_validation(self):
        """Configure validation rules from config."""
        validation = self.config.validation

        if 'required_columns' in validation:
            self.validator.add_rule(
                required_columns_rule(validation['required_columns'])
            )

        if 'no_duplicates' in validation:
            self.validator.add_rule(
                no_duplicates_rule(validation.get('no_duplicates_subset'))
            )

        if 'non_null_columns' in validation:
            self.validator.add_rule(
                non_null_rule(validation['non_null_columns'])
            )

    def _apply_transformations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply configured transformations."""
        transformer = DataTransformer(df)

        for transform in self.config.transformations:
            op = transform['operation']

            if op == 'rename':
                transformer.rename_columns(transform['mapping'])
            elif op == 'filter':
                transformer.filter_rows(transform['expression'])
            elif op == 'select':
                transformer.select_columns(transform['columns'])
            elif op == 'drop':
                transformer.drop_columns(transform['columns'])
            elif op == 'fill_nulls':
                transformer.fill_nulls(
                    value=transform.get('value'),
                    method=transform.get('method')
                )
            elif op == 'convert_types':
                transformer.convert_types(transform['types'])
            elif op == 'aggregate':
                transformer.aggregate(
                    group_by=transform['group_by'],
                    agg_spec=transform['aggregations']
                )
            elif op == 'sort':
                transformer.sort(
                    by=transform['by'],
                    ascending=transform.get('ascending', True)
                )

        return transformer.get_result()

    def run(self) -> Dict[str, Any]:
        """Execute the pipeline."""
        logger.info(f"Starting pipeline: {self.config.input_path}")

        # Read input
        df = self.reader.read(self.config.input_path, **self.config.input_options)
        logger.info(f"Loaded {len(df)} rows")

        # Validate
        self._setup_validation()
        validation_result = self.validator.validate(df)

        if not validation_result.is_valid:
            logger.error(f"Validation failed: {validation_result.errors}")
            return {
                'status': 'failed',
                'stage': 'validation',
                'errors': validation_result.errors,
                'warnings': validation_result.warnings
            }

        if validation_result.warnings:
            logger.warning(f"Validation warnings: {validation_result.warnings}")

        # Transform
        df = self._apply_transformations(df)
        logger.info(f"Transformed to {len(df)} rows")

        # Export
        export_method = getattr(self.exporter, f'to_{self.config.output_format}')
        output_path = export_method(df, self.config.output_path, **self.config.output_options)
        logger.info(f"Exported to {output_path}")

        return {
            'status': 'success',
            'input_rows': len(df),
            'output_rows': len(df),
            'output_path': output_path,
            'validation_stats': validation_result.stats,
            'warnings': validation_result.warnings
        }
```

## YAML Configuration Format

### Basic Pipeline Config

```yaml
# config/pipelines/data_clean.yaml

input:
  path: data/raw/source.csv
  options:
    delimiter: ","
    skiprows: 1

validation:
  required_columns:
    - id
    - timestamp
    - value
  non_null_columns:
    - id
    - value
  no_duplicates: true
  no_duplicates_subset:
    - id

transformations:
  - operation: rename
    mapping:
      old_name: new_name
      date_col: timestamp

  - operation: filter
    expression: "value > 0 and status != 'invalid'"

  - operation: convert_types
    types:
      timestamp: datetime
      value: numeric

  - operation: fill_nulls
    value: 0

  - operation: sort
    by: [timestamp]
    ascending: true

output:
  path: data/processed/cleaned.csv
  format: csv
  options:
    index: false
```

### Aggregation Pipeline

```yaml
# config/pipelines/monthly_summary.yaml

input:
  path: data/processed/daily_data.csv

validation:
  required_columns:
    - date
    - category
    - amount

transformations:
  - operation: convert_types
    types:
      date: datetime

  - operation: aggregate
    group_by: [category]
    aggregations:
      amount:
        - sum
        - mean
        - count

  - operation: rename
    mapping:
      amount_sum: total_amount
      amount_mean: average_amount
      amount_count: transaction_count

  - operation: sort
    by: [total_amount]
    ascending: false

output:
  path: data/results/monthly_summary.csv
  format: csv
```

## Usage Examples

### Example 1: Simple CSV Processing

```bash
# Process CSV with config
python -m data_pipeline config/pipelines/clean_data.yaml

# Override input/output
python -m data_pipeline config/pipelines/clean_data.yaml \
    --input data/custom_input.csv \
    --output data/custom_output.csv

# Dry run (validate only)
python -m data_pipeline config/pipelines/clean_data.yaml --dry-run
```

### Example 2: Programmatic Usage

```python
from data_pipeline import DataPipeline, PipelineConfig

config = PipelineConfig(
    input_path='data/raw/sales.csv',
    output_path='data/processed/sales_clean.csv',
    validation={
        'required_columns': ['date', 'product', 'amount'],
        'non_null_columns': ['amount']
    },
    transformations=[
        {'operation': 'filter', 'expression': 'amount > 0'},
        {'operation': 'sort', 'by': ['date']}
    ]
)

pipeline = DataPipeline(config)
result = pipeline.run()
print(f"Processed {result['output_rows']} rows")
```

### Example 3: Batch Processing

```python
from pathlib import Path
from data_pipeline import DataReader, DataTransformer, DataExporter

reader = DataReader()
exporter = DataExporter()

# Process all CSV files in directory
input_dir = Path('data/raw/')
output_dir = Path('data/processed/')

for csv_file in input_dir.glob('*.csv'):
    df = reader.read(str(csv_file))

    # Apply transformations
    df_clean = (DataTransformer(df)
        .fill_nulls(value=0)
        .filter_rows('value > 0')
        .sort(['timestamp'])
        .get_result())

    # Export
    output_path = output_dir / csv_file.name
    exporter.to_csv(df_clean, str(output_path))
    print(f"Processed: {csv_file.name}")
```

### Example 4: Multi-Format Export

```python
def export_all_formats(df: pd.DataFrame, base_path: str):
    """Export data to multiple formats."""
    exporter = DataExporter()

    outputs = {
        'csv': exporter.to_csv(df, f"{base_path}.csv"),
        'json': exporter.to_json(df, f"{base_path}.json"),
        'parquet': exporter.to_parquet(df, f"{base_path}.parquet"),
        'excel': exporter.to_excel(df, f"{base_path}.xlsx")
    }

    return outputs
```

## Best Practices

### Do

1. Always detect encoding before reading CSV
2. Use chunked reading for large files (>100MB)
3. Specify dtypes to reduce memory usage
4. Handle missing values explicitly
5. Validate early in the pipeline
6. Fail fast on critical errors
7. Log warnings for non-critical issues
8. Track validation statistics

### Don't

1. Assume encoding is always UTF-8
2. Load entire large files into memory
3. Skip validation steps
4. Ignore encoding errors
5. Mix transformation and validation

### Data Reading
- Always detect encoding before reading CSV
- Use chunked reading for large files (>100MB)
- Specify dtypes to reduce memory usage
- Handle missing values explicitly

### Validation
- Validate early in the pipeline
- Fail fast on critical errors
- Log warnings for non-critical issues
- Track validation statistics

### Transformation
- Use method chaining for readability
- Apply filters before expensive operations
- Convert types early to catch errors
- Document transformation logic

### Export
- Create output directories automatically
- Use appropriate formats (Parquet for large data)
- Include metadata in output
- Verify output integrity

### File Organization
```
project/
    config/
        pipelines/           # Pipeline configs
            clean_data.yaml
            aggregate.yaml
    data/
        raw/                 # Raw input data
        processed/           # Cleaned data
        results/             # Analysis results
    src/
        data_pipeline/       # Pipeline code
    scripts/
        run_pipeline.sh      # CLI wrapper
```

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `UnicodeDecodeError` | Wrong encoding | Use DataReader with encoding fallback |
| `KeyError` | Missing column | Check column names in config |
| `ValueError` | Type conversion failed | Use errors='coerce' or validate first |
| `MemoryError` | File too large | Use chunked reading |
| `FileNotFoundError` | Input file missing | Verify file path |

### Error Template

```python
def safe_pipeline_run(config: PipelineConfig) -> dict:
    """Run pipeline with comprehensive error handling."""
    try:
        # Validate input exists
        if not Path(config.input_path).exists():
            return {'status': 'error', 'stage': 'input', 'message': 'File not found'}

        pipeline = DataPipeline(config)
        return pipeline.run()

    except UnicodeDecodeError as e:
        return {'status': 'error', 'stage': 'read', 'message': f'Encoding error: {e}'}
    except KeyError as e:
        return {'status': 'error', 'stage': 'transform', 'message': f'Missing column: {e}'}
    except Exception as e:
        return {'status': 'error', 'stage': 'unknown', 'message': str(e)}
```

## Execution Checklist

- [ ] Input file exists and is readable
- [ ] Encoding detected or specified
- [ ] Required columns present
- [ ] Validation rules configured
- [ ] Transformations in correct order
- [ ] Output directory exists or is created
- [ ] Export format appropriate for data size
- [ ] Error handling covers all failure modes
- [ ] Logging configured for debugging

## Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Read Time | <1s per 100MB | Data loading speed |
| Validation Time | <500ms | Rule checking duration |
| Transform Time | Varies | Depends on operations |
| Export Time | <1s per 100MB | File writing speed |
| Memory Usage | <2x file size | Peak memory consumption |

## Related Skills

- [yaml-workflow-executor](../yaml-workflow-executor/SKILL.md) - Workflow orchestration
- [engineering-report-generator](../engineering-report-generator/SKILL.md) - Report generation
- [parallel-file-processor](../parallel-file-processor/SKILL.md) - Parallel file operations

---

## Version History

- **1.1.0** (2026-01-02): Upgraded to SKILL_TEMPLATE_v2 format with Quick Start, Error Handling, Metrics, Execution Checklist, additional examples
- **1.0.0** (2024-10-15): Initial release with DataReader, DataValidator, DataTransformer, pipeline orchestration
