---
name: ci-operations
description: Maintain CI reliability, required status checks, and build matrix health.
---

# CI Operations

## Purpose
Maintain CI reliability, required status checks, and build matrix health.

## When to Use
- CI failures on `main` or active PRs
- Monthly review of workflows and runner versions
- Dependabot updates affecting GitHub Actions

## Steps
1. Monitor workflow runs and identify failures or flaky tests.
2. Investigate root causes and fix or re-run as needed.
3. Update workflow dependencies and runner versions when required.
4. Confirm required checks for `main` are enforced.

## Output Contract
- CI passes on `main` and for active PRs.
- Workflow dependencies are current and stable.
- Required status checks remain enforced.

## References
- `.github/workflows/*` for pipeline definitions.
- `MAINTENANCE.md` for command-level procedures.
