---
name: ln-629-lifecycle-auditor
description: Application lifecycle audit worker (L3). Checks bootstrap initialization order, graceful shutdown, resource cleanup, signal handling, liveness/readiness probes. Returns findings with severity, location, effort, recommendations.
allowed-tools: Read, Grep, Glob, Bash
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Lifecycle Auditor (L3 Worker)

Specialized worker auditing application lifecycle and entry points.

## Purpose & Scope

- **Worker in ln-620 coordinator pipeline**
- Audit **lifecycle** (Category 12: Medium Priority)
- Check bootstrap, shutdown, signal handling, probes
- Calculate compliance score (X/10)

## Inputs (from Coordinator)

Receives `contextStore` with tech stack, deployment type, codebase root, output_dir.

## Workflow

1) Parse context + output_dir
2) Check lifecycle patterns
3) Collect findings
4) Calculate score
5) **Write Report:** Build full markdown report in memory per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/629-lifecycle.md` in single Write call
6) **Return Summary:** Return minimal summary to coordinator

## Audit Rules

### 1. Bootstrap Initialization Order
**Detection:**
- Check main/index file for initialization sequence
- Verify dependencies loaded before usage (DB before routes)

**Severity:**
- **HIGH:** Incorrect order causes startup failures

**Recommendation:** Initialize in correct order: config → DB → routes → server

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

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

## Output Format

**MANDATORY READ:** Load `shared/templates/audit_worker_report_template.md` for file format.

Write report to `{output_dir}/629-lifecycle.md` with `category: "Lifecycle"` and checks: bootstrap_order, graceful_shutdown, resource_cleanup, signal_handling, probes.

Return summary to coordinator:
```
Report written: docs/project/.audit/629-lifecycle.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Reference Files

- **Worker report template:** `shared/templates/audit_worker_report_template.md`
- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`

## Critical Rules

- **Do not auto-fix:** Report only, lifecycle changes risk downtime
- **Deployment-aware:** Adapt probe checks to deployment type (Kubernetes = probes required, bare metal = optional)
- **Effort realism:** S = <1h, M = 1-4h, L = >4h
- **Exclusions:** Skip CLI tools and scripts (no long-running lifecycle), skip serverless functions (platform-managed lifecycle)
- **Initialization order matters:** Flag DB usage before DB init as HIGH regardless of context

## Definition of Done

- contextStore parsed (deployment type, output_dir)
- All 5 checks completed (bootstrap order, graceful shutdown, resource cleanup, signal handling, probes)
- Findings collected with severity, location, effort, recommendation
- Score calculated per `shared/references/audit_scoring.md`
- Report written to `{output_dir}/629-lifecycle.md` (atomic single Write call)
- Summary returned to coordinator

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
