---
name: task-implement
description: Implement GitHub issues or standalone tasks with full verification
user-invocable: true
allowed-tools: Skill, Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion
---

# Task Implementation Skill

Implement tasks through goal-based workflow with automatic mode selection and verification.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `task` | required | GitHub issue number/URL or task description |
| `language` | optional | java\|javascript (auto-detects if not specified) |
| `quick` | optional | Skip review/plan, execute directly (default: false) |
| `push` | optional | Auto-push after successful implementation (default: false) |
| `handoff` | optional | Handoff structure from previous task (JSON) |

## Prerequisites

Load required skills:
```
Skill: plan-marshall:manage-memories
```

## Workflow

### Step 0: Process Handoff Input

If `handoff` parameter provided: Parse JSON, extract artifacts/decisions/constraints, load memory refs.

### Step 1: Determine Mode

```
If task matches /^\d+$/ or "github.com/*/issues/" → FULL mode (Review → Plan → Execute)
If quick=true → QUICK mode (Execute only)
Otherwise → PLAN mode (Plan → Execute)
```

### Step 2: Check Memory for Pending Workflow

```bash
python3 .plan/execute-script.py plan-marshall:manage-memories:manage-memory list --category handoffs
```
If pending found: Prompt "[R]esume / [S]tart fresh / [A]bort"

### Step 3: Execute Mode-Specific Workflow

**FULL**: Load issue (via `tools-integration-ci:issue-view`), Review requirements, Plan implementation, Execute tasks, save progress to memory.

**PLAN**: Plan implementation, Execute tasks, save progress to memory.

**QUICK**: Execute task directly.

### Step 4: Verify Implementation

Auto-detect language: `pom.xml` → Java, `package.json` → JavaScript

Run build verification. Iterate up to 3 times if fails.

### Step 5: Commit and Push

If verification succeeds: Commit via git workflow.

If push=true: Run `git push`.

### Step 6: Cleanup and Return

Cleanup memory:
```bash
python3 .plan/execute-script.py plan-marshall:manage-memories:manage-memory cleanup --category handoffs --pattern "workflow-*"
```

---

## Mode Details

### FULL Mode (GitHub Issue)

1. Load issue details from GitHub
2. Review: Analyze requirements, identify acceptance criteria
3. Plan: Break down into implementation steps
4. Execute: Implement each step
5. Verify: Run build/tests

### PLAN Mode (Task Description)

1. Plan: Analyze task, create implementation steps
2. Execute: Implement each step
3. Verify: Run build/tests

### QUICK Mode

1. Execute: Implement task directly without planning
2. Verify: Run build/tests

---

## Usage Examples

**Full workflow with GitHub issue:**
```
/task-implement task=123
```

**Quick execution (no planning):**
```
/task-implement task="Add validation to User.java" quick
```

**Java task with auto-push:**
```
/task-implement task=456 language=java push
```

**Task description with planning:**
```
/task-implement task="Implement user authentication service"
```

## Architecture

Delegates to skills:
```
/task-implement (orchestrator)
  ├─> manage-memories skill (state persistence)
  └─> workflow-integration-git skill (commit workflow)
```

## Continuous Improvement

If you discover issues or improvements during execution, record them:

1. **Activate skill**: `Skill: plan-marshall:manage-lessons`
2. **Record lesson** with component: `{type: "skill", name: "task-implement", bundle: "pm-workflow"}`

## Related

| Skill | Purpose |
|-------|---------|
| `plan-marshall:manage-memories` | State persistence for recovery |
| `pm-workflow:workflow-integration-git` | Git commit workflow |
| `pm-workflow:pr-doctor` | Fix PR issues after implementation |
