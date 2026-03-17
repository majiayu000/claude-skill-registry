---
name: spark
cluster: data-engineering
description: "Distributed processing framework for large-scale data sets using in-memory computing."
tags: ["spark","big-data","distributed-computing"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "apache spark big data processing distributed computing"
---

# spark

## Purpose
Apache Spark is a fast, distributed processing framework for handling large-scale data sets using in-memory computing. It enables efficient batch processing, real-time analytics, machine learning, and graph processing on clusters.

## When to Use
Use Spark for processing datasets larger than a single machine's memory, such as analyzing terabytes of log data or running ETL jobs. Apply it in scenarios requiring fast iterative computations, like machine learning algorithms, or when integrating with big data ecosystems like Hadoop. Avoid it for small-scale tasks where simpler tools like Pandas suffice.

## Key Capabilities
- In-memory caching for speeding up iterative algorithms, e.g., via `persist(StorageLevel.MEMORY_ONLY)`.
- Fault-tolerant distributed computing with RDDs (Resilient Distributed Datasets) for automatic recovery.
- Support for multiple languages: Scala, Python, Java, R; e.g., use PySpark for data frames with `from pyspark.sql import SparkSession`.
- Built-in libraries: Spark SQL for structured data queries, MLlib for machine learning, GraphX for graph processing, and Structured Streaming for real-time data.
- Scalability to thousands of nodes, with dynamic resource allocation via YARN or Kubernetes.

## Usage Patterns
To process data with Spark, start by creating a SparkSession in your code. For batch jobs, submit via spark-submit; for interactive work, use Spark shells. Always specify the master URL, like "yarn" for cluster mode. Handle data sources by reading from files or databases, transforming with DataFrames, and writing outputs. For streaming, use Structured Streaming to process Kafka topics in real-time.

Example 1: Word count in PySpark.
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("WordCount").getOrCreate()
words = spark.read.text("hdfs://path/to/file.txt").rdd.flatMap(lambda x: x[0].split(" "))
counts = words.map(lambda x: (x, 1)).reduceByKey(lambda a, b: a + b)
counts.saveAsTextFile("hdfs://output/path")
```

Example 2: ETL job from CSV to Parquet.
```python
spark = SparkSession.builder.master("local[*]").appName("ETL").getOrCreate()
df = spark.read.format("csv").option("header", "true").load("s3://bucket/data.csv")
df.write.format("parquet").mode("overwrite").save("hdfs://processed/data.parquet")
```
To run these, use: `spark-submit --master yarn --executor-memory 4g your_script.py`.

## Common Commands/API
Use spark-submit for running applications: `spark-submit --class MainClass --master yarn --deploy-mode cluster --driver-memory 2g your.jar arg1 arg2`. For interactive sessions, run `pyspark` or `spark-shell`. Key API calls include creating a SparkSession: `SparkSession.builder().appName("App").master("local").getOrCreate()`. Read data with `spark.read.csv("path", header=True, inferSchema=True)`. Transform data using DataFrame APIs, e.g., `df.filter(df['age'] > 30).groupBy('department').count()`. For configurations, use SparkConf: `conf = SparkConf().set("spark.executor.cores", "2")`. Set env vars for cluster access, like `$SPARK_MASTER_URL` for the master node.

## Integration Notes
Integrate Spark with Hadoop by setting `$HADOOP_CONF_DIR` env var to your Hadoop config path, then use YARN as the master. For Kafka, add the connector via `--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2` in spark-submit, and read streams with `spark.readStream.format("kafka").option("kafka.bootstrap.servers", "host:port").load()`. Connect to databases using JDBC: `df.write.jdbc(url="jdbc:postgresql://host/db", table="table", mode="append")`, requiring JDBC drivers in the classpath. Use config files like `spark-defaults.conf` for settings, e.g., `spark.sql.shuffle.partitions 200`.

## Error Handling
Handle OutOfMemory errors by increasing memory: add `--driver-memory 4g --executor-memory 8g` to spark-submit. For failed tasks, check Spark UI at `http://driver-host:4040` for logs, and use `spark.task.maxFailures` config to set retry limits. Common serialization issues (e.g., NotSerializableException) are fixed by making classes serializable, like implementing `Serializable` in Java. For data skew, repartition data with `df.repartition(100).write...`. Always wrap code in try-except for API calls, e.g., `try: df = spark.read.csv("path") except Exception as e: print(e)`.

## Graph Relationships
Connected to: data-engineering cluster (e.g., hadoop for storage, airflow for orchestration). Related tags: big-data, distributed-computing. Links: integrates with kafka for streaming, uses hadoop file systems for input/output.
