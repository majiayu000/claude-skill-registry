---
name: workflow-lite-test-review
description: Post-execution test review and fix - chain from lite-execute or standalone. Reviews implementation against plan, runs tests, auto-fixes failures.
allowed-tools: Skill, Agent, AskUserQuestion, TodoWrite, Read, Write, Edit, Bash, Glob, Grep
---

# Workflow-Lite-Test-Review

Test review and fix engine for lite-execute chain or standalone invocation.

**Project Context**: Run `ccw spec load --category test` for test framework conventions, coverage targets, and fixtures.

---

## Usage

```
<session-path|--last>      Session path or auto-detect last session (required for standalone)
```

| Flag | Description |
|------|-------------|
| `--in-memory` | Mode 1: Chain from lite-execute via `testReviewContext` global variable |
| `--skip-fix` | Review only, do not auto-fix failures |

## Input Modes

### Mode 1: In-Memory Chain (from lite-execute)

**Trigger**: `--in-memory` flag or `testReviewContext` global variable available

**Input Source**: `testReviewContext` global variable set by lite-execute Step 4

**Behavior**: Skip session discovery, inherit convergenceReviewTool from execution chain, proceed directly to TR-Phase 1.

> **Note**: lite-execute Step 5 is the chain gate. Mode 1 invocation means execution + code review are complete — proceed with convergence verification + tests.

### Mode 2: Standalone

**Trigger**: User calls with session path or `--last`

**Behavior**: Discover session → load plan + tasks → `convergenceReviewTool = 'agent'` → proceed to TR-Phase 1.

```javascript
let sessionPath, plan, taskFiles, convergenceReviewTool

if (testReviewContext) {
  // Mode 1: from lite-execute chain
  sessionPath = testReviewContext.session.folder
  plan = testReviewContext.planObject
  taskFiles = testReviewContext.taskFiles.map(tf => JSON.parse(Read(tf.path)))
  convergenceReviewTool = testReviewContext.convergenceReviewTool || 'agent'
} else {
  // Mode 2: standalone — find last session or use provided path
  sessionPath = resolveSessionPath($ARGUMENTS)  // Glob('.workflow/.lite-plan/*/plan.json'), take last
  plan = JSON.parse(Read(`${sessionPath}/plan.json`))
  taskFiles = plan.task_ids.map(id => JSON.parse(Read(`${sessionPath}/.task/${id}.json`)))
  convergenceReviewTool = 'agent'
}

const skipFix = $ARGUMENTS?.includes('--skip-fix') || false
```

## Phase Summary

| Phase | Core Action | Output |
|-------|-------------|--------|
| TR-Phase 1 | Detect test framework + gather changes | testConfig, changedFiles |
| TR-Phase 2 | Convergence verification against plan criteria | reviewResults[] |
| TR-Phase 3 | Run tests + generate checklist | test-checklist.json |
| TR-Phase 4 | Auto-fix failures (iterative, max 3 rounds) | Fixed code + updated checklist |
| TR-Phase 5 | Output report + chain to session:sync | test-review.md |

## TR-Phase 0: Initialize

Set `sessionId` from sessionPath. Create TodoWrite with 5 phases (Phase 1 = in_progress, rest = pending).

## TR-Phase 1: Detect Test Framework & Gather Changes

**Test framework detection** (check in order, first match wins):

| File | Framework | Command |
|------|-----------|---------|
| `package.json` with `scripts.test` | jest/vitest | `npm test` |
| `package.json` with `scripts['test:unit']` | jest/vitest | `npm run test:unit` |
| `pyproject.toml` | pytest | `python -m pytest -v --tb=short` |
| `Cargo.toml` | cargo-test | `cargo test` |
| `go.mod` | go-test | `go test ./...` |

**Gather git changes**: `git diff --name-only HEAD~5..HEAD` → `changedFiles[]`

Output: `testConfig = { command, framework, type }` + `changedFiles[]`

// TodoWrite: Phase 1 → completed, Phase 2 → in_progress

## TR-Phase 2: Convergence Verification

**Skip if**: `convergenceReviewTool === 'skip'`  — set all tasks to PASS, proceed to Phase 3.

Verify each task's convergence criteria are met in the implementation and identify test gaps.

**Agent Convergence Review** (convergenceReviewTool === 'agent', default):

For each task in taskFiles:
1. Extract `convergence.criteria[]` from the task
2. Match `task.files[].path` against `changedFiles` to find actually-changed files
3. Read each matched file, verify each convergence criterion with file:line evidence
4. Check test coverage gaps:
   - If `task.test.unit` defined but no matching test files in changedFiles → mark as test gap
   - If `task.test.integration` defined but no integration test in changedFiles → mark as test gap
5. Build `reviewResult = { taskId, title, criteria_met[], criteria_unmet[], test_gaps[], files_reviewed[] }`

**Verdict logic**:
- PASS = all `convergence.criteria` met + no test gaps
- PARTIAL = some criteria met OR has test gaps
- FAIL = no criteria met

**CLI Convergence Review** (convergenceReviewTool === 'gemini' or 'codex'):

```javascript
const reviewId = `${sessionId}-convergence`
const taskCriteria = taskFiles.map(t => `${t.id}: [${(t.convergence?.criteria || []).join(' | ')}]`).join('\n')
Bash(`ccw cli -p "PURPOSE: Convergence verification — check each task's completion criteria against actual implementation
TASK: • For each task below, verify every convergence criterion is satisfied in the changed files • Mark each criterion as MET (with file:line evidence) or UNMET (with what's missing) • Identify test coverage gaps (planned tests not found in changes)

TASK CRITERIA:
${taskCriteria}

CHANGED FILES: ${changedFiles.join(', ')}

MODE: analysis
CONTEXT: @${sessionPath}/plan.json @${sessionPath}/.task/*.json @**/* | Memory: lite-execute completed
EXPECTED: Per-task verdict (PASS/PARTIAL/FAIL) with per-criterion evidence + test gap list
CONSTRAINTS: Read-only | Focus strictly on convergence criteria verification, NOT code quality (code review already done in lite-execute)" --tool ${convergenceReviewTool} --mode analysis --id ${reviewId}`, { run_in_background: true })
// STOP - wait for hook callback, then parse CLI output into reviewResults format
```

// TodoWrite: Phase 2 → completed, Phase 3 → in_progress

## TR-Phase 3: Run Tests & Generate Checklist

**Build checklist** from reviewResults:
- Per task: status = `PASS` (all criteria met) / `PARTIAL` (some met) / `FAIL` (none met)
- Collect test_items from `task.test.unit[]`, `task.test.integration[]`, `task.test.success_metrics[]` + review test_gaps

**Run tests** if `testConfig.command` exists:
- Execute with 5min timeout
- Parse output: detect passed/failed patterns → `overall: 'PASS' | 'FAIL' | 'UNKNOWN'`

**Write** `${sessionPath}/test-checklist.json`

// TodoWrite: Phase 3 → completed, Phase 4 → in_progress

## TR-Phase 4: Auto-Fix Failures (Iterative)

**Skip if**: `skipFix === true` OR `testChecklist.execution?.overall !== 'FAIL'`

**Max iterations**: 3. Each iteration:

1. Delegate to test-fix-agent:

```javascript
Agent({
  subagent_type: "test-fix-agent",
  run_in_background: false,
  description: `Fix tests (iter ${iteration})`,
  prompt: `## Test Fix Iteration ${iteration}/${MAX_ITERATIONS}

**Test Command**: ${testConfig.command}
**Framework**: ${testConfig.framework}
**Session**: ${sessionPath}

### Failing Output (last 3000 chars)
\`\`\`
${testChecklist.execution.raw_output}
\`\`\`

### Plan Context
**Summary**: ${plan.summary}
**Tasks**: ${taskFiles.map(t => `${t.id}: ${t.title}`).join(' | ')}

### Instructions
1. Analyze test failure output to identify root cause
2. Fix the SOURCE CODE (not tests) unless tests themselves are wrong
3. Run \`${testConfig.command}\` to verify fix
4. If fix introduces new failures, revert and try alternative approach
5. Return: what was fixed, which files changed, test result after fix`
})
```

2. Re-run `testConfig.command` → update `testChecklist.execution`
3. Write updated `test-checklist.json`
4. Break if tests pass; continue if still failing

If still failing after 3 iterations → log "Manual investigation needed"

// TodoWrite: Phase 4 → completed, Phase 5 → in_progress

## TR-Phase 5: Report & Sync

> **CHECKPOINT**: This step is MANDATORY. Always generate report and trigger sync.

**Generate `test-review.md`** with sections:
- Header: session, summary, timestamp, framework
- **Task Verdicts** table: task_id | status | convergence (met/total) | test_items | gaps
- **Unmet Criteria**: per-task checklist of unmet items
- **Test Gaps**: list of missing unit/integration tests
- **Test Execution**: command, result, fix iteration (if applicable)

**Write** `${sessionPath}/test-review.md`

**Chain to session:sync**:
```javascript
Skill({ skill: "workflow:session:sync", args: `-y "Test review: ${testChecklist.execution?.overall || 'no-test'} — ${plan.summary}"` })
```

// TodoWrite: Phase 5 → completed

**Display summary**: Per-task verdict with [PASS]/[PARTIAL]/[FAIL] icons, convergence ratio, overall test result.

## Data Structures

### testReviewContext (Input - Mode 1, set by lite-execute Step 5)

```javascript
{
  planObject: { /* same as executionContext.planObject */ },
  taskFiles: [{ id: string, path: string }],
  convergenceReviewTool: "skip" | "agent" | "gemini" | "codex",
  executionResults: [...],
  originalUserInput: string,
  session: {
    id: string,
    folder: string,
    artifacts: { plan: string, task_dir: string }
  }
}
```

### testChecklist (Output artifact)

```javascript
{
  session: string,
  plan_summary: string,
  generated_at: string,
  test_config: { command, framework, type },
  tasks: [{
    task_id: string,
    title: string,
    status: "PASS" | "PARTIAL" | "FAIL",
    convergence: { met: string[], unmet: string[] },
    test_items: [{ type: "unit"|"integration"|"metric", desc: string, status: "pending"|"missing" }]
  }],
  execution: {
    command: string,
    timestamp: string,
    raw_output: string,       // last 3000 chars
    overall: "PASS" | "FAIL" | "UNKNOWN",
    fix_iteration?: number
  } | null
}
```

## Session Folder Structure (after test-review)

```
.workflow/.lite-plan/{session-id}/
├── exploration-*.json
├── explorations-manifest.json
├── planning-context.md
├── plan.json
├── .task/TASK-*.json
├── test-checklist.json          # structured test results
└── test-review.md               # human-readable report
```

## Error Handling

| Error | Resolution |
|-------|------------|
| No session found | "No lite-plan sessions found. Run lite-plan first." |
| Missing plan.json | "Invalid session: missing plan.json at {path}" |
| No test framework | Skip TR-Phase 3 execution, still generate review report |
| Test timeout | Capture partial output, report as FAIL |
| Fix agent fails | Log iteration, continue to next or stop at max |
| Sync fails | Log warning, do not block report generation |
