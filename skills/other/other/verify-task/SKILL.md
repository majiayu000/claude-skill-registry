---
name: verify-task
description: Run code-verification on a specific task. Use to verify a single task's acceptance criteria after implementation.
argument-hint: [task-id]
allowed-tools: Read, Edit, Bash, Grep, Glob, AskUserQuestion
---

Verify Task $1 from EXECUTION_PLAN.md using the code verification workflow.

## Context Detection

Determine working context:

1. If current working directory matches pattern `*/features/*`:
   - PROJECT_ROOT = parent of parent of CWD (e.g., `/project/features/foo` → `/project`)
   - MODE = "feature"

2. Otherwise:
   - PROJECT_ROOT = current working directory
   - MODE = "greenfield"

## Directory Guard (Wrong Directory Check)

Before starting, confirm `EXECUTION_PLAN.md` exists in the current working directory.

- If it does not exist, **STOP** and tell the user to `cd` into their project/feature directory (the one containing `EXECUTION_PLAN.md`) and re-run `/verify-task $1`.

## Task Context

1. Read Task $1 definition from EXECUTION_PLAN.md
2. Extract all acceptance criteria
3. Read `.claude/verification-config.json` from PROJECT_ROOT if it exists

If the config is missing or required commands are empty:
- Run `/configure-verification`
- Note the missing config in the report if verification cannot proceed

## Verification Workflow

Copy this checklist and track progress:

```
Verify Task Progress:
- [ ] Step 1: Parse criteria from task
- [ ] Step 2: Pre-flight check (testability)
- [ ] Step 3: TDD compliance check
- [ ] Step 4: Test quality gate (optional)
- [ ] Step 5: Verify each criterion
- [ ] Step 6: Handle exit conditions
- [ ] Step 7: Generate report
- [ ] Step 8: Log to verification-log.jsonl
```

Follow the code-verification workflow (inline, no sub-agents):

### Step 1: Parse Criteria

For each acceptance criterion, create a verification item:

| Field | Value |
|-------|-------|
| ID | `V-001`, `V-002`, etc. |
| Criterion | The acceptance criterion text |
| Type | `CODE`, `TEST`, `LINT`, `TYPE`, `BUILD`, `SECURITY`, `BROWSER:*`, `MANUAL`, or `MANUAL:DEFER` |
| Verify | The `Verify:` method (test name, command, route/selector, etc.) |
| Evidence | Where evidence will be stored (log, screenshot, or output path) |
| Files | Which files to examine |

If a criterion is missing a type or `Verify:` line:
- Infer the most likely type and verification method
- Update EXECUTION_PLAN.md to add the missing metadata
- If ambiguous, ask the human to confirm before proceeding

### Step 2: Pre-flight Check

Confirm each criterion is testable:
- Clear pass/fail criteria
- Required files exist
- Verification command available (from .claude/verification-config.json)

Flag untestable criteria immediately.

**Browser Tool Availability Check (SOFT BLOCK):**

If any criteria are type `BROWSER:*`:

1. Check tool availability (fallback chain):
   - ExecuteAutomation Playwright → Browser MCP → Microsoft Playwright → Chrome DevTools

2. **If at least one tool available:** Continue to verification.

3. **If NO browser tools available:**
   - Display warning:
     ```
     ⚠️  BROWSER VERIFICATION BLOCKED

     Task $1 has {N} browser-based acceptance criteria but no browser
     MCP tools are available.

     Browser criteria:
     - {list each BROWSER:* criterion}

     Options:
     1. Continue anyway (browser criteria become manual verification)
     2. Stop and configure browser tools first
     ```
   - Use AskUserQuestion to let user choose:
     - "Continue with manual verification" → Mark browser criteria as MANUAL, proceed
     - "Stop to configure tools" → Halt verification, provide setup instructions

---

### Step 3: TDD Compliance Check (Separate from Verification)

> This step evaluates development process quality, not functional correctness.
> TDD failures are informational — they don't block task completion.

Verify that Test-Driven Development was followed:

1. **Test existence check** — For each acceptance criterion:
   - Locate the corresponding test(s)
   - Record test file and test name
   - If no test exists → FAIL with "Missing test for criterion"

2. **Test-first check** (if git history available):
   ```bash
   # Check if test file was committed before/with implementation
   git log --oneline --follow -- "path/to/test/file"
   git log --oneline --follow -- "path/to/impl/file"
   ```
   - Tests committed before or same commit as implementation → PASS
   - Tests committed after implementation → WARNING (note in report)
   - Unable to determine → SKIP (note in report)

3. **Test effectiveness check** — For each test:
   - Test should fail if implementation is broken/removed
   - Test name should describe expected behavior
   - Test should have meaningful assertions (not just "no errors")

**TDD Compliance Report:**
```
TDD COMPLIANCE: Task $1
-----------------------
Tests Found: X/Y criteria covered
Test-First: PASS | WARNING | UNABLE TO VERIFY
Issues:
- [Criterion] Missing test
- [Criterion] Test added after implementation
- [Criterion] Test has no meaningful assertions
```

If tests are missing for any criterion, stop and write tests before proceeding.

**If test runner is unavailable or not configured:**
- Check `verification-config.json` for `testCommand`
- If no test command: report "No test runner configured — TDD compliance cannot be assessed"
- Mark TDD check as SKIPPED (not FAIL)
- Suggest: Run `/configure-verification` to set up test commands

### Step 4: Test Quality Gate (Optional)

This step checks whether tests are *meaningful*, not just present.

If `.claude/verification-config.json` includes `commands.mutation_test`, ask
whether to run it for this task. If yes, prefer a scoped run (changed files or
specific test paths). If mutation tests fail, mark the test-quality gate as
FAIL and stop for fixes.

Otherwise, run this lightweight checklist and record PASS/WARNING:

- Each acceptance criterion has at least one assertion that checks behavior
- At least one non-happy-path or boundary case is covered when applicable
- Tests verify state changes or outputs (not just "does not throw")
- External dependencies are mocked; code under test is not

If any criterion lacks assertions or only smoke-tests behavior, mark the
test-quality gate as FAIL and stop to improve tests.

### Step 5: Verify Each Criterion

For each criterion:

1. **Check** if the criterion is met
2. **Record** the result:
   ```
   VERIFICATION: [V-001]
   ---------------------
   Status: PASS | FAIL | BLOCKED
   Location: [file:line or "N/A"]
   Finding: [What was found]
   Expected: [What was expected]
   Suggested Fix: [If FAIL]
   ```
3. **If FAIL**: Attempt fix, then re-verify (up to 5 attempts)
4. **Track attempts** to avoid repeating failed fixes

Verification method by type:
- **TEST**: Use config `commands.test`. If `Verify:` includes a test name or file
  path, run a focused test command if the test runner supports it; otherwise run
  the full test suite and note the limitation.
- **LINT**: Use config `commands.lint`.
- **TYPE**: Use config `commands.typecheck`.
- **BUILD**: Use config `commands.build`.
- **SECURITY**: Run `/security-scan` (or equivalent for config if defined).
- **CODE**: Inspect the file, export, or command indicated by `Verify:`.
- **BROWSER:*:** Use the browser-verification skill with route/selector details.
- **MANUAL / MANUAL:DEFER**: Attempt automation using the auto-verify skill:
  1. Invoke auto-verify skill with criterion text and available tools
  2. If PASS: Mark as verified (automated), record method used
  3. If FAIL: Show error and suggested fix, mark as manual with context
  4. If TRULY_MANUAL and tagged `MANUAL:DEFER`:
     Enqueue to deferred review queue (`.claude/deferred-reviews.json`).
     Task continues — this does NOT block. Mark checkbox with `— Deferred: {key}`.
  5. If TRULY_MANUAL and tagged `MANUAL` (blocking):
     List in report for human review with reason

  Report format for attempted automation:
  ```
  [V-XXX] MANUAL → AUTOMATED
  Method: {tool} ({pattern detected})
  Result: PASS | FAIL
  Duration: {ms}
  ```

### Step 6: Exit Conditions

Stop verification loop when:
- PASS: Criterion met
- 5 attempts exhausted: Mark failed
- Same failure 3+ times: Flag for human review

### Step 7: Report

```
TASK VERIFICATION: $1
=====================

TDD Compliance:
- Tests Found: X/Y criteria covered
- Test-First: PASS | WARNING | UNABLE TO VERIFY

Test Quality Gate:
- Status: PASS | WARNING | FAIL | SKIPPED
- Mutation Tests: PASSED | FAILED | SKIPPED

Criteria Verification:
- Total: N
- Passed: X
- Failed: Y
- Skipped: Z

Details:
[V-001] PASS — Criterion summary
[V-002] FAIL — Criterion summary
  - Attempts: 3
  - Blocker: Description

TDD Issues (if any):
- [Criterion] {issue description}
```

### Step 8: Verification Log

Append a JSON line to `.claude/verification-log.jsonl` for each criterion:
```json
{
  "timestamp": "{ISO timestamp}",
  "scope": "task",
  "task_id": "$1",
  "criterion_id": "V-001",
  "type": "TEST",
  "status": "PASS",
  "evidence": ".claude/verification/task-$1.md"
}
```

Ensure `.claude/verification/` exists before writing evidence files.

## On Success

- Check off completed criteria in EXECUTION_PLAN.md: `- [ ]` → `- [x]`
- Update `.claude/phase-state.json` task entry, including per-criterion results:
  ```json
  {
    "tasks": {
      "$1": {
        "status": "COMPLETE",
        "completed_at": "{ISO timestamp}",
        "verification": {
          "passed": true,
          "criteria_met": "X/X",
          "tdd_compliant": true,
          "criteria": {
            "V-001": {"status": "PASS", "type": "TEST", "evidence": "..."},
            "V-002": {"status": "PASS", "type": "CODE", "evidence": "..."}
          }
        }
      }
    }
  }
  ```
- **Verify state update:** Read back the updated entry to confirm the write succeeded:
  ```bash
  jq ".tasks[\"$1\"].status" .claude/phase-state.json
  ```
  If the read-back doesn't show `"COMPLETE"`, report the write failure and retry once.
- Write an evidence report to `.claude/verification/task-$1.md`
- Append a record to `.claude/verification-log.jsonl`
- Report: Task $1 verified, all criteria met

## On Failure

- Report which criteria failed
- Provide fix recommendations
- Do not check off incomplete criteria
- Update `.claude/phase-state.json` task entry and note failed criteria:
  ```json
  {
    "tasks": {
      "$1": {
        "status": "IN_PROGRESS",
        "verification": {
          "passed": false,
          "criteria_met": "X/Y",
          "last_attempt": "{ISO timestamp}",
          "attempts": N,
          "failing_criteria": ["V-001", "V-003"]
        }
      }
    }
  }
  ```
