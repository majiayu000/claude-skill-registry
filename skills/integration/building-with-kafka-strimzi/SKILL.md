---
name: building-with-kafka-strimzi
description: Use when building event-driven systems with Apache Kafka on Kubernetes. Triggers include EDA patterns, Kafka producers/consumers, Strimzi operator deployment, Schema Registry, transactions, exactly-once semantics. NOT for general messaging (use Dapr pub/sub for abstraction).
---

# Building Event-Driven Systems with Kafka & Strimzi

Production-ready event streaming on Kubernetes using Apache Kafka with Strimzi operator.

## Persona

You are a Kafka and event-driven architecture expert with production Kubernetes experience. You understand:
- Event-driven architecture patterns (events vs commands, eventual consistency)
- Apache Kafka internals (brokers, partitions, consumer groups, offsets)
- Strimzi operator for Kubernetes-native Kafka deployment
- confluent-kafka-python for high-performance Python clients
- Schema Registry and Avro for event schema management
- Exactly-once semantics and transactional patterns

## When to Use

- Building event-driven microservices
- Deploying Kafka on Kubernetes with Strimzi
- Implementing reliable producers with delivery guarantees
- Managing consumer groups and offset handling
- Schema evolution with Avro and Schema Registry
- Change data capture with Debezium
- Transactional event processing

## Core Concepts

### Event-Driven Architecture

| Concept | Description |
|---------|-------------|
| **Events** | Immutable facts about past occurrences (e.g., "OrderCreated") |
| **Commands** | Requests to perform actions (e.g., "CreateOrder") |
| **Eventual Consistency** | Systems converge to consistent state over time |
| **Event Sourcing** | Capture state changes as event sequence |
| **CQRS** | Separate command and query processing |

### Kafka Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Kafka Cluster (KRaft Mode - No ZooKeeper)                  │
├─────────────────────────────────────────────────────────────┤
│  Controller Nodes (metadata via Raft)                       │
│   └─ __cluster_metadata topic                               │
├─────────────────────────────────────────────────────────────┤
│  Broker Nodes (message processing)                          │
│   └─ Topics → Partitions → Segments                         │
├─────────────────────────────────────────────────────────────┤
│  Producers → Topics ← Consumer Groups                       │
│   └─ Partition assignment, offset tracking                  │
└─────────────────────────────────────────────────────────────┘
```

### Strimzi Components

| Component | Role |
|-----------|------|
| **Cluster Operator** | Manages Kafka cluster lifecycle |
| **Entity Operator** | Contains Topic + User operators |
| **Topic Operator** | Manages KafkaTopic CRs |
| **User Operator** | Manages KafkaUser CRs and credentials |

## Decision Logic

| Situation | Pattern | Why |
|-----------|---------|-----|
| Critical data | `acks=all` + idempotent producer | Durability over speed |
| High throughput | `acks=1` + batching | Balance speed/safety |
| Atomic multi-topic writes | Transactions | All-or-nothing |
| Schema evolution | Avro + Schema Registry | Backward compatibility |
| Database sync | Debezium CDC + Outbox | Transactional integrity |
| Consumer scaling | Consumer groups | Parallel processing |

## Strimzi Deployment on Kubernetes

### Install Strimzi Operator

```bash
# Add Strimzi Helm repo
helm repo add strimzi https://strimzi.io/charts/
helm repo update

# Install operator
helm install strimzi-kafka-operator strimzi/strimzi-kafka-operator \
  --namespace kafka --create-namespace
```

### Create Kafka Cluster (KRaft Mode)

```yaml
# kafka-cluster.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaNodePool
metadata:
  name: dual-role
  labels:
    strimzi.io/cluster: task-events
spec:
  replicas: 1
  roles:
    - controller
    - broker
  storage:
    type: ephemeral  # Use persistent-claim for production
---
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: task-events
  annotations:
    strimzi.io/node-pools: enabled
    strimzi.io/kraft: enabled
spec:
  kafka:
    version: 3.8.0
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
      transaction.state.log.min.isr: 1
      default.replication.factor: 1
      min.insync.replicas: 1
  entityOperator:
    topicOperator: {}
    userOperator: {}
```

```bash
kubectl apply -f kafka-cluster.yaml -n kafka
```

### Create Topics via CRD

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: task-created
  labels:
    strimzi.io/cluster: task-events
spec:
  partitions: 3
  replicas: 1
  config:
    retention.ms: "604800000"  # 7 days
    cleanup.policy: delete
```

### Create Users via CRD

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaUser
metadata:
  name: task-api
  labels:
    strimzi.io/cluster: task-events
spec:
  authentication:
    type: scram-sha-512
  authorization:
    type: simple
    acls:
      - resource:
          type: topic
          name: task-*
          patternType: prefix
        operations: [Read, Write, Describe]
```

## Python Producer Patterns

### Basic Producer with Delivery Reports

```python
from confluent_kafka import Producer

def delivery_report(err, msg):
    """Callback triggered by poll() or flush()"""
    if err is not None:
        print(f'Delivery failed: {err}')
    else:
        print(f'Delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}')

producer = Producer({
    'bootstrap.servers': 'task-events-kafka-bootstrap:9092',
    'client.id': 'task-api',
    'acks': 'all',
    'enable.idempotence': True,
    'retries': 5,
    'delivery.timeout.ms': 30000
})

# Async produce (default)
producer.produce(
    topic='task-created',
    key='task-123',
    value='{"id": "task-123", "title": "Buy groceries"}',
    callback=delivery_report
)

# Service callbacks
producer.poll(0)

# Flush before shutdown
producer.flush()
```

### Idempotent Producer (Exactly-Once)

```python
producer = Producer({
    'bootstrap.servers': 'localhost:9092',
    'enable.idempotence': True,  # Prevents duplicates on retry
    'acks': 'all',               # Wait for all replicas
    'max.in.flight.requests.per.connection': 5,  # Max for idempotence
    'retries': 2147483647        # Retry indefinitely within timeout
})
```

## Python Consumer Patterns

### Basic Consumer with Manual Commit

```python
from confluent_kafka import Consumer, KafkaError

consumer = Consumer({
    'bootstrap.servers': 'task-events-kafka-bootstrap:9092',
    'group.id': 'notification-service',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False  # Manual commit for at-least-once
})

consumer.subscribe(['task-created'])

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            raise Exception(msg.error())

        # Process message
        print(f'Received: {msg.value().decode()}')

        # Commit after successful processing
        consumer.commit(message=msg)

finally:
    consumer.close()
```

### Consumer with Rebalance Callbacks

```python
def on_assign(consumer, partitions):
    print(f'Assigned: {partitions}')

def on_revoke(consumer, partitions):
    print(f'Revoking: {partitions}')
    consumer.commit(asynchronous=False)  # Commit before losing partitions

consumer.subscribe(
    ['task-created'],
    on_assign=on_assign,
    on_revoke=on_revoke
)
```

## Avro with Schema Registry

### Producer with Avro Serialization

```python
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField

# Schema Registry client
sr_client = SchemaRegistryClient({'url': 'http://schema-registry:8081'})

# Avro schema
task_schema = """
{
  "type": "record",
  "name": "TaskCreated",
  "namespace": "com.example.events",
  "fields": [
    {"name": "id", "type": "string"},
    {"name": "title", "type": "string"},
    {"name": "created_at", "type": "string"},
    {"name": "priority", "type": ["null", "int"], "default": null}
  ]
}
"""

# Serializer
serializer = AvroSerializer(
    schema_registry_client=sr_client,
    schema_str=task_schema,
    to_dict=lambda obj, ctx: obj.__dict__
)

# Produce
class TaskCreated:
    def __init__(self, id, title, created_at, priority=None):
        self.id = id
        self.title = title
        self.created_at = created_at
        self.priority = priority

event = TaskCreated('task-123', 'Buy groceries', '2025-01-01T10:00:00Z', 1)
producer.produce(
    topic='task-created',
    key='task-123',
    value=serializer(event, SerializationContext('task-created', MessageField.VALUE))
)
```

## Transactions (Exactly-Once)

### Transactional Producer

```python
producer = Producer({
    'bootstrap.servers': 'localhost:9092',
    'transactional.id': 'task-processor-1',
    'enable.idempotence': True
})

# Initialize transactions once
producer.init_transactions()

try:
    producer.begin_transaction()

    # Produce multiple messages atomically
    producer.produce('orders', key='o1', value='order-1')
    producer.produce('payments', key='p1', value='payment-1')
    producer.produce('audit', key='a1', value='audit-log')

    producer.commit_transaction()
except Exception as e:
    producer.abort_transaction()
    raise
```

### Transaction-Aware Consumer

```python
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'txn-consumer',
    'isolation.level': 'read_committed',  # Only read committed messages
    'enable.auto.commit': False
})
```

## FastAPI Integration

### Async Producer with Lifespan

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from confluent_kafka import Producer
import asyncio

producer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global producer
    producer = Producer({'bootstrap.servers': 'kafka:9092'})
    yield
    producer.flush()

app = FastAPI(lifespan=lifespan)

@app.post("/tasks")
async def create_task(title: str):
    task_id = str(uuid.uuid4())
    event = {"id": task_id, "title": title}

    producer.produce(
        'task-created',
        key=task_id,
        value=json.dumps(event)
    )
    producer.poll(0)

    return {"id": task_id}
```

### Background Consumer

```python
import asyncio
from threading import Thread

def consume_loop():
    consumer = Consumer({
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'notification-service'
    })
    consumer.subscribe(['task-created'])

    while True:
        msg = consumer.poll(1.0)
        if msg and not msg.error():
            # Process message
            pass

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start consumer in background thread
    consumer_thread = Thread(target=consume_loop, daemon=True)
    consumer_thread.start()
    yield
```

## Delivery Guarantees

| Guarantee | Producer Config | Consumer Config | Risk |
|-----------|-----------------|-----------------|------|
| **At-most-once** | `acks=0` | Auto-commit before process | Data loss |
| **At-least-once** | `acks=all`, retries | Commit after process | Duplicates |
| **Exactly-once** | Transactions + idempotence | `isolation.level=read_committed` | Complexity |

## Task API Event Examples

### Event Naming Convention

```
Domain: task
Events: task.created, task.updated, task.completed, task.deleted
Topics: task-events (single topic) or task-created, task-updated (per event)
```

### Event Schema

```json
{
  "event_id": "uuid",
  "event_type": "task.created",
  "occurred_at": "ISO-8601",
  "data": {
    "task_id": "uuid",
    "title": "string",
    "owner_id": "uuid"
  },
  "metadata": {
    "correlation_id": "uuid",
    "causation_id": "uuid"
  }
}
```

## Safety & Guardrails

### NEVER
- Use `acks=0` for critical data
- Set `max.in.flight.requests > 5` with idempotence
- Skip `consumer.close()` (causes rebalance delays)
- Store offsets before successful processing
- Expose broker addresses externally without TLS

### ALWAYS
- Use `acks=all` for important events
- Enable idempotence for exactly-once
- Handle `KafkaError._PARTITION_EOF` gracefully
- Use Schema Registry for production
- Set appropriate `retention.ms` for event topics
- Monitor consumer lag

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `NOT_ENOUGH_REPLICAS` | ISR below `min.insync.replicas` | Check broker health |
| `COORDINATOR_NOT_AVAILABLE` | Consumer group coordinator missing | Wait, retry |
| `REBALANCE_IN_PROGRESS` | Consumer group rebalancing | Wait for completion |
| `OFFSET_OUT_OF_RANGE` | Requested offset doesn't exist | Check `auto.offset.reset` |
| `UNKNOWN_TOPIC_OR_PARTITION` | Topic doesn't exist | Create topic first |

## References

- [Strimzi Documentation](https://strimzi.io/documentation/)
- [Confluent Kafka Python](https://docs.confluent.io/kafka-clients/python/current/overview.html)
- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [Schema Registry](https://docs.confluent.io/platform/current/schema-registry/)
