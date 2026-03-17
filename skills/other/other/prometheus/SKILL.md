---
name: prometheus
model: fast
version: 1.0.0
description: >
  Prometheus monitoring — scrape configuration, service discovery, recording
  rules, alert rules, and production deployment for infrastructure and
  application metrics.
category: devops
tags: [prometheus, monitoring, metrics, alerting, observability]
author: skills-factory
---

# Prometheus

Production Prometheus setup covering scrape configuration, service discovery,
recording rules, alert rules, and operational best practices for infrastructure
and application monitoring.

## When to Use

| Scenario | Example |
|----------|---------|
| Set up metrics collection | New service needs Prometheus scraping |
| Configure service discovery | K8s pods, file-based, or static targets |
| Create recording rules | Pre-compute expensive PromQL queries |
| Design alert rules | SLO-based alerts for availability and latency |
| Production deployment | HA setup with retention and storage planning |
| Troubleshoot scraping | Targets down, metrics missing, relabeling issues |

## Architecture

```
Applications ──(/metrics)──→ Prometheus Server ──→ AlertManager → Slack/PD
      ↑                           │
  client libraries          ├──→ Grafana (dashboards)
  (prom client)             └──→ Thanos/Cortex (long-term storage)
```

## Installation

### Kubernetes (Helm)

```bash
helm repo add prometheus-community \
  https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageVolumeSize=50Gi
```

## Core Configuration

### prometheus.yml

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: production
    region: us-west-2

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]

rule_files:
  - /etc/prometheus/rules/*.yml

scrape_configs:
  # Self-monitoring
  - job_name: prometheus
    static_configs:
      - targets: ["localhost:9090"]

  # Node exporters
  - job_name: node-exporter
    static_configs:
      - targets: ["node1:9100", "node2:9100", "node3:9100"]
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
        regex: "([^:]+)(:[0-9]+)?"
        replacement: "${1}"

  # Application metrics (TLS)
  - job_name: my-app
    scheme: https
    metrics_path: /metrics
    tls_config:
      ca_file: /etc/prometheus/ca.crt
    static_configs:
      - targets: ["app1:9090", "app2:9090"]
```

## Service Discovery

### Kubernetes Pods (Annotation-Based)

```yaml
scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels:
          [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels:
          [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels:
          [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod
```

**Pod annotations to enable scraping:**

```yaml
metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    prometheus.io/path: "/metrics"
```

### File-Based Discovery

```yaml
scrape_configs:
  - job_name: file-sd
    file_sd_configs:
      - files: ["/etc/prometheus/targets/*.json"]
        refresh_interval: 5m
```

**targets/production.json:**

```json
[{
  "targets": ["app1:9090", "app2:9090"],
  "labels": { "env": "production", "service": "api" }
}]
```

### Discovery Method Comparison

| Method | Best For | Dynamic |
|--------|----------|---------|
| `static_configs` | Fixed infrastructure, dev | No |
| `file_sd_configs` | CM-managed inventories | Yes (file watch) |
| `kubernetes_sd_configs` | K8s workloads | Yes (API watch) |
| `consul_sd_configs` | Consul service mesh | Yes (Consul watch) |
| `ec2_sd_configs` | AWS EC2 instances | Yes (API poll) |

## Recording Rules

Pre-compute expensive queries for dashboard and alert performance:

```yaml
# /etc/prometheus/rules/recording_rules.yml
groups:
  - name: api_metrics
    interval: 15s
    rules:
      - record: job:http_requests:rate5m
        expr: sum by (job) (rate(http_requests_total[5m]))

      - record: job:http_errors:rate5m
        expr: sum by (job) (rate(http_requests_total{status=~"5.."}[5m]))

      - record: job:http_error_rate:ratio
        expr: job:http_errors:rate5m / job:http_requests:rate5m

      - record: job:http_duration:p95
        expr: >
          histogram_quantile(0.95,
            sum by (job, le) (rate(http_request_duration_seconds_bucket[5m]))
          )

  - name: resource_metrics
    interval: 30s
    rules:
      - record: instance:node_cpu:utilization
        expr: >
          100 - (avg by (instance)
            (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

      - record: instance:node_memory:utilization
        expr: >
          100 - ((node_memory_MemAvailable_bytes
            / node_memory_MemTotal_bytes) * 100)

      - record: instance:node_disk:utilization
        expr: >
          100 - ((node_filesystem_avail_bytes
            / node_filesystem_size_bytes) * 100)
```

### Naming Convention

```
level:metric_name:operations
```

| Part | Example | Meaning |
|------|---------|---------|
| level | `job:`, `instance:` | Aggregation level |
| metric_name | `http_requests` | Base metric |
| operations | `:rate5m`, `:ratio` | Applied functions |

## Alert Rules

```yaml
# /etc/prometheus/rules/alert_rules.yml
groups:
  - name: availability
    rules:
      - alert: ServiceDown
        expr: up{job="my-app"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "{{ $labels.instance }} is down"
          description: "{{ $labels.job }} down for >1 minute"

      - alert: HighErrorRate
        expr: job:http_error_rate:ratio > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Error rate {{ $value | humanizePercentage }} for {{ $labels.job }}"

      - alert: HighP95Latency
        expr: job:http_duration:p95 > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "P95 latency {{ $value }}s for {{ $labels.job }}"

  - name: resources
    rules:
      - alert: HighCPU
        expr: instance:node_cpu:utilization > 80
        for: 5m
        labels: { severity: warning }
        annotations:
          summary: "CPU {{ $value }}% on {{ $labels.instance }}"

      - alert: HighMemory
        expr: instance:node_memory:utilization > 85
        for: 5m
        labels: { severity: warning }
        annotations:
          summary: "Memory {{ $value }}% on {{ $labels.instance }}"

      - alert: DiskSpaceLow
        expr: instance:node_disk:utilization > 90
        for: 5m
        labels: { severity: critical }
        annotations:
          summary: "Disk {{ $value }}% on {{ $labels.instance }}"
```

### Alert Severity Guide

| Severity | Threshold | Response |
|----------|-----------|----------|
| `critical` | Service down, data loss risk | Page on-call immediately |
| `warning` | Degraded, approaching limit | Investigate within hours |
| `info` | Notable but not urgent | Review in next business day |

## Validation

```bash
# Validate config syntax
promtool check config prometheus.yml

# Validate rule files
promtool check rules /etc/prometheus/rules/*.yml

# Test a query
promtool query instant http://localhost:9090 'up'

# Reload config without restart
curl -X POST http://localhost:9090/-/reload
```

## Best Practices

| Practice | Detail |
|----------|--------|
| Naming: `prefix_name_unit` | Snake_case, `_total` for counters, `_seconds`/`_bytes` for units |
| Scrape intervals 15–60s | Shorter wastes resources and storage |
| Recording rules for dashboards | Pre-compute anything queried repeatedly |
| Monitor Prometheus itself | `prometheus_tsdb_*`, `scrape_duration_seconds` |
| HA deployment | 2+ instances scraping same targets |
| Retention planning | Match `--storage.tsdb.retention.time` to disk capacity |
| Federation for scale | Global Prometheus aggregates from regional instances |
| Long-term storage | Thanos or Cortex for >30d retention |

## Troubleshooting Quick Reference

| Problem | Diagnosis | Fix |
|---------|-----------|-----|
| Target shows `DOWN` | Check `/targets` page for error | Fix firewall, verify endpoint, check TLS |
| Metrics missing | Query `up{job="x"}` | Verify scrape config, check `/metrics` endpoint |
| High cardinality | `prometheus_tsdb_head_series` growing | Drop high-cardinality labels with `metric_relabel_configs` |
| Storage filling up | Check `prometheus_tsdb_storage_*` | Reduce retention, add disk, enable compaction |
| Slow queries | Check `prometheus_engine_query_duration_seconds` | Add recording rules, reduce range, limit series |
| Config not applied | Check `prometheus_config_last_reload_successful` | Fix syntax, POST `/-/reload` |

## NEVER Do

| Anti-Pattern | Why | Do Instead |
|-------------|-----|------------|
| Scrape interval < 5s | Overwhelms targets and storage | Use 15–60s intervals |
| High-cardinality labels (user ID, request ID) | Explodes TSDB series count | Use logs for high-cardinality data |
| Alert without `for` duration | Fires on transient spikes | Always set `for: 1m` minimum |
| Skip recording rules | Dashboards compute expensive queries every load | Pre-compute with recording rules |
| Store secrets in prometheus.yml | Config often in Git | Use file-based secrets or env substitution |
| Ignore `up` metric | Miss targets silently going down | Alert on `up == 0` for all jobs |
| Single Prometheus instance in prod | Single point of failure | Run 2+ replicas with shared targets |
| Unbounded retention | Disk fills, Prometheus crashes | Set explicit `--storage.tsdb.retention.time` |

## Templates

| Template | Description |
|----------|-------------|
| [templates/prometheus.yml](templates/prometheus.yml) | Full config with static, file-based, and K8s discovery |
| [templates/alert-rules.yml](templates/alert-rules.yml) | 25+ alert rules by category |
| [templates/recording-rules.yml](templates/recording-rules.yml) | Pre-computed metrics for HTTP, latency, resources, SLOs |
