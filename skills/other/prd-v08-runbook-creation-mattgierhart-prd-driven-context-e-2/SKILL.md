---
name: prd-v08-runbook-creation
description: >
  Create operational playbooks for incident response, deployments, and maintenance during PRD v0.8 Deployment & Ops.
  Triggers on requests to create runbooks, document procedures, or when user asks "how do we handle incidents?",
  "runbook", "operational procedures", "on-call guide", "incident response", "maintenance procedures".
  Outputs RUN- entries with step-by-step operational procedures.
---

# Runbook Creation

Position in workflow: v0.8 Release Planning → **v0.8 Runbook Creation** → v0.8 Monitoring Setup

## Purpose

Create step-by-step operational playbooks that enable anyone on-call to handle incidents, perform deployments, and execute maintenance tasks without requiring deep system knowledge.

## Core Concept: Runbook as Insurance

> A runbook is not documentation—it is **operational insurance**. When systems fail at 3 AM, the runbook is the difference between 5-minute recovery and 5-hour chaos.

## Runbook Categories

| Category | Purpose | Trigger |
|----------|---------|---------|
| **Incident Response** | Handle production issues | Alert fires, user reports |
| **Deployment** | Execute release procedures | Scheduled release |
| **Maintenance** | Regular operational tasks | Scheduled windows |
| **Recovery** | Restore from failures | Disaster scenario |
| **Escalation** | Route to right people | Issue beyond capability |

## Execution

1. **Identify critical scenarios**
   - What alerts from MON- require action?
   - What deployment steps from DEP- need procedures?
   - What RISK- entries need response plans?

2. **Map each scenario to a runbook**
   - One runbook per distinct scenario
   - Clear scope—what it covers and doesn't

3. **Document step-by-step procedures**
   - Numbered steps, no ambiguity
   - Include commands, links, contact info
   - Assume operator has minimal context

4. **Define escalation paths**
   - When to escalate
   - Who to contact
   - What information to provide

5. **Add verification steps**
   - How to confirm the issue is resolved
   - What metrics should normalize

6. **Create RUN- entries** with full traceability

## RUN- Output Template

```
RUN-XXX: [Runbook Title]
Category: [Incident | Deployment | Maintenance | Recovery | Escalation]
Trigger: [What initiates this runbook]
Owner: [Team or role responsible]
Last Tested: [Date of last drill/use]

## Scope
- **Handles**: [What scenarios this covers]
- **Does NOT handle**: [Explicit exclusions]

## Prerequisites
- [ ] Access to [system/tool]
- [ ] Credentials for [service]
- [ ] Contact info for [team]

## Procedure

### Step 1: [Action Title]
[Detailed instructions]

Commands:
```bash
# Example command with placeholders
```

Verification:
- [ ] [How to confirm step succeeded]

### Step 2: [Action Title]
[Detailed instructions]

### Step N: [Final Action]
[Detailed instructions]

## Escalation
- **When to escalate**: [Conditions that require help]
- **Who to contact**: [Name/role, contact method]
- **What to provide**: [Information needed for handoff]

## Post-Incident
- [ ] Document incident timeline
- [ ] Update runbook if steps were wrong/missing
- [ ] Schedule post-mortem if severity > [threshold]

Linked IDs: [MON-XXX, DEP-XXX, RISK-XXX related]
```

**Example RUN- entries:**

```
RUN-001: Database Connection Pool Exhaustion
Category: Incident
Trigger: MON-005 alert (connection pool >90%)
Owner: Backend Team
Last Tested: 2025-01-15

## Scope
- **Handles**: Connection pool saturation, slow queries causing pooling
- **Does NOT handle**: Database server crash (see RUN-010)

## Prerequisites
- [ ] Access to AWS RDS console
- [ ] Database read credentials
- [ ] PagerDuty access for escalation

## Procedure

### Step 1: Verify Alert
Check current connection pool status:

Commands:
```sql
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';
SELECT * FROM pg_stat_activity WHERE state = 'active' ORDER BY query_start;
```

Verification:
- [ ] Connection count matches alert threshold

### Step 2: Identify Problematic Queries
Find long-running or blocked queries:

Commands:
```sql
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes';
```

### Step 3: Kill Problematic Queries (if safe)
Only kill queries that are clearly stuck:

Commands:
```sql
SELECT pg_terminate_backend(pid) FROM pg_stat_activity
WHERE pid = <problematic_pid>;
```

Verification:
- [ ] Connection count dropping
- [ ] MON-005 alert resolving

### Step 4: Investigate Root Cause
- Check recent deployments (last 24h)
- Review application logs for query patterns
- Check for missing indexes on recent queries

## Escalation
- **When to escalate**: Issue persists >15 minutes, data integrity concern
- **Who to contact**: Database Team Lead (Slack: @db-team, PagerDuty)
- **What to provide**: Timeline, queries identified, actions taken

## Post-Incident
- [ ] Document incident timeline
- [ ] File ticket for query optimization if needed
- [ ] Update this runbook if steps were wrong/missing

Linked IDs: MON-005, DEP-001, RISK-008
```

```
RUN-002: Production Deployment Procedure
Category: Deployment
Trigger: Scheduled release, all DEP- criteria met
Owner: DevOps Team
Last Tested: 2025-01-20

## Scope
- **Handles**: Standard production deployments
- **Does NOT handle**: Hotfix deployments (see RUN-003), Database migrations (see RUN-004)

## Prerequisites
- [ ] All DEP- criteria verified (DEP-002, DEP-003)
- [ ] Staging deployment successful
- [ ] Release approval in deployment channel
- [ ] On-call engineer available for rollback

## Procedure

### Step 1: Pre-Deploy Announcement
Notify stakeholders of upcoming deployment:

Commands:
```bash
# Post to #deployments Slack channel
./scripts/notify-deploy.sh --env production --version ${VERSION}
```

### Step 2: Create Deployment Checkpoint
Tag current production for rollback:

Commands:
```bash
git tag -a "pre-deploy-$(date +%Y%m%d-%H%M)" -m "Checkpoint before ${VERSION}"
git push origin --tags
```

### Step 3: Execute Deployment
Deploy to production using CI/CD:

Commands:
```bash
# Trigger production deploy pipeline
./scripts/deploy.sh --env production --version ${VERSION}
```

Verification:
- [ ] Deployment pipeline green
- [ ] New version visible in health check endpoint

### Step 4: Post-Deploy Validation
Run smoke tests and verify key flows:

Commands:
```bash
./scripts/smoke-test.sh --env production
```

Verification:
- [ ] All smoke tests pass
- [ ] Key UJ- flows verified manually
- [ ] Error rate within baseline (MON-001)

### Step 5: Monitor for 15 Minutes
Watch dashboards for anomalies:
- Error rate dashboard
- Latency dashboard
- Business metrics dashboard

Verification:
- [ ] No new alerts
- [ ] Metrics within normal range

## Escalation
- **When to escalate**: Smoke tests fail, error rate >2%, user reports
- **Who to contact**: On-call engineer, then Tech Lead
- **What to provide**: Deployment version, failure mode, logs

## Post-Incident
- [ ] Post deployment success/failure to #deployments
- [ ] Update deployment log
- [ ] Schedule retro if issues encountered

Linked IDs: DEP-001, DEP-002, DEP-003, MON-001
```

## Runbook Quality Checklist

For each runbook, verify:

| Criterion | Question | Pass? |
|-----------|----------|-------|
| **Actionable** | Can someone follow this without asking questions? | |
| **Complete** | Are all steps documented with commands? | |
| **Verifiable** | Does each step have a verification check? | |
| **Scoped** | Is it clear what this does and doesn't cover? | |
| **Escalatable** | Is the escalation path defined? | |
| **Tested** | Has this runbook been tested in a drill? | |
| **Maintained** | Is there an owner who updates it? | |

## Runbook Types by MON- Alert

Map monitoring alerts to runbooks:

| Alert Type | Runbook | Response Time |
|------------|---------|---------------|
| **Critical** | Dedicated incident RUN- | <5 min |
| **Warning** | Shared investigation RUN- | <30 min |
| **Info** | Reference documentation | Next business day |

## Common Procedures to Document

| Category | Must-Have Runbooks |
|----------|-------------------|
| **Incident** | Service down, Performance degradation, Security incident |
| **Deployment** | Standard release, Hotfix, Rollback |
| **Maintenance** | Database backup, Log rotation, Certificate renewal |
| **Recovery** | Data restore, Failover, Service restart |

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **Too vague** | "Investigate the issue" | Add specific commands and checks |
| **Too long** | 50+ step runbook | Split into focused runbooks |
| **Outdated** | References deprecated tools | Add review date, assign owner |
| **No verification** | Steps without confirmation | Add verification after each step |
| **Assuming knowledge** | "You know how to do this" | Write for someone's first day |
| **No escalation** | Dead ends with no help path | Always define escalation |

## Quality Gates

Before proceeding to Monitoring Setup:

- [ ] All critical scenarios have runbooks (RUN-)
- [ ] Each MON- alert maps to a RUN- procedure
- [ ] DEP- rollback triggers link to RUN- procedures
- [ ] RISK- high/medium entries have response runbooks
- [ ] All runbooks have owners and last-tested dates
- [ ] Escalation paths defined for all runbooks

## Downstream Connections

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **Monitoring Setup** | RUN- procedures linked from alerts | MON-001 → RUN-001 |
| **On-Call Team** | RUN- as operational reference | Night incident → RUN-001 |
| **Post-Mortems** | RUN- gaps inform improvements | "Runbook missing step" → Update RUN-001 |
| **Training** | RUN- for new engineer onboarding | Run drills using RUN-002 |

## Detailed References

- **Runbook examples by category**: See `references/runbook-examples.md`
- **RUN- entry template**: See `assets/run-template.md`
- **Incident response framework**: See `references/incident-framework.md`
