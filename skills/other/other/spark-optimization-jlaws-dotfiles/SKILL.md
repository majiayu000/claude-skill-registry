---
name: spark-optimization
description: Optimize Apache Spark jobs with partitioning, caching, shuffle optimization, and memory tuning. Use when improving Spark performance, debugging slow jobs, or scaling data processing pipelines.
---

# Apache Spark Optimization

## Key Performance Factors

| Factor | Impact | Solution |
|--------|--------|----------|
| **Shuffle** | Network I/O, disk I/O | Minimize wide transformations |
| **Data Skew** | Uneven task duration | Salting, broadcast joins |
| **Serialization** | CPU overhead | Use Kryo, columnar formats |
| **Memory** | GC pressure, spills | Tune executor memory |
| **Partitions** | Parallelism | Right-size partitions |

## Pattern 1: Optimal Partitioning

```python
# Optimal partition size: 128MB - 256MB
def calculate_partitions(data_size_gb: float, partition_size_mb: int = 128) -> int:
    return max(int(data_size_gb * 1024 / partition_size_mb), 1)

# Repartition for even distribution
df_repartitioned = df.repartition(200, "partition_key")

# Coalesce to reduce partitions (no shuffle)
df_coalesced = df.coalesce(100)

# Partition pruning with predicate pushdown
df = (spark.read.parquet("s3://bucket/data/")
    .filter(F.col("date") == "2024-01-01"))  # Pushed down

# Write with partitioning
(df.write
    .partitionBy("year", "month", "day")
    .mode("overwrite")
    .parquet("s3://bucket/partitioned_output/"))
```

## Pattern 2: Join Optimization

```python
from pyspark.sql import functions as F

# 1. Broadcast Join - Small table < 10MB
result = large_df.join(F.broadcast(small_df), on="key", how="left")

# 2. Bucket Join - Pre-sorted, no shuffle at join time
(df.write
    .bucketBy(200, "customer_id")
    .sortBy("customer_id")
    .mode("overwrite")
    .saveAsTable("bucketed_orders"))

# 3. AQE Skew Join
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5")

# 4. Manual salting for severe skew
def salt_join(df_skewed, df_other, key_col, num_salts=10):
    df_salted = df_skewed.withColumn(
        "salt", (F.rand() * num_salts).cast("int")
    ).withColumn("salted_key", F.concat(F.col(key_col), F.lit("_"), F.col("salt")))

    df_exploded = df_other.crossJoin(
        spark.range(num_salts).withColumnRenamed("id", "salt")
    ).withColumn("salted_key", F.concat(F.col(key_col), F.lit("_"), F.col("salt")))

    return df_salted.join(df_exploded, on="salted_key", how="inner")
```

## Pattern 3: Caching and Persistence

```python
from pyspark import StorageLevel

df_filtered = df.filter(F.col("status") == "active")
df_filtered.persist(StorageLevel.MEMORY_AND_DISK_SER)
df_filtered.count()  # Force materialization

# Use in multiple actions
agg1 = df_filtered.groupBy("category").count()
agg2 = df_filtered.groupBy("region").sum("amount")

df_filtered.unpersist()  # When done

# Storage levels:
# MEMORY_ONLY - Fast, may not fit
# MEMORY_AND_DISK - Spills to disk (recommended)
# MEMORY_ONLY_SER - Serialized, less memory, more CPU
# DISK_ONLY - When memory is tight

# Checkpoint for complex lineage
spark.sparkContext.setCheckpointDir("s3://bucket/checkpoints/")
df_complex.checkpoint()  # Breaks lineage, materializes
```

## Pattern 4: Memory Tuning

```python
# Memory breakdown (8GB executor):
# spark.memory.fraction = 0.6 (4.8GB for execution + storage)
#   spark.memory.storageFraction = 0.5 (2.4GB cache, 2.4GB execution)
# 40% = 3.2GB for user data structures

spark = (SparkSession.builder
    .config("spark.executor.memory", "8g")
    .config("spark.executor.memoryOverhead", "2g")
    .config("spark.memory.fraction", "0.6")
    .config("spark.memory.storageFraction", "0.5")
    .config("spark.sql.shuffle.partitions", "200")
    .config("spark.sql.autoBroadcastJoinThreshold", "50MB")
    .config("spark.sql.files.maxPartitionBytes", "128MB")
    .getOrCreate())
```

## Pattern 5: Shuffle Optimization

```python
spark.conf.set("spark.sql.shuffle.partitions", "auto")  # With AQE
spark.conf.set("spark.shuffle.compress", "true")

# Pre-aggregate before shuffle
df_optimized = (df
    .groupBy("key", "partition_col")
    .agg(F.sum("value").alias("partial_sum"))
    .groupBy("key")
    .agg(F.sum("partial_sum").alias("total")))

# Approximate distinct (no shuffle)
approx_count = df.select(F.approx_count_distinct("category")).collect()[0][0]

# Use coalesce instead of repartition when reducing
df_reduced = df.coalesce(10)  # No shuffle
```

## Pattern 6: Data Format Optimization

```python
# Column pruning - only read needed columns
df = (spark.read.parquet("s3://bucket/data/")
    .select("id", "amount", "date"))  # Only reads these

# Delta Lake optimizations
(df.write
    .format("delta")
    .option("optimizeWrite", "true")
    .option("autoCompact", "true")
    .mode("overwrite")
    .save("s3://bucket/delta_table/"))

# Z-ordering for multi-dimensional queries
spark.sql("OPTIMIZE delta.`s3://bucket/delta_table/` ZORDER BY (customer_id, date)")
```

## Pattern 7: Monitoring and Debugging

```python
# Explain query plan
df.explain(mode="extended")
# Modes: simple, extended, codegen, cost, formatted

# Identify data skew
def check_partition_skew(df):
    partition_counts = (df
        .withColumn("partition_id", F.spark_partition_id())
        .groupBy("partition_id")
        .count()
        .orderBy(F.desc("count")))

    stats = partition_counts.select(
        F.min("count").alias("min"),
        F.max("count").alias("max"),
        F.avg("count").alias("avg"),
    ).collect()[0]

    skew_ratio = stats["max"] / stats["avg"]
    print(f"Skew ratio: {skew_ratio:.2f}x (>2x indicates skew)")
```

## Configuration Cheat Sheet

```python
spark_configs = {
    # AQE
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    "spark.sql.adaptive.skewJoin.enabled": "true",
    # Memory
    "spark.executor.memory": "8g",
    "spark.executor.memoryOverhead": "2g",
    "spark.memory.fraction": "0.6",
    # Parallelism
    "spark.sql.shuffle.partitions": "200",
    "spark.default.parallelism": "200",
    # Serialization
    "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
    "spark.sql.execution.arrow.pyspark.enabled": "true",
    # Compression
    "spark.io.compression.codec": "lz4",
    "spark.shuffle.compress": "true",
    # Broadcast
    "spark.sql.autoBroadcastJoinThreshold": "50MB",
    # File handling
    "spark.sql.files.maxPartitionBytes": "128MB",
}
```
