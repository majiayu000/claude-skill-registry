---
name: service-health-check
description: "Service health monitoring: Discover, Check, Report in 3 phases."
user-invocable: false
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
routing:
  triggers:
    - "service status"
    - "process health"
    - "uptime check"
    - "is service running"
    - "check health"
  category: infrastructure
  not_for: "validating individual API endpoint responses (use endpoint-validator); only service/process liveness and uptime"
  pairs_with:
    - kubernetes-debugging
    - endpoint-validator
    - condition-based-waiting
---

# Service Health Check Skill

## Overview

This skill provides deterministic service health monitoring using the **Discover-Check-Report** pattern. It finds services, gathers health signals from multiple sources (process table, health files, port binding), and produces actionable reports identifying degraded or failed services.

**Core principle**: Health assessment is evidence-based. Never report a service healthy without verifying process status independently of health file content. Never assume a running process is functional — always cross-check against health files and port binding.

---

## Instructions

### Phase 1: DISCOVER

**Goal**: Identify all services to check before running any health probes.

**Step 1: Locate service definitions**

Search for service configuration in this order:
1. `services.json` in project root
2. Docker/docker-compose files for service definitions
3. systemd unit files or process manager configs
4. User-provided service specification

**Step 2: Build service manifest**

For each service, establish:

```markdown
## Service Manifest
| Service | Process Pattern | Health File | Port | Stale Threshold |
|---------|----------------|-------------|------|-----------------|
| api-server | gunicorn.*app:app | /tmp/api_health.json | 8000 | 300s |
| worker | celery.*worker | /tmp/worker_health.json | - | 300s |
| cache | redis-server | - | 6379 | - |
```

**Validation constraints**:
- Each process pattern must be specific enough to avoid false matches (e.g., "python" matches all Python processes—use full paths or arguments instead)
- Health file paths must be absolute
- Port numbers must be valid (1-65535)
- Pattern specificity matters: narrow patterns with full command paths, distinguishing arguments, or specific binary names

**Step 3: Validate manifest**

Confirm each entry passes the constraints above. If a pattern is too broad, use `ps aux | grep` to identify distinguishing arguments, then update the pattern.

**Gate**: Service manifest complete with at least one service. Proceed only when gate passes.

### Phase 2: CHECK

**Goal**: Gather health signals for every service in the manifest. Always check process status independently of health file content—a running process and a healthy health file are separate signals.

**Step 1: Check process status**

For each service, run process check:
```bash
pgrep -f "<process_pattern>"
```
Record: running (true/false), PIDs, process count.

**Rationale**: Process existence is the primary signal. A missing process always means the service is DOWN. A running process alone is insufficient—the service may have crashed or failed to bind to its port.

**Step 2: Parse health files (if configured)**

Read and parse JSON health files. Evaluate:
- Does the file exist?
- Does it parse as valid JSON?
- How old is the timestamp (staleness)? Default stale threshold is 300 seconds.
- What status does the service self-report?
- What is the connection state?

**Critical constraint**: Never trust health file content alone. The file could be stale from before a process crash. Always verify:
1. Process is still running
2. Health file timestamp is fresh (within configured threshold)
3. Status field matches evidence (e.g., "error" requires restart)

**Step 3: Probe ports (if configured)**

Check if expected ports are listening:
```bash
ss -tlnp "sport = :<port>"
```

**Rationale**: Verify ports are actually bound. A process can start but fail to bind to its configured port—that is effectively a DOWN state, not HEALTHY.

**Step 4: Evaluate health per service**

Apply this decision tree (constraints embedded in logic):

1. **Process not running** → **DOWN** (definitive)
2. **Process running + health file missing** → **WARNING** (limited visibility, but process is alive)
3. **Process running + health file stale** (> threshold) → **WARNING** (file hasn't updated in configured time, suggests no activity or crash recovery in progress)
4. **Process running + status=error** → **ERROR** (restart recommended immediately)
5. **Process running + disconnected > 30 minutes** → **WARNING** (long disconnect suggests stuck state, restart recommended)
6. **Process running + disconnected < 30 minutes** → **DEGRADED** (allow reconnection window, monitor)
7. **Process running + port not listening** (when port is configured) → **ERROR** (process running but failed to bind port)
8. **Process running + healthy** → **HEALTHY** (all checks pass)
9. **Process running + no health file configured** → **RUNNING** (limited visibility, process verified only)

**Gate**: All services evaluated with evidence-based status. No status is determined without concrete signal (process check, health file, or port probe). Proceed only when gate passes.

### Phase 3: REPORT

**Goal**: Produce structured, actionable health report with specific remediation commands.

**Step 1: Generate summary**

```
SERVICE HEALTH REPORT
=====================
Checked: N services
Healthy: X/N

RESULTS:
  service-name         [OK  ] HEALTHY     PID 12345, uptime 2d 4h
  background-worker    [WARN] WARNING     Health file stale (15 min)
  cache-service        [DOWN] DOWN        Process not found

RECOMMENDATIONS:
  background-worker: Restart recommended - health file not updated in 900s
  cache-service: Start service - process not running

SUGGESTED ACTIONS:
  systemctl restart background-worker
  systemctl start cache-service
```

**Step 2: Set exit status**
- All HEALTHY/RUNNING → exit 0
- Any WARNING/DEGRADED/ERROR/DOWN → exit 1

**Step 3: Present to user**
- Lead with the summary line (X/N healthy)
- Highlight any services needing action
- Provide copy-pasteable commands for remediation
- Never auto-restart without explicit user flag. Always report findings first, let user decide.

**Gate**: Report delivered with actionable recommendations for all non-healthy services.

---

## Examples

### Example 1: Routine Health Check
User says: "Are all services up?"
Actions:
1. Locate services.json, build manifest (DISCOVER)
2. Check each process, parse health files, probe ports (CHECK)
3. Output structured report showing 3/3 healthy (REPORT)
Result: Clean report, no action needed

### Example 2: Stale Worker Detection
User says: "The background worker seems stuck"
Actions:
1. Identify worker service from config (DISCOVER)
2. Find process running but health file 20 minutes stale (CHECK) — triggers WARNING decision in tree
3. Report WARNING with restart recommendation (REPORT)
Result: Specific diagnosis with actionable command

---

## Error Handling

### Error: "No Service Configuration Found"
Cause: No services.json, docker-compose, or systemd units discovered
Solution:
1. Ask user for service name and process pattern
2. Build minimal manifest from user input
3. Proceed with manual configuration

### Error: "Process Pattern Matches Too Many PIDs"
Cause: Pattern too broad (e.g., "python" matches all Python processes)
Solution:
1. Narrow pattern with full command path or arguments
2. Use `ps aux | grep` to identify distinguishing arguments
3. Update manifest with more specific pattern
4. Rationale: False positives hide real failures. Specificity is required to avoid misdiagnosis.

### Error: "Health File Exists But Cannot Parse"
Cause: Malformed JSON, permissions issue, or file being written during read
Solution:
1. Check file permissions with `ls -la`
2. Attempt raw read to inspect content
3. If mid-write, retry after 2-second delay
4. Report as WARNING with parse error details

---

## References

### Health File Format Reference

Services should write health files as:
```json
{
    "timestamp": "ISO8601, updated every 30-60s",
    "status": "healthy|degraded|error",
    "connection": "connected|disconnected|reconnecting",
    "last_activity": "ISO8601 of last meaningful action",
    "running": true,
    "uptime_seconds": 12345,
    "metrics": {}
}
```

### Key Constraints Summary

| Constraint | Rationale | Application |
|-----------|-----------|-------------|
| Process status verified independently of health file | Running process ≠ functional service | Always check process before trusting health file |
| Health file staleness detected by timestamp freshness | File could be stale from before crash | Check timestamp against 300s (configurable) threshold |
| Port binding verified when configured | Process running doesn't mean port is bound | Always verify expected port listening when port specified |
| No auto-restart without explicit flag | Restart masks root cause | Report findings first; only execute restart if user flags it |
| Narrow process patterns required | "python" matches all processes, giving false matches | Use full paths or specific args; validate with `ps aux \| grep` |
| Evidence-based status only | Status must have supporting signal | No status without concrete evidence (process, health file, or port) |
