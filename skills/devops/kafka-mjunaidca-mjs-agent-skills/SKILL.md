---
name: kafka
description: |
  Apache Kafka on Kubernetes with Strimzi (KRaft mode, no ZooKeeper).
  This skill should be used when users ask to deploy Kafka clusters, build
  producers/consumers, implement event-driven patterns, or debug Kafka issues.
  Includes tested manifests and Makefile for one-command deployment.
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/verify-kubectl-context.sh"
---

# Apache Kafka

Event streaming for Kubernetes. Strimzi operator, KRaft mode, no ZooKeeper.

## Quick Start (Tested)

```bash
make install    # Deploy Strimzi + Kafka
make test       # Verify everything works
make status     # Show resources
make uninstall  # Clean up
```

**Requirements:** Kubernetes cluster, Helm 3+

**Versions:** Strimzi 0.49+, Kafka 4.1.1

---

## Resource Detection & Adaptation

**Before generating manifests, detect the target environment:**

```bash
# Detect machine memory
sysctl -n hw.memsize 2>/dev/null | awk '{print $0/1024/1024/1024 " GB"}' || \
  grep MemTotal /proc/meminfo | awk '{print $2/1024/1024 " GB"}'

# Detect Docker Desktop allocation
docker info --format '{{.MemTotal}}' 2>/dev/null | awk '{print $0/1024/1024/1024 " GB"}'

# Detect Kubernetes node capacity
kubectl get nodes -o jsonpath='{.items[0].status.capacity.memory}' 2>/dev/null
```

**Adapt resource configuration based on detection:**

| Detected RAM | Profile | Kafka Memory | Action |
|--------------|---------|--------------|--------|
| < 12GB | Minimal | 512Mi-1Gi | Warn user about constraints |
| 12-24GB | Standard | 1Gi-2Gi | Default configuration |
| > 24GB | Production | 4Gi-8Gi | Enable full features |

### Adaptive Resource Templates

**Minimal (detected < 12GB):**
```yaml
resources:
  requests:
    memory: 512Mi
    cpu: 200m
  limits:
    memory: 1Gi
    cpu: 500m
```
⚠️ Agent should warn: "Limited resources detected. Kafka may be unstable under load."

**Standard (detected 12-24GB):**
```yaml
resources:
  requests:
    memory: 1Gi
    cpu: 250m
  limits:
    memory: 2Gi
    cpu: 1000m
```

**Production (detected > 24GB or real cluster):**
```yaml
resources:
  requests:
    memory: 4Gi
    cpu: 1000m
  limits:
    memory: 8Gi
    cpu: 4000m
```

### Agent Behavior

1. **Always detect** before generating manifests
2. **Adapt** resource configs to detected environment
3. **Warn** if resources are insufficient for requested workload
4. **Suggest** Docker Desktop settings if running locally

---

## What This Skill Does

| Task | How |
|------|-----|
| **Analyze coupling** | Identify temporal, availability, behavioral issues |
| **Explain eventual consistency** | Consistency windows, read-your-writes patterns |
| **Design events** | Domain events, CloudEvents, Avro schemas |
| Deploy Kafka | Helm (Strimzi) + kubectl (manifests) |
| Create topics | KafkaTopic CRD |
| Build producers | confluent-kafka-python templates |
| Build consumers | AIOConsumer for FastAPI |
| Debug issues | Runbooks in references/ |

## What This Skill Does NOT Do

- Deploy ZooKeeper (KRaft only)
- Manage Kafka Streams applications
- Configure multi-datacenter replication

---

## Deployment

### Install Strimzi Operator

```bash
helm repo add strimzi https://strimzi.io/charts
helm install strimzi-operator strimzi/strimzi-kafka-operator -n kafka --create-namespace --wait
```

### Deploy Kafka Cluster

```bash
kubectl apply -f manifests/kafka-cluster.yaml -n kafka
kubectl wait kafka/dev-cluster --for=condition=Ready --timeout=300s -n kafka
```

### Create Topic

```bash
kubectl apply -f manifests/kafka-topic.yaml -n kafka
```

### Verify

```bash
kubectl get kafka,kafkatopic,pods -n kafka
```

---

## Core Concepts

```
Topic      = Named stream (like a database table)
Partition  = Ordered log within topic (parallelism unit)
Consumer Group = Consumers sharing work (partition → one consumer)
Offset     = Consumer position (commit to track progress)
Broker     = Kafka server
Controller = Metadata manager (KRaft replaces ZooKeeper)
```

---

## Local Development

Connect from your host machine (no port-forward needed):

```python
# From your local machine (outside Kubernetes)
producer = Producer({'bootstrap.servers': 'localhost:30092'})
```

Connect from inside Kubernetes (pod-to-pod):

```python
# From another pod in the cluster
producer = Producer({'bootstrap.servers': 'dev-cluster-kafka-bootstrap.kafka:9092'})
```

| Location | Bootstrap Server |
|----------|------------------|
| Local machine | `localhost:30092` |
| Same namespace | `dev-cluster-kafka-bootstrap:9092` |
| Different namespace | `dev-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092` |

---

## Producer/Consumer (Python)

```python
from confluent_kafka import Producer, Consumer

# Producer (production config)
producer = Producer({
    'bootstrap.servers': 'localhost:30092',  # Or K8s service for pods
    'acks': 'all',
    'enable.idempotence': True,
})
producer.produce('my-topic', key='key', value='message')
producer.flush()

# Consumer
consumer = Consumer({
    'bootstrap.servers': 'localhost:30092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,
})
consumer.subscribe(['my-topic'])
msg = consumer.poll(1.0)
```

See `assets/templates/producer-consumer.py` for async FastAPI integration.

---

## Debugging

```bash
# Check consumer lag
kubectl exec -n kafka dev-cluster-dual-role-0 -- \
  bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --describe --group <group-name>

# List topics
kubectl exec -n kafka dev-cluster-dual-role-0 -- \
  bin/kafka-topics.sh --bootstrap-server localhost:9092 --list

# Describe topic
kubectl exec -n kafka dev-cluster-dual-role-0 -- \
  bin/kafka-topics.sh --bootstrap-server localhost:9092 \
  --describe --topic <topic-name>
```

See `references/debugging-runbooks.md` for detailed troubleshooting.

---

## Delivery Semantics

| Guarantee | Config | Use When |
|-----------|--------|----------|
| At-most-once | `acks=0` | Metrics, logs (may lose) |
| At-least-once | `acks=all` + manual commit | Most cases (may duplicate) |
| Exactly-once | Transactions | Financial (higher latency) |

**Default:** At-least-once with idempotent consumers.

---

## File Structure

```
kafka/
├── Makefile                 # Tested deployment commands
├── manifests/
│   ├── kafka-cluster.yaml   # KRaft cluster (tested)
│   └── kafka-topic.yaml     # Topic CRD
├── assets/templates/
│   └── producer-consumer.py # Python async templates
└── references/              # Deep knowledge
    ├── core-concepts.md
    ├── producers.md
    ├── consumers.md
    ├── debugging-runbooks.md
    ├── gotchas.md
    └── ... (15 files)
```

---

## Architecture Analysis

When analyzing synchronous architectures for coupling:

```
Scenario: Service A calls B, C, D directly (500ms each)

Temporal Coupling?
└── Does caller wait for all responses? → YES = coupled

Availability Coupling?
└── If B is down, does A fail? → YES = coupled

Behavioral Coupling?
└── Does A import B, C, D clients? → YES = coupled
```

**Solution:** Publish domain event, services consume independently.

See `references/architecture-patterns.md` for detailed analysis templates.

---

## References

| File | When to Read |
|------|--------------|
| `references/architecture-patterns.md` | **Coupling analysis, eventual consistency, when to use Kafka** |
| `references/agent-event-patterns.md` | **AI agent coordination, correlation IDs, fanout** |
| `references/strimzi-deployment.md` | KRaft mode, CRDs, storage sizing |
| `references/producers.md` | Producer configuration, batching, tuning |
| `references/consumers.md` | Consumer groups, commits |
| `references/delivery-semantics.md` | At-most/least/exactly-once decision tree |
| `references/outbox-pattern.md` | Transactional outbox with Debezium CDC |
| `references/debugging-runbooks.md` | Lag, rebalancing issues |
| `references/monitoring.md` | Prometheus, alerts, Grafana |
| `references/gotchas.md` | Common mistakes |
| `references/security-patterns.md` | SCRAM, mTLS |

---

## Related Skills

| Skill | Use For |
|-------|---------|
| `/kubernetes` | Cluster operations |
| `/helm` | Chart customization |
| `/docker` | Local development |
