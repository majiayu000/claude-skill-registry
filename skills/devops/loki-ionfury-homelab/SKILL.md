---
name: loki
description: |
  Query Loki API for cluster logs and debugging. Use when investigating application errors,
  searching logs, debugging pod issues, or querying log patterns.

  Use when: (1) Searching logs for errors or patterns, (2) Investigating pod or service issues via logs,
  (3) Querying Kubernetes events, (4) Debugging Flux reconciliation or platform service failures,
  (5) Running LogQL queries, (6) Checking log rates or volumes.

  Triggers: "check logs", "search logs", "query loki", "logql", "show me logs",
  "what happened in", "log errors", "find in logs", "tail logs", "kubernetes events",
  "recent logs", "log query", "debug logs"
user-invocable: false
---

# Loki Log Querying

## Setup

Loki does **not** have an HTTPRoute on the internal ingress gateway, so it requires port-forward access (unlike Prometheus and Grafana which are available via DNS).

```bash
KUBECONFIG=~/.kube/<cluster>.yaml kubectl port-forward -n monitoring svc/loki-headless 3100:3100 &
export LOKI_URL=http://localhost:3100
```

**Clusters**: `dev`, `integration`, `live`

**Why port-forward?** Loki's gateway component is disabled (`replicas: 0`) and no HTTPRoute exists for it on the internal ingress gateway. For other services that do have HTTPRoutes (Prometheus, Grafana, Alertmanager), prefer using the internal DNS URLs instead -- see the `k8s` skill for the full URL table.

## Quick Queries

Use the bundled script at `.claude/skills/loki/scripts/logql.sh`:

```bash
# Set URL (Loki requires port-forward -- no internal gateway route)
export LOKI_URL=http://localhost:3100

# Health check
./scripts/logql.sh health

# Search logs by namespace
./scripts/logql.sh tail '{namespace="monitoring"}' --since 15m

# Instant query (metric-style aggregation)
./scripts/logql.sh query 'rate({namespace="monitoring"}[5m])'

# Range query with time window
./scripts/logql.sh range '{namespace="flux-system"}' --start 1h --step 1m --limit 50

# Discover available labels
./scripts/logql.sh labels
./scripts/logql.sh labels namespace

# Find series matching a selector
./scripts/logql.sh series '{namespace="monitoring"}'
```

## Common Operations

### Search for Errors

```bash
# Errors in a namespace
./scripts/logql.sh tail '{namespace="database"} |= "error"' --since 30m

# Case-insensitive error search
./scripts/logql.sh tail '{namespace="monitoring"} |~ "(?i)error|fail|panic"' --since 15m

# Specific container logs
./scripts/logql.sh tail '{namespace="monitoring", container="prometheus"}' --since 10m --limit 50
```

### Kubernetes Events

```bash
# Warning events (via Alloy kubernetes_events)
./scripts/logql.sh tail '{job="integrations/kubernetes/eventhandler"} |= "Warning"' --since 1h

# Events for a specific namespace
./scripts/logql.sh tail '{job="integrations/kubernetes/eventhandler", namespace="database"}' --since 30m
```

### Log Rate Metrics

```bash
# Error rate per namespace
./scripts/logql.sh query 'sum by(namespace) (rate({namespace=~".+"} |= "error" [5m]))'

# Log volume by namespace
./scripts/logql.sh query 'sum by(namespace) (bytes_rate({namespace=~".+"}[5m]))'

# Top 5 noisiest pods
./scripts/logql.sh query 'topk(5, sum by(pod) (rate({namespace=~".+"}[5m])))'
```

### Direct curl (alternative)

```bash
# Instant query
curl -s "http://localhost:3100/loki/api/v1/query?query=%7Bnamespace%3D%22monitoring%22%7D&limit=10" | jq '.data.result'

# Labels
curl -s "http://localhost:3100/loki/api/v1/labels" | jq '.data'
```

## Reference

For homelab-specific LogQL queries (Flux, Cilium, CloudNative-PG, etc.), see [references/queries.md](references/queries.md).

## Loki Details

| Property | Value |
|----------|-------|
| Namespace | `monitoring` |
| Service | `loki-headless:3100` |
| API prefix | `/loki/api/v1/` |
| Log shipping | Alloy (Grafana Agent) |
| Ready endpoint | `/ready` |
