---
name: incident-response
description: Incident management, on-call procedures, and runbook execution.
---

# Incident Response

## Severity Levels

| Level | Description | Response Time |
|-------|-------------|---------------|
| **P1** | Service down | 15 min |
| **P2** | Major degradation | 30 min |
| **P3** | Minor impact | 4 hours |
| **P4** | No impact | Next business day |

## Incident Flow

```
Alert → Acknowledge → Assess → Mitigate → Resolve → Postmortem
          │             │         │
          └── Page ─────┴── Communicate
```

## On-Call Checklist

1. **Acknowledge** alert within SLA
2. **Assess** impact and severity
3. **Communicate** status to stakeholders
4. **Mitigate** - Stop the bleeding
5. **Investigate** root cause
6. **Resolve** underlying issue
7. **Document** in postmortem

## Communication Template

```
🔴 INCIDENT: [Brief description]
Impact: [Who/what is affected]
Status: [Investigating/Mitigating/Resolved]
ETA: [Expected resolution time]
Updates: [Channel/page]
```

## Common Runbooks

### High CPU

1. Identify process: `top -c`
2. Check for runaway processes
3. Scale horizontally if needed
4. Investigate root cause

### Out of Disk

1. Check usage: `df -h`
2. Find large files: `du -sh /* | sort -h`
3. Clear logs/temp files
4. Add storage or archive

### Database Slow

1. Check connections: `SHOW PROCESSLIST`
2. Identify slow queries
3. Kill blocking queries if needed
4. Scale or optimize

## Escalation Path

```
On-Call Engineer (15 min)
    ↓
Team Lead (30 min)
    ↓
Engineering Manager (1 hour)
    ↓
VP Engineering (2 hours)
```
