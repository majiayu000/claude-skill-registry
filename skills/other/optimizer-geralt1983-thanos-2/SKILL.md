---
name: Performance Optimizer
description: Performance tuning, profiling, and optimization. USE WHEN user mentions slow, performance, optimize, speed, latency, throughput, memory, CPU, bottleneck, profiling, caching, or asks why something is slow or how to make it faster.
---

# Performance Optimizer Skill

AI-powered performance guidance for identifying bottlenecks, optimizing code, and improving system throughput with focus on measurable improvements, systematic profiling, and efficient resource usage.

## What This Skill Does

This skill provides expert-level performance optimization guidance including profiling, bottleneck identification, algorithmic improvements, caching strategies, and resource management. It combines performance engineering best practices with practical, measurable improvements.

**Key Capabilities:**
- **Profiling**: CPU, memory, I/O profiling and analysis
- **Bottleneck Detection**: Identifying performance hotspots
- **Algorithm Optimization**: Time/space complexity improvements
- **Caching Strategies**: In-memory, distributed, HTTP caching
- **Database Optimization**: Query tuning, indexing, connection pooling
- **Concurrency**: Async patterns, parallelization, thread management

## Core Principles

### The Performance Mindset
- **Measure First**: Never optimize without data
- **Focus on Hotspots**: 80% of time spent in 20% of code
- **Know Your Limits**: CPU? Memory? I/O? Network?
- **Test Under Load**: Real performance requires real load
- **Avoid Premature Optimization**: Correctness before speed

### Performance Priority Hierarchy
1. **Architecture** - Is the design fundamentally sound?
2. **Algorithms** - Right data structures and algorithms?
3. **I/O** - Database, network, file system optimized?
4. **Memory** - Efficient memory usage?
5. **CPU** - Micro-optimizations (last resort)

## Performance Analysis Workflow

### 1. Establish Baseline
```
Before optimizing:
├── Define Metrics (latency, throughput, memory)
├── Set Targets (what's "fast enough"?)
├── Measure Current (where are we now?)
├── Create Benchmarks (repeatable tests)
└── Document Environment (hardware, load, data)
```

### 2. Profile and Identify
```
Find the bottlenecks:
├── CPU Profiling (where is time spent?)
├── Memory Profiling (allocations, leaks)
├── I/O Profiling (disk, network waits)
├── Database Analysis (slow queries, locks)
└── Flame Graphs (visualize call stacks)
```

### 3. Optimize
```
For each bottleneck:
├── Understand Root Cause
├── Propose Solution
├── Implement Change
├── Measure Impact
└── Verify No Regression
```

### 4. Validate
```
Confirm improvements:
├── Compare to Baseline
├── Test Under Load
├── Check for Regressions
├── Monitor in Production
└── Document Changes
```

## Profiling Tools by Language

### Python
```bash
# CPU Profiling
python -m cProfile -s cumtime script.py
python -m cProfile -o profile.pstats script.py
# Visualize with snakeviz
pip install snakeviz && snakeviz profile.pstats

# Line-by-line profiling
pip install line_profiler
kernprof -l -v script.py

# Memory profiling
pip install memory_profiler
python -m memory_profiler script.py

# Async profiling
pip install py-spy
py-spy record -o profile.svg -- python script.py
```

### JavaScript/Node.js
```bash
# Built-in profiler
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Clinic.js suite
npm install -g clinic
clinic doctor -- node app.js
clinic flame -- node app.js
clinic bubbleprof -- node app.js

# Chrome DevTools
node --inspect app.js
# Open chrome://inspect
```

### Java
```bash
# JVM flags for profiling
java -XX:+PrintGCDetails -XX:+PrintGCTimeStamps App

# Async Profiler
./profiler.sh -d 30 -f flamegraph.html <pid>

# JFR (Java Flight Recorder)
java -XX:+FlightRecorder -XX:StartFlightRecording=duration=60s,filename=rec.jfr App

# VisualVM
jvisualvm  # GUI profiler
```

### Go
```go
// Built-in profiling
import _ "net/http/pprof"

// Access at http://localhost:6060/debug/pprof/
```
```bash
# CPU profile
go test -cpuprofile=cpu.prof -bench=.
go tool pprof cpu.prof

# Memory profile
go test -memprofile=mem.prof -bench=.
go tool pprof mem.prof

# Trace
go test -trace=trace.out
go tool trace trace.out
```

## Common Performance Issues

### CPU Bottlenecks
| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Inefficient Algorithm** | O(n²) when O(n) exists | Use better algorithm/data structure |
| **Redundant Computation** | Same calculation repeated | Memoization, caching |
| **String Concatenation** | Building strings in loops | Use StringBuilder/join |
| **Regex Compilation** | Compiling regex in loops | Compile once, reuse |
| **Excessive Logging** | Log in hot paths | Reduce log level, sample |

### Memory Bottlenecks
| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Memory Leak** | Growing memory over time | Track allocations, close resources |
| **Large Object Graphs** | High GC pressure | Reduce object creation |
| **Unbounded Caches** | Memory exhaustion | Add size limits, TTL |
| **Holding References** | Objects not collected | Clear references when done |
| **Large Strings/Arrays** | Memory spikes | Stream, pagination |

### I/O Bottlenecks
| Issue | Symptoms | Solution |
|-------|----------|----------|
| **N+1 Queries** | Many small DB queries | Batch/JOIN queries |
| **Missing Indexes** | Slow queries | Add appropriate indexes |
| **Sync I/O in Async** | Blocked event loop | Use async I/O |
| **No Connection Pool** | Connection overhead | Pool connections |
| **Large Payloads** | Slow transfers | Compress, paginate |

## Caching Strategies

### Cache Layers
```
┌─────────────────────────────────────────────────────────┐
│                    Request Flow                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   Browser    →    CDN    →    App Cache    →    DB      │
│   Cache           Cache       (Redis)          Query    │
│   (Client)       (Edge)      (Server)         Cache     │
│                                                          │
│   Fastest ◄─────────────────────────────────► Slowest   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Cache Patterns
```python
# Cache-Aside (Lazy Loading)
def get_user(user_id):
    # Check cache first
    cached = cache.get(f"user:{user_id}")
    if cached:
        return cached
    
    # Miss: load from DB
    user = db.get_user(user_id)
    
    # Store in cache for next time
    cache.set(f"user:{user_id}", user, ttl=3600)
    return user

# Write-Through
def update_user(user_id, data):
    # Update DB
    user = db.update_user(user_id, data)
    
    # Update cache immediately
    cache.set(f"user:{user_id}", user, ttl=3600)
    return user

# Write-Behind (Async)
def update_user(user_id, data):
    # Update cache immediately
    cache.set(f"user:{user_id}", data, ttl=3600)
    
    # Queue DB write for later
    queue.enqueue("update_user", user_id, data)
    
    return data
```

### Cache Invalidation
```python
# Time-based (TTL)
cache.set("key", value, ttl=3600)  # Expires in 1 hour

# Event-based
def update_product(product_id, data):
    db.update_product(product_id, data)
    cache.delete(f"product:{product_id}")
    cache.delete("product_list")  # Invalidate related caches

# Version-based
def get_config():
    version = db.get_config_version()
    cached = cache.get(f"config:v{version}")
    if cached:
        return cached
    config = db.get_config()
    cache.set(f"config:v{version}", config)
    return config
```

## Database Performance

### Query Optimization
```sql
-- Use EXPLAIN to analyze queries
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Before: Full table scan
SELECT * FROM orders WHERE YEAR(created_at) = 2024;

-- After: Index-friendly
SELECT * FROM orders 
WHERE created_at >= '2024-01-01' 
  AND created_at < '2025-01-01';

-- Before: SELECT *
SELECT * FROM users WHERE id = 123;

-- After: Select only needed columns
SELECT id, name, email FROM users WHERE id = 123;

-- Before: N+1 queries
for user in users:
    orders = db.query("SELECT * FROM orders WHERE user_id = ?", user.id)

-- After: Single JOIN
SELECT u.*, o.* 
FROM users u 
LEFT JOIN orders o ON u.id = o.user_id 
WHERE u.id IN (1, 2, 3, ...);
```

### Index Strategy
```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- Covering index (includes all needed columns)
CREATE INDEX idx_orders_covering ON orders(user_id, created_at) 
INCLUDE (total, status);

-- Partial index (for filtered queries)
CREATE INDEX idx_active_users ON users(email) 
WHERE active = true;
```

### Connection Pooling
```python
# Python with SQLAlchemy
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://user:pass@localhost/db",
    pool_size=20,           # Maintained connections
    max_overflow=10,        # Extra connections when needed
    pool_timeout=30,        # Wait time for connection
    pool_recycle=1800,      # Recycle connections after 30 min
)

# Node.js with pg
const { Pool } = require('pg');
const pool = new Pool({
    max: 20,                // Max connections
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
});
```

## Async and Concurrency

### Async I/O Patterns
```python
# Python asyncio
import asyncio
import aiohttp

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def fetch_one(session, url):
    async with session.get(url) as response:
        return await response.json()

# Run concurrently instead of sequentially
results = asyncio.run(fetch_all(urls))
```

```javascript
// JavaScript Promise.all
async function fetchAll(urls) {
    const promises = urls.map(url => fetch(url).then(r => r.json()));
    return Promise.all(promises);
}

// With concurrency limit
async function fetchWithLimit(urls, limit = 5) {
    const results = [];
    for (let i = 0; i < urls.length; i += limit) {
        const batch = urls.slice(i, i + limit);
        const batchResults = await Promise.all(
            batch.map(url => fetch(url).then(r => r.json()))
        );
        results.push(...batchResults);
    }
    return results;
}
```

### Parallelization
```python
# Python multiprocessing for CPU-bound work
from concurrent.futures import ProcessPoolExecutor

def cpu_intensive_task(data):
    # Heavy computation
    return result

with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(cpu_intensive_task, data_chunks))

# ThreadPoolExecutor for I/O-bound work
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_url, urls))
```

## When to Use This Skill

**Trigger Phrases:**
- "This is too slow..."
- "How can I make this faster?"
- "Why is this taking so long?"
- "Help me optimize..."
- "The page load time is..."
- "We're hitting memory limits..."
- "How do I profile..."
- "What should I cache?"

**Example Requests:**
1. "This API endpoint takes 5 seconds, help me speed it up"
2. "How do I profile this Python function?"
3. "My memory usage keeps growing"
4. "What should I index in this database?"
5. "Help me implement caching for this data"
6. "This loop is too slow with large datasets"

## Performance Checklist

Before deploying performance-critical code:

- [ ] **Measured baseline?** Know current performance
- [ ] **Profiled?** Identified actual bottlenecks
- [ ] **Optimized hot paths?** Focus on high-impact areas
- [ ] **Tested under load?** Realistic traffic patterns
- [ ] **Checked memory?** No leaks or excessive usage
- [ ] **Reviewed queries?** Indexes, N+1, unnecessary data
- [ ] **Added caching?** Where appropriate
- [ ] **Set up monitoring?** Track performance over time

## Integration with Other Skills

- **Architect**: Architecture decisions impact performance
- **Troubleshooter**: Many bugs manifest as performance issues
- **Database Designer**: Schema and index design for performance
- **Reviewer**: Performance review in code review

---

*Skill designed for Thanos + Antigravity integration*
