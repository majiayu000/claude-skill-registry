---
name: ln-627-observability-auditor
description: Observability audit worker (L3). Checks structured logging, health check endpoints, metrics collection, request tracing, log levels. Returns findings with severity, location, effort, recommendations.
allowed-tools: Read, Grep, Glob, Bash
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Observability Auditor (L3 Worker)

Specialized worker auditing logging, monitoring, and observability.

## Purpose & Scope

- **Worker in ln-620 coordinator pipeline**
- Audit **observability** (Category 10: Medium Priority)
- Check logging, health checks, metrics, tracing
- Calculate compliance score (X/10)

## Inputs (from Coordinator)

Receives `contextStore` with tech stack, framework, codebase root, output_dir.

## Workflow

1) Parse context + output_dir
2) Check observability patterns
3) Collect findings
4) Calculate score
5) **Write Report:** Build full markdown report in memory per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/627-observability.md` in single Write call
6) **Return Summary:** Return minimal summary to coordinator

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

**MANDATORY READ:** Load `shared/templates/audit_worker_report_template.md` for file format.

Write report to `{output_dir}/627-observability.md` with `category: "Observability"` and checks: structured_logging, health_endpoints, metrics_collection, request_tracing, log_levels.

Return summary to coordinator:
```
Report written: docs/project/.audit/ln-620/{YYYY-MM-DD}/627-observability.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Reference Files

- **Worker report template:** `shared/templates/audit_worker_report_template.md`
- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`

## Critical Rules

- **Do not auto-fix:** Report only, never inject logging or endpoints
- **Framework-aware detection:** Adapt patterns to project's tech stack (winston/pino for Node, logrus/zap for Go, etc.)
- **Effort realism:** S = <1h, M = 1-4h, L = >4h
- **Exclusions:** Skip test files for console.log detection, skip dev-only scripts
- **Context-sensitive severity:** console.log in production code = MEDIUM, in dev utilities = LOW

## Definition of Done

- contextStore parsed (tech stack, framework, output_dir)
- All 5 checks completed (structured logging, health endpoints, metrics, request tracing, log levels)
- Findings collected with severity, location, effort, recommendation
- Score calculated per `shared/references/audit_scoring.md`
- Report written to `{output_dir}/627-observability.md` (atomic single Write call)
- Summary returned to coordinator

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
