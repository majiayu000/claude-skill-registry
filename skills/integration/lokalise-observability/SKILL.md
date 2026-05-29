---
name: lokalise-observability
description: |
  Set up comprehensive observability for Lokalise integrations with metrics, traces, and alerts.
  Use when implementing monitoring for Lokalise operations, setting up dashboards,
  or configuring alerting for Lokalise integration health.
  Trigger with phrases like "lokalise monitoring", "lokalise metrics",
  "lokalise observability", "monitor lokalise", "lokalise alerts", "lokalise tracing".
allowed-tools: Read, Write, Edit
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Lokalise Observability

## Overview
Set up comprehensive observability for Lokalise integrations with metrics, logging, and alerting.

## Prerequisites
- Prometheus or compatible metrics backend
- Logging infrastructure (ELK, Datadog, etc.)
- Grafana or similar dashboarding tool
- AlertManager configured

## Key Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `lokalise_requests_total` | Counter | Total API requests |
| `lokalise_request_duration_seconds` | Histogram | Request latency |
| `lokalise_errors_total` | Counter | Error count by type |
| `lokalise_rate_limit_remaining` | Gauge | Rate limit headroom |
| `lokalise_keys_total` | Gauge | Total translation keys |
| `lokalise_translation_coverage` | Gauge | Translation progress |
| `lokalise_webhook_events_total` | Counter | Webhook events received |

## Instructions

### Step 1: Prometheus Metrics Setup
```typescript
import { Registry, Counter, Histogram, Gauge } from "prom-client";

const registry = new Registry();

// Request metrics
const requestCounter = new Counter({
  name: "lokalise_requests_total",
  help: "Total Lokalise API requests",
  labelNames: ["method", "endpoint", "status"],
  registers: [registry],
});

const requestDuration = new Histogram({
  name: "lokalise_request_duration_seconds",
  help: "Lokalise request duration",
  labelNames: ["method", "endpoint"],
  buckets: [0.1, 0.25, 0.5, 1, 2.5, 5, 10],
  registers: [registry],
});

const errorCounter = new Counter({
  name: "lokalise_errors_total",
  help: "Lokalise errors by type",
  labelNames: ["error_type", "endpoint"],
  registers: [registry],
});

// Rate limit tracking
const rateLimitRemaining = new Gauge({
  name: "lokalise_rate_limit_remaining",
  help: "Remaining rate limit quota",
  registers: [registry],
});

// Translation metrics
const translationCoverage = new Gauge({
  name: "lokalise_translation_coverage",
  help: "Translation coverage percentage",
  labelNames: ["project", "language"],
  registers: [registry],
});
```

### Step 2: Instrumented Client Wrapper
```typescript
import { LokaliseApi } from "@lokalise/node-api";

export async function instrumentedRequest<T>(
  method: string,
  endpoint: string,
  operation: () => Promise<T>
): Promise<T> {
  const timer = requestDuration.startTimer({ method, endpoint });

  try {
    const result = await operation();
    requestCounter.inc({ method, endpoint, status: "success" });
    return result;
  } catch (error: any) {
    requestCounter.inc({ method, endpoint, status: "error" });
    errorCounter.inc({
      error_type: error.code?.toString() || "unknown",
      endpoint,
    });
    throw error;
  } finally {
    timer();
  }
}

// Usage
export class InstrumentedLokaliseClient {
  private client: LokaliseApi;

  constructor(apiKey: string) {
    this.client = new LokaliseApi({ apiKey });
  }

  async listProjects() {
    return instrumentedRequest("GET", "/projects", () =>
      this.client.projects().list()
    );
  }

  async listKeys(projectId: string) {
    return instrumentedRequest("GET", "/keys", () =>
      this.client.keys().list({ project_id: projectId })
    );
  }

  async downloadFiles(projectId: string, options: any) {
    return instrumentedRequest("POST", "/files/download", () =>
      this.client.files().download(projectId, options)
    );
  }
}
```

### Step 3: Structured Logging
```typescript
import pino from "pino";

const logger = pino({
  name: "lokalise",
  level: process.env.LOG_LEVEL || "info",
  formatters: {
    level: (label) => ({ level: label }),
  },
});

interface LokaliseLogContext {
  operation: string;
  projectId?: string;
  keyId?: number;
  locale?: string;
  duration?: number;
  error?: string;
}

export function logLokaliseOperation(
  level: "info" | "warn" | "error",
  message: string,
  context: LokaliseLogContext
) {
  logger[level]({
    service: "lokalise",
    ...context,
    timestamp: new Date().toISOString(),
  }, message);
}

// Usage
logLokaliseOperation("info", "Translation sync completed", {
  operation: "sync",
  projectId: "123456.abc",
  duration: 1500,
});

logLokaliseOperation("error", "API request failed", {
  operation: "listKeys",
  projectId: "123456.abc",
  error: "Rate limit exceeded",
});
```

### Step 4: Health Check Endpoint
```typescript
interface LokaliseHealth {
  status: "healthy" | "degraded" | "unhealthy";
  latencyMs: number;
  rateLimitRemaining?: number;
  lastSync?: string;
  error?: string;
}

export async function checkLokaliseHealth(): Promise<LokaliseHealth> {
  const start = Date.now();

  try {
    const client = new LokaliseApi({
      apiKey: process.env.LOKALISE_API_TOKEN!,
    });

    // Quick connectivity test
    await client.projects().list({ limit: 1 });

    const latencyMs = Date.now() - start;

    return {
      status: latencyMs < 2000 ? "healthy" : "degraded",
      latencyMs,
      lastSync: process.env.LAST_TRANSLATION_SYNC,
    };
  } catch (error: any) {
    return {
      status: "unhealthy",
      latencyMs: Date.now() - start,
      error: error.message,
    };
  }
}

// Express endpoint
app.get("/health/lokalise", async (req, res) => {
  const health = await checkLokaliseHealth();
  const statusCode = health.status === "healthy" ? 200 : 503;
  res.status(statusCode).json(health);
});
```

### Step 5: Alert Rules
```yaml
# prometheus/lokalise_alerts.yml
groups:
  - name: lokalise_alerts
    rules:
      - alert: LokaliseHighErrorRate
        expr: |
          rate(lokalise_errors_total[5m]) /
          rate(lokalise_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Lokalise error rate > 5%"
          description: "Error rate is {{ $value | printf \"%.2f\" }}%"

      - alert: LokaliseHighLatency
        expr: |
          histogram_quantile(0.95,
            rate(lokalise_request_duration_seconds_bucket[5m])
          ) > 3
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Lokalise P95 latency > 3s"

      - alert: LokaliseRateLimitLow
        expr: lokalise_rate_limit_remaining < 2
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "Lokalise rate limit nearly exhausted"

      - alert: LokaliseDown
        expr: up{job="lokalise"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Lokalise integration is down"
```

## Output
- Metrics collection enabled
- Structured logging implemented
- Health check endpoint
- Alert rules deployed

## Error Handling
| Issue | Cause | Solution |
|-------|-------|----------|
| Missing metrics | No instrumentation | Wrap client calls |
| Log flooding | Verbose level | Adjust log level |
| Alert storms | Wrong thresholds | Tune alert rules |
| Health false positive | Timeout too short | Increase timeout |

## Examples

### Grafana Dashboard Queries
```json
{
  "panels": [
    {
      "title": "Lokalise Request Rate",
      "targets": [{
        "expr": "rate(lokalise_requests_total[5m])"
      }]
    },
    {
      "title": "Lokalise Latency P50/P95/P99",
      "targets": [
        { "expr": "histogram_quantile(0.50, rate(lokalise_request_duration_seconds_bucket[5m]))" },
        { "expr": "histogram_quantile(0.95, rate(lokalise_request_duration_seconds_bucket[5m]))" },
        { "expr": "histogram_quantile(0.99, rate(lokalise_request_duration_seconds_bucket[5m]))" }
      ]
    },
    {
      "title": "Translation Coverage by Language",
      "targets": [{
        "expr": "lokalise_translation_coverage"
      }]
    }
  ]
}
```

### Collect Translation Coverage
```typescript
async function updateTranslationCoverageMetrics(projectId: string) {
  const client = new LokaliseApi({
    apiKey: process.env.LOKALISE_API_TOKEN!,
  });

  const languages = await client.languages().list({ project_id: projectId });

  for (const lang of languages.items) {
    translationCoverage.set(
      { project: projectId, language: lang.lang_iso },
      lang.statistics?.progress ?? 0
    );
  }
}

// Run periodically
setInterval(() => {
  updateTranslationCoverageMetrics(process.env.LOKALISE_PROJECT_ID!);
}, 300000);  // Every 5 minutes
```

### Metrics Endpoint
```typescript
app.get("/metrics", async (req, res) => {
  res.set("Content-Type", registry.contentType);
  res.send(await registry.metrics());
});
```

## Resources
- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)
- [Grafana Dashboards](https://grafana.com/docs/grafana/latest/dashboards/)
- [pino Logger](https://getpino.io/)

## Next Steps
For incident response, see `lokalise-incident-runbook`.
