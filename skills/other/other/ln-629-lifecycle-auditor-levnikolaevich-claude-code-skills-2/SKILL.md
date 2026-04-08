---
name: ln-629-lifecycle-auditor
description: "Checks bootstrap initialization, graceful shutdown, resource cleanup, signal handling, liveness/readiness probes. Use when auditing app lifecycle."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__trace_paths
license: MIT
model: claude-sonnet-4-6
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Lifecycle Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing application lifecycle and entry points.

## Purpose & Scope

- Audit **lifecycle** (Category 12: Medium Priority)
- Check bootstrap, shutdown, signal handling, probes
- Calculate compliance score (X/10)

## Inputs

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

Receives `contextStore` with tech stack, deployment type, codebase root, output_dir.

## Workflow

**MANDATORY READ:** Load `shared/references/two_layer_detection.md` for detection methodology.

1) Parse context + output_dir
2) Check lifecycle patterns (Layer 1: grep for SIGTERM, shutdown handlers, probes)
3) Analyze context per candidate (Layer 2):
   - Bootstrap order: read main file -- trace actual init sequence, verify dependencies satisfied before use
   - Graceful shutdown: read signal handlers -- do they actually close all resources? Or just log and exit?
   - Resource cleanup: read shutdown handler -- are ALL opened resources (DB, Redis, queues) closed?
   - Probes: check deployment config (Dockerfile, k8s manifests) -- is this containerized?
4) Collect confirmed findings
5) Calculate score
6) **Write Report:** Build full markdown report in memory per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/ln-629--global.md` in single Write call
7) **Return Summary:** Return minimal summary to coordinator

## Audit Rules

### 1. Bootstrap Initialization Order
**Detection:**
- Check main/index file for initialization sequence
- Verify dependencies loaded before usage (DB before routes)

**Severity:**
- **HIGH:** Incorrect order causes startup failures

**Recommendation:** Initialize in correct order: config -> DB -> routes -> server

**Effort:** M (refactor startup)

### 2. Graceful Shutdown
**Detection:**
- Grep for `SIGTERM`, `SIGINT` handlers
- Check `process.on('SIGTERM')` (Node.js)
- Check `signal.Notify` (Go)

**Severity:**
- **HIGH:** No shutdown handler (abrupt termination)

**Recommendation:** Add SIGTERM handler, close connections gracefully

**Effort:** M (add shutdown logic)

### 3. Resource Cleanup on Exit
**Detection:**
- Check if DB connections closed on shutdown
- Verify file handles released
- Check worker threads stopped

**Severity:**
- **MEDIUM:** Resource leaks on shutdown

**Recommendation:** Close all resources in shutdown handler

**Effort:** S-M (add cleanup calls)

### 4. Signal Handling
**Detection:**
- Check handlers for SIGTERM, SIGINT, SIGHUP
- Verify proper signal propagation to child processes

**Severity:**
- **MEDIUM:** Missing signal handlers

**Recommendation:** Handle all standard signals

**Effort:** S (add signal handlers)

### 5. Liveness/Readiness Probes
**Detection (for containerized apps):**
- Check for `/live`, `/ready` endpoints
- Verify Kubernetes probe configuration

**Severity:**
- **MEDIUM:** No probes (Kubernetes can't detect health)

**Recommendation:** Add `/live` (is running) and `/ready` (ready for traffic)

**Effort:** S (add endpoints)

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/templates/audit_worker_report_template.md`.

Write JSON summary per `shared/references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-629--global.md` with `category: "Lifecycle"` and checks: bootstrap_order, graceful_shutdown, resource_cleanup, signal_handling, probes.

Return summary per `shared/references/audit_summary_contract.md`.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/audit-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.
```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-629--global.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Reference Files

- **Audit output schema:** `shared/references/audit_output_schema.md`

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report only, lifecycle changes risk downtime
- **Deployment-aware:** Adapt probe checks to deployment type (Kubernetes = probes required, bare metal = optional)
- **Effort realism:** S = <1h, M = 1-4h, L = >4h
- **Exclusions:** Skip CLI tools and scripts (no long-running lifecycle), skip serverless functions (platform-managed lifecycle)
- **Initialization order matters:** Flag DB usage before DB init as HIGH regardless of context

## Definition of Done

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- [ ] contextStore parsed (deployment type, output_dir)
- [ ] All 5 checks completed (bootstrap order, graceful shutdown, resource cleanup, signal handling, probes)
- [ ] Findings collected with severity, location, effort, recommendation
- [ ] Score calculated per `shared/references/audit_scoring.md`
- [ ] Report written to `{output_dir}/ln-629--global.md` (atomic single Write call)
- [ ] Summary written per contract

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
