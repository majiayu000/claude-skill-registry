---
name: agent-ops-baseline
description: "Create .agent/baseline.md and later compare against it. Use when capturing baseline build/lint/test results or investigating newly introduced findings."
category: core
invokes: [agent-ops-state, agent-ops-tasks]
invoked_by: [agent-ops-validation]
state_files:
  read: [constitution.md, focus.md]
  write: [baseline.md, focus.md]
---

# Baseline Workflow

## Preconditions
- `.agent/constitution.md` exists and commands are CONFIRMED.

## CLI Commands

**Works with or without `aoc` CLI installed.** Baseline operations use direct file editing by default.

### Build/Lint/Test Commands

Get commands from `.agent/constitution.md` — these vary by project:

```bash
# Example constitution commands (project-specific)
build: npm run build
lint: npm run lint
test: npm run test
format: npm run format
```

### Issue Discovery After Baseline (File-Based — Default)

When baseline findings need to be tracked as issues:

1. Increment `.agent/issues/.counter`
2. Append issues to appropriate `.agent/issues/{priority}.md` file
3. Use type `BUG` for failures, `CHORE` for warnings

### CLI Integration (when aoc is available)

When `aoc` CLI is detected in `.agent/tools.json`, these commands provide convenience shortcuts:

| Operation | CLI Command |
|-----------|-------------|
| Create issue from finding | `aoc issues create --type BUG --priority high --title "..."` |
| List existing issues | `aoc issues list --status open` |
| Show issue | `aoc issues show <ID>` |

## Baseline Capture (mandatory before code changes)

1) Run build/lint commands from constitution
2) Write to `.agent/baseline.md`:
   - commands executed
   - exit codes
   - warnings/errors grouped by file
3) Run unit tests command from constitution
4) Write to `.agent/baseline.md`:
   - command
   - summary (pass/fail/skip counts)
   - failure details (stack traces / logs)

## Issue Discovery After Baseline

**After capturing baseline, invoke `agent-ops-tasks` discovery procedure:**

1) Collect all findings from baseline:
   - Build errors → `BUG` (critical/high)
   - Test failures → `BUG` (high)
   - Lint errors → `BUG` (medium)
   - Lint warnings → `CHORE` (low/medium)
   - Missing test coverage → `TEST` (medium)
   - Security warnings → `SEC` (high)

2) Present to user:
   ```
   📋 Baseline captured. Found {N} existing issues:
   
   High:
   - [BUG] 2 failing tests in UserService
   - [SEC] 1 security warning (npm audit)
   
   Medium:
   - [BUG] 15 lint errors
   - [TEST] Coverage below threshold (72%)
   
   Low:
   - [CHORE] 23 lint warnings
   
   Create issues for these? [A]ll / [S]elect / [N]one / [D]efer
   ```

3) If user creates issues:
   - Offer to start fixing highest priority issue
   - After fixes, re-run baseline to capture cleaner state

4) If user defers:
   - Note in focus.md: "Baseline captured with {N} pre-existing issues"
   - Continue to next workflow step

## Baseline Comparison

Use this procedure when comparing current state to baseline (called by this skill or by critical-review):

### Input
- Current build/lint/test output
- `.agent/baseline.md` contents

### Comparison Procedure

1) **Run checks** using constitution commands:
   ```
   build → lint → tests
   ```

2) **Categorize each finding**:

   | Finding | In Baseline? | Category | Action |
   |---------|--------------|----------|--------|
   | Error | No | NEW_REGRESSION | **BLOCK** — must fix |
   | Error | Yes | PRE_EXISTING | Note, continue |
   | Warning | No | NEW_WARNING | Investigate |
   | Warning | Yes | PRE_EXISTING | Ignore |
   | Test fail | No | NEW_FAILURE | **BLOCK** — must fix |
   | Test fail | Yes | PRE_EXISTING | Note, continue |
   | Fewer issues | — | IMPROVEMENT | Note improvement |

3) **Output comparison report**:
   ```markdown
   ## Comparison vs Baseline

   ### New Issues (must address)
   - [list new errors/failures]

   ### New Warnings (investigate)
   - [list new warnings]

   ### Pre-existing (noted)
   - [count of baseline issues still present]

   ### Improvements
   - [any reductions from baseline]

   ### Verdict: PASS | FAIL | INVESTIGATE
   ```

4) **Decision rules**:
   - Any NEW_REGRESSION → FAIL (block until fixed)
   - Only NEW_WARNING → INVESTIGATE (document or fix)
   - No new issues → PASS

## Template
Start from [baseline template](./templates/baseline.template.md).
