---
name: parallelization
description: "Optional workflow skill: orchestrate parallel implementation by spawning scoped developer workers and merging results safely."
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
  - Task
  - Bash
---

# Parallelization (Optional)

Use this skill when you believe part of the work can be done in parallel **without increasing merge risk**.

## Principle

- **Developer is given scope**: each worker implements **one** scoped work item (typically one acceptance criterion).
- **No extra ceremony**: do not require “announce decision” rituals.
- **Safety first**:
  - **Git writes are forbidden unless explicitly approved** (branch/commit/push/merge).
  - If git writes are not approved, workers still produce results, but do not create branches or commits.
  - **Task docs are orchestrator-owned in parallel mode**: workers must not edit shared task documents (to avoid conflicts). The orchestrator updates task docs after applying/merging worker outputs.

## Critical Rule (true parallelism)

To maximize concurrency, **spawn ALL worker Task calls in a SINGLE assistant message**.

If your Task runtime supports background execution flags, you may enable them, but the workflow must remain correct without any tool-specific background setting.

## Inputs

Provide at minimum:

- `task_document_path`: path to task doc (file or directory)

Optionally (recommended):

- `context_summary_path`: path to `CONTEXT_SUMMARY.md` (if context-loader generated it)
- `branch_name`: main feature branch name (if applicable)
- `git_writes_approved`: `true|false` (must be explicit)

## Workflow

### 1) Identify parallelizable work items

- Read the task doc and list the acceptance criteria/work items.
- Select only items that can be implemented **independently** (different files/areas, minimal shared touching).

### 2) Spawn `developer-agent` workers

For each selected item, spawn a worker (use the same prompt structure for consistency):

```
Use Task tool:
subagent_type: "developer-agent"
prompt: "Implement criterion [N] (scoped work item) for task at [task_path].

Inputs:
- task_document_path: [task_document_path]
- criterion_number: [N]
- context_summary_path: [context_summary_path or 'none']
- branch_name: [branch_name or 'none']
- git_writes_approved: [true|false]

Constraints:
- Implement ONLY criterion [N]
- Follow TDD (RED→GREEN→REFACTOR) inside scope
- Do NOT do any git operations unless git_writes_approved=true
- Do NOT edit shared task documents; return notes for orchestrator to update docs

Return JSON result when done."
```

### 3) Consolidate results

- Collect each worker’s JSON.
- If `git_writes_approved=true` and branches/commits exist:
  - Merge each sub-branch into the main feature branch.
- If `git_writes_approved=false`:
  - Apply changes manually in the main working tree based on worker outputs (files changed + summary).
- Update the task document (checkboxes/changelog/tests) **once**, after worker outputs are applied/merged, to avoid parallel edit conflicts.

### 4) Run validation (example: backend)

```bash
cd backend
npm run format:check
npm run lint:check
npx tsc --noEmit -p tsconfig.json
npm run test:silent
```

## Output (to orchestrator)

Return:

- Which criteria were executed in parallel
- Worker JSON summaries
- Any conflicts/merge risks discovered
- What remains to be done sequentially

