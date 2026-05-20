---
name: "Observability & Monitoring"
description: "Production visibility through logs, metrics, traces, and alerting — the three pillars of observability"
applyTo: "**/*observ*,**/*monitor*,**/*telemetry*,**/*logging*,**/*metrics*,**/*traces*"
---

# Observability & Monitoring Skill

> See what's happening in production. Debug without reproducing. Understand system behavior at scale.

## The Three Pillars

| Pillar | What | When | Tools |
|--------|------|------|-------|
| **Logs** | Discrete events | Debugging, auditing | Winston, Pino, Serilog |
| **Metrics** | Aggregated measurements | Alerting, dashboards | Prometheus, CloudWatch |
| **Traces** | Request flow across services | Distributed debugging | Jaeger, Zipkin |

**Modern approach:** OpenTelemetry unifies all three.

---

## Logging Best Practices

### Structured Logging

```typescript
// ❌ Bad: Unstructured
console.log(`User ${userId} clicked button ${buttonId}`);

// ✅ Good: Structured
logger.info('Button clicked', {
  userId,
  buttonId,
  timestamp: Date.now(),
  sessionId: ctx.sessionId
});
```

### Log Levels

| Level | Usage | Example |
|-------|-------|---------|
| **ERROR** | Something failed, needs attention | Payment failed |
| **WARN** | Unexpected but handled | Retry succeeded |
| **INFO** | Business events | User logged in |
| **DEBUG** | Developer details | Cache hit/miss |
| **TRACE** | Verbose internals | Function entry/exit |

### Correlation IDs

Track requests across services:

```typescript
// Middleware to propagate trace ID
app.use((req, res, next) => {
  req.traceId = req.headers['x-trace-id'] || uuid();
  res.setHeader('x-trace-id', req.traceId);
  next();
});

// Include in all logs
logger.info('Processing request', { traceId: req.traceId, ...data });
```

---

## Metrics Patterns

### The RED Method (Request-focused)

For services:
- **R**ate: Requests per second
- **E**rrors: Failed requests per second
- **D**uration: Request latency distribution

### The USE Method (Resource-focused)

For infrastructure:
- **U**tilization: % time resource busy
- **S**aturation: Queue depth
- **E**rrors: Error count

### Key Metric Types

| Type | Use Case | Example |
|------|----------|---------|
| **Counter** | Cumulative totals | requests_total |
| **Gauge** | Current value | temperature, queue_size |
| **Histogram** | Value distribution | request_duration_seconds |
| **Summary** | Quantiles | response_time_p99 |

### Golden Signals (SRE)

1. **Latency** — Time to serve request
2. **Traffic** — Demand on system
3. **Errors** — Failed requests rate
4. **Saturation** — How full is the system

---

## Distributed Tracing

### Span Structure

```
Trace: user-checkout-abc123
├── Span: api-gateway (50ms)
│   ├── Span: auth-service (10ms)
│   └── Span: order-service (35ms)
│       ├── Span: inventory-check (8ms)
│       └── Span: payment-service (20ms)
│           └── Span: database-write (5ms)
```

### Context Propagation

```typescript
// OpenTelemetry automatic propagation
import { trace, context, propagation } from '@opentelemetry/api';

// Extract context from incoming request
const ctx = propagation.extract(context.active(), req.headers);

// Create span with parent context
const span = tracer.startSpan('process-order', undefined, ctx);

// Propagate to outgoing request
propagation.inject(context.active(), headers);
```

---

## OpenTelemetry Setup

### Node.js Quick Start

```typescript
// tracing.ts - Load FIRST
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: 'http://localhost:4318/v1/traces',
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

### .NET Quick Start

```csharp
// Program.cs
builder.Services.AddOpenTelemetry()
    .WithTracing(tracing => tracing
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddOtlpExporter());
```

---

## Alerting Strategy

### Alert Hierarchy

| Severity | Response | Example |
|----------|----------|---------|
| **P1/Critical** | Wake someone up | Service down |
| **P2/High** | Fix within hours | Error rate > 5% |
| **P3/Medium** | Fix within days | Disk 80% |
| **P4/Low** | Fix when convenient | Deprecation warning |

### Alert Anti-Patterns

❌ **Alert fatigue** — Too many non-actionable alerts
❌ **Missing runbook** — Alert with no remediation steps
❌ **Threshold-only** — Alert on static value, not trend
❌ **No owner** — Alert goes to void

### Good Alert Template

```yaml
alert: HighErrorRate
expr: sum(rate(http_errors_total[5m])) / sum(rate(http_requests_total[5m])) > 0.05
for: 5m
labels:
  severity: high
  team: backend
annotations:
  summary: "Error rate above 5%"
  runbook: "https://runbooks.example.com/high-error-rate"
  dashboard: "https://grafana.example.com/d/errors"
```

---

## Dashboard Design

### Layout Principles

```
┌─────────────────────────────────────────────────────────┐
│                   SERVICE HEALTH                         │
│  [Status] [Error Rate] [Latency P50] [Latency P99]      │
├─────────────────────────────────────────────────────────┤
│                   TRAFFIC                                │
│  [Requests/sec graph over time]                         │
├─────────────────────────────────────────────────────────┤
│           ERRORS             │        LATENCY           │
│  [Error breakdown by type]   │  [Latency histogram]     │
├─────────────────────────────────────────────────────────┤
│                   RESOURCES                              │
│  [CPU] [Memory] [Disk] [Network]                        │
└─────────────────────────────────────────────────────────┘
```

### Dashboard Hierarchy

1. **Overview** — Executive view, all services
2. **Service** — Single service deep dive
3. **Debug** — Detailed metrics for investigation

---

## Cloud Provider Tools

| Cloud | Metrics | Logs | Traces |
|-------|---------|------|--------|
| **Azure** | Azure Monitor | Log Analytics | App Insights |
| **AWS** | CloudWatch | CloudWatch Logs | X-Ray |
| **GCP** | Cloud Monitoring | Cloud Logging | Cloud Trace |

### Azure Application Insights

```typescript
// Node.js
import { useAzureMonitor } from '@azure/monitor-opentelemetry';

useAzureMonitor({
  azureMonitorExporterOptions: {
    connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING
  }
});
```

---

## VS Code Extension Observability

For VS Code extensions like Alex:

### What to Monitor

| Metric | Why |
|--------|-----|
| Command execution time | User experience |
| Activation time | Startup performance |
| Error rates by command | Reliability |
| Memory usage | Resource efficiency |
| API call latency | External dependencies |

### Telemetry Implementation

```typescript
import * as vscode from 'vscode';

const telemetry = vscode.env.createTelemetryLogger({
  sendEventData(eventName, data) {
    // Send to your telemetry backend
  },
  sendErrorData(error, data) {
    // Send errors with context
  }
});

// Usage
telemetry.logUsage('command.executed', {
  commandId: 'alex.meditate',
  durationMs: 1500
});
```

---

## Debugging Patterns

### Log-Driven Debugging

1. Find error in logs
2. Get correlation ID
3. Search all logs with that ID
4. Reconstruct timeline

### Trace-Driven Debugging

1. Find slow/failed trace
2. Examine span waterfall
3. Identify bottleneck span
4. Drill into that service

### Metric-Driven Debugging

1. Notice anomaly in dashboard
2. Correlate with other metrics
3. Narrow time window
4. Switch to logs/traces for details

---

## Implementation Checklist

### New Service

- [ ] Structured logging configured
- [ ] Correlation ID propagation
- [ ] Basic metrics (RED/USE)
- [ ] Health check endpoint
- [ ] OpenTelemetry instrumentation
- [ ] Dashboard created
- [ ] Alerts defined with runbooks

### Production Readiness

- [ ] Error rates < 0.1% baseline
- [ ] P99 latency acceptable
- [ ] Logs searchable and retained
- [ ] Traces sampling configured
- [ ] On-call runbooks written

---

## Related Skills

- **performance-profiling** — Deep dive into specific bottlenecks
- **incident-response** — Using observability during outages
- **infrastructure-as-code** — Deploying monitoring stack
- **security-review** — Audit logging requirements

---

*"If you can't measure it, you can't improve it." — Peter Drucker*

*Good observability means finding the problem before your users do.*
