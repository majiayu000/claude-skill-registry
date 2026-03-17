---
name: prom-query
version: 1.0.2
description: "Prometheus Metrics Query & Alert Interpreter — query metrics, interpret timeseries, triage alerts"
author: Anvil AI
license: MIT
tags: [prometheus, metrics, monitoring, alerting, observability, thanos, mimir, victoriametrics, grafana, discord, discord-v2]
tools:
  - name: prom-query
    description: "Query Prometheus metrics, alerts, targets, and rules via the HTTP API"
    command: bash scripts/prom-query.sh
    args: "[command] [args...]"
    env:
      - PROMETHEUS_URL: "Base URL of Prometheus server (required)"
      - PROMETHEUS_TOKEN: "Bearer token for authentication (optional)"
---

# prom-query — Prometheus Metrics Query & Alert Interpreter

You have access to a Prometheus-compatible metrics server. Use this skill to query metrics, check alerts, inspect targets, and explore available metrics. You can query **Prometheus, Thanos, Mimir, and VictoriaMetrics** — they all share the same HTTP API.

## Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `query <promql>` | Instant query (current value) | `prom-query query 'up'` |
| `range <promql> [--start=] [--end=] [--step=]` | Range query (timeseries over time) | `prom-query range 'rate(http_requests_total[5m])' --start=-1h --step=1m` |
| `alerts [--state=firing\|pending\|inactive]` | List active alerts | `prom-query alerts --state=firing` |
| `targets [--state=active\|dropped\|any]` | Scrape target health | `prom-query targets` |
| `explore [pattern]` | Search available metrics by name pattern | `prom-query explore 'http_request'` |
| `rules [--type=alert\|record]` | Alerting & recording rules | `prom-query rules --type=alert` |

## How to Translate Natural Language to PromQL

When the user asks a question about their system, translate it to PromQL using these patterns:

### Error Rate
```
# "What's the error rate for the API?"
rate(http_requests_total{code=~"5.."}[5m]) / rate(http_requests_total[5m])

# "Error rate for the payments service"
rate(http_requests_total{service="payments", code=~"5.."}[5m])

# "4xx and 5xx errors per second"
sum(rate(http_requests_total{code=~"[45].."}[5m])) by (code)
```

### Latency (Histograms)
```
# "P99 latency"
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# "P50 latency by service"
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))

# "Average request duration"
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])
```

### CPU Usage
```
# "CPU usage per instance"
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# "CPU usage per pod (Kubernetes)"
sum(rate(container_cpu_usage_seconds_total{container!=""}[5m])) by (pod, namespace)

# "Which pods use the most CPU?"
topk(10, sum(rate(container_cpu_usage_seconds_total{container!=""}[5m])) by (pod, namespace))
```

### Memory
```
# "Memory usage percentage per instance"
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# "Memory usage per pod (Kubernetes)"
sum(container_memory_working_set_bytes{container!=""}) by (pod, namespace)

# "Pods using more than 1GB RAM"
sum(container_memory_working_set_bytes{container!=""}) by (pod, namespace) > 1e9
```

### Disk
```
# "Disk usage percentage"
(1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})) * 100

# "Disk will be full in 4 hours?" (linear prediction)
predict_linear(node_filesystem_avail_bytes{mountpoint="/"}[1h], 4*3600) < 0
```

### Network
```
# "Network traffic in/out per interface"
rate(node_network_receive_bytes_total[5m])
rate(node_network_transmit_bytes_total[5m])
```

### Kubernetes-Specific
```
# "How many pods are not ready?"
sum(kube_pod_status_ready{condition="false"}) by (namespace)

# "Pods in CrashLoopBackOff"
kube_pod_container_status_waiting_reason{reason="CrashLoopBackOff"}

# "Deployment replica mismatch"
kube_deployment_spec_replicas != kube_deployment_status_available_replicas

# "Node conditions"
kube_node_status_condition{condition="Ready", status="true"} == 0
```

### General Patterns
```
# "Show me everything about <service>"
# First, explore what metrics exist:
prom-query explore '<service_name>'

# "Is everything up?"
prom-query query 'up'

# "What changed in the last hour?"
# Use range query with the relevant metric and look for step changes:
prom-query range '<metric>' --start=-1h --step=1m

# Rate of any counter:
rate(<counter_metric>[5m])

# Sum across labels:
sum(<metric>) by (<label>)

# Top N:
topk(10, <metric>)
```

## How to Interpret Timeseries Data

When you get range query results, look for:

1. **Trends:** Is the value going up, down, or flat over time? Compare first vs last values.
2. **Spikes:** Look at min/max vs average. A large gap suggests spikes or dips.
3. **Step changes:** Did the value suddenly jump to a new baseline? (deployment, config change)
4. **Periodicity:** Does the pattern repeat? (daily traffic patterns, cron jobs)
5. **Correlation:** If querying multiple metrics, do changes happen at the same timestamps?

### Reading the Summary Fields

Range query results include automatic summaries for each series:
- `min` / `max` / `avg`: Statistical summary of all values
- `first` / `last`: Start and end values (shows trend direction)
- `pointCount`: Number of data points
- `downsampled`: Whether the step was automatically increased to limit data volume

### Smart Context Management

The script automatically downsamples range queries that would return more than 500 data points. When `downsampled: true`, tell the user the step was adjusted and offer to zoom into a narrower time window for full resolution.

## Incident Triage Workflow

When helping with an incident or investigating a problem:

1. **Start with alerts:** `prom-query alerts --state=firing` — see what's actually firing
2. **Check targets:** `prom-query targets` — are any scrape targets down?
3. **Query the specific metric** mentioned in the alert
4. **Range query** to see the trend leading up to the alert
5. **Explore related metrics** to find correlation
6. **Check rules** to understand alert thresholds

## Alert Interpretation

When presenting alerts to the user:
- Group by severity (critical → warning → info)
- Highlight how long each alert has been firing (from `activeAt`)
- Include the summary/description annotation
- If the alert has a `value`, explain what it means in context
- Suggest next steps: which metric to query for more detail

## Discord v2 Delivery Mode (OpenClaw v2026.2.14+)

When running in a Discord channel:

- Send a compact first summary (firing alerts, top impacted service, suggested next query).
- Keep the first message under ~1200 characters and avoid wide tables initially.
- If Discord components are available, include quick actions:
  - `Show Last 1h Trend`
  - `List Firing Alerts`
  - `Explore Related Metrics`
- If components are unavailable, provide the same options as a numbered list.
- For long timeseries explanations, send short chunks (<=15 lines per message).

## Important Notes

- All operations are **read-only**. This skill never modifies Prometheus data, rules, or configuration.
- Large result sets are automatically limited and summarized.
- The `explore` command uses regex pattern matching (case-insensitive).
- Time arguments accept: relative (`-1h`, `-30m`, `-2d`), epoch timestamps, or ISO8601 dates.
- If PROMETHEUS_TOKEN is set, it's sent as a Bearer token. Never include tokens in your responses.

## Error Handling

If a query fails:
- **"Cannot reach Prometheus"** → Check PROMETHEUS_URL and network connectivity
- **PromQL parse error** → The query syntax is wrong. Fix and retry.
- **"no data"** → The metric may not exist, or the label selector is too specific. Try `explore` to find the right metric name.
- **Timeout** → The query is too expensive. Add filters, reduce the time range, or use `topk()`.

Powered by Anvil AI 📊
