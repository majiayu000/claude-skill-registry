---
name: incident-response
description: Provides incident response best practices covering severity classification, on-call rotation, war room protocols, runbook templates, escalation policies, and blameless postmortems. Use when handling an incident, setting up on-call, writing a postmortem, creating a runbook, configuring PagerDuty or OpsGenie, or building incident management processes.
---

# Incident Response

Incidents are inevitable in any production system. The difference between a minor blip and a catastrophic failure is how prepared your team is to detect, respond, communicate, and learn. This guide covers the full incident lifecycle from classification through postmortem, with concrete templates and integration patterns.

## Severity Classification

Every incident must be classified immediately. Severity determines response speed, communication cadence, and escalation paths.

| Severity | Impact | Examples | Response Time | Duration Target |
|----------|--------|----------|---------------|-----------------|
| SEV1 | Complete outage or data loss | Service down for all users, data corruption, security breach | 5 min | Mitigate < 1 hour |
| SEV2 | Major degradation | Core feature broken for >10% users, payment failures | 15 min | Mitigate < 4 hours |
| SEV3 | Minor degradation | Non-critical feature broken, elevated error rate | 1 hour | Resolve < 24 hours |
| SEV4 | Cosmetic or low impact | UI glitch, misleading error message | Next business day | Resolve < 1 week |

### Classification Decision Tree

```
Is the service completely unavailable to all users? -> SEV1
Is there a security breach or data exposure?        -> SEV1
Is there data loss or corruption?                   -> SEV1
Is a core revenue feature broken for >10% users?    -> SEV2
Is there financial impact (failed payments)?        -> SEV2
Is a core feature broken for <10% users?            -> SEV3
Is it a non-critical feature degradation?           -> SEV3
Everything else                                     -> SEV4
```

## On-Call Setup

| Component | Recommendation | Rationale |
|-----------|---------------|-----------|
| Rotation size | 5-8 engineers minimum | Allows 1-week shifts with recovery time |
| Shift length | 1 week (Mon 09:00 to Mon 09:00) | Predictable, long enough for context |
| Primary + Secondary | Always two people on call | Backup for escalation or unavailability |
| Handoff meeting | 30 min at rotation start | Review active issues, recent changes, known risks |
| Follow-the-sun | Split by timezone for global teams | No one wakes up at 3 AM regularly |
| Compensation | On-call stipend + incident bonus | Recognizes the burden fairly |

### PagerDuty Schedule and Escalation (Terraform)

```hcl
resource "pagerduty_schedule" "primary_oncall" {
  name      = "Platform Primary On-Call"
  time_zone = "America/New_York"

  layer {
    name                         = "Primary"
    start                        = "2025-01-06T09:00:00-05:00"
    rotation_virtual_start       = "2025-01-06T09:00:00-05:00"
    rotation_turn_length_seconds = 604800  # 1 week
    users = [
      pagerduty_user.alice.id, pagerduty_user.bob.id,
      pagerduty_user.carol.id, pagerduty_user.dave.id,
      pagerduty_user.eve.id,
    ]
  }
}

resource "pagerduty_escalation_policy" "platform" {
  name      = "Platform Escalation"
  num_loops = 2

  rule {
    escalation_delay_in_minutes = 5
    target { type = "schedule_reference"; id = pagerduty_schedule.primary_oncall.id }
  }
  rule {
    escalation_delay_in_minutes = 10
    target { type = "schedule_reference"; id = pagerduty_schedule.secondary_oncall.id }
  }
  rule {
    escalation_delay_in_minutes = 15
    target { type = "user_reference"; id = pagerduty_user.engineering_manager.id }
  }
}
```

## War Room Protocol

When a SEV1 or SEV2 is declared, open a war room -- a structured environment for incident resolution.

### War Room Flow

```
1. DETECT    Alert fires -> On-call acknowledges within 5 min
2. TRIAGE    Classify severity. SEV1/SEV2 -> open war room
3. ASSEMBLE  IC assigned. Slack: #inc-YYYYMMDD-description. Video bridge opened.
4. ROLES     IC | Comms Lead | Operations Lead | Scribe | SMEs
5. INVESTIGATE  What changed? What is blast radius? What do signals show?
6. MITIGATE  Priority: restore service (rollback, feature flag, scale, failover)
7. RESOLVE   Service stable. IC declares resolved.
8. FOLLOW-UP Postmortem within 48 hours. Action items tracked.
```

### Incident Channel Template

```
**INCIDENT DECLARED**
Severity: SEV1 | Title: Order processing failing for all users
Detected: 2025-03-15 14:32 UTC
Impact: All users unable to complete checkout

**ROLES**  IC: @alice | Comms: @bob | Ops: @carol | Scribe: @dave

**LINKS**
Status Page: https://status.example.com
Runbook: https://wiki.internal/runbooks/order-processing
Dashboard: https://grafana.internal/d/orders-overview

**TIMELINE**
14:32 - Alert fired: HighErrorBudgetBurnRate_Fast
14:35 - On-call acknowledged, war room opened
14:38 - Identified: deploy changed payment gateway config
14:42 - Rollback initiated
14:47 - Rollback complete, error rate dropping
14:55 - Fully restored | 15:00 - Resolved
```

## Runbook Template

Every alert should link to a runbook with diagnosis, mitigation, and recovery steps.

```yaml
# runbooks/order-service-high-error-rate.yml
metadata:
  title: "Order Service High Error Rate"
  service: order-service
  severity: SEV1/SEV2
  owner: platform-team
  alert_names: [HighErrorBudgetBurnRate_Fast, HighErrorBudgetBurnRate_Slow]

impact: "Users cannot checkout. Revenue impact ~$2,400/min at peak."

diagnosis:
  - step: Check recent deployments
    command: "kubectl -n production rollout history deployment/order-service"
    expected: "If deploy correlates with error onset, proceed to rollback"

  - step: Check error logs
    command: '{service="order-service"} |= "error" | json | level="error"'
    expected: "Identify error type: database, upstream, or application"

  - step: Check downstream dependencies
    command: "curl -s https://payment-service.internal/healthz | jq ."
    expected: "All healthy. If not, see payment-service-down runbook"

  - step: Check database performance
    command: "psql -h orders-db -c \"SELECT pid, state, query FROM pg_stat_activity WHERE state != 'idle' ORDER BY query_start LIMIT 20;\""
    expected: "No long-running queries or lock contention"

mitigation:
  - option: Rollback last deployment
    when: "Error onset correlates with a deployment"
    command: "kubectl -n production rollout undo deployment/order-service"
    verify: "Error rate returns to baseline within 5 minutes"

  - option: Scale up
    when: "Capacity-related errors (connection pool, CPU)"
    command: "kubectl -n production scale deployment/order-service --replicas=10"
    verify: "Connection pool usage drops below 80%"

  - option: Circuit breaker
    when: "Payment service is root cause"
    command: "kubectl set env deployment/order-service PAYMENT_CIRCUIT_BREAKER=open"
    verify: "5xx rate drops, orders queue for retry"

  - option: Database failover
    when: "Primary database unresponsive"
    command: "aws rds failover-db-cluster --db-cluster-identifier orders-cluster"
    verify: "Connections re-establish within 60 seconds"

recovery:
  - "Confirm baseline error rate for 15 minutes"
  - "Check for data inconsistencies from failed transactions"
  - "Update status page to resolved"
  - "Schedule postmortem within 48 hours"
```

## Escalation Policies

| Trigger | Action | Timeout |
|---------|--------|---------|
| Alert fires | Page primary on-call | -- |
| No ack in 5 min | Escalate to secondary | 5 min |
| No ack in 15 min | Escalate to engineering manager | 10 min |
| SEV1 declared | Auto-notify VP Eng + CTO | Immediate |
| 30 min without mitigation | IC requests additional responders | IC decision |
| Customer data exposed | Notify Security + Legal | Immediate |

### Communication Templates

```markdown
# Status Page -- Investigating
**[Investigating] Elevated error rates on checkout**
We are investigating errors during checkout. Our team is engaged.
Update within 30 minutes.

# Status Page -- Identified
**[Identified] Checkout errors caused by payment config issue**
Root cause identified. Fix deploying now. Update in 15 minutes.

# Status Page -- Resolved
**[Resolved] Checkout errors resolved**
Configuration rolled back at 14:47 UTC. All systems normal.
Failed orders auto-retried. Full report within 48 hours.

# Internal Update (Slack #incidents)
**SEV1 Update -- 14:45 UTC**
Impact: Checkout down since 14:25 | Root cause: bad config deploy
Action: Rollback in progress, ETA 5 min
Revenue impact: ~$12,000 est | IC: @alice
```

## PagerDuty / OpsGenie Integration

### PagerDuty Event API v2

```typescript
async function triggerIncident(params: {
  title: string;
  severity: 'critical' | 'error' | 'warning' | 'info';
  service: string;
  dedupKey: string;
}): Promise<string> {
  const response = await fetch('https://events.pagerduty.com/v2/enqueue', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      routing_key: process.env.PAGERDUTY_ROUTING_KEY,
      event_action: 'trigger',
      dedup_key: params.dedupKey,
      payload: {
        summary: params.title,
        severity: params.severity,
        source: params.service,
      },
      links: [
        { href: `https://grafana.internal/d/${params.service}`, text: 'Dashboard' },
        { href: `https://wiki.internal/runbooks/${params.service}`, text: 'Runbook' },
      ],
    }),
  });
  return (await response.json()).dedup_key;
}

async function resolveIncident(dedupKey: string): Promise<void> {
  await fetch('https://events.pagerduty.com/v2/enqueue', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      routing_key: process.env.PAGERDUTY_ROUTING_KEY,
      event_action: 'resolve',
      dedup_key: dedupKey,
    }),
  });
}
```

## Postmortem Template

```markdown
# Postmortem: [Incident Title]

**Date:** YYYY-MM-DD | **Duration:** HH:MM | **Severity:** SEVN
**IC:** [Name] | **Authors:** [Names] | **Status:** Draft / Complete

## Summary
One paragraph: what happened, impact, resolution.

## Impact
| Metric | Value |
|--------|-------|
| User impact duration | X hours Y minutes |
| Users affected | N (Z% of total) |
| Revenue impact | $X,XXX estimated |
| SLA impact | X min against 99.9% target |

## Timeline (UTC)
| Time | Event |
|------|-------|
| 14:25 | Deploy #4521 pushed (config change) |
| 14:32 | Alert fires: HighErrorBudgetBurnRate_Fast |
| 14:36 | SEV1 declared, war room opened |
| 14:38 | Root cause: payment timeout changed 30s -> 3s |
| 14:42 | Rollback initiated |
| 14:47 | Rollback complete | 14:55 | Fully stable |

## Root Cause
[What broke and why -- focus on systems, not individuals]

## Lessons Learned
### What went well
- [Bullet points]
### What went poorly
- [Bullet points]
### Where we got lucky
- [Bullet points]

## Action Items
| ID | Action | Priority | Owner | Due | Status |
|----|--------|----------|-------|-----|--------|
| 1 | [Action] | P1 | [Name] | [Date] | Open |
```

## Blameless Postmortem Culture

| Principle | In Practice |
|-----------|------------|
| People are not the root cause | "The pipeline allowed unsafe config" not "Alice deployed bad config" |
| Focus on systems | Identify process gaps, missing guardrails, tooling deficiencies |
| Assume good intentions | Everyone tried to do the right thing with available info |
| No counterfactuals | Not "if only X..." but "what system change prevents this?" |
| Share widely | Postmortems are learning, not shame |
| Track to completion | Postmortems without follow-through teach nothing |

### Incident Timeline Reconstruction Sources

| Source | What It Provides |
|--------|-----------------|
| Alertmanager / PagerDuty | Alert fire/resolve times, ack times, escalations |
| Slack | Human decisions, observations, comms |
| Git / CI | Deploy times, code changes |
| Grafana / Metrics | Anomaly onset, metric correlation |
| Application logs | Error details, trace context |
| Kubernetes events | Pod restarts, OOM kills, scheduling |
| Cloud provider | Infrastructure changes, regional outages |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| No severity classification | Every incident treated the same | Define and enforce severity matrix |
| Hero culture | One person handles all incidents, burns out | Build rotation with 5+ engineers, document in runbooks |
| Blame-driven postmortems | People hide mistakes, learning stops | Enforce blameless process, focus on systems |
| No runbooks | Responders waste 20+ minutes figuring out what to do | Require runbook link on every alert |
| Postmortems without action items | Same incident recurs | Track items in sprint backlog with owners and deadlines |
| Alert without context | "Check failed" with no links | Include dashboard, runbook, impact in every alert |
| No communication plan | Stakeholders flood war room | Assign comms lead, use status page templates |
| Skipping postmortem for small incidents | Miss patterns that compound | Postmortem SEV1-2, lightweight review SEV3 |
| Testing in prod without rollback plan | "Quick fix" makes things worse | Always have rollback command ready first |
| Ignoring near-misses | Only learning from actual incidents | Track and review near-misses monthly |
| War room without clear roles | Everyone talks, nobody acts | Assign IC, Comms, Ops, Scribe at start |
| Over-classifying severity | Everything is SEV1, diluted response | Calibrate quarterly, push back on inflation |

## Incident Readiness Checklist

### Infrastructure

- [ ] On-call rotation configured with primary and secondary
- [ ] Escalation policy tested end-to-end (alert -> page -> ack -> resolve)
- [ ] PagerDuty / OpsGenie integrated with monitoring stack
- [ ] Incident Slack channel creation automated (bot or `/incident`)
- [ ] Status page configured with component hierarchy

### Process

- [ ] Severity classification matrix documented and team-trained
- [ ] War room protocol documented with role descriptions
- [ ] Communication templates ready (status page, internal, customer)
- [ ] Escalation matrix documented (who to call, when)
- [ ] Postmortem template in shared repository
- [ ] Action item tracking integrated with sprint planning

### Runbooks

- [ ] Every critical alert has a linked runbook
- [ ] Runbooks include diagnosis steps with actual commands
- [ ] Runbooks include mitigation options with verification
- [ ] Runbooks reviewed and updated quarterly

### Practice

- [ ] Game day / incident simulation conducted quarterly
- [ ] New on-call engineers shadow for one rotation first
- [ ] Postmortem review within 48 hours of SEV1/SEV2
- [ ] Monthly review of incident trends (frequency, MTTR, severity)
- [ ] Quarterly review of on-call burden (pages per shift, wake-ups)
