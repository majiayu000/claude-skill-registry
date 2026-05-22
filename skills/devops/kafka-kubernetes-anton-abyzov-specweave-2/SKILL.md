---
name: kafka-kubernetes
description: Kubernetes deployment expert for Apache Kafka using Helm, Strimzi, and Confluent operators. Use when deploying Kafka on K8s, configuring StatefulSets, or choosing between Kafka operators for production.
---

# Kafka on Kubernetes Deployment

Expert guidance for deploying Apache Kafka on Kubernetes using industry-standard tools.

## When to Use This Skill

I activate when you need help with:
- **Kubernetes deployments**: "Deploy Kafka on Kubernetes", "run Kafka in K8s", "Kafka Helm chart"
- **Operator selection**: "Strimzi vs Confluent Operator", "which Kafka operator to use"
- **StatefulSet patterns**: "Kafka StatefulSet best practices", "persistent volumes for Kafka"
- **Production K8s**: "Production-ready Kafka on K8s", "Kafka high availability in Kubernetes"

## What I Know

### Deployment Options Comparison

| Approach | Difficulty | Production-Ready | Best For |
|----------|-----------|------------------|----------|
| **Strimzi Operator** | Easy | ✅ Yes | Self-managed Kafka on K8s, CNCF project |
| **Confluent Operator** | Medium | ✅ Yes | Enterprise features, Confluent ecosystem |
| **Bitnami Helm Chart** | Easy | ⚠️  Mostly | Quick dev/staging environments |
| **Custom StatefulSet** | Hard | ⚠️  Requires expertise | Full control, custom requirements |

**Recommendation**: **Strimzi Operator** for most production use cases (CNCF project, active community, KRaft support)

## Deployment Approach 1: Strimzi Operator (Recommended)

**Strimzi** is a CNCF Sandbox project providing Kubernetes operators for Apache Kafka.

### Features
- ✅ KRaft mode support (Kafka 3.6+, no ZooKeeper)
- ✅ Declarative Kafka management (CRDs)
- ✅ Automatic rolling upgrades
- ✅ Built-in monitoring (Prometheus metrics)
- ✅ Mirror Maker 2 for replication
- ✅ Kafka Connect integration
- ✅ User and topic management via CRDs

### Installation (Helm)

```bash
# 1. Add Strimzi Helm repository
helm repo add strimzi https://strimzi.io/charts/
helm repo update

# 2. Create namespace
kubectl create namespace kafka

# 3. Install Strimzi Operator
helm install strimzi-kafka-operator strimzi/strimzi-kafka-operator \
  --namespace kafka \
  --set watchNamespaces="{kafka}" \
  --version 0.39.0

# 4. Verify operator is running
kubectl get pods -n kafka
# Output: strimzi-cluster-operator-... Running
```

### Deploy Kafka Cluster (KRaft Mode)

```yaml
# kafka-cluster.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaNodePool
metadata:
  name: kafka-pool
  namespace: kafka
  labels:
    strimzi.io/cluster: my-kafka-cluster
spec:
  replicas: 3
  roles:
    - controller
    - broker
  storage:
    type: jbod
    volumes:
      - id: 0
        type: persistent-claim
        size: 100Gi
        class: fast-ssd
        deleteClaim: false
---
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-kafka-cluster
  namespace: kafka
  annotations:
    strimzi.io/kraft: enabled
    strimzi.io/node-pools: enabled
spec:
  kafka:
    version: 3.7.0
    metadataVersion: 3.7-IV4
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
        authentication:
          type: tls
      - name: external
        port: 9094
        type: loadbalancer
        tls: true
        authentication:
          type: tls

    config:
      default.replication.factor: 3
      min.insync.replicas: 2
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      auto.create.topics.enable: false
      log.retention.hours: 168
      log.segment.bytes: 1073741824
      compression.type: lz4

    resources:
      requests:
        memory: 4Gi
        cpu: "2"
      limits:
        memory: 8Gi
        cpu: "4"

    jvmOptions:
      -Xms: 2048m
      -Xmx: 4096m

    metricsConfig:
      type: jmxPrometheusExporter
      valueFrom:
        configMapKeyRef:
          name: kafka-metrics
          key: kafka-metrics-config.yml
```

```bash
# Apply Kafka cluster
kubectl apply -f kafka-cluster.yaml

# Wait for cluster to be ready (5-10 minutes)
kubectl wait kafka/my-kafka-cluster --for=condition=Ready --timeout=600s -n kafka

# Check status
kubectl get kafka -n kafka
# Output: my-kafka-cluster   3.7.0   3         True
```

### Create Topics (Declaratively)

```yaml
# kafka-topics.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: user-events
  namespace: kafka
  labels:
    strimzi.io/cluster: my-kafka-cluster
spec:
  partitions: 12
  replicas: 3
  config:
    retention.ms: 604800000  # 7 days
    segment.bytes: 1073741824
    compression.type: lz4
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: order-events
  namespace: kafka
  labels:
    strimzi.io/cluster: my-kafka-cluster
spec:
  partitions: 6
  replicas: 3
  config:
    retention.ms: 2592000000  # 30 days
    min.insync.replicas: 2
```

```bash
# Apply topics
kubectl apply -f kafka-topics.yaml

# Verify topics created
kubectl get kafkatopics -n kafka
```

### Create Users (Declaratively)

```yaml
# kafka-users.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaUser
metadata:
  name: my-producer
  namespace: kafka
  labels:
    strimzi.io/cluster: my-kafka-cluster
spec:
  authentication:
    type: tls
  authorization:
    type: simple
    acls:
      - resource:
          type: topic
          name: user-events
          patternType: literal
        operations: [Write, Describe]
      - resource:
          type: topic
          name: order-events
          patternType: literal
        operations: [Write, Describe]
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaUser
metadata:
  name: my-consumer
  namespace: kafka
  labels:
    strimzi.io/cluster: my-kafka-cluster
spec:
  authentication:
    type: tls
  authorization:
    type: simple
    acls:
      - resource:
          type: topic
          name: user-events
          patternType: literal
        operations: [Read, Describe]
      - resource:
          type: group
          name: my-consumer-group
          patternType: literal
        operations: [Read]
```

```bash
# Apply users
kubectl apply -f kafka-users.yaml

# Get user credentials (TLS certificates)
kubectl get secret my-producer -n kafka -o jsonpath='{.data.user\.crt}' | base64 -d > producer.crt
kubectl get secret my-producer -n kafka -o jsonpath='{.data.user\.key}' | base64 -d > producer.key
kubectl get secret my-kafka-cluster-cluster-ca-cert -n kafka -o jsonpath='{.data.ca\.crt}' | base64 -d > ca.crt
```

## Deployment Approach 2: Confluent Operator

**Confluent for Kubernetes (CFK)** provides enterprise-grade Kafka management.

### Features
- ✅ Full Confluent Platform (Kafka, Schema Registry, ksqlDB, Connect)
- ✅ Hybrid deployments (K8s + on-prem)
- ✅ Rolling upgrades with zero downtime
- ✅ Multi-region replication
- ✅ Advanced security (RBAC, encryption)
- ⚠️  Requires Confluent Platform license (paid)

### Installation

```bash
# 1. Add Confluent Helm repository
helm repo add confluentinc https://packages.confluent.io/helm
helm repo update

# 2. Create namespace
kubectl create namespace confluent

# 3. Install Confluent Operator
helm install confluent-operator confluentinc/confluent-for-kubernetes \
  --namespace confluent \
  --version 0.921.11

# 4. Verify
kubectl get pods -n confluent
```

### Deploy Kafka Cluster

```yaml
# kafka-cluster-confluent.yaml
apiVersion: platform.confluent.io/v1beta1
kind: Kafka
metadata:
  name: kafka
  namespace: confluent
spec:
  replicas: 3
  image:
    application: confluentinc/cp-server:7.6.0
    init: confluentinc/confluent-init-container:2.7.0

  dataVolumeCapacity: 100Gi
  storageClass:
    name: fast-ssd

  metricReporter:
    enabled: true

  listeners:
    internal:
      authentication:
        type: plain
      tls:
        enabled: true
    external:
      authentication:
        type: plain
      tls:
        enabled: true

  dependencies:
    zookeeper:
      endpoint: zookeeper.confluent.svc.cluster.local:2181

  podTemplate:
    resources:
      requests:
        memory: 4Gi
        cpu: 2
      limits:
        memory: 8Gi
        cpu: 4
```

```bash
# Apply Kafka cluster
kubectl apply -f kafka-cluster-confluent.yaml

# Wait for cluster
kubectl wait kafka/kafka --for=condition=Ready --timeout=600s -n confluent
```

## Deployment Approach 3: Bitnami Helm Chart (Dev/Staging)

**Bitnami Helm Chart** is simple but less suitable for production.

### Installation

```bash
# 1. Add Bitnami repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# 2. Install Kafka (KRaft mode)
helm install kafka bitnami/kafka \
  --namespace kafka \
  --create-namespace \
  --set kraft.enabled=true \
  --set controller.replicaCount=3 \
  --set broker.replicaCount=3 \
  --set persistence.size=100Gi \
  --set persistence.storageClass=fast-ssd \
  --set metrics.kafka.enabled=true \
  --set metrics.jmx.enabled=true

# 3. Get bootstrap servers
export KAFKA_BOOTSTRAP=$(kubectl get svc kafka -n kafka -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'):9092
```

**Limitations**:
- ⚠️  Less production-ready than Strimzi/Confluent
- ⚠️  Limited declarative topic/user management
- ⚠️  Fewer advanced features (no MirrorMaker 2, limited RBAC)

## Production Best Practices

### 1. Storage Configuration

**Use SSD-backed storage classes** for Kafka logs:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/aws-ebs  # or pd.csi.storage.gke.io for GKE
parameters:
  type: gp3  # AWS EBS GP3 (or io2 for extreme performance)
  iopsPerGB: "50"
  throughput: "125"
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```

**Kafka storage requirements**:
- **Min IOPS**: 3000+ per broker
- **Min Throughput**: 125 MB/s per broker
- **Persistent**: Use `deleteClaim: false` (don't delete data on pod deletion)

### 2. Resource Limits

```yaml
resources:
  requests:
    memory: 4Gi
    cpu: "2"
  limits:
    memory: 8Gi
    cpu: "4"

jvmOptions:
  -Xms: 2048m  # Initial heap (50% of memory request)
  -Xmx: 4096m  # Max heap (50% of memory limit, leave room for OS cache)
```

**Sizing guidelines**:
- **Small (dev)**: 2 CPU, 4Gi memory
- **Medium (staging)**: 4 CPU, 8Gi memory
- **Large (production)**: 8 CPU, 16Gi memory

### 3. Pod Disruption Budgets

Ensure high availability during K8s upgrades:

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: kafka-pdb
  namespace: kafka
spec:
  maxUnavailable: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: kafka
```

### 4. Affinity Rules

**Spread brokers across availability zones**:

```yaml
spec:
  kafka:
    template:
      pod:
        affinity:
          podAntiAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              - labelSelector:
                  matchExpressions:
                    - key: strimzi.io/name
                      operator: In
                      values:
                        - my-kafka-cluster-kafka
                topologyKey: topology.kubernetes.io/zone
```

### 5. Network Policies

**Restrict access to Kafka brokers**:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: kafka-network-policy
  namespace: kafka
spec:
  podSelector:
    matchLabels:
      strimzi.io/name: my-kafka-cluster-kafka
  policyTypes:
    - Ingress
  ingress:
    - from:
      - podSelector:
          matchLabels:
            app: my-producer
      - podSelector:
          matchLabels:
            app: my-consumer
      ports:
      - protocol: TCP
        port: 9092
      - protocol: TCP
        port: 9093
```

## Monitoring Integration

### Prometheus + Grafana Setup

Strimzi provides built-in Prometheus metrics exporter:

```yaml
# kafka-metrics-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kafka-metrics
  namespace: kafka
data:
  kafka-metrics-config.yml: |
    # Use JMX Exporter config from:
    # plugins/specweave-kafka/monitoring/prometheus/kafka-jmx-exporter.yml
    lowercaseOutputName: true
    lowercaseOutputLabelNames: true
    whitelistObjectNames:
      - "kafka.server:type=BrokerTopicMetrics,name=*"
      # ... (copy from kafka-jmx-exporter.yml)
```

```bash
# Apply metrics config
kubectl apply -f kafka-metrics-configmap.yaml

# Install Prometheus Operator (if not already installed)
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace

# Create PodMonitor for Kafka
kubectl apply -f - <<EOF
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: kafka-metrics
  namespace: kafka
spec:
  selector:
    matchLabels:
      strimzi.io/kind: Kafka
  podMetricsEndpoints:
    - port: tcp-prometheus
      interval: 30s
EOF

# Access Grafana dashboards (from kafka-observability skill)
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# Open: http://localhost:3000
# Dashboards: Kafka Cluster Overview, Broker Metrics, Consumer Lag, Topic Metrics, JVM Metrics
```

## Troubleshooting

### "Pods stuck in Pending state"
**Cause**: Insufficient resources or storage class not found
**Fix**:
```bash
# Check events
kubectl describe pod kafka-my-kafka-cluster-0 -n kafka

# Check storage class exists
kubectl get storageclass

# If missing, create fast-ssd storage class (see Production Best Practices above)
```

### "Kafka broker not ready after 10 minutes"
**Cause**: Slow storage provisioning or resource limits too low
**Fix**:
```bash
# Check broker logs
kubectl logs kafka-my-kafka-cluster-0 -n kafka

# Common issues:
# 1. Low IOPS on storage → Use GP3 or better
# 2. Low memory → Increase resources.requests.memory
# 3. KRaft quorum not formed → Check all brokers are running
```

### "Cannot connect to Kafka from outside K8s"
**Cause**: External listener not configured
**Fix**:
```yaml
# Add external listener (Strimzi)
spec:
  kafka:
    listeners:
      - name: external
        port: 9094
        type: loadbalancer
        tls: true
        authentication:
          type: tls

# Get external bootstrap server
kubectl get kafka my-kafka-cluster -n kafka -o jsonpath='{.status.listeners[?(@.name=="external")].bootstrapServers}'
```

## Scaling Operations

### Horizontal Scaling (Add Brokers)

```bash
# Strimzi: Update KafkaNodePool replicas
kubectl patch kafkanodepool kafka-pool -n kafka --type='json' \
  -p='[{"op": "replace", "path": "/spec/replicas", "value": 5}]'

# Confluent: Update Kafka CR
kubectl patch kafka kafka -n confluent --type='json' \
  -p='[{"op": "replace", "path": "/spec/replicas", "value": 5}]'

# Wait for new brokers
kubectl rollout status statefulset/kafka-my-kafka-cluster-kafka -n kafka
```

### Vertical Scaling (Change Resources)

```bash
# Update resources in Kafka CR
kubectl patch kafka my-kafka-cluster -n kafka --type='json' \
  -p='[
    {"op": "replace", "path": "/spec/kafka/resources/requests/memory", "value": "8Gi"},
    {"op": "replace", "path": "/spec/kafka/resources/requests/cpu", "value": "4"}
  ]'

# Rolling restart will happen automatically
```

## Integration with Other Skills

- **kafka-iac-deployment**: Alternative to K8s (use Terraform for cloud-managed Kafka)
- **kafka-observability**: Set up Prometheus + Grafana dashboards for K8s Kafka
- **kafka-architecture**: Cluster sizing and partitioning strategy
- **kafka-cli-tools**: Test K8s Kafka cluster with kcat

## Quick Reference Commands

```bash
# Strimzi
kubectl get kafka -n kafka                    # List Kafka clusters
kubectl get kafkatopics -n kafka              # List topics
kubectl get kafkausers -n kafka               # List users
kubectl logs kafka-my-kafka-cluster-0 -n kafka  # Check broker logs

# Confluent
kubectl get kafka -n confluent                # List Kafka clusters
kubectl get schemaregistry -n confluent       # List Schema Registry
kubectl get ksqldb -n confluent               # List ksqlDB

# Port-forward for testing
kubectl port-forward -n kafka svc/my-kafka-cluster-kafka-bootstrap 9092:9092
```

---

**Next Steps After K8s Deployment**:
1. Use **kafka-observability** skill to verify Prometheus metrics and Grafana dashboards
2. Use **kafka-cli-tools** skill to test cluster with kcat
3. Deploy your producer/consumer applications to K8s
4. Set up GitOps for declarative topic/user management (ArgoCD, Flux)
