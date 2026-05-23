---
name: observability
description: Query Prometheus metrics, Loki logs, and Grafana dashboards for diagnostics and incident response.
agents: [rex, grizz, nova, blaze, bolt, cipher, cleo, tess]
triggers: [metrics, logs, prometheus, loki, grafana, monitoring, alerts, incident]
---

# Observability Tools

Query metrics, logs, and dashboards for diagnostics and incident response.

## Prometheus (Metrics)

Query metrics for performance analysis and alerting.

```
# CPU usage by pod
prometheus_query({
  query: 'rate(container_cpu_usage_seconds_total{namespace="my-service"}[5m])'
})

# Memory usage
prometheus_query({
  query: 'container_memory_usage_bytes{namespace="my-service"}'
})

# HTTP request rate
prometheus_query({
  query: 'rate(http_requests_total{namespace="my-service"}[5m])'
})

# Error rate
prometheus_query({
  query: 'rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])'
})
```

## Loki (Logs)

Query logs for debugging and incident investigation.

```
# Application logs
loki_query({
  query: '{namespace="my-service", app="api"} |= "error"',
  limit: 100
})

# Structured log parsing
loki_query({
  query: '{namespace="my-service"} | json | level="error"'
})

# Time-based filtering
loki_query({
  query: '{namespace="my-service"}',
  start: "2024-01-01T00:00:00Z",
  end: "2024-01-01T01:00:00Z"
})
```

## Common Queries

| Scenario | Query Type | Example |
|----------|------------|---------|
| High latency | Prometheus | `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))` |
| Errors spike | Loki | `{app="api"} \|= "error" \| json \| count by (error_type)` |
| Memory leak | Prometheus | `container_memory_usage_bytes{pod=~"api.*"}` |
| Failed requests | Loki | `{app="api"} \| json \| status >= 500` |

## Incident Response Flow

1. **Check alerts** - What triggered?
2. **Query metrics** - Is it resource exhaustion?
3. **Query logs** - What errors are occurring?
4. **Correlate** - Match timestamps across metrics and logs
5. **Identify root cause** - Database? Network? Code bug?

## Best Practices

1. **Start broad, then narrow** - Filter down to specific pods
2. **Use time ranges** - Don't query unbounded
3. **Correlate metrics + logs** - Same time window
4. **Check dashboard first** - Grafana may have pre-built views
