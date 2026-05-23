---
name: digital-fte-orchestrator
description: |
  Main task processing loop using Claude Code with Ralph Wiggum pattern.
  Use when running the orchestrator, debugging task processing,
  configuring approval workflows, or understanding the task lifecycle.
  NOT when creating individual watchers (use specific watcher skills).
---

# Digital FTE Orchestrator Skill

Task processing with Ralph Wiggum loop pattern.

## Quick Start

```bash
# Normal mode
python scripts/run.py

# Process once and exit
python scripts/run.py --once

# Dry run
python scripts/run.py --dry-run
```

## Task Flow

```
Needs_Action → [Claude analyzes] → Pending_Approval or Done
Pending_Approval → [Human approves] → Approved
Approved → [Claude executes] → Done
```

## Configuration

- `--max-iterations` - Max retries per task (default: 10)
- `--poll-interval` - Seconds between polls (default: 30)
- `--dry-run` - Test without execution
- `--once` - Process once and exit

## Verification

Run: `python scripts/verify.py`
