---
name: ln-627-diagnosability-auditor
description: "Checks diagnosability through structured logs, metrics, traces, correlation IDs, and useful log levels. Use when auditing incident visibility."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__find_references, mcp__hex-graph__trace_paths, mcp__hex-line__read_file, mcp__hex-line__grep_search, mcp__hex-line__outline
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

# Diagnosability Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing whether operators can diagnose incidents.

## Purpose & Scope

- Audit **diagnosability** (Category 10: Medium Priority)
- Check structured logs, metrics, tracing, correlation IDs, and log levels
- Emit `ADD_DIAGNOSTIC_SIGNAL`, `STRUCTURE_LOGS`, or `PROPAGATE_CORRELATION`
- Calculate compliance score (X/10)

## Inputs

**MANDATORY READ:** Load `references/audit_worker_core_contract.md`.
Tool policy: follow host AGENTS.md MCP preferences; load `references/mcp_tool_preferences.md` and `references/mcp_integration_patterns.md` only when host policy is absent or MCP behavior is unclear.

Receives `contextStore` with tech stack, framework, codebase root, output_dir.

Use `hex-graph` first when traces, call paths, or cross-file references materially improve the audit. Use `hex-line` first for local code reads when available. If MCP is unavailable, unsupported, or not indexed, continue with built-in `Read/Grep/Glob/Bash` and state the fallback in the report.

## Workflow

Detection policy: use two-layer detection (candidate scan, then context verification); load `references/two_layer_detection.md` only when the verification method is ambiguous.

1) Parse context + output_dir
2) **Determine project type (Layer 2 pre-check):** Is this a web service (all checks apply), CLI tool (health/probes not applicable), or library (most checks optional)? Adjust applicable checks accordingly.
3) Check observability patterns (Layer 1: grep)
4) Analyze context per candidate (Layer 2):
   - Structured logging: is this a library (no logging OK) or a service (logging required)?
   - Request tracing: monolith -> less needed. Microservice -> critical
5) Collect confirmed findings
6) Calculate score
7) **Write Report:** Build full markdown report in memory per `references/templates/audit_worker_report_template.md`, write to `{output_dir}/ln-627--global.md` in single Write call
8) **Return Summary:** Return minimal summary

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

### 2. Correlation IDs
**Detection:**
- Check for request ID/correlation ID middleware
- Verify IDs appear in logs and are propagated to outbound calls

**Severity:**
- **MEDIUM:** No correlation IDs in request-handling services

**Recommendation:** Add request ID middleware and include correlation ID in structured logs

**Effort:** M

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

**MANDATORY READ:** Load `references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `references/templates/audit_worker_report_template.md`.

Write JSON summary per `references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-627--global.md` with `category: "Diagnosability"` and checks: structured_logging, correlation_ids, metrics_collection, request_tracing, log_levels.

Return summary per `references/audit_summary_contract.md`.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/evaluation-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.
```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-627--global.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Reference Files

- **Audit output schema:** `references/audit_output_schema.md`

## Critical Rules

Apply the already-loaded `references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report only, never inject logging or endpoints
- **Framework-aware detection:** Adapt patterns to project's tech stack (winston/pino for Node, logrus/zap for Go, etc.)
- **Effort realism:** S = <1h, M = 1-4h, L = >4h
- **Exclusions:** Skip test files for console.log detection, skip dev-only scripts
- **Context-sensitive severity:** console.log in production code = MEDIUM, in dev utilities = LOW
- **Unique angle:** Audit diagnostic signal only. Liveness/readiness probes and shutdown behavior belong to lifecycle/config audit.
- **Action required:** Every finding uses `ADD_DIAGNOSTIC_SIGNAL`, `STRUCTURE_LOGS`, or `PROPAGATE_CORRELATION`.

## Definition of Done

Apply the already-loaded `references/audit_worker_core_contract.md`.

- [ ] contextStore parsed (tech stack, framework, output_dir)
- [ ] All 5 checks completed (structured logging, correlation IDs, metrics, request tracing, log levels)
- [ ] Findings collected with severity, location, effort, action, recommendation
- [ ] Score calculated per `references/audit_scoring.md`
- [ ] Report written to `{output_dir}/ln-627--global.md` (atomic single Write call)
- [ ] Summary written per contract

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
