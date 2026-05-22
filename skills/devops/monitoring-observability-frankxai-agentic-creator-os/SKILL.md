---
name: monitoring-observability
description: "Monitoring, logging, and observability patterns. Covers structured logging, metrics, tracing, alerting, and dashboards with tools like Sentry, Datadog, and OpenTelemetry."
version: 1.0.0
triggers:
  - monitoring
  - logging
  - observability
  - metrics
  - tracing
  - sentry
  - datadog
---

# Monitoring & Observability Skill

Implement comprehensive observability for production applications with logging, metrics, and tracing.

## The Three Pillars

| Pillar | Purpose | Tools |
|--------|---------|-------|
| **Logs** | What happened | Pino, Winston, Sentry |
| **Metrics** | Quantitative data | Prometheus, Datadog |
| **Traces** | Request flow | OpenTelemetry, Jaeger |

## Structured Logging

### Pino Setup (Recommended)

```typescript
// lib/logger.ts
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
  redact: ['password', 'token', 'authorization', 'cookie'],
  base: {
    env: process.env.NODE_ENV,
    version: process.env.APP_VERSION,
  },
});

// Usage
logger.info({ userId: '123', action: 'login' }, 'User logged in');
logger.error({ err, requestId }, 'Request failed');
```

### Request Logging Middleware

```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server';
import { logger } from '@/lib/logger';
import { nanoid } from 'nanoid';

export function middleware(request: NextRequest) {
  const requestId = nanoid();
  const start = Date.now();

  const response = NextResponse.next();
  response.headers.set('x-request-id', requestId);

  // Log after response
  logger.info({
    requestId,
    method: request.method,
    path: request.nextUrl.pathname,
    duration: Date.now() - start,
    status: response.status,
    userAgent: request.headers.get('user-agent'),
  }, 'Request completed');

  return response;
}
```

## Error Tracking with Sentry

### Setup

```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1, // 10% of transactions
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
});
```

### Error Boundary

```tsx
// components/ErrorBoundary.tsx
'use client';

import * as Sentry from '@sentry/nextjs';

export function ErrorBoundary({ error, reset }: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    Sentry.captureException(error);
  }, [error]);

  return (
    <div className="error-container">
      <h2>Something went wrong</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### Manual Error Capture

```typescript
import * as Sentry from '@sentry/nextjs';

try {
  await riskyOperation();
} catch (error) {
  Sentry.captureException(error, {
    tags: { feature: 'payment' },
    extra: { userId, orderId },
  });
  throw error;
}
```

## Metrics with Prometheus

### Metrics Endpoint

```typescript
// app/api/metrics/route.ts
import { Registry, Counter, Histogram, collectDefaultMetrics } from 'prom-client';

const register = new Registry();
collectDefaultMetrics({ register });

// Custom metrics
const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'path', 'status'],
  registers: [register],
});

const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration',
  labelNames: ['method', 'path'],
  buckets: [0.1, 0.3, 0.5, 1, 3, 5, 10],
  registers: [register],
});

export async function GET() {
  const metrics = await register.metrics();
  return new Response(metrics, {
    headers: { 'Content-Type': register.contentType },
  });
}

// Export for use in middleware
export { httpRequestsTotal, httpRequestDuration };
```

## Distributed Tracing with OpenTelemetry

```typescript
// instrumentation.ts
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT,
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

## Health Checks

```typescript
// app/api/health/route.ts
import { db } from '@/lib/db';
import { redis } from '@/lib/redis';

export async function GET() {
  const checks = {
    database: await checkDatabase(),
    redis: await checkRedis(),
    uptime: process.uptime(),
  };

  const healthy = Object.values(checks).every(c =>
    typeof c === 'object' ? c.status === 'ok' : true
  );

  return Response.json(
    { status: healthy ? 'healthy' : 'unhealthy', checks },
    { status: healthy ? 200 : 503 }
  );
}

async function checkDatabase() {
  try {
    await db.$queryRaw`SELECT 1`;
    return { status: 'ok' };
  } catch (error) {
    return { status: 'error', error: error.message };
  }
}

async function checkRedis() {
  try {
    await redis.ping();
    return { status: 'ok' };
  } catch (error) {
    return { status: 'error', error: error.message };
  }
}
```

## Alerting Rules

```yaml
# prometheus/alerts.yml
groups:
  - name: app-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"

      - alert: SlowResponses
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "95th percentile latency above 2s"
```

## Dashboard Queries (Grafana)

```
# Request rate
rate(http_requests_total[5m])

# Error rate percentage
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) * 100

# P95 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Active users
sum(increase(user_sessions_total[1h]))
```

## Anti-Patterns

❌ Logging sensitive data (passwords, tokens)
❌ No request IDs for correlation
❌ Sampling at 100% in production
❌ Ignoring errors silently
❌ No alerts on critical paths

✅ Structured JSON logs with redaction
✅ Request ID propagation
✅ Appropriate sampling rates
✅ Capture and alert on errors
✅ Runbooks for each alert
