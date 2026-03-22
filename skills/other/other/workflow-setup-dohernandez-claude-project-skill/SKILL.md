---
name: workflow-setup
description: Setup development branch and workflow context for task-based workflows.
user-invocable: false
allowed-tools: [Read, Write, Edit, Bash, Glob]
---

# CI E2E Runner Workflow Setup

## Purpose
Automate the development environment setup for branch-based workflows. This skill is called by `workflow` during the "start" phase to create a feature branch and workflow context.

## Quick Reference
- **Creates**: Git branch from main, workflow context directory, context.json
- **Requires**: Branch name, title, and type from workflow
- **Output**: Branch checked out, context.json written
- **Not user-invocable**: Called internally by `/workflow start`

## What It Does

1. **Updates main branch** (fetch + pull)
2. **Creates feature branch** from latest main
3. **Creates workflow directory** at `.claude/workflow/<branch>/`
4. **Writes context.json** with workflow metadata

## Procedure

### Step 1: Update Base Branch

**CRITICAL**: Update main before creating branch to avoid branching from stale code.

```bash
git fetch origin main
git checkout main
git pull origin main
```

### Step 2: Create Feature Branch

```bash
git checkout -b <branch> main
```

Handle errors:
- Branch already exists locally: ask user how to proceed
- Branch already exists remotely: ask user if they want to track it

### Step 3: Create Workflow Directory

```bash
mkdir -p .claude/workflow/<branch>
```

### Step 4: Write Context

Write `context.json` with workflow metadata:

```json
{
  "source": "text",
  "title": "Add retry logic to E2E pipeline",
  "branch": "feat/add-retry-logic-to-e2e-pipeline",
  "type": "feat",
  "createdAt": "2026-02-22T10:30:00Z"
}
```

### Step 5: Report Completion

Inform the workflow skill that setup is complete:
- Branch name and current branch confirmed
- Context file location
- Ready for implementation delegation

## Integration with workflow

This skill is called from `workflow` after branch name generation:

```
workflow start "Add retry logic to E2E pipeline"
  1. Safety checks
  2. Determine type (feat)
  3. Generate branch name
  4. >>> Call workflow-setup <<<
  5. Delegate to /task or /bugfix
```

## Example Usage

Called internally by workflow:

```
/workflow start "Add retry logic to E2E pipeline"
  -> workflow generates branch: feat/add-retry-logic-to-e2e-pipeline
  -> workflow-setup:
     - Updates main (fetch + pull)
     - Creates branch feat/add-retry-logic-to-e2e-pipeline
     - Creates .claude/workflow/feat/add-retry-logic-to-e2e-pipeline/
     - Writes context.json
  -> workflow delegates to /task
```
