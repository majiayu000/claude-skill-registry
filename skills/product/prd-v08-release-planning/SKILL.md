---
name: prd-v08-release-planning
description: >
  Define release criteria, deployment environments, and rollback strategies during PRD v0.8 Deployment & Ops.
  Triggers on requests to plan releases, define deployment criteria, or when user asks "how do we deploy?",
  "release criteria", "deployment plan", "rollback strategy", "go-live checklist".
  Outputs DEP- entries with deployment steps and release criteria.
---

# Release Planning

Position in workflow: v0.7 Implementation Loop → **v0.8 Release Planning** → v0.8 Runbook Creation

## Purpose

Transform completed EPICs into production-ready releases by defining deployment environments, release criteria, rollback triggers, and operational readiness gates.

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
