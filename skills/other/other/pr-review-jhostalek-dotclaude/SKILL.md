---
name: pr-review
description: Use when reviewing a pull request, merge request, or local diff for correctness, security, and code quality.
argument-hint: [PR number, branch name, or local path]
---

target = $ARGUMENTS

If target is not provided, review the PR/MR of the current branch.
If target is a local path or branch name (not a PR/MR number), use `git diff` directly.

## Review Philosophy

Help the author ship better code — ask questions over directives, explain impact over citing rules, suggest concrete fixes. Gatekeeping tone erodes trust and misses the point.

## Review Dimensions

Beyond correctness, these dimensions catch real bugs that diffs hide:

**Security** — Trace user-controlled data from source to sink: string concatenation in queries, user input reaching command execution or file paths, hardcoded secrets, missing authorization on new endpoints, removed input validation. Source-to-sink flow without sanitization is CRITICAL.

**Breaking changes** — Modified signatures, removed exports, changed response shapes, new required fields, migrations without backward compatibility. The diff won't show broken callers — look for them.

**Performance** — Database queries inside loops (N+1), quadratic algorithms in hot paths, unbounded allocations, resource leaks, blocking operations in async contexts.

**Dependencies** — New dependencies: check license, maintenance status, known CVEs. Major version bumps may carry breaking API changes.

**Over-engineering** — LLM-generated code has a specific failure mode: unnecessary abstractions, helper functions used once, patterns for hypothetical flexibility. Flag explicitly — these are common and costly.

## Output

### Findings

Every CRITICAL and IMPORTANT finding includes *why it matters* and a *concrete fix suggestion*.

Number findings sequentially for easy reference.

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

Only submit a review to the platform if the user explicitly asks — default is local report only.
