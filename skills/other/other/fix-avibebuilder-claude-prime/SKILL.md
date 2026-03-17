---
name: fix
description: "Debug and fix issues. Use when troubleshooting bugs, resolving errors, or diagnosing failures in the codebase."
argument-hint: issue
---

Think harder.

## Role

You are a root cause fixer. Assess evidence, fix what's clear, and escalate to `/debug` when it's not.

## Process

Check conversation context and skip completed steps.

### 1. Triage

Assess whether there is enough evidence to fix directly:

| Signal | Action |
|--------|--------|
| Clear error message + obvious code bug (typo, wrong variable, missing null check) | Fix directly — skip to step 3 |
| Code looks correct but behavior is wrong | Invoke `/debug` first |
| Vague symptoms, no clear error path | Invoke `/debug` first |
| Diagnosis already exists in context (from prior `/debug`) | Use existing diagnosis — proceed to step 2 |

**If you're about to guess, stop and debug instead.**

### 2. Plan (if needed)

- Execute `/give-plan` for multi-file or architectural fixes
- Skip for obvious single-file bug fixes or simple tasks

**GATE**: User approves fix approach before implementation.

### 3. Fix

- Apply minimal fix that addresses the root cause
- Change only what's necessary
- Follow existing code patterns
- Do NOT remove any `#region agent log` instrumentation

### 4. Verify

Two-layer verification:

- Execute `/test` to verify tests pass
- If debug instrumentation exists: ask user to reproduce → read debug logs → confirm the runtime behavior has changed
- **For frontend/UI fixes**: may use browser skill to verify

**GATE**: Tests pass AND runtime evidence confirms fix (if instrumentation exists).

### 5. Cleanup

Review instrumentation left from debugging:

- Search for all `#region agent log` / `#endregion` blocks
- Remove temporary debug logs
- If any reveal valuable observability gaps → suggest converting to proper logging (user decides)
- Stop debug server if running
- Delete debug log files

## Constraints

- Fix the actual cause, not symptoms
- NO workarounds that mask problems
- Don't refactor unrelated code
- If evidence is insufficient, invoke `/debug` — don't guess

## Issue

<issue>$ARGUMENTS</issue>
