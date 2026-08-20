---
name: prd-v08-runbook-creation
description: >
  Create operational playbooks for incident response, deployments, and maintenance during PRD v0.8 Deployment & Ops.
  Triggers on requests to create runbooks, document procedures, or when user asks "how do we handle incidents?",
  "runbook", "operational procedures", "on-call guide", "incident response", "maintenance procedures".
  Outputs RUN- entries with step-by-step operational procedures.
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

# Runbook Creation

Position in workflow: v0.8 Release Planning → **v0.8 Runbook Creation** → v0.8 Monitoring Setup

## Execution Mode

Default is **standard**. See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md) for selection logic.

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | 2–3 runbooks covering the top RISK-/MON- pairs |
| **standard** | Incident + deployment + maintenance runbooks linked to MON- and DEP-, with escalation paths |
| **deep** | Full matrix + drill schedule + recovery scenarios + tabletop exercise outputs |

## Consumes

This skill requires prior work from v0.8 Release Planning and earlier stages:

- **DEP-\* deployment entries** (from v0.8 Release Planning) — Deployment procedures from DEP- rollback/validation sections inform RUN- deployment and recovery runbooks
- **RISK-\* risk entries** (from v0.5 Risk Discovery) — High/medium RISK- entries must have response runbooks; mitigations become procedures
- **MON-\* monitoring specifications** (planned from v0.8 Monitoring Setup, or anticipated) — Key alerts from MON- (before formalization) inform incident response runbooks; runbooks will be referenced FROM monitoring
- **ARC-\* architecture decisions** (from v0.6 Architecture Design) — System structure (single service vs microservices, databases, integrations) determines incident scope and escalation paths
- **TECH-\* technology stack** (from v0.5 Technical Stack Selection) — Technology choices (database, cloud provider, APM tools) determine specific commands and tools in runbook procedures
- **API-\* endpoint contracts** (from v0.6 Technical Specification) — For reference if incident involves specific endpoints or payloads

This skill assumes DEP- entries are complete with rollback procedures and post-deploy validation steps defined.

## Produces

This skill creates/updates:

- **RUN-\* entries** (operational runbooks, category-based) — Step-by-step procedures for incident response, deployment execution, maintenance tasks, recovery from failures, and escalation paths
- **Incident response matrix** — Mapping of scenarios (connection pool exhaustion, latency spike, deployment failure, etc.) to RUN- procedures
- **Runbook cross-reference** — Links from RUN- procedures to DEP- rollback conditions, anticipated MON- alerts, and RISK- entries they address

All RUN- entries are **operational procedures**, not confidence-based. They are:
- **Executable** (numbered steps with specific commands and tools)
- **Verifiable** (each step has a verification check confirming success)
- **Scoped** (explicit "Handles" and "Does NOT handle" sections)
- **Escalatable** (clear escalation paths and contact information)
- **Tested** (should be drilled regularly; includes "Last Tested" date)

Example RUN- entries:
```markdown
RUN-001: Database Connection Pool Exhaustion
Category: Incident
Trigger: MON-005 alert (connection pool >90%) — from v0.8 Monitoring Setup
Owner: Backend Team
Last Tested: 2025-02-20

## Scope
- **Handles**: Connection pool saturation, slow queries causing pooling
- **Does NOT handle**: Database server crash (see RUN-010), Network failure (see RUN-011)

## Prerequisites
- [ ] Access to AWS RDS console
- [ ] PostgreSQL read credentials in LastPass
- [ ] PagerDuty access for escalation
- [ ] Datadog dashboard access (MON-005 source)

## Procedure

### Step 1: Verify Alert
Check current connection pool status:

Commands:
\`\`\`sql
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';
SELECT * FROM pg_stat_activity WHERE state = 'active' ORDER BY query_start;
\`\`\`

Verification:
- [ ] Connection count ≥90% of max pool (check DEP-001 pool config)

### Step 2: Identify Problematic Queries
Find long-running or blocked queries:

Commands:
\`\`\`sql
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes';
\`\`\`

Verification:
- [ ] At least one query identified running >5 minutes

### Step 3: Kill Problematic Queries (if safe)
Only kill queries that are clearly stuck:

Commands:
\`\`\`sql
SELECT pg_terminate_backend(pid) FROM pg_stat_activity
WHERE pid = <problematic_pid>;
\`\`\`

Verification:
- [ ] Connection count dropping within 2 minutes
- [ ] MON-005 alert resolving

### Step 4: Investigate Root Cause
- Check recent deployments (last 24h via git log)
- Review application logs for query patterns (Datadog logs)
- Check for missing indexes on recent queries

## Escalation
- **When to escalate**: Issue persists >15 minutes, data integrity concern, cannot kill queries safely
- **Who to contact**: Database Team Lead (Slack: @db-team, PagerDuty)
- **What to provide**: Timeline, queries identified, actions taken, connection count trend

## Post-Incident
- [ ] Document incident timeline (who was paged, when actions taken)
- [ ] File ticket for query optimization if needed
- [ ] Update this runbook if steps were wrong/missing
- [ ] Schedule team drill of this runbook within 1 week if escalated

Linked IDs: MON-005 (alert), DEP-001 (pool config), RISK-008 (data integrity)

---

RUN-002: Production Deployment Procedure
Category: Deployment
Trigger: Scheduled release when all DEP- criteria met
Owner: DevOps Team
Last Tested: 2025-02-18

## Scope
- **Handles**: Standard production deployments (mainline releases)
- **Does NOT handle**: Hotfix deployments (see RUN-003), Database migrations (see RUN-004), Emergency rollback (see RUN-005)

## Prerequisites
- [ ] All DEP- criteria verified
  - [ ] DEP-002: All tests pass in staging
  - [ ] DEP-003: No critical RISK- blockers
  - [ ] DEP-004: Security review complete
- [ ] Staging deployment successful
- [ ] Release approval from Tech Lead in #deployments channel
- [ ] On-call engineer available for rollback (next 30 minutes)

## Procedure

### Step 1: Pre-Deploy Announcement
Notify stakeholders of upcoming deployment:

Commands:
\`\`\`bash
./scripts/notify-deploy.sh --env production --version v${VERSION} --channel #deployments
\`\`\`

Verification:
- [ ] Message posted to #deployments

### Step 2: Create Deployment Checkpoint
Tag current production for rollback (per DEP-003):

Commands:
\`\`\`bash
git tag -a "pre-deploy-$(date +%Y%m%d-%H%M)" -m "Checkpoint before v${VERSION}"
git push origin --tags
\`\`\`

Verification:
- [ ] Tag created and pushed to git

### Step 3: Execute Deployment
Deploy to production using CI/CD:

Commands:
\`\`\`bash
./scripts/deploy.sh --env production --version v${VERSION}
\`\`\`

Verification:
- [ ] Deployment pipeline exits with status 0
- [ ] New version visible: curl https://api.prod.example.com/health | jq .version

### Step 4: Post-Deploy Validation
Run smoke tests (per DEP-004):

Commands:
\`\`\`bash
./scripts/smoke-test.sh --env production --suite critical
\`\`\`

Verification:
- [ ] All smoke tests pass
- [ ] Manual spot-check: key UJ- flows work (test signup, login, create report)
- [ ] Error rate within baseline: curl https://api.prod.example.com/metrics | jq .error_rate_5m

### Step 5: Monitor for 30 Minutes
Watch dashboards for anomalies:

Verification:
- [ ] No new critical/warning alerts (check Datadog/Slack #alerts)
- [ ] Latency (MON-001) within normal range (<500ms p95)
- [ ] Error rate (MON-002) within baseline (<0.5%)
- [ ] Business metrics dashboard shows expected traffic

## Escalation
- **When to escalate**: Smoke tests fail, error rate >2%, user reports critical issue, latency >2s
- **Who to contact**: On-call engineer (PagerDuty), then Tech Lead
- **What to provide**: Version deployed, failure mode, logs from Datadog, timeline

## Post-Deployment
- [ ] Post deployment success to #deployments
- [ ] Update deployment log in runbook folder
- [ ] If issues: Escalate and execute RUN-005 (emergency rollback)

Linked IDs: DEP-001/002/003/004 (release criteria), RUN-005 (emergency rollback)
```

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
