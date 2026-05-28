---
name: observability
description: Implement observability solutions. Use when setting up monitoring, logging, or tracing. Covers OpenTelemetry, metrics, and alerting.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Observability

## Three Pillars

### 1. Logs
Discrete events with context.

```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "level": "error",
  "message": "Failed to process order",
  "orderId": "123",
  "error": "Payment declined",
  "traceId": "abc123"
}
```

### 2. Metrics
Numeric measurements over time.

```
http_requests_total{method="GET", status="200"} 1234
http_request_duration_seconds{quantile="0.95"} 0.23
```

### 3. Traces
Request flow through services.

```
Trace: abc123
├── API Gateway (50ms)
│   ├── Auth Service (10ms)
│   └── Order Service (35ms)
│       └── Database (20ms)
```

## OpenTelemetry Setup

```typescript
import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: 'http://collector:4318/v1/traces',
  }),
  serviceName: 'my-service',
});

sdk.start();
```

## Key Metrics

### RED Method (Request-focused)
- **R**ate: Requests per second
- **E**rrors: Failed requests per second
- **D**uration: Request latency

### USE Method (Resource-focused)
- **U**tilization: % time busy
- **S**aturation: Queue depth
- **E**rrors: Error count

## Alerting

### Good Alerts
- Actionable: Something can be done
- Urgent: Needs immediate attention
- Specific: Clear what's wrong

### Alert Template
```yaml
alert: HighErrorRate
expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.01
for: 5m
labels:
  severity: critical
annotations:
  summary: "High error rate on {{ $labels.service }}"
  description: "Error rate is {{ $value | humanizePercentage }}"
```

## Dashboards

Essential panels:
1. Request rate
2. Error rate
3. Latency (P50, P95, P99)
4. Saturation (CPU, memory)
5. Active alerts
