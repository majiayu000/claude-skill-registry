---
name: scalable-routing-and-code-splitting
description: Design routing and code-splitting strategies that scale to large applications with minimal load-time overhead.
---

# Scalable Routing and Code Splitting (React 18)

## Summary

Design routing and code-splitting strategies that scale to large applications with minimal load-time overhead.

## Key Capabilities

- Implement route-based and component-based splitting with preloading.
- Coordinate code-splitting with `Suspense` and streaming SSR.
- Optimize preload heuristics based on navigation prediction.

## PhD-Level Challenges

- Model navigation predictions and minimize prefetch waste.
- Prove correctness of lazy-loading error recovery.
- Quantify trade-offs between bundle count and latency.

## Acceptance Criteria

- Demonstrate measurable improvements in initial load time.
- Provide preload heuristics and evaluation results.
- Document error recovery for lazy-loaded routes.

