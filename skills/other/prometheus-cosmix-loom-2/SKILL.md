---
name: prometheus
description: |
  Prometheus monitoring and alerting for cloud-native observability.

  USE WHEN: Writing PromQL queries, configuring Prometheus scrape targets, creating alerting rules, setting up recording rules, instrumenting applications with Prometheus metrics, configuring service discovery.
  DO NOT USE: For building dashboards (use /grafana), for log analysis (use /logging-observability), for general observability architecture (use senior-software-engineer with infrastructure focus).

  TRIGGERS: metrics, prometheus, promql, counter, gauge, histogram, summary, alert, alertmanager, alerting rule, recording rule, scrape, target, label, service discovery, relabeling, exporter, instrumentation, slo, error budget.
triggers:
  - metrics
  - prometheus
  - promql
  - counter
  - gauge
  - histogram
  - summary
  - alert
  - alertmanager
  - alerting rule
  - recording rule
  - scrape
  - target
  - label
  - service discovery
  - relabeling
  - exporter
  - instrumentation
  - slo
  - error budget
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Prometheus Monitoring and Alerting

## Overview

Prometheus is a powerful open-source monitoring and alerting system designed for reliability and scalability in cloud-native environments. Built for multi-dimensional time-series data with flexible querying via PromQL.

### Architecture Components

- **Prometheus Server**: Core component that scrapes and stores time-series data with local TSDB
- **Alertmanager**: Handles alerts, deduplication, grouping, routing, and notifications to receivers
- **Pushgateway**: Allows ephemeral jobs to push metrics (use sparingly - prefer pull model)
- **Exporters**: Convert metrics from third-party systems to Prometheus format (node, blackbox, etc.)
- **Client Libraries**: Instrument application code (Go, Java, Python, Rust, etc.)
- **Prometheus Operator**: Kubernetes-native deployment and management via CRDs
- **Remote Storage**: Long-term storage via Thanos, Cortex, Mimir for multi-cluster federation

### Data Model

- **Metrics**: Time-series data identified by metric name and key-value labels
- **Format**: `metric_name{label1="value1", label2="value2"} sample_value timestamp`
- **Metric Types**:
  - **Counter**: Monotonically increasing value (requests, errors) - use `rate()` or `increase()` for querying
  - **Gauge**: Value that can go up/down (temperature, memory usage, queue length)
  - **Histogram**: Observations in configurable buckets (latency, request size) - exposes `_bucket`, `_sum`, `_count`
  - **Summary**: Similar to histogram but calculates quantiles client-side - use histograms for aggregation

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

## PromQL Query Patterns

PromQL is the query language for Prometheus. Key concepts: instant vectors, range vectors, scalar, string literals, selectors, operators, functions, and aggregation.

### Selectors and Matchers

```promql
# Instant vector selector (latest sample for each time-series)
http_requests_total

# Filter by label values
http_requests_total{method="GET", status="200"}

# Regex matching (=~) and negative regex (!~)
http_requests_total{status=~"5.."}  # 5xx errors
http_requests_total{endpoint!~"/admin.*"}  # exclude admin endpoints

# Label absence/presence
http_requests_total{job="api", status=""}  # empty label
http_requests_total{job="api", status!=""}  # non-empty label

# Range vector selector (samples over time)
http_requests_total[5m]  # last 5 minutes of samples
```

### Rate Calculations

```promql
# Request rate (requests per second) - ALWAYS use rate() for counters
rate(http_requests_total[5m])

# Sum by service
sum(rate(http_requests_total[5m])) by (service)

# Increase over time window (total count) - for alerts/dashboards showing total
increase(http_requests_total[1h])

# irate() for volatile, fast-moving counters (more sensitive to spikes)
irate(http_requests_total[5m])
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

### Binary Operators and Vector Matching

```promql
# Arithmetic operators (+, -, *, /, %, ^)
node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes

# Comparison operators (==, !=, >, <, >=, <=) - filter to matching values
http_request_duration_seconds > 1

# Logical operators (and, or, unless)
up{job="api"} and rate(http_requests_total[5m]) > 100

# One-to-one matching (default)
method:http_requests:rate5m / method:http_requests:total

# Many-to-one matching with group_left
sum(rate(http_requests_total[5m])) by (instance, method)
  / on(instance) group_left
sum(rate(http_requests_total[5m])) by (instance)

# One-to-many matching with group_right
sum(rate(http_requests_total[5m])) by (instance)
  / on(instance) group_right
sum(rate(http_requests_total[5m])) by (instance, method)
```

### Time Functions and Offsets

```promql
# Compare with previous time period
rate(http_requests_total[5m]) / rate(http_requests_total[5m] offset 1h)

# Day-over-day comparison
http_requests_total - http_requests_total offset 1d

# Time-based filtering
http_requests_total and hour() >= 9 and hour() < 17  # business hours
day_of_week() == 0 or day_of_week() == 6  # weekends

# Timestamp functions
time() - process_start_time_seconds  # uptime in seconds
```

## Service Discovery

Prometheus supports multiple service discovery mechanisms for dynamic environments where targets appear and disappear.

### Static Configuration

```yaml
scrape_configs:
  - job_name: "static-targets"
    static_configs:
      - targets:
          - "host1:9100"
          - "host2:9100"
        labels:
          env: production
          region: us-east-1
```

### File-based Service Discovery

```yaml
scrape_configs:
  - job_name: 'file-sd'
    file_sd_configs:
      - files:
          - '/etc/prometheus/targets/*.json'
          - '/etc/prometheus/targets/*.yml'
        refresh_interval: 30s

# targets/webservers.json
[
  {
    "targets": ["web1:8080", "web2:8080"],
    "labels": {
      "job": "web",
      "env": "prod"
    }
  }
]
```

### Kubernetes Service Discovery

```yaml
scrape_configs:
  # Pod-based discovery
  - job_name: "kubernetes-pods"
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
            - production
            - staging
    relabel_configs:
      # Keep only pods with prometheus.io/scrape=true annotation
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true

      # Extract custom scrape path from annotation
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)

      # Extract custom port from annotation
      - source_labels:
          [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__

      # Add standard Kubernetes labels
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: kubernetes_pod_name

  # Service-based discovery
  - job_name: "kubernetes-services"
    kubernetes_sd_configs:
      - role: service
    relabel_configs:
      - source_labels:
          [__meta_kubernetes_service_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels:
          [__meta_kubernetes_service_annotation_prometheus_io_scheme]
        action: replace
        target_label: __scheme__
        regex: (https?)
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)

  # Node-based discovery (for node exporters)
  - job_name: "kubernetes-nodes"
    kubernetes_sd_configs:
      - role: node
    relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
      - target_label: __address__
        replacement: kubernetes.default.svc:443
      - source_labels: [__meta_kubernetes_node_name]
        regex: (.+)
        target_label: __metrics_path__
        replacement: /api/v1/nodes/${1}/proxy/metrics

  # Endpoints discovery (for service endpoints)
  - job_name: "kubernetes-endpoints"
    kubernetes_sd_configs:
      - role: endpoints
    relabel_configs:
      - source_labels:
          [__meta_kubernetes_service_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_endpoint_port_name]
        action: keep
        regex: metrics
```

### Consul Service Discovery

```yaml
scrape_configs:
  - job_name: "consul-services"
    consul_sd_configs:
      - server: "consul.example.com:8500"
        datacenter: "dc1"
        services: ["web", "api", "cache"]
        tags: ["production"]
    relabel_configs:
      - source_labels: [__meta_consul_service]
        target_label: service
      - source_labels: [__meta_consul_tags]
        target_label: tags
```

### EC2 Service Discovery

```yaml
scrape_configs:
  - job_name: "ec2-instances"
    ec2_sd_configs:
      - region: us-east-1
        access_key: YOUR_ACCESS_KEY
        secret_key: YOUR_SECRET_KEY
        port: 9100
        filters:
          - name: tag:Environment
            values: [production]
          - name: instance-state-name
            values: [running]
    relabel_configs:
      - source_labels: [__meta_ec2_tag_Name]
        target_label: instance_name
      - source_labels: [__meta_ec2_availability_zone]
        target_label: availability_zone
      - source_labels: [__meta_ec2_instance_type]
        target_label: instance_type
```

### DNS Service Discovery

```yaml
scrape_configs:
  - job_name: "dns-srv-records"
    dns_sd_configs:
      - names:
          - "_prometheus._tcp.example.com"
        type: "SRV"
        refresh_interval: 30s
    relabel_configs:
      - source_labels: [__meta_dns_name]
        target_label: instance
```

### Relabeling Actions Reference

| Action      | Description                                        | Use Case                           |
| ----------- | -------------------------------------------------- | ---------------------------------- |
| `keep`      | Keep targets where regex matches source labels     | Filter targets by annotation/label |
| `drop`      | Drop targets where regex matches source labels     | Exclude specific targets           |
| `replace`   | Replace target label with value from source labels | Extract custom labels/paths/ports  |
| `labelmap`  | Map source label names to target labels via regex  | Copy all Kubernetes labels         |
| `labeldrop` | Drop labels matching regex                         | Remove internal metadata labels    |
| `labelkeep` | Keep only labels matching regex                    | Reduce cardinality                 |
| `hashmod`   | Set target label to hash of source labels modulo N | Sharding/routing                   |

## High Availability and Scalability

### Prometheus High Availability Setup

```yaml
# Deploy multiple identical Prometheus instances scraping same targets
# Use external labels to distinguish instances
global:
  external_labels:
    replica: prometheus-1 # Change to prometheus-2, etc.
    cluster: production

# Alertmanager will deduplicate alerts from multiple Prometheus instances
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager-1:9093
            - alertmanager-2:9093
            - alertmanager-3:9093
```

### Alertmanager Clustering

```yaml
# alertmanager.yml - HA cluster configuration
global:
  resolve_timeout: 5m

route:
  receiver: "default"
  group_by: ["alertname", "cluster"]
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h

receivers:
  - name: "default"
    slack_configs:
      - api_url: "https://hooks.slack.com/services/YOUR/WEBHOOK"
        channel: "#alerts"

# Start Alertmanager cluster members
# alertmanager-1: --cluster.peer=alertmanager-2:9094 --cluster.peer=alertmanager-3:9094
# alertmanager-2: --cluster.peer=alertmanager-1:9094 --cluster.peer=alertmanager-3:9094
# alertmanager-3: --cluster.peer=alertmanager-1:9094 --cluster.peer=alertmanager-2:9094
```

### Federation for Hierarchical Monitoring

```yaml
# Global Prometheus federating from regional instances
scrape_configs:
  - job_name: "federate"
    scrape_interval: 15s
    honor_labels: true
    metrics_path: "/federate"
    params:
      "match[]":
        # Pull aggregated metrics only
        - '{job="prometheus"}'
        - '{__name__=~"job:.*"}' # Recording rules
        - "up"
    static_configs:
      - targets:
          - "prometheus-us-east-1:9090"
          - "prometheus-us-west-2:9090"
          - "prometheus-eu-west-1:9090"
        labels:
          region: "us-east-1"
```

### Remote Storage for Long-term Retention

```yaml
# Prometheus remote write to Thanos/Cortex/Mimir
remote_write:
  - url: "http://thanos-receive:19291/api/v1/receive"
    queue_config:
      capacity: 10000
      max_shards: 50
      min_shards: 1
      max_samples_per_send: 5000
      batch_send_deadline: 5s
      min_backoff: 30ms
      max_backoff: 100ms
    write_relabel_configs:
      # Drop high-cardinality metrics before remote write
      - source_labels: [__name__]
        regex: "go_.*"
        action: drop

# Prometheus remote read from long-term storage
remote_read:
  - url: "http://thanos-query:9090/api/v1/read"
    read_recent: true
```

### Thanos Architecture for Global View

```yaml
# Thanos Sidecar - runs alongside Prometheus
thanos sidecar \
  --prometheus.url=http://localhost:9090 \
  --tsdb.path=/prometheus \
  --objstore.config-file=/etc/thanos/bucket.yml \
  --grpc-address=0.0.0.0:10901 \
  --http-address=0.0.0.0:10902

# Thanos Store - queries object storage
thanos store \
  --data-dir=/var/thanos/store \
  --objstore.config-file=/etc/thanos/bucket.yml \
  --grpc-address=0.0.0.0:10901 \
  --http-address=0.0.0.0:10902

# Thanos Query - global query interface
thanos query \
  --http-address=0.0.0.0:9090 \
  --grpc-address=0.0.0.0:10901 \
  --store=prometheus-1-sidecar:10901 \
  --store=prometheus-2-sidecar:10901 \
  --store=thanos-store:10901

# Thanos Compactor - downsample and compact blocks
thanos compact \
  --data-dir=/var/thanos/compact \
  --objstore.config-file=/etc/thanos/bucket.yml \
  --retention.resolution-raw=30d \
  --retention.resolution-5m=90d \
  --retention.resolution-1h=365d
```

### Horizontal Sharding with Hashmod

```yaml
# Split scrape targets across multiple Prometheus instances using hashmod
scrape_configs:
  - job_name: "kubernetes-pods-shard-0"
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      # Hash pod name and keep only shard 0 (mod 3)
      - source_labels: [__meta_kubernetes_pod_name]
        modulus: 3
        target_label: __tmp_hash
        action: hashmod
      - source_labels: [__tmp_hash]
        regex: "0"
        action: keep

  - job_name: "kubernetes-pods-shard-1"
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_name]
        modulus: 3
        target_label: __tmp_hash
        action: hashmod
      - source_labels: [__tmp_hash]
        regex: "1"
        action: keep

  # shard-2 similar pattern...
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

## Quick Reference

### Common PromQL Patterns

```promql
# Request rate per second
rate(http_requests_total[5m])

# Error ratio percentage
100 * sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# P95 latency from histogram
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# Average latency from histogram
sum(rate(http_request_duration_seconds_sum[5m])) / sum(rate(http_request_duration_seconds_count[5m]))

# Memory utilization percentage
100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)

# CPU utilization (non-idle)
100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])))

# Disk space remaining percentage
100 * node_filesystem_avail_bytes / node_filesystem_size_bytes

# Top 5 endpoints by request rate
topk(5, sum(rate(http_requests_total[5m])) by (endpoint))

# Service uptime in days
(time() - process_start_time_seconds) / 86400

# Request rate growth compared to 1 hour ago
rate(http_requests_total[5m]) / rate(http_requests_total[5m] offset 1h)
```

### Alert Rule Patterns

```yaml
# High error rate (symptom-based)
alert: HighErrorRate
expr: |
  sum(rate(http_requests_total{status=~"5.."}[5m]))
  / sum(rate(http_requests_total[5m])) > 0.05
for: 5m
labels:
  severity: critical
annotations:
  summary: "Error rate is {{ $value | humanizePercentage }}"
  runbook: "https://runbooks.example.com/high-error-rate"

# High latency P95
alert: HighLatency
expr: |
  histogram_quantile(0.95,
    sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
  ) > 1
for: 5m
labels:
  severity: warning

# Service down
alert: ServiceDown
expr: up{job="critical-service"} == 0
for: 2m
labels:
  severity: critical

# Disk space low (cause-based, warning only)
alert: DiskSpaceLow
expr: |
  node_filesystem_avail_bytes{mountpoint="/"}
  / node_filesystem_size_bytes{mountpoint="/"} < 0.1
for: 10m
labels:
  severity: warning

# Pod crash looping
alert: PodCrashLooping
expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
for: 5m
labels:
  severity: warning
```

### Recording Rule Naming Convention

```yaml
# Format: level:metric:operations
# level = aggregation level (job, instance, cluster)
# metric = base metric name
# operations = transformations applied (rate5m, sum, ratio)

groups:
  - name: aggregation_rules
    rules:
      # Instance-level aggregation
      - record: instance:node_cpu_utilization:ratio
        expr: 1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)

      # Job-level aggregation
      - record: job:http_requests:rate5m
        expr: sum(rate(http_requests_total[5m])) by (job)

      # Job-level error ratio
      - record: job:http_request_errors:ratio
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (job)
          / sum(rate(http_requests_total[5m])) by (job)

      # Cluster-level aggregation
      - record: cluster:cpu_utilization:ratio
        expr: avg(instance:node_cpu_utilization:ratio)
```

### Metric Naming Best Practices

| Pattern          | Good Example                    | Bad Example                            |
| ---------------- | ------------------------------- | -------------------------------------- |
| Counter suffix   | `http_requests_total`           | `http_requests`                        |
| Base units       | `http_request_duration_seconds` | `http_request_duration_ms`             |
| Ratio range      | `cache_hit_ratio` (0.0-1.0)     | `cache_hit_percentage` (0-100)         |
| Byte units       | `response_size_bytes`           | `response_size_kb`                     |
| Namespace prefix | `myapp_http_requests_total`     | `http_requests_total`                  |
| Label naming     | `{method="GET", status="200"}`  | `{httpMethod="GET", statusCode="200"}` |

### Label Cardinality Guidelines

| Cardinality     | Examples                                 | Recommendation          |
| --------------- | ---------------------------------------- | ----------------------- |
| Low (<10)       | HTTP method, status code, environment    | Safe for all labels     |
| Medium (10-100) | API endpoint, service name, pod name     | Safe with aggregation   |
| High (100-1000) | Container ID, hostname                   | Use only when necessary |
| Unbounded       | User ID, IP address, timestamp, URL path | Never use as label      |

### Kubernetes Annotation-based Scraping

```yaml
# Pod annotations for automatic Prometheus scraping
apiVersion: v1
kind: Pod
metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/metrics"
    prometheus.io/scheme: "http"
spec:
  containers:
    - name: app
      image: myapp:latest
      ports:
        - containerPort: 8080
          name: metrics
```

### Alertmanager Routing Patterns

```yaml
route:
  receiver: default
  group_by: ["alertname", "cluster"]
  routes:
    # Critical alerts to PagerDuty
    - match:
        severity: critical
      receiver: pagerduty
      continue: true # Also send to default

    # Team-based routing
    - match:
        team: database
      receiver: dba-team
      group_by: ["alertname", "instance"]

    # Environment-based routing
    - match:
        env: development
      receiver: slack-dev
      repeat_interval: 4h

    # Time-based routing (office hours only)
    - match:
        severity: warning
      receiver: email
      active_time_intervals:
        - business-hours

time_intervals:
  - name: business-hours
    time_intervals:
      - times:
          - start_time: "09:00"
            end_time: "17:00"
        weekdays: ["monday:friday"]
```

## Additional Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Best Practices](https://prometheus.io/docs/practices/)
- [Alerting Rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)
- [Recording Rules](https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/)
- [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator)
- [Thanos Documentation](https://thanos.io/tip/thanos/getting-started.md/)
- [Google SRE Book - Monitoring](https://sre.google/sre-book/monitoring-distributed-systems/)
