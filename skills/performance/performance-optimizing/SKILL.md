---
name: 'performance-optimizing'
description: 'Identifies and fixes performance bottlenecks. Use when optimizing code performance, fixing slow operations, or when asked to improve speed.'
---

# Performance Optimizing

## Optimization Workflow

1. **Measure first** - Don't optimize without data
2. **Find bottlenecks** - Profile to identify hot paths
3. **Fix the biggest issue** - Pareto principle (80/20)
4. **Measure again** - Verify improvement
5. **Document** - Record what changed and why

## Common Bottlenecks

### Database

| Problem          | Solution                          |
| ---------------- | --------------------------------- |
| N+1 queries      | Eager loading, batching           |
| Missing indexes  | Add indexes on WHERE/JOIN columns |
| Full table scans | Optimize queries, add indexes     |
| Over-fetching    | Select only needed columns        |

```typescript
// Bad - N+1 queries
for (const user of users) {
  const posts = await db.posts.findByUserId(user.id);
}

// Good - single query with join
const usersWithPosts = await db.users.findAll({
  include: ['posts'],
});
```

### Memory

| Problem         | Solution                      |
| --------------- | ----------------------------- |
| Memory leaks    | Clear references, use WeakMap |
| Large objects   | Stream processing, pagination |
| Duplicated data | Normalize, use references     |

### CPU

| Problem                | Solution               |
| ---------------------- | ---------------------- |
| Blocking operations    | Use async/workers      |
| Redundant computation  | Memoization, caching   |
| Inefficient algorithms | Better data structures |

```typescript
// Bad - O(n) lookup on every iteration
for (const item of items) {
  if (list.includes(item.id)) { ... }
}

// Good - O(1) lookup with Set
const idSet = new Set(list);
for (const item of items) {
  if (idSet.has(item.id)) { ... }
}
```

### Network

| Problem           | Solution                |
| ----------------- | ----------------------- |
| Too many requests | Batching, HTTP/2        |
| Large payloads    | Compression, pagination |
| No caching        | HTTP caching, CDN       |

## Quick Wins

1. **Add indexes** on frequently queried columns
2. **Enable compression** (gzip/brotli)
3. **Implement caching** at appropriate layers
4. **Use pagination** for large datasets
5. **Lazy load** non-critical resources

## Anti-Patterns

- Premature optimization without measurement
- Micro-optimizations that hurt readability
- Caching everything (cache invalidation is hard)
- Optimizing cold paths
