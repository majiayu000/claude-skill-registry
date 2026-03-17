---
name: streaming-data-processing
description: Process real-time data streams with Kafka Streams, Flink, and windowing patterns
---

# Streaming Data Processing

## Decision Table

| Requirement | Framework | Why |
|-------------|-----------|-----|
| Sub-second latency, simple transforms | Kafka Consumers (Python) | Minimal infra, direct control |
| Complex event processing, stateful | Apache Flink | True streaming, exactly-once, watermarks |
| Existing Spark cluster, micro-batch OK | Spark Structured Streaming | Unified batch+stream API |
| Lightweight, embedded stream processing | Faust (Python) | Pure Python, Kafka-native, async |
| CDC / database replication | Debezium + Kafka Connect | Schema-aware, no app code |

## Kafka Consumer Patterns

### Manual Offset Management

```python
# consumer.py
from confluent_kafka import Consumer, KafkaException, TopicPartition
import json

def create_consumer(group_id: str, brokers: str = "localhost:9092") -> Consumer:
    return Consumer({
        "bootstrap.servers": brokers,
        "group.id": group_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,  # manual commit for at-least-once
    })

def consume_loop(consumer: Consumer, topics: list[str],
                  process_fn, batch_size: int = 100):
    """Consume with manual offset commit after processing."""
    consumer.subscribe(topics)
    buffer = []
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            buffer.append((msg, json.loads(msg.value().decode("utf-8"))))
            if len(buffer) >= batch_size:
                process_fn([r for _, r in buffer])
                consumer.commit(offsets=[
                    TopicPartition(m.topic(), m.partition(), m.offset() + 1)
                    for m, _ in buffer
                ], asynchronous=False)
                buffer.clear()
    finally:
        consumer.close()
```

### Exactly-Once with Transactions

```python
# transactional_producer.py
from confluent_kafka import Producer

def create_transactional_producer(txn_id: str, brokers: str = "localhost:9092"):
    producer = Producer({
        "bootstrap.servers": brokers,
        "transactional.id": txn_id,
        "enable.idempotence": True,
    })
    producer.init_transactions()
    return producer

def consume_transform_produce(consumer, producer, process_fn):
    """Read-process-write in a single Kafka transaction."""
    consumer.subscribe(["input-topic"])
    while True:
        msg = consumer.poll(1.0)
        if msg is None or msg.error():
            continue
        result = process_fn(msg.value())
        producer.begin_transaction()
        try:
            producer.produce("output-topic", value=result)
            producer.send_offsets_to_transaction(
                consumer.position(consumer.assignment()),
                consumer.consumer_group_metadata(),
            )
            producer.commit_transaction()
        except Exception:
            producer.abort_transaction()
            raise
```

## Flink Python API (PyFlink)

```python
# flink_stream.py
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import (
    KafkaSource, KafkaOffsetsInitializer)
from pyflink.common import WatermarkStrategy, Duration
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.window import TumblingEventTimeWindows, Time
import json

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(4)
env.enable_checkpointing(60000)  # checkpoint every 60s

source = (KafkaSource.builder()
    .set_bootstrap_servers("localhost:9092")
    .set_topics("events")
    .set_group_id("flink-processor")
    .set_starting_offsets(KafkaOffsetsInitializer.earliest())
    .set_value_only_deserializer(SimpleStringSchema())
    .build())

watermark = (WatermarkStrategy
    .for_bounded_out_of_orderness(Duration.of_seconds(5))
    .with_timestamp_assigner(lambda e, _: json.loads(e)["timestamp_ms"]))

ds = env.from_source(source, watermark, "kafka-source")
(ds.map(lambda raw: json.loads(raw))
   .key_by(lambda e: e["user_id"])
   .window(TumblingEventTimeWindows.of(Time.minutes(5)))
   .reduce(lambda a, b: {
       "user_id": a["user_id"],
       "event_count": a.get("event_count", 1) + b.get("event_count", 1),
       "total_value": a.get("total_value", 0) + b.get("total_value", 0),
   }).print())
env.execute("event-aggregation")
```

## Spark Structured Streaming

```python
# spark_stream.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, sum as spark_sum, count
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

spark = SparkSession.builder.appName("streaming-agg").getOrCreate()
schema = StructType([
    StructField("user_id", StringType()), StructField("amount", DoubleType()),
    StructField("event_time", TimestampType()),
])

raw = (spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "transactions").load())
parsed = raw.select(from_json(col("value").cast("string"), schema).alias("d")).select("d.*")

windowed = (parsed
    .withWatermark("event_time", "10 minutes")
    .groupBy(window(col("event_time"), "5 minutes", "1 minute"), col("user_id"))
    .agg(spark_sum("amount").alias("total"), count("*").alias("cnt")))

def write_to_db(batch_df, batch_id):
    (batch_df.write.format("jdbc")
     .option("url", "jdbc:postgresql://localhost:5432/analytics")
     .option("dbtable", "windowed_agg").mode("append").save())

query = (windowed.writeStream.foreachBatch(write_to_db)
    .option("checkpointLocation", "/tmp/checkpoints/txn")
    .outputMode("update").start())
query.awaitTermination()
```

## Windowing Patterns

| Window Type | Behavior | Use Case |
|-------------|----------|----------|
| Tumbling | Fixed, non-overlapping | Hourly metrics, daily rollups |
| Sliding | Fixed, overlapping | Moving averages, trend detection |
| Session | Gap-based, variable size | User activity sessions |
| Global | Single window per key | Accumulate until trigger fires |

## Exactly-Once Semantics Comparison

| Framework | Mechanism | Overhead |
|-----------|-----------|----------|
| Kafka Transactions | Txn producer + consumer offsets in txn | Low (~5%) |
| Flink | Distributed snapshots (Chandy-Lamport) | Medium |
| Spark Streaming | WAL + idempotent sinks + checkpoints | Medium |
| Faust | Kafka transactions (changelog topics) | Low |

## State Management and Checkpointing

```python
# Flink checkpoint config
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.checkpointing_mode import CheckpointingMode

env = StreamExecutionEnvironment.get_execution_environment()
env.enable_checkpointing(60000, CheckpointingMode.EXACTLY_ONCE)
env.get_checkpoint_config().set_min_pause_between_checkpoints(30000)
env.get_checkpoint_config().set_checkpoint_timeout(120000)
env.get_checkpoint_config().set_max_concurrent_checkpoints(1)
env.set_state_backend("rocksdb")  # disk-backed, supports TBs of state
```

## Gotchas

- **Consumer lag monitoring** -- track `kafka_consumer_group_lag`; unbounded lag means processing cannot keep up
- **Watermark stalls** -- idle partitions prevent watermark advancement; configure idle source timeout
- **Checkpoint size growth** -- large state slows checkpoints; use incremental checkpoints with RocksDB
- **Spark micro-batch latency** -- minimum ~100ms per batch; not suitable for sub-second requirements
- **Kafka rebalancing storms** -- frequent consumer joins/leaves trigger rebalances; use static group membership
- **Serialization costs** -- Avro/Protobuf with schema registry beats JSON by 5-10x in throughput
- **Out-of-order data** -- always set watermarks; late data beyond watermark is silently dropped
- **foreachBatch idempotency** -- Spark may re-execute a batch on failure; sink must handle duplicates
- **Faust is single-process** -- scale by running multiple instances with same app name
- **Transaction timeout** -- Kafka default `transaction.timeout.ms` is 60s; long processing needs higher values
