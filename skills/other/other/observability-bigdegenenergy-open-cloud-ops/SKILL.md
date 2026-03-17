---
name: observability
description: Observability patterns including logging, metrics, tracing, and alerting. Auto-triggers when implementing monitoring, debugging production issues, or setting up alerts.
---

# Observability Skill

## Three Pillars of Observability

### 1. Logs
- **What happened**: Discrete events with context
- **Use for**: Debugging, audit trails, error investigation
- **Challenge**: Volume and searchability

### 2. Metrics
- **How much/how often**: Numeric measurements over time
- **Use for**: Dashboards, alerting, capacity planning
- **Challenge**: Cardinality explosion

### 3. Traces
- **Where time was spent**: Request flow across services
- **Use for**: Latency analysis, dependency mapping
- **Challenge**: Sampling and storage

## Structured Logging

### Log Format
```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "error",
  "message": "Payment failed",
  "service": "payment-service",
  "trace_id": "abc123",
  "span_id": "def456",
  "user_id": "user_789",
  "error": {
    "type": "PaymentDeclined",
    "code": "INSUFFICIENT_FUNDS"
  },
  "duration_ms": 234
}
```

### Log Levels
| Level | Use Case |
|-------|----------|
| ERROR | Failures requiring attention |
| WARN | Unexpected but recoverable |
| INFO | Business events, state changes |
| DEBUG | Development troubleshooting |
| TRACE | Fine-grained diagnostic |

### Best Practices
- Use structured JSON format
- Include correlation IDs (trace_id)
- Never log sensitive data (PII, secrets)
- Use consistent field names
- Set appropriate log levels

## Metrics Design

### Types of Metrics
| Type | Example | Use Case |
|------|---------|----------|
| Counter | requests_total | Monotonically increasing |
| Gauge | temperature_celsius | Value that goes up/down |
| Histogram | request_duration_seconds | Distribution of values |
| Summary | request_latency_quantiles | Quantile calculations |

### Naming Convention
```
<namespace>_<name>_<unit>

Examples:
- http_requests_total
- http_request_duration_seconds
- db_connections_active
- queue_messages_waiting
```

### RED Method (Services)
- **R**ate: Requests per second
- **E**rror: Error rate
- **D**uration: Latency distribution

### USE Method (Resources)
- **U**tilization: % time busy
- **S**aturation: Queue depth
- **E**rrors: Error count

### Golden Signals
1. Latency (response time)
2. Traffic (requests/sec)
3. Errors (error rate)
4. Saturation (resource utilization)

## Distributed Tracing

### Trace Structure
```
Trace (trace_id: abc123)
├── Span: HTTP Request (span_id: 001, parent: null)
│   ├── Span: Auth Check (span_id: 002, parent: 001)
│   ├── Span: DB Query (span_id: 003, parent: 001)
│   │   └── Span: Connection Pool (span_id: 004, parent: 003)
│   └── Span: External API (span_id: 005, parent: 001)
```

### Context Propagation
```
# HTTP Headers
traceparent: 00-abc123-def456-01
tracestate: vendor=value
```

### Sampling Strategies
| Strategy | Use Case |
|----------|----------|
| Always sample | Development, low traffic |
| Probabilistic | Production (1-10%) |
| Rate limiting | Control volume |
| Tail-based | Capture errors/slow requests |

## Alerting

### Alert Design
```yaml
# Good alert
name: High Error Rate
expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.01
for: 5m
severity: critical
annotations:
  summary: "Error rate above 1% for 5 minutes"
  runbook: "https://wiki/runbooks/high-error-rate"
```

### Alert Quality
- **Actionable**: Clear remediation steps
- **Relevant**: Indicates real problems
- **Timely**: Fast enough to matter
- **Not noisy**: Avoid alert fatigue

### SLOs and Error Budgets
```
SLI: 99.9% of requests complete in < 200ms
SLO: 99.9% availability per month
Error Budget: 0.1% = 43.2 minutes downtime/month
```

## Dashboards

### Layout Principles
1. **Overview first**: Key metrics at top
2. **Then details**: Drill-down sections
3. **Time alignment**: Consistent time ranges
4. **Annotations**: Mark deployments/incidents

### Essential Panels
- Request rate (traffic)
- Error rate (errors)
- Latency percentiles (P50, P95, P99)
- Resource utilization (CPU, memory)
- Queue depths (saturation)
