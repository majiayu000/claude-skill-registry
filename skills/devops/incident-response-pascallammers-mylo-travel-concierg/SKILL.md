---
name: incident-response
description: Respond to production incidents systematically with triage, investigation, resolution, and post-mortem analysis to minimize downtime and prevent recurrence. Use when handling production outages, triaging incidents, investigating critical bugs, coordinating incident response, implementing hotfixes, conducting post-mortems, or establishing incident response procedures.
---

# Incident Response - Production Issue Management

## When to use this skill

- Responding to production outages
- Triaging critical incidents
- Investigating high-severity bugs
- Coordinating incident response teams
- Implementing emergency hotfixes
- Conducting post-mortem analyses
- Establishing incident response procedures
- Communicating status during incidents
- Creating runbooks for common issues
- Implementing rollback strategies
- Documenting incident timelines
- Preventing incident recurrence

## When to use this skill

- Responding to outages, managing incidents, conducting postmortems.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Responding to outages, managing incidents, conducting postmortems.

## Incident Response Process

### 1. Detect
- Monitoring alerts
- User reports
- Automated checks

### 2. Triage
- Assess severity (P0-P4)
- Page on-call engineer
- Create incident channel

### 3. Mitigate
- Rollback to last known good
- Scale resources
- Apply hotfix
- Communicate status

### 4. Resolve
- Verify fix
- Monitor metrics
- Update status page
- Close incident

### 5. Postmortem
- Timeline of events
- Root cause analysis
- Action items
- Follow-up tasks

## Severity Levels
- **P0 (Critical)**: Complete outage, data loss
- **P1 (High)**: Major feature broken, revenue impact
- **P2 (Medium)**: Degraded performance, workaround exists
- **P3 (Low)**: Minor bug, cosmetic issue
- **P4 (Informational)**: Enhancement request

## Example Runbook
\`\`\`markdown
# High CPU Usage Runbook

## Symptoms
- Server CPU > 90%
- Slow response times
- Request timeouts

## Investigation
1. Check top processes: \`top\`
2. Check memory: \`free -h\`
3. Check logs: \`tail -f app.log\`

## Mitigation
1. Scale horizontally: Add servers
2. Restart service: \`systemctl restart app\`
3. Rate limit: Enable aggressive rate limiting

## Resolution
1. Identify root cause (N+1 query, memory leak, etc.)
2. Deploy fix
3. Monitor for 1 hour
\`\`\`

## Communication Template
\`\`\`
[INCIDENT] Service X degraded

Status: Investigating
Impact: 20% of users seeing slow load times
ETA: 30 minutes

Updates:
- 10:00 AM: Issue detected
- 10:05 AM: On-call paged, investigation started
- 10:15 AM: Root cause identified (database bottleneck)
- 10:30 AM: Fix deployed, monitoring

Next update: 11:00 AM
\`\`\`

## Resources
- [Incident Management Guide](https://www.pagerduty.com/resources/learn/what-is-incident-management/)
- [Postmortem Template](https://github.com/dastergon/postmortem-templates)
- [PagerDuty](https://www.pagerduty.com/)
