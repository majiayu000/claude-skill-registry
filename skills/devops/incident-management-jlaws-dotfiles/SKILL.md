---
name: incident-management
description: Use when building runbooks, responding to incidents, handling on-call handoffs, or writing postmortems.
---

# Incident Management

## Severity Framework

| Severity | Impact | Response Time | Example |
|----------|--------|---------------|---------|
| **SEV1** | Complete outage, data loss | 15 min | Production down |
| **SEV2** | Major degradation | 30 min | Critical feature broken |
| **SEV3** | Minor impact | 2 hours | Non-critical bug |
| **SEV4** | Minimal impact | Next business day | Cosmetic issue |

## Runbook Structure

Every runbook needs: Overview, Detection, Triage, Mitigation, Root Cause, Resolution, Verification, Escalation.

### Triage Decision Table

| Symptom | Likely Cause | Action |
|---------|--------------|--------|
| All requests failing | Service down | Rollback |
| High latency | Database/dependency | Check connections |
| Partial failures | Code bug | Feature flag disable |
| Spike in errors | Traffic surge | Scale up |

### Escalation Triggers

**Immediate:** SEV1, data breach, unable to diagnose within 30 min
**Consider:** Spans multiple teams, requires expertise you lack, uncertain about next steps

| Condition | Escalate To |
|-----------|-------------|
| > 15 min unresolved SEV1 | Engineering Manager |
| Data breach suspected | Security Team |
| Customer communication needed | Support Lead |

## On-Call Handoff

### Required Components

| Component | Purpose |
|-----------|---------|
| Active Incidents | What's currently broken |
| Ongoing Investigations | Issues being debugged |
| Recent Changes | Deployments, configs |
| Known Issues | Workarounds in place |
| Upcoming Events | Maintenance, releases |

### Handoff Timing

30 min overlap: outgoing writes handoff (15 min) + sync call (15 min). Incoming reviews + verifies alerting.

### Pre-Shift Checklist

- [ ] VPN, kubectl, database, log aggregator access
- [ ] PagerDuty shows you as primary
- [ ] Phone notifications enabled
- [ ] Test alert received
- [ ] Review recent incidents (past 2 weeks)

### Mid-Incident Handoff (Critical)

Must transfer: current state + metrics, what's been tried, root cause theories, next steps with escalation triggers, key people involved.

## Postmortem Writing

### Blameless Culture

| Blame-Focused | Blameless |
|---------------|-----------|
| "Who caused this?" | "What conditions allowed this?" |
| Punish individuals | Improve systems |
| Hide information | Share learnings |

### Timeline

```
Day 0: Incident occurs
Day 1-2: Draft postmortem
Day 3-5: Postmortem meeting (60 min)
Day 5-7: Finalize, create tickets
Week 2+: Action item completion
Quarterly: Review patterns
```

### Required Sections

1. **Executive Summary** -- 1-2 sentences: what, impact, resolution
2. **Timeline (UTC)** -- timestamped events
3. **Root Cause (5 Whys)** -- keep asking "why" until you hit a systemic issue
4. **Detection** -- what worked, what didn't
5. **Response** -- what worked, what could improve
6. **Lessons Learned** -- went well, went wrong, got lucky
7. **Action Items** -- priority, owner, due date, ticket (always concrete)

### Meeting Structure (60 min)

1. Opening (5 min) -- remind blameless culture
2. Timeline review (15 min)
3. Analysis (20 min) -- what failed, why, prevention
4. Action items (15 min) -- prioritize, assign owners
5. Closing (5 min) -- confirm owners

### Postmortem Anti-Patterns

- Blame game instead of systems focus
- Shallow analysis (ask "why" 5 times)
- No action items or unrealistic ones
- No follow-up -- track in ticketing system

## Communication Templates

**Initial:**
```
INCIDENT: [Service] Degradation
Severity: [SEV] | Status: Investigating | Impact: [description]
Start Time: [TIME] | Incident Commander: [NAME]
Updates in [channel]
```

**Resolution:**
```
RESOLVED: [Service] Incident
Duration: [X] minutes | Impact: [affected users/transactions]
Root Cause: [brief] | Resolution: [what was done]
Follow-up: Postmortem scheduled [DATE]
```
