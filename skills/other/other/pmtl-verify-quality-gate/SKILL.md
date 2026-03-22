---
name: pmtl-verify-quality-gate
description: PMTL_VN verification skill for code quality gates. Use after meaningful changes to run the strongest relevant checks, usually targeted tests, typecheck, lint, and build-oriented validation, instead of relying on manual confidence.
---

# PMTL Verify Quality Gate

## Purpose

Run the strongest relevant checks after implementation so delivery is backed by evidence instead of confidence.

## Use When

- Any meaningful code change is considered done.
- You need a deterministic verification path for web, CMS, or repo-wide edits.

## Required Inputs

- touched scope: `web`, `cms`, or `all`
- whether tests may be skipped for a narrowly justified reason
- whether narrower domain verifiers are also required

## Expected Output

- Command results that show what passed, what failed, and which runtime was used.

## Default order

1. Targeted tests for touched areas.
2. Typecheck for the affected package or the monorepo.
3. Lint for the affected package or the monorepo.
4. Build or smoke verification when contracts changed.

## Execution Approach

1. Choose the narrowest scope that still proves the change.
2. Run the quality gate through the repo wrapper instead of ad hoc commands.
3. Escalate to smoke or domain-specific verification when contracts changed.

## Script

Primary entrypoint: `py infra/tools/codex_actions.py quality-gate ...`

Compatibility wrapper: `scripts/run_quality_gate.py`

Example:

```bash
py infra/tools/codex_actions.py quality-gate --scope all
py infra/tools/codex_actions.py quality-gate --scope web --skip-tests
```

## Verification

- Treat non-zero exit codes as a failed gate.
- Include the real command output summary in the final report, not only "tests passed".

## Quality Criteria

- Verification scope is as narrow as possible without becoming misleading.
- Final reporting includes the actual executed scope and runtime.
- Quality gate is not used as a substitute for auth/search/domain-specific verification when those lanes changed.

## Edge Cases

- Legacy `cms` naming still exists in the helper even though forward architecture is `apps/api`; call that out plainly when relevant.
- A passing quality gate does not prove runtime health, auth correctness, or search freshness by itself.
- Local environment issues can break a gate independently of the code change; distinguish infra failure from code failure.

## References

- `infra/tools/codex_actions.py`
- `scripts/run_quality_gate.py`
