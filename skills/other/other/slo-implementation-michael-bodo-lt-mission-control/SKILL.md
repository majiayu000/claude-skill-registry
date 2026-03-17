---
version: 4.1.0-fractal
name: slo-implementation
description: Define and implement Service Level Indicators (SLIs) and Service Level Objectives (SLOs) with error budgets and alerting. Use when establishing reliability targets, implementing SRE practices, or measuring service performance.
---

# SLO Implementation

Framework for defining and implementing Service Level Indicators (SLIs), Service Level Objectives (SLOs), and error budgets.

## Do not use this skill when

- The task is unrelated to slo implementation
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Purpose

Implement measurable reliability targets using SLIs, SLOs, and error budgets to balance reliability with innovation velocity.

## Use this skill when

- Define service reliability targets
- Measure user-perceived reliability
- Implement error budgets
- Create SLO-based alerts
- Track reliability goals

## SLI/SLO/SLA Hierarchy

```
SLA (Service Level Agreement)
  ↓ Contract with customers
SLO (Service Level Objective)
  ↓ Internal reliability target
SLI (Service Level Indicator)
  ↓ Actual measurement
```

## Defining SLIs

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [Common SLI Types](./sub-skills/common-sli-types.md)
### 2. [Availability SLO Examples](./sub-skills/availability-slo-examples.md)
### 3. [Choose Appropriate SLOs](./sub-skills/choose-appropriate-slos.md)
### 4. [Error Budget Formula](./sub-skills/error-budget-formula.md)
### 5. [Error Budget Policy](./sub-skills/error-budget-policy.md)
### 6. [Prometheus Recording Rules](./sub-skills/prometheus-recording-rules.md)
### 7. [SLO Alerting Rules](./sub-skills/slo-alerting-rules.md)
### 8. [Weekly Review](./sub-skills/weekly-review.md)
### 9. [Monthly Review](./sub-skills/monthly-review.md)
### 10. [Quarterly Review](./sub-skills/quarterly-review.md)
