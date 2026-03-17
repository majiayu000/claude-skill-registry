---
name: performance-optimization
description: Systematic approach to identifying and resolving performance bottlenecks in software systems. Use when application response times exceed SLAs, resource usage is high, before scaling infrastructure, during performance testing, or when users report slowness.
---

# Performance Optimization Skill

## Core Principle

**Measure first, optimize second. Never guess at performance.**

Performance optimization without measurement is guesswork. Every optimization must:

- **Start with profiling** — Identify actual bottlenecks, not assumed ones
- **Establish baselines** — Know current performance before changing anything
- **Measure impact** — Verify optimizations actually improve performance
- **Avoid premature optimization** — Optimize based on real-world needs, not theoretical concerns
- **Consider trade-offs** — Every optimization has costs (complexity, maintainability, development time)

---

## When to Optimize

### Good Times to Optimize

✅ **SLA violations** — Response times consistently exceed service level agreements
✅ **High resource usage** — CPU, memory, or I/O consistently at capacity
✅ **Before scaling** — Optimize code before throwing more hardware at the problem
✅ **User complaints** — Real users reporting slowness or timeouts
✅ **Performance testing** — During regular performance validation cycles
✅ **After profiling** — When bottlenecks are identified and measured

### Bad Times to Optimize

❌ **Without profiling** — Don't optimize without knowing where the bottleneck is
❌ **Premature optimization** — Don't optimize before you have performance problems
❌ **During feature development** — Build it first, optimize later
❌ **Without tests** — Can't verify correctness after optimization
❌ **Based on hunches** — "I think this is slow" without measurement

---

## Performance Profiling

### Profiling Categories

#### 1. CPU Profiling

**What it measures:** Where CPU time is spent in your code

**When to use:**
- High CPU usage
- Slow computation or algorithms
- Long request processing times

**Tools by language:**

**Python:**
```bash
# cProfile - built-in profiler
python -m cProfile -s cumulative script.py

# py-spy - sampling profiler (no code changes needed)
py-spy record -o profile.svg -- python script.py

# line_profiler - line-by-line profiling
kernprof -l -v script.py
```

**JavaScript/Node.js:**
```bash
# Chrome DevTools
node --inspect script.js
# Open chrome://inspect

# clinic.js - Node.js performance profiling
clinic doctor -- node script.js
clinic flame -- node script.js

# Built-in profiler
node --prof script.js
node --prof-process isolate-*.log
```

**Go:**
```bash
# pprof - built-in profiler
go test -cpuprofile=cpu.prof -bench=.
go tool pprof cpu.prof

# In production with net/http/pprof
import _ "net/http/pprof"
# Access http://localhost:6060/debug/pprof/
```

**Rust:**
```bash
# cargo flamegraph
cargo install flamegraph
cargo flamegraph

# perf (Linux)
perf record --call-graph=dwarf ./target/release/app
perf report
```

**Java:**
```bash
# JProfiler, VisualVM, or async-profiler
java -agentpath:/path/to/libasyncProfiler.so=start,file=profile.html -jar app.jar
```

---

#### 2. Memory Profiling

**What it measures:** Memory allocation, usage, and leaks

**When to use:**
- High memory consumption
- Out of memory errors
- Memory leaks (growing memory over time)
- Garbage collection pressure

**Tools by language:**

**Python:**
```bash
# memory_profiler
pip install memory_profiler
python -m memory_profiler script.py

# memray - modern memory profiler
pip install memray
memray run script.py
memray flamegraph output.bin

# objgraph - find memory leaks
import objgraph
objgraph.show_most_common_types()
```

**JavaScript/Node.js:**
```bash
# Chrome DevTools heap snapshot
node --inspect script.js

# clinic.js heapprofiler
clinic heapprofiler -- node script.js

# node-memwatch
npm install @airbnb/node-memwatch
```

**Go:**
```bash
# Memory profiling with pprof
go test -memprofile=mem.prof -bench=.
go tool pprof mem.prof

# Heap dump
import _ "net/http/pprof"
curl http://localhost:6060/debug/pprof/heap > heap.prof
go tool pprof heap.prof
```

**Rust:**
```bash
# Valgrind massif
valgrind --tool=massif ./target/release/app
ms_print massif.out.*

# heaptrack
heaptrack ./target/release/app
```

---

#### 3. I/O Profiling

**What it measures:** Disk and network I/O operations

**When to use:**
- Slow file operations
- Network latency
- Database query performance
- API call delays

**Tools:**

```bash
# strace (Linux) - system call tracing
strace -c python script.py  # Count calls
strace -T python script.py  # Time each call

# iotop (Linux) - disk I/O monitoring
sudo iotop -o  # Only show processes doing I/O

# tcpdump - network traffic analysis
sudo tcpdump -i any -w capture.pcap

# Wireshark - GUI network analysis
wireshark capture.pcap
```

---

#### 4. Database Profiling

**What it measures:** Query performance, connection usage, lock contention

**PostgreSQL:**
```sql
-- Enable query logging
ALTER SYSTEM SET log_min_duration_statement = 100;  -- Log queries > 100ms

-- Analyze query plan
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';

-- Find slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan;
```

**MySQL:**
```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 0.1;  -- 100ms

-- Analyze query
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';

-- Show running queries
SHOW FULL PROCESSLIST;
```

**MongoDB:**
```javascript
// Enable profiling
db.setProfilingLevel(1, { slowms: 100 });

// Analyze query
db.users.find({ email: 'user@example.com' }).explain("executionStats");

// View slow queries
db.system.profile.find().sort({ ts: -1 }).limit(10);
```

---

#### 5. Frontend Profiling

**What it measures:** Rendering, JavaScript execution, bundle size, network requests

**Tools:**

**Chrome DevTools:**
```javascript
// Performance tab - record timeline
// Network tab - analyze requests
// Coverage tab - find unused code
// Lighthouse - comprehensive audit
```

**Web Vitals:**
```javascript
// Core Web Vitals monitoring
import { getCLS, getFID, getLCP } from 'web-vitals';

getCLS(console.log);  // Cumulative Layout Shift
getFID(console.log);  // First Input Delay
getLCP(console.log);  // Largest Contentful Paint
```

**Bundle analysis:**
```bash
# webpack-bundle-analyzer
npm install --save-dev webpack-bundle-analyzer
npx webpack-bundle-analyzer dist/stats.json

# source-map-explorer
npm install -g source-map-explorer
source-map-explorer bundle.js bundle.js.map
```

---

## Optimization Techniques by Layer

### 1. Algorithm and Data Structure Optimization

**Before (O(n²) - inefficient):**
```python
def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates

# O(n²) time complexity
```

**After (O(n) - efficient):**
```python
def find_duplicates(items):
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)

# O(n) time complexity, much faster for large lists
```

**Key principle:** Choose the right data structure for the problem
- Lists for ordered data, O(n) search
- Sets for uniqueness, O(1) search
- Dicts for key-value lookups, O(1) access
- Heaps for priority queues
- Trees for hierarchical data

---

### 2. Database Optimization

#### Add Missing Indexes

**Before (slow full table scan):**
```sql
-- Query without index
SELECT * FROM orders WHERE user_id = 12345 AND status = 'pending';

-- EXPLAIN shows: Seq Scan on orders (cost=0.00..1500.00 rows=100)
```

**After (fast index scan):**
```sql
-- Add composite index
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Now: Index Scan using idx_orders_user_status (cost=0.43..12.50 rows=100)
-- 100x+ faster!
```

#### Fix N+1 Query Problem

**Before (N+1 queries - extremely slow):**
```python
# 1 query to get posts
posts = Post.query.all()

# N queries - one per post to get author
for post in posts:
    print(f"{post.title} by {post.author.name}")  # Separate query each time!

# 1 + N queries (if 100 posts = 101 queries)
```

**After (2 queries with join - fast):**
```python
# Single query with join
posts = Post.query.options(joinedload(Post.author)).all()

for post in posts:
    print(f"{post.title} by {post.author.name}")  # No additional queries

# Only 2 queries (or 1 with proper join)
```

#### Batch Operations

**Before (slow - many round trips):**
```python
for user_id in user_ids:
    db.execute("UPDATE users SET active = true WHERE id = %s", (user_id,))

# 1000 users = 1000 database round trips
```

**After (fast - single batch operation):**
```python
db.execute(
    "UPDATE users SET active = true WHERE id = ANY(%s)",
    (user_ids,)
)

# 1 database round trip
```

#### Connection Pooling

**Before (creating connection each time - slow):**
```python
def get_user(user_id):
    conn = psycopg2.connect(DATABASE_URL)  # New connection every time!
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user
```

**After (connection pool - fast):**
```python
from psycopg2 import pool

# Create connection pool at startup
connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=20,
    dsn=DATABASE_URL
)

def get_user(user_id):
    conn = connection_pool.getconn()  # Reuse existing connection
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cursor.fetchone()
    finally:
        connection_pool.putconn(conn)  # Return to pool
```

---

### 3. Network Optimization

#### Compression

**Before (large uncompressed responses):**
```javascript
// Express without compression
app.get('/api/data', (req, res) => {
    res.json(largeDataObject);  // 500KB uncompressed
});
```

**After (compressed responses - 5x smaller):**
```javascript
const compression = require('compression');
app.use(compression());

app.get('/api/data', (req, res) => {
    res.json(largeDataObject);  // ~100KB compressed with gzip
});
```

#### HTTP/2 Server Push

```javascript
// Push critical resources early
app.get('/', (req, res) => {
    res.push('/styles.css', {
        response: { 'content-type': 'text/css' }
    });
    res.push('/script.js', {
        response: { 'content-type': 'application/javascript' }
    });
    res.sendFile('index.html');
});
```

#### CDN for Static Assets

**Before (serving from origin):**
```html
<!-- Slow - from your server -->
<img src="https://yourserver.com/images/logo.png">
```

**After (CDN - fast, globally distributed):**
```html
<!-- Fast - from nearest CDN edge location -->
<img src="https://cdn.yoursite.com/images/logo.png">
```

---

### 4. Frontend Optimization

#### Code Splitting and Lazy Loading

**Before (single large bundle):**
```javascript
// Everything loaded upfront - 2MB bundle
import Dashboard from './Dashboard';
import Analytics from './Analytics';
import Settings from './Settings';

function App() {
    return (
        <Router>
            <Route path="/dashboard" component={Dashboard} />
            <Route path="/analytics" component={Analytics} />
            <Route path="/settings" component={Settings} />
        </Router>
    );
}
```

**After (lazy loaded routes):**
```javascript
// Each route loads only when needed - initial bundle 200KB
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./Dashboard'));
const Analytics = lazy(() => import('./Analytics'));
const Settings = lazy(() => import('./Settings'));

function App() {
    return (
        <Router>
            <Suspense fallback={<Loading />}>
                <Route path="/dashboard" component={Dashboard} />
                <Route path="/analytics" component={Analytics} />
                <Route path="/settings" component={Settings} />
            </Suspense>
        </Router>
    );
}
```

#### Memoization

**Before (re-rendering unnecessarily):**
```javascript
function ProductList({ products, filters }) {
    // Expensive calculation runs on every render
    const filteredProducts = products.filter(p =>
        p.category === filters.category && p.price <= filters.maxPrice
    );

    return <div>{filteredProducts.map(renderProduct)}</div>;
}
```

**After (memoized calculation):**
```javascript
import { useMemo } from 'react';

function ProductList({ products, filters }) {
    // Only recalculates when products or filters change
    const filteredProducts = useMemo(
        () => products.filter(p =>
            p.category === filters.category && p.price <= filters.maxPrice
        ),
        [products, filters]
    );

    return <div>{filteredProducts.map(renderProduct)}</div>;
}
```

#### Image Optimization

**Before (large unoptimized images):**
```html
<!-- 5MB JPEG loaded for all devices -->
<img src="photo.jpg" alt="Photo">
```

**After (responsive, optimized images):**
```html
<!-- Modern formats, responsive sizes -->
<picture>
    <source srcset="photo-400.webp 400w, photo-800.webp 800w" type="image/webp">
    <source srcset="photo-400.jpg 400w, photo-800.jpg 800w" type="image/jpeg">
    <img src="photo-400.jpg" alt="Photo" loading="lazy">
</picture>
<!-- 100-300KB depending on device, lazy loaded -->
```

---

### 5. Caching Strategies

#### Application-Level Caching

**Before (expensive computation every time):**
```python
def get_trending_products():
    # Complex aggregation query taking 5 seconds
    return db.query("""
        SELECT product_id, COUNT(*) as views
        FROM product_views
        WHERE timestamp > NOW() - INTERVAL '24 hours'
        GROUP BY product_id
        ORDER BY views DESC
        LIMIT 10
    """).all()
```

**After (cached results):**
```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=1)
def get_trending_products_cached(cache_key):
    # Same query, but results cached for 5 minutes
    return db.query("""
        SELECT product_id, COUNT(*) as views
        FROM product_views
        WHERE timestamp > NOW() - INTERVAL '24 hours'
        GROUP BY product_id
        ORDER BY views DESC
        LIMIT 10
    """).all()

def get_trending_products():
    # Cache key changes every 5 minutes
    cache_key = datetime.now().replace(second=0, microsecond=0) // timedelta(minutes=5)
    return get_trending_products_cached(cache_key)

# 5 seconds -> ~1ms (cached)
```

#### Redis Caching

```python
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379)

def get_user_profile(user_id):
    # Try cache first
    cache_key = f"user:{user_id}:profile"
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)  # Cache hit - instant

    # Cache miss - query database
    profile = db.query("SELECT * FROM users WHERE id = %s", user_id)

    # Store in cache for 1 hour
    redis_client.setex(cache_key, 3600, json.dumps(profile))

    return profile
```

#### HTTP Caching Headers

```javascript
app.get('/api/products/:id', (req, res) => {
    const product = getProduct(req.params.id);

    // Cache for 5 minutes in browser and CDN
    res.set('Cache-Control', 'public, max-age=300');

    // Use ETag for conditional requests
    res.set('ETag', product.updated_at);

    // If client has current version, return 304 Not Modified
    if (req.headers['if-none-match'] === product.updated_at) {
        return res.status(304).end();
    }

    res.json(product);
});
```

---

### 6. Asynchronous Processing

**Before (synchronous - blocks request):**
```python
@app.route('/send-report', methods=['POST'])
def send_report():
    report_data = generate_report()  # Takes 30 seconds
    send_email(report_data)          # Takes 5 seconds

    return jsonify({"status": "sent"})  # User waits 35 seconds!
```

**After (async with background tasks):**
```python
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379')

@celery.task
def generate_and_send_report_async(user_id):
    report_data = generate_report()  # Runs in background
    send_email(report_data)

@app.route('/send-report', methods=['POST'])
def send_report():
    generate_and_send_report_async.delay(current_user.id)

    return jsonify({"status": "processing"})  # Returns immediately!
```

---

## Performance Optimization Workflow

### Step 1: Establish Baseline

Before any optimization, measure current performance:

```bash
# Load testing with k6
k6 run --vus 10 --duration 30s load-test.js

# Results:
#   http_req_duration..............: avg=250ms min=100ms max=1.2s
#   http_reqs......................: 1200 (40/s)
#   http_req_failed................: 5% (60 failures)
```

Document baseline metrics:
- Response times (p50, p95, p99)
- Throughput (requests/second)
- Error rates
- Resource usage (CPU, memory)

---

### Step 2: Profile to Find Bottlenecks

Use profiling tools to identify where time is spent:

```bash
# Python example
py-spy record -o profile.svg -- python app.py
```

Analyze the profile:
- What function takes the most time?
- Are there unexpected bottlenecks?
- Is it CPU, memory, I/O, or network bound?

---

### Step 3: Prioritize Optimizations

Create optimization candidates based on:

1. **Impact** — Will this significantly improve performance?
2. **Effort** — How difficult is this to implement?
3. **Risk** — Could this break existing functionality?

**Optimization priority matrix:**
```
High Impact + Low Effort = DO FIRST
High Impact + High Effort = Do after quick wins
Low Impact + Low Effort = Do if time permits
Low Impact + High Effort = Don't do
```

---

### Step 4: Implement One Optimization

Make ONE change at a time:

✅ Good: Add database index for slow query
✅ Good: Implement caching for expensive API call
❌ Bad: Add index + caching + connection pooling + compression

---

### Step 5: Measure Impact

After implementing optimization, measure again:

```bash
# Run the same load test
k6 run --vus 10 --duration 30s load-test.js

# Results:
#   http_req_duration..............: avg=100ms min=50ms max=400ms
#   http_reqs......................: 3000 (100/s)
#   http_req_failed................: 0.5% (15 failures)
```

Compare to baseline:
- Response time: 250ms → 100ms (60% improvement)
- Throughput: 40/s → 100/s (2.5x improvement)
- Error rate: 5% → 0.5% (10x improvement)

---

### Step 6: Document and Monitor

Document the optimization:

```markdown
## Performance Optimization: Added Database Index

**Date:** 2026-01-10
**Problem:** User search queries taking 2-5 seconds
**Root Cause:** Full table scan on users table (10M rows)
**Solution:** Added index on email column
**Impact:**
- Response time: 2500ms → 50ms (50x improvement)
- Database CPU: 80% → 20%

**Command:**
CREATE INDEX idx_users_email ON users(email);

**Monitoring:** Set alert if p95 response time > 200ms
```

Set up monitoring to catch regressions:
```python
# Alert if response time exceeds threshold
if p95_response_time > 200:
    send_alert("User search performance degraded")
```

---

## Common Performance Patterns

### 1. Caching

**When to use:** Expensive operations called frequently with same inputs

**Strategies:**
- **In-memory cache:** Fast, limited by memory (Redis, Memcached)
- **Database query cache:** Reduce database load
- **CDN cache:** Serve static assets from edge locations
- **Browser cache:** Reduce network requests

**Cache invalidation:**
```python
# Time-based expiration
cache.set('key', value, expire=3600)  # 1 hour

# Event-based invalidation
def update_user(user_id, data):
    db.update(user_id, data)
    cache.delete(f'user:{user_id}')  # Invalidate cache
```

---

### 2. Connection Pooling

**When to use:** Applications making many database/API connections

**Benefits:**
- Reuse existing connections
- Avoid connection overhead
- Limit concurrent connections

**Implementation:**
```python
# Database connection pool
from sqlalchemy import create_engine, pool

engine = create_engine(
    DATABASE_URL,
    poolclass=pool.QueuePool,
    pool_size=20,          # Keep 20 connections open
    max_overflow=10,       # Allow 10 more if needed
    pool_pre_ping=True     # Check connection before use
)
```

---

### 3. Batch Processing

**When to use:** Many small operations that can be grouped

**Example:**
```python
# Bad: Insert one at a time
for user in users:
    db.execute("INSERT INTO users VALUES (%s, %s)", (user.id, user.name))
# 1000 users = 1000 round trips

# Good: Batch insert
db.executemany(
    "INSERT INTO users VALUES (%s, %s)",
    [(user.id, user.name) for user in users]
)
# 1000 users = 1 round trip
```

---

### 4. Asynchronous Processing

**When to use:** Long-running tasks that don't need immediate response

**Use cases:**
- Email sending
- Report generation
- Image processing
- Data exports

**Pattern:**
```python
# Synchronous - user waits
def process_order(order_id):
    order = get_order(order_id)
    send_confirmation_email(order)  # 2 seconds
    update_inventory(order)          # 5 seconds
    generate_invoice(order)          # 3 seconds
    return {"status": "complete"}    # User waits 10 seconds

# Asynchronous - immediate response
def process_order(order_id):
    background_task.delay(order_id)
    return {"status": "processing"}  # Returns immediately
```

---

## Performance Testing

### Load Testing with k6

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    stages: [
        { duration: '1m', target: 10 },   // Ramp up to 10 users
        { duration: '3m', target: 10 },   // Stay at 10 users
        { duration: '1m', target: 50 },   // Ramp up to 50 users
        { duration: '3m', target: 50 },   // Stay at 50 users
        { duration: '1m', target: 0 },    // Ramp down
    ],
    thresholds: {
        http_req_duration: ['p(95)<500'],  // 95% of requests under 500ms
        http_req_failed: ['rate<0.01'],    // Less than 1% errors
    },
};

export default function() {
    let response = http.get('https://api.example.com/products');

    check(response, {
        'status is 200': (r) => r.status === 200,
        'response time < 500ms': (r) => r.timings.duration < 500,
    });

    sleep(1);
}
```

Run test:
```bash
k6 run load-test.js
```

---

## Safety Checklist

Before optimizing:

- [ ] Baseline metrics established
- [ ] Profiling completed to identify bottleneck
- [ ] Tests exist and pass (verify correctness)
- [ ] Optimization is prioritized (high impact, reasonable effort)
- [ ] You understand the root cause

During optimization:

- [ ] Making one change at a time
- [ ] Tests still pass after each change
- [ ] Code remains readable and maintainable
- [ ] No premature optimization

After optimization:

- [ ] Performance improvement measured and documented
- [ ] Tests still pass
- [ ] Monitoring/alerts configured
- [ ] Team informed of changes
- [ ] Ready for code review

---

## Integration with Other Skills

### With Refactoring

- Refactor before optimizing to improve code structure
- Optimization often reveals opportunities for refactoring
- Keep optimizations separate from refactorings in commits

### With Testing Strategy

- Write performance tests before optimizing
- Use tests to verify correctness after optimization
- Add regression tests for performance-critical paths

### With Monitoring

- Set up monitoring before optimization
- Use metrics to identify optimization targets
- Monitor for performance regressions after deployment

### With CI/CD

- Run performance tests in CI pipeline
- Fail builds if performance regresses
- Automate load testing before production deployment

---

## Common Pitfalls

❌ **Optimizing without profiling** — You'll optimize the wrong thing
❌ **Premature optimization** — "Premature optimization is the root of all evil" - Donald Knuth
❌ **Over-optimization** — Sacrificing readability for minimal gains
❌ **Ignoring the 80/20 rule** — 80% of performance issues come from 20% of code
❌ **Not measuring impact** — Can't prove optimization worked
❌ **Breaking functionality** — Tests must pass after optimization
❌ **Optimizing the wrong layer** — Fix slow algorithm before throwing hardware at it

✅ **Profile first, optimize second**
✅ **Measure baseline and impact**
✅ **Optimize high-impact bottlenecks**
✅ **Keep tests passing**
✅ **Document optimizations**
✅ **Monitor for regressions**

---

**Remember:** Performance optimization is a cycle: measure, identify, optimize, measure. Always start with profiling to find actual bottlenecks, and always measure to verify your optimizations work. Fast code that's wrong is useless—keep your tests passing!
