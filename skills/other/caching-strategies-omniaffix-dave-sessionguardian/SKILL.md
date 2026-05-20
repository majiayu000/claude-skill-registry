---
name: caching-strategies
description: Identify expensive, pure computations that are called with the same inputs Use when optimizing code performance. Performance category skill.
metadata:
  category: Performance
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_caching_strategies
---

# Caching Strategies

Identify expensive, pure computations that are called with the same inputs. Use memoization for function results. Consider cache invalidation carefully—stale data can cause subtle bugs. Implement appropriate cache eviction (LRU, TTL). For distributed systems, consider cache consistency. Always measure cache hit rates to verify caching is beneficial.