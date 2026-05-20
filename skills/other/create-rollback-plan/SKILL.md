---
name: create-rollback-plan
description: Create a deployment rollback plan when the user asks to prepare a rollback strategy, plan for deployment failure, create a revert plan, or document rollback procedures for a release
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash, Write
argument-hint: "[version to deploy or deployment context]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: ops, rollback, safety
---

# Create Rollback Plan

## Overview

Create a comprehensive rollback plan for a deployment that covers trigger criteria, step-by-step procedures, data considerations, feature flag rollback, cache invalidation, communication protocols, and verification steps. A rollback plan must be written and tested before the deployment, not improvised during an incident.

## Workflow

1. **Read project context** — Check `.chalk/docs/engineering/` for:
   - Architecture and deployment topology docs (monolith vs. microservices, deploy targets, CDN setup)
   - Database migration patterns and tools
   - Feature flag infrastructure and current flag states
   - Previous rollback plans (to inherit project-specific procedures)
   - Release checklists for the current version
   - CI/CD pipeline configuration

2. **Understand the deployment** — From `$ARGUMENTS` and conversation:
   - What version is being deployed
   - What changes are included (features, migrations, config changes)
   - What is the deployment mechanism (blue-green, canary, rolling, big-bang)
   - What infrastructure is involved (servers, containers, serverless, CDN)
   - What database changes are included (if any)

3. **Identify rollback risks** — For this specific deployment:
   - Are there database migrations? Are they reversible?
   - Are there data format changes? Is old code compatible with new data?
   - Are there external API contract changes? Will consumers break?
   - Are there feature flags that can independently control new behavior?
   - Are there cache entries that will be stale after rollback?
   - Are there scheduled jobs or background workers affected?

4. **Define trigger criteria** — Specify concrete, measurable conditions that should trigger a rollback:
   - Error rate thresholds (absolute and relative to baseline)
   - Latency thresholds (P50, P95, P99)
   - Business metric thresholds (conversion rate, active users, revenue)
   - Critical flow failures (login, checkout, data persistence)
   - Manual trigger conditions (customer reports, support ticket spike)
   - Time-based triggers (if metrics do not stabilize within X minutes)

5. **Write the rollback procedure** — Step-by-step commands and actions:
   - Exact commands to execute the rollback (copy-pasteable)
   - Order of operations (which service first if multi-service)
   - Database rollback procedure (if migrations were run)
   - Feature flag changes (which flags to disable)
   - Cache and CDN invalidation steps
   - DNS or load balancer changes (if applicable)
   - Background job/worker considerations

6. **Document data considerations** — Critical for any deployment with data changes:
   - Can the migration be reversed without data loss?
   - Will data written by the new code be readable by the old code?
   - Are there irreversible data transformations?
   - What is the backup strategy and restore procedure?
   - How long does a data restore take?

7. **Write the communication plan** — Who to notify and when:
   - Engineering team (before rollback begins)
   - On-call engineer (if not already engaged)
   - Support team (to expect user reports)
   - Stakeholders (if user-visible impact exceeds threshold)
   - External consumers (if API changes are reverted)
   - Status page updates (if public-facing)

8. **Define verification steps** — How to confirm the rollback succeeded:
   - Health check endpoints to verify
   - Key user flows to test manually
   - Metrics to watch and expected values
   - Time to wait before declaring rollback complete
   - How to confirm no data corruption occurred

9. **Determine the next file number** — List files in `.chalk/docs/engineering/` matching `*_rollback_plan*`. Find the highest number and increment by 1.

10. **Write the plan** — Save to `.chalk/docs/engineering/<n>_rollback_plan_<version>.md`.

11. **Confirm** — Present the plan with key highlights: trigger criteria summary, estimated rollback time, and any risks that cannot be mitigated by rollback alone.

## Filename Convention

```
<number>_rollback_plan_<version>.md
```

Examples:
- `9_rollback_plan_v1_3_0.md`
- `15_rollback_plan_v2_0_0.md`

## Rollback Plan Format

```markdown
# Rollback Plan: <version>

Last updated: <YYYY-MM-DD>
**Deployment date**: <date or TBD>
**Rollback owner**: <name or role>
**Estimated rollback time**: <minutes>
**Risk level**: Low | Medium | High

## Deployment Summary

<1-2 sentences: what is being deployed, key changes, and why a rollback plan is needed.>

### Changes Included
- <Change 1: brief description and risk level>
- <Change 2: brief description and risk level>

### Rollback Complexity
| Factor | Assessment |
|--------|-----------|
| Database migrations | Reversible / Irreversible / None |
| Data format changes | Compatible / Incompatible / None |
| Feature flags available | Yes / Partial / No |
| External API changes | Breaking / Non-breaking / None |
| Multi-service coordination | Required / Not required |

## Trigger Criteria

### Automatic Rollback Triggers
Rollback should be initiated immediately if any of the following are observed:

| Metric | Baseline | Threshold | Monitoring Dashboard |
|--------|----------|-----------|---------------------|
| Error rate (5xx) | <X%> | > <Y%> for 5 min | <dashboard link> |
| P99 latency | <Xms> | > <Yms> for 5 min | <dashboard link> |
| <Critical flow> success rate | <X%> | < <Y%> for 3 min | <dashboard link> |

### Manual Rollback Triggers
Rollback should be considered if:
- Support reports > <n> tickets about <issue type> within <timeframe>
- <Critical business metric> drops below <threshold>
- On-call engineer observes <specific symptom>

### Decision Authority
- **Auto-trigger**: On-call engineer can initiate without approval
- **Manual trigger**: Requires sign-off from <role> during business hours, on-call engineer authority after hours

## Rollback Procedure

### Pre-Rollback (2 minutes)

1. **Announce** — Post in <channel>: "Initiating rollback of <version>. Reason: <trigger>. ETA: <minutes>."
2. **Snapshot current state** — Record current error rates, latency, and active user count for comparison.

### Step 1: Feature Flags (if applicable)

Disable the following feature flags immediately to reduce impact while the full rollback proceeds:

| Flag | Current State | Rollback State | Command |
|------|---------------|----------------|---------|
| `<flag_name>` | enabled | disabled | `<exact command>` |

### Step 2: Application Rollback

```bash
# Exact commands to roll back the application
<command to revert to previous version>
```

**For multi-service deployments**, roll back in this order:
1. <Service A> — `<command>` (depends on nothing)
2. <Service B> — `<command>` (depends on Service A)

### Step 3: Database Rollback (if applicable)

```bash
# Exact commands to reverse the migration
<migration rollback command>
```

**Pre-check before running**:
- [ ] Confirm no data written by new code is incompatible with old schema
- [ ] Confirm migration reversal does not drop columns containing user data
- [ ] Take a database snapshot before reversing: `<snapshot command>`

### Step 4: Cache and CDN Invalidation

```bash
# Invalidate stale cache entries
<cache invalidation command>
```

| Cache Layer | Action | Command |
|-------------|--------|---------|
| Application cache | Flush keys matching `<pattern>` | `<command>` |
| CDN | Purge paths: `<paths>` | `<command>` |
| Browser cache | Set `Cache-Control: no-cache` on affected endpoints | <config change> |

### Step 5: Verify Rollback

See Verification section below.

## Data Considerations

### Data Compatibility Matrix

| Data Type | New Format | Old Format Compatible? | Action on Rollback |
|-----------|-----------|----------------------|-------------------|
| <data type> | <new format> | Yes / No | <action needed> |

### Irreversible Changes

<List any data transformations that cannot be undone. For each:>
- **What**: <description of the irreversible change>
- **Impact**: <what happens if we rollback>
- **Mitigation**: <backup/restore procedure or manual fix>

### Backup and Restore

| Asset | Backup Method | Backup Location | Restore Time |
|-------|--------------|-----------------|-------------|
| Database | <method> | <location> | <estimated time> |
| File storage | <method> | <location> | <estimated time> |

## Communication Plan

### During Rollback

| When | Who | Channel | Message |
|------|-----|---------|---------|
| Rollback initiated | Engineering team | <channel> | "Rolling back <version>. Reason: <reason>. ETA: <time>." |
| Rollback in progress | On-call engineer | <channel> | Status updates every 5 minutes |
| Rollback complete | Engineering + Support | <channel> | "Rollback complete. <version_prev> is live. Monitoring for stability." |

### If User-Facing Impact

| When | Who | Channel | Message |
|------|-----|---------|---------|
| Impact confirmed | Support team | Support channels | <prepared message for users> |
| Resolution | Support team | Support channels | <prepared resolution message> |
| Post-incident | Stakeholders | Email | Incident summary with timeline |

## Verification

### Immediate Checks (first 5 minutes)

- [ ] Health check endpoints returning 200: `<curl command or URL>`
- [ ] Application version confirmed as previous: `<version check command>`
- [ ] Error rate returning to baseline: <dashboard link>
- [ ] P99 latency returning to baseline: <dashboard link>

### Functional Checks (next 15 minutes)

- [ ] <Critical user flow 1>: <how to test>
- [ ] <Critical user flow 2>: <how to test>
- [ ] <Critical user flow 3>: <how to test>

### Extended Monitoring (next 1-2 hours)

- [ ] Business metrics stable: <metrics and expected values>
- [ ] No new error patterns in logs: <log query>
- [ ] Background jobs processing normally: <how to verify>

### Rollback Complete Criteria

The rollback is declared complete when ALL of the following are true:
- Error rate is at or below pre-deployment baseline for 30 minutes
- All critical user flows verified working
- No new support tickets related to the deployment
- On-call engineer confirms system stability
```

## Anti-patterns

- **"Just revert the commit"** — Reverting code does not revert database migrations, cache state, feature flag changes, or data written by the new code. A rollback plan must address every layer of the system, not just the application code.
- **Not considering data migrations** — If the deployment includes a database migration that adds a column, reverting the code while leaving the new column is usually fine. But if it renames a column or changes data formats, the old code may break against the new schema. Always assess data compatibility.
- **No trigger criteria** — "We will roll back if something goes wrong" is not a plan. Define specific, measurable thresholds that trigger a rollback. Without them, the decision becomes a debate during an outage.
- **No verification step** — Rolling back and assuming it worked is dangerous. Define explicit checks that confirm the rollback succeeded: health endpoints, user flows, error rates, and business metrics.
- **Not testing the rollback** — A rollback plan that has never been tested is a hypothesis, not a plan. Test the rollback procedure on staging before the production deployment.
- **Missing communication plan** — Rolling back without notifying the team leads to confusion, duplicate debugging, and conflicting actions. Define who to notify, through which channel, and what to say.
- **Assuming rollback is instantaneous** — DNS propagation, cache expiration, client-side caching, and mobile app versions mean that some users will still see the new version after rollback. Account for this in the plan.
- **No data backup before migration** — If the migration is irreversible and something goes wrong, the only recovery is from a backup. Always take a backup before running migrations, and document the restore procedure with time estimates.
