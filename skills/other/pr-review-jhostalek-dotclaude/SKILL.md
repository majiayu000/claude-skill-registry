---
name: pr-review
description: Use when reviewing a pull request, merge request, or local diff for correctness, security, and code quality.
argument-hint: [PR number, branch name, or local path]
---

target = $ARGUMENTS

## Resolve the target

- Empty → PR/MR of the current branch.
- Number → that PR/MR on the current remote (use `gh` for GitHub, `glab` for GitLab).
- Branch name or local path → diff against its merge base.

Read the PR description, linked issues, and commit messages before the diff — a review grounded only in diff lines misses when code drifts from stated intent. Pull CI status too; a failing pipeline is load-bearing context.

## Stance

Frame feedback as questions and impact; the author decides the fix. A reviewer who cites rules instead of explaining consequences trains authors to work around the review rather than with it.

## Dimensions

Correctness is table stakes — the diff shows bugs directly. These dimensions catch what the diff hides:

**Security** — Trace user-controlled data from source to sink: SQL concatenation, input reaching command execution or file paths, hardcoded secrets, missing authorization on new endpoints, removed or weakened validation. Source-to-sink flow without sanitization is CRITICAL regardless of perceived exploitability.

**Breaking changes** — Modified signatures, removed exports, changed response shapes, new required fields, migrations without backward compatibility. Grep for callers of changed symbols — the diff cannot show consumers it doesn't touch.

**Performance** — N+1 queries, quadratic algorithms in hot paths, unbounded allocations, resource leaks, blocking operations in async contexts.

**Dependencies** — New dependencies: license, maintenance status, known CVEs. Major version bumps may carry breaking API changes — read the changelog; version number alone is not evidence.

**Tests** — Critical paths covered (auth, data integrity, payments), boundaries and failure paths exercised, assertions test outcomes not implementation. Missing tests for new branches are a gap; snapshot-only tests for logic-heavy code are usually a gap disguised as coverage.

**Over-engineering** — LLM-generated code has a specific failure mode: unnecessary abstractions, helpers used once, patterns for hypothetical flexibility, premature configurability. Flag explicitly — common, costly, reviewers underweight them.

## Severity

- **CRITICAL** — security exposure, data loss or corruption, breaking change without migration, crash on normal input. Blocks merge.
- **IMPORTANT** — correctness bug on uncommon paths, performance regression in a hot path, missing test for a critical branch, contract drift callers will hit.
- **SUGGESTION** — clarity, naming, or structural wins. Author can defer.
- **QUESTION** — intent or context unclear; author clarification needed before severity can be assigned.

## Output

### Findings

Every CRITICAL and IMPORTANT finding includes *why it matters* and a *concrete fix suggestion*.

```
1. [CRITICAL] file:line — Title
   Why: impact explanation
   Fix: concrete code or approach

2. [IMPORTANT] file:line — Title
   Why: impact explanation
   Fix: concrete code or approach

3. [SUGGESTION] file:line — Title
   Fix: brief recommendation

4. [QUESTION] file:line — Title
   Clarification needed.
```

### Summary

| Area | Status |
|------|--------|
| CI | passing / failing / not run |
| Scope | clean / needs split |
| Correctness | clean / N issues |
| Security | clean / N issues |
| Breaking changes | none / N risks |
| Performance | clean / N issues |
| Tests | adequate / gaps noted |

### Verdict

- Any CRITICAL → **REQUEST_CHANGES**
- Only IMPORTANT/SUGGESTION/QUESTION → **APPROVE** (with comments)
- Clean → **APPROVE**

## Submitting

Default is local report only. Post to the platform only when the user explicitly asks.
