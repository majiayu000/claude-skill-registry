---
description: Full-stack observability architect for Prometheus, Grafana, OpenTelemetry, distributed tracing (Jaeger/Tempo), SLIs/SLOs, error budgets, and alerting. Use for metrics, dashboards, traces, or reliability engineering.
allowed-tools: Read, Write, Edit, Bash
model: opus
context: fork
---

# Observability Engineer - Full-Stack Monitoring Expert

## ⚠️ Chunking Rule

Large monitoring stacks (Prometheus + Grafana + OpenTelemetry + logs) = 1000+ lines. Generate ONE component per response: Metrics → Dashboards → Alerting → Tracing → Logs.

## Purpose

Design and implement comprehensive observability systems covering metrics, logs, traces, and reliability engineering.

## When to Use

- Set up Prometheus monitoring
- Create Grafana dashboards
- Implement distributed tracing (Jaeger, Tempo)
- Define SLIs/SLOs and error budgets
- Configure alerting systems
- Prevent alert fatigue
- Debug microservices latency

## Scope Boundaries

This skill covers **OBSERVABILITY STRATEGY**: SLIs/SLOs, error budgets, dashboards, alerting design.

- For OpenTelemetry instrumentation details → use `/sw-infra:opentelemetry`

## Core Concepts

### Three Pillars of Observability

```
┌─────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY                             │
├─────────────────┬─────────────────┬─────────────────────────┤
│    METRICS      │     LOGS        │        TRACES           │
├─────────────────┼─────────────────┼─────────────────────────┤
│ Prometheus      │ Loki/ELK        │ Jaeger/Tempo            │
│ What happened?  │ Why happened?   │ How requests flow?      │
│ Aggregated data │ Event details   │ Request journey         │
└─────────────────┴─────────────────┴─────────────────────────┘
```

### RED Method (Services)
- **Rate** - Requests per second
- **Errors** - Error rate percentage
- **Duration** - Latency/response time

### USE Method (Resources)
- **Utilization** - % time resource is busy
- **Saturation** - Queue length/wait time
- **Errors** - Error count

## Prometheus Setup

### Installation (Kubernetes)

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  --set prometheus.prometheusSpec.retention=30d
```

### Key Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

### Recording Rules

```yaml
groups:
  - name: api_metrics
    rules:
      - record: job:http_requests:rate5m
        expr: sum by (job) (rate(http_requests_total[5m]))
      - record: job:http_requests_error_rate:percentage
        expr: (sum by (job) (rate(http_requests_total{status=~"5.."}[5m])) / sum by (job) (rate(http_requests_total[5m]))) * 100
```

## Grafana Dashboards

### Dashboard Design Principles

```
┌─────────────────────────────────────┐
│  Critical Metrics (Big Numbers)     │
├─────────────────────────────────────┤
│  Key Trends (Time Series)           │
├─────────────────────────────────────┤
│  Detailed Metrics (Tables/Heatmaps) │
└─────────────────────────────────────┘
```

### Essential Queries

```promql
# Request rate
sum(rate(http_requests_total[5m])) by (service)

# Error rate %
(sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100

# P95 Latency
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))
```

## Distributed Tracing

### OpenTelemetry Setup (Node.js)

```javascript
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { JaegerExporter } = require('@opentelemetry/exporter-jaeger');
const { registerInstrumentations } = require('@opentelemetry/instrumentation');
const { HttpInstrumentation } = require('@opentelemetry/instrumentation-http');

const provider = new NodeTracerProvider();
provider.addSpanProcessor(new BatchSpanProcessor(new JaegerExporter()));
provider.register();

registerInstrumentations({
  instrumentations: [new HttpInstrumentation()],
});
```

### Context Propagation

```
traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
```

### Jaeger Deployment

```yaml
# Kubernetes
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: jaeger
spec:
  strategy: production
  storage:
    type: elasticsearch
```

## SLIs/SLOs

### Defining SLOs

```yaml
slos:
  - name: api_availability
    target: 99.9%  # 43.2 min downtime/month
    window: 28d
    sli: sum(rate(http_requests_total{status!~"5.."}[28d])) / sum(rate(http_requests_total[28d]))

  - name: api_latency_p95
    target: 99%    # 99% requests < 500ms
    window: 28d
    sli: sum(rate(http_request_duration_seconds_bucket{le="0.5"}[28d])) / sum(rate(http_request_duration_seconds_count[28d]))
```

### Error Budget

```
Error Budget = 1 - SLO Target
Example: 99.9% SLO → 0.1% error budget → 43.2 min/month
```

### Burn Rate Alerts

```yaml
rules:
  - alert: SLOErrorBudgetBurnFast
    expr: slo:http_availability:burn_rate_1h > 14.4 and slo:http_availability:burn_rate_5m > 14.4
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "Fast error budget burn - consuming 2% budget in 1 hour"
```

## Alert Fatigue Prevention

### Multi-Window Alerting

```yaml
# Combine short + long windows to reduce false positives
- alert: HighLatency
  expr: |
    (job:http_request_duration:p95_5m > 1 AND job:http_request_duration:p95_1h > 0.8)
  for: 5m
```

### Severity Levels

| Severity | Response | Examples |
|----------|----------|----------|
| critical | Page immediately | Service down, data loss |
| warning | Review in hours | Degraded performance |
| info | Daily review | Capacity planning |

## Best Practices

1. **Start with RED/USE methods** for consistent metrics
2. **Use recording rules** for expensive queries
3. **Implement multi-window alerts** to reduce noise
4. **Set achievable SLOs** (don't aim for 100%)
5. **Track error budget** consistently
6. **Correlate traces with metrics** using trace IDs
7. **Sample traces appropriately** (1-10% in production)
8. **Add context to spans** (user_id, request_id)

## Related Skills

- `devops` - Infrastructure provisioning
