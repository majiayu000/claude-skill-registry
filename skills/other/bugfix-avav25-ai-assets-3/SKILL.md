---
name: bugfix
description: End-to-end bugfix workflow that gathers evidence, identifies the affected stack, fixes the root cause, adds regression coverage, and verifies the result.
---

# Bugfix

Investigate, fix, and verify a defect with minimal blast radius.

## 1. Capture the Bug

Record:

- Expected behavior
- Actual behavior
- Reproduction steps
- Environment
- Severity

## 2. Analyze the Environment

Choose the appropriate path:

- Local environment -> `analyze-local`
- Production environment -> `analyze-prod`
- Code-only issue -> proceed directly to code investigation

## 3. Detect the Affected Stack

Read:

1. Root `AGENTS.md`
2. Relevant scoped `AGENTS.md`
3. Service configs and stack traces

Identify the primary implementation area:

- Frontend
- Java backend
- Python backend
- DevOps or infrastructure
- Database
- ML or data
- Cross-cutting shared logic

## 4. Gather Evidence

Collect:

- Error output
- Logs
- Reproduction details
- Scope of impact
- Suspected code path
- Any recent changes likely related

## 5. Prepare a Root-Cause Fix Plan

Include:

- Root cause
- Files to change
- Regression tests to add
- Risks

## 6. Implement

Fix the cause, not the symptom.

Rules:

- Keep changes focused
- Follow local project conventions
- Add regression coverage
- Avoid unrelated refactors

## 7. Verify

Confirm:

- The bug no longer reproduces
- New regression tests pass
- Relevant existing tests still pass
- No unrelated files changed

## 8. Report

Summarize:

- Root cause
- Files changed
- Tests added or updated
- Verification performed
- Remaining risks