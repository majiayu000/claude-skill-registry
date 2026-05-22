---
name: fabric-pandas-perf-remediate
description: Troubleshoot and optimize pandas performance in Microsoft Fabric Spark notebooks. Use when diagnosing slow pandas operations, toPandas() out-of-memory errors, pandas API on Spark (pyspark.pandas) bottlenecks, DataFrame conversion failures, collect() memory issues, driver memory exhaustion, notebook cell timeouts, or when optimizing pandas workloads for Fabric capacity. Covers pandas vs Spark DataFrame conversion, memory profiling, broadcast joins, shuffle tuning, resource profiles, and Native Execution Engine integration.
license: Complete terms in LICENSE.txt
---

# Fabric Pandas Performance Troubleshooting

Diagnose and resolve pandas-related performance issues in Microsoft Fabric Spark notebooks, including memory exhaustion, slow conversions, and suboptimal pandas API on Spark usage.

## When to Use This Skill

- Notebook cells hang or timeout during pandas operations
- `toPandas()` fails with OutOfMemoryError or Java heap space errors
- `collect()` crashes the driver node
- Pandas API on Spark (`pyspark.pandas` / `ps`) runs slower than expected
- DataFrame conversion between Spark and pandas causes memory spikes
- Notebook kernel restarts unexpectedly during data processing
- Large dataset operations exhaust driver memory on Fabric capacity
- Need to choose between pandas, Spark DataFrame, or pandas API on Spark

## Prerequisites

- Microsoft Fabric workspace with Data Engineering experience
- Fabric capacity F2 or higher (F64+ recommended for large datasets)
- PySpark notebook with Spark session active
- Basic familiarity with pandas and PySpark DataFrames

## Quick Diagnosis

### Symptom-to-Solution Map

| Symptom | Likely Cause | Jump To |
|---------|-------------|---------|
| `toPandas()` OOM error | Dataset too large for driver | [toPandas Optimization](#topandas-optimization) |
| Kernel restart during pandas op | Driver memory exhausted | [Driver Memory Tuning](#driver-memory-tuning) |
| `pyspark.pandas` slower than native pandas | Spark overhead on small data | [Right-Size Your Approach](#right-size-your-approach) |
| Slow groupby/merge in pandas API on Spark | Excessive shuffling | [Shuffle Optimization](#shuffle-optimization) |
| Cell timeout on DataFrame conversion | Large collect to driver | [Incremental Processing](#incremental-processing) |
| `ArrowInvalid` or conversion errors | Schema mismatch / nulls | [Arrow Conversion Fixes](#arrow-conversion-fixes) |
| High memory but slow pandas operations | GC pressure / fragmentation | [Memory Profiling](#memory-profiling) |

## Right-Size Your Approach

**Critical Decision**: Choose the right DataFrame API for your data size and workload.

```
Dataset Size Decision Tree:
─────────────────────────────────────────────────────────
< 100 MB          → Native pandas (pd.DataFrame)
100 MB - 1 GB     → pandas API on Spark (ps.DataFrame)
> 1 GB            → PySpark DataFrame (spark.DataFrame)
> 10 GB           → PySpark + partitioning + Delta optimization

Mixed workload?   → Process in Spark, convert final aggregation to pandas
Visualization?    → Aggregate in Spark first, toPandas() on summary only
ML feature eng?   → Spark for transforms, pandas for final model input
```

### API Comparison

| Operation | Native pandas | pandas API on Spark | PySpark DataFrame |
|-----------|--------------|--------------------|--------------------|
| Memory model | Single-node (driver) | Distributed | Distributed |
| Max practical size | ~2-4 GB | 10s-100s GB | TB+ |
| Startup overhead | None | Spark session | Spark session |
| groupby speed (small) | Fast | Slower (shuffle) | Slower (shuffle) |
| groupby speed (large) | OOM risk | Fast | Fast |
| Interop with Spark | `.toPandas()` | `.to_spark()` | Native |

## toPandas Optimization

### Problem
`toPandas()` collects the **entire distributed DataFrame** to the single driver node. This is the #1 cause of OOM in Fabric notebooks.

### Solutions (Progressive)

**1. Reduce data BEFORE conversion**
```python
# BAD - converts entire table
pdf = spark_df.toPandas()

# GOOD - filter and select first
pdf = (spark_df
    .filter("date >= '2024-01-01'")
    .select("customer_id", "revenue", "region")
    .toPandas())
```

**2. Aggregate in Spark, convert summary**
```python
# BAD - convert raw data then aggregate in pandas
pdf = spark_df.toPandas()
result = pdf.groupby('region')['revenue'].sum()

# GOOD - aggregate in Spark first
summary = spark_df.groupBy("region").agg(F.sum("revenue").alias("total_revenue"))
pdf = summary.toPandas()  # Only converting small aggregated result
```

**3. Enable Apache Arrow for faster conversion**
```python
# Enable Arrow-based columnar transfer (3-100x faster)
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
spark.conf.set("spark.sql.execution.arrow.pyspark.fallback.enabled", "true")

# Now toPandas() uses Arrow columnar format
pdf = spark_df.toPandas()
```

**4. Use sampling for exploration**
```python
# Sample before converting (for EDA/visualization)
pdf = spark_df.sample(fraction=0.01, seed=42).toPandas()

# Or limit rows
pdf = spark_df.limit(100000).toPandas()
```

**5. Chunk large conversions**
```python
# Process in chunks using partitioning
def process_in_chunks(spark_df, chunk_col="date", process_fn=None):
    """Convert Spark DF to pandas in manageable chunks."""
    chunks = [row[chunk_col] for row in spark_df.select(chunk_col).distinct().collect()]
    results = []
    for chunk_val in chunks:
        chunk_pdf = spark_df.filter(F.col(chunk_col) == chunk_val).toPandas()
        if process_fn:
            chunk_pdf = process_fn(chunk_pdf)
        results.append(chunk_pdf)
    return pd.concat(results, ignore_index=True)
```

## Driver Memory Tuning

### Fabric Driver Memory by Node Size

| Node Size | vCores | Memory | Recommended Max toPandas() |
|-----------|--------|--------|---------------------------|
| Small | 4 | 32 GB | ~4-6 GB |
| Medium | 8 | 64 GB | ~10-12 GB |
| Large | 16 | 128 GB | ~20-25 GB |
| X-Large | 32 | 256 GB | ~40-50 GB |

**Rule of thumb**: `toPandas()` safe limit ≈ 15-20% of total driver memory (pandas creates copies during operations).

### Configure Driver Memory
```python
# Check current driver memory
print(f"Driver memory: {spark.conf.get('spark.driver.memory', 'default')}")

# Set via environment Spark properties (before session starts)
# In Fabric Environment > Spark properties:
# spark.driver.memory = 28g  (for Medium nodes)

# Or override in notebook (must be first cell)
%%configure
{
    "driverMemory": "28g",
    "driverCores": 8
}
```

### Resource Profile Selection for Pandas Workloads
```python
# For notebooks heavy on pandas operations (read-heavy pattern)
spark.conf.set("spark.fabric.resourceProfile", "readHeavyForSpark")

# Key settings this enables:
# - spark.databricks.delta.optimizeWrite.enabled = true
# - Optimized read paths for Delta tables
```

## Shuffle Optimization

### Tune for pandas API on Spark Operations

```python
# Reduce shuffle partitions for smaller datasets
# Default 200 is too high for datasets < 10 GB
spark.conf.set("spark.sql.shuffle.partitions", "auto")  # Adaptive (AQE)

# Or set explicitly based on data size
# Rule: ~128 MB per partition
data_size_gb = 5
optimal_partitions = max(1, int(data_size_gb * 1024 / 128))
spark.conf.set("spark.sql.shuffle.partitions", str(optimal_partitions))

# Enable Adaptive Query Execution (on by default in Fabric)
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```

### Broadcast Join Optimization
```python
# Increase broadcast threshold for pandas API on Spark joins
# Default: 10 MB - increase for medium lookup tables
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "100m")  # 100 MB

# Force broadcast for known small DataFrames
from pyspark.sql.functions import broadcast
result = large_df.join(broadcast(small_lookup_df), "key_col")
```

### Enable Autotune
```python
# Let Fabric auto-optimize shuffle, broadcast, and partition settings
spark.conf.set("spark.ms.autotune.enabled", "true")

# Autotune requires:
# - Runtime 1.1 or 1.2
# - Queries > 15 seconds
# - Not in high concurrency mode
# - ~20-25 iterations to learn optimal settings
```

## Arrow Conversion Fixes

### Common Errors and Solutions

| Error | Cause | Fix |
|-------|-------|-----|
| `ArrowInvalid: Could not convert X` | Unsupported type | Cast column before conversion |
| `ArrowNotImplementedError` | Nested types | Flatten struct/array columns |
| `pyarrow.lib.ArrowMemoryError` | OOM during Arrow transfer | Reduce data size or increase memory |
| Null handling mismatch | Pandas NaN vs Spark null | Use `spark.sql.execution.arrow.pyspark.fallback.enabled` |

```python
# Fix mixed types before conversion
from pyspark.sql.types import StringType, DoubleType

spark_df = spark_df.withColumn("mixed_col", F.col("mixed_col").cast(StringType()))

# Flatten nested structs
spark_df = spark_df.select(
    "simple_col",
    F.col("struct_col.field1").alias("field1"),
    F.col("struct_col.field2").alias("field2")
)

# Handle null-heavy columns
spark_df = spark_df.fillna({"numeric_col": 0, "string_col": ""})
```

## Incremental Processing

### Pattern: Spark Processing with Pandas Finish

```python
import pyspark.sql.functions as F
import pandas as pd

# Step 1: Heavy lifting in Spark (distributed)
aggregated = (spark_df
    .filter(F.col("status") == "active")
    .groupBy("category", "month")
    .agg(
        F.sum("amount").alias("total"),
        F.count("*").alias("cnt"),
        F.avg("score").alias("avg_score")
    ))

# Step 2: Verify size before conversion
row_count = aggregated.count()
print(f"Rows to convert: {row_count:,}")
assert row_count < 1_000_000, f"Too many rows ({row_count:,}) for toPandas()"

# Step 3: Convert small result to pandas for visualization/export
pdf = aggregated.toPandas()

# Step 4: Pandas-specific operations (plotting, styling, etc.)
pivot = pdf.pivot_table(index='category', columns='month', values='total')
```

## Memory Profiling

### Monitor Driver Memory in Notebook
```python
import os, psutil

def check_memory():
    """Report current driver memory usage."""
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    print(f"RSS Memory:  {mem_info.rss / 1024**3:.2f} GB")
    print(f"VMS Memory:  {mem_info.vms / 1024**3:.2f} GB")
    
    # System-wide
    sys_mem = psutil.virtual_memory()
    print(f"System Used: {sys_mem.used / 1024**3:.2f} / {sys_mem.total / 1024**3:.2f} GB ({sys_mem.percent}%)")

# Call before/after pandas operations
check_memory()
pdf = spark_df.toPandas()
check_memory()
```

### Reduce pandas Memory Footprint
```python
def optimize_pandas_dtypes(df):
    """Downcast pandas DataFrame dtypes to reduce memory."""
    for col in df.select_dtypes(include=['int64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:  # Categorical threshold
            df[col] = df[col].astype('category')
    return df

pdf = optimize_pandas_dtypes(pdf)
print(f"Memory after optimization: {pdf.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
```

## pandas API on Spark Best Practices

### Use `pyspark.pandas` Instead of Conversion
```python
import pyspark.pandas as ps

# Read directly as pandas-on-Spark DataFrame
psdf = ps.read_delta("Tables/my_table")

# Or convert from Spark DataFrame (lazy, no collect)
psdf = spark_df.pandas_api()

# Operations run distributed (no driver memory pressure)
result = psdf.groupby("region")["revenue"].sum()

# Convert to pandas only for final small result
pdf = result.to_pandas()
```

### Common Pitfalls

```python
# BAD: iterrows/itertuples on pandas-on-Spark (extremely slow)
for idx, row in psdf.iterrows():  # Anti-pattern!
    process(row)

# GOOD: Use vectorized operations
psdf["new_col"] = psdf["col_a"] * psdf["col_b"]

# BAD: apply with Python UDF (serialization overhead)
psdf["result"] = psdf["col"].apply(lambda x: complex_fn(x))

# GOOD: Use Spark-native functions or pandas_udf
from pyspark.sql.functions import pandas_udf
@pandas_udf("double")
def optimized_fn(series: pd.Series) -> pd.Series:
    return series * 2 + 1
```

## Troubleshooting Checklist

1. **Check data size** before any `toPandas()` / `collect()` call
2. **Enable Arrow** transfer: `spark.sql.execution.arrow.pyspark.enabled = true`
3. **Filter/aggregate** in Spark before converting to pandas
4. **Match node size** to workload (Medium 64 GB minimum for pandas-heavy notebooks)
5. **Use pandas API on Spark** for distributed pandas-like operations
6. **Monitor memory** with `psutil` before/after conversions
7. **Set resource profile** to `readHeavyForSpark` for notebook-heavy workloads
8. **Enable autotune** for automatic shuffle and partition optimization
9. **Downcast dtypes** after conversion to reduce pandas memory footprint
10. **Chunk processing** for datasets that exceed single-node memory

## Automation & Diagnostics

Run the [diagnostic script](./scripts/Invoke-PandasDiagnostics.ps1) to collect Spark session configuration, memory settings, and environment details for troubleshooting.

See the [detailed reference guide](./references/pandas-performance-deep-dive.md) for advanced patterns including pandas UDFs, Koalas migration, Native Execution Engine integration, and capacity planning formulas.

Use the [notebook template](./templates/pandas-performance-template.py) as a starting point for memory-safe pandas workflows in Fabric notebooks.
