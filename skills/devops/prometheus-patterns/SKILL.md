---
name: prometheus-patterns
description: PromQL queries, alerting rules, recording rules, Grafana dashboard JSON, SLO
---

# Prometheus Patterns

## PromQL Essentials

### Rate and Error Calculations

```promql
# Request rate (per second, 5m window)
rate(http_requests_total[5m])

# Error rate percentage
sum(rate(http_requests_total{status=~"5.."}[5m]))
/ sum(rate(http_requests_total[5m])) * 100

# P99 latency from histogram
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# P50 latency by endpoint
histogram_quantile(0.50,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, handler)
)

# Saturation: CPU usage per pod
sum(rate(container_cpu_usage_seconds_total[5m])) by (pod)
/ sum(kube_pod_container_resource_limits{resource="cpu"}) by (pod) * 100
```

### SLO: Error Budget

```promql
# SLO: 99.9% availability over 30 days
# Error budget = 0.1% = 43.2 minutes/month

# Current burn rate (how fast consuming budget)
1 - (
  sum(rate(http_requests_total{status!~"5.."}[1h]))
  / sum(rate(http_requests_total[1h]))
) / (1 - 0.999)

# Remaining error budget (percentage)
1 - (
  sum(increase(http_requests_total{status=~"5.."}[30d]))
  / (sum(increase(http_requests_total[30d])) * 0.001)
)
```

## Recording Rules

```yaml
groups:
  - name: sli_rules
    interval: 30s
    rules:
      - record: job:http_request_rate:5m
        expr: sum(rate(http_requests_total[5m])) by (job)

      - record: job:http_error_rate:5m
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (job)
          / sum(rate(http_requests_total[5m])) by (job)

      - record: job:http_latency_p99:5m
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, job)
          )
```

## Alerting Rules

```yaml
groups:
  - name: slo_alerts
    rules:
      - alert: HighErrorRate
        expr: job:http_error_rate:5m > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Error rate above 1% for {{ $labels.job }}"
          runbook: "https://wiki.internal/runbooks/high-error-rate"

      - alert: HighLatency
        expr: job:http_latency_p99:5m > 0.5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "P99 latency above 500ms for {{ $labels.job }}"

      - alert: ErrorBudgetBurn
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[1h]))
            / sum(rate(http_requests_total[1h]))
          ) > 14.4 * 0.001
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Burning error budget 14.4x faster than allowed"
```

## Instrumentation (Go)

```go
import "github.com/prometheus/client_golang/prometheus"

var (
    httpRequests = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total HTTP requests",
        },
        []string{"method", "handler", "status"},
    )
    httpDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration",
            Buckets: []float64{0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5},
        },
        []string{"method", "handler"},
    )
)
```

## Checklist

- [ ] RED metrics (Rate, Errors, Duration) for every service
- [ ] Recording rules for expensive queries
- [ ] Alerts have runbook links
- [ ] Error budget alerts with multi-window burn rate
- [ ] Histogram buckets match expected latency distribution
- [ ] Labels have low cardinality (no user IDs, request IDs)
- [ ] Grafana dashboards use recording rules, not raw queries
- [ ] Alert severity matches response SLA

## Anti-Patterns

- High cardinality labels (user_id, trace_id) causing metric explosion
- Using `avg()` for latency instead of histograms/quantiles
- Missing `for` clause in alerts causing alert storms
- Recording rules with too short intervals wasting resources
- Alerting on symptoms without linking to causes
- Not setting meaningful histogram bucket boundaries
