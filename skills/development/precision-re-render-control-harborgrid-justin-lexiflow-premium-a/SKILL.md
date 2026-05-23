---
name: precision-re-render-control
description: Minimize unnecessary re-renders through precise state partitioning and selector-driven updates.
---

# Precision Re-render Control (React 18)

## Summary

Minimize unnecessary re-renders through precise state partitioning and selector-driven updates.

## Key Capabilities

- Implement selector-based memoization for fine-grained updates.
- Partition global state to isolate hot paths.
- Detect referential instability and eliminate it.

## PhD-Level Challenges

- Construct a formal model of re-render propagation.
- Prove minimality of renders under defined constraints.
- Evaluate selector stability with adversarial updates.

## Acceptance Criteria

- Provide render-count baselines and improvements.
- Demonstrate stable selectors with no thrashing.
- Document state partition strategy.

