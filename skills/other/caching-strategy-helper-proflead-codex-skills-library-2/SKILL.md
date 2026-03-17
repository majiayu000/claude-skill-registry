---
name: caching-strategy-helper
description: Recommend caching strategies and invalidation patterns. Use when a mid-level developer needs performance guidance.
---

# Caching Strategy Helper

## Purpose
Recommend caching strategies and invalidation patterns.

## Inputs to request
- Hot paths and read/write ratios.
- Freshness and consistency requirements.
- Traffic patterns and cache budgets.

## Workflow
1. Identify hot paths, read/write ratios, and freshness needs.
2. Recommend cache type and eviction policy.
3. Outline invalidation triggers and metrics.

## Output
- Caching plan with risks and metrics.

## Quality bar
- Clarify stale data tolerances.
- Include cache hit metrics to validate.
