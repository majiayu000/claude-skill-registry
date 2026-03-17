---
name: deterministic-effects-and-side-effects
description: Master side-effect design under StrictMode and concurrent rendering, ensuring deterministic behavior.
---

# Deterministic Effects and Side Effects (React 18)

## Summary

Master side-effect design under StrictMode and concurrent rendering, ensuring deterministic behavior.

## Key Capabilities

- Design idempotent effects with precise cleanup semantics.
- Prevent race conditions in async effect workflows.
- Use `AbortController` and cancellation patterns consistently.

## PhD-Level Challenges

- Prove effect idempotency under double invocation.
- Analyze effect ordering constraints across nested components.
- Provide a taxonomy of effect hazards and mitigations.

## Acceptance Criteria

- Demonstrate stable effect behavior under StrictMode.
- Provide test cases covering race condition scenarios.
- Document cancellation patterns for async effects.

