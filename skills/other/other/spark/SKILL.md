---
name: spark
description: Apache Spark distributed computing. Use for big data processing.
---

# Apache Spark

Spark is the king of Big Data. v4.0 (2024/2025) makes **Spark Connect** the default, allowing thin clients (like VS Code) to connect to massive clusters easily.

## When to Use

- **Data Engineering**: ETL at Petabyte scale.
- **Streaming**: Structured Streaming for real-time analytics.
- **Legacy ML**: `spark.ml` (though mostly replaced by XGBoost/Torch).

## Core Concepts

### Spark Connect

Decouples client (your laptop) from server (the cluster). Allows using Spark from Go/Rust/TypeScript.

### Catalyst Optimizer

Optimizes your SQL/DataFrame queries before execution.

### RDD

The low-level API. Almost never used directly in modern Spark.

## Best Practices (2025)

**Do**:

- **Use PySpark**: It is now a first-class citizen with Python UDF profiling.
- **Use Delta Lake / Iceberg**: Spark works best with modern table formats.
- **Use `pandas_udf`**: For vectorized Python UDFs.

**Don't**:

- **Don't use `rdd.map`**: It is slow (Python serialization). Use DataFrames.

## References

- [Apache Spark](https://spark.apache.org/)
