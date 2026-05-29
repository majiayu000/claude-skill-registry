---
name: resource-cache-invalidation
description: Implement advanced caching with precise invalidation for highly dynamic data domains.
---

# Resource Cache Invalidation (React 18)

## Summary

Implement advanced caching with precise invalidation for highly dynamic data domains.

## Key Capabilities

- Design multi-tier caches (in-memory + persisted) with TTL policies.
- Implement versioned cache keys to prevent stale hydration.
- Use dependency-based invalidation with minimal recomputation.

## PhD-Level Challenges

- Formally reason about cache staleness windows and correctness.
- Analyze invalidation cascades in high-churn data graphs.
- Derive optimal TTL under changing network conditions.

## Acceptance Criteria

- Provide cache hit-rate analysis before/after improvements.
- Demonstrate deterministic cache invalidation behavior.
- Document consistency guarantees and failure modes.

