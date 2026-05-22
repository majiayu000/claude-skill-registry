---
name: observability-setup
description: "Set up logging, metrics, health checks, and alerting. Creates observability infrastructure for production systems. Use when user says 'monitoring', 'observability', 'metrics', 'logging', 'alerts', or 'health check'."
allowed-tools: Bash, Read, Write, Edit, Glob
---

# Observability Setup

You are an expert at setting up observability infrastructure for production systems.

## When To Use

- User wants logging setup
- User asks about metrics or monitoring
- User needs health check endpoints
- User wants alerting configuration
- Project going to production needs observability

## Philosophy

**Observe before you optimize.** You can't improve what you can't measure.

Keep it simple:
- Start with structured logging (free)
- Add health endpoints (free)
- Prometheus metrics when needed
- Alerts only for actionable issues

## Structured Logging

### Python (structlog)

```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)

log = structlog.get_logger()

# Usage
log.info("user_action", user_id=123, action="login")
# Output: {"timestamp": "2024-...", "event": "user_action", "user_id": 123, "action": "login"}
```

### Python (stdlib)

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "time": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module
        })

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logging.root.addHandler(handler)
logging.root.setLevel(logging.INFO)
```

### Log Levels

| Level | When | Example |
|-------|------|---------|
| DEBUG | Development only | Variable values, flow tracing |
| INFO | Normal operations | User actions, requests processed |
| WARNING | Recoverable issues | Retry succeeded, degraded mode |
| ERROR | Failures | Request failed, exception caught |
| CRITICAL | System down | Database unreachable, out of memory |

### Anti-Patterns

- Logging sensitive data (passwords, tokens, PII)
- Logging in hot loops (performance killer)
- Unstructured log messages ("Something happened")
- Ignoring log rotation (disk fills up)

## Health Check Endpoints

### Standard Endpoints

| Endpoint | Purpose | Response |
|----------|---------|----------|
| `/health` | Basic liveness | `{"status": "ok"}` |
| `/ready` | Ready to serve traffic | `{"status": "ready", "checks": {...}}` |
| `/live` | Process is alive | `{"status": "alive"}` |

### FastAPI Example

```python
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    checks = {
        "database": check_db(),
        "cache": check_cache()
    }
    all_ok = all(checks.values())
    return Response(
        content=json.dumps({"status": "ready" if all_ok else "degraded", "checks": checks}),
        status_code=200 if all_ok else 503
    )

def check_db():
    try:
        db.execute("SELECT 1")
        return True
    except:
        return False

def check_cache():
    try:
        cache.ping()
        return True
    except:
        return False
```

### Flask Example

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify(status="ok")

@app.route('/ready')
def ready():
    return jsonify(status="ready", checks={"db": True})
```

## Prometheus Metrics

### Python (prometheus_client)

```python
from prometheus_client import Counter, Histogram, start_http_server

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Request latency', ['endpoint'])

# Usage
REQUEST_COUNT.labels(method='GET', endpoint='/api/users', status='200').inc()
with REQUEST_LATENCY.labels(endpoint='/api/users').time():
    process_request()

# Expose metrics on :8000/metrics
start_http_server(8000)
```

### Key Metrics to Track

| Metric | Type | Purpose |
|--------|------|---------|
| `http_requests_total` | Counter | Request volume |
| `http_request_duration_seconds` | Histogram | Latency (p50, p95, p99) |
| `http_requests_in_progress` | Gauge | Concurrent requests |
| `errors_total` | Counter | Error rate |
| `db_query_duration_seconds` | Histogram | Database performance |

### Metric Naming

- Use snake_case
- Include unit in name: `_seconds`, `_bytes`, `_total`
- Be specific: `http_requests_total` not `requests`

## Alerting

### Alert Design Principles

1. **Actionable**: Every alert should have a clear action
2. **Urgent**: Alert only on issues needing immediate attention
3. **Rare**: Too many alerts = alert fatigue = ignored alerts

### Good Alerts

| Alert | Trigger | Action |
|-------|---------|--------|
| `HighErrorRate` | >5% errors for 5min | Check logs, rollback if needed |
| `HighLatency` | p95 >2s for 5min | Scale up or investigate |
| `DiskFull` | >90% disk usage | Clean up or expand |
| `ServiceDown` | Health check fails 3x | Restart or investigate |

### Bad Alerts (Avoid)

- CPU >80% (normal during load)
- Any single error (too noisy)
- Low disk space <50% (not urgent)
- Informational events (use dashboards)

### Simple Alert Script

```bash
#!/bin/bash
# Simple health check alerter (cron every 5 min)

ENDPOINT="http://localhost:8000/health"
SLACK_WEBHOOK="https://hooks.slack.com/..."

if ! curl -sf "$ENDPOINT" > /dev/null; then
    curl -X POST "$SLACK_WEBHOOK" \
        -H 'Content-Type: application/json' \
        -d '{"text": "ALERT: Health check failed for service"}'
fi
```

## OpenTelemetry (Optional)

For complex systems needing distributed tracing:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(OTLPSpanExporter())
)

# Usage
with tracer.start_as_current_span("process_order"):
    # Your code here
    pass
```

**Skip this unless**: Microservices, complex request flows, debugging distributed systems.

## Quick Start Checklist

### Minimum (Every Project)

- [ ] Structured JSON logging
- [ ] `/health` endpoint
- [ ] Log rotation configured

### Production Ready

- [ ] `/ready` endpoint with dependency checks
- [ ] Request count and latency metrics
- [ ] Error rate monitoring
- [ ] Basic alerting (health check failures)

### Advanced (When Needed)

- [ ] Distributed tracing (OpenTelemetry)
- [ ] Custom business metrics
- [ ] Dashboards (Grafana)
- [ ] On-call rotation

## Outputs

- Logging configuration added
- Health check endpoints created
- Metrics endpoint (if requested)
- Alert configuration (if requested)
- Updated README with observability section

## Anti-Patterns

- Metrics without alerts (why collect?)
- Alerts without runbooks (what do I do?)
- Logging PII or secrets
- Alert on every error (noise)
- Complex tracing for simple apps (overkill)

## Keywords

monitoring, observability, metrics, logging, alerts, health check, prometheus, grafana, structured logging, tracing, opentelemetry
