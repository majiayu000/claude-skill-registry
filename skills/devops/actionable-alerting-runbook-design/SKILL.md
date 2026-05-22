---
name: actionable-alerting-runbook-design
version: "1.0"
description: >
  Designing effective alerts and runbooks for incident response.
  PROACTIVELY activate for: (1) Creating alerting rules, (2) Writing runbooks,
  (3) Reducing alert fatigue, (4) On-call escalation setup, (5) Incident response procedures.
  Triggers: "alerting", "runbook", "on-call", "pagerduty", "incident", "alert fatigue", "escalation", "playbook"
core-integration:
  techniques:
    primary: ["systematic_analysis"]
    secondary: ["structured_evaluation"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Actionable Alerting and Runbook Design

This skill provides expertise in designing alerts and runbooks for effective incident response.

## Overview

Good alerting enables quick incident detection and resolution. Bad alerting causes fatigue and missed issues.

## Alerting Principles

### What Makes an Alert Actionable?

1. **Specific**: Clear about what's wrong
2. **Contextual**: Includes relevant information
3. **Timely**: Fires before users notice
4. **Actionable**: Recipient can do something about it
5. **Linked**: Points to runbook or dashboard

### Alert Anti-Patterns

- **Flapping alerts**: Constantly firing and resolving
- **Too sensitive**: Alerts on normal variance
- **No runbook**: Alert with no remediation guidance
- **Wrong audience**: Alerting people who can't help

## Runbook Structure

```markdown
# Alert: High API Error Rate

## Summary
API error rate exceeds 5% for 5 minutes

## Impact
Users experiencing failed requests

## Diagnosis Steps
1. Check error logs: [link]
2. Check recent deployments: [link]
3. Check database health: [link]

## Remediation Steps
1. If recent deployment, rollback: `kubectl rollout undo...`
2. If database issue, scale: `gcloud sql instances patch...`
3. If unknown, escalate to: @team-leads

## Escalation
- L1: On-call engineer
- L2: Team lead (if not resolved in 15min)
- L3: VP Engineering (if customer impact > 30min)
```

## Best Practices

1. Alert on symptoms, not causes
2. Use multi-window alerting to reduce noise
3. Include dashboards and runbook links in alerts
4. Review and prune alerts quarterly
5. Track alert-to-incident ratio

[Content to be expanded based on plugin_spec_agentient-observability.md specifications]
