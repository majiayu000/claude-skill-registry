---
name: polars
version: 1.0.0
description: High-performance DataFrame library for fast data processing with lazy evaluation, parallel execution, and memory efficiency
author: workspace-hub
category: data-analysis
capabilities:
  - Lazy evaluation and query optimization
  - Parallel processing on all CPU cores
  - Memory-efficient operations for large datasets
  - Expression-based API for complex transformations
  - Streaming processing for out-of-memory datasets
  - Zero-copy data sharing with Arrow
tools:
  - polars
  - pyarrow
  - connectorx
tags: [polars, dataframe, performance, parallel, lazy-evaluation, arrow, rust, data-processing]
platforms: [python, rust]
related_skills:
  - pandas-data-processing
  - numpy-numerical-analysis
  - streamlit
  - dash
---

# Polars High-Performance DataFrame Skill

Master Polars for blazing-fast data processing with lazy evaluation, parallel execution, and memory-efficient operations on datasets of any size.

## When to Use This Skill

### USE Polars when:
- **Large datasets** - Working with data too large for pandas (10GB+)
- **Performance critical** - Need maximum speed for data transformations
- **Memory constrained** - Limited RAM requires efficient memory usage
- **Parallel processing** - Want to utilize all CPU cores automatically
- **Complex aggregations** - Group by, window functions, rolling calculations
- **Lazy evaluation** - Query optimization before execution matters
- **ETL pipelines** - Building production data pipelines
- **Streaming data** - Processing data larger than memory

### DON'T USE Polars when:
- **Pandas ecosystem required** - Need specific pandas-only libraries
- **Small datasets** - Under 100MB where pandas is sufficient
- **Legacy code** - Extensive existing pandas codebase
- **Matplotlib/Seaborn direct integration** - These work better with pandas
- **Time series with specialized needs** - Some pandas time series features are more mature

## Prerequisites

```bash
# Basic installation
pip install polars

# With all optional dependencies
pip install 'polars[all]'

# Specific extras
pip install 'polars[numpy,pandas,pyarrow,fsspec,connectorx,xlsx2csv,deltalake,timezone]'

# Using uv (recommended)
uv pip install polars pyarrow connectorx
```

## Core Capabilities

### 1. DataFrame Creation and I/O

**Creating DataFrames:**
```python
import polars as pl
import numpy as np
from datetime import datetime, date

# From Python dictionaries
df = pl.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "value": [100.5, 200.3, 150.7, 300.2, 250.8],
    "category": ["A", "B", "A", "C", "B"],
    "timestamp": [
        datetime(2025, 1, 1, 10, 0),
        datetime(2025, 1, 2, 11, 30),
        datetime(2025, 1, 3, 9, 15),
        datetime(2025, 1, 4, 14, 45),
        datetime(2025, 1, 5, 16, 0),
    ]
})

print(df)
print(f"Shape: {df.shape}")
print(f"Schema: {df.schema}")

# From NumPy arrays
np_data = np.random.randn(1000, 5)
df_numpy = pl.DataFrame(
    np_data,
    schema=["col_a", "col_b", "col_c", "col_d", "col_e"]
)

# From list of dictionaries
records = [
    {"x": 1, "y": "a"},
    {"x": 2, "y": "b"},
    {"x": 3, "y": "c"}
]
df_records = pl.DataFrame(records)

# Specify schema explicitly
df_typed = pl.DataFrame(
    {
        "integers": [1, 2, 3],
        "floats": [1.0, 2.0, 3.0],
        "strings": ["a", "b", "c"]
    },
    schema={
        "integers": pl.Int32,
        "floats": pl.Float64,
        "strings": pl.Utf8
    }
)
```

**Reading Files:**
```python
# CSV files
df = pl.read_csv("data.csv")

# With options
df = pl.read_csv(
    "data.csv",
    separator=",",
    has_header=True,
    skip_rows=0,
    n_rows=10000,  # Read only first N rows
    columns=["col1", "col2", "col3"],  # Select columns
    dtypes={"id": pl.Int64, "value": pl.Float32},  # Specify types
    null_values=["NA", "N/A", ""],
    ignore_errors=True,
    try_parse_dates=True,
    encoding="utf8"
)

# Parquet files (recommended for large data)
df = pl.read_parquet("data.parquet")

# Multiple Parquet files with globbing
df = pl.read_parquet("data/*.parquet")

# Parquet with row group filtering
df = pl.read_parquet(
    "large_data.parquet",
    columns=["id", "value", "date"],
    n_rows=100000,
    row_count_name="row_nr"
)

# JSON files
df = pl.read_json("data.json")

# JSON Lines (newline-delimited JSON)
df = pl.read_ndjson("data.jsonl")

# Excel files
df = pl.read_excel("data.xlsx", sheet_name="Sheet1")

# Delta Lake
df = pl.read_delta("delta_table/")

# From SQL database using ConnectorX (fast!)
df = pl.read_database(
    query="SELECT * FROM sales WHERE date > '2025-01-01'",
    connection="postgresql://user:pass@localhost/db"
)

# From URL
df = pl.read_csv("https://example.com/data.csv")
```

**Writing Files:**
```python
# CSV
df.write_csv("output.csv")

# Parquet (recommended)
df.write_parquet(
    "output.parquet",
    compression="zstd",  # zstd, lz4, snappy, gzip, brotli
    compression_level=3,
    statistics=True,
    row_group_size=100000
)

# JSON
df.write_json("output.json", row_oriented=True)
df.write_ndjson("output.jsonl")

# Delta Lake
df.write_delta("delta_table/", mode="overwrite")

# IPC/Arrow format (fastest for inter-process communication)
df.write_ipc("output.arrow")
```

### 2. Lazy Evaluation and Query Optimization

**LazyFrame Basics:**
```python
import polars as pl

# Create lazy frame (no computation yet)
lf = pl.scan_csv("large_data.csv")

# Or convert from eager DataFrame
df = pl.DataFrame({"x": [1, 2, 3]})
lf = df.lazy()

# Chain operations (still no computation)
result_lf = (
    lf
    .filter(pl.col("date") >= "2025-01-01")
    .with_columns([
        (pl.col("revenue") - pl.col("cost")).alias("profit"),
        pl.col("category").cast(pl.Categorical)
    ])
    .group_by("category")
    .agg([
        pl.col("profit").sum().alias("total_profit"),
        pl.col("profit").mean().alias("avg_profit"),
        pl.count().alias("count")
    ])
    .sort("total_profit", descending=True)
)

# View the query plan
print(result_lf.explain())

# Execute and collect results
result_df = result_lf.collect()

# Execute with streaming (for very large data)
result_df = result_lf.collect(streaming=True)

# Fetch only first N rows
sample = result_lf.fetch(1000)
```

**Query Optimization Benefits:**
```python
# Polars optimizes this automatically:
lf = (
    pl.scan_parquet("data/*.parquet")
    .filter(pl.col("country") == "USA")  # Predicate pushdown
    .select(["id", "name", "revenue"])   # Projection pushdown
    .filter(pl.col("revenue") > 1000)    # Combined with first filter
)

# View optimized plan
print("Naive plan:")
print(lf.explain(optimized=False))

print("\nOptimized plan:")
print(lf.explain(optimized=True))

# The optimizer will:
# 1. Push filters to data source (read less data)
# 2. Select only needed columns (reduce memory)
# 3. Combine/reorder operations for efficiency
# 4. Eliminate redundant operations
```

**Streaming Large Files:**
```python
# Process files larger than memory
def process_large_file(input_path: str, output_path: str):
    """Process file that doesn't fit in memory."""
    result = (
        pl.scan_csv(input_path)
        .filter(pl.col("status") == "active")
        .group_by("region")
        .agg([
            pl.col("sales").sum(),
            pl.col("customers").n_unique()
        ])
        .collect(streaming=True)  # Stream processing
    )

    result.write_parquet(output_path)
    return result

# Sink directly to file (even more memory efficient)
(
    pl.scan_csv("huge_file.csv")
    .filter(pl.col("value") > 0)
    .sink_parquet("filtered_output.parquet")
)
```

### 3. Expression API

**Basic Expressions:**
```python
import polars as pl

df = pl.DataFrame({
    "a": [1, 2, 3, 4, 5],
    "b": [10, 20, 30, 40, 50],
    "c": ["x", "y", "x", "y", "x"],
    "d": [1.5, 2.5, 3.5, 4.5, 5.5]
})

# Column selection
df.select(pl.col("a"))
df.select(pl.col("a", "b", "c"))
df.select(pl.col("^a.*$"))  # Regex pattern
df.select(pl.all())
df.select(pl.exclude("c"))

# Arithmetic operations
df.select([
    pl.col("a"),
    (pl.col("a") + pl.col("b")).alias("sum"),
    (pl.col("a") * pl.col("d")).alias("product"),
    (pl.col("b") / pl.col("a")).alias("ratio"),
    (pl.col("a") ** 2).alias("squared"),
    (pl.col("a") % 2).alias("modulo")
])

# Conditional expressions
df.select([
    pl.col("a"),
    pl.when(pl.col("a") > 3)
      .then(pl.lit("high"))
      .otherwise(pl.lit("low"))
      .alias("category"),

    pl.when(pl.col("a") < 2)
      .then(pl.lit("low"))
      .when(pl.col("a") < 4)
      .then(pl.lit("medium"))
      .otherwise(pl.lit("high"))
      .alias("tier")
])

# String operations
df_str = pl.DataFrame({
    "text": ["Hello World", "Polars is Fast", "Data Analysis"]
})

df_str.select([
    pl.col("text"),
    pl.col("text").str.to_lowercase().alias("lower"),
    pl.col("text").str.to_uppercase().alias("upper"),
    pl.col("text").str.len_chars().alias("length"),
    pl.col("text").str.split(" ").alias("words"),
    pl.col("text").str.contains("a").alias("has_a"),
    pl.col("text").str.replace("a", "X").alias("replaced")
])
```

**Advanced Expressions:**
```python
# List operations
df_list = pl.DataFrame({
    "values": [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
})

df_list.select([
    pl.col("values"),
    pl.col("values").list.len().alias("count"),
    pl.col("values").list.sum().alias("sum"),
    pl.col("values").list.mean().alias("mean"),
    pl.col("values").list.first().alias("first"),
    pl.col("values").list.last().alias("last"),
    pl.col("values").list.get(0).alias("index_0"),
    pl.col("values").list.contains(5).alias("has_5")
])

# Struct operations
df_struct = pl.DataFrame({
    "point": [{"x": 1, "y": 2}, {"x": 3, "y": 4}]
})

df_struct.select([
    pl.col("point"),
    pl.col("point").struct.field("x").alias("x"),
    pl.col("point").struct.field("y").alias("y")
])

# Date/time operations
df_dt = pl.DataFrame({
    "timestamp": pl.date_range(
        datetime(2025, 1, 1),
        datetime(2025, 12, 31),
        "1d",
        eager=True
    )
})

df_dt.select([
    pl.col("timestamp"),
    pl.col("timestamp").dt.year().alias("year"),
    pl.col("timestamp").dt.month().alias("month"),
    pl.col("timestamp").dt.day().alias("day"),
    pl.col("timestamp").dt.weekday().alias("weekday"),
    pl.col("timestamp").dt.week().alias("week"),
    pl.col("timestamp").dt.quarter().alias("quarter"),
    pl.col("timestamp").dt.strftime("%Y-%m-%d").alias("formatted")
])
```

### 4. GroupBy and Aggregations

**Basic GroupBy:**
```python
import polars as pl

df = pl.DataFrame({
    "category": ["A", "B", "A", "B", "A", "C"],
    "subcategory": ["x", "y", "x", "y", "z", "x"],
    "value": [100, 200, 150, 250, 175, 300],
    "quantity": [10, 20, 15, 25, 12, 30]
})

# Simple aggregation
result = df.group_by("category").agg([
    pl.col("value").sum().alias("total_value"),
    pl.col("value").mean().alias("avg_value"),
    pl.col("value").min().alias("min_value"),
    pl.col("value").max().alias("max_value"),
    pl.col("value").std().alias("std_value"),
    pl.col("quantity").sum().alias("total_quantity"),
    pl.count().alias("count")
])

print(result)

# Multiple group keys
result = df.group_by(["category", "subcategory"]).agg([
    pl.col("value").sum(),
    pl.count()
])

# Maintain order
result = df.group_by("category", maintain_order=True).agg(
    pl.col("value").sum()
)

# Dynamic aggregations
agg_exprs = [
    pl.col(c).mean().alias(f"{c}_mean")
    for c in ["value", "quantity"]
]
result = df.group_by("category").agg(agg_exprs)
```

**Advanced Aggregations:**
```python
# Multiple aggregations on same column
result = df.group_by("category").agg([
    pl.col("value").sum().alias("sum"),
    pl.col("value").mean().alias("mean"),
    pl.col("value").median().alias("median"),
    pl.col("value").quantile(0.25).alias("q25"),
    pl.col("value").quantile(0.75).alias("q75"),
    pl.col("value").var().alias("variance"),
    pl.col("value").skew().alias("skewness")
])

# Conditional aggregations
result = df.group_by("category").agg([
    pl.col("value").filter(pl.col("quantity") > 15).sum().alias("high_qty_value"),
    pl.col("value").filter(pl.col("quantity") <= 15).sum().alias("low_qty_value")
])

# First/last values
result = df.group_by("category").agg([
    pl.col("value").first().alias("first_value"),
    pl.col("value").last().alias("last_value"),
    pl.col("value").head(3).alias("top_3"),
    pl.col("value").tail(2).alias("bottom_2")
])

# Unique values
result = df.group_by("category").agg([
    pl.col("subcategory").n_unique().alias("unique_subcats"),
    pl.col("subcategory").unique().alias("subcategories")
])

# Custom aggregation with map_elements
result = df.group_by("category").agg([
    pl.col("value").map_elements(
        lambda s: s.to_numpy().std(ddof=1),
        return_dtype=pl.Float64
    ).alias("custom_std")
])
```

### 5. Window Functions

**Basic Window Functions:**
```python
import polars as pl

df = pl.DataFrame({
    "date": pl.date_range(date(2025, 1, 1), date(2025, 1, 10), eager=True),
    "category": ["A", "B"] * 5,
    "value": [100, 110, 105, 115, 108, 120, 112, 125, 118, 130]
})

# Row number within groups
df.with_columns([
    pl.col("value").rank().over("category").alias("rank"),
    pl.col("value").rank(descending=True).over("category").alias("rank_desc")
])

# Running calculations
df.with_columns([
    pl.col("value").cum_sum().over("category").alias("cumsum"),
    pl.col("value").cum_max().over("category").alias("cummax"),
    pl.col("value").cum_min().over("category").alias("cummin"),
    pl.col("value").cum_count().over("category").alias("cumcount")
])

# Lag and lead
df.with_columns([
    pl.col("value").shift(1).over("category").alias("lag_1"),
    pl.col("value").shift(-1).over("category").alias("lead_1"),
    pl.col("value").shift(2).over("category").alias("lag_2"),
    (pl.col("value") - pl.col("value").shift(1).over("category")).alias("diff")
])

# Percentage change
df.with_columns([
    pl.col("value").pct_change().over("category").alias("pct_change")
])
```

**Rolling Windows:**
```python
# Rolling calculations
df.with_columns([
    pl.col("value").rolling_mean(window_size=3).over("category").alias("rolling_mean_3"),
    pl.col("value").rolling_sum(window_size=3).over("category").alias("rolling_sum_3"),
    pl.col("value").rolling_std(window_size=3).over("category").alias("rolling_std_3"),
    pl.col("value").rolling_min(window_size=3).over("category").alias("rolling_min_3"),
    pl.col("value").rolling_max(window_size=3).over("category").alias("rolling_max_3")
])

# Time-based rolling windows
df_ts = pl.DataFrame({
    "timestamp": pl.datetime_range(
        datetime(2025, 1, 1),
        datetime(2025, 1, 10),
        "1h",
        eager=True
    ),
    "value": range(217)
})

df_ts.with_columns([
    pl.col("value").rolling_mean_by(
        by="timestamp",
        window_size="6h"
    ).alias("rolling_mean_6h"),

    pl.col("value").rolling_sum_by(
        by="timestamp",
        window_size="1d"
    ).alias("rolling_sum_1d")
])

# Exponential weighted functions
df.with_columns([
    pl.col("value").ewm_mean(span=3).alias("ewm_mean"),
    pl.col("value").ewm_std(span=3).alias("ewm_std")
])
```

### 6. Joins and Concatenation

**Join Operations:**
```python
import polars as pl

# Sample data
orders = pl.DataFrame({
    "order_id": [1, 2, 3, 4, 5],
    "customer_id": [101, 102, 101, 103, 104],
    "amount": [250.0, 150.0, 300.0, 200.0, 175.0]
})

customers = pl.DataFrame({
    "customer_id": [101, 102, 103, 105],
    "name": ["Alice", "Bob", "Charlie", "Diana"],
    "region": ["East", "West", "East", "North"]
})

# Inner join (default)
result = orders.join(customers, on="customer_id", how="inner")

# Left join
result = orders.join(customers, on="customer_id", how="left")

# Right join
result = orders.join(customers, on="customer_id", how="right")

# Outer/full join
result = orders.join(customers, on="customer_id", how="full")

# Cross join (cartesian product)
result = orders.join(customers, how="cross")

# Semi join (filter left by right)
result = orders.join(customers, on="customer_id", how="semi")

# Anti join (filter left NOT in right)
result = orders.join(customers, on="customer_id", how="anti")

# Join on multiple columns
df1 = pl.DataFrame({"a": [1, 2], "b": ["x", "y"], "val1": [10, 20]})
df2 = pl.DataFrame({"a": [1, 2], "b": ["x", "z"], "val2": [100, 200]})
result = df1.join(df2, on=["a", "b"], how="inner")

# Join with different column names
result = orders.join(
    customers.rename({"customer_id": "cust_id"}),
    left_on="customer_id",
    right_on="cust_id"
)

# Join with suffix for duplicate columns
df1 = pl.DataFrame({"id": [1, 2], "value": [10, 20]})
df2 = pl.DataFrame({"id": [1, 2], "value": [100, 200]})
result = df1.join(df2, on="id", suffix="_right")
```

**Concatenation:**
```python
# Vertical concatenation (stack rows)
df1 = pl.DataFrame({"a": [1, 2], "b": [3, 4]})
df2 = pl.DataFrame({"a": [5, 6], "b": [7, 8]})
df3 = pl.DataFrame({"a": [9, 10], "b": [11, 12]})

combined = pl.concat([df1, df2, df3])

# Horizontal concatenation (stack columns)
df1 = pl.DataFrame({"a": [1, 2, 3]})
df2 = pl.DataFrame({"b": [4, 5, 6]})
combined = pl.concat([df1, df2], how="horizontal")

# Diagonal concatenation (union with different schemas)
df1 = pl.DataFrame({"a": [1, 2], "b": [3, 4]})
df2 = pl.DataFrame({"b": [5, 6], "c": [7, 8]})
combined = pl.concat([df1, df2], how="diagonal")

# Align schemas before concat
df1 = pl.DataFrame({"a": [1, 2], "b": [3, 4]})
df2 = pl.DataFrame({"a": [5, 6], "c": [7, 8]})
combined = pl.concat([df1, df2], how="diagonal_relaxed")
```

**Asof Joins (Time-based):**
```python
# For joining on nearest timestamp
trades = pl.DataFrame({
    "time": pl.datetime_range(datetime(2025, 1, 1, 9, 0), datetime(2025, 1, 1, 9, 10), "1m", eager=True),
    "price": [100.0, 101.0, 100.5, 102.0, 101.5, 103.0, 102.5, 104.0, 103.5, 105.0, 104.5]
})

quotes = pl.DataFrame({
    "time": pl.datetime_range(datetime(2025, 1, 1, 9, 0), datetime(2025, 1, 1, 9, 10), "2m", eager=True),
    "bid": [99.5, 100.5, 101.5, 102.5, 103.5, 104.5]
})

# Join each trade with the most recent quote
result = trades.join_asof(
    quotes,
    on="time",
    strategy="backward"  # Use most recent quote
)
```

## Complete Examples

### Example 1: ETL Pipeline for Sales Data

```python
import polars as pl
from pathlib import Path
from datetime import datetime

def etl_sales_pipeline(
    input_dir: Path,
    output_dir: Path,
    min_date: str = "2025-01-01"
) -> dict:
    """
    Complete ETL pipeline for sales data processing.

    Demonstrates: lazy evaluation, joins, aggregations, window functions.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load data lazily
    sales = pl.scan_parquet(input_dir / "sales/*.parquet")
    products = pl.scan_parquet(input_dir / "products.parquet")
    customers = pl.scan_parquet(input_dir / "customers.parquet")

    # 2. Clean and transform sales data
    sales_clean = (
        sales
        .filter(
            (pl.col("date") >= min_date) &
            (pl.col("quantity") > 0) &
            (pl.col("unit_price") > 0)
        )
        .with_columns([
            (pl.col("quantity") * pl.col("unit_price")).alias("revenue"),
            pl.col("date").str.strptime(pl.Date, "%Y-%m-%d").alias("date_parsed")
        ])
        .with_columns([
            pl.col("date_parsed").dt.year().alias("year"),
            pl.col("date_parsed").dt.month().alias("month"),
            pl.col("date_parsed").dt.weekday().alias("weekday")
        ])
    )

    # 3. Enrich with product and customer data
    enriched = (
        sales_clean
        .join(products, on="product_id", how="left")
        .join(customers, on="customer_id", how="left")
    )

    # 4. Calculate metrics with window functions
    with_metrics = (
        enriched
        .with_columns([
            # Running total by customer
            pl.col("revenue")
              .cum_sum()
              .over(["customer_id"])
              .alias("customer_cumulative_revenue"),

            # Rank products by revenue within category
            pl.col("revenue")
              .rank(descending=True)
              .over(["category", "month"])
              .alias("category_month_rank"),

            # 7-day rolling average
            pl.col("revenue")
              .rolling_mean(window_size=7)
              .over(["product_id"])
              .alias("rolling_7d_avg")
        ])
    )

    # 5. Generate aggregated summaries
    daily_summary = (
        with_metrics
        .group_by(["date_parsed", "category"])
        .agg([
            pl.col("revenue").sum().alias("total_revenue"),
            pl.col("quantity").sum().alias("total_quantity"),
            pl.col("order_id").n_unique().alias("order_count"),
            pl.col("customer_id").n_unique().alias("unique_customers"),
            pl.col("revenue").mean().alias("avg_order_value")
        ])
        .sort(["date_parsed", "category"])
    )

    monthly_summary = (
        with_metrics
        .group_by(["year", "month", "category"])
        .agg([
            pl.col("revenue").sum().alias("total_revenue"),
            pl.col("revenue").mean().alias("avg_revenue"),
            pl.col("revenue").std().alias("std_revenue"),
            pl.count().alias("transaction_count")
        ])
        .sort(["year", "month", "category"])
    )

    customer_summary = (
        with_metrics
        .group_by("customer_id")
        .agg([
            pl.col("revenue").sum().alias("lifetime_value"),
            pl.col("order_id").n_unique().alias("order_count"),
            pl.col("date_parsed").min().alias("first_purchase"),
            pl.col("date_parsed").max().alias("last_purchase"),
            pl.col("category").n_unique().alias("categories_purchased")
        ])
        .with_columns([
            (pl.col("last_purchase") - pl.col("first_purchase"))
              .dt.total_days()
              .alias("customer_tenure_days"),
            (pl.col("lifetime_value") / pl.col("order_count"))
              .alias("avg_order_value")
        ])
        .sort("lifetime_value", descending=True)
    )

    # 6. Execute and save results
    results = {
        "daily": daily_summary.collect(),
        "monthly": monthly_summary.collect(),
        "customer": customer_summary.collect(),
        "detailed": with_metrics.collect(streaming=True)
    }

    # Save outputs
    results["daily"].write_parquet(output_dir / "daily_summary.parquet")
    results["monthly"].write_parquet(output_dir / "monthly_summary.parquet")
    results["customer"].write_parquet(output_dir / "customer_summary.parquet")
    results["detailed"].write_parquet(
        output_dir / "detailed_sales.parquet",
        compression="zstd"
    )

    # Return summary stats
    return {
        "total_revenue": results["daily"]["total_revenue"].sum(),
        "total_orders": results["daily"]["order_count"].sum(),
        "unique_customers": results["customer"].height,
        "date_range": f"{results['daily']['date_parsed'].min()} to {results['daily']['date_parsed'].max()}"
    }

# Usage
summary = etl_sales_pipeline(
    input_dir=Path("data/raw"),
    output_dir=Path("data/processed"),
    min_date="2025-01-01"
)
print(f"Pipeline complete: {summary}")
```

### Example 2: Time Series Analysis

```python
import polars as pl
import numpy as np
from datetime import datetime, timedelta

def analyze_time_series(
    df: pl.DataFrame,
    value_column: str,
    time_column: str,
    group_column: str = None
) -> dict:
    """
    Comprehensive time series analysis with Polars.

    Returns statistics, trends, seasonality indicators.
    """
    # Ensure proper types
    df = df.with_columns([
        pl.col(time_column).cast(pl.Datetime).alias(time_column)
    ])

    # Add time components
    df = df.with_columns([
        pl.col(time_column).dt.year().alias("year"),
        pl.col(time_column).dt.month().alias("month"),
        pl.col(time_column).dt.day().alias("day"),
        pl.col(time_column).dt.weekday().alias("weekday"),
        pl.col(time_column).dt.hour().alias("hour"),
        pl.col(time_column).dt.week().alias("week_of_year")
    ])

    # Overall statistics
    stats = df.select([
        pl.col(value_column).mean().alias("mean"),
        pl.col(value_column).std().alias("std"),
        pl.col(value_column).min().alias("min"),
        pl.col(value_column).max().alias("max"),
        pl.col(value_column).median().alias("median"),
        pl.col(value_column).quantile(0.25).alias("q25"),
        pl.col(value_column).quantile(0.75).alias("q75"),
        pl.col(value_column).skew().alias("skewness"),
        pl.col(value_column).kurtosis().alias("kurtosis")
    ]).to_dicts()[0]

    # Trend analysis
    df_trend = df.with_columns([
        # Moving averages
        pl.col(value_column).rolling_mean(window_size=7).alias("ma_7"),
        pl.col(value_column).rolling_mean(window_size=30).alias("ma_30"),
        pl.col(value_column).rolling_mean(window_size=90).alias("ma_90"),

        # Exponential moving averages
        pl.col(value_column).ewm_mean(span=7).alias("ema_7"),
        pl.col(value_column).ewm_mean(span=30).alias("ema_30"),

        # Percent change
        pl.col(value_column).pct_change().alias("pct_change_1"),
        pl.col(value_column).pct_change(n=7).alias("pct_change_7"),

        # Difference
        (pl.col(value_column) - pl.col(value_column).shift(1)).alias("diff_1"),

        # Z-score (standardized)
        ((pl.col(value_column) - pl.col(value_column).mean()) /
         pl.col(value_column).std()).alias("z_score")
    ])

    # Seasonality patterns
    monthly_pattern = (
        df
        .group_by("month")
        .agg([
            pl.col(value_column).mean().alias("avg"),
            pl.col(value_column).std().alias("std"),
            pl.count().alias("count")
        ])
        .sort("month")
    )

    weekday_pattern = (
        df
        .group_by("weekday")
        .agg([
            pl.col(value_column).mean().alias("avg"),
            pl.col(value_column).std().alias("std"),
            pl.count().alias("count")
        ])
        .sort("weekday")
    )

    hourly_pattern = (
        df
        .group_by("hour")
        .agg([
            pl.col(value_column).mean().alias("avg"),
            pl.col(value_column).std().alias("std"),
            pl.count().alias("count")
        ])
        .sort("hour")
    )

    # Detect anomalies (beyond 3 standard deviations)
    mean_val = df[value_column].mean()
    std_val = df[value_column].std()

    anomalies = df.filter(
        (pl.col(value_column) > mean_val + 3 * std_val) |
        (pl.col(value_column) < mean_val - 3 * std_val)
    )

    return {
        "statistics": stats,
        "trend_data": df_trend,
        "monthly_pattern": monthly_pattern,
        "weekday_pattern": weekday_pattern,
        "hourly_pattern": hourly_pattern,
        "anomalies": anomalies,
        "anomaly_count": anomalies.height
    }

# Generate sample data
np.random.seed(42)
n_points = 10000
base = np.sin(np.linspace(0, 20 * np.pi, n_points)) * 100  # Seasonality
trend = np.linspace(0, 50, n_points)  # Trend
noise = np.random.randn(n_points) * 10  # Noise

sample_df = pl.DataFrame({
    "timestamp": pl.datetime_range(
        datetime(2024, 1, 1),
        datetime(2024, 1, 1) + timedelta(hours=n_points),
        "1h",
        eager=True
    )[:n_points],
    "value": base + trend + noise
})

# Run analysis
results = analyze_time_series(
    sample_df,
    value_column="value",
    time_column="timestamp"
)

print("Statistics:", results["statistics"])
print(f"Anomalies detected: {results['anomaly_count']}")
print("\nMonthly pattern:")
print(results["monthly_pattern"])
```

### Example 3: Large-Scale Data Processing with Streaming

```python
import polars as pl
from pathlib import Path
import time

def process_large_dataset(
    input_pattern: str,
    output_path: str,
    chunk_report_every: int = 1_000_000
) -> dict:
    """
    Process very large datasets using streaming.

    This approach handles datasets larger than available RAM.
    """
    start_time = time.time()

    # Create lazy frame from multiple files
    lf = pl.scan_parquet(input_pattern)

    # Define transformations
    processed = (
        lf
        # Filter early to reduce data
        .filter(
            (pl.col("status") == "completed") &
            (pl.col("amount") > 0)
        )

        # Calculate derived columns
        .with_columns([
            (pl.col("amount") * pl.col("quantity")).alias("total"),
            pl.col("timestamp").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S"),
            pl.col("category").cast(pl.Categorical)
        ])

        # Extract date parts
        .with_columns([
            pl.col("timestamp").dt.date().alias("date"),
            pl.col("timestamp").dt.hour().alias("hour")
        ])

        # Aggregate
        .group_by(["date", "category"])
        .agg([
            pl.col("total").sum().alias("daily_total"),
            pl.col("total").mean().alias("daily_avg"),
            pl.col("total").count().alias("transaction_count"),
            pl.col("user_id").n_unique().alias("unique_users")
        ])

        # Sort for output
        .sort(["date", "category"])
    )

    # Show query plan
    print("Query plan:")
    print(processed.explain())

    # Execute with streaming
    result = processed.collect(streaming=True)

    # Save result
    result.write_parquet(
        output_path,
        compression="zstd",
        compression_level=3
    )

    elapsed = time.time() - start_time

    return {
        "rows_output": result.height,
        "columns": result.columns,
        "elapsed_seconds": elapsed,
        "output_path": output_path
    }

# Alternative: Sink directly to file (even more memory efficient)
def sink_large_dataset(input_pattern: str, output_path: str):
    """
    Process and write directly to file without collecting in memory.
    """
    (
        pl.scan_parquet(input_pattern)
        .filter(pl.col("status") == "completed")
        .with_columns([
            (pl.col("amount") * pl.col("quantity")).alias("total")
        ])
        .group_by("category")
        .agg([
            pl.col("total").sum(),
            pl.count()
        ])
        .sink_parquet(output_path)
    )

    print(f"Results written to {output_path}")
```

## Integration Examples

### Polars with Plotly Visualization

```python
import polars as pl
import plotly.express as px
import plotly.graph_objects as go

def create_dashboard_data(df: pl.DataFrame) -> dict:
    """Prepare data for Plotly dashboard."""

    # Time series for line chart
    daily_trend = (
        df
        .group_by("date")
        .agg([
            pl.col("revenue").sum().alias("revenue"),
            pl.col("orders").sum().alias("orders")
        ])
        .sort("date")
        .to_pandas()  # Convert for Plotly
    )

    # Category breakdown for pie chart
    category_breakdown = (
        df
        .group_by("category")
        .agg(pl.col("revenue").sum())
        .sort("revenue", descending=True)
        .to_pandas()
    )

    # Regional comparison for bar chart
    regional = (
        df
        .group_by("region")
        .agg([
            pl.col("revenue").sum(),
            pl.col("orders").count()
        ])
        .to_pandas()
    )

    return {
        "daily_trend": daily_trend,
        "category_breakdown": category_breakdown,
        "regional": regional
    }

def plot_time_series(df_pandas, x_col, y_col, title):
    """Create interactive time series plot."""
    fig = px.line(
        df_pandas,
        x=x_col,
        y=y_col,
        title=title
    )
    fig.update_layout(hovermode="x unified")
    return fig
```

### Polars with Pandas Interop

```python
import polars as pl
import pandas as pd

# Convert Polars to Pandas (when needed for libraries that require pandas)
polars_df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
pandas_df = polars_df.to_pandas()

# Convert Pandas to Polars
pandas_df = pd.DataFrame({"x": [1, 2, 3], "y": ["a", "b", "c"]})
polars_df = pl.from_pandas(pandas_df)

# Efficient conversion with zero-copy when possible
polars_df = pl.from_pandas(pandas_df, nan_to_null=True)

# Use Polars for heavy lifting, Pandas for compatibility
def hybrid_pipeline(input_path: str):
    """Use Polars for processing, Pandas for visualization libraries."""

    # Heavy processing with Polars
    processed = (
        pl.scan_parquet(input_path)
        .filter(pl.col("value") > 0)
        .group_by("category")
        .agg([
            pl.col("value").sum(),
            pl.col("value").mean().alias("avg_value")
        ])
        .collect()
    )

    # Convert for seaborn/matplotlib
    import seaborn as sns
    pandas_df = processed.to_pandas()
    sns.barplot(data=pandas_df, x="category", y="value")

    return processed
```

## Best Practices

### 1. Use Lazy Evaluation by Default

```python
# GOOD: Lazy evaluation allows optimization
lf = pl.scan_parquet("data.parquet")
result = (
    lf
    .filter(pl.col("x") > 0)
    .select(["x", "y"])
    .collect()
)

# AVOID: Eager evaluation for large files
df = pl.read_parquet("data.parquet")  # Loads everything
df = df.filter(pl.col("x") > 0)
df = df.select(["x", "y"])
```

### 2. Chain Operations

```python
# GOOD: Single chain, optimized execution
result = (
    df
    .filter(pl.col("status") == "active")
    .with_columns([
        (pl.col("a") + pl.col("b")).alias("sum"),
        pl.col("date").dt.year().alias("year")
    ])
    .group_by("year")
    .agg(pl.col("sum").mean())
)

# AVOID: Multiple separate operations
df = df.filter(pl.col("status") == "active")
df = df.with_columns((pl.col("a") + pl.col("b")).alias("sum"))
df = df.with_columns(pl.col("date").dt.year().alias("year"))
result = df.group_by("year").agg(pl.col("sum").mean())
```

### 3. Use Appropriate Data Types

```python
# Optimize memory with correct types
df = df.with_columns([
    pl.col("small_int").cast(pl.Int16),
    pl.col("category").cast(pl.Categorical),
    pl.col("flag").cast(pl.Boolean),
    pl.col("precise_float").cast(pl.Float32)  # If precision allows
])

# Check memory usage
print(df.estimated_size("mb"))
```

### 4. Filter Early

```python
# GOOD: Filter before expensive operations
result = (
    pl.scan_parquet("data.parquet")
    .filter(pl.col("date") >= "2025-01-01")  # Filter first
    .group_by("category")
    .agg(pl.col("value").sum())
    .collect()
)

# AVOID: Filter after loading everything
result = (
    pl.scan_parquet("data.parquet")
    .group_by("category")
    .agg(pl.col("value").sum())
    .filter(...)  # Too late, already processed all data
    .collect()
)
```

### 5. Use Expressions Over Apply

```python
# GOOD: Vectorized expression
df.with_columns([
    pl.when(pl.col("x") > 0).then(pl.col("x")).otherwise(0).alias("positive_x")
])

# AVOID: Python function (slow)
df.with_columns([
    pl.col("x").map_elements(lambda v: v if v > 0 else 0).alias("positive_x")
])
```

## Troubleshooting

### Common Issues

**Issue: Out of Memory**
```python
# Solution 1: Use streaming
result = lf.collect(streaming=True)

# Solution 2: Sink to file
lf.sink_parquet("output.parquet")

# Solution 3: Process in chunks
for chunk in pl.read_csv_batched("large.csv", batch_size=100000):
    process(chunk)
```

**Issue: Slow Performance**
```python
# Check query plan for inefficiencies
print(lf.explain(optimized=True))

# Use profiling
result = lf.profile()
print(result[1])  # Timing information
```

**Issue: Type Mismatch in Join**
```python
# Ensure matching types before join
df1 = df1.with_columns(pl.col("id").cast(pl.Int64))
df2 = df2.with_columns(pl.col("id").cast(pl.Int64))
result = df1.join(df2, on="id")
```

**Issue: Date Parsing Errors**
```python
# Explicit format specification
df = df.with_columns([
    pl.col("date_str").str.strptime(pl.Date, "%Y-%m-%d"),
    pl.col("datetime_str").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S")
])
```

## Version History

- **1.0.0** (2026-01-17): Initial release with comprehensive Polars coverage
  - Core DataFrame operations
  - Lazy evaluation patterns
  - Expression API reference
  - GroupBy and window functions
  - Join operations
  - ETL pipeline examples
  - Time series analysis
  - Streaming for large datasets
  - Integration examples
  - Best practices and troubleshooting

## Resources

- **Official Documentation**: https://docs.pola.rs/
- **User Guide**: https://docs.pola.rs/user-guide/
- **API Reference**: https://docs.pola.rs/api/python/stable/reference/
- **GitHub**: https://github.com/pola-rs/polars
- **Cookbook**: https://docs.pola.rs/user-guide/misc/cookbook/

---

**Use Polars for maximum performance on large datasets with intuitive, expressive data transformations!**
