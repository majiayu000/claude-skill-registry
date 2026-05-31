---
name: streaming-data
description: Build event streaming and real-time data pipelines with Kafka, Pulsar, Redpanda, Flink, and Spark. Covers producer/consumer patterns, stream processing, event sourcing, and CDC across TypeScript, Python, Go, and Java. When building real-time systems, microservices communication, or data integration pipelines.
---

# Streaming Data Processing

Build production-ready event streaming systems and real-time data pipelines using modern message brokers and stream processors.

## When to Use This Skill

Use this skill when:
- Building event-driven architectures and microservices communication
- Processing real-time analytics, monitoring, or alerting systems
- Implementing data integration pipelines (CDC, ETL/ELT)
- Creating log or metrics aggregation systems
- Developing IoT platforms or high-frequency trading systems

## Core Concepts

### Message Brokers vs Stream Processors

**Message Brokers** (Kafka, Pulsar, Redpanda):
- Store and distribute event streams
- Provide durability, replay capability, partitioning
- Handle producer/consumer coordination

**Stream Processors** (Flink, Spark, Kafka Streams):
- Transform and aggregate streaming data
- Provide windowing, joins, stateful operations
- Execute complex event processing (CEP)

### Delivery Guarantees

**At-Most-Once**:
- Messages may be lost, no duplicates
- Lowest overhead
- Use for: Metrics, logs where loss is acceptable

**At-Least-Once**:
- Messages never lost, may have duplicates
- Moderate overhead, requires idempotent consumers
- Use for: Most applications (default choice)

**Exactly-Once**:
- Messages never lost or duplicated
- Highest overhead, requires transactional processing
- Use for: Financial transactions, critical state updates

## Quick Start Guide

### Step 1: Choose a Message Broker

See references/broker-selection.md for detailed comparison.

**Quick decision**:
- **Apache Kafka**: Mature ecosystem, enterprise features, event sourcing
- **Redpanda**: Low latency, Kafka-compatible, simpler operations (no ZooKeeper)
- **Apache Pulsar**: Multi-tenancy, geo-replication, tiered storage
- **RabbitMQ**: Traditional message queues, RPC patterns

### Step 2: Choose a Stream Processor (if needed)

See references/processor-selection.md for detailed comparison.

**Quick decision**:
- **Apache Flink**: Millisecond latency, real-time analytics, CEP
- **Apache Spark**: Batch + stream hybrid, ML integration, analytics
- **Kafka Streams**: Embedded in microservices, no separate cluster
- **ksqlDB**: SQL interface for stream processing

### Step 3: Implement Producer/Consumer Patterns

Choose language-specific guide:
- TypeScript/Node.js: references/typescript-patterns.md (KafkaJS)
- Python: references/python-patterns.md (confluent-kafka-python)
- Go: references/go-patterns.md (kafka-go)
- Java/Scala: references/java-patterns.md (Apache Kafka Java Client)

## Common Patterns

### Basic Producer Pattern

Send events to a topic with error handling:

```
1. Create producer with broker addresses
2. Configure delivery guarantees (acks, retries, idempotence)
3. Send messages with key (for partitioning) and value
4. Handle delivery callbacks or errors
5. Flush and close producer on shutdown
```

### Basic Consumer Pattern

Process events from topics with offset management:

```
1. Create consumer with broker addresses and group ID
2. Subscribe to topics
3. Poll for messages
4. Process each message
5. Commit offsets (auto or manual)
6. Handle errors (retry, DLQ, skip)
7. Close consumer gracefully
```

### Error Handling Strategy

For production systems, implement:
- **Dead Letter Queue (DLQ)**: Send failed messages to separate topic
- **Retry Logic**: Configurable retry attempts with backoff
- **Graceful Shutdown**: Finish processing, commit offsets, close connections
- **Monitoring**: Track consumer lag, error rates, throughput

## Decision Frameworks

### Framework: Message Broker Selection

```
START: What are requirements?

1. Need Kafka API compatibility?
   YES → Kafka or Redpanda
   NO → Continue

2. Is multi-tenancy critical?
   YES → Apache Pulsar
   NO → Continue

3. Operational simplicity priority?
   YES → Redpanda (single binary, no ZooKeeper)
   NO → Continue

4. Mature ecosystem needed?
   YES → Apache Kafka
   NO → Redpanda (better performance)

5. Task queues (not event streams)?
   YES → RabbitMQ or message-queues skill
   NO → Kafka/Redpanda/Pulsar
```

### Framework: Stream Processor Selection

```
START: What is latency requirement?

1. Millisecond-level latency needed?
   YES → Apache Flink
   NO → Continue

2. Batch + stream in same pipeline?
   YES → Apache Spark Streaming
   NO → Continue

3. Embedded in microservice?
   YES → Kafka Streams
   NO → Continue

4. SQL interface for analysts?
   YES → ksqlDB
   NO → Flink or Spark

5. Python primary language?
   YES → Spark (PySpark) or Faust
   NO → Flink (Java/Scala)
```

### Framework: Language Selection

**TypeScript/Node.js**:
- API gateways, web services, real-time dashboards
- KafkaJS library (827 code snippets, high reputation)

**Python**:
- Data science, ML pipelines, analytics
- confluent-kafka-python (192 snippets, score 68.8)

**Go**:
- High-performance microservices, infrastructure tools
- kafka-go (42 snippets, idiomatic Go)

**Java/Scala**:
- Enterprise applications, Kafka Streams, Flink, Spark
- Apache Kafka Java Client (683 snippets, score 76.9)

## Advanced Patterns

### Event Sourcing

Store state changes as immutable events. See references/event-sourcing.md for:
- Event store design patterns
- Event schema evolution
- Snapshot strategies
- Temporal queries and audit trails

### Change Data Capture (CDC)

Capture database changes as events. See references/cdc-patterns.md for:
- Debezium integration (MySQL, PostgreSQL, MongoDB)
- Real-time data synchronization
- Microservices data integration patterns

### Exactly-Once Processing

Implement transactional guarantees. See references/exactly-once.md for:
- Idempotent producers
- Transactional consumers
- End-to-end exactly-once pipelines

### Error Handling

Production-grade error management. See references/error-handling.md for:
- Dead letter queue patterns
- Retry strategies with exponential backoff
- Backpressure handling
- Circuit breakers for downstream failures

## Reference Files

### Decision Guides
- references/broker-selection.md - Kafka vs Pulsar vs Redpanda comparison
- references/processor-selection.md - Flink vs Spark vs Kafka Streams
- references/delivery-guarantees.md - At-least-once, exactly-once patterns

### Language-Specific Implementation
- references/typescript-patterns.md - KafkaJS patterns (producer, consumer, error handling)
- references/python-patterns.md - confluent-kafka-python patterns
- references/go-patterns.md - kafka-go patterns
- references/java-patterns.md - Apache Kafka Java client patterns

### Advanced Topics
- references/event-sourcing.md - Event sourcing architecture
- references/cdc-patterns.md - Change Data Capture with Debezium
- references/exactly-once.md - Transactional processing
- references/error-handling.md - DLQ, retries, backpressure
- references/performance-tuning.md - Throughput optimization, partitioning strategies

## Validation Scripts

Run these scripts for token-free validation and generation:

### Validate Kafka Configuration
```bash
python scripts/validate-kafka-config.py --config producer.yaml
python scripts/validate-kafka-config.py --config consumer.yaml
```

Checks: broker connectivity, configuration validity, serialization format

### Generate Schema Registry Templates
```bash
python scripts/generate-schema.py --type avro --entity User
python scripts/generate-schema.py --type protobuf --entity Event
```

Creates: Avro/Protobuf schema definitions for Schema Registry

### Benchmark Throughput
```bash
bash scripts/benchmark-throughput.sh --broker localhost:9092 --topic test
```

Tests: Producer/consumer throughput, latency percentiles

## Code Examples

### TypeScript Example (KafkaJS)

See examples/typescript/ for:
- basic-producer.ts - Simple event producer with error handling
- basic-consumer.ts - Consumer with manual offset commits
- transactional-producer.ts - Exactly-once producer pattern
- consumer-with-dlq.ts - Dead letter queue implementation

### Python Example (confluent-kafka-python)

See examples/python/ for:
- basic_producer.py - Producer with delivery callbacks
- basic_consumer.py - Consumer with error handling
- async_producer.py - AsyncIO producer (aiokafka)
- schema_registry.py - Avro serialization with Schema Registry

### Go Example (kafka-go)

See examples/go/ for:
- basic_producer.go - Idiomatic Go producer
- basic_consumer.go - Consumer with manual commits
- high_perf_consumer.go - Concurrent processing pattern
- batch_producer.go - Batch message sending

### Java Example (Apache Kafka)

See examples/java/ for:
- BasicProducer.java - Producer with idempotence
- BasicConsumer.java - Consumer with error recovery
- TransactionalProducer.java - Exactly-once transactions
- StreamsAggregation.java - Kafka Streams aggregation

## Technology Comparison

### Message Broker Comparison

| Feature | Kafka | Pulsar | Redpanda | RabbitMQ |
|---------|-------|--------|----------|----------|
| Throughput | Very High | High | Very High | Medium |
| Latency | Medium | Medium | Low | Low |
| Event Replay | Yes | Yes | Yes | No |
| Multi-Tenancy | Manual | Native | Manual | Manual |
| Operational Complexity | Medium | High | Low | Low |
| Best For | Enterprise, big data | SaaS, IoT | Performance-critical | Task queues |

### Stream Processor Comparison

| Feature | Flink | Spark | Kafka Streams | ksqlDB |
|---------|-------|-------|---------------|--------|
| Processing Model | True streaming | Micro-batch | Library | SQL engine |
| Latency | Millisecond | Second | Millisecond | Second |
| Deployment | Cluster | Cluster | Embedded | Server |
| Best For | Real-time analytics | Batch + stream | Microservices | Analysts |

### Client Library Recommendations

| Language | Library | Trust Score | Snippets | Use Case |
|----------|---------|-------------|----------|----------|
| TypeScript | KafkaJS | High | 827 | Web services, APIs |
| Python | confluent-kafka-python | High (68.8) | 192 | Data pipelines, ML |
| Go | kafka-go | High | 42 | High-perf services |
| Java | Kafka Java Client | High (76.9) | 683 | Enterprise, Flink/Spark |

## Related Skills

For authentication and security patterns, see the auth-security skill.
For infrastructure deployment (Kubernetes operators, Terraform), see the infrastructure-as-code skill.
For monitoring metrics and tracing, see the observability skill.
For API design patterns, see the api-design-principles skill.
For data architecture and warehousing, see the data-architecture skill.

## Troubleshooting

### Consumer Lag Issues
- Check partition count vs consumer count (match for parallelism)
- Increase consumer instances or reduce processing time
- Monitor with Kafka consumer lag metrics

### Message Loss
- Verify producer acks=all configuration
- Check broker replication factor (>1)
- Ensure consumers commit offsets after processing

### Duplicate Messages
- Implement idempotent consumers (track message IDs)
- Use exactly-once semantics (transactions)
- Design for at-least-once delivery

### Performance Bottlenecks
- Increase partition count for parallelism
- Tune batch size and linger time
- Enable compression (GZIP, LZ4, Snappy)
- See references/performance-tuning.md for details
