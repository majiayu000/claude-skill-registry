---
name: incident-response
description: Handle production incidents: diagnose, mitigate, resolve, learn from failures
category: DevOps Operations
---

# Skill: incident-response

## What I do

I provide the technical expertise to handle production incidents effectively. I focus on rapid diagnosis, swift mitigation to restore service, and systematic resolution of the underlying issue, all while ensuring that every failure becomes a learning opportunity.

## When to use me

- When an alert is triggered (e.g., high error rate, service down)
- During a production outage or significant performance degradation
- When a security breach or vulnerability is detected
- To coordinate technical efforts across teams during an incident

## Core principles

1. **Mitigate before you root cause** — Stop the bleeding first. Restore service through workarounds or rollbacks before spending too much time on a deep diagnosis.
2. **OODA Loop (Observe-Orient-Decide-Act)** — Continuously evaluate new information and adapt the response strategy.
3. **Roles and Responsibilities** — Clearly define the Incident Commander, Communications Lead, and Technical Leads to avoid duplication of effort.
4. **Log everything** — Maintain a detailed timeline of actions, observations, and decisions for the post-incident review.

## Patterns & examples

**Incident Severity Classification (P0-P3):**
- **P0 (Critical)**: Total system outage. Core business functionality is unavailable.
- **P1 (High)**: Significant impact. Key feature unavailable or performance severely degraded for many users.
- **P2 (Medium)**: Partial impact. Some features unavailable, but core functionality remains.
- **P3 (Low)**: Minor impact. UI bugs, non-critical features, or performance issues for a small group of users.

**Response Sequence:**
1. **Identify**: Detect the issue via monitoring or user reports.
2. **Mitigate**: Apply a quick fix (e.g., rollback, kill switch, cache clear) to restore service.
3. **Resolve**: Fix the root cause once the system is stable.
4. **Review**: Perform a blameless post-mortem to prevent recurrence.

## Anti-patterns to avoid

- ❌ **The "Lone Wolf" approach** — Attempting to fix a major incident without informing others or asking for help.
- ❌ **Speculating in public** — Guessing the root cause in stakeholder channels before it's confirmed.
- ❌ **Fixing forward without a rollback plan** — Applying a patch that might make things worse without a way to undo it.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/DevOps-Operations/Incident Response.md`

## Related skills

- `incident-communication` — Coordinating stakeholder updates
- `monitoring` — Detecting and observability
- `rollback-recovery` — Swiftly undoing problematic changes
- `blameless-postmortem` — Learning from technical failures
- `logging-observability` — Using logs and traces for diagnosis
