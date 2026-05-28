---
name: suspense-data-architectures
description: Engineer data-fetching architectures that fully leverage `Suspense`, streaming SSR, and granular cache invalidation.
---

# Suspense Data Architectures (React 18)

## Summary

Engineer data-fetching architectures that fully leverage `Suspense`, streaming SSR, and granular cache invalidation.

## Key Capabilities

- Build a resource cache with deterministic invalidation boundaries.
- Compose data dependencies across micro-frontends without waterfalling.
- Integrate streaming SSR with client hydration and error recovery.

## PhD-Level Challenges

- Formalize dependency graphs and compute optimal prefetch sets.
- Prove bounded revalidation strategies under concurrent updates.
- Analyze cache coherence trade-offs using real-world latency traces.

## Acceptance Criteria

- Demonstrate Suspense-enabled data loading with abortable fetches.
- Implement error boundaries that isolate failed data segments.
- Provide a diagram of dependency graph and cache invalidation paths.

