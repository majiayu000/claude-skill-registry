---
name: release-engineering
description: Plan and verify software releases with versioning, changelogs, release branches, feature flags, canaries, migration gates, rollback, deployment checks, and release readiness. Use when preparing a release, shipping a risky PR, coordinating app/backend/database rollout, recovering from a bad deploy, or defining release policy for a repo.
---

# Release Engineering

## Purpose

Use this skill to turn "ready to merge" into a controlled release. It connects code, data, config, deployment, monitoring, and rollback.

## Release Classification

Classify the release before choosing gates:

| Type | Extra Gates |
|---|---|
| Patch fix | focused regression test, rollback proof |
| Feature release | feature flag, docs/changelog, product acceptance |
| API or SDK change | versioning, deprecation, compatibility tests |
| Database migration | `data-contract-migrations`, backup, backfill, recovery |
| Config or secret change | `config-secrets-environments`, rotation, drift check |
| Infrastructure change | canary, health checks, capacity and rollback |

## Release Plan

For non-trivial releases, require:

1. Version or release identifier.
2. Changelog entries grouped by user impact.
3. Build artifacts and provenance.
4. Migration and config gates.
5. Canary or staged rollout plan.
6. Monitoring dashboard and alert expectations.
7. Rollback or roll-forward command.
8. Owner, decision time, and abort criteria.

## Verification

Use fresh commands from the current session. Typical gates:

```bash
git status --short
git log --oneline -n 5
# project-specific build/test command
# migration dry run or validation query
# deployment health check
```

Do not claim a release shipped unless remote git, CI, artifact, and runtime state have each been checked at the required level.

## Output Shape

```text
release_scope:
version_or_identifier:
included_changes:
excluded_changes:
pre_release_checks:
rollout_steps:
migration_and_config_gates:
monitoring:
rollback_or_recovery:
go_no_go_status:
```
