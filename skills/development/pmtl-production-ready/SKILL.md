---
name: pmtl-production-ready
description: PMTL_VN production-ready operating skill. Use for implementation, debugging, hardening, monitoring, deployment-impacting changes, or release-minded code review. This is the high-agency umbrella skill for turning PMTL work into production-safe work with explicit verification and documented recovery paths.
---

# PMTL Production Ready

Legacy umbrella skill. Do not use by default when the canonical taxonomy skills already cover the task.

Use this skill when the task is bigger than a local code tweak and has production implications.

## Operating model

This skill is not just a reminder list. It decides which lane to follow:

- implementation lane
- incident/debug lane
- release gate lane
- hardening lane

Run `scripts/select_playbook.py --task "<user task>"` when the right lane is not obvious.

## Read only what applies

- For implementation and refactor work: `references/implementation-lane.md`
- For runtime failures and regressions: `references/incident-lane.md`
- For final checks before merge, deploy, or “done”: `references/release-gate.md`

## Non-negotiables

- Keep logging structured with pino at real boundaries.
- Validate user input and env contracts with Zod.
- Preserve monorepo boundaries and NestJS module pattern (module + controller + service + dto + entities).
- Treat verification as part of delivery, not an optional extra.
- Update docs, skills, and project rules together when conventions change.

## Pair with

- `pmtl-production-baseline` for baseline repo rules
- `pmtl-verify-quality-gate` after meaningful edits
- `pmtl-verify-auth-flow` and `pmtl-verify-search-sync` for domain-specific checks
- `pmtl-runbook-docker-dev-recovery` when the task is Docker/infra incident-oriented
