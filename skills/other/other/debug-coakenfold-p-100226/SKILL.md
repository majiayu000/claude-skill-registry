---
name: debug
description: "Systematic debugging workflow: reproduce, isolate, fix, verify"
argument-hint: "[issue-description-or-error]"
allowed-tools: "Read, Edit, Write, Glob, Grep, Bash, Task"
---

# Debugging Workflow

> PROSE constraints: **Reduced Scope** (narrow the problem systematically) +
> **Progressive Disclosure** (gather context incrementally).

## Phase 1: Understand the Problem

1. Parse `$ARGUMENTS` for error messages, stack traces, or symptom descriptions
2. Search the codebase for relevant code paths
3. Read related test files to understand expected behavior

## Phase 2: Reproduce

1. Identify a minimal reproduction path
2. Run relevant tests to confirm the failure: `npm test -- [relevant-test]`
3. If no test exists, create one that demonstrates the bug

## Phase 3: Isolate

1. Trace the execution path from symptom to root cause
2. Check recent changes: `git log --oneline -20`
3. Narrow scope — identify the single function or condition causing the issue
4. State the root cause clearly before proceeding

## Validation Gate

**STOP**: Present the root cause analysis and proposed fix. Wait for confirmation.

## Phase 4: Fix

1. Make the minimal change that fixes the root cause
2. Don't refactor surrounding code — fix the bug only
3. Update or add a test that would have caught this bug

## Phase 5: Verify

1. Run the failing test to confirm it passes: `npm test -- [test-file]`
2. Run the full test suite to check for regressions: `npm test`
3. Run the linter: `npm run lint`

## Output Summary

```markdown
## Bug Fix: [title]

### Root Cause
[What was wrong and why]

### Fix
[What was changed]

### Files Modified
- [file] — [change description]

### Verification
- [test] — passes
- Full suite — no regressions
```
