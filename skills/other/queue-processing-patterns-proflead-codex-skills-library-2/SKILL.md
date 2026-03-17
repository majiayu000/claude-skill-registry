---
name: queue-processing-patterns
description: Design safe queue consumers and retries. Use when a mid-level developer needs reliable background processing.
---

# Queue Processing Patterns

## Purpose
Design safe queue consumers and retries.

## Inputs to request
- Queue system and delivery semantics.
- Idempotency requirements.
- Failure modes and retry limits.

## Workflow
1. Define idempotency and retry policy.
2. Set visibility timeout and dead-letter routing.
3. Add metrics for lag and failure rates.

## Output
- Queue handling checklist.

## Quality bar
- Ensure retries do not amplify failures.
- Document poison message handling.
