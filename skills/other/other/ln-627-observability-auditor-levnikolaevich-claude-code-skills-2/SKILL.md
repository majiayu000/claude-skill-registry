---
name: ln-627-observability-auditor
description: "Checks structured logging, health checks, metrics collection, request tracing, log levels. Use when auditing observability."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__find_references, mcp__hex-graph__trace_paths
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Observability Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing logging, monitoring, and observability.

## Purpose & Scope

- Audit **observability** (Category 10: Medium Priority)
- Check logging, health checks, metrics, tracing
- Calculate compliance score (X/10)

## Inputs

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

Receives `contextStore` with tech stack, framework, codebase root, output_dir.

## Workflow

**MANDATORY READ:** Load `shared/references/two_layer_detection.md` for detection methodology.

1) Parse context + output_dir
2) **Determine project type (Layer 2 pre-check):** Is this a web service (all checks apply), CLI tool (health/probes not applicable), or library (most checks optional)? Adjust applicable checks accordingly.
3) Check observability patterns (Layer 1: grep)
4) Analyze context per candidate (Layer 2):
   - Structured logging: is this a library (no logging OK) or a service (logging required)?
   - Health endpoints: web service -> required. CLI/library -> skip
   - Request tracing: monolith -> less needed. Microservice -> critical
5) Collect confirmed findings
6) Calculate score
7) **Write Report:** Build full markdown report in memory per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/ln-627--global.md` in single Write call
8) **Return Summary:** Return minimal summary to coordinator

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

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/templates/audit_worker_report_template.md`.

Write JSON summary per `shared/references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-627--global.md` with `category: "Observability"` and checks: structured_logging, health_endpoints, metrics_collection, request_tracing, log_levels.

Return summary per `shared/references/audit_summary_contract.md`.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/audit-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.
```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-627--global.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Reference Files

- **Audit output schema:** `shared/references/audit_output_schema.md`

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report only, never inject logging or endpoints
- **Framework-aware detection:** Adapt patterns to project's tech stack (winston/pino for Node, logrus/zap for Go, etc.)
- **Effort realism:** S = <1h, M = 1-4h, L = >4h
- **Exclusions:** Skip test files for console.log detection, skip dev-only scripts
- **Context-sensitive severity:** console.log in production code = MEDIUM, in dev utilities = LOW

## Definition of Done

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- [ ] contextStore parsed (tech stack, framework, output_dir)
- [ ] All 5 checks completed (structured logging, health endpoints, metrics, request tracing, log levels)
- [ ] Findings collected with severity, location, effort, recommendation
- [ ] Score calculated per `shared/references/audit_scoring.md`
- [ ] Report written to `{output_dir}/ln-627--global.md` (atomic single Write call)
- [ ] Summary written per contract

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
