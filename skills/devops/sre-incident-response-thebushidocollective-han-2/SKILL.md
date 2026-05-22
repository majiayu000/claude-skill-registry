---
name: sre-incident-response
description: Use when responding to production incidents following SRE principles and best practices.
allowed-tools: []
---

# SRE Incident Response

Managing incidents and conducting effective postmortems.

## Incident Severity Levels

### P0 - Critical

- **Impact**: Service completely down or major functionality unavailable
- **Response**: Immediate, all-hands
- **Communication**: Every 30 minutes
- **Examples**: Complete outage, data loss, security breach

### P1 - High

- **Impact**: Significant degradation affecting many users
- **Response**: Immediate, primary on-call
- **Communication**: Every hour
- **Examples**: Elevated error rates, slow response times

### P2 - Medium

- **Impact**: Minor degradation or single component affected
- **Response**: Next business day
- **Communication**: Daily updates
- **Examples**: Single region issue, non-critical feature down

### P3 - Low

- **Impact**: No user impact yet, potential future issue
- **Response**: Track in backlog
- **Communication**: Async
- **Examples**: Monitoring gaps, capacity warnings

## Incident Response Process

### 1. Detection

```
Alert fires → On-call acknowledges → Initial assessment
```

### 2. Triage

```
- Assess severity
- Page additional responders if needed
- Establish incident channel
- Assign incident commander
```

### 3. Mitigation

```
- Identify mitigation options
- Execute fastest safe mitigation
- Monitor for improvement
- Escalate if not improving
```

### 4. Resolution

```
- Verify service health
- Communicate resolution
- Document actions taken
- Schedule postmortem
```

### 5. Follow-up

```
- Conduct postmortem
- Identify action items
- Track completion
- Update runbooks
```

## Incident Roles

### Incident Commander (IC)

- Owns incident response
- Makes decisions
- Coordinates responders
- Manages communication
- Declares incident resolved

### Operations Lead

- Executes technical remediation
- Proposes mitigation strategies
- Implements fixes
- Tests changes

### Communications Lead

- Updates status page
- Posts to incident channel
- Notifies stakeholders
- Prepares external messaging

### Planning Lead

- Tracks action items
- Takes detailed notes
- Monitors responder fatigue
- Coordinates shift changes

## Communication Templates

### Initial Notification

```
🚨 INCIDENT DECLARED - P0

Service: API Gateway
Impact: All API requests failing
Started: 2024-01-15 14:23 UTC
IC: @alice
Status Channel: #incident-001

Current Status: Investigating
Next Update: 30 minutes
```

### Status Update

```
📊 INCIDENT UPDATE #2 - P0

Service: API Gateway
Elapsed: 45 minutes

Progress: Identified root cause as database connection pool exhaustion.
Mitigation: Increasing pool size and restarting services.

ETA to Resolution: 15 minutes
Next Update: 15 minutes or when resolved
```

### Resolution Notice

```
✅ INCIDENT RESOLVED - P0

Service: API Gateway
Duration: 1h 12m
Impact: 100% of API requests failed

Resolution: Increased database connection pool and restarted services.

Next Steps:
- Postmortem scheduled for tomorrow 10am
- Monitoring for recurrence
- Action items being tracked in #incident-001
```

## Blameless Postmortem

### Template

```markdown
# Incident Postmortem: API Outage 2024-01-15

## Summary

On January 15th, our API was completely unavailable for 72 minutes due to
database connection pool exhaustion.

## Impact

- Duration: 72 minutes (14:23 - 15:35 UTC)
- Severity: P0
- Users Affected: 100% of API users (~50,000 requests failed)
- Revenue Impact: ~$5,000 in SLA credits

## Timeline

**14:23** - Alerts fire for elevated error rate
**14:25** - IC paged, incident channel created
**14:30** - Identified all database connections exhausted
**14:45** - Decided to increase pool size
**15:00** - Configuration deployed
**15:15** - Services restarted
**15:35** - Error rate returned to normal, incident resolved

## Root Cause

Database connection pool was sized for normal load (100 connections).
Traffic spike from new feature launch (3x normal) exhausted connections.
No alerting existed for connection pool utilization.

## What Went Well

- Detection was quick (2 minutes from issue start)
- Team assembled rapidly
- Clear communication maintained

## What Didn't Go Well

- No capacity testing before feature launch
- Connection pool metrics not monitored
- No automated rollback capability

## Action Items

1. [P0] Add connection pool utilization monitoring (@bob, 1/17)
2. [P0] Implement automated rollback for deploys (@charlie, 1/20)
3. [P1] Establish capacity testing process (@diana, 1/25)
4. [P1] Increase connection pool to 300 (@bob, 1/16)
5. [P2] Update deployment runbook with load testing (@eve, 1/30)

## Lessons Learned

- Always load test before launching features
- Monitor resource utilization at all layers
- Have rollback mechanisms ready
```

## Runbooks

### Example Runbook

```markdown
# Runbook: High Database Latency

## Symptoms

- Database query times > 500ms
- Elevated API latency
- Alert: DatabaseLatencyHigh

## Impact

Users experience slow page loads. P1 severity if p95 > 1s.

## Investigation

1. Check database metrics in Grafana
   https://grafana.example.com/d/db-overview

2. Identify slow queries:
   ```sql
   SELECT * FROM pg_stat_statements 
   ORDER BY total_time DESC LIMIT 10;
   ```

1. Check for locks:

   ```sql
   SELECT * FROM pg_stat_activity 
   WHERE state = 'active';
   ```

## Mitigation

**Quick fixes:**

- Kill long-running queries if safe
- Add missing indexes if identified
- Scale up read replicas if read-heavy

**Escalation:**
If latency > 2s for > 15 minutes, page DBA team.

## Prevention

- Regular query performance reviews
- Automated index recommendations
- Capacity planning for growth

```

## Best Practices

### Blameless Culture

- Focus on systems, not individuals
- Assume good intentions
- Learn from mistakes
- Reward transparency

### Clear Severity Definitions

- Severity should be based on user impact
- Document response time expectations
- Update definitions based on learnings

### Practice Incident Response

- Run "game days" quarterly
- Practice different scenarios
- Test on-call handoffs
- Review and improve runbooks

### Track Action Items

- Assign owners and due dates
- Review in team meetings
- Close loop on completion
- Measure time to completion
