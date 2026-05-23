---
name: Kafka Streaming
description: Comprehensive guide to Apache Kafka for real-time data streaming including topics, producers, consumers, stream processing, and production best practices
---

# Kafka Streaming

## What is Kafka?

**Apache Kafka:** Distributed event streaming platform for high-throughput, fault-tolerant, real-time data pipelines.

### Core Concepts
```
Producer → Topic (Partitions) → Consumer

Producer: Writes events
Topic: Category of events
Partition: Ordered log within topic
Consumer: Reads events
```

### Use Cases
- **Event streaming:** User clicks, transactions
- **Log aggregation:** Application logs
- **Metrics collection:** System metrics
- **Data integration:** CDC, ETL pipelines
- **Messaging:** Microservices communication

---

## Architecture

### Components
```
Producers → Kafka Cluster (Brokers) → Consumers
                ↓
            ZooKeeper (metadata)
```

**Broker:** Kafka server (node in cluster)
**ZooKeeper:** Coordination service (being replaced by KRaft)
**Topic:** Logical channel for events
**Partition:** Physical log file
**Consumer Group:** Set of consumers working together

---

## Topics and Partitions

### Topic
```
Topic: "user-events"
Partitions: 3

Partition 0: [event1, event4, event7, ...]
Partition 1: [event2, event5, event8, ...]
Partition 2: [event3, event6, event9, ...]
```

### Partitioning Strategy
```python
# Key-based partitioning (same key → same partition)
producer.send('user-events', key='user123', value=event)

# Round-robin (no key)
producer.send('user-events', value=event)

# Custom partitioner
class CustomPartitioner:
    def partition(self, key, all_partitions):
        return hash(key) % len(all_partitions)
```

### Why Partitions?
- **Parallelism:** Multiple consumers read simultaneously
- **Scalability:** Add partitions to increase throughput
- **Ordering:** Events with same key stay in order

---

## Producers

### Basic Producer (Python)
```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8') if k else None
)

# Send event
event = {
    'user_id': '123',
    'action': 'click',
    'timestamp': '2024-01-15T10:00:00Z'
}

future = producer.send(
    topic='user-events',
    key='user123',
    value=event
)

# Wait for confirmation
record_metadata = future.get(timeout=10)
print(f"Sent to partition {record_metadata.partition} at offset {record_metadata.offset}")

producer.close()
```

### Producer Configuration
```python
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    
    # Serialization
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    
    # Acknowledgments (reliability)
    acks='all',  # Wait for all replicas (most reliable)
    # acks=1     # Wait for leader only
    # acks=0     # Don't wait (fastest, least reliable)
    
    # Retries
    retries=3,
    
    # Batching (performance)
    batch_size=16384,  # 16KB
    linger_ms=10,      # Wait 10ms to batch
    
    # Compression
    compression_type='gzip',  # or 'snappy', 'lz4', 'zstd'
    
    # Idempotence (exactly-once)
    enable_idempotence=True
)
```

---

## Consumers

### Basic Consumer (Python)
```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers=['localhost:9092'],
    group_id='analytics-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',  # Start from beginning
    enable_auto_commit=True
)

for message in consumer:
    event = message.value
    print(f"Received: {event}")
    
    # Process event
    process_event(event)

consumer.close()
```

### Consumer Groups
```
Topic: user-events (3 partitions)
Consumer Group: analytics-group (3 consumers)

Consumer 1 → Partition 0
Consumer 2 → Partition 1
Consumer 3 → Partition 2

Each partition consumed by exactly one consumer in group
```

### Offset Management
```python
# Auto-commit (default)
consumer = KafkaConsumer(
    'user-events',
    enable_auto_commit=True,
    auto_commit_interval_ms=5000  # Commit every 5 seconds
)

# Manual commit
consumer = KafkaConsumer(
    'user-events',
    enable_auto_commit=False
)

for message in consumer:
    process_event(message.value)
    consumer.commit()  # Commit after processing
```

---

## Stream Processing

### Kafka Streams (Java)
```java
StreamsBuilder builder = new StreamsBuilder();

KStream<String, String> source = builder.stream("user-events");

// Filter
KStream<String, String> filtered = source.filter(
    (key, value) -> value.contains("click")
);

// Map
KStream<String, String> mapped = source.mapValues(
    value -> value.toUpperCase()
);

// Aggregate
KTable<String, Long> counts = source
    .groupByKey()
    .count();

// Join
KStream<String, String> joined = stream1.join(
    stream2,
    (value1, value2) -> value1 + value2,
    JoinWindows.of(Duration.ofMinutes(5))
);

// Output
filtered.to("filtered-events");
```

### ksqlDB (SQL for Kafka)
```sql
-- Create stream
CREATE STREAM user_events (
    user_id VARCHAR,
    action VARCHAR,
    timestamp BIGINT
) WITH (
    KAFKA_TOPIC='user-events',
    VALUE_FORMAT='JSON'
);

-- Filter
CREATE STREAM click_events AS
SELECT * FROM user_events
WHERE action = 'click';

-- Aggregate
CREATE TABLE user_click_counts AS
SELECT user_id, COUNT(*) as click_count
FROM click_events
GROUP BY user_id;

-- Join
CREATE STREAM enriched_events AS
SELECT
    e.user_id,
    e.action,
    u.name,
    u.email
FROM user_events e
LEFT JOIN users u ON e.user_id = u.user_id;
```

---

## Schemas and Serialization

### Avro with Schema Registry
```python
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

# Define schema
value_schema = avro.loads('''
{
    "type": "record",
    "name": "UserEvent",
    "fields": [
        {"name": "user_id", "type": "string"},
        {"name": "action", "type": "string"},
        {"name": "timestamp", "type": "long"}
    ]
}
''')

# Producer with schema
producer = AvroProducer({
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://localhost:8081'
}, default_value_schema=value_schema)

# Send event
event = {
    'user_id': '123',
    'action': 'click',
    'timestamp': 1705315200000
}

producer.produce(topic='user-events', value=event)
producer.flush()
```

---

## Exactly-Once Semantics

### Producer Idempotence
```python
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    enable_idempotence=True,  # Prevents duplicates
    acks='all',
    retries=3
)
```

### Transactions
```python
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    transactional_id='my-transactional-id',
    enable_idempotence=True
)

producer.init_transactions()

try:
    producer.begin_transaction()
    
    # Send multiple messages atomically
    producer.send('topic1', value=event1)
    producer.send('topic2', value=event2)
    
    producer.commit_transaction()
except Exception as e:
    producer.abort_transaction()
```

---

## Monitoring and Operations

### Key Metrics
```
Throughput:
- Messages/sec
- Bytes/sec

Latency:
- Producer latency
- End-to-end latency

Consumer Lag:
- How far behind consumers are
- Critical metric!

Broker Metrics:
- CPU, memory, disk usage
- Network throughput
```

### Consumer Lag
```bash
# Check consumer lag
kafka-consumer-groups --bootstrap-server localhost:9092 \
  --group analytics-group --describe

# Output:
# TOPIC         PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
# user-events   0          1000            1500            500
# user-events   1          2000            2100            100
```

---

## Best Practices

### 1. Choose Partition Count Carefully
```
Too few: Limited parallelism
Too many: Overhead

Rule of thumb: 
- Start with 3-6 partitions
- Increase based on throughput needs
- Consider: partitions = max(consumers, throughput/target_per_partition)
```

### 2. Use Appropriate Replication Factor
```
Replication factor = 3 (recommended)

Provides:
- Fault tolerance (2 brokers can fail)
- High availability
- Data durability
```

### 3. Monitor Consumer Lag
```
Alert if lag > threshold
Indicates:
- Slow consumers
- Insufficient consumers
- Processing issues
```

### 4. Use Schema Registry
```
Benefits:
- Schema evolution
- Backward compatibility
- Type safety
```

### 5. Tune Batch Size and Linger
```python
# For throughput
producer = KafkaProducer(
    batch_size=32768,  # 32KB
    linger_ms=100      # Wait 100ms
)

# For latency
producer = KafkaProducer(
    batch_size=1,
    linger_ms=0
)
```

---

## Common Patterns

### Event Sourcing
```
Store all state changes as events
Rebuild state by replaying events

Example:
- user.created
- user.updated
- user.deleted

Replay → Current user state
```

### CDC (Change Data Capture)
```
Capture database changes → Kafka

Tools:
- Debezium (MySQL, PostgreSQL, MongoDB)
- Maxwell (MySQL)
- Kafka Connect

Flow:
Database → CDC → Kafka → Consumers
```

### CQRS (Command Query Responsibility Segregation)
```
Write model: Commands → Kafka → Write DB
Read model: Events → Kafka → Read DB (denormalized)

Benefits:
- Optimized for reads and writes separately
- Scalability
```

---

## Kafka Connect

### Source Connector (Database → Kafka)
```json
{
  "name": "mysql-source",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "database.hostname": "localhost",
    "database.port": "3306",
    "database.user": "debezium",
    "database.password": "dbz",
    "database.server.id": "184054",
    "database.server.name": "mysql",
    "table.include.list": "inventory.customers",
    "database.history.kafka.bootstrap.servers": "kafka:9092",
    "database.history.kafka.topic": "schema-changes.inventory"
  }
}
```

### Sink Connector (Kafka → Database)
```json
{
  "name": "postgres-sink",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "connection.url": "jdbc:postgresql://localhost:5432/analytics",
    "connection.user": "postgres",
    "connection.password": "password",
    "topics": "user-events",
    "auto.create": "true",
    "insert.mode": "upsert",
    "pk.mode": "record_key"
  }
}
```

---

## Summary

**Kafka:** Distributed event streaming platform

**Core Concepts:**
- Topics: Logical channels
- Partitions: Physical logs (parallelism)
- Producers: Write events
- Consumers: Read events
- Consumer Groups: Parallel processing

**Guarantees:**
- At-least-once (default)
- Exactly-once (with idempotence + transactions)

**Stream Processing:**
- Kafka Streams (Java)
- ksqlDB (SQL)

**Best Practices:**
- Choose partition count carefully
- Replication factor = 3
- Monitor consumer lag
- Use schema registry
- Tune batch size and linger

**Common Patterns:**
- Event sourcing
- CDC
- CQRS

**Tools:**
- Kafka Connect (integrations)
- Schema Registry (Avro schemas)
- ksqlDB (SQL queries)
