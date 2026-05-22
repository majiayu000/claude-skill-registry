---
name: observability-setup
description: Set up metrics, logs, and traces for a service. Use when a mid-level developer needs basic observability coverage.
---

# Observability Setup

## Purpose
Set up metrics, logs, and traces for a service.

## Inputs to request
- Service architecture and key endpoints.
- Existing logging and monitoring tools.
- SLI or reliability targets.

## Workflow
1. Define key service indicators and error budget metrics.
2. Instrument logs with correlation IDs.
3. Set alerts for critical thresholds.

## Output
- Instrumentation checklist and alert plan.

## Quality bar
- Measure user impact, not just system health.
- Avoid noisy alerts by defining clear thresholds.
