---
name: pandas-specialist
description: Master pandas data manipulation patterns including efficient data transformations, performance optimization, memory management, and vectorized operations. Use PROACTIVELY when working with pandas DataFrames for data analysis, cleaning, or transformation.
---

# Pandas Specialist

Master efficient data manipulation with pandas, focusing on performance, memory management, and avoiding common pitfalls.

## When to Use This Skill

- Data cleaning and preprocessing
- Exploratory data analysis (EDA)
- Data transformation and reshaping
- Large dataset processing
- Time series manipulation
- Data aggregation and grouping

## Quick Reference

```python
import pandas as pd
import numpy as np

# Always start with inspection
df.head(), df.info(), df.describe(), df.shape
df.memory_usage(deep=True)  # Check memory

# Key patterns
df.query("col > 5")                    # Fast filtering
df.assign(new_col=lambda x: x.a + 1)   # Method chaining
df.groupby("key").agg({"val": "sum"})  # Aggregation
df.pipe(my_function)                    # Pipeline
```

---

## Data Inspection

### Always Start with Understanding

```python
# ✅ First steps with any dataset
def inspect_dataframe(df: pd.DataFrame) -> None:
    """Comprehensive DataFrame inspection."""
    print(f"Shape: {df.shape}")
    print(f"\nData Types:\n{df.dtypes}")
    print(f"\nMemory Usage:\n{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"\nMissing Values:\n{df.isnull().sum()}")
    print(f"\nSample Data:\n{df.head()}")
    print(f"\nStatistics:\n{df.describe()}")

# Use profiling for comprehensive analysis
from ydata_profiling import ProfileReport
profile = ProfileReport(df, title="Data Report")
profile.to_file("report.html")
```

---

## Vectorized Operations

### Avoid Loops - Use Vectorization

```python
# ❌ SLOW: Using loops
result = []
for i in range(len(df)):
    result.append(df.iloc[i]['a'] * 2 + df.iloc[i]['b'])
df['result'] = result

# ❌ SLOW: Using iterrows
for index, row in df.iterrows():
    df.at[index, 'result'] = row['a'] * 2 + row['b']

# ❌ MEDIUM: Using apply (still slow for large data)
df['result'] = df.apply(lambda row: row['a'] * 2 + row['b'], axis=1)

# ✅ FAST: Vectorized operations
df['result'] = df['a'] * 2 + df['b']
```

### Conditional Logic

```python
# ❌ SLOW: apply with lambda
df['category'] = df['value'].apply(lambda x: 'high' if x > 100 else 'low')

# ✅ FAST: np.where for simple conditions
df['category'] = np.where(df['value'] > 100, 'high', 'low')

# ✅ FAST: np.select for multiple conditions
conditions = [
    df['value'] > 100,
    df['value'] > 50,
    df['value'] > 0
]
choices = ['high', 'medium', 'low']
df['category'] = np.select(conditions, choices, default='none')

# ✅ FAST: pd.cut for binning
df['category'] = pd.cut(
    df['value'],
    bins=[0, 50, 100, np.inf],
    labels=['low', 'medium', 'high']
)
```

### String Operations

```python
# ❌ SLOW: apply on strings
df['lower'] = df['name'].apply(lambda x: x.lower())

# ✅ FAST: Vectorized string methods
df['lower'] = df['name'].str.lower()
df['contains_a'] = df['name'].str.contains('a', na=False)
df['first_word'] = df['name'].str.split().str[0]
df['length'] = df['name'].str.len()
```

---

## Method Chaining

### Clean, Readable Pipelines

```python
# ❌ BAD: Intermediate variables (creates copies, hard to maintain)
df1 = df[df['status'] == 'active']
df2 = df1.dropna(subset=['value'])
df3 = df2.assign(value_normalized=df2['value'] / df2['value'].max())
df4 = df3.groupby('category').agg({'value_normalized': 'mean'})
result = df4.reset_index()

# ✅ GOOD: Method chaining (clean, efficient)
result = (
    df
    .query("status == 'active'")
    .dropna(subset=['value'])
    .assign(value_normalized=lambda x: x['value'] / x['value'].max())
    .groupby('category')
    .agg({'value_normalized': 'mean'})
    .reset_index()
)
```

### Using pipe() for Custom Functions

```python
def remove_outliers(df: pd.DataFrame, column: str, n_std: float = 3) -> pd.DataFrame:
    """Remove rows with outliers beyond n standard deviations."""
    mean = df[column].mean()
    std = df[column].std()
    return df[np.abs(df[column] - mean) <= n_std * std]

def add_log_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Add log-transformed column."""
    return df.assign(**{f"{column}_log": np.log1p(df[column])})

# Chain with pipe
result = (
    df
    .pipe(remove_outliers, 'value')
    .pipe(add_log_column, 'value')
    .query("value_log > 0")
)
```

---

## Efficient Filtering

### Boolean Indexing

```python
# ✅ FAST: Boolean indexing
active_users = df[df['status'] == 'active']
high_value = df[df['value'] > 1000]

# ✅ FAST: Multiple conditions with & and |
filtered = df[(df['status'] == 'active') & (df['value'] > 1000)]

# ✅ FAST: query() for readable complex filters
filtered = df.query("status == 'active' and value > 1000 and category in @categories")

# ✅ FAST: isin() for membership testing
categories = ['A', 'B', 'C']
filtered = df[df['category'].isin(categories)]

# ❌ SLOW: apply for filtering
filtered = df[df['category'].apply(lambda x: x in categories)]
```

### Filtering with loc and iloc

```python
# ✅ Use loc for label-based selection
df.loc[df['value'] > 100, 'category'] = 'high'

# ✅ Use iloc for position-based selection
first_10_rows = df.iloc[:10]
specific_columns = df.iloc[:, [0, 2, 4]]

# ✅ Combined selection
df.loc[df['status'] == 'active', ['name', 'value']]
```

---

## GroupBy Operations

### Efficient Aggregations

```python
# ✅ Basic groupby aggregation
summary = df.groupby('category')['value'].sum()

# ✅ Multiple aggregations per column
summary = df.groupby('category')['value'].agg(['sum', 'mean', 'count'])

# ✅ Different aggregations per column
summary = df.groupby('category').agg({
    'value': ['sum', 'mean'],
    'quantity': 'sum',
    'date': 'max'
})

# ✅ Named aggregations (cleaner output)
summary = df.groupby('category').agg(
    total_value=('value', 'sum'),
    avg_value=('value', 'mean'),
    count=('value', 'count')
)
```

### Transform and Apply

```python
# ✅ transform: returns same-shape as input
df['value_normalized'] = df.groupby('category')['value'].transform(
    lambda x: (x - x.mean()) / x.std()
)

# ✅ Group-wise operations
df['rank_in_group'] = df.groupby('category')['value'].rank(ascending=False)
df['pct_of_group'] = df.groupby('category')['value'].transform(
    lambda x: x / x.sum()
)

# ✅ Apply for complex group operations
def top_n(group, n=3):
    return group.nlargest(n, 'value')

top_per_category = df.groupby('category').apply(top_n, n=3)
```

---

## Memory Optimization

### Optimize Data Types

```python
# Check current memory usage
print(f"Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# ✅ Optimize numeric types
def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Reduce memory by downcasting dtypes."""
    df = df.copy()

    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')

    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')

    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:  # Low cardinality
            df[col] = df[col].astype('category')

    return df

df = optimize_dtypes(df)
print(f"Optimized: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
```

### Category Type for Low Cardinality

```python
# ❌ String columns use lots of memory
df['status'] = df['status'].astype('object')  # Each value stored separately

# ✅ Category type for repeated values
df['status'] = df['status'].astype('category')
df['country'] = df['country'].astype('category')

# Memory savings can be 50-90% for low cardinality columns
```

### Specify dtypes on Read

```python
# ✅ Define dtypes upfront (faster, less memory)
dtypes = {
    'id': 'int32',
    'value': 'float32',
    'name': 'string',
    'status': 'category',
    'count': 'int16'
}

df = pd.read_csv('data.csv', dtype=dtypes)
```

---

## Large Dataset Handling

### Chunked Reading

```python
# ✅ Process large files in chunks
chunk_size = 100_000
results = []

for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    # Process each chunk
    processed = (
        chunk
        .query("value > 0")
        .groupby('category')
        .agg({'value': 'sum'})
    )
    results.append(processed)

# Combine results
final = pd.concat(results).groupby(level=0).sum()
```

### Select Only Needed Columns

```python
# ❌ Load all columns
df = pd.read_csv('data.csv')  # Loads everything

# ✅ Load only needed columns
columns = ['id', 'name', 'value']
df = pd.read_csv('data.csv', usecols=columns)

# ✅ Filter while reading
df = pd.read_csv(
    'data.csv',
    usecols=columns,
    dtype={'id': 'int32', 'value': 'float32'},
    parse_dates=['date']
)
```

### Consider Alternatives for Very Large Data

```python
# For datasets larger than RAM
# Option 1: Dask for parallel processing
import dask.dataframe as dd
ddf = dd.read_csv('large_file.csv')
result = ddf.groupby('category')['value'].sum().compute()

# Option 2: Polars for faster processing
import polars as pl
df = pl.read_csv('large_file.csv')
result = df.group_by('category').agg(pl.col('value').sum())

# Option 3: SQLite for query-based analysis
import sqlite3
conn = sqlite3.connect(':memory:')
df.to_sql('data', conn, index=False)
result = pd.read_sql("SELECT category, SUM(value) FROM data GROUP BY category", conn)
```

---

## Date/Time Operations

### Efficient Datetime Handling

```python
# ✅ Parse dates on read
df = pd.read_csv('data.csv', parse_dates=['date'])

# ✅ Convert to datetime
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# ✅ Extract components efficiently
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek
df['is_weekend'] = df['date'].dt.dayofweek >= 5

# ✅ Date math
df['days_since'] = (pd.Timestamp.now() - df['date']).dt.days

# ✅ Resampling time series
daily = df.set_index('date').resample('D')['value'].sum()
monthly = df.set_index('date').resample('M')['value'].mean()
```

---

## Merging and Joining

### Efficient Joins

```python
# ✅ Merge with explicit keys
merged = pd.merge(df1, df2, on='id', how='left')

# ✅ Specify suffixes for overlapping columns
merged = pd.merge(
    df1, df2,
    on='id',
    how='left',
    suffixes=('_left', '_right')
)

# ✅ Join on index
df1.set_index('id').join(df2.set_index('id'), how='left')

# ✅ Merge indicator for debugging
merged = pd.merge(df1, df2, on='id', how='outer', indicator=True)
print(merged['_merge'].value_counts())
```

---

## Common Pitfalls

| Pitfall                 | Problem                | Solution                            |
| ----------------------- | ---------------------- | ----------------------------------- |
| `iterrows()`            | O(n) slow              | Vectorized operations               |
| `apply()` on large data | Slow                   | `np.where`, `np.select`, vectorized |
| Default dtypes          | Memory waste           | Specify `dtype`, use `category`     |
| Full file load          | Memory overflow        | `chunksize`, `usecols`              |
| Chain assignment        | SettingWithCopyWarning | Use `.loc[]` or `.assign()`         |
| Repeated computation    | Wasted time            | Cache intermediate results          |

## Performance Checklist

```markdown
## Pandas Performance Checklist

- [ ] Inspected data with info(), describe(), memory_usage()
- [ ] Optimized dtypes (downcast, category)
- [ ] Used vectorized operations (no loops)
- [ ] Method chaining (not intermediate variables)
- [ ] Filtered early (reduce data volume)
- [ ] Used query() for complex filters
- [ ] GroupBy with agg() not apply()
- [ ] Chunked reading for large files
- [ ] Only loaded needed columns
```

## Best Practices Summary

1. **Inspect First** - `info()`, `describe()`, `memory_usage()`
2. **Vectorize Everything** - No loops, no `iterrows`
3. **Chain Methods** - Clean, efficient pipelines
4. **Optimize Types** - `float32`, `int32`, `category`
5. **Filter Early** - Reduce data volume ASAP
6. **Use Built-ins** - `query()`, `isin()`, `groupby()`
7. **Chunk Large Files** - Don't load everything at once
8. **Consider Alternatives** - Polars, Dask for huge datasets


## Parent Hub
- [_data-ai-mastery](../_data-ai-mastery/SKILL.md)


## Part of Workflow
This skill is utilized in the following sequential workflows:
- [_workflow-data-pipeline](../_workflow-data-pipeline/SKILL.md)
