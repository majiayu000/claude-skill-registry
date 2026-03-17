---
name: spark-basics
description: PySpark fundamentals for distributed data processing.
---

# Spark Basics

## SparkSession

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ETL Job") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()
```

## Reading Data

```python
# CSV
df = spark.read.csv("s3://bucket/data.csv", header=True, inferSchema=True)

# Parquet
df = spark.read.parquet("s3://bucket/data/")

# JSON
df = spark.read.json("s3://bucket/data.json")

# Delta Lake
df = spark.read.format("delta").load("s3://bucket/delta/")
```

## Transformations

```python
from pyspark.sql import functions as F

# Select and rename
df = df.select(
    F.col("id").alias("user_id"),
    F.col("name"),
    F.col("created_at").cast("timestamp")
)

# Filter
df = df.filter(F.col("status") == "active")

# Aggregate
summary = df.groupBy("category").agg(
    F.count("*").alias("count"),
    F.sum("amount").alias("total"),
    F.avg("amount").alias("average")
)

# Join
result = orders.join(customers, "customer_id", "left")

# Window functions
from pyspark.sql.window import Window

window = Window.partitionBy("user_id").orderBy("created_at")
df = df.withColumn("row_num", F.row_number().over(window))
```

## Writing Data

```python
# Parquet with partitions
df.write \
    .partitionBy("year", "month") \
    .mode("overwrite") \
    .parquet("s3://bucket/output/")

# Delta Lake
df.write \
    .format("delta") \
    .mode("merge") \
    .save("s3://bucket/delta/")
```

## Optimization

- Use `cache()` for reused DataFrames
- Avoid `collect()` on large data
- Broadcast small tables
- Repartition before joins
- Use predicate pushdown
