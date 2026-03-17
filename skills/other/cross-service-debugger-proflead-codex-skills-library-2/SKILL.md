---
name: cross-service-debugger
description: Coordinate debugging across multiple services. Use when a senior developer needs to trace a distributed issue.
---

# Cross-Service Debugger

## Purpose
Coordinate debugging across multiple services.

## Inputs to request
- Request IDs and trace context.
- Service list and ownership.
- Time window and environment.

## Workflow
1. Gather request IDs and trace context.
2. Correlate logs across services and time ranges.
3. Isolate the failing hop and propose fixes.

## Output
- Cross-service trace summary and next steps.

## Quality bar
- Anchor analysis on a single request ID.
- Distinguish upstream vs downstream errors.
