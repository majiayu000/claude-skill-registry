---
name: sre-monitoring-and-observability
description: Use when building comprehensive monitoring and observability systems.
allowed-tools: []
---

# SRE Monitoring and Observability

Building comprehensive monitoring and observability systems.

## Four Golden Signals

### Latency

Time to process requests:

```prometheus
# Request duration
http_request_duration_seconds

# Query
histogram_quantile(0.95, 
  rate(http_request_duration_seconds_bucket[5m])
)
```

### Traffic

Demand on the system:

```prometheus
# Requests per second
rate(http_requests_total[5m])

# By endpoint
sum(rate(http_requests_total[5m])) by (endpoint)
```

### Errors

Rate of failed requests:

```prometheus
# Error rate
rate(http_requests_total{status=~"5.."}[5m])
/ 
rate(http_requests_total[5m])

# SLI compliance
1 - (error_rate / slo_target)
```

### Saturation

Resource utilization:

```prometheus
# CPU usage
100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) 
/ node_memory_MemTotal_bytes * 100
```

## Service Level Indicators (SLIs)

### Availability SLI

```prometheus
# Successful requests / Total requests
sum(rate(http_requests_total{status=~"[23].."}[30d]))
/
sum(rate(http_requests_total[30d]))
```

### Latency SLI

```prometheus
# Requests faster than threshold / Total requests
sum(rate(http_request_duration_seconds_bucket{le="0.5"}[30d]))
/
sum(rate(http_request_duration_seconds_count[30d]))
```

### Throughput SLI

```prometheus
# Requests processed within capacity
clamp_max(
  rate(http_requests_total[5m]) / capacity_requests_per_second,
  1.0
)
```

## Alerting

### Alert Severity Levels

**P0 - Critical**: Service down or severe degradation
**P1 - High**: Significant impact, error budget at risk  
**P2 - Medium**: Degradation, not user-facing yet
**P3 - Low**: Awareness, no immediate action needed

### Example Alerts

```yaml
# High error rate
groups:
  - name: sre
    rules:
      - alert: HighErrorRate
        expr: |
          rate(http_requests_total{status=~"5.."}[5m])
          / rate(http_requests_total[5m])
          > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate on {{ $labels.service }}"
          
      - alert: LatencyP95High
        expr: |
          histogram_quantile(0.95,
            rate(http_request_duration_seconds_bucket[5m])
          ) > 1.0
        for: 10m
        labels:
          severity: warning
          
      - alert: ErrorBudgetBurn
        expr: |
          (1 - sli_availability) > (error_budget_remaining * 10)
        for: 1h
        labels:
          severity: high
```

## Dashboards

### Overview Dashboard

- Service health (red/yellow/green)
- Request rate
- Error rate
- Latency percentiles (p50, p95, p99)
- Saturation metrics

### Detailed Dashboard

- Per-endpoint metrics
- Dependency health
- Database performance
- Cache hit rates
- Queue depths

## Distributed Tracing

### OpenTelemetry

```javascript
const { trace } = require('@opentelemetry/api');
const tracer = trace.getTracer('my-service');

async function handleRequest(req) {
  const span = tracer.startSpan('handle_request');
  
  try {
    span.setAttribute('user.id', req.user.id);
    span.setAttribute('request.path', req.path);
    
    const result = await processRequest(req);
    
    span.setStatus({ code: SpanStatusCode.OK });
    return result;
  } catch (error) {
    span.setStatus({
      code: SpanStatusCode.ERROR,
      message: error.message,
    });
    throw error;
  } finally {
    span.end();
  }
}
```

## Structured Logging

```javascript
logger.info('request_processed', {
  request_id: req.id,
  user_id: req.user.id,
  endpoint: req.path,
  method: req.method,
  status_code: res.statusCode,
  duration_ms: duration,
  error: error?.message,
});
```

## Best Practices

### USE Method

For resources:

- **Utilization**: % time resource is busy
- **Saturation**: Work queued but not serviced
- **Errors**: Error count

### RED Method

For requests:

- **Rate**: Requests per second
- **Errors**: Failed requests per second
- **Duration**: Request latency distribution

### Alert on Symptoms, Not Causes

```yaml
# Good - alert on user impact
- alert: HighLatency
  expr: p95_latency > 1s

# Bad - alert on potential cause
- alert: HighCPU
  expr: cpu_usage > 80%
```

### Runbook Links

```yaml
annotations:
  runbook: "https://wiki.example.com/runbooks/high-error-rate"
  dashboard: "https://grafana.example.com/d/abc123"
```
