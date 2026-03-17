---
name: data-profiler
description: Generate comprehensive data profiles for DataFrames. Use for EDA, data discovery, and understanding dataset characteristics.
allowed-tools: Read Write Edit Bash
---

# Data Profiler

**Audience:** Data engineers and analysts exploring new datasets.

**Goal:** Generate comprehensive profiles including statistics, correlations, and missing patterns.

## Scripts

Execute profiling functions from `scripts/profiling.py`:

```python
from scripts.profiling import (
    profile_dataframe,
    print_profile_summary,
    profile_correlations,
    profile_missing_patterns
)
```

## Usage Examples

### Basic Profiling

```python
import pandas as pd
from scripts.profiling import profile_dataframe, print_profile_summary

df = pd.read_csv('data.csv')
profile = profile_dataframe(df)
print_profile_summary(profile)
```

**Output:**
```
Shape: 10,000 rows x 15 columns
Memory: 1.23 MB

Column Summary:
  id (int64): 10,000 unique, no nulls
  email (object): 9,847 unique, 1.53% null
  revenue (float64): 3,421 unique, no nulls
  created_at (datetime64[ns]): 365 unique, no nulls
```

### Correlation Analysis

```python
from scripts.profiling import profile_correlations

corr = profile_correlations(df, threshold=0.7)

if corr['high_correlations']:
    print("Highly correlated columns:")
    for c in corr['high_correlations']:
        print(f"  {c['col1']} <-> {c['col2']}: {c['correlation']}")
```

### Missing Data Patterns

```python
from scripts.profiling import profile_missing_patterns

missing = profile_missing_patterns(df)

for col, stats in missing.items():
    if col != 'co_missing_columns':
        print(f"{col}: {stats['percent']}% missing, max {stats['consecutive_max']} consecutive")

# Check for columns missing together
if 'co_missing_columns' in missing:
    for col1, col2, pct in missing['co_missing_columns']:
        print(f"{col1} and {col2} both missing {pct}% of time")
```

## Profile Output Schema

```yaml
shape: [rows, columns]
memory_mb: float
columns:
  column_name:
    dtype: string
    null_count: int
    null_pct: float
    unique_count: int
    unique_pct: float
    # Numeric columns add:
    min: float
    max: float
    mean: float
    std: float
    median: float
    zeros: int
    negatives: int
    # String columns add:
    min_length: int
    max_length: int
    top_values: {value: count}
    # Datetime columns add:
    min_date: string
    max_date: string
    date_range_days: int
```

## Dependencies

```
pandas
```
