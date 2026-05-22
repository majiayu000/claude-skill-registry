---
name: deploying-kafka-k8s
description: |
  Deploys Apache Kafka on Kubernetes using the Strimzi operator with KRaft mode.
  Use when setting up Kafka for event-driven microservices, message queuing, or pub/sub patterns.
  Covers operator installation, cluster creation, topic management, and producer/consumer testing.
  NOT when using managed Kafka (Confluent Cloud, MSK) or local development without K8s.
---

# Deploying Kafka on Kubernetes

Deploy production-ready Apache Kafka clusters using Strimzi operator (v0.49.1+) with KRaft mode.

## Quick Start

```bash
# 1. Create namespace
kubectl create namespace kafka

# 2. Install Strimzi operator
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

# 3. Wait for operator
kubectl wait deployment/strimzi-cluster-operator --for=condition=Available -n kafka --timeout=300s

# 4. Deploy Kafka cluster
kubectl apply -f https://strimzi.io/examples/latest/kafka/kraft/kafka-single-node.yaml -n kafka

# 5. Wait for ready
kubectl wait kafka/my-cluster --for=condition=Ready --timeout=300s -n kafka
```

## Strimzi Operator Installation

### Standard Install (Cluster-wide)

```bash
kubectl create namespace kafka
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
kubectl get pods -n kafka -w
```

### Namespace-scoped Install

```bash
# Download and modify for single namespace
curl -L https://strimzi.io/install/latest?namespace=kafka > strimzi-install.yaml
# Edit RoleBindings and ClusterRoles as needed
kubectl apply -f strimzi-install.yaml -n kafka
```

## Kafka Cluster Configurations

### Single Node (Development)

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
  namespace: kafka
spec:
  kafka:
    version: 3.9.0
    replicas: 1
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
    storage:
      type: ephemeral
  entityOperator:
    topicOperator: {}
    userOperator: {}
```

### Production Cluster (3 Nodes + KRaft)

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: kafka-production
  namespace: kafka
spec:
  kafka:
    version: 3.9.0
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
      - name: external
        port: 9094
        type: nodeport
        tls: false
    config:
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      default.replication.factor: 3
      min.insync.replicas: 2
      inter.broker.protocol.version: "3.9"
    storage:
      type: jbod
      volumes:
        - id: 0
          type: persistent-claim
          size: 100Gi
          deleteClaim: false
    resources:
      requests:
        memory: 2Gi
        cpu: "500m"
      limits:
        memory: 4Gi
        cpu: "2"
  entityOperator:
    topicOperator: {}
    userOperator: {}
```

## Topic Management

### Create Topic via CRD

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: task-events
  namespace: kafka
  labels:
    strimzi.io/cluster: my-cluster
spec:
  partitions: 3
  replicas: 1
  config:
    retention.ms: 604800000    # 7 days
    segment.bytes: 1073741824  # 1GB
```

### List and Describe Topics

```bash
# List topics
kubectl -n kafka run kafka-topics -ti --rm --restart=Never \
  --image=quay.io/strimzi/kafka:0.49.1-kafka-3.9.0 -- \
  bin/kafka-topics.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --list

# Describe topic
kubectl -n kafka run kafka-topics -ti --rm --restart=Never \
  --image=quay.io/strimzi/kafka:0.49.1-kafka-3.9.0 -- \
  bin/kafka-topics.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 \
  --describe --topic task-events
```

## Producer/Consumer Testing

### Console Producer

```bash
kubectl -n kafka run kafka-producer -ti --rm --restart=Never \
  --image=quay.io/strimzi/kafka:0.49.1-kafka-3.9.0 -- \
  bin/kafka-console-producer.sh \
  --bootstrap-server my-cluster-kafka-bootstrap:9092 \
  --topic my-topic
```

### Console Consumer

```bash
kubectl -n kafka run kafka-consumer -ti --rm --restart=Never \
  --image=quay.io/strimzi/kafka:0.49.1-kafka-3.9.0 -- \
  bin/kafka-console-consumer.sh \
  --bootstrap-server my-cluster-kafka-bootstrap:9092 \
  --topic my-topic --from-beginning
```

## Service Discovery

Kafka bootstrap services for client connections:

| Service | Port | Use |
|---------|------|-----|
| `my-cluster-kafka-bootstrap:9092` | Plain | Internal cluster apps |
| `my-cluster-kafka-bootstrap:9093` | TLS | Secure internal apps |
| `my-cluster-kafka-0.my-cluster-kafka-brokers:9092` | Plain | Direct broker access |

### Connect from Another Namespace

```yaml
# In your app deployment
env:
  - name: KAFKA_BOOTSTRAP_SERVERS
    value: "my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092"
```

## Monitoring

### Enable Prometheus Metrics

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
spec:
  kafka:
    metricsConfig:
      type: jmxPrometheusExporter
      valueFrom:
        configMapKeyRef:
          name: kafka-metrics
          key: kafka-metrics-config.yml
```

### Check Cluster Status

```bash
kubectl get kafka -n kafka
kubectl describe kafka my-cluster -n kafka
kubectl get pods -n kafka -l strimzi.io/cluster=my-cluster
```

## Troubleshooting

### Operator Not Starting

```bash
kubectl logs deployment/strimzi-cluster-operator -n kafka
kubectl describe pod -l name=strimzi-cluster-operator -n kafka
```

### Kafka Pods Not Ready

```bash
kubectl describe pod my-cluster-kafka-0 -n kafka
kubectl logs my-cluster-kafka-0 -n kafka
kubectl get events -n kafka --sort-by='.lastTimestamp'
```

### Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| PVC pending | No storage class | Add `storageClassName` or use ephemeral |
| Pods OOMKilled | Insufficient memory | Increase resource limits |
| Connection refused | Wrong bootstrap URL | Use `cluster-kafka-bootstrap:9092` |

## Cleanup

```bash
# Delete cluster
kubectl -n kafka delete kafka my-cluster

# Delete PVCs (data)
kubectl delete pvc -l strimzi.io/name=my-cluster-kafka -n kafka

# Remove operator
kubectl -n kafka delete -f 'https://strimzi.io/install/latest?namespace=kafka'

# Delete namespace
kubectl delete namespace kafka
```

## Integration with Dapr

For Dapr pub/sub integration, see `configuring-dapr-pubsub` skill:

```yaml
# Dapr component pointing to Strimzi Kafka
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  metadata:
    - name: brokers
      value: "my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092"
    - name: authType
      value: "none"
```

## Verification

Run: `python scripts/verify.py`

## Related Skills

- `operating-k8s-local` - Local Minikube cluster setup
- `configuring-dapr-pubsub` - Dapr Kafka pub/sub integration
- `scaffolding-fastapi-dapr` - FastAPI services with Kafka events