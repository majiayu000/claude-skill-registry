---
name: performance-profiler
description: Auto-activates when user mentions performance, profiling, optimization, slow code, or bottlenecks. Profiles and optimizes code performance.
category: performance
---

# Performance Profiler

Analyzes and optimizes code performance with actionable recommendations.

## When This Activates

- User says: "profile this", "performance", "optimize", "why is this slow?"
- Code is running slowly
- Before production deployment (performance audit)

## Performance Analysis Checklist

### 1. Time Complexity Analysis
- [ ] Identify algorithm complexity (Big O notation)
- [ ] Find nested loops (O(n²) or worse)
- [ ] Check recursion depth
- [ ] Analyze sort/search operations

### 2. Database Performance
- [ ] Check for N+1 query problems
- [ ] Verify indexes exist on queried columns
- [ ] Analyze query execution plans
- [ ] Check for missing pagination

### 3. Memory Usage
- [ ] Check for memory leaks
- [ ] Analyze object retention
- [ ] Verify proper cleanup (event listeners, timers)
- [ ] Check for large data structures

### 4. Network Performance
- [ ] Check API request count
- [ ] Verify response caching
- [ ] Check for sequential requests (should be parallel)
- [ ] Analyze payload sizes

### 5. Frontend Performance
- [ ] Check bundle size
- [ ] Analyze render performance
- [ ] Verify lazy loading
- [ ] Check for unnecessary re-renders

## Profiling Tools

### JavaScript/TypeScript
```bash
# Node.js profiling
node --prof app.js
node --prof-process isolate-*-v8.log > processed.txt

# Chrome DevTools
# Open DevTools → Performance → Record

# Lighthouse
npx lighthouse https://yoursite.com --view

# Bundle analysis
npx webpack-bundle-analyzer stats.json
```

### Python
```python
# cProfile
python -m cProfile -s cumtime script.py

# line_profiler
@profile
def slow_function():
    # Code to profile
    pass
```

## Common Performance Issues

### Issue 1: N+1 Query Problem

**Bad:**
```javascript
// 1 query to get users + N queries to get posts
const users = await db.query('SELECT * FROM users');
for (const user of users) {
  user.posts = await db.query('SELECT * FROM posts WHERE user_id = $1', [user.id]);
}
```

**Good:**
```javascript
// 1 query with JOIN
const users = await db.query(`
  SELECT u.*, json_agg(p.*) as posts
  FROM users u
  LEFT JOIN posts p ON p.user_id = u.id
  GROUP BY u.id
`);
```

### Issue 2: Missing Indexes

**Diagnosis:**
```sql
-- Check query performance
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';
-- If "Seq Scan", missing index!
```

**Fix:**
```sql
CREATE INDEX idx_users_email ON users(email);
```

### Issue 3: Memory Leak

**Bad:**
```javascript
// Event listener never removed
element.addEventListener('click', handler);
// Memory leak if element is removed from DOM
```

**Good:**
```javascript
const controller = new AbortController();
element.addEventListener('click', handler, {
  signal: controller.signal
});
// Cleanup
controller.abort();
```

### Issue 4: Unnecessary Re-renders (React)

**Bad:**
```javascript
function Component() {
  // Creates new array on every render
  const items = users.map(u => transform(u));
  return <List items={items} />;
}
```

**Good:**
```javascript
function Component() {
  // Memoize expensive computation
  const items = useMemo(
    () => users.map(u => transform(u)),
    [users]
  );
  return <List items={items} />;
}
```

### Issue 5: Large Bundle Size

**Diagnosis:**
```bash
npx webpack-bundle-analyzer dist/stats.json
```

**Fixes:**
```javascript
// Lazy load routes
const Dashboard = lazy(() => import('./Dashboard'));

// Tree-shake unused code
import { specific } from 'library';  // not: import * as lib

// Use lighter alternatives
// lodash (full): 71KB → lodash-es (single function): 1KB
import debounce from 'lodash-es/debounce';
```

## Performance Report

```markdown
## ⚡ Performance Analysis Report

### 📊 Metrics

**Before:**
- Page load: 4.2s
- Time to Interactive (TTI): 5.8s
- First Contentful Paint: 2.1s
- Bundle size: 850KB
- API calls: 15 requests

**After:**
- Page load: 1.8s ✅ (57% faster)
- TTI: 2.3s ✅ (60% faster)
- FCP: 0.9s ✅ (57% faster)
- Bundle size: 320KB ✅ (62% reduction)
- API calls: 3 requests ✅ (80% reduction)

### 🐌 Bottlenecks Found

1. **N+1 Query Problem** (src/api/users.ts:45)
   - Impact: 2.5s added to response time
   - Fix: Use JOIN query instead of loop
   - Priority: HIGH

2. **Missing Index** (users.email)
   - Impact: 800ms per query
   - Fix: `CREATE INDEX idx_users_email ON users(email)`
   - Priority: HIGH

3. **Large Bundle** (moment.js: 280KB)
   - Impact: 1.2s additional load time
   - Fix: Replace with date-fns (11KB)
   - Priority: MEDIUM

4. **Unnecessary Re-renders** (Dashboard component)
   - Impact: Laggy UI, CPU usage
   - Fix: Add React.memo() and useMemo()
   - Priority: MEDIUM

### ✅ Optimizations Applied

1. Implemented query batching → **2.5s saved**
2. Added database indexes → **800ms saved per query**
3. Replaced heavy libraries → **530KB bundle reduction**
4. Memoized React components → **60% fewer renders**
5. Enabled response caching → **70% fewer API calls**

### 📈 Performance Score

- **Before:** 45/100 (Poor)
- **After:** 92/100 (Excellent) ✅

### 💡 Next Steps

1. Implement lazy loading for dashboard routes
2. Add CDN for static assets
3. Enable HTTP/2 server push
4. Consider service worker for offline support
```

## Benchmarking

```javascript
// Measure execution time
console.time('operation');
expensiveOperation();
console.timeEnd('operation');

// More precise
const start = performance.now();
expensiveOperation();
const end = performance.now();
console.log(`Took ${end - start}ms`);

// Benchmark multiple runs
function benchmark(fn, runs = 100) {
  const times = [];
  for (let i = 0; i < runs; i++) {
    const start = performance.now();
    fn();
    times.push(performance.now() - start);
  }
  const avg = times.reduce((a, b) => a + b) / times.length;
  console.log(`Average: ${avg}ms`);
  console.log(`Min: ${Math.min(...times)}ms`);
  console.log(`Max: ${Math.max(...times)}ms`);
}
```

## Performance Budget

Set performance budgets:

```json
{
  "budgets": [
    {
      "resourceSizes": [
        { "resourceType": "script", "budget": 300 },
        { "resourceType": "total", "budget": 500 }
      ]
    },
    {
      "timings": [
        { "metric": "interactive", "budget": 3000 },
        { "metric": "first-contentful-paint", "budget": 1000 }
      ]
    }
  ]
}
```

## Best Practices

✅ **DO:**
- Profile before optimizing (measure first!)
- Focus on bottlenecks (80/20 rule)
- Use production mode for realistic metrics
- Test with realistic data sizes
- Measure impact of optimizations

❌ **DON'T:**
- Premature optimization
- Optimize without profiling
- Sacrifice readability for micro-optimizations
- Forget to test after optimizations
- Optimize everything at once

**Profile code, identify bottlenecks, suggest optimizations, measure improvements.**
