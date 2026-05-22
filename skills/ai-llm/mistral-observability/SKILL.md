---
name: mistral-observability
description: |
  Set up comprehensive observability for Mistral AI integrations with metrics, traces, and alerts.
  Use when implementing monitoring for Mistral AI operations, setting up dashboards,
  or configuring alerting for Mistral AI integration health.
  Trigger with phrases like "mistral monitoring", "mistral metrics",
  "mistral observability", "monitor mistral", "mistral alerts", "mistral tracing".
allowed-tools: Read, Write, Edit
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Mistral AI Observability

## Overview
Set up comprehensive observability for Mistral AI integrations.

## Prerequisites
- Prometheus or compatible metrics backend
- OpenTelemetry SDK installed (optional)
- Grafana or similar dashboarding tool
- AlertManager or similar alerting system

## Instructions

### Step 1: Define Key Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `mistral_requests_total` | Counter | Total API requests |
| `mistral_request_duration_seconds` | Histogram | Request latency |
| `mistral_tokens_total` | Counter | Tokens used (input/output) |
| `mistral_errors_total` | Counter | Error count by type |
| `mistral_cost_usd` | Counter | Estimated cost |
| `mistral_cache_hits_total` | Counter | Cache hit count |

### Step 2: Implement Prometheus Metrics

```typescript
import { Registry, Counter, Histogram, Gauge } from 'prom-client';

const registry = new Registry();

// Request counter
const requestCounter = new Counter({
  name: 'mistral_requests_total',
  help: 'Total Mistral AI API requests',
  labelNames: ['model', 'status', 'endpoint'],
  registers: [registry],
});

// Latency histogram
const requestDuration = new Histogram({
  name: 'mistral_request_duration_seconds',
  help: 'Mistral AI request duration in seconds',
  labelNames: ['model', 'endpoint'],
  buckets: [0.1, 0.25, 0.5, 1, 2.5, 5, 10],
  registers: [registry],
});

// Token counter
const tokenCounter = new Counter({
  name: 'mistral_tokens_total',
  help: 'Total tokens used',
  labelNames: ['model', 'type'], // type: input, output
  registers: [registry],
});

// Error counter
const errorCounter = new Counter({
  name: 'mistral_errors_total',
  help: 'Mistral AI errors by type',
  labelNames: ['model', 'error_type', 'status_code'],
  registers: [registry],
});

// Cost gauge (estimated)
const costCounter = new Counter({
  name: 'mistral_cost_usd_total',
  help: 'Estimated cost in USD',
  labelNames: ['model'],
  registers: [registry],
});

export { registry, requestCounter, requestDuration, tokenCounter, errorCounter, costCounter };
```

### Step 3: Create Instrumented Client Wrapper

```typescript
import Mistral from '@mistralai/mistralai';
import {
  requestCounter,
  requestDuration,
  tokenCounter,
  errorCounter,
  costCounter,
} from './metrics';

// Pricing per 1M tokens (update as needed)
const PRICING: Record<string, { input: number; output: number }> = {
  'mistral-small-latest': { input: 0.20, output: 0.60 },
  'mistral-large-latest': { input: 2.00, output: 6.00 },
  'mistral-embed': { input: 0.10, output: 0 },
};

export async function instrumentedChat(
  client: Mistral,
  model: string,
  messages: any[],
  options?: { temperature?: number; maxTokens?: number }
): Promise<any> {
  const timer = requestDuration.startTimer({ model, endpoint: 'chat.complete' });

  try {
    const response = await client.chat.complete({
      model,
      messages,
      ...options,
    });

    // Record success
    requestCounter.inc({ model, status: 'success', endpoint: 'chat.complete' });

    // Record tokens
    if (response.usage) {
      tokenCounter.inc({ model, type: 'input' }, response.usage.promptTokens || 0);
      tokenCounter.inc({ model, type: 'output' }, response.usage.completionTokens || 0);

      // Estimate cost
      const pricing = PRICING[model] || PRICING['mistral-small-latest'];
      const cost =
        ((response.usage.promptTokens || 0) / 1_000_000) * pricing.input +
        ((response.usage.completionTokens || 0) / 1_000_000) * pricing.output;
      costCounter.inc({ model }, cost);
    }

    return response;
  } catch (error: any) {
    // Record error
    requestCounter.inc({ model, status: 'error', endpoint: 'chat.complete' });
    errorCounter.inc({
      model,
      error_type: error.code || 'unknown',
      status_code: error.status?.toString() || 'unknown',
    });
    throw error;
  } finally {
    timer();
  }
}
```

### Step 4: OpenTelemetry Distributed Tracing

```typescript
import { trace, SpanStatusCode, Span } from '@opentelemetry/api';

const tracer = trace.getTracer('mistral-client');

export async function tracedChat<T>(
  operationName: string,
  operation: () => Promise<T>,
  attributes?: Record<string, string>
): Promise<T> {
  return tracer.startActiveSpan(`mistral.${operationName}`, async (span: Span) => {
    if (attributes) {
      Object.entries(attributes).forEach(([key, value]) => {
        span.setAttribute(key, value);
      });
    }

    try {
      const result = await operation();

      // Add result attributes
      if ((result as any).usage) {
        span.setAttribute('mistral.input_tokens', (result as any).usage.promptTokens);
        span.setAttribute('mistral.output_tokens', (result as any).usage.completionTokens);
      }

      span.setStatus({ code: SpanStatusCode.OK });
      return result;
    } catch (error: any) {
      span.setStatus({
        code: SpanStatusCode.ERROR,
        message: error.message,
      });
      span.recordException(error);
      throw error;
    } finally {
      span.end();
    }
  });
}

// Usage
const response = await tracedChat(
  'chat.complete',
  () => client.chat.complete({ model, messages }),
  { model, 'user.id': userId }
);
```

### Step 5: Structured Logging

```typescript
import pino from 'pino';

const logger = pino({
  name: 'mistral',
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
});

interface MistralLogContext {
  requestId: string;
  model: string;
  operation: string;
  durationMs: number;
  inputTokens?: number;
  outputTokens?: number;
  cached?: boolean;
  error?: string;
}

export function logMistralOperation(context: MistralLogContext): void {
  const { error, ...rest } = context;

  if (error) {
    logger.error({ ...rest, error }, 'Mistral operation failed');
  } else {
    logger.info(rest, 'Mistral operation completed');
  }
}

// Usage
logMistralOperation({
  requestId: 'req-123',
  model: 'mistral-small-latest',
  operation: 'chat.complete',
  durationMs: 250,
  inputTokens: 100,
  outputTokens: 50,
});
```

### Step 6: Alert Configuration

```yaml
# prometheus/mistral_alerts.yaml
groups:
  - name: mistral_alerts
    rules:
      # High error rate
      - alert: MistralHighErrorRate
        expr: |
          rate(mistral_errors_total[5m]) /
          rate(mistral_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Mistral AI error rate > 5%"
          description: "Error rate is {{ $value | humanizePercentage }}"

      # High latency
      - alert: MistralHighLatency
        expr: |
          histogram_quantile(0.95,
            rate(mistral_request_duration_seconds_bucket[5m])
          ) > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Mistral AI P95 latency > 5s"

      # Rate limit approaching
      - alert: MistralRateLimitWarning
        expr: |
          rate(mistral_errors_total{error_type="rate_limit"}[5m]) > 0
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Mistral AI rate limiting detected"

      # High cost
      - alert: MistralHighCost
        expr: |
          increase(mistral_cost_usd_total[1h]) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Mistral AI cost > $10/hour"

      # API unavailable
      - alert: MistralUnavailable
        expr: |
          rate(mistral_errors_total{status_code="503"}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Mistral AI service unavailable"
```

### Step 7: Grafana Dashboard

```json
{
  "title": "Mistral AI Monitoring",
  "panels": [
    {
      "title": "Request Rate",
      "type": "timeseries",
      "targets": [{
        "expr": "rate(mistral_requests_total[5m])",
        "legendFormat": "{{model}} - {{status}}"
      }]
    },
    {
      "title": "Latency P50/P95/P99",
      "type": "timeseries",
      "targets": [
        {
          "expr": "histogram_quantile(0.5, rate(mistral_request_duration_seconds_bucket[5m]))",
          "legendFormat": "P50"
        },
        {
          "expr": "histogram_quantile(0.95, rate(mistral_request_duration_seconds_bucket[5m]))",
          "legendFormat": "P95"
        },
        {
          "expr": "histogram_quantile(0.99, rate(mistral_request_duration_seconds_bucket[5m]))",
          "legendFormat": "P99"
        }
      ]
    },
    {
      "title": "Token Usage",
      "type": "timeseries",
      "targets": [{
        "expr": "rate(mistral_tokens_total[5m])",
        "legendFormat": "{{model}} - {{type}}"
      }]
    },
    {
      "title": "Estimated Cost ($/hour)",
      "type": "stat",
      "targets": [{
        "expr": "increase(mistral_cost_usd_total[1h])"
      }]
    }
  ]
}
```

## Output
- Prometheus metrics collection
- OpenTelemetry tracing
- Structured logging
- Alert rules configured

## Error Handling
| Issue | Cause | Solution |
|-------|-------|----------|
| Missing metrics | No instrumentation | Wrap client calls |
| Trace gaps | Missing propagation | Check context headers |
| Alert storms | Wrong thresholds | Tune alert rules |
| High cardinality | Too many labels | Reduce label values |

## Examples

### Metrics Endpoint (Express)
```typescript
import express from 'express';
import { registry } from './metrics';

const app = express();

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', registry.contentType);
  res.send(await registry.metrics());
});
```

## Resources
- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Pino Logger](https://getpino.io/)

## Next Steps
For incident response, see `mistral-incident-runbook`.
