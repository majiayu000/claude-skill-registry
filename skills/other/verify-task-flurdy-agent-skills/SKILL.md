---
name: verify-task
description: "Verify that a task's implementation meets its requirements and has adequate test coverage (happy path, sad path, edge cases). Use before /complete-task."
allowed-tools: "Read,Bash(bd:*),Bash(make:*),Bash(npm:*),Bash(npx:*),Bash(git:*),Grep,Glob,AskUserQuestion"
version: "1.0.0"
author: "flurdy"
---

# Verify Task

Check that an implementation fulfills its task requirements and that tests adequately cover the changes.

## When to Use

- After finishing implementation, before committing
- When unsure if test coverage is sufficient
- As a quality gate before `/complete-task`
- When reviewing your own work for completeness

## Usage

```
/verify-task              # Auto-detect in-progress bead
/verify-task <bead-id>    # Verify against a specific bead
```

## Instructions

### 1. Identify the Task

```bash
# If bead ID provided, use it directly
bd show <bead-id>

# Otherwise, find the in-progress bead
bd list --status=in_progress
```

If multiple beads are in progress, ask the user which one to verify.

### 2. Gather Context

Collect the full picture of what changed and what was required:

```bash
# Read the bead requirements
bd show <bead-id>

# See what files changed
git status
git diff
git diff --cached
```

Read the bead description carefully. Extract:

- **Explicit requirements** — what the bead says to do
- **Implicit requirements** — obvious behaviors that follow from the description (e.g., a "delete" feature implies confirmation, error handling)
- **Type of change** — feature, bug fix, refactor, config, docs, chore

### 3. Verify Requirements Are Met

Read each changed file. Compare the implementation against the requirements.

**Check:**

- [ ] Every explicit requirement from the bead is addressed
- [ ] The implementation is functionally correct (logic, data flow)
- [ ] No partial implementations left behind (TODOs, placeholder code)
- [ ] Changes are scoped to the task (no unrelated modifications)

If requirements are not met, report what's missing and stop.

### 4. Assess Test Needs

Not every task needs new tests. Determine the test obligation:

| Change Type | Tests Needed? | Examples |
|------------|---------------|----------|
| New feature / component | Yes — always | New screen, new utility, new hook |
| Bug fix | Yes — regression test | Fix parsing error, fix state bug |
| Behavior change | Yes — updated tests | Change validation rules, modify flow |
| Refactor (same behavior) | Maybe — verify existing tests still pass | Rename, extract function, restructure |
| Config / build change | Rarely | Update Makefile, tsconfig, deps |
| Docs / comments only | No | README, JSDoc, inline comments |
| Styling / UI-only | Rarely | Colors, spacing, layout tweaks |
| Translation / i18n strings | No | Adding locale keys |

If the change clearly doesn't need tests (config, docs, translations, pure styling), skip to step 6. State why tests are not needed.

### 5. Verify Test Coverage

If tests are needed, check that they exist and are adequate.

#### 5a. Find Related Tests

Locate test files for the changed source files:

```bash
# For a changed file like src/utils/foo.ts, look for:
#   src/utils/__tests__/foo.test.ts
#   src/utils/__tests__/foo.test.tsx
```

Follow the project's test co-location convention (`__tests__/` directories alongside source).

#### 5b. Read the Tests

Read each relevant test file. Evaluate coverage across these dimensions:

**Happy path** — Does the test verify the feature works correctly under normal conditions?

- Valid inputs produce expected outputs
- Main use case is exercised
- State changes are verified (if applicable)

**Sad path / error handling** — Does the test verify behavior when things go wrong?

- Invalid inputs are handled (empty strings, nulls, wrong types)
- Error states are tested (network failure, missing data, permission denied)
- Error messages or fallback behavior is verified

**Edge cases** — Does the test cover boundary and unusual conditions?

- Empty collections, single-item collections
- Boundary values (zero, negative, max int, very long strings)
- Concurrent or duplicate operations
- Platform-specific behavior (web vs. native, if applicable)

**Regression** (for bug fixes) — Is there a test that specifically reproduces the bug?

- The test should fail without the fix and pass with it
- The test should cover the exact scenario that caused the bug

#### 5c. Rate Coverage

Rate the test coverage for each changed module:

| Rating | Meaning | Action |
|--------|---------|--------|
| Sufficient | Happy + sad + relevant edge cases covered | Proceed |
| Partial | Happy path covered but missing sad/edge cases | List gaps |
| Missing | No tests for new/changed behavior | List what's needed |

#### 5d. Report Gaps

If coverage is partial or missing, report specifically what tests are needed. Be concrete:

```
Missing tests for src/utils/dateParser.ts:
- Sad path: parseDatesFromText with malformed date string "2025-13-45"
- Edge case: parseDatesFromText with empty string input
- Edge case: parseDatesFromText with multiple dates in one string
```

Do NOT write the tests yourself — report the gaps and let the user (or a follow-up step) decide how to proceed.

### 6. Run Existing Tests

```bash
make test
```

All tests must pass. If tests fail:

- Determine if the failure is caused by the current changes or is pre-existing
- Report the failure with context
- Do not proceed until the user acknowledges

### 7. Report

Provide a structured verification report:

```
## Verification Report: <bead-id> — <title>

### Requirements: ✅ Met | ❌ Not met
- [x] Requirement 1 — addressed in src/foo.ts
- [x] Requirement 2 — addressed in src/bar.ts
- [ ] Requirement 3 — NOT addressed (explain)

### Test Coverage: ✅ Sufficient | ⚠️ Gaps found | ⏭️ Not needed
- src/utils/foo.ts: ✅ Happy + sad + edge cases covered
- src/components/Bar.tsx: ⚠️ Missing sad path for error state
- src/i18n/locales/en.json: ⏭️ Translation — no tests needed

### Tests: ✅ All passing | ❌ Failures
- X tests passed, Y failed

### Verdict: ✅ Ready to commit | ❌ Needs work
```

If the verdict is "Needs work", list concrete next steps.

## Handling Edge Cases

- **No in-progress beads**: Ask user what task to verify against, or verify uncommitted changes without a bead
- **No code changes**: Inform user there's nothing to verify
- **Test infrastructure missing**: If the project has no test framework configured, note it and skip test steps
- **Large change set**: Focus verification on the most critical/complex files first; summarize simpler changes
- **Bead has no description**: Use the title and infer intent; ask user to clarify if ambiguous

## Rules

- Never write code or tests — this skill only verifies and reports
- Never modify files — read-only analysis
- Be specific about gaps — "needs more tests" is not helpful; name the exact scenarios
- Do not block on cosmetic issues — focus on functional correctness and test coverage
- If unsure whether a test gap matters, mention it but don't flag it as blocking
