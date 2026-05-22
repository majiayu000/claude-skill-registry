---
name: pandas-coder
description: DataFrame manipulation with chunked processing, memory optimization, and vectorized operations.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Pandas-Coder

Expert in pandas DataFrame manipulation with focus on production-ready patterns for large datasets.

## Memory-Efficient Reading

```python
# Chunked CSV reading - default for files > 100MB
chunks = pd.read_csv('large.csv', chunksize=50_000)
for chunk in chunks:
    process(chunk)

# Read only needed columns
df = pd.read_csv('data.csv', usecols=['id', 'name', 'value'])

# Optimize dtypes on load
df = pd.read_csv('data.csv', dtype={
    'id': 'int32',           # not int64
    'category': 'category',  # not object
    'flag': 'bool'
})
```

## Category Type for Repeated Strings

```python
# BEFORE: 800MB with object dtype
df['status'] = df['status'].astype('category')  # AFTER: 50MB

# Set categories explicitly for consistency across files
df['status'] = pd.Categorical(
    df['status'],
    categories=['pending', 'active', 'completed', 'cancelled']
)
```

## Vectorized Operations Over Loops

```python
# BAD - iterating rows
for idx, row in df.iterrows():
    df.loc[idx, 'total'] = row['price'] * row['qty']

# GOOD - vectorized
df['total'] = df['price'] * df['qty']

# BAD - apply with Python function
df['clean'] = df['name'].apply(lambda x: x.strip().lower())

# GOOD - vectorized string methods
df['clean'] = df['name'].str.strip().str.lower()
```

## Conditional Assignment

```python
# Use np.where for simple conditions
df['tier'] = np.where(df['revenue'] > 1000, 'premium', 'standard')

# Use np.select for multiple conditions
conditions = [
    df['score'] >= 90,
    df['score'] >= 70,
    df['score'] >= 50
]
choices = ['A', 'B', 'C']
df['grade'] = np.select(conditions, choices, default='F')
```

## GroupBy Optimizations

```python
# Named aggregations (pandas 2.0+)
result = df.groupby('category').agg(
    total_sales=('sales', 'sum'),
    avg_price=('price', 'mean'),
    count=('id', 'count')
)

# Transform for broadcasting back to original shape
df['pct_of_group'] = df.groupby('category')['value'].transform(
    lambda x: x / x.sum()
)
```

## Index Operations

```python
# Set index for frequent lookups
df = df.set_index('user_id')
user_data = df.loc[12345]  # O(1) lookup

# Reset before groupby if index not needed
df.reset_index(drop=True, inplace=True)

# Multi-index for hierarchical data
df = df.set_index(['region', 'date'])
df.loc[('US', '2024-01')]  # Hierarchical access
```

## Memory Reduction Recipe

```python
def reduce_memory(df: pd.DataFrame) -> pd.DataFrame:
    """Reduce DataFrame memory by 50-90%."""
    for col in df.columns:
        col_type = df[col].dtype

        if col_type == 'object':
            if df[col].nunique() / len(df) < 0.5:
                df[col] = df[col].astype('category')

        elif col_type == 'int64':
            if df[col].min() >= 0:
                if df[col].max() < 255:
                    df[col] = df[col].astype('uint8')
                elif df[col].max() < 65535:
                    df[col] = df[col].astype('uint16')
            else:
                if df[col].min() > -128 and df[col].max() < 127:
                    df[col] = df[col].astype('int8')
                elif df[col].min() > -32768 and df[col].max() < 32767:
                    df[col] = df[col].astype('int16')

        elif col_type == 'float64':
            df[col] = df[col].astype('float32')

    return df
```

## Parquet Over CSV

```python
# Save with compression
df.to_parquet('data.parquet', compression='snappy', index=False)

# Read specific columns (predicate pushdown)
df = pd.read_parquet('data.parquet', columns=['id', 'value'])

# Partitioned writes for large datasets
df.to_parquet(
    'data/',
    partition_cols=['year', 'month'],
    compression='snappy'
)
```

## DateTime Handling

```python
# Parse dates efficiently
df['date'] = pd.to_datetime(df['date_str'], format='%Y-%m-%d')

# Extract components without apply
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['weekday'] = df['date'].dt.day_name()

# Date arithmetic
df['days_ago'] = (pd.Timestamp.now() - df['date']).dt.days
```

## Merge Optimization

```python
# Sort before merge for performance
left = left.sort_values('key')
right = right.sort_values('key')
result = pd.merge(left, right, on='key')

# Use categorical keys for memory efficiency
for df in [left, right]:
    df['key'] = df['key'].astype('category')
```

## Query vs Boolean Indexing

```python
# Boolean indexing - standard
filtered = df[(df['status'] == 'active') & (df['value'] > 100)]

# query() - more readable for complex conditions
filtered = df.query('status == "active" and value > 100')

# query() with variables
min_val = 100
filtered = df.query('value > @min_val')
```
