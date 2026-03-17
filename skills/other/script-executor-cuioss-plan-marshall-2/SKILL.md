---
name: tools-script-executor
description: Universal script execution pattern via execute-script.py proxy
user-invocable: false
allowed-tools: Read, Bash
---

# Script Executor Skill

## Overview

All marketplace scripts are executed through `.plan/execute-script.py`:

```bash
python3 .plan/execute-script.py {notation} {subcommand} {args...}
```

## Notation Format

Simplified notation: `{bundle}:{skill}`

| Example |
|---------|
| `pm-workflow:manage-files` |
| `pm-dev-builder:builder-maven-rules` |

## Examples

```bash
# Document operations (typed documents)
python3 .plan/execute-script.py pm-workflow:manage-plan-documents:manage-plan-documents request create --plan-id my-plan --title "My Task" --source description --body "Task details"
python3 .plan/execute-script.py pm-workflow:manage-plan-documents:manage-plan-documents request read --plan-id my-plan

# File operations (generic files)
python3 .plan/execute-script.py pm-workflow:manage-files:manage-files write --plan-id my-plan --file notes.md --content "..."

# Build operations
python3 .plan/execute-script.py pm-dev-java:plan-marshall-plugin:maven run --targets clean,verify

# References operations
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references set --plan-id my-plan --key foo --value bar
```

## Error Handling

The executor standardizes error output:

```
SCRIPT_ERROR    {notation}    {exit_code}    {summary}
```

## Execution Logging

The executor provides two-tier logging:

### Plan-Scoped Logging

When a plan ID is provided, logs to:
```
.plan/plans/{plan-id}/script-execution.log
```

**Two ways to enable plan-scoped logging:**

| Parameter | Use Case | Behavior |
|-----------|----------|----------|
| `--plan-id` | Scripts that accept it (manage-* scripts) | Script uses value + logging picks it up |
| `--trace-plan-id` | Scripts without `--plan-id` (scan-*, analyze-*) | Stripped before passing to script, logging only |

**Example with --plan-id** (script uses it):
```bash
python3 .plan/execute-script.py pm-workflow:manage-files:manage-files add \
  --plan-id my-plan --file task.md
```

**Example with --trace-plan-id** (logging only, stripped):
```bash
python3 .plan/execute-script.py pm-plugin-development:tools-marketplace-inventory:scan-marketplace-inventory \
  --trace-plan-id my-plan --include-descriptions
```

The `--trace-plan-id` parameter is removed before the script executes, so the script never sees it. This enables plan-scoped logging for scripts that don't have their own `--plan-id` parameter.

**Benefits**:
- Tied to plan lifecycle (deleted when plan archived/deleted)
- Enables per-plan audit trail

### Global Logging

Fallback when no plan context:
```
.plan/logs/script-execution-YYYY-MM-DD.log
```

**Benefits**:
- Session-based daily logs
- Automatically cleaned by `/marshall-steward` (7 days retention)

### Log Entry Formats

**Success entries** (single-line):
```
[2025-12-08T10:30:00Z] [INFO] [SCRIPT] pm-workflow:manage-files:manage-files add (0.15s)
```

**Error entries** (multi-line with fields):
```
[2025-12-08T10:31:00Z] [ERROR] [SCRIPT] pm-workflow:manage-files:manage-files add (0.23s)
  exit_code: 1
  args: --plan-id my-plan --file missing.md
  stderr: FileNotFoundError: missing.md not found
```

See `plan-marshall:manage-logging` skill for full log format specification.

## Environment Variables

The executor exports environment variables to child scripts:

| Variable | Purpose | Default |
|----------|---------|---------|
| `PLAN_DIR_NAME` | Directory name for plan storage (e.g., `.plan`) | `.plan` |
| `PYTHONPATH` | Cross-skill import paths | Auto-built from all script directories |

### PLAN_DIR_NAME Usage

Scripts should use this for path construction instead of hardcoding `.plan`:

```python
import os
from pathlib import Path

# Get the plan directory name
_PLAN_DIR_NAME = os.environ.get('PLAN_DIR_NAME', '.plan')

# Use in path construction
DATA_DIR = Path(_PLAN_DIR_NAME) / "project-architecture"
LOG_DIR = Path(_PLAN_DIR_NAME) / "logs"
```

**Key points**:
- Always provide `.plan` as fallback for standalone execution
- The executor uses `setdefault()` to respect existing values (e.g., from test infrastructure)
- This enables test isolation and parallel project execution without interference

## Setup

Run `/marshall-steward` to generate the executor after bundle changes.

## Architecture

```
.plan/
├── execute-script.py      # Generated executor with embedded mappings
├── marshall-state.toon    # Plugin root path + metadata
└── logs/                  # Global execution logs (no plan context)
    └── script-execution-YYYY-MM-DD.log

~/.claude/plugins/cache/plan-marshall/
└── {bundle}/              # Installed plugin bundles
    └── {version}/         # Versioned bundle contents
        └── skills/...     # Skills with scripts
```

## Bootstrap Pattern (Before Executor Exists)

When `.plan/execute-script.py` doesn't exist yet (first run), use the bootstrap pattern:

### Step 1: Get Plugin Root

Check `.plan/marshall-state.toon` for cached `plugin_root`, or detect it:

```bash
python3 ~/.claude/plugins/cache/*/plan-marshall/*/skills/marshall-steward/scripts/bootstrap-plugin.py get-root
```

Output:
```
plugin_root	/Users/.../.claude/plugins/cache/plan-marshall
source	detected|cached
```

### Step 2: Execute Scripts Directly

Use the plugin root with glob pattern for version:

```bash
python3 ${PLUGIN_ROOT}/plan-marshall/*/skills/{skill}/scripts/{script}.py {args}
```

### State File Format

`.plan/marshall-state.toon`:
```
plugin_root	/Users/oliver/.claude/plugins/cache/plan-marshall
detected_at	2025-12-12T10:30:00+00:00
```

This pattern enables:
- Plugin scripts to work in any project (not just the marketplace repo)
- Caching for fast subsequent lookups
- Version-agnostic paths via glob

## Wait Pattern (Optional)

The script executor includes a synchronous polling utility for blocking until async operations complete.

**When to Load**: Activate when implementing workflows that wait for:
- CI/CD pipeline completion
- Sonar analysis completion
- External service readiness
- Any async operation requiring polling

**Load Reference**:
```
Read standards/wait-pattern.md
```

**Quick Usage**:

```bash
# Adaptive mode (timeout managed via run-config)
# Outer shell timeout (600s) prevents Claude from canceling
timeout 600s python3 .plan/execute-script.py plan-marshall:tools-script-executor:await-until poll \
  --check-cmd "python3 .plan/execute-script.py plan-marshall:tools-integration-ci:github ci status --pr-number 123" \
  --success-field "status=success" \
  --failure-field "status=failure" \
  --command-key "ci:pr_checks"

# Explicit mode (manual timeout)
timeout 600s python3 .plan/execute-script.py plan-marshall:tools-script-executor:await-until poll \
  --check-cmd "gh pr checks 123 --json state" \
  --success-field "status=success" \
  --timeout 300 \
  --interval 30
```

**Note**: When using Bash tool, set `timeout` parameter to `600000` (ms) to match shell timeout.

**Output** (TOON format):
```
status          success|timeout|failure
duration_sec    Actual wait duration in seconds
polls           Number of condition checks
timeout_used_sec Timeout value used in seconds
timeout_source  explicit|adaptive|default
command_key     The command key (if adaptive)
final_result.*  Flattened fields from last check
```

## Integration with Verification

The verification skill recognizes this execution pattern:

**Allowed**:
- `python3 .plan/execute-script.py {notation} ...`

**Violation**:
- `python3 {direct_script_path} ...` (after migration complete)
