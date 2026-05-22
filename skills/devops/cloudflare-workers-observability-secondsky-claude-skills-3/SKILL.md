---
name: workers-observability
description: Cloudflare Workers observability with logging, Analytics Engine, Tail Workers, metrics, and alerting. Use for monitoring, debugging, tracing, or encountering log parsing, metric aggregation, alert configuration errors.
---

# Cloudflare Workers Observability

Production-grade observability for Cloudflare Workers: logging, metrics, tracing, and alerting.

## Quick Start

```typescript
// Structured logging with context
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const requestId = crypto.randomUUID();
    const logger = createLogger(requestId, env);

    try {
      logger.info('Request received', { method: request.method, url: request.url });

      const result = await handleRequest(request, env);

      logger.info('Request completed', { status: result.status });
      return result;
    } catch (error) {
      logger.error('Request failed', { error: error.message, stack: error.stack });
      throw error;
    }
  }
};

// Simple logger factory
function createLogger(requestId: string, env: Env) {
  return {
    info: (msg: string, data?: object) => console.log(JSON.stringify({ level: 'info', requestId, msg, ...data, timestamp: Date.now() })),
    error: (msg: string, data?: object) => console.error(JSON.stringify({ level: 'error', requestId, msg, ...data, timestamp: Date.now() })),
    warn: (msg: string, data?: object) => console.warn(JSON.stringify({ level: 'warn', requestId, msg, ...data, timestamp: Date.now() })),
  };
}
```

## Critical Rules

1. **Always use structured JSON logging** - Plain text logs are hard to parse and aggregate
2. **Include request context** - Request ID, method, path in every log entry
3. **Never log sensitive data** - Redact tokens, passwords, PII from logs
4. **Use appropriate log levels** - ERROR for failures, WARN for recoverable issues, INFO for operations
5. **Sample high-volume logs** - Use 1-10% sampling for request logs in production

## Observability Components

| Component | Purpose | When to Use |
|-----------|---------|-------------|
| `console.log` | Basic logging | Development, debugging |
| **Tail Workers** | Real-time log streaming | Production log aggregation |
| **Analytics Engine** | Custom metrics/analytics | Business metrics, performance tracking |
| **Logpush** | Log export to external services | Long-term storage, compliance |
| **Workers Trace Events** | Distributed tracing | Request flow debugging |

## Top 8 Errors Prevented

| Error | Symptom | Prevention |
|-------|---------|------------|
| Logs not appearing | No output in dashboard | Enable "Standard" logging in wrangler.jsonc |
| Log truncation | Messages cut off at 128KB | Chunk large payloads, use sampling |
| Tail Worker not receiving | No events processed | Check binding name matches wrangler.jsonc |
| Analytics Engine write fails | Data not recorded | Verify AE binding, check blobs format |
| PII in logs | Security/compliance violation | Implement redaction middleware |
| Missing request context | Can't correlate logs | Add requestId to all log entries |
| Log volume explosion | High costs, noise | Implement sampling for high-frequency events |
| Alerting gaps | Incidents not detected | Configure monitors for error rate thresholds |

## Logging Configuration

**wrangler.jsonc**:
```jsonc
{
  "name": "my-worker",
  "observability": {
    "enabled": true,
    "head_sampling_rate": 1 // 0-1, 1 = 100% of requests
  },
  "tail_consumers": [
    {
      "service": "log-aggregator", // Tail Worker name
      "environment": "production"
    }
  ],
  "analytics_engine_datasets": [
    {
      "binding": "ANALYTICS",
      "dataset": "my_worker_metrics"
    }
  ]
}
```

## Structured Logging Pattern

```typescript
interface LogEntry {
  level: 'debug' | 'info' | 'warn' | 'error';
  message: string;
  requestId: string;
  timestamp: number;
  // Contextual data
  method?: string;
  path?: string;
  status?: number;
  duration?: number;
  // Error details
  error?: {
    name: string;
    message: string;
    stack?: string;
  };
  // Custom fields
  [key: string]: unknown;
}

class Logger {
  constructor(private requestId: string, private baseContext: object = {}) {}

  private log(level: LogEntry['level'], message: string, data?: object) {
    const entry: LogEntry = {
      level,
      message,
      requestId: this.requestId,
      timestamp: Date.now(),
      ...this.baseContext,
      ...data,
    };

    // Redact sensitive fields
    const sanitized = this.redact(entry);

    const output = JSON.stringify(sanitized);
    level === 'error' ? console.error(output) : console.log(output);
  }

  private redact(entry: LogEntry): LogEntry {
    const sensitiveKeys = ['password', 'token', 'secret', 'authorization', 'cookie'];
    const redacted = { ...entry };

    for (const key of Object.keys(redacted)) {
      if (sensitiveKeys.some(s => key.toLowerCase().includes(s))) {
        redacted[key] = '[REDACTED]';
      }
    }
    return redacted;
  }

  info(message: string, data?: object) { this.log('info', message, data); }
  warn(message: string, data?: object) { this.log('warn', message, data); }
  error(message: string, data?: object) { this.log('error', message, data); }
  debug(message: string, data?: object) { this.log('debug', message, data); }
}
```

## Analytics Engine Usage

```typescript
interface Env {
  ANALYTICS: AnalyticsEngineDataset;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const start = Date.now();
    const url = new URL(request.url);

    try {
      const response = await handleRequest(request, env);

      // Write success metric
      env.ANALYTICS.writeDataPoint({
        blobs: [request.method, url.pathname, String(response.status)],
        doubles: [Date.now() - start], // Response time in ms
        indexes: [url.pathname.split('/')[1] || 'root'], // Index for fast queries
      });

      return response;
    } catch (error) {
      // Write error metric
      env.ANALYTICS.writeDataPoint({
        blobs: [request.method, url.pathname, 'error', error.message],
        doubles: [Date.now() - start],
        indexes: ['error'],
      });
      throw error;
    }
  }
};
```

## Tail Worker Pattern

```typescript
// tail-worker.ts - Receives logs from other workers
interface TailEvent {
  scriptName: string;
  event: {
    request?: { method: string; url: string };
    response?: { status: number };
  };
  logs: Array<{
    level: string;
    message: unknown[];
    timestamp: number;
  }>;
  exceptions: Array<{
    name: string;
    message: string;
    timestamp: number;
  }>;
  outcome: 'ok' | 'exception' | 'exceededCpu' | 'exceededMemory' | 'canceled';
  eventTimestamp: number;
}

export default {
  async tail(events: TailEvent[], env: Env): Promise<void> {
    for (const event of events) {
      // Filter and forward logs
      const errorLogs = event.logs.filter(l => l.level === 'error');
      const exceptions = event.exceptions;

      if (errorLogs.length > 0 || exceptions.length > 0) {
        // Send to external logging service
        await fetch(env.LOGGING_ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            scriptName: event.scriptName,
            timestamp: event.eventTimestamp,
            errors: errorLogs,
            exceptions,
            outcome: event.outcome,
          }),
        });
      }
    }
  }
};
```

## When to Load References

Load specific references based on the task:

- **Setting up logging?** → Load `references/logging.md` for structured logging patterns, log levels, redaction
- **Building custom metrics?** → Load `references/analytics-engine.md` for Analytics Engine SQL queries, data modeling
- **Implementing log aggregation?** → Load `references/tail-workers.md` for Tail Worker patterns, external service integration
- **Creating dashboards/tracking?** → Load `references/custom-metrics.md` for business metrics, performance tracking
- **Setting up alerts?** → Load `references/alerting.md` for error rate monitoring, PagerDuty/Slack integration

## Templates

| Template | Purpose | Use When |
|----------|---------|----------|
| `templates/logging-setup.ts` | Production logging class | Setting up new worker with logging |
| `templates/analytics-worker.ts` | Analytics Engine integration | Adding custom metrics |
| `templates/tail-worker.ts` | Complete Tail Worker | Building log aggregation pipeline |

## Scripts

| Script | Purpose | Command |
|--------|---------|---------|
| `scripts/setup-logging.sh` | Configure logging settings | `./setup-logging.sh` |
| `scripts/analyze-logs.sh` | Query and analyze logs | `./analyze-logs.sh --errors --last 1h` |

## Resources

- Workers Observability: https://developers.cloudflare.com/workers/observability/
- Analytics Engine: https://developers.cloudflare.com/analytics/analytics-engine/
- Tail Workers: https://developers.cloudflare.com/workers/observability/tail-workers/
- Logpush: https://developers.cloudflare.com/logs/get-started/
