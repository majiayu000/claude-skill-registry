---
name: alto-protocol
description: Use when working with ALTO protocol files - runs/state.json, runs/handoffs/*.md, runs/tasks/*.md, runs/plan.md, or runs/milestones.md. Reference for file formats and state machine.
---

# ALTO Protocol

## Required Folders
- `runs/milestones.md` — high-level architecture (orchestrator output)
- `runs/decisions.md` — architectural decisions (orchestrator output)
- `runs/plan.md` — detailed batch plan (planner output)
- `runs/planning-config.json` — planning configuration
- `runs/state.json` — protocol state
- `runs/tasks/` — task files
- `runs/handoffs/` — task completion handoffs

## runs/state.json Schema

```json
{
  "protocol": "alto-v1",
  "run_branch": "run/001",
  "phase": "ARCHITECTURE | PLANNING | IN_TASK | BETWEEN_TASKS | BLOCKED | COMPLETED | DEBUG",
  "current_task_id": "task-001",
  "current_role": "alto-backend",
  "current_handoff": "runs/handoffs/task-001.md",
  "completed_task_ids": [],
  "last_handoff": null,
  "estimated_tasks": 12,
  "replan_every": 4,
  "needs_architect": false,
  "updated_at": "ISO-8601"
}
```

**Note:** When setting `current_task_id`, also set `current_handoff` and pre-create the handoff template.

### Phase Values
- `ARCHITECTURE` — orchestrator exploring codebase, designing milestones
- `PLANNING` — planner creating task files from milestones
- `IN_TASK` — role agent executing a task
- `BETWEEN_TASKS` — task complete, checking for replan or next task
- `BLOCKED` — human review required
- `COMPLETED` — all tasks done, awaiting human decision (debug or next feature)
- `DEBUG` — human testing, fixing issues before merge

## runs/planning-config.json Schema

```json
{
  "require_approval": true,
  "replan_strategy": "auto",
  "fixed_batch_size": 5,
  "architect_model": "opus",
  "planner_model": "opus"
}
```

## runs/milestones.md Format (Orchestrator Output)

```markdown
# Milestones

## Summary
Brief description of the feature and overall approach.

## Estimated Scope
- **Estimated tasks:** 12
- **Replan every:** 4 tasks
- **Complexity:** low | medium | high

## Milestones

### Milestone 1: <name>
- Description of what this milestone achieves
- Objective items addressed: 6.1, 6.2
- Estimated tasks: 3

### Milestone 2: <name>
- Description
- Objective items addressed: 6.3
- Estimated tasks: 4

## Key Decisions
See `runs/decisions.md` for detailed trade-offs.
```

## runs/decisions.md Format (Orchestrator Output)

```markdown
# Architectural Decisions

## Decision 1: <title>
**Context:** Why this decision was needed
**Options considered:**
1. Option A - pros/cons
2. Option B - pros/cons
**Decision:** Which option and why
**Consequences:** What this means for implementation

## Decision 2: <title>
...
```

## Arbiter Checkpoint Folders
- `runs/arbiter/config.json` — thresholds
- `runs/arbiter/state.json` — last checkpoint metadata
- `runs/arbiter/pending.json` — snapshot triggering arbiter
- `runs/arbiter/decision.json` — arbiter output
- `runs/arbiter/checkpoints/` — historical reports

## Task File Format (runs/tasks/task-XXX.md)

Each task starts with YAML frontmatter:

```yaml
---
task_id: task-001
title: Short human title
role: alto-backend | alto-frontend | alto-docs | alto-gitops | alto-qa
follow_roles: []            # optional: list of agent names to additionally obey
post: []                    # optional: list of agent names to run after role succeeds
depends_on: []              # optional
inputs:
  - runs/milestones.md
  - runs/handoffs/task-000.md
allowed_paths:
  - backend/**
handoff: runs/handoffs/task-001.md
---
```

Then Markdown body with:

* Goal
* Constraints (if any)
* Definition of Done (must be concrete)
* How to verify (tests to run, commands, manual checks)

## Handoff Format (runs/handoffs/<task_id>.md)

**Required sections** (validated by `handoff-validate` hook):

* `## Summary` — what was done
* `## Files` / `## Files Touched` — list of modified files
* `## How to Verify` / `## Verification` — commands to validate

**Optional sections:**

* `## Interfaces` — API/contract changes
* `## Next Steps` — follow-up work or risks

Handoffs are validated on SubagentStop. Missing required sections block task completion.

### Handoff Template (Pre-created by Orchestrator)

```markdown
# Handoff: task-001

## Summary
<!-- What was accomplished -->

## Files Touched
<!-- List files modified -->

## How to Verify
<!-- Commands or manual checks -->
```

Role agents **Edit** this file (don't create from scratch). Path is in `state.json` → `current_handoff`.

### Post-Agent Handoffs

Post-agents (alto-qa, code-simplifier, alto-gitops) write separate files by appending their suffix:

```
current_handoff: runs/handoffs/task-001.md

alto-qa         → runs/handoffs/task-001-qa.md
code-simplifier → runs/handoffs/task-001-simplifier.md
alto-gitops     → runs/handoffs/task-001-gitops.md
```

Post-agents read `current_handoff` from state.json and derive their path.

## plan.md Format (Planner Output)

```markdown
# Plan: <Feature Name> - Batch N

## Current Milestone
<Which milestone this batch addresses>

## Tasks in This Batch

| ID | Title | Role | Depends On |
|----|-------|------|------------|
| task-001 | ... | alto-backend | - |
| task-002 | ... | alto-frontend | task-001 |

## Implementation Notes
<Detailed implementation notes for this batch>

## Progress
- Milestones completed: 1/4
- Tasks completed: 3/12
- Objective items done: 2/8
```
