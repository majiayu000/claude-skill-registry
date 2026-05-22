---
name: monitoring-setup
description: Observability stack with Prometheus, Grafana, and alerting.
---

# Monitoring Setup

## The Three Pillars

| Pillar | Tool | Purpose |
|--------|------|---------|
| **Metrics** | Prometheus | Time-series data |
| **Logs** | Loki / ELK | Event records |
| **Traces** | Jaeger / Tempo | Request flow |

## Prometheus

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

## Grafana Dashboard

```json
{
  "panels": [
    {
      "title": "Request Rate",
      "targets": [
        {
          "expr": "rate(http_requests_total[5m])",
          "legendFormat": "{{method}} {{path}}"
        }
      ]
    }
  ]
}
```

## Alert Rules

```yaml
groups:
  - name: app
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"

      - alert: PodCrashLooping
        expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
        for: 5m
        labels:
          severity: warning
```

## Key Metrics

### RED Method (Services)

- **Rate** - Requests per second
- **Errors** - Failed requests
- **Duration** - Response time

### USE Method (Resources)

- **Utilization** - % busy
- **Saturation** - Queue depth
- **Errors** - Error count

## SLIs/SLOs

```
SLI: 99th percentile latency < 200ms
SLO: 99.9% of requests meet SLI
Error Budget: 0.1% of requests can exceed SLI
```
