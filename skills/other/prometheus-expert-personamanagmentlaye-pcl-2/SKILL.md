---
name: prometheus-expert
version: 1.0.0
description: Expert-level Prometheus monitoring, metrics collection, PromQL queries, alerting, and production operations
category: devops
author: PCL Team
license: Apache-2.0
tags:
  - prometheus
  - monitoring
  - metrics
  - observability
  - alerting
  - promql
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(kubectl:*, promtool:*)
  - Glob
  - Grep
requirements:
  prometheus: ">=2.45"
  kubernetes: ">=1.28"
---

# Prometheus Expert

You are an expert in Prometheus with deep knowledge of metrics collection, PromQL queries, recording rules, alerting rules, service discovery, and production operations. You design and manage comprehensive observability systems following monitoring best practices.

## Core Expertise

### Prometheus Architecture

**Components:**
```
Prometheus Stack:
├── Prometheus Server (TSDB + scraper)
├── Alertmanager (alert routing)
├── Pushgateway (batch jobs)
├── Exporters (metrics exposure)
├── Service Discovery (target discovery)
└── Client Libraries (instrumentation)
```

### Installation on Kubernetes

**Prometheus Operator:**
```bash
# Install with Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=50Gi
```

**Prometheus Config:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      scrape_timeout: 10s
      evaluation_interval: 15s
      external_labels:
        cluster: production
        region: us-east-1

    # Alertmanager configuration
    alerting:
      alertmanagers:
      - static_configs:
        - targets:
          - alertmanager:9093

    # Rule files
    rule_files:
    - /etc/prometheus/rules/*.yml

    # Scrape configurations
    scrape_configs:
    # Prometheus itself
    - job_name: prometheus
      static_configs:
      - targets:
        - localhost:9090

    # Kubernetes API server
    - job_name: kubernetes-apiservers
      kubernetes_sd_configs:
      - role: endpoints
      scheme: https
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      relabel_configs:
      - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
        action: keep
        regex: default;kubernetes;https

    # Kubernetes nodes
    - job_name: kubernetes-nodes
      kubernetes_sd_configs:
      - role: node
      scheme: https
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)

    # Kubernetes pods
    - job_name: kubernetes-pods
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: kubernetes_pod_name
```

### ServiceMonitor (Prometheus Operator)

**ServiceMonitor for Application:**
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp
  namespace: production
  labels:
    app: myapp
    release: prometheus
spec:
  selector:
    matchLabels:
      app: myapp

  namespaceSelector:
    matchNames:
    - production

  endpoints:
  - port: metrics
    path: /metrics
    interval: 30s
    scrapeTimeout: 10s
    relabelings:
    - sourceLabels: [__meta_kubernetes_pod_name]
      targetLabel: pod
    - sourceLabels: [__meta_kubernetes_pod_node_name]
      targetLabel: node
```

**PodMonitor:**
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: myapp-pods
  namespace: production
spec:
  selector:
    matchLabels:
      app: myapp

  podMetricsEndpoints:
  - port: metrics
    path: /metrics
    interval: 30s
    relabelings:
    - sourceLabels: [__meta_kubernetes_pod_name]
      targetLabel: instance
    - sourceLabels: [__meta_kubernetes_pod_container_name]
      targetLabel: container
```

### PromQL Queries

**Basic Queries:**
```promql
# Instant vector - current value
http_requests_total

# Rate of requests (per second over 5m)
rate(http_requests_total[5m])

# Sum by label
sum(rate(http_requests_total[5m])) by (job, method)

# CPU usage percentage
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage percentage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100

# Disk usage percentage
(node_filesystem_size_bytes{mountpoint="/"} - node_filesystem_avail_bytes{mountpoint="/"}) / node_filesystem_size_bytes{mountpoint="/"} * 100
```

**Advanced Queries:**
```promql
# Request latency (95th percentile)
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, job, method)
)

# Error rate
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100

# Requests per second by status code
sum(rate(http_requests_total[5m])) by (status)

# Top 10 endpoints by request count
topk(10, sum(rate(http_requests_total[1h])) by (endpoint))

# Prediction (linear regression)
predict_linear(node_filesystem_free_bytes{mountpoint="/"}[1h], 4 * 3600)

# Aggregation over time
avg_over_time(http_requests_total[1h])
max_over_time(http_requests_total[1h])
min_over_time(http_requests_total[1h])

# Join metrics
rate(http_requests_total[5m]) * on(instance) group_left(node) node_cpu_seconds_total
```

**Kubernetes-Specific Queries:**
```promql
# Pod CPU usage
sum(rate(container_cpu_usage_seconds_total{namespace="production"}[5m])) by (pod)

# Pod memory usage
sum(container_memory_working_set_bytes{namespace="production"}) by (pod)

# Pod restart count
kube_pod_container_status_restarts_total{namespace="production"}

# Available replicas
kube_deployment_status_replicas_available{namespace="production"}

# Pending pods
count(kube_pod_status_phase{phase="Pending"}) by (namespace)

# Node resource usage
sum(kube_pod_container_resource_requests{resource="cpu"}) by (node) /
sum(kube_node_status_allocatable{resource="cpu"}) by (node) * 100
```

### Recording Rules

**Recording Rules Configuration:**
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: recording-rules
  namespace: monitoring
  labels:
    prometheus: kube-prometheus
spec:
  groups:
  - name: api_performance
    interval: 30s
    rules:
    # Request rate by endpoint
    - record: api:http_requests:rate5m
      expr: |
        sum(rate(http_requests_total[5m])) by (job, endpoint, method)

    # Request rate by status
    - record: api:http_requests:rate5m:status
      expr: |
        sum(rate(http_requests_total[5m])) by (job, status)

    # Error rate
    - record: api:http_requests:error_rate5m
      expr: |
        sum(rate(http_requests_total{status=~"5.."}[5m])) by (job) /
        sum(rate(http_requests_total[5m])) by (job)

    # Latency percentiles
    - record: api:http_request_duration:p50
      expr: |
        histogram_quantile(0.50,
          sum(rate(http_request_duration_seconds_bucket[5m])) by (le, job)
        )

    - record: api:http_request_duration:p95
      expr: |
        histogram_quantile(0.95,
          sum(rate(http_request_duration_seconds_bucket[5m])) by (le, job)
        )

    - record: api:http_request_duration:p99
      expr: |
        histogram_quantile(0.99,
          sum(rate(http_request_duration_seconds_bucket[5m])) by (le, job)
        )

  - name: node_resources
    interval: 30s
    rules:
    # Node CPU usage
    - record: instance:node_cpu:utilization
      expr: |
        100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

    # Node memory usage
    - record: instance:node_memory:utilization
      expr: |
        100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))

    # Node disk usage
    - record: instance:node_disk:utilization
      expr: |
        100 * (1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}))
```

### Alerting Rules

**Alerting Rules Configuration:**
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: alerting-rules
  namespace: monitoring
  labels:
    prometheus: kube-prometheus
spec:
  groups:
  - name: application_alerts
    interval: 30s
    rules:
    # High error rate
    - alert: HighErrorRate
      expr: |
        sum(rate(http_requests_total{status=~"5.."}[5m])) by (job) /
        sum(rate(http_requests_total[5m])) by (job) > 0.05
      for: 5m
      labels:
        severity: warning
        team: backend
      annotations:
        summary: "High error rate detected"
        description: "{{ $labels.job }} has error rate of {{ $value | humanizePercentage }}"

    # High latency
    - alert: HighLatency
      expr: |
        histogram_quantile(0.95,
          sum(rate(http_request_duration_seconds_bucket[5m])) by (le, job)
        ) > 1
      for: 10m
      labels:
        severity: warning
        team: backend
      annotations:
        summary: "High latency detected"
        description: "{{ $labels.job }} 95th percentile latency is {{ $value }}s"

    # Service down
    - alert: ServiceDown
      expr: up{job="myapp"} == 0
      for: 1m
      labels:
        severity: critical
        team: platform
      annotations:
        summary: "Service is down"
        description: "{{ $labels.job }} on {{ $labels.instance }} is down"

  - name: infrastructure_alerts
    interval: 30s
    rules:
    # High CPU usage
    - alert: HighCPUUsage
      expr: |
        100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
      for: 10m
      labels:
        severity: warning
        team: platform
      annotations:
        summary: "High CPU usage"
        description: "Instance {{ $labels.instance }} CPU usage is {{ $value }}%"

    # High memory usage
    - alert: HighMemoryUsage
      expr: |
        100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) > 85
      for: 10m
      labels:
        severity: warning
        team: platform
      annotations:
        summary: "High memory usage"
        description: "Instance {{ $labels.instance }} memory usage is {{ $value }}%"

    # Disk space low
    - alert: DiskSpaceLow
      expr: |
        100 * (1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})) > 85
      for: 5m
      labels:
        severity: warning
        team: platform
      annotations:
        summary: "Disk space low"
        description: "Instance {{ $labels.instance }} disk usage is {{ $value }}%"

  - name: kubernetes_alerts
    interval: 30s
    rules:
    # Pod not ready
    - alert: PodNotReady
      expr: kube_pod_status_phase{phase!="Running"} > 0
      for: 5m
      labels:
        severity: warning
        team: platform
      annotations:
        summary: "Pod not ready"
        description: "Pod {{ $labels.namespace }}/{{ $labels.pod }} is in {{ $labels.phase }} state"

    # Pod restart loop
    - alert: PodRestartLoop
      expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
      for: 5m
      labels:
        severity: warning
        team: platform
      annotations:
        summary: "Pod restarting frequently"
        description: "Pod {{ $labels.namespace }}/{{ $labels.pod }} is restarting frequently"

    # Deployment replica mismatch
    - alert: DeploymentReplicaMismatch
      expr: |
        kube_deployment_spec_replicas != kube_deployment_status_replicas_available
      for: 5m
      labels:
        severity: warning
        team: platform
      annotations:
        summary: "Deployment replica mismatch"
        description: "Deployment {{ $labels.namespace }}/{{ $labels.deployment }} has {{ $value }} available replicas"
```

### Alertmanager Configuration

**Alertmanager Config:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: alertmanager-config
  namespace: monitoring
data:
  alertmanager.yml: |
    global:
      resolve_timeout: 5m
      slack_api_url: 'https://hooks.slack.com/services/XXX/YYY/ZZZ'

    route:
      receiver: default
      group_by: ['alertname', 'cluster', 'service']
      group_wait: 10s
      group_interval: 10s
      repeat_interval: 12h

      routes:
      # Critical alerts to PagerDuty
      - match:
          severity: critical
        receiver: pagerduty
        continue: true

      # Platform team alerts
      - match:
          team: platform
        receiver: platform-team

      # Backend team alerts
      - match:
          team: backend
        receiver: backend-team

    receivers:
    - name: default
      slack_configs:
      - channel: '#alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

    - name: pagerduty
      pagerduty_configs:
      - service_key: 'YOUR_PAGERDUTY_KEY'
        description: '{{ .GroupLabels.alertname }}'

    - name: platform-team
      slack_configs:
      - channel: '#platform-alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

    - name: backend-team
      slack_configs:
      - channel: '#backend-alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

    inhibit_rules:
    # Inhibit warning if critical is firing
    - source_match:
        severity: critical
      target_match:
        severity: warning
      equal: ['alertname', 'instance']
```

## Exporters

**Node Exporter (Infrastructure Metrics):**
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-exporter
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: node-exporter
  template:
    metadata:
      labels:
        app: node-exporter
    spec:
      hostNetwork: true
      hostPID: true
      containers:
      - name: node-exporter
        image: prom/node-exporter:latest
        ports:
        - containerPort: 9100
          name: metrics
        args:
        - --path.procfs=/host/proc
        - --path.sysfs=/host/sys
        - --collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)
        volumeMounts:
        - name: proc
          mountPath: /host/proc
          readOnly: true
        - name: sys
          mountPath: /host/sys
          readOnly: true
      volumes:
      - name: proc
        hostPath:
          path: /proc
      - name: sys
        hostPath:
          path: /sys
```

**Custom Application Metrics (Go):**
```go
package main

import (
    "net/http"
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
    httpRequestsTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total number of HTTP requests",
        },
        []string{"method", "endpoint", "status"},
    )

    httpRequestDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name: "http_request_duration_seconds",
            Help: "HTTP request duration in seconds",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "endpoint"},
    )
)

func init() {
    prometheus.MustRegister(httpRequestsTotal)
    prometheus.MustRegister(httpRequestDuration)
}

func main() {
    http.Handle("/metrics", promhttp.Handler())
    http.ListenAndServe(":9090", nil)
}
```

## Best Practices

### 1. Use Recording Rules for Complex Queries
```yaml
# Pre-compute expensive queries
- record: api:http_requests:rate5m
  expr: sum(rate(http_requests_total[5m])) by (job)
```

### 2. Label Cardinality
```promql
# AVOID: High cardinality labels
http_requests_total{user_id="123"}  # BAD

# USE: Low cardinality labels
http_requests_total{endpoint="/api/users"}  # GOOD
```

### 3. Appropriate Retention
```yaml
# Balance storage vs history
retention: 30d  # Production
retention: 7d   # Development
```

### 4. Alert Fatigue Prevention
```yaml
# Use appropriate thresholds and durations
for: 10m  # Avoid flapping
```

### 5. Use Histograms for Latency
```promql
# Better than average
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

## Anti-Patterns

**1. Missing Rate Function:**
```promql
# BAD: Raw counter
http_requests_total

# GOOD: Use rate
rate(http_requests_total[5m])
```

**2. Too Many Labels:**
```promql
# BAD: Unique labels per request
{request_id="abc123"}

# GOOD: Aggregate labels
{endpoint="/api/users"}
```

**3. No Resource Limits:**
```yaml
# GOOD: Set limits
resources:
  limits:
    memory: 4Gi
    cpu: 2
```

## Approach

When implementing Prometheus monitoring:

1. **Start with Golden Signals**: Latency, Traffic, Errors, Saturation
2. **Define SLIs/SLOs**: Service Level Indicators and Objectives
3. **Implement Recording Rules**: Pre-compute complex queries
4. **Set Up Alerting**: Alert on symptoms, not causes
5. **Monitor Prometheus**: Prometheus monitoring itself
6. **Retention Strategy**: Balance storage and history
7. **High Availability**: Run multiple Prometheus instances

Always design monitoring that is actionable, reliable, and maintainable.

## Resources

- Prometheus Documentation: https://prometheus.io/docs/
- PromQL Guide: https://prometheus.io/docs/prometheus/latest/querying/basics/
- Prometheus Operator: https://prometheus-operator.dev/
- Best Practices: https://prometheus.io/docs/practices/
