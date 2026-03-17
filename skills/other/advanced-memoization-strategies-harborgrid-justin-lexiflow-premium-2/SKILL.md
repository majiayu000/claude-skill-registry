---
name: advanced-memoization-strategies
description: Apply principled memoization techniques to reduce re-rendering without introducing correctness bugs.
---

# Advanced Memoization Strategies (React 18)

## Summary

Apply principled memoization techniques to reduce re-rendering without introducing correctness bugs.

## Key Capabilities

- Distinguish structural vs semantic memoization benefits.
- Detect memoization thrashing and unstable dependencies.
- Use fine-grained memoization with stable object identity.

## PhD-Level Challenges

- Construct a formal cost model for memoization trade-offs.
- Prove absence of stale closure bugs under refactoring.
- Quantify memoization impact using real workloads.

## Acceptance Criteria

- Provide before/after render counts for target components.
- Demonstrate stable dependency graphs for memoized hooks.
- Document memoization policy and its rationale.

