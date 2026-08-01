---
name: checkpoint-workflow
description: Reference for agents working with the workflow checkpoint system.
---

# Checkpoint Workflow Skill

Reference for agents working with the workflow checkpoint system.

## Purpose

The checkpoint system enables workflow resume after context compaction. Each `/work-on-issue` session creates a workflow that tracks:
- Current phase (setup → research → implement → review → finalize)
- Actions taken (plan created, PR opened, etc.)
- Commits made during the workflow

## Database Location

Checkpoint state is stored in `.claude/execution-state.db` (gitignored).

## CLI Commands

All commands use `pnpm checkpoint workflow <action>`.

### Create Workflow

```bash
pnpm checkpoint workflow create <issue_number> "<branch_name>"
```

**Output:** JSON with `id`, `issue_number`, `branch_name`, `status`, `current_phase`

**Example:**
```bash
pnpm checkpoint workflow create 12 "feat/12-add-parser"
```

### Find Workflow by Issue

```bash
pnpm checkpoint workflow find <issue_number>
```

**Output:** JSON workflow or `null`

**Use case:** Check if workflow exists before creating a new one.

### Get Workflow Summary

```bash
pnpm checkpoint workflow get <workflow_id>
```

**Output:** JSON with `workflow`, `actions`, `commits`

**Use case:** Full context for resuming work.

### List Workflows

```bash
pnpm checkpoint workflow list [--status=running|completed|failed] [--limit=N]
```

**Output:** JSON array of workflows

### Set Phase

```bash
pnpm checkpoint workflow set-phase <workflow_id> <phase>
```

**Phases:** `setup`, `research`, `implement`, `review`, `finalize`

### Set Status

```bash
pnpm checkpoint workflow set-status <workflow_id> <status>
```

**Statuses:** `running`, `paused`, `completed`, `failed`

### Log Action

```bash
pnpm checkpoint workflow log-action <workflow_id> <action_type> <status> [details]
```

**Status values:** `success`, `failed`, `skipped`

**Common action types:**
- `workflow_started`
- `dev_plan_created`
- `implementation_complete`
- `pr_created`

### Log Commit

```bash
pnpm checkpoint workflow log-commit <workflow_id> <sha> "<message>"
```

**CRITICAL: Commit logging pattern**

Always log commits in two separate commands:

```bash
# 1. Get SHA (separate command)
git rev-parse HEAD

# 2. Log to checkpoint (use literal SHA, not variable)
pnpm checkpoint workflow log-commit "abc123" "a1b2c3d" "feat: add feature"
```

**NEVER combine with `&&` or use shell variables.** This prevents errors if the git command fails.

### Delete Workflow

```bash
pnpm checkpoint workflow delete <workflow_id>
```

## Integration Patterns

### At Workflow Start (setup-agent)

```bash
# Check for existing workflow
pnpm checkpoint workflow find {issue_number}

# If found with status=running, offer to resume
# If not found, create new workflow
pnpm checkpoint workflow create {issue_number} "{branch_name}"
```

### After Plan Creation (issue-researcher)

```bash
pnpm checkpoint workflow set-phase "{workflow_id}" research
pnpm checkpoint workflow log-action "{workflow_id}" "dev_plan_created" success
```

### After Each Commit (atomic-developer)

```bash
# Get SHA first
git rev-parse HEAD
# Then log (with actual SHA value)
pnpm checkpoint workflow log-commit "{workflow_id}" "{sha}" "{message}"
```

### After PR Creation (finalize-agent)

```bash
pnpm checkpoint workflow log-action "{workflow_id}" "pr_created" success
pnpm checkpoint workflow set-status "{workflow_id}" completed
```

## Resume Flow

When starting `/work-on-issue`:

1. Check for existing workflow: `pnpm checkpoint workflow find {issue_number}`
2. If found with `status=running`:
   - Show current phase and recent actions
   - Ask: "Resume from {phase}?" or "Start fresh?"
3. If resuming, skip to the saved phase
4. If starting fresh, delete old workflow and create new one

## Error Handling

If a checkpoint command fails:
1. Log the error
2. Continue with the workflow (checkpoints are advisory, not blocking)
3. The work can still be done, just without resume capability
