---
name: prometheus
description: 'Prometheus monitoring and alerting for cloud-native observability. Use
  when implementing metrics collection, PromQL queries, alerting rules, or service
  discovery. Triggers: prometheus, promql, metrics'
---

---
name: prometheus
description: Prometheus monitoring and alerting for cloud-native observability. Use when implementing metrics collection, PromQL queries, alerting rules, or service discovery. Triggers: prometheus, promql, metrics, alertmanager, service discovery, recording rules, alerting, scrape config.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Prometheus Monitoring and Alerting

## Overview

Prometheus is a powerful open-source monitoring and alerting system designed for reliability and scalability in cloud-native environments.

### Architecture Components

- **Prometheus Server**: Core component that scrapes and stores time-series data
- **Alertmanager**: Handles alerts, deduplication, grouping, routing, and notifications
- **Pushgateway**: Allows ephemeral jobs to push metrics (use sparingly)
- **Exporters**: Convert metrics from third-party systems to Prometheus format
- **Client Libraries**: Instrument application code (Go, Java, Python, etc.)
- **Prometheus Operator**: Kubernetes-native deployment and management

### Data Model

- **Metrics**: Time-series data identified by metric name and key-value labels
- **Metric Types**:
  - Counter: Monotonically increasing value (requests, errors)
  - Gauge: Value that can go up/down (temperature, memory usage)
  - Histogram: Observations in configurable buckets (latency, request size)
  - Summary: Similar to histogram but calculates quantiles client-side

## Setup and Configuration

### Basic Prometheus Server Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  scrape_timeout: 10s
  evaluation_interval: 15s
  external_labels:
    cluster: "production"
    region: "us-east-1"

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

# Load rules files
rule_files:
  - "alerts/*.yml"
  - "rules/*.yml"

# Scrape configurations
scrape_configs:
  # Prometheus itself
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  # Application services
  - job_name: "application"
    metrics_path: "/metrics"
    static_configs:
      - targets:
          - "app-1:8080"
          - "app-2:8080"
        labels:
          env: "production"
          team: "backend"

  # Kubernetes service discovery
  - job_name: "kubernetes-pods"
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      # Only scrape pods with prometheus.io/scrape annotation
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      # Use custom metrics path if specified
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      # Use custom port if specified
      - source_labels:
          [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      # Add namespace label
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: kubernetes_namespace
      # Add pod name label
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: kubernetes_pod_name
      # Add service name label
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: replace
        target_label: app

  # Node Exporter for host metrics
  - job_name: "node-exporter"
    static_configs:
      - targets:
          - "node-exporter:9100"
```

### Alertmanager Configuration

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
  pagerduty_url: "https://events.pagerduty.com/v2/enqueue"

# Template files for custom notifications
templates:
  - "/etc/alertmanager/templates/*.tmpl"

# Route alerts to appropriate receivers
route:
  group_by: ["alertname", "cluster", "service"]
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: "default"

  routes:
    # Critical alerts go to PagerDuty
    - match:
        severity: critical
      receiver: "pagerduty"
      continue: true

    # Database alerts to DBA team
    - match:
        team: database
      receiver: "dba-team"
      group_by: ["alertname", "instance"]

    # Development environment alerts
    - match:
        env: development
      receiver: "slack-dev"
      group_wait: 5m
      repeat_interval: 4h

# Inhibition rules (suppress alerts)
inhibit_rules:
  # Suppress warning alerts if critical alert is firing
  - source_match:
      severity: "critical"
    target_match:
      severity: "warning"
    equal: ["alertname", "instance"]

  # Suppress instance alerts if entire service is down
  - source_match:
      alertname: "ServiceDown"
    target_match_re:
      alertname: ".*"
    equal: ["service"]

receivers:
  - name: "default"
    slack_configs:
      - channel: "#alerts"
        title: "Alert: {{ .GroupLabels.alertname }}"
        text: "{{ range .Alerts }}{{ .Annotations.description }}{{ end }}"

  - name: "pagerduty"
    pagerduty_configs:
      - service_key: "YOUR_PAGERDUTY_SERVICE_KEY"
        description: "{{ .GroupLabels.alertname }}"

  - name: "dba-team"
    slack_configs:
      - channel: "#database-alerts"
    email_configs:
      - to: "dba-team@example.com"
        headers:
          Subject: "Database Alert: {{ .GroupLabels.alertname }}"

  - name: "slack-dev"
    slack_configs:
      - channel: "#dev-alerts"
        send_resolved: true
```

## Best Practices

### Metric Naming Conventions

Follow these naming patterns for consistency:

```text
# Format: <namespace>_<subsystem>_<metric>_<unit>

# Counters (always use _total suffix)
http_requests_total
http_request_errors_total
cache_hits_total

# Gauges
memory_usage_bytes
active_connections
queue_size

# Histograms (use _bucket, _sum, _count suffixes automatically)
http_request_duration_seconds
response_size_bytes
db_query_duration_seconds

# Use consistent base units
- seconds for duration (not milliseconds)
- bytes for size (not kilobytes)
- ratio for percentages (0.0-1.0, not 0-100)
```

### Label Cardinality Management

#### DO

```yaml
# Good: Bounded cardinality
http_requests_total{method="GET", status="200", endpoint="/api/users"}

# Good: Reasonable number of label values
db_queries_total{table="users", operation="select"}
```

#### DON'T

```yaml
# Bad: Unbounded cardinality (user IDs, email addresses, timestamps)
http_requests_total{user_id="12345"}
http_requests_total{email="user@example.com"}
http_requests_total{timestamp="1234567890"}

# Bad: High cardinality (full URLs, IP addresses)
http_requests_total{url="/api/users/12345/profile"}
http_requests_total{client_ip="192.168.1.100"}
```

#### Guidelines

- Keep label values to < 10 per label (ideally)
- Total unique time-series per metric should be < 10,000
- Use recording rules to pre-aggregate high-cardinality metrics
- Avoid labels with unbounded values (IDs, timestamps, user input)

### Recording Rules for Performance

Use recording rules to pre-compute expensive queries:

```yaml
# rules/recording_rules.yml
groups:
  - name: performance_rules
    interval: 30s
    rules:
      # Pre-calculate request rates
      - record: job:http_requests:rate5m
        expr: sum(rate(http_requests_total[5m])) by (job)

      # Pre-calculate error rates
      - record: job:http_request_errors:rate5m
        expr: sum(rate(http_request_errors_total[5m])) by (job)

      # Pre-calculate error ratio
      - record: job:http_request_error_ratio:rate5m
        expr: |
          job:http_request_errors:rate5m
          /
          job:http_requests:rate5m

      # Pre-aggregate latency percentiles
      - record: job:http_request_duration_seconds:p95
        expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))

      - record: job:http_request_duration_seconds:p99
        expr: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))

  - name: aggregation_rules
    interval: 1m
    rules:
      # Multi-level aggregation for dashboards
      - record: instance:node_cpu_utilization:ratio
        expr: |
          1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)

      - record: cluster:node_cpu_utilization:ratio
        expr: avg(instance:node_cpu_utilization:ratio)

      # Memory aggregation
      - record: instance:node_memory_utilization:ratio
        expr: |
          1 - (
            node_memory_MemAvailable_bytes
            /
            node_memory_MemTotal_bytes
          )
```

### Alert Design (Symptoms vs Causes)

#### Alert on symptoms (user-facing impact), not causes

```yaml
# alerts/symptom_based.yml
groups:
  - name: symptom_alerts
    rules:
      # GOOD: Alert on user-facing symptoms
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          ) > 0.05
        for: 5m
        labels:
          severity: critical
          team: backend
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }} (threshold: 5%)"
          runbook: "https://wiki.example.com/runbooks/high-error-rate"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          ) > 1
        for: 5m
        labels:
          severity: warning
          team: backend
        annotations:
          summary: "High latency on {{ $labels.service }}"
          description: "P95 latency is {{ $value }}s (threshold: 1s)"
          impact: "Users experiencing slow page loads"

      # GOOD: SLO-based alerting
      - alert: SLOBudgetBurnRate
        expr: |
          (
            1 - (
              sum(rate(http_requests_total{status!~"5.."}[1h]))
              /
              sum(rate(http_requests_total[1h]))
            )
          ) > (14.4 * (1 - 0.999))  # 14.4x burn rate for 99.9% SLO
        for: 5m
        labels:
          severity: critical
          team: sre
        annotations:
          summary: "SLO budget burning too fast"
          description: "At current rate, monthly error budget will be exhausted in {{ $value | humanizeDuration }}"
```

#### Cause-based alerts (use for debugging, not paging)

```yaml
# alerts/cause_based.yml
groups:
  - name: infrastructure_alerts
    rules:
      # Lower severity for infrastructure issues
      - alert: HighMemoryUsage
        expr: |
          (
            node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes
          ) / node_memory_MemTotal_bytes > 0.9
        for: 10m
        labels:
          severity: warning # Not critical unless symptoms appear
          team: infrastructure
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is {{ $value | humanizePercentage }}"

      - alert: DiskSpaceLow
        expr: |
          (
            node_filesystem_avail_bytes{mountpoint="/"}
            /
            node_filesystem_size_bytes{mountpoint="/"}
          ) < 0.1
        for: 5m
        labels:
          severity: warning
          team: infrastructure
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Only {{ $value | humanizePercentage }} disk space remaining"
          action: "Clean up logs or expand disk"
```

### Alert Best Practices

1. **For duration**: Use `for` clause to avoid flapping
2. **Meaningful annotations**: Include summary, description, runbook URL, impact
3. **Proper severity levels**: critical (page immediately), warning (ticket), info (log)
4. **Actionable alerts**: Every alert should require human action
5. **Include context**: Add labels for team ownership, service, environment

## PromQL Examples

### Rate Calculations

```promql
# Request rate (requests per second)
rate(http_requests_total[5m])

# Sum by service
sum(rate(http_requests_total[5m])) by (service)

# Increase over time window (total count)
increase(http_requests_total[1h])
```

### Error Ratios

```promql
# Error rate ratio
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))

# Success rate
sum(rate(http_requests_total{status=~"2.."}[5m]))
/
sum(rate(http_requests_total[5m]))
```

### Histogram Queries

```promql
# P95 latency
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
)

# P50, P95, P99 latency by service
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))

# Average request duration
sum(rate(http_request_duration_seconds_sum[5m])) by (service)
/
sum(rate(http_request_duration_seconds_count[5m])) by (service)
```

### Aggregation Operations

```promql
# Sum across all instances
sum(node_memory_MemTotal_bytes) by (cluster)

# Average CPU usage
avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)

# Maximum value
max(http_request_duration_seconds) by (service)

# Minimum value
min(node_filesystem_avail_bytes) by (instance)

# Count number of instances
count(up == 1) by (job)

# Standard deviation
stddev(http_request_duration_seconds) by (service)
```

### Advanced Queries

```promql
# Top 5 services by request rate
topk(5, sum(rate(http_requests_total[5m])) by (service))

# Bottom 3 instances by available memory
bottomk(3, node_memory_MemAvailable_bytes)

# Predict disk full time (linear regression)
predict_linear(node_filesystem_avail_bytes{mountpoint="/"}[1h], 4 * 3600) < 0

# Compare with 1 day ago
http_requests_total - http_requests_total offset 1d

# Rate of change (derivative)
deriv(node_memory_MemAvailable_bytes[5m])

# Absent metric detection
absent(up{job="critical-service"})
```

### Complex Aggregations

```promql
# Calculate Apdex score (Application Performance Index)
(
  sum(rate(http_request_duration_seconds_bucket{le="0.1"}[5m]))
  +
  sum(rate(http_request_duration_seconds_bucket{le="0.5"}[5m])) * 0.5
)
/
sum(rate(http_request_duration_seconds_count[5m]))

# Multi-window multi-burn-rate SLO
(
  sum(rate(http_requests_total{status=~"5.."}[1h]))
  /
  sum(rate(http_requests_total[1h]))
  > 0.001 * 14.4
)
and
(
  sum(rate(http_requests_total{status=~"5.."}[5m]))
  /
  sum(rate(http_requests_total[5m]))
  > 0.001 * 14.4
)
```

## Kubernetes Integration

### ServiceMonitor for Prometheus Operator

```yaml
# servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: app-metrics
  namespace: monitoring
  labels:
    app: myapp
    release: prometheus
spec:
  # Select services to monitor
  selector:
    matchLabels:
      app: myapp

  # Define namespaces to search
  namespaceSelector:
    matchNames:
      - production
      - staging

  # Endpoint configuration
  endpoints:
    - port: metrics # Service port name
      path: /metrics
      interval: 30s
      scrapeTimeout: 10s

      # Relabeling
      relabelings:
        - sourceLabels: [__meta_kubernetes_pod_name]
          targetLabel: pod
        - sourceLabels: [__meta_kubernetes_namespace]
          targetLabel: namespace

      # Metric relabeling (filter/modify metrics)
      metricRelabelings:
        - sourceLabels: [__name__]
          regex: "go_.*"
          action: drop # Drop Go runtime metrics
        - sourceLabels: [status]
          regex: "[45].."
          targetLabel: error
          replacement: "true"

  # Optional: TLS configuration
  # tlsConfig:
  #   insecureSkipVerify: true
  #   ca:
  #     secret:
  #       name: prometheus-tls
  #       key: ca.crt
```

### PodMonitor for Direct Pod Scraping

```yaml
# podmonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: app-pods
  namespace: monitoring
  labels:
    release: prometheus
spec:
  # Select pods to monitor
  selector:
    matchLabels:
      app: myapp

  # Namespace selection
  namespaceSelector:
    matchNames:
      - production

  # Pod metrics endpoints
  podMetricsEndpoints:
    - port: metrics
      path: /metrics
      interval: 15s

      # Relabeling
      relabelings:
        - sourceLabels: [__meta_kubernetes_pod_label_version]
          targetLabel: version
        - sourceLabels: [__meta_kubernetes_pod_node_name]
          targetLabel: node
```

### PrometheusRule for Alerts and Recording Rules

```yaml
# prometheusrule.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: app-rules
  namespace: monitoring
  labels:
    release: prometheus
    role: alert-rules
spec:
  groups:
    - name: app_alerts
      interval: 30s
      rules:
        - alert: HighErrorRate
          expr: |
            (
              sum(rate(http_requests_total{status=~"5..", app="myapp"}[5m]))
              /
              sum(rate(http_requests_total{app="myapp"}[5m]))
            ) > 0.05
          for: 5m
          labels:
            severity: critical
            team: backend
          annotations:
            summary: "High error rate on {{ $labels.namespace }}/{{ $labels.pod }}"
            description: "Error rate is {{ $value | humanizePercentage }}"
            dashboard: "https://grafana.example.com/d/app-overview"
            runbook: "https://wiki.example.com/runbooks/high-error-rate"

        - alert: PodCrashLooping
          expr: |
            rate(kube_pod_container_status_restarts_total[15m]) > 0
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} is crash looping"
            description: "Container {{ $labels.container }} has restarted {{ $value }} times in 15m"

    - name: app_recording_rules
      interval: 30s
      rules:
        - record: app:http_requests:rate5m
          expr: sum(rate(http_requests_total{app="myapp"}[5m])) by (namespace, pod, method, status)

        - record: app:http_request_duration_seconds:p95
          expr: |
            histogram_quantile(0.95,
              sum(rate(http_request_duration_seconds_bucket{app="myapp"}[5m])) by (le, namespace, pod)
            )
```

### Prometheus Custom Resource

```yaml
# prometheus.yaml
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: prometheus
  namespace: monitoring
spec:
  replicas: 2
  version: v2.45.0

  # Service account for Kubernetes API access
  serviceAccountName: prometheus

  # Select ServiceMonitors
  serviceMonitorSelector:
    matchLabels:
      release: prometheus

  # Select PodMonitors
  podMonitorSelector:
    matchLabels:
      release: prometheus

  # Select PrometheusRules
  ruleSelector:
    matchLabels:
      release: prometheus
      role: alert-rules

  # Resource limits
  resources:
    requests:
      memory: 2Gi
      cpu: 1000m
    limits:
      memory: 4Gi
      cpu: 2000m

  # Storage
  storage:
    volumeClaimTemplate:
      spec:
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: 50Gi
        storageClassName: fast-ssd

  # Retention
  retention: 30d
  retentionSize: 45GB

  # Alertmanager configuration
  alerting:
    alertmanagers:
      - namespace: monitoring
        name: alertmanager
        port: web

  # External labels
  externalLabels:
    cluster: production
    region: us-east-1

  # Security context
  securityContext:
    fsGroup: 2000
    runAsNonRoot: true
    runAsUser: 1000

  # Enable admin API for management operations
  enableAdminAPI: false

  # Additional scrape configs (from Secret)
  additionalScrapeConfigs:
    name: additional-scrape-configs
    key: prometheus-additional.yaml
```

## Application Instrumentation Examples

### Go Application

```go
// main.go
package main

import (
    "net/http"
    "time"

    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
    "github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
    // Counter for total requests
    httpRequestsTotal = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total number of HTTP requests",
        },
        []string{"method", "endpoint", "status"},
    )

    // Histogram for request duration
    httpRequestDuration = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration in seconds",
            Buckets: []float64{.001, .005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10},
        },
        []string{"method", "endpoint"},
    )

    // Gauge for active connections
    activeConnections = promauto.NewGauge(
        prometheus.GaugeOpts{
            Name: "active_connections",
            Help: "Number of active connections",
        },
    )

    // Summary for response sizes
    responseSizeBytes = promauto.NewSummaryVec(
        prometheus.SummaryOpts{
            Name:       "http_response_size_bytes",
            Help:       "HTTP response size in bytes",
            Objectives: map[float64]float64{0.5: 0.05, 0.9: 0.01, 0.99: 0.001},
        },
        []string{"endpoint"},
    )
)

// Middleware to instrument HTTP handlers
func instrumentHandler(endpoint string, handler http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        activeConnections.Inc()
        defer activeConnections.Dec()

        // Wrap response writer to capture status code
        wrapped := &responseWriter{ResponseWriter: w, statusCode: 200}

        handler(wrapped, r)

        duration := time.Since(start).Seconds()
        httpRequestDuration.WithLabelValues(r.Method, endpoint).Observe(duration)
        httpRequestsTotal.WithLabelValues(r.Method, endpoint,
            http.StatusText(wrapped.statusCode)).Inc()
    }
}

type responseWriter struct {
    http.ResponseWriter
    statusCode int
}

func (rw *responseWriter) WriteHeader(code int) {
    rw.statusCode = code
    rw.ResponseWriter.WriteHeader(code)
}

func handleUsers(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    w.Write([]byte(`{"users": []}`))
}

func main() {
    // Register handlers
    http.HandleFunc("/api/users", instrumentHandler("/api/users", handleUsers))
    http.Handle("/metrics", promhttp.Handler())

    // Start server
    http.ListenAndServe(":8080", nil)
}
```

### Python Application (Flask)

```python
# app.py
from flask import Flask, request
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time

app = Flask(__name__)

# Define metrics
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=[.001, .005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10]
)

active_requests = Gauge(
    'active_requests',
    'Number of active requests'
)

# Middleware for instrumentation
@app.before_request
def before_request():
    active_requests.inc()
    request.start_time = time.time()

@app.after_request
def after_request(response):
    active_requests.dec()

    duration = time.time() - request.start_time
    request_duration.labels(
        method=request.method,
        endpoint=request.endpoint or 'unknown'
    ).observe(duration)

    request_count.labels(
        method=request.method,
        endpoint=request.endpoint or 'unknown',
        status=response.status_code
    ).inc()

    return response

@app.route('/metrics')
def metrics():
    return generate_latest()

@app.route('/api/users')
def users():
    return {'users': []}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

## Production Deployment Checklist

- [ ] Set appropriate retention period (balance storage vs history needs)
- [ ] Configure persistent storage with adequate size
- [ ] Enable high availability (multiple Prometheus replicas or federation)
- [ ] Set up remote storage for long-term retention (Thanos, Cortex, Mimir)
- [ ] Configure service discovery for dynamic environments
- [ ] Implement recording rules for frequently-used queries
- [ ] Create symptom-based alerts with proper annotations
- [ ] Set up Alertmanager with appropriate routing and receivers
- [ ] Configure inhibition rules to reduce alert noise
- [ ] Add runbook URLs to all critical alerts
- [ ] Implement proper label hygiene (avoid high cardinality)
- [ ] Monitor Prometheus itself (meta-monitoring)
- [ ] Set up authentication and authorization
- [ ] Enable TLS for scrape targets and remote storage
- [ ] Configure rate limiting for queries
- [ ] Test alert and recording rule validity (`promtool check rules`)
- [ ] Implement backup and disaster recovery procedures
- [ ] Document metric naming conventions for the team
- [ ] Create dashboards in Grafana for common queries
- [ ] Set up log aggregation alongside metrics (Loki)

## Troubleshooting Commands

```bash
# Check Prometheus configuration syntax
promtool check config prometheus.yml

# Check rules file syntax
promtool check rules alerts/*.yml

# Test PromQL queries
promtool query instant http://localhost:9090 'up'

# Check which targets are up
curl http://localhost:9090/api/v1/targets

# Query current metric values
curl 'http://localhost:9090/api/v1/query?query=up'

# Check service discovery
curl http://localhost:9090/api/v1/targets/metadata

# View TSDB stats
curl http://localhost:9090/api/v1/status/tsdb

# Check runtime information
curl http://localhost:9090/api/v1/status/runtimeinfo
```

## Additional Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Best Practices](https://prometheus.io/docs/practices/)
- [Alerting Rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)
- [Recording Rules](https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/)
- [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator)
