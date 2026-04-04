---
name: monitoring-observability
description: Provides monitoring and observability best practices covering the three pillars (logs, metrics, traces), OpenTelemetry instrumentation, Prometheus/Grafana dashboards, SLO-based alerting, and APM strategies. Use when setting up monitoring, observability, prometheus, grafana, opentelemetry, alerting, tracing, logging, metrics, dashboards, SLOs, or APM.
---

# Monitoring and Observability

Production systems require visibility into their behavior. Observability goes beyond simple monitoring by enabling you to ask arbitrary questions about system state using logs, metrics, and traces. This guide covers instrumentation, collection, visualization, alerting, and the operational patterns that prevent alert fatigue while keeping systems reliable.

## The Three Pillars

| Pillar | What It Captures | Best For | Key Tools |
|--------|-----------------|----------|-----------|
| Logs | Discrete events with context | Debugging specific requests, audit trails | ELK, Loki, CloudWatch Logs |
| Metrics | Numeric measurements over time | Trends, thresholds, capacity planning | Prometheus, Datadog, CloudWatch Metrics |
| Traces | Request flow across services | Latency breakdown, dependency mapping | Jaeger, Tempo, X-Ray |

| Question | Signal |
|----------|--------|
| "Why did this request fail?" | Logs (event detail) + Traces (call chain) |
| "Is error rate increasing?" | Metrics (counters over time) |
| "Which service is slow?" | Traces (span timing) |
| "What happened at 3:42 AM?" | Logs (timestamped events) |
| "Are we within SLO budget?" | Metrics (error ratio, latency percentiles) |
| "How do services depend on each other?" | Traces (service graph) |

## OpenTelemetry SDK Setup

OpenTelemetry provides a vendor-neutral API for emitting all three signals. Instrument once, export anywhere.

### Node.js Auto-Instrumentation

```typescript
// tracing.ts -- Load BEFORE application code
import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-http';
import { PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { Resource } from '@opentelemetry/resources';
import { ATTR_SERVICE_NAME, ATTR_SERVICE_VERSION } from '@opentelemetry/semantic-conventions';

const sdk = new NodeSDK({
  resource: new Resource({
    [ATTR_SERVICE_NAME]: 'order-service',
    [ATTR_SERVICE_VERSION]: process.env.APP_VERSION || '0.0.0',
  }),
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4318/v1/traces',
  }),
  metricReader: new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter(),
    exportIntervalMillis: 15000,
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      '@opentelemetry/instrumentation-fs': { enabled: false },
      '@opentelemetry/instrumentation-http': {
        ignoreIncomingPaths: ['/healthz', '/readyz', '/metrics'],
      },
    }),
  ],
});

sdk.start();
process.on('SIGTERM', () => sdk.shutdown().finally(() => process.exit(0)));
```

### Manual Span Creation

```typescript
import { trace, SpanStatusCode } from '@opentelemetry/api';

const tracer = trace.getTracer('order-service', '1.0.0');

async function processOrder(orderId: string): Promise<Order> {
  return tracer.startActiveSpan('processOrder', async (span) => {
    try {
      span.setAttribute('order.id', orderId);

      const order = await tracer.startActiveSpan('db.fetchOrder', async (dbSpan) => {
        dbSpan.setAttribute('db.system', 'postgresql');
        const result = await db.orders.findById(orderId);
        dbSpan.end();
        return result;
      });

      span.addEvent('order.validated', { 'order.total': order.total });
      await chargePayment(order);
      span.setStatus({ code: SpanStatusCode.OK });
      return order;
    } catch (error) {
      span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
      span.recordException(error);
      throw error;
    } finally {
      span.end();
    }
  });
}
```

## Prometheus Metrics

Prometheus uses a pull model -- it scrapes HTTP endpoints at intervals.

| Type | Use Case | Example |
|------|----------|---------|
| Counter | Cumulative count (only goes up) | Total requests, errors, bytes sent |
| Gauge | Current value (goes up and down) | Active connections, queue depth |
| Histogram | Distribution of values in buckets | Request latency, response size |
| Summary | Quantiles calculated client-side | Legacy use -- prefer histograms |

### Express Application Metrics

```typescript
import express from 'express';
import promClient from 'prom-client';

const app = express();
promClient.collectDefaultMetrics({ prefix: 'orderservice_' });

const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
});

const httpRequestsTotal = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
});

app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer();
  res.on('finish', () => {
    const labels = { method: req.method, route: req.route?.path || req.path, status_code: res.statusCode.toString() };
    end(labels);
    httpRequestsTotal.inc(labels);
  });
  next();
});

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', promClient.register.contentType);
  res.end(await promClient.register.metrics());
});
```

## Grafana Dashboard

Define dashboards as JSON for version control. Key panels for any service overview:

```json
{
  "dashboard": {
    "title": "Order Service Overview",
    "refresh": "30s",
    "panels": [
      {
        "title": "Request Rate",
        "type": "timeseries",
        "targets": [{
          "expr": "sum(rate(http_requests_total{service=\"order-service\"}[5m])) by (status_code)",
          "legendFormat": "{{status_code}}"
        }],
        "fieldConfig": { "defaults": { "unit": "reqps" } }
      },
      {
        "title": "P99 Latency",
        "type": "timeseries",
        "targets": [{
          "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service=\"order-service\"}[5m])) by (le, route))",
          "legendFormat": "{{route}}"
        }],
        "fieldConfig": { "defaults": { "unit": "s" } }
      },
      {
        "title": "Error Rate (SLO: 99.9%)",
        "type": "stat",
        "targets": [{
          "expr": "1 - (sum(rate(http_requests_total{service=\"order-service\", status_code=~\"5..\"}[1h])) / sum(rate(http_requests_total{service=\"order-service\"}[1h])))",
          "instant": true
        }],
        "fieldConfig": { "defaults": { "unit": "percentunit" } }
      }
    ]
  }
}
```

## SLO-Based Alerting

Alert on Service Level Objectives, not raw thresholds. This ties alerting to user-visible impact.

| Concept | Definition | Example |
|---------|-----------|---------|
| SLI | Service Level Indicator -- a measured metric | Proportion of requests < 300ms |
| SLO | Service Level Objective -- target for the SLI | 99.9% of requests < 300ms |
| Error Budget | Allowed failures = 1 - SLO | 0.1% can be slow (43 min/month) |
| Burn Rate | How fast you consume error budget | 2x = burning twice as fast as sustainable |

### Multi-Window Burn Rate Alerts

```yaml
# alerts/slo-alerts.yml
groups:
  - name: slo-burn-rate
    rules:
      # Fast burn -- 2% of 30-day budget in 1 hour
      - alert: HighErrorBudgetBurnRate_Fast
        expr: |
          (
            sum(rate(http_requests_total{status_code=~"5..", service="order-service"}[1h]))
            / sum(rate(http_requests_total{service="order-service"}[1h]))
          ) > (14.4 * 0.001)
          and
          (
            sum(rate(http_requests_total{status_code=~"5..", service="order-service"}[5m]))
            / sum(rate(http_requests_total{service="order-service"}[5m]))
          ) > (14.4 * 0.001)
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Burning error budget 14.4x faster than sustainable"
          runbook: "https://wiki.internal/runbooks/order-service-high-errors"

      # Slow burn -- 10% of budget in 3 days
      - alert: HighErrorBudgetBurnRate_Slow
        expr: |
          (
            sum(rate(http_requests_total{status_code=~"5..", service="order-service"}[6h]))
            / sum(rate(http_requests_total{service="order-service"}[6h]))
          ) > (1.0 * 0.001)
        for: 30m
        labels:
          severity: warning
        annotations:
          summary: "Slowly burning error budget"

      # Latency SLO
      - alert: LatencySLOBreach
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket{service="order-service"}[5m])) by (le)
          ) > 0.3
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "P99 latency exceeds 300ms SLO"
```

## Log Aggregation Patterns

### Structured Logging with Trace Correlation

```typescript
import pino from 'pino';
import { context, trace } from '@opentelemetry/api';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  mixin() {
    const span = trace.getSpan(context.active());
    if (span) {
      const { traceId, spanId } = span.spanContext();
      return { traceId, spanId };
    }
    return {};
  },
  redact: {
    paths: ['req.headers.authorization', 'password', 'ssn', 'creditCard'],
    censor: '[REDACTED]',
  },
});

// Good: structured with context
logger.info({ orderId, userId, total: order.total }, 'Order placed successfully');

// Bad: unstructured string interpolation -- not queryable, PII leaks
// logger.info(`Order ${orderId} placed by user ${userId} for $${total}`);
```

### Loki Query Examples

```logql
# Find errors for a specific trace
{service="order-service"} |= "error" | json | traceId="abc123def456"

# Error rate by service
sum(rate({service=~".+"} |= "error" [5m])) by (service)

# Slow database queries
{service="order-service"} | json | db_duration_ms > 500
```

## Distributed Tracing with Context Propagation

```
Client -> API Gateway -> Order Service -> Payment Service -> Database
  |           |              |                |
  trace_id=abc trace_id=abc  trace_id=abc     trace_id=abc
  span_id=001  span_id=002   span_id=003      span_id=004
               parent=001    parent=002       parent=003
```

```typescript
import { context, propagation } from '@opentelemetry/api';

// Outgoing: inject trace context into headers
async function callPaymentService(order: Order): Promise<PaymentResult> {
  const headers: Record<string, string> = {};
  propagation.inject(context.active(), headers);

  return fetch('https://payment-service/charge', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...headers },
    body: JSON.stringify({ orderId: order.id, amount: order.total }),
  }).then(r => r.json());
}

// Incoming via message queue: extract manually
function processMessage(message: QueueMessage) {
  const parentContext = propagation.extract(context.active(), message.headers);
  context.with(parentContext, () => {
    tracer.startActiveSpan('processMessage', (span) => {
      // spans here are children of the original trace
      span.end();
    });
  });
}
```

## APM Business Metrics

```typescript
import { metrics } from '@opentelemetry/api';

const meter = metrics.getMeter('order-service', '1.0.0');

const orderCounter = meter.createCounter('orders_total', {
  description: 'Total orders processed',
});
const orderValue = meter.createHistogram('order_value_dollars', {
  description: 'Distribution of order values',
});

async function completeOrder(order: Order) {
  orderCounter.add(1, { payment_method: order.paymentMethod, region: order.region });
  orderValue.record(order.total, { currency: order.currency });
}
```

## Alert Fatigue Prevention

| Strategy | Implementation | Impact |
|----------|---------------|--------|
| Alert on symptoms, not causes | Alert on error rate, not CPU | Fewer alerts, user-facing focus |
| Multi-window burn rates | Short + long window must both fire | Eliminates transient spikes |
| Severity routing | Critical -> page, Warning -> ticket | Right urgency for right signal |
| Alert deduplication | Group related alerts by service | One alert per incident |
| Regular alert review | Monthly: delete or tune noisy alerts | Continuous improvement |
| Require runbook links | Every alert links to a runbook | Responders know what to do |
| Error budget based | Alert when burning budget, not on every error | Tolerates expected failure rate |
| Inhibition rules | Critical suppresses warning for same service | Reduces duplicate noise |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Alerting on raw thresholds (CPU > 80%) | Alerts on non-issues, misses real problems | Alert on SLOs and user-facing symptoms |
| No structured logging | Logs are unsearchable at scale | Use JSON structured logging with consistent fields |
| Missing trace context in logs | Cannot correlate logs with traces | Inject traceId/spanId via logger mixin |
| High-cardinality metric labels | Prometheus memory explosion, slow queries | Never use userId, requestId, or IP as label values |
| Alerting without runbooks | Responders waste time figuring out what to do | Require runbook URL in every alert annotation |
| Sampling 100% of traces | Storage costs explode, collectors overloaded | Use head-based or tail-based sampling (1-10%) |
| Logging PII in plaintext | Compliance violations (GDPR, HIPAA) | Redact sensitive fields, use structured redaction |
| Dashboard sprawl without ownership | Stale dashboards with broken queries | Assign team owners, review quarterly |
| Monitoring only infrastructure | Misses application-level failures | Add business KPI metrics (orders/sec, revenue) |
| Ignoring metric staleness | Stale metrics give false "all clear" | Alert on absent metrics with `absent()` function |
| No log retention policy | Storage costs grow indefinitely | Set TTLs: 7d hot, 30d warm, 90d cold, archive |
| Synchronous log shipping | Log pipeline failure blocks application | Use async buffered shipping with local fallback |
| No baseline for normal | Cannot detect anomalies | Record baselines during stable periods |

## Observability Maturity Checklist

### Level 1: Foundations

- [ ] Structured JSON logging with consistent field names across services
- [ ] Health check endpoints (`/healthz`, `/readyz`) on all services
- [ ] Prometheus metrics endpoint exposed on all services
- [ ] Default runtime metrics collected (memory, CPU, GC, event loop)
- [ ] Centralized log aggregation (ELK, Loki, or cloud-native)

### Level 2: Instrumentation

- [ ] OpenTelemetry SDK integrated with auto-instrumentation
- [ ] Custom business metrics defined (orders/sec, revenue, conversion)
- [ ] Distributed tracing with context propagation across services
- [ ] Trace context injected into log entries (traceId, spanId)
- [ ] Grafana dashboards with RED metrics (Rate, Errors, Duration)

### Level 3: Alerting

- [ ] SLOs defined for each critical user journey
- [ ] Multi-window burn rate alerts replacing threshold alerts
- [ ] Every alert has a linked runbook with remediation steps
- [ ] Alert routing configured by severity (page / ticket / dashboard)
- [ ] Alert fatigue review conducted monthly
- [ ] `absent()` alerts for metrics that stop reporting

### Level 4: Advanced

- [ ] Tail-based trace sampling to capture errors and slow requests
- [ ] Exemplars linking metrics to specific traces
- [ ] Error budget tracking visible on team dashboards
- [ ] Anomaly detection on key business metrics
- [ ] Observability costs tracked and optimized
