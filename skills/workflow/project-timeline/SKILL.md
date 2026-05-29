---
name: Project Timeline
description: Systematic checklist execution (CLI-based) (project)
---

# Project Timeline CLI

Manage project timeline with CLI: `venv/bin/python SCRIPTS/timeline_cli.py` (use as `timeline`)

## When to Load This Skill

- Starting a new work session (get next task)
- Completing any checklist item (mark complete)
- Unsure what to work on next
- Checking progress

## CLI Commands

### Get Next Task
```bash
# What should I work on?
venv/bin/python SCRIPTS/timeline_cli.py next

# Next task in week 1
venv/bin/python SCRIPTS/timeline_cli.py next --week 1

# Next task in test section
venv/bin/python SCRIPTS/timeline_cli.py next --section test

# JSON output
venv/bin/python SCRIPTS/timeline_cli.py next --json
```

### Mark Complete
```bash
# Mark done + automatic git commit
venv/bin/python SCRIPTS/timeline_cli.py complete w1-test-003

# Mark done without commit
venv/bin/python SCRIPTS/timeline_cli.py complete w1-test-003 --no-commit

# Custom commit message
venv/bin/python SCRIPTS/timeline_cli.py complete w1-test-003 -m "Custom message"
```

### Check Status
```bash
# Current week progress
venv/bin/python SCRIPTS/timeline_cli.py status

# JSON output
venv/bin/python SCRIPTS/timeline_cli.py status --json
```

### Find Tasks
```bash
# All pending tasks
venv/bin/python SCRIPTS/timeline_cli.py find --status pending

# Week 1 tasks
venv/bin/python SCRIPTS/timeline_cli.py find --week 1

# Completed tasks in test section
venv/bin/python SCRIPTS/timeline_cli.py find --status completed --section test

# First 5 tasks
venv/bin/python SCRIPTS/timeline_cli.py find --limit 5
```

## Workflow

1. **Start Session**: `timeline next` → Get next pending task
2. **Do Work**: Implement/test/document
3. **Complete**: `timeline complete TASK_ID` → Updates JSON + git commit
4. **Push**: `git push` (if configured)

## Core Principles

### Priority 1: Complete the Framework
**Establish baseline → Research dependencies → Complete framework logic**

Focus on building complete system first:
- ✅ All commands exist and work
- ✅ All wrappers exist and work
- ✅ All skills exist
- ✅ State machine works
- ✅ Integration works end-to-end

**DO NOT get distracted by:**
- Testing multiple hypotheses (1-2 validates system)
- Optimizing performance (works first, fast second)
- Adding features not in checklist
- Extensive documentation (minimal docs, focus on code)

### Priority 2: Validate the Framework
**Validate logic paths → Test robustness → Calibrate thresholds**

Only after Priority 1 complete:
- Test decision framework with diverse scenarios
- Measure false positive/negative rates
- Calibrate thresholds
- Validate reliability

**Robustness is meaningless without completeness.**

## Authoritative Documentation (Source of Truth)

**When confused about workflow, phases, or decisions:**
- Read: `PROJECT_DOCUMENTATION/autonomous_decision_framework.md`
- Contains: 5-phase workflow, decision thresholds, routing logic

**When confused about architecture or how components fit:**
- Read: `PREVIOUS_WORK/PROJECT_DOCUMENTATION/autonomous_workflow_architecture.md`
- Contains: Complete system architecture, state machine, integration patterns

**Never guess. Always research first. Use authoritative docs as source of truth.**

## CLI Help

Use `--help` for command details:
```bash
venv/bin/python SCRIPTS/timeline_cli.py --help
venv/bin/python SCRIPTS/timeline_cli.py next --help
venv/bin/python SCRIPTS/timeline_cli.py complete --help
```

**Do not read timeline_cli.py source code. Use --help for usage.**

---

**Context Savings**: 60 lines (vs 631 lines in old skill) = 90% reduction

**Progressive Disclosure**: Load only what you need (next task, not entire timeline)

**Trifecta**: CLI works for humans, teams, AND agents
