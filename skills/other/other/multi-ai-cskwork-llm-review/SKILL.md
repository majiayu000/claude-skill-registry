---
name: multi-ai
description: Start the multi-AI pipeline with a given request. Cleans up old task files and guides through plan → review → implement → review workflow.
plugin-scoped: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Multi-AI Pipeline Command

You are starting the multi-AI pipeline. Follow this process exactly.

**Note:** Scripts are located at `${CLAUDE_PLUGIN_ROOT}/scripts/`. The `.task/` directory is created in your project at `${CLAUDE_PROJECT_DIR}/.task/`.

## Step 1: Clean Up Previous Task

First, reset the pipeline state:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/orchestrator.sh" reset
```

This removes old `.task/` files and sets state to `idle`.

## Step 2: Create User Request

Write the user's request to `.task/user-request.txt`:

```bash
mkdir -p "${CLAUDE_PROJECT_DIR:-.}/.task"
```

Then write the request content to `.task/user-request.txt`.

## Step 3: Set Initial State

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh" set plan_drafting ""
```

## Step 4: Create Initial Plan

Create `.task/plan.json` with:
- `id`: "plan-YYYYMMDD-HHMMSS"
- `title`: Short descriptive title
- `description`: What the user wants
- `requirements`: List of requirements
- `created_at`: ISO8601 timestamp
- `created_by`: "claude"

## Step 5: Transition to Refining

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh" set plan_refining "$(bun ${CLAUDE_PLUGIN_ROOT}/scripts/json-tool.ts get .task/plan.json .id)"
```

## Step 6: Refine Plan

Create `.task/plan-refined.json` with technical details:
- Research the codebase
- Add `technical_approach`
- Add `files_to_modify` and `files_to_create`
- Add `potential_challenges`

## Step 7: Sequential Plan Reviews

Run reviews in order. Fix issues after each before continuing:

1. **Invoke /review-sonnet** → If issues, fix them
2. **Invoke /review-codex** → If issues, fix and restart from step 1

When all approve, continue.

## Step 8: Implement

**Invoke /implement-sonnet** to implement the approved plan.

This skill will:
- Write the code following the approved plan
- Add tests
- Output to `.task/impl-result.json`

## Step 9: Sequential Code Reviews

Run reviews in order. Fix issues after each before continuing:

1. **Invoke /review-sonnet** → If issues, fix them
2. **Invoke /review-codex** → If issues, fix and restart from step 1

When all approve, continue.

## Step 10: Complete

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh" set complete "$(bun ${CLAUDE_PLUGIN_ROOT}/scripts/json-tool.ts get .task/plan-refined.json .id)"
```

Report success to the user.

---

## Important Rules

- Follow this process exactly - no shortcuts
- Fix ALL issues raised by reviewers before continuing
- If codex rejects, restart the review cycle from sonnet
- Keep the user informed of progress at each major step
