---
name: observability
description: Structured logging with Pino/Winston, OpenTelemetry tracing, metrics collection, Grafana dashboards, and alerting rules.
---

# Observability Patterns

Three pillars of observability: logs, traces, and metrics. Each answers different questions.

## Structured Logging with Pino (Node.js)

Pino is the fastest Node.js logger. Always emit JSON; never plain strings.

```typescript
// logger.ts
import pino from 'pino'

export const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  formatters: {
    level(label) {
      return { level: label }        // emit "level":"info" not numeric
    }
  },
  base: {
    service: process.env.SERVICE_NAME ?? 'api',
    version: process.env.APP_VERSION ?? 'unknown',
    env: process.env.NODE_ENV ?? 'development'
  },
  timestamp: pino.stdTimeFunctions.isoTime,
  redact: {
    paths: ['req.headers.authorization', 'body.password', '*.token'],
    censor: '[REDACTED]'
  }
})
```

```typescript
// Usage examples
import { logger } from './logger'

// Child logger with request context
const reqLogger = logger.child({
  requestId: crypto.randomUUID(),
  userId: user.id,
  path: req.path
})

reqLogger.info('Processing payment')
reqLogger.warn({ amount, currency }, 'Payment above threshold')
reqLogger.error({ err }, 'Payment failed')
```

## Structured Logging with Python (structlog)

```python
# logging_config.py
import structlog
import logging

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

log = structlog.get_logger()
```

```python
# Usage
log.info("request.received", path="/api/users", method="GET")
log.warning("rate_limit.approaching", user_id=user.id, count=95, limit=100)
log.error("payment.failed", exc_info=True, order_id=order.id, amount=99.99)

# Bind context for duration of request
structlog.contextvars.bind_contextvars(request_id=request_id, user_id=user_id)
log.info("order.created")   # request_id and user_id included automatically
structlog.contextvars.clear_contextvars()
```

## Log Levels Usage Guide

| Level | When to Use | Example |
|-------|-------------|---------|
| `trace` | Detailed execution path (dev only) | Function entry/exit, loop iterations |
| `debug` | Diagnostic info for debugging | SQL queries, cache hit/miss |
| `info` | Normal operations | Request received, job started, user login |
| `warn` | Unexpected but recoverable | Retry attempt, fallback used, slow query |
| `error` | Errors requiring investigation | DB connection failed, 3rd party API error |
| `fatal` | Process must exit | Config missing, port in use |

```typescript
// Good log message guidelines
// ✅ Include who, what, why, and relevant IDs
logger.info({ userId, orderId, amount }, 'order.created')

// ❌ Vague message, no context
logger.info('Order done')

// ✅ Error includes the actual error object
logger.error({ err, orderId }, 'order.payment.failed')

// ❌ Error swallowed or only string
logger.error('Payment error: ' + err.message)
```

## Request Correlation IDs

Trace a request across multiple services by propagating a unique ID.

```typescript
// Express middleware: assign or forward correlation ID
import { randomUUID } from 'crypto'
import { AsyncLocalStorage } from 'async_hooks'

const requestContext = new AsyncLocalStorage<{ requestId: string; userId?: string }>()

export function correlationMiddleware(req: Request, res: Response, next: NextFunction) {
  const requestId = (req.headers['x-request-id'] as string) ?? randomUUID()

  res.setHeader('x-request-id', requestId)

  requestContext.run({ requestId }, () => {
    next()
  })
}

// Get context anywhere in call stack (no prop drilling)
export function getRequestId(): string {
  return requestContext.getStore()?.requestId ?? 'unknown'
}

// Logger auto-includes correlation ID
export function getLogger() {
  return logger.child({ requestId: getRequestId() })
}
```

## OpenTelemetry Tracing

```typescript
// tracing.ts - must be imported FIRST before other modules
import { NodeSDK } from '@opentelemetry/sdk-node'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'
import { HttpInstrumentation } from '@opentelemetry/instrumentation-http'
import { ExpressInstrumentation } from '@opentelemetry/instrumentation-express'
import { PgInstrumentation } from '@opentelemetry/instrumentation-pg'

const sdk = new NodeSDK({
  serviceName: process.env.SERVICE_NAME ?? 'api',
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT ?? 'http://localhost:4318/v1/traces'
  }),
  instrumentations: [
    new HttpInstrumentation(),
    new ExpressInstrumentation(),
    new PgInstrumentation()
  ]
})

sdk.start()

process.on('SIGTERM', () => sdk.shutdown())
```

```typescript
// Manual spans for business logic
import { trace, SpanStatusCode, context } from '@opentelemetry/api'

const tracer = trace.getTracer('payment-service')

async function processPayment(orderId: string, amount: number) {
  return tracer.startActiveSpan('payment.process', async (span) => {
    span.setAttributes({
      'order.id': orderId,
      'payment.amount': amount,
      'payment.currency': 'USD'
    })

    try {
      const result = await chargeCard(amount)
      span.setStatus({ code: SpanStatusCode.OK })
      return result
    } catch (error) {
      span.recordException(error as Error)
      span.setStatus({ code: SpanStatusCode.ERROR, message: (error as Error).message })
      throw error
    } finally {
      span.end()
    }
  })
}
```

## Custom Metrics with Prometheus

```typescript
// metrics.ts
import { Registry, Counter, Histogram, Gauge } from 'prom-client'

export const registry = new Registry()

// HTTP request counter
export const httpRequestTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
  registers: [registry]
})

// Request duration histogram
export const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
  registers: [registry]
})

// Active connections gauge
export const activeConnections = new Gauge({
  name: 'active_connections',
  help: 'Number of active WebSocket connections',
  registers: [registry]
})
```

```typescript
// Metrics middleware
export function metricsMiddleware(req: Request, res: Response, next: NextFunction) {
  const start = Date.now()

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000
    const labels = {
      method: req.method,
      route: req.route?.path ?? req.path,
      status_code: String(res.statusCode)
    }
    httpRequestTotal.inc(labels)
    httpRequestDuration.observe(labels, duration)
  })

  next()
}

// Metrics endpoint (scrape target for Prometheus)
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', registry.contentType)
  res.send(await registry.metrics())
})
```

## Error Tracking with Sentry

```typescript
// sentry.ts
import * as Sentry from '@sentry/node'
import { nodeProfilingIntegration } from '@sentry/profiling-node'

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  release: process.env.APP_VERSION,
  integrations: [nodeProfilingIntegration()],
  tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,
  profilesSampleRate: 0.1,
  beforeSend(event, hint) {
    // Strip PII from errors
    if (event.user) {
      delete event.user.email
      delete event.user.ip_address
    }
    return event
  }
})

// Capture with context
try {
  await processOrder(orderId)
} catch (error) {
  Sentry.withScope((scope) => {
    scope.setTag('order.id', orderId)
    scope.setLevel('error')
    Sentry.captureException(error)
  })
  throw error
}
```

## Grafana Dashboard Templates

```json
// dashboard panel: Request Rate (PromQL)
{
  "title": "Request Rate",
  "type": "timeseries",
  "targets": [{
    "expr": "sum(rate(http_requests_total[5m])) by (route)",
    "legendFormat": "{{route}}"
  }]
}
```

```
# PromQL expressions for common panels

# Request rate (req/s over 5 min window)
sum(rate(http_requests_total[5m])) by (route, method)

# Error rate (%)
sum(rate(http_requests_total{status_code=~"5.."}[5m]))
  / sum(rate(http_requests_total[5m])) * 100

# Latency percentiles
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, route))
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, route))
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, route))

# Apdex score (satisfied < 0.3s, tolerated < 1.2s)
(
  sum(rate(http_request_duration_seconds_bucket{le="0.3"}[5m]))
  + sum(rate(http_request_duration_seconds_bucket{le="1.2"}[5m]))
) / 2 / sum(rate(http_request_duration_seconds_count[5m]))
```

## Alert Rules (SLO-Based)

```yaml
# prometheus/alerts.yml
groups:
  - name: slo.alerts
    rules:
      # Error budget burn rate (fast burn = page immediately)
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status_code=~"5.."}[5m]))
            / sum(rate(http_requests_total[5m]))
          ) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Error rate above 1% SLO"
          description: "Error rate is {{ $value | humanizePercentage }}"

      # p99 latency SLO breach
      - alert: HighLatencyP99
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
          ) > 1.0
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "p99 latency above 1s SLO"

      # Service availability
      - alert: ServiceDown
        expr: up{job="api"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "API service is down"
```

## Health Check Monitoring

```typescript
// Composite health check endpoint
interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy'
  checks: Record<string, { status: string; latencyMs?: number; error?: string }>
}

app.get('/health/detailed', async (req, res) => {
  const checks: HealthStatus['checks'] = {}

  // Database check
  const dbStart = Date.now()
  try {
    await db.execute('SELECT 1')
    checks.database = { status: 'ok', latencyMs: Date.now() - dbStart }
  } catch (err) {
    checks.database = { status: 'fail', error: (err as Error).message }
  }

  // Redis check
  const redisStart = Date.now()
  try {
    await redis.ping()
    checks.redis = { status: 'ok', latencyMs: Date.now() - redisStart }
  } catch (err) {
    checks.redis = { status: 'fail', error: (err as Error).message }
  }

  const allHealthy = Object.values(checks).every(c => c.status === 'ok')
  const anyFailing = Object.values(checks).some(c => c.status === 'fail')

  const overall: HealthStatus['status'] = allHealthy
    ? 'healthy'
    : anyFailing ? 'unhealthy' : 'degraded'

  res.status(allHealthy ? 200 : 503).json({ status: overall, checks })
})
```

## Dynamic Log Level in Production

```typescript
// Change log level without restart
import { logger } from './logger'

app.put('/admin/log-level', requireAdminAuth, (req, res) => {
  const { level } = req.body
  const validLevels = ['trace', 'debug', 'info', 'warn', 'error', 'fatal']

  if (!validLevels.includes(level)) {
    return res.status(400).json({ error: 'Invalid level' })
  }

  logger.level = level
  logger.info({ level }, 'Log level changed')
  res.json({ level })
})
```

## Log Rotation and Retention

```bash
# logrotate config: /etc/logrotate.d/app
/var/log/app/*.log {
  daily
  rotate 14          # keep 14 days
  compress
  delaycompress
  missingok
  notifempty
  postrotate
    kill -USR1 $(cat /var/run/app.pid) 2>/dev/null || true
  endscript
}
```

```yaml
# Docker logging with size-based rotation
services:
  api:
    logging:
      driver: json-file
      options:
        max-size: "50m"
        max-file: "5"
        labels: "service,version"
```

## APM Integration (Datadog-style without vendor lock-in)

```typescript
// OpenTelemetry collector config: otel-collector.yml
# ships to multiple backends simultaneously
exporters:
  otlp/datadog:
    endpoint: https://api.datadoghq.com/v1/traces
    headers:
      dd-api-key: ${DD_API_KEY}
  prometheus:
    endpoint: 0.0.0.0:8889
  loki:
    endpoint: http://loki:3100/loki/api/v1/push

pipelines:
  traces:
    receivers: [otlp]
    processors: [batch, resourcedetection]
    exporters: [otlp/datadog]
  metrics:
    receivers: [otlp, prometheus]
    exporters: [prometheus]
  logs:
    receivers: [otlp]
    exporters: [loki]
```

**Key principle**: Correlate logs, traces, and metrics by the same `requestId`/`traceId`. Emit structured JSON from day one — retrofitting is painful. Set up alerts on SLO burn rate, not absolute thresholds.
