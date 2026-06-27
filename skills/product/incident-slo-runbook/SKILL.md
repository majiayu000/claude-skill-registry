---
name: incident-slo-runbook
description: Create or audit SLOs, SLIs, alert rules, incident response steps, escalation paths, postmortems, operational runbooks, and customer-impact communication. Use when defining production reliability, preparing launch readiness, responding to an outage, writing a runbook, tuning alerts, or closing the loop after an incident.
---

# Incident SLO Runbook

## Purpose

Use this skill to connect observability to action. Metrics and logs are not enough; each critical user journey needs an SLO, alert, owner, response path, and post-incident learning loop.

## SLO Design

Define:

1. User journey or system capability.
2. SLI: request success, latency, freshness, durability, or job completion.
3. SLO target and measurement window.
4. Error budget and burn-rate alerts.
5. Exclusions with rationale.
6. Dashboard and data source.
7. Owner and escalation path.

Avoid vanity metrics. Prefer user-visible success and latency over internal counters unless internal counters are the only reliable proxy.

## Runbook Requirements

Each runbook should include:

- Symptom and alert name.
- Impacted users or systems.
- First 5-minute checks.
- Triage decision tree.
- Mitigation steps with commands.
- Rollback or failover path.
- Escalation owner.
- Customer/support communication note.
- Postmortem trigger.

Commands must be safe to run or explicitly labeled destructive.

## Incident Flow

1. Declare severity and incident commander.
2. Confirm impact from live evidence.
3. Stabilize with the lowest-risk mitigation.
4. Communicate status on a fixed cadence.
5. Preserve evidence before cleanup.
6. Write a blameless postmortem with action items and owners.

## Output Shape

```text
service_or_journey:
slo:
alerts:
dashboard_or_queries:
runbook:
escalation:
postmortem_template:
verification:
```
