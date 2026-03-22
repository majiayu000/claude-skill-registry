---
name: data-lakehouse
cluster: data-engineering
description: "Design and implement data lakehouse architectures for scalable big data storage and analytics."
tags: ["data-lakehouse","big-data","data-engineering"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "data lakehouse big data analytics engineering"
---

# data-lakehouse

## Purpose
This skill enables the design and implementation of data lakehouse architectures, combining data lakes with warehouse features for scalable big data storage and analytics. Use it to manage petabyte-scale data with ACID transactions, schema evolution, and optimized query performance on platforms like Delta Lake or Iceberg.

## When to Use
- When handling large-scale data ingestion from sources like S3 or Kafka, requiring both raw storage and structured querying.
- For analytics workloads needing real-time updates, such as ETL pipelines in e-commerce or IoT data processing.
- If you're integrating with Spark or Presto for SQL analytics on unstructured data.

## Key Capabilities
- **Architecture Design**: Generate blueprints for lakehouse setups, including partitioning strategies and metadata management (e.g., using Iceberg for table formats).
- **Data Ingestion**: Support for batch and streaming ingestion with tools like Apache Spark, handling formats like Parquet or ORC.
- **Query Optimization**: Implement caching and indexing for faster queries, such as creating Delta Lake tables with Z-order clustering.
- **Scalability**: Auto-scale storage and compute resources via cloud APIs, e.g., AWS Glue for ETL jobs.
- **Security**: Enforce row-level access controls using policies like AWS Lake Formation grants.

## Usage Patterns
- **Pattern 1**: For new lakehouse setup, invoke the skill to generate a configuration file, then use it to initialize storage. Example: Create a Delta Lake table from CSV data.
- **Pattern 2**: In analytics workflows, use the skill to optimize queries by adding indexes, then execute via Spark SQL.
- **Pattern 3**: For maintenance, periodically run checks for schema evolution and merge operations on existing tables.

## Common Commands/API
Use the OpenClaw CLI or API for this skill. Authentication requires setting `$DATA_LAKEHOUSE_API_KEY` as an environment variable.

- **CLI Command**: Initialize a lakehouse project:
  ```
  openclaw skill data-lakehouse init --project my-lakehouse --storage s3://my-bucket --engine delta
  ```
  This creates a basic configuration file with S3 bucket and Delta Lake engine.

- **API Endpoint**: Create a table via POST request:
  ```
  curl -H "Authorization: Bearer $DATA_LAKEHOUSE_API_KEY" \
       -d '{"table_name": "sales_data", "format": "parquet", "partition_by": ["date"]}' \
       https://api.openclaw.ai/data-lakehouse/tables
  ```
  Response includes table metadata for immediate use.

- **Code Snippet**: In Python, integrate with Spark:
  ```
  from pyspark.sql import SparkSession
  spark = SparkSession.builder.appName("lakehouse").getOrCreate()
  df = spark.read.format("delta").load("s3://my-bucket/sales_data")
  df.write.format("delta").mode("append").save("s3://my-bucket/sales_data")
  ```
  This appends data to a Delta table; ensure Spark is configured with AWS credentials.

- **Config Format**: Use JSON for lakehouse configs, e.g.:
  ```
  {
    "storage": "s3://my-bucket",
    "engine": "iceberg",
    "auth": {"key": "$DATA_LAKEHOUSE_API_KEY"}
  }
  ```
  Load this via CLI: `openclaw skill data-lakehouse apply --config path/to/config.json`.

## Integration Notes
- **With Other Skills**: Link to "big-data" skills by passing outputs, e.g., pipe data from a Kafka ingestion skill into this one using Spark streaming.
- **External Tools**: Integrate with AWS S3 by setting bucket policies; use `--aws-region us-west-2` in CLI commands. For Spark, ensure dependencies like `spark.delta` are in your environment.
- **API Integration**: When calling from other services, handle retries for rate limits; example: Use the same `$DATA_LAKEHOUSE_API_KEY` in chained API calls.
- **Dependency Management**: Always specify versions, e.g., require Spark 3.0+ for Delta Lake compatibility.

## Error Handling
- **Common Errors**: Handle authentication failures by checking if `$DATA_LAKEHOUSE_API_KEY` is set; use `os.environ.get('DATA_LAKEHOUSE_API_KEY')` in scripts.
- **Prescriptive Steps**: For storage access errors (e.g., S3 permissions), add try-except blocks:
  ```
  try:
      spark.read.format("delta").load("s3://my-bucket/data")
  except Exception as e:
      print(f"Error: {e}. Check bucket permissions and retry.")
  ```
  Retry transient errors like network issues with exponential backoff in API calls.
- **Debugging**: Use CLI flag `--verbose` for detailed logs, e.g., `openclaw skill data-lakehouse init --verbose`. Validate configs with `openclaw skill data-lakehouse validate --file config.json`.

## Concrete Usage Examples
- **Example 1**: Building a sales analytics lakehouse:
  First, initialize: `openclaw skill data-lakehouse init --project sales-ana --storage s3://sales-data`. Then, ingest data: Use the API to create a table, and append via Spark as shown above. Finally, query with: `spark.sql("SELECT * FROM sales_data WHERE date > '2023-01-01'")`.
  
- **Example 2**: Optimizing an existing lakehouse for IoT data:
  Run: `openclaw skill data-lakehouse optimize --table iot_metrics --add-index date`. This adds an index; verify with a query snippet: `df = spark.read.format("iceberg").load("s3://iot-bucket/metrics").filter(df.date > current_date())`. Monitor performance post-optimization.

## Graph Relationships
- Related to: "big-data" (shares tags for data processing pipelines), "data-engineering" (cluster affiliation for ETL workflows).
- Connected via: Tags like "data-lakehouse" for cross-skill queries, and "data-engineering" cluster for sequential task flows.
