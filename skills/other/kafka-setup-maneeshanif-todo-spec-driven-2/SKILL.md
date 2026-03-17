---
name: kafka-setup
description: Set up Apache Kafka for event streaming - Strimzi for local Kubernetes, Redpanda Cloud for production. Use when configuring event-driven messaging for Phase 5. (project)
allowed-tools: Bash, Write, Read, Glob, Edit, Grep
---

# Kafka Setup Skill

## Quick Start

1. **Read Phase 5 Constitution** - `constitution-prompt-phase-5.md`
2. **Choose deployment** - Strimzi (local) or Redpanda Cloud (production)
3. **Install Strimzi operator** - For Kubernetes deployment
4. **Create Kafka cluster** - Using Strimzi CRDs
5. **Create topics** - task-events, reminder-events, audit-events
6. **Configure Dapr component** - Connect Dapr to Kafka

## Deployment Options

| Option | Environment | Use Case |
|--------|-------------|----------|
| **Strimzi** | Minikube/DOKS | Full Kubernetes-native Kafka |
| **Redpanda Cloud** | Production | Managed Kafka-compatible streaming |
| **Docker Compose** | Local Dev | Quick local development |

## Strimzi Installation (Kubernetes)

### Install Strimzi Operator

```bash
# Create namespace
kubectl create namespace kafka

# Install Strimzi operator
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

# Wait for operator to be ready
kubectl wait deployment/strimzi-cluster-operator \
  --for=condition=available \
  --timeout=300s \
  -n kafka
```

### Create Kafka Cluster

Create `kafka/kafka-cluster.yaml`:

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: todo-kafka
  namespace: kafka
spec:
  kafka:
    version: 3.6.0
    replicas: 3
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
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      default.replication.factor: 3
      min.insync.replicas: 2
      inter.broker.protocol.version: "3.6"
    storage:
      type: jbod
      volumes:
        - id: 0
          type: persistent-claim
          size: 10Gi
          deleteClaim: false
    resources:
      requests:
        memory: 1Gi
        cpu: "500m"
      limits:
        memory: 2Gi
        cpu: "1"
  zookeeper:
    replicas: 3
    storage:
      type: persistent-claim
      size: 5Gi
      deleteClaim: false
    resources:
      requests:
        memory: 512Mi
        cpu: "250m"
      limits:
        memory: 1Gi
        cpu: "500m"
  entityOperator:
    topicOperator: {}
    userOperator: {}
```

### Minikube-Optimized Cluster (Single Node)

Create `kafka/kafka-cluster-minikube.yaml`:

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: todo-kafka
  namespace: kafka
spec:
  kafka:
    version: 3.6.0
    replicas: 1
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
    config:
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
      transaction.state.log.min.isr: 1
      default.replication.factor: 1
      min.insync.replicas: 1
    storage:
      type: ephemeral
    resources:
      requests:
        memory: 512Mi
        cpu: "250m"
      limits:
        memory: 1Gi
        cpu: "500m"
  zookeeper:
    replicas: 1
    storage:
      type: ephemeral
    resources:
      requests:
        memory: 256Mi
        cpu: "100m"
      limits:
        memory: 512Mi
        cpu: "250m"
  entityOperator:
    topicOperator: {}
```

### Create Kafka Topics

Create `kafka/kafka-topics.yaml`:

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: task-events
  namespace: kafka
  labels:
    strimzi.io/cluster: todo-kafka
spec:
  partitions: 3
  replicas: 1
  config:
    retention.ms: 604800000  # 7 days
    cleanup.policy: delete
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: reminder-events
  namespace: kafka
  labels:
    strimzi.io/cluster: todo-kafka
spec:
  partitions: 3
  replicas: 1
  config:
    retention.ms: 604800000
    cleanup.policy: delete
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: audit-events
  namespace: kafka
  labels:
    strimzi.io/cluster: todo-kafka
spec:
  partitions: 3
  replicas: 1
  config:
    retention.ms: 2592000000  # 30 days
    cleanup.policy: delete
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: task-updates
  namespace: kafka
  labels:
    strimzi.io/cluster: todo-kafka
spec:
  partitions: 3
  replicas: 1
  config:
    retention.ms: 86400000  # 1 day
    cleanup.policy: delete
```

## Docker Compose (Local Development)

Add to `docker-compose.yaml`:

```yaml
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"
    networks:
      - todo-network

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    container_name: kafka
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
      - "29092:29092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:29092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
    networks:
      - todo-network

  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    container_name: kafka-ui
    depends_on:
      - kafka
    ports:
      - "8080:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:9092
    networks:
      - todo-network
```

## Redpanda Cloud Setup (Production)

### Create Redpanda Cloud Cluster

1. Sign up at https://cloud.redpanda.com
2. Create a new cluster (Dedicated or Serverless)
3. Get connection credentials

### Configure Dapr for Redpanda

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: taskpubsub
  namespace: todo-app
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      secretKeyRef:
        name: redpanda-secrets
        key: brokers
    - name: authType
      value: "password"
    - name: saslUsername
      secretKeyRef:
        name: redpanda-secrets
        key: username
    - name: saslPassword
      secretKeyRef:
        name: redpanda-secrets
        key: password
    - name: saslMechanism
      value: "SCRAM-SHA-256"
    - name: tls
      value: "true"
```

## Dapr Pub/Sub Component

Create `dapr-components/pubsub.yaml`:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: taskpubsub
  namespace: todo-app
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "todo-kafka-kafka-bootstrap.kafka.svc.cluster.local:9092"
    - name: consumerGroup
      value: "todo-consumer-group"
    - name: authType
      value: "none"
    - name: disableTls
      value: "true"
    - name: maxMessageBytes
      value: "1048576"
    - name: consumeRetryInterval
      value: "100ms"
scopes:
  - backend
  - notification-service
  - recurring-service
  - audit-service
  - websocket-service
```

## Python Kafka Client (Direct)

### Installation

```bash
uv add aiokafka
```

### Producer

```python
from aiokafka import AIOKafkaProducer
import json

class KafkaEventProducer:
    def __init__(self, bootstrap_servers: str):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def publish(self, topic: str, event: dict):
        await self.producer.send_and_wait(topic, event)
```

### Consumer

```python
from aiokafka import AIOKafkaConsumer
import json

class KafkaEventConsumer:
    def __init__(self, bootstrap_servers: str, topics: list[str], group_id: str):
        self.consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    async def consume(self):
        async for msg in self.consumer:
            yield msg.topic, msg.value
```

## Verification Checklist

- [ ] Kafka cluster running (Strimzi or Docker)
- [ ] All topics created (task-events, reminder-events, audit-events, task-updates)
- [ ] Dapr component configured
- [ ] Producer can publish messages
- [ ] Consumer receives messages
- [ ] Kafka UI accessible (optional)
- [ ] Redpanda Cloud configured (for production)

## Topic Schema

### task-events

```json
{
  "event_type": "task.created | task.updated | task.deleted | task.completed",
  "task_id": "uuid",
  "user_id": "uuid",
  "task": {
    "id": "uuid",
    "title": "string",
    "description": "string",
    "priority": "low | medium | high",
    "status": "pending | in_progress | completed",
    "due_date": "ISO8601",
    "tags": ["string"]
  },
  "timestamp": "ISO8601"
}
```

### reminder-events

```json
{
  "event_type": "reminder.triggered | reminder.created | reminder.deleted",
  "reminder_id": "uuid",
  "task_id": "uuid",
  "user_id": "uuid",
  "message": "string",
  "timestamp": "ISO8601"
}
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Broker not reachable | Wrong address | Use internal K8s DNS |
| Topic not found | Not created | Apply KafkaTopic CRD |
| Consumer lag | Slow processing | Scale consumers |
| Auth failed | Wrong credentials | Check secrets |

## References

- [Strimzi Documentation](https://strimzi.io/docs/)
- [Apache Kafka](https://kafka.apache.org/documentation/)
- [Redpanda Cloud](https://docs.redpanda.com/docs/deploy/deployment-option/cloud/)
- [Dapr Kafka Pub/Sub](https://docs.dapr.io/reference/components-reference/supported-pubsub/setup-apache-kafka/)
- [Phase 5 Constitution](../../../constitution-prompt-phase-5.md)
