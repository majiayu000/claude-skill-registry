---
name: incident-management
description: Handle production incidents effectively. Use when responding to outages, conducting post-mortems, or improving reliability. Covers incident response and blameless culture.
allowed-tools: Read, Write, Glob, Grep
---

# Incident Management

## Incident Severity

| Level | Impact | Response Time |
|-------|--------|---------------|
| SEV1 | Complete outage | Immediate |
| SEV2 | Major degradation | < 15 min |
| SEV3 | Minor degradation | < 1 hour |
| SEV4 | Low impact | Next business day |

## Incident Response

### 1. Detect
- Monitoring alerts
- Customer reports
- Error logs

### 2. Triage
- Assess severity
- Assign incident commander
- Create communication channel

### 3. Investigate
- Check recent changes
- Review logs and metrics
- Identify root cause

### 4. Mitigate
- Apply quick fix
- Rollback if needed
- Communicate status

### 5. Resolve
- Confirm fix
- Monitor for recurrence
- Close incident

### 6. Learn
- Post-mortem meeting
- Document findings
- Create action items

## Post-Mortem Template

```markdown
# Post-Mortem: [Incident Title]

## Summary
[Brief description of what happened]

## Timeline
- HH:MM - [Event]
- HH:MM - [Event]
- HH:MM - [Resolution]

## Impact
- Duration: [X hours]
- Users affected: [X]
- Revenue impact: [if applicable]

## Root Cause
[What caused this incident]

## Contributing Factors
- [Factor 1]
- [Factor 2]

## What Went Well
- [Positive 1]
- [Positive 2]

## What Could Be Improved
- [Improvement 1]
- [Improvement 2]

## Action Items
- [ ] [Action 1] - Owner: [Name]
- [ ] [Action 2] - Owner: [Name]
```

## Blameless Culture

- Focus on systems, not people
- "What failed?" not "Who failed?"
- Share learnings openly
- Celebrate near-misses
