---
name: telemetry
description: CTO observability stack expertise - Prometheus metrics, Loki logs, Grafana dashboards. Use when querying logs, metrics, or debugging via telemetry.
---

# Telemetry Skill

Access the CTO observability stack for logs, metrics, and dashboards.

## When to Use

- Querying pod logs via Loki
- Checking metrics via Prometheus
- Viewing dashboards in Grafana
- Debugging agent failures
- Monitoring Play workflow health

---

## Stack Overview

| Service | Port | Purpose |
|---------|------|---------|
| **Prometheus** | 9090 | Metrics collection and querying |
| **Loki** | 3100 | Log aggregation (like Prometheus for logs) |
| **Grafana** | 3000 | Dashboards and visualization |

### Port Forwards (Required for Local Access)

```bash
kubectl port-forward svc/prometheus-server -n observability 9090:80
kubectl port-forward svc/loki-gateway -n observability 3100:80
kubectl port-forward svc/grafana -n observability 3000:80
```

---

## MCP Tools Available

### Prometheus Tools

| Tool | Purpose |
|------|---------|
| `prometheus_query` | Instant query (current value) |
| `prometheus_query_range` | Range query (time series) |
| `prometheus_labels` | List all label names |
| `prometheus_series` | Find series matching labels |

### Loki Tools

| Tool | Purpose |
|------|---------|
| `loki_query` | Query logs with LogQL |
| `loki_labels` | List all label names |
| `loki_label_values` | Get values for a label |

### Grafana Tools

| Tool | Purpose |
|------|---------|
| `grafana_search_dashboards` | Find dashboards by name |
| `grafana_get_dashboard` | Get dashboard definition |
| `grafana_query_prometheus` | Query Prometheus via Grafana |
| `grafana_query_loki_logs` | Query Loki via Grafana |
| `grafana_list_alert_rules` | List configured alerts |

---

## Loki (Logs)

### LogQL Basics

```logql
# All logs from CTO namespace
{namespace="cto"}

# Filter by pod name
{namespace="cto", pod=~"coderun-.*"}

# Search for errors
{namespace="cto"} |= "error"

# JSON parsing
{namespace="cto"} | json | level="error"

# Regex filter
{namespace="cto"} |~ "tool.*mismatch"
```

### Common Queries for CTO

```logql
# All CodeRun pod logs
{namespace="cto", app="coderun"}

# Morgan intake logs
{namespace="cto", pod=~"intake-.*"}

# Play workflow logs
{namespace="cto", pod=~"play-.*"}

# Errors only
{namespace="cto"} |= "error" | json

# Tool inventory issues (A10)
{namespace="cto"} |~ "tool.*(mismatch|missing)"

# MCP initialization failures (A12)
{namespace="cto"} |~ "mcp.*failed"

# Config issues (A11)
{namespace="cto"} |~ "cto-config.*(missing|invalid)"
```

### Via MCP Tool

```
loki_query(query='{namespace="cto"} |= "error"', limit=100)
```

### Via curl

```bash
curl -G "http://localhost:3100/loki/api/v1/query_range" \
  --data-urlencode 'query={namespace="cto"} |= "error"' \
  --data-urlencode 'limit=100' | jq
```

---

## Prometheus (Metrics)

### PromQL Basics

```promql
# Current CPU usage
container_cpu_usage_seconds_total{namespace="cto"}

# Memory usage
container_memory_usage_bytes{namespace="cto"}

# Rate of requests
rate(http_requests_total{namespace="cto"}[5m])

# Pod restarts
kube_pod_container_status_restarts_total{namespace="cto"}
```

### Common Queries for CTO

```promql
# CodeRun pod count
count(kube_pod_info{namespace="cto", pod=~"coderun-.*"})

# Memory by pod
container_memory_usage_bytes{namespace="cto", container!=""}

# CPU by pod
rate(container_cpu_usage_seconds_total{namespace="cto"}[5m])

# OOM killed containers
kube_pod_container_status_last_terminated_reason{namespace="cto", reason="OOMKilled"}

# Pod restart count
sum(kube_pod_container_status_restarts_total{namespace="cto"}) by (pod)
```

### Via MCP Tool

```
prometheus_query(query='count(kube_pod_info{namespace="cto"})')
```

### Via curl

```bash
curl "http://localhost:9090/api/v1/query" \
  --data-urlencode 'query=kube_pod_info{namespace="cto"}' | jq
```

---

## Grafana (Dashboards)

### Access

- URL: http://localhost:3000
- Default credentials: admin/admin (or configured)

### Common Dashboards

| Dashboard | Purpose |
|-----------|---------|
| Kubernetes / Pods | Pod resource usage |
| Loki / Logs | Log explorer |
| CTO Overview | Platform health (if configured) |

### Via MCP Tool

```
grafana_search_dashboards(query="kubernetes")
grafana_get_dashboard(uid="abc123")
```

---

## kubectl Alternatives

When MCP tools aren't available, use kubectl directly:

### Stream Logs

```bash
# All CTO pods
kubectl logs -n cto -l app.kubernetes.io/part-of=cto -f --tail=100

# Specific CodeRun
kubectl logs -n cto -l app=coderun -f

# With grep
kubectl logs -n cto -l app=coderun -f | grep -E "error|mismatch|failed"
```

### Get Pod Status

```bash
kubectl get pods -n cto -o wide
kubectl describe pod -n cto <pod-name>
```

### Events

```bash
kubectl get events -n cto --sort-by='.lastTimestamp'
```

---

## Healer Integration

Healer uses Loki to watch for patterns:

```rust
// From crates/healer/src/scanner.rs
// Patterns that trigger alerts:
"tool\\s+inventory\\s+mismatch"  // A10
"cto-config.*(missing|invalid)" // A11
"mcp.*failed\\s+to\\s+initialize" // A12
```

### Query Healer-Relevant Logs

```logql
# All Healer detection patterns
{namespace="cto"} |~ "tool.*mismatch|cto-config.*(missing|invalid)|mcp.*failed"
```

---

## Troubleshooting

### No Logs Appearing

1. Check port forward is running: `lsof -i :3100`
2. Verify Loki pods: `kubectl get pods -n observability -l app=loki`
3. Check label: `loki_labels()` to see available labels

### Metrics Not Found

1. Check port forward: `lsof -i :9090`
2. Verify Prometheus: `kubectl get pods -n observability -l app=prometheus`
3. List metrics: `prometheus_labels()` or browse http://localhost:9090/targets

### Grafana Not Loading

1. Check port forward: `lsof -i :3000`
2. Verify pod: `kubectl get pods -n observability -l app.kubernetes.io/name=grafana`

---

## Reference

- [Loki LogQL Documentation](https://grafana.com/docs/loki/latest/logql/)
- [Prometheus PromQL Documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
