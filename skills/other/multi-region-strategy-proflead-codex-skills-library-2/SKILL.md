---
name: multi-region-strategy
description: Design a multi-region architecture strategy. Use when a senior developer needs geo-redundant planning.
---

# Multi-Region Strategy

## Purpose
Design a multi-region architecture strategy.

## Inputs to request
- Availability targets and RTO/RPO.
- Data consistency requirements.
- Regions and regulatory constraints.

## Workflow
1. Define availability goals and data consistency.
2. Choose active-active or active-passive patterns.
3. Plan failover testing and monitoring.

## Output
- Multi-region strategy with tradeoffs.

## Quality bar
- Explicitly call out data replication risks.
- Include periodic failover tests.
