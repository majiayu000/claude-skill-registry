---
name: kafka-observability
description: Kafka monitoring and observability expert for Prometheus, Grafana, and JMX metrics. Use when setting up Kafka monitoring, configuring alerting rules, or building performance dashboards.
---

# Kafka Monitoring & Observability

Expert guidance for implementing comprehensive monitoring and observability for Apache Kafka using Prometheus and Grafana.

## When to Use This Skill

I activate when you need help with:
- **Monitoring setup**: "Set up Kafka monitoring", "configure Prometheus for Kafka", "Grafana dashboards for Kafka"
- **Metrics collection**: "Kafka JMX metrics", "export Kafka metrics to Prometheus"
- **Alerting**: "Kafka alerting rules", "alert on under-replicated partitions", "critical Kafka metrics"
- **Troubleshooting**: "Monitor Kafka performance", "track consumer lag", "broker health monitoring"

## What I Know

### Available Monitoring Components

This plugin provides a complete monitoring stack:

#### 1. **Prometheus JMX Exporter Configuration**
- **Location**: `plugins/specweave-kafka/monitoring/prometheus/kafka-jmx-exporter.yml`
- **Purpose**: Export Kafka JMX metrics to Prometheus format
- **Metrics Exported**:
  - Broker topic metrics (bytes in/out, messages in, request rate)
  - Replica manager (under-replicated partitions, ISR shrinks/expands)
  - Controller metrics (active controller, offline partitions, leader elections)
  - Request metrics (produce/fetch latency)
  - Log metrics (flush rate, flush latency)
  - JVM metrics (heap, GC, threads, file descriptors)

#### 2. **Grafana Dashboards** (5 Dashboards)
- **Location**: `plugins/specweave-kafka/monitoring/grafana/dashboards/`
- **Dashboards**:
  1. **kafka-cluster-overview.json** - Cluster health and throughput
  2. **kafka-broker-metrics.json** - Per-broker performance
  3. **kafka-consumer-lag.json** - Consumer lag monitoring
  4. **kafka-topic-metrics.json** - Topic-level metrics
  5. **kafka-jvm-metrics.json** - JVM health (heap, GC, threads)

#### 3. **Grafana Provisioning**
- **Location**: `plugins/specweave-kafka/monitoring/grafana/provisioning/`
- **Files**:
  - `dashboards/kafka.yml` - Dashboard provisioning config
  - `datasources/prometheus.yml` - Prometheus datasource config

## Setup Workflow 1: JMX Exporter (Self-Hosted Kafka)

For Kafka running on VMs or bare metal (non-Kubernetes).

### Step 1: Download JMX Prometheus Agent

```bash
# Download JMX Prometheus agent JAR
cd /opt
wget https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.20.0/jmx_prometheus_javaagent-0.20.0.jar

# Copy JMX Exporter config
cp plugins/specweave-kafka/monitoring/prometheus/kafka-jmx-exporter.yml /opt/kafka-jmx-exporter.yml
```

### Step 2: Configure Kafka Broker

Add JMX exporter to Kafka startup script:

```bash
# Edit Kafka startup (e.g., /etc/systemd/system/kafka.service)
[Service]
Environment="KAFKA_OPTS=-javaagent:/opt/jmx_prometheus_javaagent-0.20.0.jar=7071:/opt/kafka-jmx-exporter.yml"
```

Or add to `kafka-server-start.sh`:

```bash
export KAFKA_OPTS="-javaagent:/opt/jmx_prometheus_javaagent-0.20.0.jar=7071:/opt/kafka-jmx-exporter.yml"
```

### Step 3: Restart Kafka and Verify

```bash
# Restart Kafka broker
sudo systemctl restart kafka

# Verify JMX exporter is running (port 7071)
curl localhost:7071/metrics | grep kafka_server

# Expected output: kafka_server_broker_topic_metrics_bytesin_total{...} 12345
```

### Step 4: Configure Prometheus Scraping

Add Kafka brokers to Prometheus config:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'kafka'
    static_configs:
      - targets:
        - 'kafka-broker-1:7071'
        - 'kafka-broker-2:7071'
        - 'kafka-broker-3:7071'
    scrape_interval: 30s
```

```bash
# Reload Prometheus
sudo systemctl reload prometheus

# OR send SIGHUP
kill -HUP $(pidof prometheus)

# Verify scraping
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | select(.job=="kafka")'
```

## Setup Workflow 2: Strimzi (Kubernetes)

For Kafka running on Kubernetes with Strimzi Operator.

### Step 1: Create JMX Exporter ConfigMap

```bash
# Create ConfigMap from JMX exporter config
kubectl create configmap kafka-metrics \
  --from-file=kafka-metrics-config.yml=plugins/specweave-kafka/monitoring/prometheus/kafka-jmx-exporter.yml \
  -n kafka
```

### Step 2: Configure Kafka CR with Metrics

```yaml
# kafka-cluster.yaml (add metricsConfig section)
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-kafka-cluster
  namespace: kafka
spec:
  kafka:
    version: 3.7.0
    replicas: 3

    # ... other config ...

    metricsConfig:
      type: jmxPrometheusExporter
      valueFrom:
        configMapKeyRef:
          name: kafka-metrics
          key: kafka-metrics-config.yml
```

```bash
# Apply updated Kafka CR
kubectl apply -f kafka-cluster.yaml

# Verify metrics endpoint (wait for rolling restart)
kubectl exec -it kafka-my-kafka-cluster-0 -n kafka -- curl localhost:9404/metrics | grep kafka_server
```

### Step 3: Install Prometheus Operator (if not installed)

```bash
# Add Prometheus Community Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install kube-prometheus-stack (Prometheus + Grafana + Alertmanager)
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
  --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false
```

### Step 4: Create PodMonitor for Kafka

```yaml
# kafka-podmonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: kafka-metrics
  namespace: kafka
  labels:
    app: strimzi
spec:
  selector:
    matchLabels:
      strimzi.io/kind: Kafka
  podMetricsEndpoints:
    - port: tcp-prometheus
      interval: 30s
```

```bash
# Apply PodMonitor
kubectl apply -f kafka-podmonitor.yaml

# Verify Prometheus is scraping Kafka
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
# Open: http://localhost:9090/targets
# Should see kafka-metrics/* targets
```

## Setup Workflow 3: Grafana Dashboards

### Installation (Docker Compose)

If using Docker Compose for local development:

```yaml
# docker-compose.yml (add to existing Kafka setup)
version: '3.8'
services:
  # ... Kafka services ...

  prometheus:
    image: prom/prometheus:v2.48.0
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana:10.2.0
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
      - ./monitoring/grafana/dashboards:/var/lib/grafana/dashboards
      - grafana-data:/var/lib/grafana

volumes:
  prometheus-data:
  grafana-data:
```

```bash
# Start monitoring stack
docker-compose up -d prometheus grafana

# Access Grafana
# URL: http://localhost:3000
# Username: admin
# Password: admin
```

### Installation (Kubernetes)

Dashboards are auto-provisioned if using kube-prometheus-stack:

```bash
# Create ConfigMaps for each dashboard
for dashboard in plugins/specweave-kafka/monitoring/grafana/dashboards/*.json; do
  name=$(basename "$dashboard" .json)
  kubectl create configmap "kafka-dashboard-$name" \
    --from-file="$dashboard" \
    -n monitoring \
    --dry-run=client -o yaml | kubectl apply -f -
done

# Label ConfigMaps for Grafana auto-discovery
kubectl label configmap -n monitoring kafka-dashboard-* grafana_dashboard=1

# Grafana will auto-import dashboards (wait 30-60 seconds)

# Access Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# URL: http://localhost:3000
# Username: admin
# Password: prom-operator (default kube-prometheus-stack password)
```

### Manual Dashboard Import

If auto-provisioning doesn't work:

```bash
# 1. Access Grafana UI
# 2. Go to: Dashboards → Import
# 3. Upload JSON files from:
#    plugins/specweave-kafka/monitoring/grafana/dashboards/

# Or use Grafana API
for dashboard in plugins/specweave-kafka/monitoring/grafana/dashboards/*.json; do
  curl -X POST http://admin:admin@localhost:3000/api/dashboards/db \
    -H "Content-Type: application/json" \
    -d @"$dashboard"
done
```

## Dashboard Overview

### 1. **Kafka Cluster Overview** (`kafka-cluster-overview.json`)

**Purpose**: High-level cluster health

**Key Metrics**:
- Active Controller Count (should be exactly 1)
- Under-Replicated Partitions (should be 0) ⚠️  CRITICAL
- Offline Partitions Count (should be 0) ⚠️  CRITICAL
- Unclean Leader Elections (should be 0)
- Cluster Throughput (bytes in/out per second)
- Request Rate (produce, fetch requests per second)
- ISR Changes (shrinks/expands)
- Leader Election Rate

**Use When**: Checking overall cluster health

### 2. **Kafka Broker Metrics** (`kafka-broker-metrics.json`)

**Purpose**: Per-broker performance

**Key Metrics**:
- Broker CPU Usage (% utilization)
- Broker Heap Memory Usage
- Broker Network Throughput (bytes in/out)
- Request Handler Idle Percentage (low = CPU saturation)
- File Descriptors (open vs max)
- Log Flush Latency (p50, p99)
- JVM GC Collection Count/Time

**Use When**: Investigating broker performance issues

### 3. **Kafka Consumer Lag** (`kafka-consumer-lag.json`)

**Purpose**: Consumer lag monitoring

**Key Metrics**:
- Consumer Lag per Topic/Partition
- Total Lag per Consumer Group
- Offset Commit Rate
- Current Consumer Offset
- Log End Offset (producer offset)
- Consumer Group Members

**Use When**: Troubleshooting slow consumers or lag spikes

### 4. **Kafka Topic Metrics** (`kafka-topic-metrics.json`)

**Purpose**: Topic-level metrics

**Key Metrics**:
- Messages Produced per Topic
- Bytes per Topic (in/out)
- Partition Count per Topic
- Replication Factor
- In-Sync Replicas
- Log Size per Partition
- Current Offset per Partition
- Partition Leader Distribution

**Use When**: Analyzing topic throughput and hotspots

### 5. **Kafka JVM Metrics** (`kafka-jvm-metrics.json`)

**Purpose**: JVM health monitoring

**Key Metrics**:
- Heap Memory Usage (used vs max)
- Heap Utilization Percentage
- GC Collection Rate (collections/sec)
- GC Collection Time (ms/sec)
- JVM Thread Count
- Heap Memory by Pool (young gen, old gen, survivor)
- Off-Heap Memory Usage (metaspace, code cache)
- GC Pause Time Percentiles (p50, p95, p99)

**Use When**: Investigating memory leaks or GC pauses

## Critical Alerts Configuration

Create Prometheus alerting rules for critical Kafka metrics:

```yaml
# kafka-alerts.yml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: kafka-alerts
  namespace: monitoring
spec:
  groups:
    - name: kafka.rules
      interval: 30s
      rules:
        # CRITICAL: Under-Replicated Partitions
        - alert: KafkaUnderReplicatedPartitions
          expr: sum(kafka_server_replica_manager_under_replicated_partitions) > 0
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "Kafka has under-replicated partitions"
            description: "{{ $value }} partitions are under-replicated. Data loss risk!"

        # CRITICAL: Offline Partitions
        - alert: KafkaOfflinePartitions
          expr: kafka_controller_offline_partitions_count > 0
          for: 1m
          labels:
            severity: critical
          annotations:
            summary: "Kafka has offline partitions"
            description: "{{ $value }} partitions are offline. Service degradation!"

        # CRITICAL: No Active Controller
        - alert: KafkaNoActiveController
          expr: kafka_controller_active_controller_count == 0
          for: 1m
          labels:
            severity: critical
          annotations:
            summary: "No active Kafka controller"
            description: "Cluster has no active controller. Cannot perform administrative operations!"

        # WARNING: High Consumer Lag
        - alert: KafkaConsumerLagHigh
          expr: sum by (consumergroup) (kafka_consumergroup_lag) > 10000
          for: 10m
          labels:
            severity: warning
          annotations:
            summary: "Consumer group {{ $labels.consumergroup }} has high lag"
            description: "Lag is {{ $value }} messages. Consumers may be slow."

        # WARNING: High CPU Usage
        - alert: KafkaBrokerHighCPU
          expr: os_process_cpu_load{job="kafka"} > 0.8
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "Broker {{ $labels.instance }} has high CPU usage"
            description: "CPU usage is {{ $value | humanizePercentage }}. Consider scaling."

        # WARNING: Low Heap Memory
        - alert: KafkaBrokerLowHeapMemory
          expr: jvm_memory_heap_used_bytes{job="kafka"} / jvm_memory_heap_max_bytes{job="kafka"} > 0.9
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "Broker {{ $labels.instance }} has low heap memory"
            description: "Heap usage is {{ $value | humanizePercentage }}. Risk of OOM!"

        # WARNING: High GC Time
        - alert: KafkaBrokerHighGCTime
          expr: rate(jvm_gc_collection_time_ms_total{job="kafka"}[5m]) > 500
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "Broker {{ $labels.instance }} spending too much time in GC"
            description: "GC time is {{ $value }}ms/sec. Application pauses likely."
```

```bash
# Apply alerts (Kubernetes)
kubectl apply -f kafka-alerts.yml

# Verify alerts loaded
kubectl get prometheusrules -n monitoring
```

## Troubleshooting

### "Prometheus not scraping Kafka metrics"

**Symptoms**: No Kafka metrics in Prometheus

**Fix**:
```bash
# 1. Verify JMX exporter is running
curl http://kafka-broker:7071/metrics

# 2. Check Prometheus targets
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | select(.job=="kafka")'

# 3. Check Prometheus logs
kubectl logs -n monitoring prometheus-kube-prometheus-prometheus-0

# Common issues:
# - Firewall blocking port 7071
# - Incorrect scrape config
# - Kafka broker not running
```

### "Grafana dashboards not loading"

**Symptoms**: Dashboards show "No data"

**Fix**:
```bash
# 1. Verify Prometheus datasource
# Grafana UI → Configuration → Data Sources → Prometheus → Test

# 2. Check if Kafka metrics exist in Prometheus
# Prometheus UI → Graph → Enter: kafka_server_broker_topic_metrics_bytesin_total

# 3. Verify dashboard queries match your Prometheus job name
# Dashboard panels use job="kafka" by default
# If your job name is different, update dashboard JSON
```

### "Consumer lag metrics missing"

**Symptoms**: Consumer lag dashboard empty

**Fix**:
Consumer lag metrics require **Kafka Exporter** (separate from JMX Exporter):

```bash
# Install Kafka Exporter (Kubernetes)
helm install kafka-exporter prometheus-community/prometheus-kafka-exporter \
  --namespace monitoring \
  --set kafkaServer={kafka-bootstrap:9092}

# Or run as Docker container
docker run -d -p 9308:9308 \
  danielqsj/kafka-exporter \
  --kafka.server=kafka:9092 \
  --web.listen-address=:9308

# Add to Prometheus scrape config
scrape_configs:
  - job_name: 'kafka-exporter'
    static_configs:
      - targets: ['kafka-exporter:9308']
```

## Integration with Other Skills

- **kafka-iac-deployment**: Set up monitoring during Terraform deployment
- **kafka-kubernetes**: Configure monitoring for Strimzi Kafka on K8s
- **kafka-architecture**: Use cluster sizing metrics to validate capacity planning
- **kafka-cli-tools**: Use kcat to generate test traffic and verify metrics

## Quick Reference Commands

```bash
# Check JMX exporter metrics
curl http://localhost:7071/metrics | grep -E "(kafka_server|kafka_controller)"

# Prometheus query examples
curl -g 'http://localhost:9090/api/v1/query?query=kafka_server_replica_manager_under_replicated_partitions'

# Grafana dashboard export
curl http://admin:admin@localhost:3000/api/dashboards/uid/kafka-cluster-overview | jq .dashboard > backup.json

# Reload Prometheus config
kill -HUP $(pidof prometheus)

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | select(.job=="kafka")'
```

---

**Next Steps After Monitoring Setup**:
1. Review all 5 Grafana dashboards to familiarize yourself with metrics
2. Set up alerting (Slack, PagerDuty, email)
3. Create runbooks for critical alerts (under-replicated partitions, offline partitions, no controller)
4. Monitor for 7 days to establish baseline metrics
5. Tune JVM settings based on GC metrics
