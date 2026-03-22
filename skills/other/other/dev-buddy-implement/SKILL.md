---
name: dev-buddy-implement
description: Implement a plan using TDD loop with TaskManagement progress tracking. Reads Implementation Steps from plan file, dispatches implementer step-by-step, runs tests after each step. Fully autonomous — no user prompts.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TaskOutput, TaskCreate, TaskUpdate, TaskList, TaskGet
---

# Implementation Stage Skill

Implement an approved plan using a TDD loop with TaskManagement-based progress tracking. Reads Implementation Steps and TDD Test Plan from the plan file. Dispatches the implementer agent step-by-step, runs mapped tests after each step.

**Fully autonomous — does NOT use AskUserQuestion.** Only true blockers (missing credentials, external dependency down) stop execution.

---

## Step 1: Validate Inputs

Read the plan file and verify required sections exist:
- `## Requirements` with acceptance criteria
- `## TDD Test Plan` with test IDs
- `## Implementation Steps` with step details
- `## Plan Review Record` with `"status": "approved"` in its fenced JSON block
- `## Risk Registry` with all risks acknowledged

If plan review is not approved, tell the user to run `/dev-buddy-review --plan` first.
If any risk is unacknowledged, tell the user to acknowledge risks first.

**Code review repair mode:** If `## Code Review Record` exists with `"status": "needs_changes"` in its fenced JSON block, this is a repair invocation:
1. Read the `must_fix` findings from the code review record's fenced JSON
2. For each finding, identify which implementation step is affected (via `contract_reference` field referencing AC or step)
3. Reset affected steps' status from `[x] done` back to `[ ] not started` in the plan file
4. Inject the findings into the implementer prompt for affected steps as:
   ```
   ISSUES FROM PRIOR REVIEW:
   - {finding.description} (file: {finding.file}:{finding.line}, fix: {finding.suggestion})
   ```
5. Re-run the TDD loop only for reset steps (skip steps still marked `[x] done`)

---

## Step 2: Load Config

```bash
bun -e "
import { loadDevBuddyConfig, getProviderType } from '${CLAUDE_PLUGIN_ROOT}/scripts/pipeline-config.ts';
const config = loadDevBuddyConfig();
const stage = config.stages['implementation'];
const executors = stage.executors.map(exec => ({
  ...exec,
  providerType: getProviderType(exec.preset)
}));
console.log(JSON.stringify({ executors, max_tdd_iterations: config.max_tdd_iterations }));
"
```

---

## Step 3: Extract Steps and Tests from Plan File

Read the plan file and extract:
1. All implementation steps (titles, AC mappings, test IDs, files, descriptions, rollbacks)
2. All tests from TDD Test Plan (IDs, commands, AC mappings)
3. Total step count

Parse the step status checkboxes:
- `[ ] not started` — pending
- `[x] done` — completed (skip)
- `[!] blocked` — blocked (skip)

This enables resume after context compaction.

---

## Step 4: Create Progress Tasks (TaskManagement)

**Create one task per implementation step using TaskCreate.**

```
For each step N (that is not already completed):
  T{N} = TaskCreate(
    subject='Step {N}: {title}',
    description='AC: {ac_ids} | Tests: {test_ids}
Files: {files}
What to do: {description}
Rollback: {rollback}',
    activeForm='Implementing step {N}...'
  )

  If step has dependencies from the plan (e.g., "Dependencies: Step 1, Step 3"):
    TaskUpdate(T{N}, addBlockedBy: [T{dep1}, T{dep2}])
  Else if N > 1 (fallback — linear chain):
    TaskUpdate(T{N}, addBlockedBy: [T{N-1}])
```

This creates a visible task list with dependency chaining.

---

## Step 5: TDD Execution Loop

For each step in order (skip completed/blocked):

### 5a. Claim the step
```
TaskUpdate(step_task_id, status: 'in_progress')
```

### 5b. Run mapped tests FIRST (establish failing baseline)

For each test ID mapped to this step (from TDD Test Plan):
- Run the test command via Bash
- Record the baseline result (expected to fail — this IS TDD)

### 5c. Dispatch implementer

Construct the implementation prompt for this specific step:

```
SINGLE_STEP_MODE: step {N}

STRICT PLAN ADHERENCE: Follow the plan EXACTLY. No deviations.

STEP DETAILS (from plan file):
Title: {title}
AC: {ac_ids}
Tests: {test_ids}
Files to modify: {files_to_modify}
Files to create: {files_to_create}
Existing code to reuse: {existing_code_to_reuse}
What to do: {description}
Rollback: {rollback}

TDD CYCLE:
1. The mapped tests have been run — they should be failing (red)
2. Implement EXACTLY what the step says — no more, no less
3. Run the mapped tests again — they must pass (green)
4. Write your output

Write output to {TMPDIR}/.vcp/oneshot/impl-{RAND}-step{N}.json
```

**Resolve system prompt and dispatch** (same stage/role composition as other skills).

Route by provider type:
- **subscription:** `Task(subagent_type: "general-purpose", model, prompt)`
- **api:** `Bash(run_in_background: true)` → `bun "${CLAUDE_PLUGIN_ROOT}/scripts/one-shot-runner.ts" --type api --output-id impl-{RAND}-step{N} --preset "{PRESET}" --model "{MODEL}" --cwd "${CLAUDE_PROJECT_DIR}" --task-stdin`

### 5d. Collect result and run tests

**For API/CLI executors:** The output file is wrapped in an envelope `{"event":"complete","provider":"...","model":"...","result":"..."}`. Parse the `result` field to get the actual implementer output. For subscription executors, the result is returned directly from the Task tool.

Read the implementer's output. Then run ALL mapped tests for this step:
- Run each test command from the TDD Test Plan where `test_ids` includes tests mapped to this step
- Check pass/fail

### 5e. Handle test results

**If all tests pass:**
1. `TaskUpdate(step_task_id, status: 'completed')`
2. Update plan file: change step status from `[ ] not started` to `[x] done` via Edit tool
3. Continue to next step

**If any test fails:**
1. Increment TDD iteration counter for this step
2. If iterations < max_tdd_iterations:
   - Re-dispatch implementer with failure output appended:
     ```
     ISSUES FROM PRIOR ATTEMPT:
     Test {test_id} failed:
     {test output}

     Fix the issue and ensure the test passes.
     ```
   - Return to 5d
3. If iterations >= max_tdd_iterations:
   - `TaskUpdate(step_task_id, status: 'blocked')`
   - Update plan file: change step status to `[!] blocked — test {test_id} fails after {N} retries`
   - **Do NOT ask the user** — continue to next step

---

## Step 6: Full Test Suite

After all steps are completed or blocked:

1. Run ALL test commands from the TDD Test Plan (full suite)
2. Record results

---

## Step 7: Update Plan File

Update the plan file with implementation results:

1. Update `**Status:**` to `code-review`
2. Verify all step statuses are updated (`[x] done` or `[!] blocked`)

---

## Step 8: Cleanup and Report

1. Remove temp files: `rm -f "{TMPDIR}/.vcp/oneshot/impl-{RAND}-"*`
2. Present to user:
   - Steps completed: {count}/{total}
   - Steps blocked: {count} (if any, with reasons)
   - Test results: {passed}/{total}
3. If any steps blocked: report which ones and why
4. Suggest next step: `/dev-buddy-review --code`

---

## Resume After Context Compaction

If the conversation context is compacted mid-implementation:

1. Read the plan file — step statuses show what's done vs pending
2. `TaskList()` — shows task statuses with dependency chain
3. Find the first non-completed step
4. Continue from that step (skip completed ones)

The combination of plan file checkboxes + TaskManagement ensures no work is lost.

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Plan not approved | Tell user to run `/dev-buddy-review --plan` first |
| Risks unacknowledged | Tell user to acknowledge risks first |
| All implementer dispatches fail | Report error to user |
| Test fails after max retries | Mark step blocked, continue to next |
| Missing credentials (true blocker) | Set status partial, report to user |
| No implementation executors configured | Report error, suggest `/dev-buddy-config` |

---

## Anti-Patterns

- Do NOT ask the user anything — you are fully autonomous
- Do NOT skip TaskCreate/TaskUpdate — progress must be tracked
- Do NOT deviate from the plan — follow it exactly
- Do NOT implement from memory — read step details from plan file
- Do NOT skip tests — TDD is mandatory
- Do NOT stop after some steps — implement ALL steps (mark blocked ones and continue)
