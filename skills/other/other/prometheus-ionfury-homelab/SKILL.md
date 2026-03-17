---
name: prometheus
description: Query Prometheus API for cluster metrics, alerts, and observability data. Use when investigating cluster health, performance issues, resource utilization, or alert status. Triggers on questions like "what's the CPU usage", "show me firing alerts", "check memory pressure", "query prometheus for", or any PromQL-related requests.
user-invocable: false
---

# Prometheus Querying

## Setup

Prometheus and Alertmanager are behind **OAuth2 Proxy** on the internal gateway. DNS URLs (`https://prometheus.internal.tomnowak.work`) redirect to an OAuth login page and **cannot be used for API queries via curl**.

### Access Methods

**Option 1: kubectl exec (quick, no setup)**

```bash
# Query Prometheus API directly inside the pod
KUBECONFIG=~/.kube/<cluster>.yaml kubectl exec -n monitoring prometheus-kube-prometheus-stack-0 -c prometheus -- \
  wget -qO- 'http://localhost:9090/api/v1/query?query=up' | jq '.data.result'

# Query Alertmanager API
KUBECONFIG=~/.kube/<cluster>.yaml kubectl exec -n monitoring alertmanager-kube-prometheus-stack-0 -c alertmanager -- \
  wget -qO- 'http://localhost:9093/api/v2/alerts' | jq .
```

**Option 2: Port-forward (for scripts and repeated queries)**

```bash
KUBECONFIG=~/.kube/<cluster>.yaml kubectl port-forward -n monitoring svc/prometheus-operated 9090:9090 &
export PROMETHEUS_URL=http://localhost:9090
```

The `promql.sh` script defaults to `http://localhost:9090` and works with port-forward out of the box.

## Quick Queries

Use the bundled script at `.claude/skills/prometheus/scripts/promql.sh`:

```bash
# Start port-forward first (script defaults to http://localhost:9090)
KUBECONFIG=~/.kube/<cluster>.yaml kubectl port-forward -n monitoring svc/prometheus-operated 9090:9090 &

# Instant query
./scripts/promql.sh query 'up'

# Range query (last hour, 15s resolution)
./scripts/promql.sh range 'node_cpu_seconds_total' --start 1h --step 15s

# Firing alerts only
./scripts/promql.sh alerts --firing

# All alert rules
./scripts/promql.sh rules

# Find metrics by label
./scripts/promql.sh series '{job="node-exporter"}'

# Health check
./scripts/promql.sh health
```

## Common Operations

### Check Cluster Health

```bash
# CPU usage %
./scripts/promql.sh query 'avg(1 - rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100'

# Memory usage %
./scripts/promql.sh query '(1 - sum(node_memory_MemAvailable_bytes) / sum(node_memory_MemTotal_bytes)) * 100'

# Problem pods
./scripts/promql.sh query 'kube_pod_status_phase{phase!~"Running|Succeeded"} == 1'

# Container restarts (last hour)
./scripts/promql.sh query 'increase(kube_pod_container_status_restarts_total[1h]) > 0'
```

### Check Alerts

```bash
# All firing alerts
./scripts/promql.sh alerts --firing

# Full alert details
./scripts/promql.sh alerts --verbose
```

### Direct kubectl exec (alternative)

```bash
# Instant query via kubectl exec (no port-forward needed)
KUBECONFIG=~/.kube/<cluster>.yaml kubectl exec -n monitoring prometheus-kube-prometheus-stack-0 -c prometheus -- \
  wget -qO- 'http://localhost:9090/api/v1/query?query=up' | jq '.data.result'

# Alerts
KUBECONFIG=~/.kube/<cluster>.yaml kubectl exec -n monitoring prometheus-kube-prometheus-stack-0 -c prometheus -- \
  wget -qO- 'http://localhost:9090/api/v1/alerts' | jq '.data.alerts'
```

## Reference

For homelab-specific PromQL queries (Longhorn, CloudNative-PG, Cilium, etc.), see [references/queries.md](references/queries.md).

## Creating Monitoring Resources

This skill covers **querying** Prometheus. For **authoring** new monitoring resources
(PrometheusRules, ServiceMonitors, PodMonitors, AlertmanagerConfig, recording rules),
see the [monitoring-authoring skill](../monitoring-authoring/SKILL.md).

## Prometheus Details

| Property | Value |
|----------|-------|
| Namespace | `monitoring` |
| Service | `prometheus-operated:9090` |
| Retention | 14 days / 50GB |
| External label | `prometheus_source: ${cluster_name}` |
