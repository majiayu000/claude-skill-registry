---
name: spec-update
description: Update spec documents by analyzing git history to sync task status with reality.
---

# Spec Update Skill

Synchronize spec documents with actual project state by analyzing git commits and working directory changes.

## Command Syntax

```
/spec.update [spec-path] [--mode=status|content|full] [--context="user instructions"]
```

**Arguments:**
- `spec-path` (optional): Path to spec file. If omitted, finds most recent in `./specs/active/*/`
- `--mode` (optional):
  - `status` (default): Update completion status only
  - `content`: Update spec structure based on learnings
  - `full`: Both status and content updates
- `--context` (optional): Manual overrides/clarifications

## Core Workflow

### Step 1: Locate and Parse Spec

1. **Find spec file:**
   - If path provided: use that
   - Else: search `./specs/active/**/spec.md` for most recent

2. **Parse structure:**
   - Identify task format (checkboxes, numbered lists, sections)
   - Extract tasks with current status
   - Preserve formatting

3. **Determine baseline:**
   - Use file creation time or first commit mentioning spec

### Step 2: Analyze Current State

Run git commands to gather evidence:

```bash
# Commits since plan creation
git log --oneline --since="<plan-creation-time>" --all
git log --stat --since="<plan-creation-time>" --all

# Current state
git status --short
git branch -vv

# Files changed since baseline
git diff <baseline>..HEAD --name-status
```

**Collect:**
- Commits that map to plan tasks
- Files created/modified/deleted
- Working directory changes
- Branch/sync status

### Step 2.5: Sync TodoWrite to tasks.yaml (if active)

If TodoWrite has entries matching spec tasks:

1. For each "completed" todo, update corresponding task in tasks.yaml to `status: completed`
2. For each "in_progress" todo, update to `status: in_progress`
3. Update `meta.last_updated` and `meta.progress` fields

This catches any completions that weren't synced immediately during task execution.

### Step 3: Map Evidence to Tasks

For each task:

1. **Search for evidence:**
   - Commit messages mentioning task
   - Files mentioned in task were modified
   - Tests exist if task mentions testing
   - Dependencies met

2. **Determine status:**
   - `completed`: Clear evidence in commits + files exist
   - `in_progress`: Working directory changes or partial completion
   - `pending`: No evidence
   - `blocked`: Explicit context or dependencies not met (add to task's `blocked_by` field)

3. **Collect evidence notes:**
   - Which commits
   - Which files changed
   - Test/build results

### Step 4: Update tasks.yaml

**Status mode** (`--mode=status`):

Update task statuses and add evidence:

```yaml
tasks:
  - id: PROJ-001
    content: Set up project structure
    status: completed
    active_form: Setting up project structure
    evidence:
      commits: [c228fea, 2f069d7]
      files: [src/feature_link/temporal.py, tests/test_errata_example.py]

  - id: PROJ-002
    content: Implement core logic
    status: in_progress
    active_form: Implementing core logic
    evidence:
      notes: "3 files changed in working directory"

  - id: PROJ-003
    content: Write integration tests
    status: pending
    active_form: Writing integration tests

meta:
  last_updated: 2025-12-17
  progress: 1/3
```

**Content mode** (`--mode=content`):

Also update structure:
- Add new tasks via dignity's `add_task()` function
- Update task content/active_form via `update_task()`
- Remove obsolete tasks via `discard_task()`
- Update phases and checkpoints as needed

**User context**: If `--context` provided, apply manual overrides (takes precedence over auto-detection).

### Step 5: Present Summary

```
## Spec Update Summary

Spec: ./specs/active/refactor/
Tasks: tasks.yaml (progress: 5/10)
Baseline: c228fea (2025-11-06)

Status:
  ✓ Completed: 5 tasks
  • In Progress: 2 tasks
  ○ Pending: 3 tasks

Recent Activity:
  - 8 commits since plan creation
  - 12 files modified

Next actions:
  1. REFAC-006: Implement validation (ready)
  2. REFAC-007: Add error handling (ready)
```

---

## Matching Heuristics

**Strong evidence (auto-mark complete):**
- Commit message explicitly references task
- Commit modifies exact files mentioned
- All acceptance criteria met

**Weak evidence (mark in-progress):**
- Commit touches related files
- Working directory has related changes
- Partial completion of multi-step task

**Conservative approach:** When uncertain, prefer in-progress over completed

## Best Practices

### Preserve Structure
- Keep all non-task content unchanged
- Maintain indentation and formatting
- Append evidence (don't remove existing notes)
- Don't remove user comments

### Handle tasks.yaml Structure
- Core fields: spec, code, next_id, tasks
- Task statuses: pending, in_progress, completed
- Optional: phases with checkpoints
- Optional: evidence (commits, files, notes)

## Examples

```bash
# Update most recent spec status
/spec.update

# Full update with content changes
/spec.update --mode=full

# Manual override for blocker
/spec.update --context="Task 5 blocked waiting for API docs"

# Specific spec
/spec.update ./specs/active/auth/spec.md --mode=full
```

---

## Integration

- Created by `/spec.create`
- Updated regularly as work progresses
- Provides visibility into completion status
- Informs `/spec.archive` decision

**Best practice:** Run at end of each work session to keep synchronized with reality.
