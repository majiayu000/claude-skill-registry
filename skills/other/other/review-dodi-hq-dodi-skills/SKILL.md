---
name: review
description: Use after implementation is complete and before creating a PR — agent-driven code review checking spec compliance, code quality, security, and regression risk
---

# Review

Comprehensive agent-driven code review. Run after implementation, before PR.

## What to Check

| Category | What to Look For |
|----------|------------------|
| **Spec compliance** | Does the code implement what was specified? Nothing missing, nothing extra |
| **Code quality** | Clean, idiomatic, follows project conventions (CLAUDE.md, style guides) |
| **Security** | Injection, auth bypass, data leaks, OWASP top 10 |
| **Regression risk** | Does this change break assumptions in callers/consumers? |
| **Error handling** | Silent failures, swallowed exceptions, missing edge cases |
| **API contracts** | If touching APIs — are request/response shapes backwards-compatible? |

## Process

1. Identify the spec/plan and the diff (`git diff <base>...HEAD`)
2. Dispatch review subagent (see review-prompt.md) with:
   - The spec/plan path
   - The diff or list of changed files
   - Project conventions (CLAUDE.md path)
3. If issues found: fix them, re-run review
4. When approved: proceed to `dodi-dev:submit`

## Don't Skip This

"Tests pass" is not a review. Tests verify behavior; review verifies intent, quality, and risk.
