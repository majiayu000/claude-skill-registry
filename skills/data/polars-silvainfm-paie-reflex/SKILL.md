---
name: polars
description: Lightning-fast DataFrame library written in Rust for high-performance data manipulation and analysis. Use when user wants blazing fast data transformations, working with large datasets, lazy evaluation pipelines, or needs better performance than pandas. Ideal for ETL, data wrangling, aggregations, joins, and reading/writing CSV, Parquet, JSON files.
---

# Polars

## Overview

Polars is a blazingly fast DataFrame library written in Rust with Python bindings. Built for performance and memory efficiency, Polars leverages parallel execution and lazy evaluation to process data faster than pandas, especially on large datasets.

## When to Use This Skill

Activate when the user:
- Wants to work with DataFrames and needs high performance
- Mentions Polars explicitly or asks for "fast" data processing
- Needs to process large datasets (millions of rows)
- Wants lazy evaluation for query optimization
- Asks for data transformations, filtering, grouping, or aggregations
- Needs to read/write CSV, Parquet, JSON, or other data formats
- Wants to combine with DuckDB for SQL + DataFrame workflows

## Installation

Check if Polars is installed:

```bash
python3 -c "import polars as pl; print(pl.__version__)"
```

If not installed:

```bash
pip3 install polars
```

For full features including Parquet support:

```bash
pip3 install 'polars[pyarrow]'
```

For DuckDB integration:

```bash
pip3 install polars duckdb 'polars[pyarrow]'
```

## Core Capabilities

### 1. Reading Data

Polars can read data from various formats:

```python
import polars as pl

# Read CSV
df = pl.read_csv('data.csv')

# Read Parquet (fast, columnar format)
df = pl.read_parquet('data.parquet')

# Read JSON
df = pl.read_json('data.json')

# Read multiple files
df = pl.read_csv('data/*.csv')

# Read with lazy evaluation (doesn't load until needed)
lazy_df = pl.scan_csv('large_data.csv')
lazy_df = pl.scan_parquet('data/*.parquet')
```

### 2. Data Selection and Filtering

```python
import polars as pl

df = pl.read_csv('data.csv')

# Select columns
result = df.select(['name', 'age', 'city'])

# Select with expressions
result = df.select([
    pl.col('name'),
    pl.col('age'),
    pl.col('salary').alias('annual_salary')
])

# Filter rows
result = df.filter(pl.col('age') > 25)

# Multiple conditions
result = df.filter(
    (pl.col('age') > 25) &
    (pl.col('city') == 'NYC')
)

# Filter with string methods
result = df.filter(pl.col('name').str.contains('John'))
```

### 3. Transformations and New Columns

```python
import polars as pl

df = pl.read_csv('sales.csv')

# Add new columns
result = df.with_columns([
    (pl.col('quantity') * pl.col('price')).alias('total'),
    pl.col('product').str.to_uppercase().alias('product_upper'),
    pl.when(pl.col('quantity') > 10)
        .then(pl.lit('bulk'))
        .otherwise(pl.lit('retail'))
        .alias('sale_type')
])

# Modify existing columns
result = df.with_columns([
    pl.col('price').round(2),
    pl.col('date').str.strptime(pl.Date, '%Y-%m-%d')
])

# Rename columns
result = df.rename({'old_name': 'new_name'})
```

### 4. Aggregations and Grouping

```python
import polars as pl

df = pl.read_csv('sales.csv')

# Group by and aggregate
result = df.group_by('category').agg([
    pl.col('sales').sum().alias('total_sales'),
    pl.col('sales').mean().alias('avg_sales'),
    pl.col('sales').count().alias('num_sales'),
    pl.col('product').n_unique().alias('unique_products')
])

# Multiple group by columns
result = df.group_by(['category', 'region']).agg([
    pl.col('revenue').sum(),
    pl.col('customer_id').n_unique().alias('unique_customers')
])

# Aggregation without grouping
stats = df.select([
    pl.col('sales').sum(),
    pl.col('sales').mean(),
    pl.col('sales').median(),
    pl.col('sales').std(),
    pl.col('sales').min(),
    pl.col('sales').max()
])
```

### 5. Sorting and Ranking

```python
import polars as pl

df = pl.read_csv('data.csv')

# Sort by single column
result = df.sort('age')

# Sort descending
result = df.sort('salary', descending=True)

# Sort by multiple columns
result = df.sort(['department', 'salary'], descending=[False, True])

# Add rank column
result = df.with_columns([
    pl.col('salary').rank(method='dense').over('department').alias('dept_rank')
])
```

### 6. Joins

```python
import polars as pl

customers = pl.read_csv('customers.csv')
orders = pl.read_csv('orders.csv')

# Inner join
result = customers.join(orders, on='customer_id', how='inner')

# Left join
result = customers.join(orders, on='customer_id', how='left')

# Join on different column names
result = customers.join(
    orders,
    left_on='id',
    right_on='customer_id',
    how='inner'
)

# Join on multiple columns
result = df1.join(df2, on=['col1', 'col2'], how='inner')
```

### 7. Window Functions

```python
import polars as pl

df = pl.read_csv('sales.csv')

# Calculate running total
result = df.with_columns([
    pl.col('sales').cum_sum().over('region').alias('running_total')
])

# Calculate rolling average
result = df.with_columns([
    pl.col('sales').rolling_mean(window_size=7).alias('7_day_avg')
])

# Rank within groups
result = df.with_columns([
    pl.col('sales').rank().over('category').alias('category_rank')
])

# Lag and lead
result = df.with_columns([
    pl.col('sales').shift(1).over('product').alias('prev_sales'),
    pl.col('sales').shift(-1).over('product').alias('next_sales')
])
```

## Lazy Evaluation for Performance

Polars' lazy API optimizes queries before execution:

```python
import polars as pl

# Start with lazy scan (doesn't load data yet)
lazy_df = (
    pl.scan_csv('large_data.csv')
    .filter(pl.col('date') >= '2024-01-01')
    .select(['customer_id', 'product', 'sales', 'date'])
    .group_by('customer_id')
    .agg([
        pl.col('sales').sum().alias('total_sales'),
        pl.col('product').n_unique().alias('unique_products')
    ])
    .filter(pl.col('total_sales') > 1000)
    .sort('total_sales', descending=True)
)

# Execute the optimized query
result = lazy_df.collect()

# Or get execution plan
print(lazy_df.explain())
```

## Common Patterns

### Pattern 1: ETL Pipeline

```python
import polars as pl
from datetime import datetime

# Extract and Transform
result = (
    pl.scan_csv('raw_data.csv')
    # Clean data
    .filter(
        (pl.col('amount') > 0) &
        (pl.col('quantity') > 0)
    )
    # Transform columns
    .with_columns([
        pl.col('date').str.strptime(pl.Date, '%Y-%m-%d'),
        pl.col('product').str.strip().str.to_uppercase(),
        (pl.col('quantity') * pl.col('amount')).alias('total'),
        pl.when(pl.col('quantity') > 10)
            .then(pl.lit('bulk'))
            .otherwise(pl.lit('retail'))
            .alias('order_type')
    ])
    # Aggregate
    .group_by(['date', 'product', 'order_type'])
    .agg([
        pl.col('total').sum().alias('daily_total'),
        pl.col('quantity').sum().alias('daily_quantity'),
        pl.count().alias('num_orders')
    ])
    .collect()
)

# Load (save results)
result.write_parquet('processed_data.parquet')
```

### Pattern 2: Data Exploration

```python
import polars as pl

df = pl.read_csv('data.csv')

# Quick overview
print(df.head())
print(df.describe())
print(df.schema)

# Column statistics
print(df.select([
    pl.col('age').min(),
    pl.col('age').max(),
    pl.col('age').mean(),
    pl.col('age').median(),
    pl.col('age').std()
]))

# Count nulls
print(df.null_count())

# Value counts
print(df['category'].value_counts())

# Unique values
print(df['status'].n_unique())
```

### Pattern 3: Combining with DuckDB

Use Polars for data loading and DuckDB for SQL analytics:

```python
import polars as pl
import duckdb

# Load data with Polars
df = pl.read_parquet('data/*.parquet')

# Use DuckDB for complex SQL
result = duckdb.sql("""
    SELECT
        category,
        DATE_TRUNC('month', date) as month,
        SUM(revenue) as monthly_revenue,
        COUNT(DISTINCT customer_id) as unique_customers
    FROM df
    WHERE date >= '2024-01-01'
    GROUP BY category, month
    ORDER BY month DESC, monthly_revenue DESC
""").pl()  # Convert back to Polars DataFrame

# Continue with Polars
final = result.with_columns([
    (pl.col('monthly_revenue') / pl.col('unique_customers')).alias('revenue_per_customer')
])
```

### Pattern 4: Writing Data

```python
import polars as pl

df = pl.read_csv('data.csv')

# Write to CSV
df.write_csv('output.csv')

# Write to Parquet (recommended for large data)
df.write_parquet('output.parquet')

# Write to JSON
df.write_json('output.json')

# Write partitioned Parquet files
df.write_parquet('output/', partition_by='date')
```

## Expression Chaining

Polars uses a powerful expression syntax:

```python
import polars as pl

result = df.select([
    # String operations
    pl.col('name').str.to_lowercase().str.strip().alias('clean_name'),

    # Arithmetic
    (pl.col('price') * 1.1).round(2).alias('price_with_tax'),

    # Conditional logic
    pl.when(pl.col('age') < 18)
        .then(pl.lit('minor'))
        .when(pl.col('age') < 65)
        .then(pl.lit('adult'))
        .otherwise(pl.lit('senior'))
        .alias('age_group'),

    # Date operations
    pl.col('date').dt.year().alias('year'),
    pl.col('date').dt.month().alias('month'),

    # List operations
    pl.col('tags').list.len().alias('num_tags'),
])
```

## Performance Tips

1. **Use lazy evaluation** for large datasets - lets Polars optimize the query
2. **Use Parquet format** - columnar, compressed, much faster than CSV
3. **Filter early** - push filters before other operations
4. **Avoid row iteration** - use vectorized operations instead
5. **Use expressions** - more efficient than pandas-style operations

```python
# Good: Lazy + filter early
result = (
    pl.scan_parquet('large.parquet')
    .filter(pl.col('date') >= '2024-01-01')  # Filter first
    .select(['col1', 'col2', 'col3'])  # Then select
    .collect()
)

# Less efficient: Eager loading
df = pl.read_parquet('large.parquet')
result = df.filter(pl.col('date') >= '2024-01-01').select(['col1', 'col2', 'col3'])
```

## Polars vs Pandas

Key differences:
- **Immutability**: Polars DataFrames are immutable (operations return new DataFrames)
- **Performance**: Polars is typically 5-10x faster than pandas
- **Lazy evaluation**: Polars can optimize queries before execution
- **Expressions**: Polars uses expression API instead of method chaining
- **Parallel**: Polars automatically parallelizes operations

```python
# Pandas style
df['new_col'] = df['col1'] * df['col2']

# Polars style
df = df.with_columns([
    (pl.col('col1') * pl.col('col2')).alias('new_col')
])
```

## Integration with DuckDB

For the best of both worlds, combine Polars and DuckDB:

```python
import polars as pl
import duckdb

# Polars: Fast data loading and transformation
df = (
    pl.scan_parquet('data/*.parquet')
    .filter(pl.col('active') == True)
    .collect()
)

# DuckDB: SQL analytics
result = duckdb.sql("""
    SELECT
        category,
        SUM(amount) as total,
        AVG(amount) as average
    FROM df
    GROUP BY category
""").pl()
```

See the `duckdb` skill for more SQL capabilities and the references/api_reference.md file for detailed Polars API documentation.

## Error Handling

```python
import polars as pl

try:
    df = pl.read_csv('data.csv')
except FileNotFoundError:
    print("File not found")
except pl.exceptions.ComputeError as e:
    print(f"Polars compute error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Resources

- **references/api_reference.md**: Detailed Polars API documentation and examples
- Official docs: https://docs.pola.rs/
- API reference: https://docs.pola.rs/api/python/stable/reference/
