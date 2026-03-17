---
name: ln-629-lifecycle-auditor
description: Application lifecycle audit worker (L3). Checks bootstrap initialization order, graceful shutdown, resource cleanup, signal handling, liveness/readiness probes. Returns findings with severity, location, effort, recommendations.
allowed-tools: Read, Grep, Glob, Bash
---

# Lifecycle Auditor (L3 Worker)

Specialized worker auditing application lifecycle and entry points.

## Purpose & Scope

- **Worker in ln-620 coordinator pipeline**
- Audit **lifecycle** (Category 12: Medium Priority)
- Check bootstrap, shutdown, signal handling, probes
- Calculate compliance score (X/10)

## Inputs (from Coordinator)

Receives `contextStore` with tech stack, deployment type, codebase root.

## Workflow

1) Parse context
2) Check lifecycle patterns
3) Collect findings
4) Calculate score
5) Return JSON

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

```json
{
  "category": "Lifecycle",
  "score": 7,
  "total_issues": 4,
  "critical": 0,
  "high": 1,
  "medium": 3,
  "low": 0,
  "checks": [
    {"id": "bootstrap_order", "name": "Bootstrap Order", "status": "passed", "details": "Initialization sequence correct: config -> DB -> routes -> server"},
    {"id": "graceful_shutdown", "name": "Graceful Shutdown", "status": "failed", "details": "No SIGTERM handler found"},
    {"id": "resource_cleanup", "name": "Resource Cleanup", "status": "warning", "details": "DB connection closed, but file handles not released"},
    {"id": "signal_handling", "name": "Signal Handling", "status": "warning", "details": "SIGINT handled, SIGTERM missing"},
    {"id": "probes", "name": "Liveness/Readiness Probes", "status": "passed", "details": "/health and /ready endpoints present"}
  ],
  "findings": [
    {
      "severity": "HIGH",
      "location": "src/index.ts:1-50",
      "issue": "No SIGTERM handler for graceful shutdown",
      "principle": "Graceful Shutdown / Resource Management",
      "recommendation": "Add SIGTERM handler to close DB connections and server gracefully",
      "effort": "M"
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
