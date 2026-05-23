---
name: kafka-event-driven
description: Expert guidance for building event-driven architectures with Apache Kafka from hello-world prototypes to production-ready systems. Use when working with (1) Kafka producers and consumers, (2) Event streaming and stream processing with Kafka Streams, (3) Data integration with Kafka Connect, (4) Cluster setup and operations, (5) Production deployment and monitoring, (6) Schema management and data contracts, (7) Performance tuning and fault tolerance. Covers Java, Python, Node.js implementations.
---

# Apache Kafka Event-Driven Architecture

Build scalable event-driven systems with Apache Kafka - from local development to production deployment.

## Core Concepts

### Event Streaming Platform

Kafka is a distributed event streaming platform with three core capabilities:

1. **Publish and Subscribe** - Read and write streams of events (records)
2. **Store** - Durably store event streams with fault tolerance
3. **Process** - Process event streams in real-time or retrospectively

### Key Components

- **Producers** - Applications that publish events to topics
- **Consumers** - Applications that subscribe to topics and process events
- **Brokers** - Kafka servers that store and serve data
- **Topics** - Named event streams organized into partitions
- **Partitions** - Ordered, immutable sequences of events within a topic
- **Consumer Groups** - Load-balanced consumption across multiple consumers
- **Replication** - Data redundancy across brokers for fault tolerance

## Quick Start Workflows

### 1. Hello World - Local Setup

**Start Kafka with Docker:**

```bash
# Pull and run Apache Kafka (includes KRaft - no Zookeeper needed)
docker pull apache/kafka:latest
docker run -p 9092:9092 apache/kafka:latest
```

**Create a topic:**

```bash
# Using Kafka CLI tools (if installed locally)
bin/kafka-topics.sh --bootstrap-server localhost:9092 \
  --create --topic hello-world \
  --partitions 3 --replication-factor 1

# Using Docker
docker exec <container-id> /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create --topic hello-world \
  --partitions 3 --replication-factor 1
```

**Produce messages:**

```bash
bin/kafka-console-producer.sh --topic hello-world \
  --bootstrap-server localhost:9092
```

**Consume messages:**

```bash
bin/kafka-console-consumer.sh --topic hello-world \
  --from-beginning --bootstrap-server localhost:9092
```

### 2. Basic Producer (Java)

See `scripts/simple_producer.java` for a complete working example.

Key configuration:

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("acks", "all"); // Wait for all replicas
props.put("retries", 3); // Retry on transient errors

KafkaProducer<String, String> producer = new KafkaProducer<>(props);
```

### 3. Basic Consumer (Java)

See `scripts/simple_consumer.java` for a complete working example.

Key configuration:

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("group.id", "my-consumer-group");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("enable.auto.commit", "false"); // Manual offset management
props.put("auto.offset.reset", "earliest"); // Start from beginning if no offset

consumer.subscribe(Collections.singletonList("my-topic"));
```

## Advanced Patterns

### Stream Processing with Kafka Streams

For stateful stream processing, windowing, joins, and aggregations, see:
- **Reference**: [STREAMS_GUIDE.md](references/STREAMS_GUIDE.md)
- **Script**: `scripts/word_count_streams.java`

**When to use Kafka Streams:**
- Real-time aggregations and analytics
- Stream enrichment via joins (stream-stream, stream-table)
- Windowed computations (tumbling, hopping, sliding)
- Stateful transformations requiring local state stores

### Data Integration with Kafka Connect

For integrating Kafka with databases, file systems, and external systems, see:
- **Reference**: [CONNECT_GUIDE.md](references/CONNECT_GUIDE.md)
- **Script**: `scripts/source_connector.java`

**When to use Kafka Connect:**
- Import data from databases (CDC patterns)
- Export Kafka data to data warehouses
- File-based integrations
- Managed, scalable data pipelines without custom code

### Transactions and Exactly-Once Semantics

For mission-critical applications requiring strong guarantees:

```java
// Producer configuration
props.put("enable.idempotence", true);
props.put("transactional.id", "my-transactional-producer-1");

producer.initTransactions();

try {
    producer.beginTransaction();
    producer.send(record1);
    producer.send(record2);
    producer.commitTransaction();
} catch (Exception e) {
    producer.abortTransaction();
}
```

See `scripts/transactional_producer.java` for complete implementation.

## Production Deployment

### Topic Configuration

**Critical settings for production topics:**

```bash
# Create topic with production settings
kafka-topics.sh --bootstrap-server localhost:9092 --create \
  --topic production-events \
  --partitions 12 \
  --replication-factor 3 \
  --config min.insync.replicas=2 \
  --config retention.ms=604800000 \  # 7 days
  --config compression.type=lz4
```

**Key parameters:**
- `partitions` - Parallelism (more = higher throughput)
- `replication-factor` - Data redundancy (typically 3)
- `min.insync.replicas` - Minimum replicas for writes (typically 2)
- `retention.ms` - How long to keep data
- `compression.type` - Compression algorithm (lz4, snappy, gzip, zstd)

### Producer Configuration for Production

```java
props.put("acks", "all"); // Wait for all in-sync replicas
props.put("retries", Integer.MAX_VALUE); // Retry indefinitely
props.put("max.in.flight.requests.per.connection", 5);
props.put("enable.idempotence", true); // Prevent duplicates
props.put("compression.type", "lz4"); // Compress messages
props.put("batch.size", 32768); // Batch size in bytes
props.put("linger.ms", 10); // Wait time for batching
props.put("buffer.memory", 67108864); // 64MB buffer
```

### Consumer Configuration for Production

```java
props.put("enable.auto.commit", false); // Manual commit control
props.put("max.poll.records", 500); // Records per poll
props.put("max.poll.interval.ms", 300000); // 5 minutes
props.put("session.timeout.ms", 10000); // 10 seconds
props.put("heartbeat.interval.ms", 3000); // 3 seconds
props.put("fetch.min.bytes", 1024); // Minimum fetch size
props.put("fetch.max.wait.ms", 500); // Max wait for fetch
```

### Monitoring and Observability

See [OPERATIONS_GUIDE.md](references/OPERATIONS_GUIDE.md) for comprehensive monitoring setup.

**Key metrics to monitor:**
- **Producer**: `record-send-rate`, `request-latency-avg`, `record-error-rate`
- **Consumer**: `records-consumed-rate`, `records-lag-max`, `commit-latency-avg`
- **Broker**: `under-replicated-partitions`, `offline-partitions-count`, `request-queue-size`

### Security Configuration

For SSL/TLS and SASL authentication:

```java
// SSL configuration
props.put("security.protocol", "SSL");
props.put("ssl.truststore.location", "/path/to/truststore.jks");
props.put("ssl.truststore.password", "password");
props.put("ssl.keystore.location", "/path/to/keystore.jks");
props.put("ssl.keystore.password", "password");

// SASL/PLAIN configuration
props.put("security.protocol", "SASL_SSL");
props.put("sasl.mechanism", "PLAIN");
props.put("sasl.jaas.config",
    "org.apache.kafka.common.security.plain.PlainLoginModule required " +
    "username=\"admin\" password=\"secret\";");
```

## Schema Management

For data contracts and schema evolution, see:
- **Reference**: [SCHEMA_MANAGEMENT.md](references/SCHEMA_MANAGEMENT.md)

**Schema Registry integration** (when using Confluent Schema Registry):

```java
// Avro producer
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("schema.registry.url", "http://localhost:8081");
```

## Architecture Decision Guide

### Choosing Number of Partitions

**Factors to consider:**
- Target throughput (more partitions = higher throughput)
- Number of consumers in consumer group (max parallelism)
- File handles per broker (more partitions = more file descriptors)

**Rule of thumb:** Start with `max(target_throughput / partition_throughput, num_consumers)`

### Consumer Group vs. Independent Consumers

**Use Consumer Groups when:**
- You need load balancing across multiple instances
- Each message should be processed once by the group
- You want automatic partition rebalancing

**Use Independent Consumers when:**
- Each consumer needs to process all messages
- You need broadcast semantics
- You want manual partition assignment

### Kafka Streams vs. Custom Consumer

**Use Kafka Streams when:**
- You need stateful processing (aggregations, joins, windowing)
- You want built-in fault tolerance and state management
- Processing logic is complex with multiple transformations

**Use Custom Consumer when:**
- Simple message-by-message processing
- Integration with non-Kafka systems
- Fine-grained control over consumption logic

## Error Handling Patterns

### Producer Error Handling

```java
producer.send(record, (metadata, exception) -> {
    if (exception != null) {
        if (exception instanceof RetriableException) {
            // Automatic retry by producer
            logger.warn("Retriable error: {}", exception.getMessage());
        } else {
            // Non-retriable - handle explicitly
            logger.error("Failed to send: {}", exception.getMessage());
            // Dead letter queue, alert, etc.
        }
    } else {
        logger.info("Sent to partition {} offset {}",
            metadata.partition(), metadata.offset());
    }
});
```

### Consumer Error Handling

```java
while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));

    for (ConsumerRecord<String, String> record : records) {
        try {
            processRecord(record);
        } catch (TransientException e) {
            // Retry with backoff
            retryWithBackoff(record);
        } catch (PermanentException e) {
            // Send to DLQ
            sendToDeadLetterQueue(record, e);
        }
    }

    consumer.commitSync(); // Commit after successful processing
}
```

## Multi-Language Support

### Python

See `scripts/python_producer.py` and `scripts/python_consumer.py` for working examples using `confluent-kafka-python`.

**Quick start:**

```python
from confluent_kafka import Producer, Consumer

# Producer
producer = Producer({'bootstrap.servers': 'localhost:9092'})
producer.produce('topic', key='key', value='value')
producer.flush()

# Consumer
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['topic'])

while True:
    msg = consumer.poll(1.0)
    if msg and not msg.error():
        print(f'Received: {msg.value().decode("utf-8")}')
```

### Node.js

See `scripts/nodejs_producer.js` and `scripts/nodejs_consumer.js` for working examples using `kafkajs`.

**Quick start:**

```javascript
const { Kafka } = require('kafkajs');

const kafka = new Kafka({ brokers: ['localhost:9092'] });

// Producer
const producer = kafka.producer();
await producer.connect();
await producer.send({
  topic: 'topic',
  messages: [{ key: 'key', value: 'value' }]
});

// Consumer
const consumer = kafka.consumer({ groupId: 'my-group' });
await consumer.connect();
await consumer.subscribe({ topic: 'topic' });
await consumer.run({
  eachMessage: async ({ message }) => {
    console.log(message.value.toString());
  }
});
```

## Common Patterns and Anti-Patterns

### ✅ Best Practices

1. **Always set `acks=all`** for producers in production
2. **Use consumer groups** for scalable consumption
3. **Disable auto-commit** for at-least-once or exactly-once semantics
4. **Set appropriate `retention.ms`** based on replay requirements
5. **Monitor consumer lag** to detect processing bottlenecks
6. **Use compression** (`lz4` or `snappy`) to reduce network bandwidth
7. **Configure `min.insync.replicas=2`** with `replication-factor=3`

### ❌ Anti-Patterns

1. **Creating too many topics** - Use partitions for parallelism, not topics
2. **Small batch sizes** - Reduces throughput; increase `batch.size` and `linger.ms`
3. **Synchronous sends** without batching - Kills performance
4. **Auto-commit without error handling** - Can lead to message loss
5. **Not monitoring consumer lag** - Silent degradation
6. **Single partition topics** - No parallelism or load balancing
7. **Hardcoding broker addresses** - Use DNS or service discovery

## Troubleshooting

### Producer Issues

**Slow throughput:**
- Increase `batch.size` and `linger.ms`
- Enable compression
- Check network latency to brokers
- Increase `buffer.memory`

**Messages not arriving:**
- Check producer error callbacks
- Verify topic exists and is accessible
- Check broker logs for errors
- Verify `acks` configuration

### Consumer Issues

**High lag:**
- Increase consumer instances (up to partition count)
- Optimize processing logic
- Increase `max.poll.records` if processing is fast
- Check for rebalancing issues

**Rebalancing storms:**
- Increase `max.poll.interval.ms`
- Reduce processing time per batch
- Decrease `max.poll.records`
- Check session timeout settings

## Reference Files

For detailed implementation guidance:

- **[STREAMS_GUIDE.md](references/STREAMS_GUIDE.md)** - Kafka Streams API, windowing, joins, state stores
- **[CONNECT_GUIDE.md](references/CONNECT_GUIDE.md)** - Kafka Connect, source/sink connectors, REST API
- **[OPERATIONS_GUIDE.md](references/OPERATIONS_GUIDE.md)** - Production deployment, monitoring, disaster recovery
- **[SCHEMA_MANAGEMENT.md](references/SCHEMA_MANAGEMENT.md)** - Schema Registry, Avro, schema evolution

## Script Directory

All scripts are tested and ready to use:

- `simple_producer.java` - Basic producer with error handling
- `simple_consumer.java` - Basic consumer with manual commit
- `transactional_producer.java` - Exactly-once semantics
- `word_count_streams.java` - Kafka Streams word count
- `source_connector.java` - Custom Kafka Connect source connector
- `python_producer.py` - Python producer example
- `python_consumer.py` - Python consumer example
- `nodejs_producer.js` - Node.js producer example
- `nodejs_consumer.js` - Node.js consumer example
