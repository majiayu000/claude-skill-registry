---
name: triage-workflow
description: Standardize issue and pull request triage so incoming work is labeled,
  prioritized, and routed consistently.
---

# Triage Workflow

## Purpose
Standardize issue and pull request triage so incoming work is labeled, prioritized, and routed consistently.

## When to Use
- New issues or PRs arrive
- Weekly triage cadence
- Security-related reports appear

## Steps
1. Validate the report has enough context and reproduction details.
2. Apply type labels (`bug`, `enhancement`, `documentation`, `question`, `security`).
3. Apply area labels (`area/swift`, `area/javascript`, `area/ci`, `area/docs`, `area/examples`).
4. Apply priority (`priority/critical`, `priority/high`, `priority/normal`, `priority/low`).
5. Assign or add to the appropriate milestone/backlog.
6. For security reports, route to the Security Contact and restrict visibility.
7. Apply staleness policy if applicable and add `keep-open` to exempt.

## Output Contract
- Issue/PR has correct labels and priority.
- Ownership or next action is clear (assignee or milestone).
- Security items are escalated and handled privately.
