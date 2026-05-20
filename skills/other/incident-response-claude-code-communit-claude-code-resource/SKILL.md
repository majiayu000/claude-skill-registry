---
name: incident-response
description: Incident response procedures — triage, communication, investigation, mitigation, and post-incident review. Use when handling production incidents or writing runbooks.
---

# Incident Response

## Severity Levels

Assign a severity level immediately upon incident detection. Severity determines response urgency, communication cadence, and escalation path.

| Severity | Name | Description | Examples | Response Time | Update Cadence | Responders |
|----------|------|-------------|----------|---------------|----------------|------------|
| **P0** | Total Outage | Complete service unavailability. All users affected. Revenue-impacting. | Site completely down, data corruption, security breach with active exploitation | < 15 minutes | Every 15 minutes | All hands on deck, executive notification |
| **P1** | Major Degradation | Core functionality severely impaired. Large portion of users affected. | Payment processing broken, authentication failing for most users, major data pipeline stalled | < 30 minutes | Every 30 minutes | On-call engineer + team lead, stakeholder notification |
| **P2** | Partial Impact | Non-core functionality broken or core functionality degraded for a subset of users. | Search feature down, slow responses in one region, intermittent errors for some users | < 2 hours | Every 2 hours | On-call engineer |
| **P3** | Minor Issue | Cosmetic issues, minor bugs, or issues with workarounds available. | UI glitch, non-critical background job delayed, minor data inconsistency | Next business day | Daily (if ongoing) | Assigned engineer |

### Escalation Rules

- If a P2 is not resolved within 4 hours, escalate to P1.
- If a P1 is not resolved within 2 hours, escalate to P0.
- Any incident involving data breach or security compromise is automatically P0.
- When in doubt, over-classify. It is better to downgrade than to under-respond.

## Triage Procedure

When an incident is detected (alert, user report, or monitoring), follow this triage sequence:

### Step 1: Assess Impact

Answer these questions within the first 5 minutes:

- [ ] Who is affected? (All users, subset, internal only)
- [ ] What is broken? (Specific feature, entire service, data integrity)
- [ ] When did it start? (Check monitoring for onset time)
- [ ] Is it getting worse? (Error rate trending up, stable, or recovering)

### Step 2: Assign Severity

Based on the impact assessment, assign a severity level using the table above. Document the severity and reasoning.

### Step 3: Assemble the Response Team

| Severity | Who to Notify |
|----------|--------------|
| P0 | On-call engineer, engineering manager, VP Engineering, customer support lead, communications |
| P1 | On-call engineer, engineering manager, customer support lead |
| P2 | On-call engineer, relevant team lead |
| P3 | Assigned engineer (via ticket) |

### Step 4: Designate Roles

For P0 and P1 incidents, explicitly assign these roles:

| Role | Responsibility |
|------|---------------|
| **Incident Commander (IC)** | Coordinates response, makes decisions, delegates tasks. Does NOT debug. |
| **Technical Lead** | Leads investigation and mitigation. Communicates findings to IC. |
| **Communications Lead** | Drafts and sends status updates to stakeholders and customers. |
| **Scribe** | Documents timeline, actions taken, and decisions in real time. |

### Step 5: Open Incident Channel

Create a dedicated communication channel (Slack channel, incident bridge call):

- Name it clearly: `#incident-2024-03-15-payments-down`
- Pin the initial assessment and severity level.
- All discussion and decisions happen in this channel.

## Communication Templates

### Initial Alert

```
INCIDENT DECLARED: [P0/P1/P2] - [Brief description]

Impact: [Who is affected and how]
Start time: [When it began, UTC]
Current status: [Investigating / Identified / Mitigating]
Incident Commander: [Name]
Channel: #incident-[date]-[topic]

Next update in [15/30] minutes.
```

### Status Update

```
INCIDENT UPDATE: [P0/P1/P2] - [Brief description]

Status: [Investigating / Identified / Mitigating / Resolved]
Duration: [Time since start]
Current state: [What is happening now]
Actions taken: [What has been tried]
Next steps: [What will be done next]

Next update in [15/30] minutes.
```

### Resolution Notification

```
INCIDENT RESOLVED: [P0/P1/P2] - [Brief description]

Duration: [Total time from detection to resolution]
Root cause: [One-sentence summary]
Resolution: [What fixed it]
Customer impact: [Summary of user-facing impact]
Follow-up: Post-incident review scheduled for [date/time].

Monitoring for recurrence.
```

### Customer-Facing Communication

```
[Service Name] Status Update

We are aware of an issue affecting [description of user impact].
Our team is actively working to resolve this.

Started: [Time, timezone]
Current status: [Brief, non-technical description]

We will provide updates every [30 minutes / 1 hour].
We apologize for the inconvenience.
```

## Investigation Methodology

Follow this structured approach rather than randomly checking things. Work from symptoms toward root cause.

### Step 1: Check Dashboards

Start with the service overview dashboard. Look for:

- Error rate spikes (when exactly did they start?)
- Latency increases (gradual degradation or sudden jump?)
- Traffic anomalies (unexpected spike or drop?)
- Resource utilization (CPU, memory, disk, connections)

### Step 2: Check Recent Deploys

Most incidents are caused by recent changes. Check:

```bash
# What was deployed recently?
git log --oneline --since="2 hours ago" origin/main

# Any recent infrastructure changes?
# Check deployment pipeline history, Terraform runs, config changes
```

Questions to answer:

- Was anything deployed in the last 2 hours?
- Was there a configuration change (feature flags, environment variables)?
- Was there an infrastructure change (scaling, migration, certificate renewal)?

### Step 3: Examine Logs

Search logs filtered to the incident timeframe:

```
# Example queries (adapt to your log aggregation platform)
# ELK/Kibana: level:ERROR AND service:order-service AND @timestamp >= "2024-03-15T14:00:00"
# Datadog: service:order-service status:error
# CloudWatch: filter @message like /ERROR/ | sort @timestamp desc
```

Look for:

- Error messages with stack traces.
- Repeated error patterns (same error thousands of times).
- New error types that were not present before the incident.
- Correlation between errors and the timeline.

### Step 4: Hypothesize and Test

Based on data gathered, form a hypothesis and test it:

| Hypothesis | How to Test |
|------------|------------|
| Bad deploy caused it | Compare error timeline with deploy timestamp. Roll back and observe. |
| Database is overloaded | Check connection pool, slow query log, lock contention. |
| External dependency is down | Check dependency status page, test connectivity, check timeout rates. |
| Traffic spike overwhelmed the service | Check request rate, compare to normal baseline, check auto-scaling. |
| DNS or certificate issue | Test DNS resolution, check certificate expiry, verify SSL handshake. |
| Memory leak | Check memory usage trend, look for OOM kills in system logs. |
| Data corruption | Query for inconsistent data, check recent migration or backfill jobs. |

### Step 5: Verify the Fix

After applying a fix:

- [ ] Error rate returning to baseline.
- [ ] Latency returning to normal.
- [ ] No new error patterns appearing.
- [ ] Affected functionality manually verified.
- [ ] Monitor for at least 15 minutes (P0/P1) or 30 minutes (P2) before declaring resolved.

## Common Mitigation Actions

When the root cause is identified (or even before, to reduce impact), apply the appropriate mitigation:

| Action | When to Use | How | Risk |
|--------|------------|-----|------|
| **Rollback** | Bad deploy identified | Revert to previous known-good version via deployment pipeline | May lose new features; verify database compatibility |
| **Feature flag toggle** | New feature causing issues | Disable the flag in your feature management system | Requires feature flags to be in place |
| **Horizontal scaling** | Service overwhelmed by traffic | Increase instance count via auto-scaler or manual scaling | Increased cost; may not help if bottleneck is downstream |
| **Cache clear** | Stale or corrupted cached data | Flush application cache (Redis `FLUSHDB`, CDN purge) | Temporary increase in origin load after flush |
| **Circuit breaker** | Failing dependency cascading | Activate circuit breaker to fail fast instead of waiting | Gracefully degraded experience for users |
| **Traffic shedding** | Total overload | Rate limit or redirect traffic, enable maintenance page | Users see errors or degraded service |
| **Database failover** | Primary database unresponsive | Promote replica to primary (if configured) | Brief downtime during promotion; verify replication lag |
| **DNS redirect** | Entire region or provider down | Update DNS to point to backup region or provider | Propagation delay (use low TTL proactively) |
| **Restart** | Process stuck, memory leak | Rolling restart of application instances | Brief capacity reduction during restart |
| **Hotfix** | Small targeted code fix needed | Fast-track a minimal change through deployment pipeline | Bypasses normal review; must be reviewed post-incident |

### Rollback Procedure

```bash
# Verify the last known-good version
git log --oneline -10 origin/main

# Tag the rollback point
git tag -a incident-rollback-2024-03-15 -m "Rolling back due to P1 incident"

# Trigger deployment of previous version
# (Adapt to your deployment pipeline)
# Example: Kubernetes
kubectl rollout undo deployment/order-service

# Verify rollback is deployed
kubectl rollout status deployment/order-service

# Monitor error rate and confirm reduction
```

## Post-Incident Review

Conduct a post-incident review (PIR) within 48 hours of resolution for P0/P1 incidents and within one week for P2 incidents.

### Post-Incident Review Template

```markdown
# Post-Incident Review: [Incident Title]

**Date**: [date] | **Severity**: [P0/P1/P2] | **Duration**: [time] | **Author**: [name]

## Summary
[2-3 sentences: what happened, the impact, and the resolution.]

## Timeline (UTC)
| Time | Event |
|------|-------|
| 14:00 | Alert fires: order error rate > 5% |
| 14:05 | P1 declared, incident channel created |
| 14:15 | Recent deploy at 13:45 identified as suspect |
| 14:25 | Rollback deployed |
| 14:45 | Resolved, monitoring for recurrence |

## Impact
Users affected, duration, revenue/SLA impact, data impact.

## Root Cause
[Detailed technical explanation of what went wrong and why.]

## Five Whys
1. **Why** did orders fail? -> Payment validation threw an exception.
2. **Why** did validation throw? -> Null value for a non-nullable field.
3. **Why** was the field null? -> Migration added column but did not backfill.
4. **Why** was backfill missed? -> No checklist step for backfill verification.
5. **Why** no checklist step? -> Migration procedures were undocumented.

## Action Items
| Action | Owner | Priority | Due Date | Status |
|--------|-------|----------|----------|--------|
| Add integration test for null field validation | @alice | High | YYYY-MM-DD | TODO |
| Lower alert threshold from 5% to 2% | @bob | High | YYYY-MM-DD | TODO |
| Add feature flag to payment flow | @carol | Medium | YYYY-MM-DD | TODO |

## Lessons Learned
- What went well: [e.g., quick detection, rapid team assembly]
- What could improve: [e.g., rollback automation, test coverage]
```

## Blameless Culture Principles

Post-incident reviews are learning opportunities, not blame sessions. Adhere to these principles:

| Principle | Practice |
|-----------|----------|
| **Assume good intent** | People made the best decisions they could with the information they had at the time. |
| **Focus on systems, not individuals** | Ask "what allowed this to happen?" not "who caused this?" |
| **Separate the what from the who** | Describe actions taken without naming individuals in the root cause. Use role titles if context is needed. |
| **Reward transparency** | Publicly thank people who report incidents, share mistakes, or identify risks. |
| **Follow through on action items** | PIR action items are tracked and completed. Unfixed systemic issues lead to repeat incidents. |
| **Share learnings broadly** | Publish PIR summaries (redacted if needed) so other teams learn too. |

## Runbook Authoring Guide

A runbook is a step-by-step guide for responding to a specific alert or operational scenario.

### Runbook Structure

Every runbook follows this structure:

```markdown
# Runbook: [Alert or Scenario Name]

## When to Use
[Describe the alert, symptom, or scenario that triggers this runbook.]

## Prerequisites
- Access to [systems, dashboards, tools]
- Permissions: [required roles or access levels]

## Steps

### 1. Verify the Problem
```bash
curl -s https://monitoring.example.com/api/v1/query \
  --data-urlencode 'query=rate(http_errors_total{service="order-service"}[5m])'
```
**Expected**: Error rate below 0.01. If above, continue. If normal, check thresholds and close.

### 2. Apply Mitigation
```bash
# Option A: Restart
kubectl rollout restart deployment/order-service
# Option B: Rollback
kubectl rollout undo deployment/order-service
```

### 3. Verify Resolution
**Expected**: Error rate drops below 0.01 within 5 minutes.

### 4. Escalation
If unresolved: escalate to [team], contact [channel/phone], provide [context].
```

### Runbook Best Practices

| Practice | Reason |
|----------|--------|
| Use exact commands, not descriptions | Under stress, responders should copy-paste, not interpret |
| Include expected output | So responders know if the command worked |
| Provide verification after each step | Catch issues early, do not proceed blindly |
| Include a rollback for each step | If a mitigation step makes things worse |
| Test runbooks regularly | Outdated runbooks cause confusion during real incidents |
| Date-stamp and version runbooks | Know when it was last verified |
| Link from alert to runbook | Reduce time-to-runbook to one click |

## Incident Response Checklist

Quick reference during an active incident:

- [ ] Impact assessed (who, what, when, trending).
- [ ] Severity assigned and documented.
- [ ] Incident channel or bridge opened.
- [ ] Roles assigned (IC, Technical Lead, Comms, Scribe).
- [ ] Initial stakeholder notification sent.
- [ ] Timeline being recorded in real time.
- [ ] Investigation following structured methodology (dashboards, deploys, logs, hypothesize, test).
- [ ] Mitigation applied and impact reducing.
- [ ] Resolution verified with monitoring data.
- [ ] All-clear communication sent.
- [ ] Post-incident review scheduled (within 48 hours for P0/P1).
- [ ] Action items created with owners and due dates.
