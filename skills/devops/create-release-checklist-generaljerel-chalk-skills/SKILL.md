---
name: create-release-checklist
description: Generate a comprehensive release checklist when the user asks to prepare a release, create a release plan, or ship a version
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash, Write
argument-hint: "[version number, e.g., v1.2.0]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: release, checklist, deployment
---

# Create Release Checklist

## Overview

Generate a structured, actionable release checklist that covers the full deployment lifecycle from code freeze to post-deploy verification. The output is a markdown file with checkboxes and owner assignments saved to `.chalk/docs/engineering/`.

## Workflow

1. **Read project context** — Check for `.chalk/docs/engineering/` files to understand:
   - Architecture and deployment topology (monolith vs. microservices, deploy targets)
   - Existing monitoring and alerting setup
   - Database migration patterns
   - Feature flag infrastructure
   - Previous release checklists (to inherit any project-specific items)
   - CI/CD pipeline configuration

2. **Determine the version** — From `$ARGUMENTS`:
   - If a version is provided, use it
   - If not, check `package.json`, `pyproject.toml`, `Cargo.toml`, or equivalent for the current version and suggest the next one based on the changes (semver)
   - Run `git log --oneline <last-tag>..HEAD` to understand what is being released

3. **Analyze the release scope** — Categorize the changes since the last release:
   - Run `git log --oneline <last-tag>..HEAD` to list all commits
   - Identify: new features, bugfixes, breaking changes, dependency updates, migrations
   - Flag high-risk changes: database migrations, API contract changes, new external integrations, auth changes
   - Check for any open PRs that should be included or excluded

4. **Generate the checklist** — Build the checklist using the template in the Output section. Customize it based on:
   - The project's tech stack (skip irrelevant sections)
   - The risk level of the release (more gates for riskier releases)
   - The project's deployment infrastructure (Kubernetes, serverless, bare metal, etc.)
   - Whether this is a major, minor, or patch release

5. **Find the next file number** — Read filenames in `.chalk/docs/engineering/` to find the highest numbered file. The next number is `highest + 1`.

6. **Write the checklist** — Save to `.chalk/docs/engineering/<n>_release_checklist_<version>.md` where `<version>` uses underscores instead of dots (e.g., `v1_2_0`).

7. **Confirm** — Tell the user the checklist was created with its path. Highlight any high-risk items that need extra attention.

## Output

The checklist file follows this structure:

```markdown
# Release Checklist: <version>

Last updated: <YYYY-MM-DD> (initial creation)

**Release date**: <target date or TBD>
**Release manager**: <assign or TBD>
**Risk level**: Low | Medium | High
**Summary**: <1-2 sentences describing what this release contains>

## Changes in This Release

<!-- Auto-generated from git log -->
- <commit summaries grouped by type: features, fixes, chores>

## Pre-Release

### Code Freeze
- [ ] Feature branch merged to release branch — **Owner: TBD**
- [ ] All PRs for this release are merged — **Owner: TBD**
- [ ] No open blockers in the issue tracker — **Owner: TBD**
- [ ] Version number bumped in source files — **Owner: TBD**
- [ ] Changelog updated with user-facing changes — **Owner: TBD**

### Dependency Audit
- [ ] `npm audit` / `pip audit` / equivalent shows no critical vulnerabilities — **Owner: TBD**
- [ ] All new dependencies reviewed for license compatibility — **Owner: TBD**
- [ ] Lock file is committed and up to date — **Owner: TBD**

### Migration Review
- [ ] Database migrations tested on a copy of production data — **Owner: TBD**
- [ ] Migrations are backward-compatible (can roll back without data loss) — **Owner: TBD**
- [ ] Migration execution time estimated for production data volume — **Owner: TBD**
- [ ] Data backups scheduled before migration runs — **Owner: TBD**

## Testing

### Staging Deployment
- [ ] Deployed to staging environment successfully — **Owner: TBD**
- [ ] Staging environment matches production configuration — **Owner: TBD**
- [ ] Environment variables and secrets configured — **Owner: TBD**

### Test Execution
- [ ] Full test suite passes in CI — **Owner: TBD**
- [ ] Smoke tests pass on staging — **Owner: TBD**
- [ ] Regression test suite passes — **Owner: TBD**
- [ ] Performance baseline measured (response times, memory, CPU) — **Owner: TBD**
- [ ] Load testing completed if this release changes hot paths — **Owner: TBD**

### Manual Verification
- [ ] Critical user flows tested end-to-end on staging — **Owner: TBD**
- [ ] New features verified against acceptance criteria — **Owner: TBD**
- [ ] UI changes verified across supported browsers/devices — **Owner: TBD**
- [ ] Accessibility audit for UI changes — **Owner: TBD**

## Deploy

### Feature Flags
- [ ] New feature flags configured with correct default states — **Owner: TBD**
- [ ] Feature flag rollout plan documented (percentage ramp, timeline) — **Owner: TBD**
- [ ] Kill switch verified for high-risk features — **Owner: TBD**

### Monitoring
- [ ] Monitoring dashboards updated for new features — **Owner: TBD**
- [ ] Alerting thresholds reviewed and adjusted — **Owner: TBD**
- [ ] Error rate baseline recorded pre-deploy — **Owner: TBD**
- [ ] Key business metrics baseline recorded pre-deploy — **Owner: TBD**

### Deployment Execution
- [ ] Deploy window communicated to the team — **Owner: TBD**
- [ ] Deploy executed (canary -> percentage rollout -> full) — **Owner: TBD**
- [ ] Health checks passing on all instances — **Owner: TBD**
- [ ] Error rates stable within normal thresholds — **Owner: TBD**
- [ ] Response times within acceptable range — **Owner: TBD**
- [ ] Smoke tests pass on production — **Owner: TBD**

## Rollback

### Trigger Criteria
Define the conditions under which you will roll back:
- Error rate exceeds <X>% (baseline + threshold)
- P99 latency exceeds <X>ms
- Critical user flow failure (login, checkout, etc.)
- Data integrity issue detected

### Rollback Procedure
- [ ] Rollback command documented and tested: `<command>` — **Owner: TBD**
- [ ] Database rollback procedure documented (if migrations were run) — **Owner: TBD**
- [ ] Feature flags can be disabled independently of code rollback — **Owner: TBD**
- [ ] Rollback does not require data migration reversal — **Owner: TBD**
- [ ] Rollback verified on staging before production deploy — **Owner: TBD**

### Data Considerations
- [ ] Data written by new code is compatible with old code after rollback — **Owner: TBD**
- [ ] No irreversible data transformations in this release — **Owner: TBD**
- [ ] Cache invalidation plan for rollback scenario — **Owner: TBD**

## Communication

### Internal
- [ ] Engineering team notified of deploy window — **Owner: TBD**
- [ ] Support team briefed on new features and known issues — **Owner: TBD**
- [ ] Support documentation updated with new feature guides — **Owner: TBD**
- [ ] On-call engineer identified for the deploy window — **Owner: TBD**

### External
- [ ] Release notes drafted for users — **Owner: TBD**
- [ ] API changelog updated if public API changed — **Owner: TBD**
- [ ] Migration guide written if breaking changes affect consumers — **Owner: TBD**
- [ ] Status page updated if maintenance window needed — **Owner: TBD**

## Post-Deploy Verification

- [ ] Monitor error rates for 1 hour post-deploy — **Owner: TBD**
- [ ] Verify key metrics are stable (conversion rate, active users, etc.) — **Owner: TBD**
- [ ] Confirm feature flag rollout proceeding as planned — **Owner: TBD**
- [ ] Collect initial user feedback if applicable — **Owner: TBD**
- [ ] Schedule post-mortem if any issues occurred — **Owner: TBD**
- [ ] Tag the release in git: `git tag -a <version> -m "Release <version>"` — **Owner: TBD**
```

## Customization by Risk Level

### Low Risk (patch release, minor bugfixes)
- Migration Review section can be skipped if no schema changes
- Load testing is optional
- Canary deploy can be shortened or skipped
- Rollback section is still required but can be simplified

### Medium Risk (minor release, new features)
- Full checklist applies
- Feature flag section is mandatory for new features
- Manual verification required for all new user flows

### High Risk (major release, breaking changes, large migrations)
- All sections are mandatory with no shortcuts
- Add a "War Room" section: who is on-call, communication channel, escalation path
- Require sign-off from at least two engineers before deploy
- Extend post-deploy monitoring to 24 hours
- Schedule a dry-run deploy to staging with production-like traffic

## Day-of-Week Guidance

- **Monday-Wednesday**: Preferred deploy days. Full team available for monitoring.
- **Thursday**: Acceptable for low-risk releases only. Ensure Friday coverage.
- **Friday**: Do not deploy unless it is a critical hotfix with a rollback plan already tested. The team will not be at full capacity if issues arise over the weekend.
- **Weekends/Holidays**: Emergency hotfixes only. Require explicit approval and on-call staffing.

## Anti-patterns

- **Skipping staging** — "It works on my machine" is not a deployment strategy. Every release goes through staging, no exceptions.
- **No rollback plan** — If you cannot describe how to undo this release in under 5 minutes, you are not ready to ship it.
- **Untested migrations** — Running a migration on production for the first time is reckless. Test on a copy of production data, measure execution time, and have a reversal plan.
- **Deploying on Friday** — Unless it is a critical hotfix, wait until Monday. Weekend incidents with a skeleton crew lead to extended outages and burnout.
- **Not notifying support** — Support teams field user complaints. If they do not know what changed, they cannot help users, and they will escalate everything to engineering.
- **No monitoring for new features** — If you ship a feature without a dashboard or alerts, you will not know it is broken until users tell you. Instrument first, ship second.
- **Big-bang deploys** — Ship behind feature flags and ramp gradually. A 1% rollout that catches a bug saves 99% of your users from experiencing it.
- **Skipping the post-deploy check** — "It deployed successfully" is not the same as "it works in production." Verify user flows, check error rates, and watch metrics for at least an hour.
- **Undocumented rollback** — "We will figure it out if we need to" is not a rollback plan. Write down the exact commands and test them before you need them.
