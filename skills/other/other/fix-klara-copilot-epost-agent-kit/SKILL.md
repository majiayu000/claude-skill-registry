---
name: fix
description: (ePost) Use when user says "fix", "broken", "error", "failing", "this doesn't work", or pastes an error message — identifies error type and applies platform-appropriate fix
user-invocable: true
metadata:
  argument-hint: "[issue description]"
---

# Fix — Unified Fix Command

Fix issues with automatic error type detection. Absorbs `:fast`, `:test`, `:types`, `:logs` into one auto-detecting command.

## Step 0 — Flag Override

If `$ARGUMENTS` starts with `--ci`: skip auto-detection, load `references/ci-mode.md` and execute. Remaining args are the issue description.
If `$ARGUMENTS` starts with `--deep`: skip auto-detection, load `references/deep-mode.md` and execute.
If `$ARGUMENTS` starts with `--ui`: skip auto-detection, load `references/ui-mode.md` and execute **inline** (main context — do NOT fork).
If `$ARGUMENTS` starts with `--a11y`: skip auto-detection, load `references/a11y-mode.md` and execute **inline** (main context — do NOT fork).
Otherwise: continue to Error Type Auto-Detection.

## Dispatch Routing

| Flag | Execution | Specialist |
|------|-----------|-----------|
| `--ui` | Inline in main context | Main context dispatches epost-muji via Agent tool |
| `--a11y` | Inline in main context | Main context dispatches epost-a11y-specialist via Agent tool |
| `--deep` | Dispatch to epost-debugger via Agent tool | epost-debugger runs deep investigation |
| `--ci` | Dispatch to epost-debugger via Agent tool | epost-debugger handles CI log analysis |
| _(auto-detect)_ | Dispatch to epost-debugger via Agent tool | epost-debugger handles general debugging |

## Aspect Files

| File | Purpose |
|------|---------|
| `references/deep-mode.md` | Systematic deep fix with full investigation |
| `references/ci-mode.md` | Fix CI pipeline failures |
| `references/ui-mode.md` | Fix UI component findings from known-findings DB | Loads fix/references/ui-mode.md | epost-muji |
| `references/a11y-mode.md` | Fix accessibility findings from known-findings.json |

## Error Type Auto-Detection

**Dispatch to epost-debugger via Agent tool** with the full issue context before proceeding. epost-debugger will handle detection, investigation, and fixing. The modes below are instructions for epost-debugger.

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

For cases where auto-detection isn't enough, use flags:
- `/fix --deep` — full systematic investigation with documentation
- `/fix --ci` — CI pipeline debugging (reads CI logs, reproduces locally)
- `/fix --ui` — UI component findings from `.epost-data/ui/known-findings.json` (delegates to epost-muji)
- `/fix --a11y` — accessibility findings from `.epost-data/a11y/known-findings.json`

<issue>$ARGUMENTS</issue>

**IMPORTANT:** Analyze the skills catalog and activate needed skills.
