---
name: prd-v08-release-planning
description: >
  Define release criteria, deployment environments, and rollback strategies during PRD v0.8 Deployment & Ops.
  Triggers on requests to plan releases, define deployment criteria, or when user asks "how do we deploy?",
  "release criteria", "deployment plan", "rollback strategy", "go-live checklist".
  Outputs DEP- entries with deployment steps and release criteria.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash

execution_modes:
  default: standard
  supports: [quick, standard, deep]
---

# Release Planning

Position in workflow: v0.7 Implementation Loop → **v0.8 Release Planning** → v0.8 Runbook Creation

## Execution Mode

Default is **standard**. See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md) for selection logic.

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | Staging→prod only; 3–5 release criteria; one rollback trigger |
| **standard** | Dev/staging/preview/prod environments; full criteria checklist; multiple rollback triggers; post-deploy validation |
| **deep** | Full environments + IaC review + canary/blue-green strategy + risk-weighted criteria + post-mortem hooks |

## Consumes

This skill requires prior work from v0.7 Implementation Loop and v0.6-v0.9:

- **EPIC-\* completed entries** (from v0.7 Implementation Loop) — Finished work packages define what's being released; must have State=Complete, all TEST- passing
- **TEST-\* test entries** (from v0.7 Test Planning) — All TEST- must pass in staging before release criteria can be met
- **API-\* endpoint contracts** (referenced in EPIC Context & IDs) — Define SLA and performance baselines for release criteria
- **ENV-\* environment specifications** (from v0.6 Environment Setup) — Local/CI/CD/production configurations inform DEP- entries for each environment
- **ARC-\* architecture decisions** (from v0.6 Architecture Design) — System structure (monolith, microservices, deployment topology) drives environment setup
- **TECH-\* technology stack** (from v0.5 Technical Stack Selection) — Technology choices inform infrastructure requirements and deployment tooling
- **RISK-\* high-priority entries** (from v0.5 Risk Discovery) — High RISK- must be mitigated or explicitly accepted before release
- **KPI-\* metrics** (from v0.3 and v0.9) — Target KPI values inform monitoring baselines and rollback thresholds

This skill assumes v0.7 Implementation is complete with all EPIC- entries marked Complete and all TEST- passing.

## Produces

This skill creates/updates:

- **DEP-\* entries** (deployment specifications, environment/criteria/rollback/validation types) — Release readiness checklist with environment configs, go/no-go criteria, rollback triggers and thresholds, post-deploy validation steps
- **Release readiness checklist** — Pre-deploy validation matrix showing which DEP- criteria must be met before release proceeds
- **Rollback decision tree** — Mapping of DEP- rollback triggers to execution procedures and escalation paths (feeds v0.8 Runbook Creation)

All DEP- entries are **operational contracts**, not confidence-based. They are:
- **Environment-specific** (each environment from staging to production has defined configuration)
- **Verifiable** (each criterion has a concrete check or metric threshold)
- **Enforceable** (release stops if DEP- criteria not met)
- **Traceable** (each DEP- links to EPIC-, TEST-, API-, KPI- that validate it)

Example DEP- entries:
```markdown
DEP-001: Production Environment Configuration
Type: Environment
Stage: Pre-deploy

Description: AWS production environment setup for application
Name: production
Infrastructure: AWS us-east-1, ECS Fargate, RDS PostgreSQL
Configuration:
  - NODE_ENV=production
  - LOG_LEVEL=info
  - RATE_LIMIT=100/min
  - METRICS_COLLECTION=enabled
Secrets: AWS Secrets Manager, rotated monthly
Access: DevOps team (deploy), On-call (read-only access)

Linked IDs: ARC-001 (monolith structure), TECH-005 (AWS)

---

DEP-002: All Tests Pass in Staging
Type: Criteria
Stage: Pre-deploy

Description: Complete test suite must pass in staging environment before production release
Requirement: All TEST- entries pass with >95% success rate, including smoke tests and E2E tests
Verification: CI/CD pipeline reports green; test report generated and reviewed
Blocker: Yes — Release cannot proceed if this fails
Owner: QA Lead

Linked IDs: TEST-001 to TEST-050 (from EPIC-01 through EPIC-07)

---

DEP-003: Error Rate Rollback Trigger
Type: Rollback
Stage: Post-deploy

Description: Automatic rollback if error rate exceeds baseline post-deployment
Trigger: 5xx error rate exceeds pre-deployment baseline
Threshold: >2% of requests for 5 minutes (currently 0.5% baseline from MON-001)
Procedure:
  1. Alert on-call engineer (PagerDuty)
  2. Pause traffic to new version
  3. Revert to pre-deploy git tag
  4. Investigate root cause
Notification: #incidents Slack, PagerDuty, Engineering Lead

Linked IDs: MON-001 (error rate metric), RUN-002 (rollback procedure), API-001–020 (endpoints affected)

---

DEP-004: Post-Deployment Smoke Tests
Type: Validation
Stage: Post-deploy

Description: Automated smoke tests to verify critical user journeys work post-deployment
Check: All critical UJ- (UJ-000, UJ-001, UJ-005, UJ-010) complete successfully
Method: Automated (tests/e2e/smoke.spec.ts) + manual spot-check
Success Criteria: All journeys complete <2 seconds, no auth failures, data persists
Escalation: If smoke tests fail, execute DEP-003 rollback and investigate

Linked IDs: UJ-000/001/005/010 (critical journeys), TEST-050 (E2E suite)
```

## Core Concept: Release as Contract

> A release is not "code that works locally." It is a **contract** between development and operations—a formal handoff that includes everything needed to deploy, validate, and recover.

## Release Components

| Component | Purpose | Output |
|-----------|---------|--------|
| **Deployment Environment** | Where code runs | DEP- (environment config) |
| **Release Criteria** | What must be true to deploy | DEP- (checklist) |
| **Rollback Triggers** | When to revert | DEP- (conditions) |
| **Validation Steps** | How to verify success | DEP- (post-deploy checks) |

## Execution

1. **Inventory completed EPICs**
   - Which EPIC- entries are "Complete"?
   - What API-, DBT-, FEA- are included in this release?

2. **Define deployment environments**
   - Staging, Production, Preview
   - Environment-specific configurations
   - Secrets management approach

3. **Establish release criteria**
   - All TEST- pass in staging
   - Performance baselines met (from MON-)
   - No critical RISK- blockers
   - Security review complete

4. **Define rollback triggers**
   - Error rate thresholds
   - Latency thresholds
   - User-reported critical issues
   - Data integrity concerns

5. **Document validation steps**
   - Post-deployment smoke tests
   - Key journey verification (UJ-)
   - Metric baseline confirmation

6. **Create DEP- entries** with full traceability

## DEP- Output Template

```
DEP-XXX: [Deployment Item Title]
Type: [Environment | Criteria | Rollback | Validation | Step]
Stage: [Pre-deploy | Deploy | Post-deploy | Rollback]

Description: [What this deployment item covers]

For Environment Type:
  Name: [staging | production | preview]
  Infrastructure: [Cloud provider, region, resources]
  Configuration: [Environment-specific settings]
  Secrets: [How secrets are managed]
  Access: [Who can deploy, who can access]

For Criteria Type:
  Requirement: [What must be true]
  Verification: [How to check this]
  Blocker: [Yes | No] — Does failure block deploy?
  Owner: [Who verifies]

For Rollback Type:
  Trigger: [What condition initiates rollback]
  Threshold: [Specific metric or condition]
  Procedure: [How to execute rollback]
  Notification: [Who to alert]

For Validation Type:
  Check: [What to verify post-deploy]
  Method: [Manual | Automated | Both]
  Success Criteria: [Expected result]
  Escalation: [What if validation fails]

Linked IDs: [EPIC-XXX, API-XXX, TEST-XXX related]
```

**Example DEP- entries:**

```
DEP-001: Production Environment Configuration
Type: Environment
Stage: Pre-deploy

Description: AWS production environment setup for main application

Name: production
Infrastructure: AWS us-east-1, ECS Fargate, RDS PostgreSQL
Configuration:
  - NODE_ENV=production
  - LOG_LEVEL=info
  - RATE_LIMIT=100/min
Secrets: AWS Secrets Manager, rotated monthly
Access: DevOps team (deploy), On-call (read-only)

Linked IDs: ARC-001, TECH-005
```

```
DEP-002: All Tests Pass in Staging
Type: Criteria
Stage: Pre-deploy

Description: Complete test suite must pass in staging environment

Requirement: All TEST- entries pass with >95% success rate
Verification: CI/CD pipeline green status, test report review
Blocker: Yes
Owner: QA Lead

Linked IDs: TEST-001 to TEST-050
```

```
DEP-003: Error Rate Rollback Trigger
Type: Rollback
Stage: Post-deploy

Description: Automatic rollback if error rate exceeds threshold

Trigger: 5xx error rate exceeds baseline
Threshold: >2% of requests for 5 minutes
Procedure:
  1. Alert on-call engineer
  2. Pause traffic to new version (if canary)
  3. Revert to previous known-good version
  4. Investigate root cause
Notification: #incidents Slack, PagerDuty

Linked IDs: MON-001, RUN-005
```

## Environment Progression

| Stage | Environment | Purpose | Gate |
|-------|-------------|---------|------|
| 1 | **Development** | Engineer testing | Tests pass locally |
| 2 | **Staging** | Integration testing | All TEST- pass |
| 3 | **Preview** | Stakeholder review | Sign-off from PM |
| 4 | **Production** | Live users | All DEP- criteria met |

## Release Criteria Categories

| Category | Examples | Priority |
|----------|----------|----------|
| **Functional** | Tests pass, features work | Must-have |
| **Performance** | Latency <200ms, throughput >100rps | Must-have |
| **Security** | No critical vulns, secrets rotated | Must-have |
| **Operational** | Runbooks ready, monitoring active | Should-have |
| **Documentation** | Release notes, API docs updated | Should-have |

## Rollback Strategy Patterns

| Pattern | When to Use | Complexity |
|---------|-------------|------------|
| **Blue-Green** | Need instant rollback, can afford 2x infra | Medium |
| **Canary** | Gradual rollout, catch issues early | High |
| **Rolling** | Zero-downtime, standard approach | Low |
| **Feature Flags** | Decouple deploy from release | Medium |

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **Deploy and pray** | No validation steps defined | Add DEP- validation entries |
| **Manual everything** | No automation, error-prone | Automate repeatable steps |
| **No rollback plan** | "We'll figure it out" | Define triggers and procedures upfront |
| **Environment drift** | Staging doesn't match production | Infrastructure as code, sync configs |
| **Missing criteria** | "It works on my machine" | Formal DEP- criteria checklist |
| **Unclear ownership** | No one knows who approves | Assign owner to each DEP- |

## Quality Gates

Before proceeding to Runbook Creation:

- [ ] All deployment environments documented (DEP- Environment type)
- [ ] Release criteria defined with clear blockers (DEP- Criteria type)
- [ ] Rollback triggers specified with thresholds (DEP- Rollback type)
- [ ] Post-deploy validation steps defined (DEP- Validation type)
- [ ] Each DEP- entry has an owner
- [ ] Criteria trace back to EPIC-, TEST-, API- IDs

## Downstream Connections

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **Runbook Creation** | DEP- rollback procedures become runbook inputs | DEP-003 → RUN-005 |
| **Monitoring Setup** | DEP- thresholds inform alerting | DEP-003 (2% error) → MON-001 |
| **v0.9 GTM Strategy** | Release readiness gates launch | All DEP- met → GTM-001 |
| **EPIC- Future Releases** | DEP- becomes template for next release | DEP-001 reused |

## Detailed References

- **Environment configuration examples**: See `references/environment-examples.md`
- **DEP- entry template**: See `assets/dep-template.md`
- **Rollback procedure guide**: See `references/rollback-guide.md`
