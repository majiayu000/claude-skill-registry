---
name: concurrent-safe-state-machines
description: Design deterministic state machines that remain correct under concurrent rendering and re-entrancy.
---

# Concurrent-Safe State Machines (React 18)

## Summary

Design deterministic state machines that remain correct under concurrent rendering and re-entrancy.

## Key Capabilities

- Apply idempotent reducers and effect cleanup patterns.
- Model state transitions as pure functions with replay tolerance.
- Prevent torn reads during interleaved renders.

## PhD-Level Challenges

- Prove invariants under double-invocation in StrictMode.
- Provide a correctness argument for side-effect isolation.
- Stress-test state transitions under randomized scheduling.

## Acceptance Criteria

- Document state invariants and transition table.
- Demonstrate correctness under StrictMode double effects.
- Provide property-based tests for state machine correctness.

