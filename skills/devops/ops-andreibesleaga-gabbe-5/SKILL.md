---
name: reliability-sre
description: Apply SRE principles (SLO, Error Budget, Chaos Engineering).
context_cost: medium
---
# Reliability & SRE Skill

## Triggers
- sre
- reliability
- slo
- sli
- error budget
- chaos engineering
- postmortem
- incident
- oncall

## Purpose
To treat operations as a software problem and balance improved reliability with feature velocity.

## Capabilities

### 1. Service Level Objectives (SLO)
-   **SLI**: What you measure (e.g., Latency < 100ms).
-   **SLO**: The target (e.g., 99.9% of requests meet SLI).
-   **Structure**: 28-day rolling window. 99.9% = 43m downtime.

### 2. Error Budgets
-   **Definition**: `1 - SLO`. The allowed unreliability.
-   **Policy**: If budget is exhausted -> Freeze feature launches -> Focus on stability.

### 3. Incident Management
-   **Postmortems**: Blameless analysis of *process* failure, not *human* error.
-   **Severity Levels**: SEV1 (Critical/Down) to SEV4 (Minor bug).
-   **MTTR**: Mean Time To Recovery (Focus on fixing fast, not just preventing failure).

## Instructions
1.  **Define Golden Signals**: Latency, Traffic, Errors, Saturation.
2.  **Chaos Engineering**: Test failure modes *before* they happen in production.
3.  **Alerting**: Alert on *symptoms* (User Pain), not *causes* (CPU High).

## Deliverables
-   `slo-definition.md`: Document metrics and targets.
-   `runbook.md`: Step-by-step recovery guide for on-call.
-   `postmortem.md`: Incident analysis.
