---
name: stream-processing
cluster: data-engineering
description: "Process continuous data streams in real-time using frameworks like Kafka and Flink for efficient data engineering."
tags: ["streaming","data-processing","real-time"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "stream processing real-time data kafka flink apache spark"
---

# stream-processing

## Purpose
This skill enables real-time processing of continuous data streams using frameworks like Kafka, Flink, and Apache Spark. It's designed for scenarios requiring immediate data ingestion, transformation, and analysis to support data engineering pipelines.

## When to Use
Use this skill for high-volume data sources like IoT sensors, log files, or financial transactions that need real-time analytics. Apply it when batch processing is insufficient, such as monitoring system metrics, detecting anomalies, or updating dashboards dynamically.

## Key Capabilities
- Handle high-throughput streams with Kafka's distributed architecture, supporting topics, partitions, and replication for fault tolerance.
- Perform stateful computations in Flink using windowing (e.g., tumbling windows for 1-minute aggregations) and exactly-once processing semantics.
- Integrate Apache Spark Streaming for scalable processing, leveraging DStreams or Structured Streaming APIs for transformations like map and reduce.
- Support backpressure handling to prevent overloads, as in Flink's configurable checkpointing intervals.

## Usage Patterns
- **Producer-Consumer Pattern**: Ingest data via Kafka producers and process with Flink consumers. For example, send logs to a Kafka topic and use Flink to filter and aggregate them in real-time.
- **Windowed Aggregation**: Apply time-based windows in Flink for summarizing data, such as counting events per minute.
- **ETL Pipelines**: Use Spark Streaming to extract from Kafka, transform with SQL queries, and load into databases like Elasticsearch.
- **Fault-Tolerant Processing**: Configure checkpoints in Flink jobs to resume from failures, ensuring no data loss in production environments.

## Common Commands/API
- **Kafka CLI Commands**: Use `kafka-console-producer --topic my-topic --broker-list localhost:9092` to send messages. For consumption: `kafka-console-consumer --topic my-topic --from-beginning --bootstrap-server localhost:9092`.
- **Flink Commands**: Submit a job with `flink run -c com.example.StreamJob /path/to/jar --input kafka-topic --output file:///output` to process streams. Use Flink's REST API at `http://localhost:8081/jobs/overview` for monitoring.
- **Spark Streaming API**: In Scala, create a stream with `val stream = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092").load()`. Then apply transformations: `stream.selectExpr("CAST(value AS STRING)").writeStream.outputMode("append").format("console").start()`.
- **Config Formats**: Kafka requires a properties file like `key.serializer=org.apache.kafka.common.serialization.StringSerializer` for producers. Flink uses YAML for configurations, e.g., `execution.checkpointing.interval: 1min`.

## Integration Notes
Integrate Kafka as a source for Flink by adding dependencies in your Flink job (e.g., via Maven: `<dependency><groupId>org.apache.flink</groupId><artifactId>flink-connector-kafka</artifactId></dependency>`). For authentication, set environment variables like `$KAFKA_API_KEY` in your producer script: `export KAFKA_API_KEY=your_key; kafka-console-producer --broker-list localhost:9092 --producer.config /path/to/config.properties`. Link Spark with Kafka using Spark's built-in connectors, ensuring cluster compatibility (e.g., Spark 3.x with Kafka 2.8+). For external services, use API keys via env vars, e.g., `$SPARK_MASTER_URL` for connecting to a Spark cluster.

## Error Handling
Handle Kafka connection errors by implementing retries in producers, e.g., using a loop with exponential backoff: `try { producer.send(record) } catch (Exception e) { Thread.sleep(2000 * attempts); }`. In Flink, enable restart strategies with `env.setRestartStrategy(RestartStrategies.fixedDelayRestart(3, Time.of(10, TimeUnit.SECONDS)))` to recover from task failures. For Spark, use checkpointing in streaming queries: `writeStream.option("checkpointLocation", "/path/to/checkpoints").start()` to restore state on failures. Log errors with structured formats, e.g., via SLF4J, and monitor with tools like Prometheus for real-time alerts.

## Concrete Usage Examples
1. **Kafka-Flink Real-Time Log Processing**: Ingest logs into Kafka with `kafka-console-producer --topic logs --broker-list localhost:9092`. Then run a Flink job: `flink run -c com.example.LogProcessor /path/to/jar --input logs`. The job filters errors: `env.addSource(new FlinkKafkaConsumer<>("logs", ...)).filter(line -> line.contains("ERROR")).print()`.
2. **Spark Streaming for Sensor Data Aggregation**: Read from Kafka in Spark: `val df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092").option("subscribe", "sensors").load()`. Aggregate data: `df.groupBy(window($"timestamp", "1 minute")).avg("value").writeStream.format("console").start()`. This processes IoT sensor streams for minute-level averages.

## Graph Relationships
- Related to cluster: data-engineering
- Linked skills: data-ingestion (as a data source), machine-learning (for real-time model inference on streams)
- Dependencies: Requires skills like containerization for deploying Kafka/Flink clusters
