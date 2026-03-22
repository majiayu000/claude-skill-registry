---
name: pmtl-automation-smoke-suite
description: PMTL_VN automation skill for repeatable smoke and monitoring commands. Use when the task needs to run repo-backed smoke tests, monitoring drills, or Telegram alert checks through a stable wrapper instead of ad hoc shell typing.
---

# PMTL Automation Smoke Suite

## Purpose

Provide stable wrapper-based smoke and monitoring commands so PMTL checks run through a repeatable entrypoint instead of ad hoc shell typing.

## Use When

- The command itself is the task, such as smoke, monitoring, or Telegram alert verification.
- You need a quick verification companion after code or config changes.
- You want a repo-approved wrapper instead of reconstructing commands manually.

## Required Inputs

- target suite: `smoke`, `monitoring`, or `telegram`
- whether the suite is the main task or only one verification step
- any known runtime prerequisite such as Docker stack or local credentials

## Expected Output

- A structured success/failure result from the repo wrapper.
- Clear knowledge of which suite was actually exercised and what that suite is meant to prove.

## Supported suites

- `smoke`
- `monitoring`
- `telegram`

## What each suite should prove

- `smoke`
  - the main app surfaces boot and the core smoke flow still completes
- `monitoring`
  - monitoring or observability drill entrypoints still run without obvious failure
- `telegram`
  - Telegram or alert-notification wiring still responds through the repo-backed test path

## Execution Approach

1. Pick the narrowest suite that matches the current verification need.
2. Run the wrapper rather than rebuilding the command manually.
3. Read the JSON result instead of assuming a shell exit code tells the whole story.
4. If the suite is too coarse for the changed surface, say so and add targeted checks.

## Script

Primary entrypoint: `py infra/tools/codex_actions.py smoke-suite ...`

Compatibility wrapper: `scripts/run_smoke_suite.py`

```bash
py infra/tools/codex_actions.py smoke-suite --suite smoke
py infra/tools/codex_actions.py smoke-suite --suite monitoring
```

## Verification

- Confirm the selected suite matches the surface that changed.
- Read emitted JSON and stderr, not just the command exit code.
- If a suite fails because runtime prerequisites are missing, report that explicitly instead of calling the app broken.

## Quality Criteria

- The chosen suite is minimal but relevant.
- Wrapper output is interpreted correctly and not inflated into a broader claim than it supports.
- Smoke verification stays tied to the touched area, not generic confidence theater.

## Edge Cases

- `smoke` is broader than many narrow changes and can miss contract-specific drift.
- `monitoring` or `telegram` failures can reflect missing local credentials or environment setup rather than product regression.
- This skill does not replace area-specific verification lanes like auth or search verification.

## References

- `infra/tools/codex_actions.py`
- `docs/runbooks.md`
- `docs/troubleshooting.md`

## Pair with

- `pmtl-verify-quality-gate` after meaningful code changes.
- `pmtl-runbook-docker-dev-recovery` when the wrapper failure is actually a Docker/dev-stack incident.
