---
name: manage-logging
description: Unified logging infrastructure for script execution, work progress, and decision tracking
user-invocable: false
allowed-tools: Read, Bash
---

# Logging Skill

Unified logging infrastructure providing script execution logging, semantic work progress tracking, and decision logging.

## Overview

This skill provides a single unified API for three logging concerns:

1. **Script Execution Logging**: Tracking of script executor invocations (type: `script`)
2. **Work Logging**: Semantic tracking of work progress (type: `work`)
3. **Decision Logging**: Tracking of decisions made during execution (type: `decision`)

## Log Files

All plan-scoped logs are stored in the `logs/` subdirectory of the plan.

### Script Execution Log

**File**: `.plan/plans/{plan-id}/logs/script-execution.log` (plan-scoped)
**Fallback**: `.plan/logs/script-execution-YYYY-MM-DD.log` (global)

### Work Log

**File**: `.plan/plans/{plan-id}/logs/work.log`
**Fallback**: `.plan/logs/work-YYYY-MM-DD.log` (global)

### Decision Log

**File**: `.plan/plans/{plan-id}/logs/decision.log`
**Fallback**: `.plan/logs/decision-YYYY-MM-DD.log` (global)

---

## CLI Script Usage

Script: `plan-marshall:manage-logging:manage-log`

### Write API (Positional)

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  {type} {plan_id} {level} "{message}"
```

**Arguments** (all positional, all required):

| Argument | Values | Description |
|----------|--------|-------------|
| `type` | `script`, `work`, `decision` | Log type (determines output file) |
| `plan_id` | kebab-case | Plan identifier |
| `level` | `INFO`, `WARN`, `ERROR` | Log level |
| `message` | string | Log message |

**Output**: None (exit code only)

### Read API

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  read --plan-id {plan_id} --type {work|script|decision} [--limit N] [--phase PHASE]
```

**Arguments**:

| Argument | Required | Description |
|----------|----------|-------------|
| `--plan-id` | Yes | Plan identifier |
| `--type` | Yes | Log type: `work`, `script`, or `decision` |
| `--limit` | No | Max entries to return (most recent) |
| `--phase` | No | Filter by phase (work/decision logs only) |

**Output** (TOON):

```toon
status: success
plan_id: my-plan
log_type: work
total_entries: 5
showing: 3

entries:
  - timestamp: 2025-12-11T11:14:30Z
    level: INFO
    hash_id: c8d3e2
    message: [STATUS] (pm-workflow:phase-1-init) Starting init phase
    phase: 1-init
  - timestamp: 2025-12-11T11:15:20Z
    level: INFO
    hash_id: f1a9b3
    message: [ARTIFACT] (pm-workflow:phase-1-init) Created deliverable: auth module
```

### Examples

```bash
# Write: Script execution logging
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  script my-plan INFO "pm-workflow:manage-task:manage-task add (0.15s)"

python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  script my-plan ERROR "pm-workflow:manage-task:manage-task add failed (exit 1)"

# Write: Work logging (include [CATEGORY] (caller) prefix)
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work my-plan INFO "[ARTIFACT] (pm-workflow:phase-1-init) Created deliverable: auth module"

python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work my-plan WARN "[STATUS] (pm-workflow:phase-5-execute) Skipped validation step"

# Write: Decision logging (NO [DECISION] prefix - file is the category)
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision my-plan INFO "(pm-workflow:phase-1-init) Detected domain: java - pom.xml found"

python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision my-plan INFO "(pm-plugin-development:ext-outline-plugin) Scope: bundles=all"

# Read: All work log entries
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  read --plan-id my-plan --type work

# Read: All decision log entries
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  read --plan-id my-plan --type decision

# Read: Last 5 work log entries
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  read --plan-id my-plan --type work --limit 5

# Read: Work log entries for 1-init phase only
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  read --plan-id my-plan --type work --phase 1-init
```

---

## Log Format

### Standard Entry Structure

```
[{timestamp}] [{level}] [{hash}] {message}
```

Every log entry automatically includes a 6-character hash computed from the message content. This provides:
- **Transparent ID generation**: Callers don't need to compute or track hashes
- **Deterministic**: Same message always produces the same hash
- **Traceability**: Findings can be linked across stages (analysis → resolution → Q-gate)

### Example Output

**script-execution.log**:
```
[2025-12-11T12:14:26Z] [INFO] [a3f2c1] pm-workflow:manage-files:manage-files create (0.19s)
[2025-12-11T12:17:50Z] [ERROR] [b7e4d9] pm-workflow:manage-task:manage-task add failed (exit 1)
```

**work.log**:
```
[2025-12-11T11:14:30Z] [INFO] [c8d3e2] [STATUS] (pm-workflow:phase-1-init) Starting init phase
[2025-12-11T11:15:20Z] [INFO] [f1a9b3] [ARTIFACT] (pm-workflow:phase-1-init) Created deliverable: auth module
[2025-12-11T11:17:30Z] [INFO] [e5c7d4] [PROGRESS] (pm-workflow:phase-5-execute) Task 1 completed
```

**decision.log**:
```
[2025-12-11T11:14:48Z] [INFO] [d2e8f1] (pm-workflow:phase-1-init) Detected domain: java - pom.xml found
[2025-12-11T11:20:15Z] [INFO] [a4b6c8] (pm-plugin-development:ext-outline-plugin) Scope: bundles=all
```

Note: Decision entries do NOT include a `[DECISION]` prefix - the file itself indicates the entry type. The hash ID (e.g., `[d2e8f1]`) is automatically generated from the message content.

### Log Levels

| Level | Description |
|-------|-------------|
| `INFO` | Progress, informational, or successful completion message |
| `WARN` | Warning (non-fatal issue) |
| `ERROR` | Error with details |

---

## Python Import (from scripts run via executor)

Scripts run via the executor have PYTHONPATH set up for cross-skill imports:

```python
from plan_logging import log_entry

# Log to global script log
log_entry('script', 'global', 'INFO', '[MY-COMPONENT] Processing started')

# Log to plan-specific log
log_entry('work', 'my-plan', 'INFO', '[ARTIFACT] Created deliverable')
```

**Note**: IDE warnings about unresolved imports are expected - PYTHONPATH is set at runtime by the executor.

---

## Storage Locations

### Plan-Scoped Logs

```
.plan/plans/{plan-id}/
└── logs/
    ├── script-execution.log    # Script execution tracking
    ├── work.log                # Work progress tracking
    └── decision.log            # Decision tracking
```

### Global Logs

```
.plan/logs/
├── script-execution-YYYY-MM-DD.log    # Daily global script logs
├── work-YYYY-MM-DD.log                # Daily global work logs (when no plan)
└── decision-YYYY-MM-DD.log            # Daily global decision logs
```

**Scope Selection**:
- If `plan_id` is provided and plan directory exists: plan-scoped log
- Otherwise: global log (both script and work types supported)

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PLAN_BASE_DIR` | Base directory for .plan structure | `.plan` |
| `LOG_MAX_OUTPUT` | Max chars to capture from stdout/stderr | `2000` |
| `LOG_RETENTION_DAYS` | Days to keep global logs | `7` |

---

## Integration Points

### With Script Executor

The executor automatically calls `log_script_execution()` after each script run.

### With Planning Skills

Planning skills call the simplified API:

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work my-plan INFO "[ARTIFACT] (pm-workflow:phase-4-plan) Created task: implement auth module"
```

---

## Scripts

| Script | Notation | Description |
|--------|----------|-------------|
| `manage-log.py` | `plan-marshall:manage-logging:manage-log` | CLI for logging operations (write and read) |
| `plan_logging.py` | - | Python module (imported, not executed) |

### Script Commands

| Command | Parameters | Description |
|---------|------------|-------------|
| (positional) | `{type} {plan_id} {level} "{message}"` | Write log entry |
| `read` | `--plan-id --type [--limit] [--phase]` | Read log entries (TOON output) |
