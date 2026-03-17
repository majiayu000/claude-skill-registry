---
name: ln-627-observability-auditor
description: Observability audit worker (L3). Checks structured logging, health check endpoints, metrics collection, request tracing, log levels. Returns findings with severity, location, effort, recommendations.
allowed-tools: Read, Grep, Glob, Bash
---

# Observability Auditor (L3 Worker)

Specialized worker auditing logging, monitoring, and observability.

## Purpose & Scope

- **Worker in ln-620 coordinator pipeline**
- Audit **observability** (Category 10: Medium Priority)
- Check logging, health checks, metrics, tracing
- Calculate compliance score (X/10)

## Inputs (from Coordinator)

Receives `contextStore` with tech stack, framework, codebase root.

## Workflow

1) Parse context
2) Check observability patterns
3) Collect findings
4) Calculate score
5) Return JSON

## Audit Rules

### 1. Structured Logging
**Detection:**
- Grep for `console.log` (unstructured)
- Check for proper logger: winston, pino, logrus, zap

**Severity:**
- **MEDIUM:** Production code using console.log
- **LOW:** Dev code using console.log

**Recommendation:** Use structured logger (winston, pino)

**Effort:** M (add logger, replace calls)

### 2. Health Check Endpoints
**Detection:**
- Grep for `/health`, `/ready`, `/live` routes
- Check API route definitions

**Severity:**
- **HIGH:** No health check endpoint (monitoring blind spot)

**Recommendation:** Add `/health` endpoint

**Effort:** S (add simple route)

### 3. Metrics Collection
**Detection:**
- Check for Prometheus client, StatsD, CloudWatch
- Grep for metric recording: `histogram`, `counter`

**Severity:**
- **MEDIUM:** No metrics instrumentation

**Recommendation:** Add Prometheus metrics

**Effort:** M (instrument code)

### 4. Request Tracing
**Detection:**
- Check for correlation IDs in logs
- Verify trace propagation (OpenTelemetry, Zipkin)

**Severity:**
- **MEDIUM:** No correlation IDs (hard to debug distributed systems)

**Recommendation:** Add request ID middleware

**Effort:** M (add middleware, propagate IDs)

### 5. Log Levels
**Detection:**
- Check if logger supports levels (info, warn, error, debug)
- Verify proper level usage

**Severity:**
- **LOW:** Only error logging (insufficient visibility)

**Recommendation:** Add info/debug logs

**Effort:** S (add log statements)

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

## Output Format

```json
{
  "category": "Observability",
  "score": 6,
  "total_issues": 5,
  "critical": 0,
  "high": 1,
  "medium": 3,
  "low": 1,
  "checks": [
    {"id": "structured_logging", "name": "Structured Logging", "status": "warning", "details": "3 console.log calls in production code"},
    {"id": "health_endpoints", "name": "Health Endpoints", "status": "failed", "details": "No /health endpoint found"},
    {"id": "metrics_collection", "name": "Metrics Collection", "status": "passed", "details": "Prometheus client configured"},
    {"id": "request_tracing", "name": "Request Tracing", "status": "warning", "details": "Correlation IDs missing in 2 services"}
  ],
  "findings": [
    {
      "severity": "HIGH",
      "location": "src/api/server.ts",
      "issue": "No /health endpoint for monitoring",
      "principle": "Observability / Health Checks",
      "recommendation": "Add GET /health route returning { status: 'ok', uptime, ... }",
      "effort": "S"
    }
  ]
}
```

## Reference Files

- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
