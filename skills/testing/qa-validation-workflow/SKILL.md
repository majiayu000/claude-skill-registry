---
name: qa-validation-workflow
description: Full validation workflow for QA agent. Runs automated checks (type-check, lint, test, build) and browser testing with E2E tests. Use when validating implementation after code review.
category: validation
---

# Validation Workflow Skill

> "Trust but verify – automated tests catch regressions, browser tests catch reality."

## When to Use This Skill

Use when:

- `currentTask.status === "ready_for_qa"`
- Developer has committed changes
- Ready to validate implementation

---

## MANDATORY: Worktree Verification (CRITICAL - FIRST STEP)

**⚠️ CRITICAL: You MUST validate from the CORRECT worktree where the code was implemented!**

### Step 1: Determine Which Worktree to Validate

**Check the task's `agent` field to know which worktree contains the code:**

| Task Agent | Worktree Path            | Branch Name           | Command to Navigate         |
| ---------- | ------------------------ | --------------------- | --------------------------- |
| developer  | `../developer-worktree`  | `developer-worktree`  | `cd ../developer-worktree`  |
| techartist | `../techartist-worktree` | `techartist-worktree` | `cd ../techartist-worktree` |
| qa         | `.` (current directory)  | `main`                | Stay in current directory   |

**⚠️ NEVER validate from main if the task was implemented in a worktree!**

### Step 2: Navigate and Verify (MANDATORY - DO NOT SKIP)

```bash
# 1. CHECK current location BEFORE doing anything
pwd
git branch --show-current

# 2. Navigate to the CORRECT worktree based on task.agent
# If task.agent == "developer":
cd ../developer-worktree

# If task.agent == "techartist":
cd ../techartist-worktree

# If task.agent == "qa":
# Stay in current directory (no cd needed)

# 3. VERIFY you're in the RIGHT place (MANDATORY CHECK)
pwd
git branch --show-current
# This MUST show the expected worktree branch!

# 4. ONLY THEN proceed with validation steps below
```

### Step 3: If You Ran Tests in Wrong Worktree

**Stop immediately and report the error:**

1. The validation results are INVALID
2. Send message to PM: "ERROR: Validated wrong worktree. Re-running..."
3. Navigate to correct worktree
4. Re-run ALL validation steps

**Remember: QA validates the agent's worktree, NOT main (unless task.agent = "qa")**

---

## Quick Start

```bash
# Run full validation suite
npm run type-check && npm run lint && npm run build && npm run test && npm run test:e2e
```

---

## Validation Pipeline

```
      [GATE: E2E tests MUST exist - CREATE if missing]
                  │
                  ▼
┌─────────────┐    ┌──────────┐    ┌──────────────┐    ┌──────────┐
│ Type Check  │───▶│   Lint   │───▶│ TEST CHECK   │───▶│  Build   │
│    (tsc)    │    │ (eslint) │    │  (Coverage)  │    │  (vite)  │
└─────────────┘    └──────────┘    └──────────────┘    └──────────┘
       │                │                   │                  │
       ▼                ▼                   ▼                  ▼
   Pass/Fail       Pass/Fail          Tests Missing?      Pass/Fail
       │                │                   │                  │
       │                │            ┌──────┴──────┐          │
       │                │            │             │          │
       │                │         Create Tests   CANNOT PASS  │
       │                │            │          WITHOUT TEST  │
       │                │            │             │          │
       │                └────────────┴─────────────┘          │
       │                                                      │
       └──────────────────────────────────────────────────────┘
                                          │
                                          ▼
                              ┌─────────────────────┐
                              │  E2E TEST EXECUTION │ ◄── MANDATORY GATE
                              │  (npm run test:e2e)  │     NO EXCEPTIONS
                              └─────────────────────┘
                                          │
                              ┌──────────┴──────────┐
                              │                     │
                         PASS                   FAIL
                          │                        │
                          ▼                        ▼
                    Update PRD            Fix either the code or the test, following test plan.
```

**⚠️ MANDATORY RULE: If Unit/E2E tests don't exist, CREATE THEM before validation can pass.**

## **DO NOT mark validation as PASSED without Unit/ E2E tests covering the task acceptance criteria.**

## Progressive Guide

### Test Coverage Check (BEFORE Automated Checks)

1. **Load qa-test-creation skill**

   ```bash
   Skill("qa-test-creation")
   ```

2. **Identify modified source files**

   ```bash
   # Get files changed in this task
   git diff --name-only HEAD~5 | grep '^src/'
   # Or read from task context in current-task-qa.json
   ```

3. **For EACH modified source file, check test coverage:**

   **Unit Test Check:**
   - Source: `src/components/game/player/index.ts`
   - Test must exist: `src/tests/components/game/player/index.test.ts`
   - If missing: **BLOCK** - invoke test-creator

   **E2E Test Check:**
   - Check if `tests/e2e/{feature}-suite.spec.ts` exists
   - Example: `tests/e2e/gameplay-suite.spec.ts`, `tests/e2e/ui-suite.spec.ts`
   - If missing: **BLOCK** - invoke test-creator

4. **COVERAGE VERIFICATION TABLE** (Must pass ALL rows):

   | Check Type       | Pattern                                         | Status | Action             |
   | ---------------- | ----------------------------------------------- | ------ | ------------------ |
   | Unit test exists | `src/tests/**/*.test.ts` for each `src/**/*.ts` | ✅/❌  | If ❌: BLOCK       |
   | E2E test exists  | `tests/e2e/*-suite.spec.ts`                     | ✅/❌  | If ❌: BLOCK       |
   | Tests run        | `npm run test` passes                           | ✅/❌  | If ❌: Report bugs |
   | E2E tests run    | `npm run test:e2e` passes                       | ✅/❌  | If ❌: Report bugs |

### Acceptance Criteria Verification

For each acceptance criterion in `current-task-qa.json` (acceptanceCriteria array):

```markdown
## Acceptance Criteria Verification

### Criterion 1: "Vehicle responds to WASD input"

- **Test**: Pressed W, A, S, D keys
- **Result**: ✅ PASS / ❌ FAIL
- **Notes**: Vehicle moves forward, left, backward, right correctly

### Criterion 2: "Physics simulation runs at 60Hz"

- **Test**: Checked physics debug panel
- **Result**: ✅ PASS / ❌ FAIL
- **Notes**: Physics running at target rate
```

## Anti-Patterns

❌ **DON'T:**

- Use Playwright MCP directly for validation
- Assume automated tests are sufficient
- Mark as passed without running E2E tests
- Ignore console warnings/errors

✅ **DO:**

- Always run E2E tests for validation
- Verify each acceptance criterion via test output
- Review test screenshots as evidence
- Document any concerns in bug notes
- Check console for errors in test output
