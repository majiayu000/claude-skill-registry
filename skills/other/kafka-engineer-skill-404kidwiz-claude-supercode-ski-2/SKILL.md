---
name: kafka-engineer
description: Expert in Apache Kafka, Event Streaming, and Real-time Data Pipelines. Specializes in Kafka Connect, KSQL, and Schema Registry.
---

# Kafka Engineer

## Purpose

Provides Apache Kafka and event streaming expertise specializing in scalable event-driven architectures and real-time data pipelines. Builds fault-tolerant streaming platforms with exactly-once processing, Kafka Connect, and Schema Registry management.

## When to Use

- Designing event-driven microservices architectures
- Setting up Kafka Connect pipelines (CDC, S3 Sink)
- Writing stream processing apps (Kafka Streams / ksqlDB)
- Debugging consumer lag, rebalancing storms, or broker performance
- Designing schemas (Avro/Protobuf) with Schema Registry
- Configuring ACLs and mTLS security

---
---

## 2. Decision Framework

### Architecture Selection

```
What is the use case?
│
├─ **Data Integration (ETL)**
│  ├─ DB to DB/Data Lake? → **Kafka Connect** (Zero code)
│  └─ Complex transformations? → **Kafka Streams**
│
├─ **Real-Time Analytics**
│  ├─ SQL-like queries? → **ksqlDB** (Quick aggregation)
│  └─ Complex stateful logic? → **Kafka Streams / Flink**
│
└─ **Microservices Comm**
   ├─ Event Notification? → **Standard Producer/Consumer**
   └─ Event Sourcing? → **State Stores (RocksDB)**
```

### Config Tuning (The "Big 3")

1.  **Throughput:** `batch.size`, `linger.ms`, `compression.type=lz4`.
2.  **Latency:** `linger.ms=0`, `acks=1`.
3.  **Durability:** `acks=all`, `min.insync.replicas=2`, `replication.factor=3`.

**Red Flags → Escalate to `sre-engineer`:**
- "Unclean leader election" enabled (Data loss risk)
- Zookeeper dependency in new clusters (Use KRaft mode)
- Disk usage > 80% on brokers
- Consumer lag constantly increasing (Capacity mismatch)

---
---

## 3. Core Workflows

### Workflow 1: Kafka Connect (CDC)

**Goal:** Stream changes from PostgreSQL to S3.

**Steps:**

1.  **Source Config (`postgres-source.json`)**
    ```json
    {
      "name": "postgres-source",
      "config": {
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "database.hostname": "db-host",
        "database.dbname": "mydb",
        "database.user": "kafka",
        "plugin.name": "pgoutput"
      }
    }
    ```

2.  **Sink Config (`s3-sink.json`)**
    ```json
    {
      "name": "s3-sink",
      "config": {
        "connector.class": "io.confluent.connect.s3.S3SinkConnector",
        "s3.bucket.name": "my-datalake",
        "format.class": "io.confluent.connect.s3.format.parquet.ParquetFormat",
        "flush.size": "1000"
      }
    }
    ```

3.  **Deploy**
    -   `curl -X POST -d @postgres-source.json http://connect:8083/connectors`

---
---

### Workflow 3: Schema Registry Integration

**Goal:** Enforce schema compatibility.

**Steps:**

1.  **Define Schema (`user.avsc`)**
    ```json
    {
      "type": "record",
      "name": "User",
      "fields": [
        {"name": "id", "type": "int"},
        {"name": "name", "type": "string"}
      ]
    }
    ```

2.  **Producer (Java)**
    -   Use `KafkaAvroSerializer`.
    -   Registry URL: `http://schema-registry:8081`.

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: Large Messages

**What it looks like:**
-   Sending 10MB images payload in Kafka message.

**Why it fails:**
-   Kafka is optimized for small messages (< 1MB). Large messages block the broker threads.

**Correct approach:**
-   Store image in **S3**.
-   Send **Reference URL** in Kafka message.

### ❌ Anti-Pattern 2: Too Many Partitions

**What it looks like:**
-   Creating 10,000 partitions on a small cluster.

**Why it fails:**
-   Slow leader election (Zookeeper overhead).
-   High file handle usage.

**Correct approach:**
-   Limit partitions per broker (~4000). Use fewer topics or larger clusters.

### ❌ Anti-Pattern 3: Blocking Consumer

**What it looks like:**
-   Consumer doing heavy HTTP call (30s) for each message.

**Why it fails:**
-   Rebalance storm (Consumer leaves group due to timeout).

**Correct approach:**
-   **Async Processing:** Move work to a thread pool.
-   **Pause/Resume:** `consumer.pause()` if buffer is full.

---
---

## 7. Quality Checklist

**Configuration:**
-   [ ] **Replication:** Factor 3 for production.
-   [ ] **Min.ISR:** 2 (Prevents data loss).
-   [ ] **Retention:** Configured correctly (Time vs Size).

**Observability:**
-   [ ] **Lag:** Consumer Lag monitored (Burrow/Prometheus).
-   [ ] **Under-replicated:** Alert on under-replicated partitions (>0).
-   [ ] **JMX:** Metrics exported.

## Examples

### Example 1: Real-Time Fraud Detection Pipeline

**Scenario:** A financial services company needs real-time fraud detection using Kafka streaming.

**Architecture Implementation:**
1. **Event Ingestion**: Kafka Connect CDC from PostgreSQL transaction database
2. **Stream Processing**: Kafka Streams application for real-time pattern detection
3. **Alert System**: Producer to alert topic triggering notifications
4. **Storage**: S3 sink for historical analysis and compliance

**Pipeline Configuration:**
| Component | Configuration | Purpose |
|-----------|---------------|---------|
| Topics | 3 (transactions, alerts, enriched) | Data organization |
| Partitions | 12 (3 brokers × 4) | Parallelism |
| Replication | 3 | High availability |
| Compression | LZ4 | Throughput optimization |

**Key Logic:**
- Detects velocity patterns (5+ transactions in 1 minute)
- Identifies geographic anomalies (impossible travel)
- Flags high-risk merchant categories

**Results:**
- 99.7% of fraud detected in under 100ms
- False positive rate reduced from 5% to 0.3%
- Compliance audit passed with zero findings

### Example 2: E-Commerce Order Processing System

**Scenario:** Build a resilient order processing system with Kafka for high reliability.

**System Design:**
1. **Order Events**: Topic for order lifecycle events
2. **Inventory Service**: Consumes orders, updates stock
3. **Payment Service**: Processes payments, publishes results
4. **Notification Service**: Sends confirmations via email/SMS

**Resilience Patterns:**
- Dead Letter Queue for failed processing
- Idempotent producers for exactly-once semantics
- Consumer groups with manual offset management
- Retries with exponential backoff

**Configuration:**
```yaml
# Producer Configuration
acks: all
retries: 3
enable.idempotence: true

# Consumer Configuration
auto.offset.reset: earliest
enable.auto.commit: false
max.poll.records: 500
```

**Results:**
- 99.99% message delivery reliability
- Zero duplicate orders in 6 months
- Peak processing: 10,000 orders/second

### Example 3: IoT Telemetry Platform

**Scenario:** Process millions of IoT device telemetry messages with Kafka.

**Platform Architecture:**
1. **Device Gateway**: MQTT to Kafka proxy
2. **Data Enrichment**: Stream processing adds device metadata
3. **Time-Series Storage**: S3 sink partitioned by device_id/date
4. **Real-Time Alerts**: Threshold-based alerting for anomalies

**Scalability Configuration:**
- 50 partitions for parallel processing
- Compression enabled for cost optimization
- Retention: 7 days hot, 1 year cold in S3
- Schema Registry for data contracts

**Performance Metrics:**
| Metric | Value |
|--------|-------|
| Throughput | 500,000 messages/sec |
| Latency (P99) | 50ms |
| Consumer lag | < 1 second |
| Storage efficiency | 60% reduction with compression |

## Best Practices

### Topic Design

- **Naming Conventions**: Use clear, hierarchical topic names (domain.entity.event)
- **Partition Strategy**: Plan for future growth (3x expected throughput)
- **Retention Policies**: Match retention to business requirements
- **Cleanup Policies**: Use delete for time-based, compact for state
- **Schema Management**: Enforce schemas via Schema Registry

### Producer Optimization

- **Batching**: Increase batch.size and linger.ms for throughput
- **Compression**: Use LZ4 for balance of speed and size
- **Acks Configuration**: Use all for reliability, 1 for latency
- **Retry Strategy**: Implement retries with backoff
- **Idempotence**: Enable for exactly-once semantics in critical paths

### Consumer Best Practices

- **Offset Management**: Use manual commit for critical processing
- **Batch Processing**: Increase max.poll.records for efficiency
- **Rebalance Handling**: Implement graceful shutdown
- **Error Handling**: Dead letter queues for poison messages
- **Monitoring**: Track consumer lag and processing time

### Security Configuration

- **Encryption**: TLS for all client-broker communication
- **Authentication**: SASL/SCRAM or mTLS for production
- **Authorization**: ACLs with least privilege principle
- **Quotas**: Implement client quotas to prevent abuse
- **Audit Logging**: Log all access and configuration changes

### Performance Tuning

- **Broker Configuration**: Optimize for workload type (throughput vs latency)
- **JVM Tuning**: Heap size and garbage collector selection
- **OS Tuning**: File descriptor limits, network settings
- **Monitoring**: Metrics for throughput, latency, and errors
- **Capacity Planning**: Regular review and scaling assessment

**Security:**
-   [ ] **Encryption:** TLS enabled for Client-Broker and Inter-broker.
-   [ ] **Auth:** SASL/SCRAM or mTLS enabled.
-   [ ] **ACLs:** Principle of least privilege (Topic read/write).
