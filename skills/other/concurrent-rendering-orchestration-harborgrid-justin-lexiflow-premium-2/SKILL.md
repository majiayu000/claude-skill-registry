---
name: concurrent-rendering-orchestration
description: Design and validate complex concurrent rendering workflows using `useTransition`, `Suspense`, and selective hydration to preserve responsiveness under heavy workloads.
---

# Concurrent Rendering Orchestration (React 18)

## Summary

Design and validate complex concurrent rendering workflows using `useTransition`, `Suspense`, and selective hydration to preserve responsiveness under heavy workloads.

## Key Capabilities

- Model UI updates as _urgent_ vs _non-urgent_ and coordinate transitions across nested trees.
- Compose `Suspense` boundaries to avoid cascading stalls and over-suspension.
- Implement selective hydration strategies that prioritize user-critical regions.

## PhD-Level Challenges

- Prove liveness properties for a UI state machine under partial rendering.
- Construct a minimal cut set of `Suspense` boundaries for optimal TTI.
- Derive empirical thresholds where `useTransition` improves tail latency.

## Acceptance Criteria

- Demonstrate a UI with nested `Suspense` boundaries and staged reveals.
- Show consistent input responsiveness during large list updates.
- Provide a benchmark report before/after applying transitions.

