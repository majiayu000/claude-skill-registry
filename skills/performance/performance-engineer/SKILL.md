---
name: performance-engineer
description: Performance optimization specialist for improving application speed and efficiency. Use when investigating performance issues or optimizing code.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Performance Engineer

Specialist in analyzing and optimizing application performance, identifying bottlenecks, and implementing efficiency improvements.

## When This Skill Activates

Activates when you:
- Report performance issues
- Need performance optimization
- Mention "slow" or "latency"
- Want to improve efficiency

## Performance Analysis Process

### Phase 1: Identify the Problem

1. **Define metrics**
   - What's the baseline?
   - What's the target?
   - What's acceptable?

2. **Measure current performance**
   ```bash
   # Response time
   curl -w "@curl-format.txt" -o /dev/null -s https://example.com/users

   # Database query time
   # Add timing logs to queries

   # Memory usage
   # Use profiler
   ```

3. **Profile the application**
   ```bash
   # Node.js
   node --prof app.js

   # Python
   python -m cProfile app.py

   # Go
   go test -cpuprofile=cpu.prof
   ```

### Phase 2: Find the Bottleneck

Common bottleneck locations:

| Layer | Common Issues |
|-------|---------------|
| **Database** | N+1 queries, missing indexes, large result sets |
| **API** | Over-fetching, no caching, serial requests |
| **Application** | Inefficient algorithms, excessive logging |
| **Frontend** | Large bundles, re-renders, no lazy loading |
| **Network** | Too many requests, large payloads, no compression |

### Phase 3: Optimize

#### Database Optimization

**N+1 Queries:**
```typescript
// Bad: N+1 queries
const users = await User.findAll();
for (const user of users) {
  user.posts = await Post.findAll({ where: { userId: user.id } });
}

// Good: Eager loading
const users = await User.findAll({
  include: [{ model: Post, as: 'posts' }]
});
```

**Missing Indexes:**
```sql
-- Add index on frequently queried columns
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_post_user_id ON posts(user_id);
```

#### API Optimization

**Pagination:**
```typescript
// Always paginate large result sets
const users = await User.findAll({
  limit: 100,
  offset: page * 100
});
```

**Field Selection:**
```typescript
// Select only needed fields
const users = await User.findAll({
  attributes: ['id', 'name', 'email']
});
```

**Compression:**
```typescript
// Enable gzip compression
app.use(compression());
```

#### Frontend Optimization

**Code Splitting:**
```typescript
// Lazy load routes
const Dashboard = lazy(() => import('./Dashboard'));
```

**Memoization:**
```typescript
// Use useMemo for expensive calculations
const filtered = useMemo(() =>
  items.filter(item => item.active),
  [items]
);
```

**Image Optimization:**
- Use WebP format
- Lazy load images
- Use responsive images
- Compress images

### Phase 4: Verify

1. **Measure again**
2. **Compare to baseline**
3. **Ensure no regressions**
4. **Document the improvement**

## Performance Targets

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| API Response (p50) | < 100ms | < 500ms |
| API Response (p95) | < 500ms | < 1s |
| API Response (p99) | < 1s | < 2s |
| Database Query | < 50ms | < 200ms |
| Page Load (FMP) | < 2s | < 3s |
| Time to Interactive | < 3s | < 5s |
| Memory Usage | < 512MB | < 1GB |

## Common Optimizations

### Caching Strategy

```typescript
// Cache expensive computations
const cache = new Map();

async function getUserStats(userId: string) {
  if (cache.has(userId)) {
    return cache.get(userId);
  }

  const stats = await calculateUserStats(userId);
  cache.set(userId, stats);

  // Invalidate after 5 minutes
  setTimeout(() => cache.delete(userId), 5 * 60 * 1000);

  return stats;
}
```

### Batch Processing

```typescript
// Bad: Individual requests
for (const id of userIds) {
  await fetchUser(id);
}

// Good: Batch request
await fetchUsers(userIds);
```

### Debouncing/Throttling

```typescript
// Debounce search input
const debouncedSearch = debounce(search, 300);

// Throttle scroll events
const throttledScroll = throttle(handleScroll, 100);
```

## Performance Monitoring

### Key Metrics

- **Response Time**: Time to process request
- **Throughput**: Requests per second
- **Error Rate**: Failed requests percentage
- **Memory Usage**: Heap/RAM used
- **CPU Usage**: Processor utilization

### Monitoring Tools

| Tool | Purpose |
|------|---------|
| Lighthouse | Frontend performance |
| New Relic | APM monitoring |
| Datadog | Infrastructure monitoring |
| Prometheus | Metrics collection |

## Scripts

Profile application:
```bash
python scripts/profile.py
```

Generate performance report:
```bash
python scripts/perf_report.py
```

## References

- `references/optimization.md` - Optimization techniques
- `references/monitoring.md` - Monitoring setup
- `references/checklist.md` - Performance checklist
