---
name: advanced-ssr-cache-design
description: Engineer SSR caching strategies that preserve correctness under concurrent updates and streaming.
---

# Advanced SSR Cache Design (React 18)

## Summary

Engineer SSR caching strategies that preserve correctness under concurrent updates and streaming.

## Key Capabilities

- Design cache keys that include routing and personalization parameters.
- Implement safe cache invalidation with deterministic outcomes.
- Integrate cache policy with streaming SSR.

## PhD-Level Challenges

- Formalize correctness conditions for SSR cache hits.
- Analyze cache coherence across distributed render nodes.
- Derive optimal cache TTL under churn.

## Acceptance Criteria

- Provide cache policy documentation and tests.
- Demonstrate correctness under concurrent personalization.
- Report cache hit ratios before/after tuning.

