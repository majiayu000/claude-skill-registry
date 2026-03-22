---
name: pmtl-production-baseline
description: PMTL_VN production-grade coding and runtime baseline. Use when implementing or refactoring features that need repo-specific defaults for logging, validation, security posture, caching, monitoring, deployment boundaries, and documentation sync.
---

# PMTL Production Baseline

## Purpose

Provide the non-negotiable PMTL repo defaults for production-grade implementation, runtime safety, validation, logging, and documentation sync.

## Use When

- Implementing or refactoring features that affect real runtime behavior.
- Changing logging, env contracts, validation, caching, or request boundaries.
- You need the default PMTL baseline before applying narrower skills.
- The task spans multiple apps or modules and needs one shared runtime policy anchor before deeper specialization.

## Required Inputs

- touched app/package/module
- relevant owner docs or design files for the changed runtime rule
- expected verification scope

## Expected Output

- Code and docs that follow the same repo-wide production baseline.
- No silent runtime policy drift across apps, packages, and docs.

## Read first

1. Read `AGENTS.md`.
2. Read `docs/architecture/conventions.md`.
3. Read `docs/architecture/skills-taxonomy.md` when changing AI workflow or skill routing.
4. Read `docs/runbooks.md` and `docs/troubleshooting.md` when the task touches monitoring or recovery.

## Execution Approach

1. Confirm the touched layer and keep logic in the correct package or app boundary.
2. Validate user input and env contracts before changing runtime behavior.
3. Add or preserve structured logging at real operational boundaries.
4. Update docs and skill routing in the same task when rules change.
5. Hand off to narrower PMTL skills when the task becomes mostly frontend behavior, auth verification, search verification, or incident recovery.

## Baseline rules

- Preserve monorepo boundaries from `pmtl-vn-architecture`.
- Validate user input and env contracts with Zod.
- Log operational failures with structured context using pino.
- Keep Vietnamese text fully accented in UI, API messages, and seeded content.
- Keep Next.js request-boundary logic in `apps/web/src/proxy.ts` unless official versioned guidance proves otherwise.
- Prefer `"use cache"` helpers and data-layer caching over page-level cache flags.
- Do not leave runtime rule changes undocumented. Update `AGENTS.md`, local skills, and affected docs together.

## Verification

- Re-read the touched docs and confirm the rule still matches code.
- Pair with `pmtl-verify-quality-gate` after meaningful edits.
- If auth or search contracts changed, pair with the dedicated verification skill for that area.

## Quality Criteria

- Runtime policy stays aligned across docs, code, and skill routing.
- Boundary ownership remains explicit; no logic leaks into the wrong app or package.
- Rule changes are documented in the same task instead of becoming tribal knowledge.

## Edge Cases

- Older audit notes can conflict with current repo reality; prefer verified 2026 docs.
- Convenience fixes in one app can accidentally break monorepo boundaries or request ownership.

## References

- `docs/architecture/conventions.md`
- `docs/architecture/skills-taxonomy.md`
- `docs/runbooks.md`
- `docs/troubleshooting.md`

## Use this skill with

- `pmtl-fe-implementation` for frontend code changes.
- `pmtl-ui-behavior` and `pmtl-ui-style-system` for UI work.
- `pmtl-verify-quality-gate` after meaningful edits.
- `pmtl-runbook-docker-dev-recovery` when the task is a local/dev incident.
