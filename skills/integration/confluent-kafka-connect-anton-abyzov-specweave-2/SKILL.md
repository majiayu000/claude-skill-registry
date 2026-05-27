---
description: Kafka Connect integration expert. Covers source and sink connectors, JDBC, Elasticsearch, S3, Debezium CDC, SMT (Single Message Transforms), connector configuration, and data pipeline patterns. Activates for kafka connect, connectors, source connector, sink connector, jdbc connector, debezium, smt, data pipeline, cdc.
---

# Confluent Kafka Connect Skill

Expert knowledge of Kafka Connect for building data pipelines with source and sink connectors.

## What I Know

### Connector Types

**Source Connectors** (External System → Kafka):
- JDBC Source: Databases → Kafka
- Debezium: CDC (MySQL, PostgreSQL, MongoDB) → Kafka
- S3 Source: AWS S3 files → Kafka
- File Source: Local files → Kafka

**Sink Connectors** (Kafka → External System):
- JDBC Sink: Kafka → Databases
- Elasticsearch Sink: Kafka → Elasticsearch
- S3 Sink: Kafka → AWS S3
- HDFS Sink: Kafka → Hadoop HDFS

**Single Message Transforms (SMTs)**:
- Field operations: Insert, Mask, Replace, TimestampConverter
- Routing: RegexRouter, TimestampRouter
- Filtering: Filter, Predicates

## When to Use This Skill

Activate me when you need help with:
- Connector setup ("Configure JDBC connector")
- CDC patterns ("Debezium MySQL CDC")
- Data pipelines ("Stream database changes to Kafka")
- SMT transforms ("Mask sensitive fields")
- Connector troubleshooting ("Connector task failed")

## Common Patterns

### Pattern 1: JDBC Source (Database → Kafka)

**Use Case**: Stream database table changes to Kafka

**Configuration**:
```json
{
  "name": "jdbc-source-users",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "tasks.max": "1",
    "connection.url": "jdbc:postgresql://localhost:5432/mydb",
    "connection.user": "postgres",
    "connection.password": "password",
    "mode": "incrementing",
    "incrementing.column.name": "id",
    "topic.prefix": "postgres-",
    "table.whitelist": "users,orders",
    "poll.interval.ms": "5000"
  }
}
```

**Modes**:
- `incrementing`: Track by auto-increment ID
- `timestamp`: Track by timestamp column
- `timestamp+incrementing`: Both (most reliable)

### Pattern 2: Debezium CDC (MySQL → Kafka)

**Use Case**: Capture all database changes (INSERT/UPDATE/DELETE)

**Configuration**:
```json
{
  "name": "debezium-mysql-cdc",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "tasks.max": "1",
    "database.hostname": "localhost",
    "database.port": "3306",
    "database.user": "debezium",
    "database.password": "password",
    "database.server.id": "1",
    "database.server.name": "mysql",
    "database.include.list": "mydb",
    "table.include.list": "mydb.users,mydb.orders",
    "schema.history.internal.kafka.bootstrap.servers": "localhost:9092",
    "schema.history.internal.kafka.topic": "schema-changes.mydb"
  }
}
```

**Output Format** (Debezium Envelope):
```json
{
  "before": null,
  "after": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "source": {
    "version": "1.9.0",
    "connector": "mysql",
    "name": "mysql",
    "ts_ms": 1620000000000,
    "snapshot": "false",
    "db": "mydb",
    "table": "users",
    "server_id": 1,
    "gtid": null,
    "file": "mysql-bin.000001",
    "pos": 12345,
    "row": 0,
    "thread": null,
    "query": null
  },
  "op": "c",  // c=CREATE, u=UPDATE, d=DELETE, r=READ
  "ts_ms": 1620000000000
}
```

### Pattern 3: JDBC Sink (Kafka → Database)

**Use Case**: Write Kafka events to PostgreSQL

**Configuration**:
```json
{
  "name": "jdbc-sink-enriched-orders",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "tasks.max": "3",
    "topics": "enriched-orders",
    "connection.url": "jdbc:postgresql://localhost:5432/analytics",
    "connection.user": "postgres",
    "connection.password": "password",
    "auto.create": "true",
    "auto.evolve": "true",
    "insert.mode": "upsert",
    "pk.mode": "record_value",
    "pk.fields": "order_id",
    "table.name.format": "orders_${topic}"
  }
}
```

**Insert Modes**:
- `insert`: Append only (fails on duplicate)
- `update`: Update only (requires PK)
- `upsert`: INSERT or UPDATE (recommended)

### Pattern 4: S3 Sink (Kafka → AWS S3)

**Use Case**: Archive Kafka topics to S3

**Configuration**:
```json
{
  "name": "s3-sink-events",
  "config": {
    "connector.class": "io.confluent.connect.s3.S3SinkConnector",
    "tasks.max": "3",
    "topics": "user-events,order-events",
    "s3.region": "us-east-1",
    "s3.bucket.name": "my-kafka-archive",
    "s3.part.size": "5242880",
    "flush.size": "1000",
    "rotate.interval.ms": "60000",
    "rotate.schedule.interval.ms": "3600000",
    "timezone": "UTC",
    "format.class": "io.confluent.connect.s3.format.json.JsonFormat",
    "partitioner.class": "io.confluent.connect.storage.partitioner.TimeBasedPartitioner",
    "path.format": "'year'=YYYY/'month'=MM/'day'=dd/'hour'=HH",
    "locale": "US",
    "timestamp.extractor": "Record"
  }
}
```

**Partitioning** (S3 folder structure):
```
s3://my-kafka-archive/
  topics/user-events/year=2025/month=01/day=15/hour=10/
    user-events+0+0000000000.json
    user-events+0+0000001000.json
  topics/order-events/year=2025/month=01/day=15/hour=10/
    order-events+0+0000000000.json
```

### Pattern 5: Elasticsearch Sink (Kafka → Elasticsearch)

**Use Case**: Index Kafka events for search

**Configuration**:
```json
{
  "name": "elasticsearch-sink-logs",
  "config": {
    "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
    "tasks.max": "3",
    "topics": "application-logs",
    "connection.url": "http://localhost:9200",
    "connection.username": "elastic",
    "connection.password": "password",
    "key.ignore": "true",
    "schema.ignore": "true",
    "type.name": "_doc",
    "index.write.wait_for_active_shards": "1"
  }
}
```

## Single Message Transforms (SMTs)

### Transform 1: Mask Sensitive Fields

**Use Case**: Hide email/phone in Kafka topics

**Configuration**:
```json
{
  "transforms": "maskEmail",
  "transforms.maskEmail.type": "org.apache.kafka.connect.transforms.MaskField$Value",
  "transforms.maskEmail.fields": "email,phone"
}
```

**Before**:
```json
{"id": 1, "name": "John", "email": "john@example.com", "phone": "555-1234"}
```

**After**:
```json
{"id": 1, "name": "John", "email": null, "phone": null}
```

### Transform 2: Add Timestamp

**Use Case**: Add processing timestamp to all messages

**Configuration**:
```json
{
  "transforms": "insertTimestamp",
  "transforms.insertTimestamp.type": "org.apache.kafka.connect.transforms.InsertField$Value",
  "transforms.insertTimestamp.timestamp.field": "processed_at"
}
```

### Transform 3: Route by Field Value

**Use Case**: Route high-value orders to separate topic

**Configuration**:
```json
{
  "transforms": "routeByValue",
  "transforms.routeByValue.type": "org.apache.kafka.connect.transforms.RegexRouter",
  "transforms.routeByValue.regex": "(.*)",
  "transforms.routeByValue.replacement": "$1-high-value",
  "transforms.routeByValue.predicate": "isHighValue",
  "predicates": "isHighValue",
  "predicates.isHighValue.type": "org.apache.kafka.connect.transforms.predicates.TopicNameMatches",
  "predicates.isHighValue.pattern": "orders"
}
```

### Transform 4: Flatten Nested JSON

**Use Case**: Flatten nested structures for JDBC sink

**Configuration**:
```json
{
  "transforms": "flatten",
  "transforms.flatten.type": "org.apache.kafka.connect.transforms.Flatten$Value",
  "transforms.flatten.delimiter": "_"
}
```

**Before**:
```json
{
  "user": {
    "id": 1,
    "profile": {
      "name": "John",
      "email": "john@example.com"
    }
  }
}
```

**After**:
```json
{
  "user_id": 1,
  "user_profile_name": "John",
  "user_profile_email": "john@example.com"
}
```

## Best Practices

### 1. Use Idempotent Connectors

✅ **DO**:
```json
// JDBC Sink with upsert mode
{
  "insert.mode": "upsert",
  "pk.mode": "record_value",
  "pk.fields": "id"
}
```

❌ **DON'T**:
```json
// WRONG: insert mode (duplicates on restart!)
{
  "insert.mode": "insert"
}
```

### 2. Monitor Connector Status

```bash
# Check connector status
curl http://localhost:8083/connectors/jdbc-source-users/status

# Check task status
curl http://localhost:8083/connectors/jdbc-source-users/tasks/0/status
```

### 3. Use Schema Registry

✅ **DO**:
```json
{
  "value.converter": "io.confluent.connect.avro.AvroConverter",
  "value.converter.schema.registry.url": "http://localhost:8081"
}
```

### 4. Configure Error Handling

```json
{
  "errors.tolerance": "all",
  "errors.log.enable": "true",
  "errors.log.include.messages": "true",
  "errors.deadletterqueue.topic.name": "dlq-jdbc-sink",
  "errors.deadletterqueue.context.headers.enable": "true"
}
```

## Connector Management

### Deploy Connector

```bash
# Create connector via REST API
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d @jdbc-source.json

# Update connector
curl -X PUT http://localhost:8083/connectors/jdbc-source-users/config \
  -H "Content-Type: application/json" \
  -d @jdbc-source.json
```

### Monitor Connectors

```bash
# List all connectors
curl http://localhost:8083/connectors

# Get connector info
curl http://localhost:8083/connectors/jdbc-source-users

# Get connector status
curl http://localhost:8083/connectors/jdbc-source-users/status

# Get connector tasks
curl http://localhost:8083/connectors/jdbc-source-users/tasks
```

### Pause/Resume Connectors

```bash
# Pause connector
curl -X PUT http://localhost:8083/connectors/jdbc-source-users/pause

# Resume connector
curl -X PUT http://localhost:8083/connectors/jdbc-source-users/resume

# Restart connector
curl -X POST http://localhost:8083/connectors/jdbc-source-users/restart

# Restart task
curl -X POST http://localhost:8083/connectors/jdbc-source-users/tasks/0/restart
```

## Common Issues & Solutions

### Issue 1: Connector Task Failed

**Symptoms**: Task state = FAILED

**Solutions**:
1. Check connector logs: `docker logs connect-worker`
2. Validate configuration: `curl http://localhost:8083/connector-plugins/<class>/config/validate`
3. Restart task: `curl -X POST .../tasks/0/restart`

### Issue 2: Schema Evolution Error

**Error**: `Incompatible schema detected`

**Solution**: Enable auto-evolution:
```json
{
  "auto.create": "true",
  "auto.evolve": "true"
}
```

### Issue 3: JDBC Connection Pool Exhausted

**Error**: `Could not get JDBC connection`

**Solution**: Increase pool size:
```json
{
  "connection.attempts": "3",
  "connection.backoff.ms": "10000"
}
```

## References

- Kafka Connect Documentation: https://kafka.apache.org/documentation/#connect
- Confluent Hub: https://www.confluent.io/hub/
- Debezium Documentation: https://debezium.io/documentation/
- Transform Reference: https://kafka.apache.org/documentation/#connect_transforms

---

**Invoke me when you need Kafka Connect, connectors, CDC, or data pipeline expertise!**
