---
name: performance-hunter
version: 1.0.0
type: optimization
tags: [performance, optimization, profiling, speed, universal]
compatibility: any-project
dependencies: optional
language: any
description: Find and fix performance bottlenecks in ANY language or framework
---

# Performance Hunter - Universal Speed Optimization

## 🎯 When to Use This Skill

Use when experiencing:
- Slow page loads
- High CPU/memory usage
- Sluggish UI responses
- Database timeouts
- API latency issues
- "It used to be faster"

## ⚡ Quick Wins (80/20 Rule)

### The Big 5 Performance Killers (Check These First):
1. **N+1 Queries** - Multiple DB calls in loops
2. **Missing Indexes** - Unindexed database queries
3. **Large Bundles** - Unoptimized assets/dependencies
4. **Memory Leaks** - Unreleased references
5. **Blocking I/O** - Synchronous operations

## 🔍 Step 1: MEASURE (Don't Guess!)

### WITH MCP Tools:
```
"Profile the performance of [feature/endpoint/page]"
"Find performance bottlenecks in my application"
```

### WITHOUT MCP:

#### Quick Measurements:
```bash
# Overall response time
time curl http://localhost:3000/api/endpoint

# Multiple requests
for i in {1..10}; do time curl -s http://localhost:3000 > /dev/null; done

# Database query time (add to your queries temporarily)
console.time('query');
// your database query
console.timeEnd('query');
```

#### Browser Performance (Frontend):
```javascript
// Add performance marks
performance.mark('myFeature-start');
// ... your code ...
performance.mark('myFeature-end');
performance.measure('myFeature', 'myFeature-start', 'myFeature-end');

// View results
performance.getEntriesByType('measure');
```

## 🎯 Step 2: PROFILE (Find Bottlenecks)

### Universal Profiling by Language:

#### JavaScript/Node.js:
```bash
# Built-in profiler
node --inspect app.js
# Open chrome://inspect

# Or use console timing
console.time('operation');
// code
console.timeEnd('operation');
```

#### Python:
```python
import cProfile
import pstats

cProfile.run('your_function()', 'profile_stats')
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative').print_stats(10)
```

#### Java:
```bash
# Use JProfiler or VisualVM
jstack <pid>  # Thread dump
jmap -histo <pid>  # Memory histogram
```

#### Go:
```go
import _ "net/http/pprof"
// Visit http://localhost:6060/debug/pprof/
```

#### Database Profiling:
```sql
-- PostgreSQL
EXPLAIN ANALYZE SELECT ...;

-- MySQL
SET profiling = 1;
SHOW PROFILES;
SHOW PROFILE FOR QUERY 1;

-- MongoDB
db.collection.find().explain("executionStats")
```

## 🔧 Step 3: OPTIMIZE (Fix Bottlenecks)

### 1. Database Optimization

#### WITH MCP (DB Schema Designer):
```
"Optimize my database queries for performance"
```

#### WITHOUT MCP:

**N+1 Query Fix:**
```javascript
// BAD: N+1 queries
const users = await getUsers();
for (const user of users) {
  user.posts = await getPostsByUserId(user.id); // N queries!
}

// GOOD: Single query with join
const usersWithPosts = await getUsersWithPosts(); // 1 query!
```

**Add Indexes:**
```sql
-- Find slow queries first
-- PostgreSQL
SELECT query, calls, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC;

-- Add index
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at);
```

### 2. Frontend Optimization

**Bundle Size:**
```bash
# Analyze bundle
npm run build -- --stats
webpack-bundle-analyzer stats.json

# Common fixes:
# - Lazy load routes
# - Tree shake unused code
# - Use CDN for large libraries
```

**React/Vue Specific:**
```javascript
// Use React.memo/Vue.computed
const ExpensiveComponent = React.memo(({ data }) => {
  // Only re-renders if data changes
});

// Virtualize long lists
import { FixedSizeList } from 'react-window';
```

### 3. Backend Optimization

**Caching Strategy:**
```javascript
// Memory cache for frequently accessed data
const cache = new Map();

async function getExpensiveData(key) {
  if (cache.has(key)) {
    return cache.get(key);
  }

  const data = await expensive_operation();
  cache.set(key, data);

  // TTL (time to live)
  setTimeout(() => cache.delete(key), 60000); // 1 minute

  return data;
}
```

**Async/Parallel Processing:**
```javascript
// BAD: Sequential
for (const item of items) {
  await processItem(item); // Slow!
}

// GOOD: Parallel (with limit)
const pLimit = require('p-limit');
const limit = pLimit(5); // Max 5 concurrent

await Promise.all(
  items.map(item => limit(() => processItem(item)))
);
```

### 4. Memory Optimization

**Find Memory Leaks:**
```javascript
// Node.js
if (global.gc) {
  global.gc();
  const used = process.memoryUsage();
  console.log('Memory:', Math.round(used.heapUsed / 1024 / 1024), 'MB');
}

// Common leak sources:
// - Event listeners not removed
// - Timers not cleared
// - Large objects in closures
// - Circular references
```

**Fix Common Leaks:**
```javascript
// Clean up event listeners
componentWillUnmount() {
  window.removeEventListener('resize', this.handler);
}

// Clear timers
const timer = setTimeout(...);
// Later:
clearTimeout(timer);

// WeakMap for object references
const cache = new WeakMap(); // GC-friendly
```

## 📊 Performance Monitoring

### Quick Monitoring Setup:

```javascript
// Log slow operations
function monitor(fn, name, threshold = 100) {
  return async (...args) => {
    const start = Date.now();
    const result = await fn(...args);
    const duration = Date.now() - start;

    if (duration > threshold) {
      console.warn(`⚠️ Slow operation: ${name} took ${duration}ms`);
    }

    return result;
  };
}

// Usage
const fastQuery = monitor(slowQuery, 'UserQuery', 50);
```

## 🚀 Quick Performance Checklist

### Frontend:
- [ ] Bundle size < 300KB (gzipped)
- [ ] First Contentful Paint < 1.8s
- [ ] Time to Interactive < 3.8s
- [ ] No layout shifts (CLS < 0.1)
- [ ] Images optimized (WebP, lazy loading)
- [ ] Code splitting implemented
- [ ] Service worker for caching

### Backend:
- [ ] API response time < 200ms (p95)
- [ ] Database queries < 50ms
- [ ] Connection pooling configured
- [ ] Rate limiting implemented
- [ ] Response compression enabled
- [ ] Static assets CDN cached
- [ ] Background jobs for heavy tasks

### Database:
- [ ] All queries use indexes
- [ ] No N+1 queries
- [ ] Connection pool sized correctly
- [ ] Read replicas for heavy reads
- [ ] Pagination for large datasets
- [ ] Vacuum/analyze scheduled (PostgreSQL)
- [ ] Query cache enabled (MySQL)

## 💡 Language-Specific Quick Wins

### Node.js:
```javascript
// Use cluster for multi-core
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

if (cluster.isMaster) {
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
}
```

### Python:
```python
# Use built-in accelerators
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(param):
    # Cached after first call
    return complex_calculation(param)
```

### Java:
```java
// Use StringBuilder for string concatenation
StringBuilder sb = new StringBuilder();
for (String s : strings) {
    sb.append(s); // Much faster than + operator
}
```

## 🎯 Performance Goals by Type

### Web Application:
- Page load: < 3 seconds
- API calls: < 500ms
- Search: < 200ms
- Form submit: < 1 second

### Mobile App:
- Launch: < 2 seconds
- Screen transition: < 300ms
- List scroll: 60 FPS
- Network retry: Exponential backoff

### API Service:
- p50 latency: < 50ms
- p95 latency: < 200ms
- p99 latency: < 1 second
- Error rate: < 0.1%

## 📈 Before/After Metrics Template

```markdown
## Performance Optimization Report

### Metric | Before | After | Improvement
---------|---------|--------|-------------
Page Load | 4.2s | 1.8s | -57%
API Response | 800ms | 180ms | -77%
Memory Usage | 512MB | 320MB | -37%
Bundle Size | 1.2MB | 420KB | -65%

### Changes Made:
1. Added database indexes
2. Implemented caching layer
3. Enabled gzip compression
4. Lazy loaded images
5. Code split routes
```

Remember: Measure → Profile → Optimize → Verify! 🚀