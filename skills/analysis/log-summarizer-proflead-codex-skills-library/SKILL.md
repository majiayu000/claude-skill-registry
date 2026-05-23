---
name: log-summarizer
description: Summarize noisy logs into likely causes and next steps. Use when a junior developer needs help interpreting logs.
---

# Log Summarizer

## Purpose
Summarize noisy logs into likely causes and next steps.

## Inputs to request
- Log snippet and time range.
- Service or component name.
- Recent deploys or config changes.

## Workflow
1. Group similar errors and identify the first failure.
2. Translate error messages into likely causes.
3. Suggest immediate checks or fixes.

## Output
- Top error groups with counts.
- Likely root cause and next actions.

## Quality bar
- Focus on the earliest failing signal.
- Separate symptoms from root causes.
