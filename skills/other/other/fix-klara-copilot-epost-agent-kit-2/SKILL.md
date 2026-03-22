---
name: fix
description: "(ePost) Fix issues — auto-detects error type and platform"
user-invokable: true
context: fork
agent: epost-debugger
metadata:
  argument-hint: "[issue description]"
  connections:
    conflicts: [fix-deep]
    enhances: [fix-deep, fix-ci, fix-ui]
---

# Fix — Unified Fix Command

Fix issues with automatic error type detection. Absorbs `:fast`, `:test`, `:types`, `:logs` into one auto-detecting command.

## Error Type Auto-Detection

Before fixing, detect the error type from context:

### 1. TypeScript Errors (formerly types subcommand)
**Detection:** Web platform detected AND `tsconfig.json` exists
**Action:** Run `tsc --noEmit` → fix all type errors → repeat until clean (zero errors)
**Rules:** NEVER use `any` type. Use proper narrowing, generics, utility types. No `@ts-ignore`.

### 2. Test Failures (formerly test subcommand → use `/fix-deep` for systematic)
**Detection:** User mentions "test" OR recent test runner output shows "FAIL"/"ERROR"
**Action:** Run test suite → analyze failures → fix production code (not tests) → re-run until green
**Rules:** Do NOT comment out or skip tests. Do NOT change assertions. Fix root causes.

### 3. Log-Based (formerly logs subcommand)
**Detection:** User provides log file path OR `./logs.txt` exists
**Action:** Read log file → grep errors (last 30 lines) → locate in codebase → fix → verify logs clean
**Rules:** Fix ALL logged errors, not just the first one. Set up log piping if missing.

### 4. Quick Fix (default mode, formerly fast subcommand)
**Detection:** None of the above matched
**Action:** Quick diagnosis → minimal correct change → verify (typecheck, tests, build) → add regression test
**Rules:** Fix root causes, not symptoms. Keep changes minimal.

## Platform Detection

Same as `/cook` — detect from changed files or `$ARGUMENTS` platform hint.

## Explicit Overrides

For cases where auto-detection isn't enough, users can still use:
- `/fix-deep` — full systematic investigation with documentation
- `/fix-ci` — CI pipeline debugging (reads CI logs, reproduces locally)
- `/fix-ui` — visual/layout issues (CSS, a11y check, cross-browser)
- `/fix-a11y` — accessibility findings from `.epost-data/a11y/known-findings.json`

<issue>$ARGUMENTS</issue>

**IMPORTANT:** Analyze the skills catalog and activate needed skills.
