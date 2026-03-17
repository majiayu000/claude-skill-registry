---
name: incident-response
description: Incident triage, cascade prevention, and postmortem methodology. Use when handling production incidents, designing resilience patterns, or conducting chaos engineering exercises.
---

# Incident Response

Structured incident management from detection through postmortem, with resilience patterns for preventing and containing cascading failures.

## When to Use

- Production incident in progress (outage, degradation, data loss)
- Designing circuit breakers, bulkheads, or fallback strategies
- Conducting or planning chaos engineering exercises
- Writing or reviewing postmortem documents
- Establishing on-call procedures and escalation paths

Avoid when:
- The issue is a development-time bug with no production impact
- Designing general system architecture (use system-design instead)

## Quick Reference

| Topic | Load reference |
| --- | --- |
| **Triage Framework** | `skills/incident-response/references/triage-framework.md` |
| **Postmortem Patterns** | `skills/incident-response/references/postmortem-patterns.md` |

## Incident Response Workflow

### Phase 1: Detect

- Alert fires or user report received
- Confirm the issue is real (not a false positive)
- Identify affected services and user impact scope

### Phase 2: Triage

- Classify severity (P0-P3)
- Assign incident commander
- Open communication channel (war room, Slack channel)
- Begin status page updates

### Phase 3: Contain

- Stop the bleeding: rollback, feature flag, traffic shift
- Prevent cascade: circuit breakers, load shedding, bulkhead isolation
- Communicate: stakeholder updates every 15 minutes for P0/P1

### Phase 4: Resolve

- Implement fix (minimal viable fix first)
- Validate in staging if time permits
- Deploy with monitoring and rollback plan ready
- Confirm recovery with metrics returning to baseline

### Phase 5: Postmortem

- Document timeline within 48 hours
- Conduct blameless review with all participants
- Identify root cause and contributing factors
- Assign action items with owners and deadlines
- Update runbooks and alerting based on lessons learned

## Severity Framework

| Level | Impact | Response Time | Examples |
|-------|--------|---------------|---------|
| **P0** | Complete outage, data loss, security breach | Immediate (< 5 min) | Service down, data corruption, credential leak |
| **P1** | Major feature broken, significant user impact | < 30 min | Payment processing failed, auth broken for region |
| **P2** | Degraded performance, partial feature loss | < 4 hours | Elevated latency, non-critical feature unavailable |
| **P3** | Minor issue, workaround available | Next business day | UI glitch, slow report generation, cosmetic error |

## Output

- Incident timeline and severity classification
- Containment actions taken
- Postmortem document with action items
- Updated runbooks and alerting rules

## Common Mistakes

- Skipping severity classification and treating everything as P0
- Making changes without a rollback plan
- Forgetting to communicate status to stakeholders
- Writing postmortems that assign blame instead of identifying systemic issues
- Not following up on postmortem action items
