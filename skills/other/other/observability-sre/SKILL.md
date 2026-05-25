---
name: observability-sre
description: Observability and SRE expert. Use when setting up monitoring, logging, tracing, defining SLOs, or managing incidents. Covers Prometheus, Grafana, OpenTelemetry, and incident response best practices.
---
# Observability & Site Reliability Engineering

## Core Principles

- **Three Pillars** — Metrics, Logs, and Traces provide holistic visibility
- **Observability-First** — Build systems that explain their own behavior
- **SLO-Driven** — Define reliability targets that matter to users
- **Proactive Detection** — Find issues before customers do
- **Blameless Culture** — Learn from failures without blame
- **Automate Toil** — Reduce repetitive operational work
- **Continuous Improvement** — Each incident makes systems more resilient
- **Full-Stack Visibility** — Monitor from infrastructure to business metrics

---

## Hard Rules (Must Follow)

> These rules are mandatory. Violating them means the skill is not working correctly.

### Symptom-Based Alerts Only

**Alert on user-facing symptoms, not internal infrastructure metrics.**

```yaml
# ❌ FORBIDDEN: Alerting on internal metrics
- alert: CPUHigh
  expr: cpu_usage > 70%
  # Users don't care about CPU, they care about latency

- alert: MemoryHigh
  expr: memory_usage > 80%
  # Internal metric, may not affect users

# ✅ REQUIRED: Alert on user experience
- alert: APILatencyHigh
  expr: slo:api_latency:p95 > 0.200
  annotations:
    summary: "Users experiencing slow response times"

- alert: ErrorRateHigh
  expr: slo:api_errors:rate5m > 0.001
  annotations:
    summary: "Users encountering errors"
```

### Low Cardinality Labels

**Loki/Prometheus labels must have low cardinality (<10 unique labels).**

```yaml
# ❌ FORBIDDEN: High cardinality labels
labels:
  user_id: "usr_123"      # Millions of values!
  order_id: "ord_456"     # Millions of values!
  request_id: "req_789"   # Every request is unique!

# ✅ REQUIRED: Low cardinality only
labels:
  namespace: "production"  # Few values
  app: "api-server"        # Few values
  level: "error"           # 5-6 values
  method: "GET"            # ~10 values

# High cardinality data goes in log body:
logger.info({
  user_id: "usr_123",      # In JSON body, not label
  order_id: "ord_456",
}, "Order processed");
```

### SLO-Based Error Budgets

**Every service must have defined SLOs with error budget tracking.**

```yaml
# ❌ FORBIDDEN: No SLO definition
# Just monitoring without targets

# ✅ REQUIRED: Explicit SLO with budget
# SLO: 99.9% availability
# Error Budget: 0.1% = 43.2 minutes/month downtime

groups:
  - name: slo_tracking
    rules:
      - record: slo:api_availability:ratio
        expr: sum(rate(http_requests_total{status!~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

      - alert: ErrorBudgetBurnRate
        expr: slo:api_availability:ratio < 0.999
        for: 5m
        annotations:
          summary: "Burning error budget too fast"
```

### Trace Context in Logs

**All logs must include trace_id for correlation with distributed traces.**

```typescript
// ❌ FORBIDDEN: Logs without trace context
logger.info("Payment processed");

// ✅ REQUIRED: Include trace_id in every log
const span = trace.getActiveSpan();
logger.info({
  trace_id: span?.spanContext().traceId,
  span_id: span?.spanContext().spanId,
  order_id: "ord_123",
}, "Payment processed");

// Output includes correlation:
// {"trace_id":"abc123","span_id":"def456","order_id":"ord_123","msg":"Payment processed"}
```

---

## Quick Reference

### When to Use What

| Scenario | Tool/Pattern | Reason |
|----------|--------------|--------|
| Metrics collection | Prometheus + Grafana | Industry standard, powerful query language |
| Distributed tracing | OpenTelemetry + Tempo/Jaeger | Vendor-neutral, CNCF standard |
| Log aggregation (cost-sensitive) | Grafana Loki | Indexes only labels, 10x cheaper |
| Log aggregation (search-heavy) | ELK Stack | Full-text search, advanced analytics |
| Unified observability | Elastic/Datadog/Dynatrace | Single pane of glass for all telemetry |
| Incident management | PagerDuty/Opsgenie | Alert routing, on-call scheduling |
| Chaos engineering | Gremlin/Chaos Mesh | Controlled failure injection |
| AIOps/Anomaly detection | Dynatrace/Datadog | AI-driven root cause analysis |

### The Three Pillars

| Pillar | What | When | Tools |
|--------|------|------|-------|
| **Metrics** | Numerical time-series data | Real-time monitoring, alerting | Prometheus, StatsD, CloudWatch |
| **Logs** | Event records with context | Debugging, audit trails | Loki, ELK, Splunk |
| **Traces** | Request journey across services | Performance analysis, dependencies | OpenTelemetry, Jaeger, Zipkin |

**Fourth Pillar (Emerging):** Continuous Profiling — Code-level performance data (CPU, memory usage at function level)

---

## Observability Architecture

### Layered Prometheus Setup

```yaml
# 2025 Best Practice: Federated architecture
# Prevents metric chaos while enabling drill-down

# Layer 1: Application Prometheus
# - Detailed business logic metrics
# - High cardinality acceptable
# - Short retention (7 days)

# Layer 2: Cluster Prometheus
# - Per-environment/cluster metrics
# - Medium retention (30 days)
# - Aggregates from application level

# Layer 3: Global Prometheus
# - Cross-cluster critical metrics
# - Long retention (1 year)
# - Federation from cluster level

# Global Prometheus config
scrape_configs:
  - job_name: 'federate'
    scrape_interval: 15s
    honor_labels: true
    metrics_path: '/federate'
    params:
      'match[]':
        - '{job="kubernetes-nodes"}'
        - '{__name__=~"job:.*"}'  # Recording rules only
    static_configs:
      - targets:
        - 'cluster-prom-us-east.internal:9090'
        - 'cluster-prom-eu-west.internal:9090'
```

### Recording Rules for Performance

```yaml
# Precompute expensive queries
groups:
  - name: api_performance
    interval: 30s
    rules:
      # Request rate (requests per second)
      - record: job:api_requests:rate5m
        expr: sum(rate(http_requests_total[5m])) by (job, method, status)

      # Error rate
      - record: job:api_errors:rate5m
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (job)
          /
          sum(rate(http_requests_total[5m])) by (job)

      # P95 latency
      - record: job:api_latency:p95
        expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))
```

### Resource Optimization

```yaml
# Increase scrape interval for high-target deployments
scrape_interval: 30s  # Default: 15s reduces load by 50%

# Use relabeling to drop unnecessary metrics
metric_relabel_configs:
  - source_labels: [__name__]
    regex: 'go_.*|process_.*'  # Drop Go runtime metrics
    action: drop

# Limit sample retention
storage:
  tsdb:
    retention.time: 15d  # Keep only 15 days locally
    retention.size: 50GB # Or max 50GB
```

---

## Distributed Tracing with OpenTelemetry

### Auto-Instrumentation Setup

```typescript
// Node.js auto-instrumentation
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: 'http://otel-collector:4318/v1/traces',
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      // Auto-instruments HTTP, Express, PostgreSQL, Redis, etc.
      '@opentelemetry/instrumentation-fs': { enabled: false }, // Too noisy
    }),
  ],
});

sdk.start();
```

### Manual Instrumentation for Business Logic

```typescript
import { trace, SpanStatusCode } from '@opentelemetry/api';

const tracer = trace.getTracer('payment-service', '1.0.0');

async function processPayment(orderId: string, amount: number) {
  // Create custom span for business operation
  return tracer.startActiveSpan('processPayment', async (span) => {
    try {
      // Add business context
      span.setAttributes({
        'order.id': orderId,
        'payment.amount': amount,
        'payment.currency': 'USD',
      });

      // Child span for external API call
      const paymentResult = await tracer.startActiveSpan('stripe.charge', async (childSpan) => {
        const result = await stripe.charges.create({ amount, currency: 'usd' });
        childSpan.setAttribute('stripe.charge_id', result.id);
        childSpan.setStatus({ code: SpanStatusCode.OK });
        childSpan.end();
        return result;
      });

      span.setStatus({ code: SpanStatusCode.OK });
      return paymentResult;
    } catch (error) {
      span.recordException(error);
      span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
      throw error;
    } finally {
      span.end();
    }
  });
}
```

### Sampling Strategies

```yaml
# OpenTelemetry Collector config
processors:
  # Probabilistic sampling: Keep 10% of traces
  probabilistic_sampler:
    sampling_percentage: 10

  # Tail sampling: Make decisions after seeing full trace
  tail_sampling:
    policies:
      # Always sample errors
      - name: error-traces
        type: status_code
        status_code: {status_codes: [ERROR]}

      # Always sample slow requests
      - name: slow-traces
        type: latency
        latency: {threshold_ms: 1000}

      # Sample 5% of normal traffic
      - name: normal-traces
        type: probabilistic
        probabilistic: {sampling_percentage: 5}
```

### Context Propagation

```typescript
// Ensure trace context flows across services
import { propagation, context } from '@opentelemetry/api';

// Outgoing HTTP request (automatic with auto-instrumentation)
fetch('https://api.example.com/data', {
  headers: {
    // W3C Trace Context headers injected automatically:
    // traceparent: 00-<trace-id>-<span-id>-01
    // tracestate: vendor=value
  },
});

// Manual propagation for non-HTTP (e.g., message queues)
const carrier = {};
propagation.inject(context.active(), carrier);
await publishMessage(queue, { data: payload, headers: carrier });
```

---

## Structured Logging Best Practices

### JSON Logging Format

```typescript
// Use structured logging library
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
  // Include trace context in logs
  mixin() {
    const span = trace.getActiveSpan();
    if (!span) return {};

    const { traceId, spanId } = span.spanContext();
    return {
      trace_id: traceId,
      span_id: spanId,
    };
  },
});

// Structured logging with context
logger.info(
  {
    user_id: '123',
    order_id: 'ord_456',
    amount: 99.99,
    payment_method: 'card',
  },
  'Payment processed successfully'
);

// Output:
// {"level":"info","time":"2025-01-15T10:30:00.000Z","trace_id":"abc123","span_id":"def456","user_id":"123","order_id":"ord_456","amount":99.99,"payment_method":"card","msg":"Payment processed successfully"}
```

### Log Levels

```typescript
// Follow standard severity levels
logger.trace({ details }, 'Low-level debugging');     // Very verbose
logger.debug({ state }, 'Debug information');          // Development
logger.info({ event }, 'Normal operation');            // Production default
logger.warn({ issue }, 'Warning condition');           // Potential issues
logger.error({ error, context }, 'Error occurred');    // Errors
logger.fatal({ critical }, 'Fatal error');             // Process crash
```

### Grafana Loki Configuration

```yaml
# Promtail config - ships logs to Loki
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: kubernetes
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      # Add pod labels as Loki labels (LOW cardinality only!)
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod
      - source_labels: [__meta_kubernetes_pod_label_app]
        target_label: app
    pipeline_stages:
      # Parse JSON logs
      - json:
          expressions:
            level: level
            trace_id: trace_id
      # Extract fields as labels
      - labels:
          level:
          trace_id:
```

### Loki Best Practices

- **Low Cardinality Labels** — Use only 5-10 labels (namespace, app, level)
- **High Cardinality in Log Body** — Put user_id, order_id in JSON, not labels
- **LogQL for Filtering** — Use `{app="api"} | json | user_id="123"`
- **Retention Policy** — Keep recent logs longer, compress old logs

```promql
# LogQL query examples
{namespace="production", app="api"} |= "error"  # Text search

{app="api"} | json | level="error" | line_format "{{.msg}}"  # JSON parsing

rate({app="api"}[5m])  # Log rate per second

sum by (level) (count_over_time({namespace="production"}[1h]))  # Count by level
```

---


## Extended Reference

Detailed material starting at `## SLO/SLI/SLA Management` has been moved to [`reference/extended.md`](reference/extended.md) to keep this skill concise. Load that reference when the task requires the moved examples, command catalogs, checklists, platform details, or implementation templates.
