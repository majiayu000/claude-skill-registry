---
name: Profiling (Node.js & Python)
description: Comprehensive guide to CPU and memory profiling in Node.js and Python for identifying bottlenecks and optimizing performance
---

# Profiling (Node.js & Python)

## Why Profiling Matters

Profiling is the foundation of performance optimization. Without profiling, you're guessing.

### Key Benefits
- **Identify Bottlenecks**: Find the actual slow parts (not where you think they are)
- **Optimize Hot Paths**: Focus on code that runs frequently or takes the most time
- **Reduce Resource Usage**: Lower CPU, memory, and I/O consumption
- **Improve User Experience**: Faster response times, better scalability
- **Data-Driven Decisions**: Measure before and after optimizations

### The Golden Rule
> "Premature optimization is the root of all evil" - Donald Knuth

Always profile first, optimize second. Developers are notoriously bad at guessing where performance issues lie.

---

## Types of Profiling

### 1. CPU Profiling (Where Time is Spent)
- **Purpose**: Identify functions consuming the most CPU time
- **Use Cases**: Slow endpoints, high CPU usage, algorithm optimization
- **Output**: Call trees, flamegraphs, function timing

### 2. Memory Profiling (Allocation and Leaks)
- **Purpose**: Track memory allocation, identify leaks, analyze heap usage
- **Use Cases**: Memory leaks, high memory consumption, OOM crashes
- **Output**: Heap snapshots, allocation timelines, retainer graphs

### 3. I/O Profiling (Network, Disk)
- **Purpose**: Measure time spent on I/O operations
- **Use Cases**: Slow database queries, network latency, file operations
- **Output**: I/O wait times, throughput metrics

### 4. Lock Profiling (Concurrency Issues)
- **Purpose**: Detect contention, deadlocks, and blocking
- **Use Cases**: Multi-threaded applications, race conditions
- **Output**: Lock wait times, contention graphs

---

## Node.js CPU Profiling

### 1. Built-in Profiler: `node --prof`

**Basic Usage:**
```bash
# Generate profiling data
node --prof app.js

# Process the output
node --prof-process isolate-0xnnnnnnnnnnnn-v8.log > processed.txt
```

**Pros:**
- Built-in, no dependencies
- Low overhead

**Cons:**
- Output is hard to read
- Requires post-processing

### 2. Chrome DevTools

**Usage:**
```bash
# Start Node.js with inspector
node --inspect app.js

# Or for immediate break
node --inspect-brk app.js
```

**Steps:**
1. Open `chrome://inspect` in Chrome
2. Click "inspect" on your Node.js process
3. Go to "Profiler" tab
4. Start recording, run your code, stop recording

**Pros:**
- Visual interface
- Flamegraphs built-in
- Heap snapshots available

**Cons:**
- Requires Chrome
- Not suitable for production

### 3. Clinic.js Doctor

**Installation:**
```bash
npm install -g clinic
```

**Usage:**
```bash
# Profile your application
clinic doctor -- node app.js

# Load test while profiling
clinic doctor -- node app.js &
autocannon http://localhost:3000
```

**Output:**
- HTML report with recommendations
- Detects event loop delays, I/O issues, CPU bottlenecks

**Pros:**
- Automatic diagnosis
- Beautiful visualizations
- Beginner-friendly

### 4. 0x (Flamegraph Generator)

**Installation:**
```bash
npm install -g 0x
```

**Usage:**
```bash
# Profile and generate flamegraph
0x app.js

# With load testing
0x -o app.js &
autocannon http://localhost:3000
```

**Output:**
- Interactive HTML flamegraph
- Optimized and unoptimized code views

**Pros:**
- Production-ready (low overhead)
- Beautiful flamegraphs
- Easy to identify hot paths

### 5. v8-profiler

**Installation:**
```bash
npm install v8-profiler-next
```

**Usage:**
```javascript
const profiler = require('v8-profiler-next');
const fs = require('fs');

// Start profiling
profiler.startProfiling('CPU profile');

// Your code here
doExpensiveOperation();

// Stop profiling
const profile = profiler.stopProfiling();
profile.export((error, result) => {
  fs.writeFileSync('profile.cpuprofile', result);
  profile.delete();
});
```

**Load in Chrome DevTools:**
1. Open DevTools → Profiler
2. Load `profile.cpuprofile`

---

## Node.js Memory Profiling

### 1. Chrome DevTools Heap Snapshot

**Usage:**
```bash
node --inspect app.js
```

**Steps:**
1. Open `chrome://inspect`
2. Go to "Memory" tab
3. Take heap snapshot
4. Analyze objects, retainers, and memory usage

**What to Look For:**
- Large objects
- Unexpected object counts
- Retainer paths (what's keeping objects alive)

### 2. clinic-heapprofiler

**Usage:**
```bash
clinic heapprofiler -- node app.js
```

**Output:**
- Memory allocation timeline
- Leak detection

### 3. memwatch-next

**Installation:**
```bash
npm install @airbnb/node-memwatch
```

**Usage:**
```javascript
const memwatch = require('@airbnb/node-memwatch');

// Detect leaks
memwatch.on('leak', (info) => {
  console.error('Memory leak detected:', info);
});

// Track heap diff
const hd = new memwatch.HeapDiff();
// ... run code ...
const diff = hd.end();
console.log(diff);
```

### 4. node --inspect (Manual Snapshots)

**Usage:**
```javascript
const v8 = require('v8');
const fs = require('fs');

// Take heap snapshot
const snapshot = v8.writeHeapSnapshot();
console.log('Heap snapshot written to', snapshot);
```

---

## Python CPU Profiling

### 1. cProfile (Built-in)

**Usage:**
```bash
# Profile a script
python -m cProfile -o output.prof script.py

# Profile with stats
python -m cProfile -s cumulative script.py
```

**Analyze Results:**
```python
import pstats

stats = pstats.Stats('output.prof')
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions
```

**Pros:**
- Built-in, no installation
- Comprehensive data

**Cons:**
- High overhead (not for production)
- Output is text-based

### 2. py-spy (Sampling Profiler)

**Installation:**
```bash
pip install py-spy
```

**Usage:**
```bash
# Profile a running process
py-spy top --pid 12345

# Generate flamegraph
py-spy record -o profile.svg -- python script.py

# Profile running process
py-spy record -o profile.svg --pid 12345
```

**Pros:**
- **Production-safe** (low overhead)
- No code changes required
- Beautiful flamegraphs

**Cons:**
- Sampling (not deterministic)

### 3. line_profiler (Line-by-Line)

**Installation:**
```bash
pip install line_profiler
```

**Usage:**
```python
# Add @profile decorator
@profile
def slow_function():
    # Your code
    pass
```

**Run:**
```bash
kernprof -l -v script.py
```

**Output:**
```
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     8                                           @profile
     9                                           def slow_function():
    10         1       1000.0   1000.0     50.0      time.sleep(0.001)
    11         1       1000.0   1000.0     50.0      time.sleep(0.001)
```

**Pros:**
- Line-level granularity
- Easy to pinpoint exact slow lines

**Cons:**
- Requires code modification
- High overhead

### 4. pyinstrument (Flamegraphs)

**Installation:**
```bash
pip install pyinstrument
```

**Usage:**
```python
from pyinstrument import Profiler

profiler = Profiler()
profiler.start()

# Your code here
slow_function()

profiler.stop()
profiler.print()

# Or save as HTML
profiler.open_in_browser()
```

**Pros:**
- Low overhead
- Beautiful HTML output
- Call tree and flamegraph views

---

## Python Memory Profiling

### 1. memory_profiler

**Installation:**
```bash
pip install memory_profiler
```

**Usage:**
```python
from memory_profiler import profile

@profile
def my_func():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a
```

**Run:**
```bash
python -m memory_profiler script.py
```

**Output:**
```
Line #    Mem usage    Increment   Line Contents
================================================
     3   38.816 MiB   38.816 MiB   @profile
     4                             def my_func():
     5   46.492 MiB    7.676 MiB       a = [1] * (10 ** 6)
     6  198.867 MiB  152.375 MiB       b = [2] * (2 * 10 ** 7)
     7   46.492 MiB -152.375 MiB       del b
     8   46.492 MiB    0.000 MiB       return a
```

### 2. tracemalloc (Built-in)

**Usage:**
```python
import tracemalloc

tracemalloc.start()

# Your code
data = [i for i in range(1000000)]

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

for stat in top_stats[:10]:
    print(stat)
```

**Pros:**
- Built-in (Python 3.4+)
- Low overhead

### 3. pympler

**Installation:**
```bash
pip install pympler
```

**Usage:**
```python
from pympler import asizeof, muppy, summary

# Size of object
size = asizeof.asizeof(my_object)

# All objects
all_objects = muppy.get_objects()
sum1 = summary.summarize(all_objects)
summary.print_(sum1)
```

### 4. guppy3

**Installation:**
```bash
pip install guppy3
```

**Usage:**
```python
from guppy import hpy

h = hpy()
print(h.heap())
```

---

## Profiling in Development

### Best Practices

1. **Use Representative Workload**
   - Don't profile "hello world"
   - Use realistic data volumes
   - Simulate production traffic patterns

2. **Profile Specific Endpoints**
   ```javascript
   // Node.js: Profile specific route
   app.get('/slow-endpoint', (req, res) => {
     const profiler = require('v8-profiler-next');
     profiler.startProfiling('slow-endpoint');
     
     // Your code
     const result = expensiveOperation();
     
     const profile = profiler.stopProfiling();
     profile.export((error, result) => {
       fs.writeFileSync('slow-endpoint.cpuprofile', result);
       profile.delete();
     });
     
     res.json(result);
   });
   ```

3. **Isolate the Problem**
   - Profile incrementally
   - Test one change at a time
   - Use microbenchmarks for specific functions

4. **Warm Up First**
   - JIT compilers need warm-up
   - Run code multiple times before profiling
   - Discard first few runs

---

## Profiling in Production

### Continuous Profiling

**Tools:**
- **Datadog Continuous Profiler**: Always-on profiling with <1% overhead
- **Pyroscope**: Open-source continuous profiling
- **Google Cloud Profiler**: For GCP applications
- **AWS CodeGuru Profiler**: For AWS applications

**Benefits:**
- Catch issues in production (not just dev)
- Historical data for trend analysis
- Low overhead (always on)

**Example (Datadog):**
```javascript
// Node.js
const tracer = require('dd-trace').init({
  profiling: true,
  env: 'production'
});
```

```python
# Python
import ddtrace
ddtrace.profiling.auto.start()
```

### Sampling Profiling (Low Overhead)

**Node.js:**
- Use `0x` with sampling mode
- Use `clinic` in production mode

**Python:**
- Use `py-spy` (attach to running process)

**Example:**
```bash
# Profile production process without restart
py-spy record -o profile.svg --pid $(pgrep -f "python app.py")
```

### On-Demand Profiling

**Trigger Manually:**
```javascript
// Node.js: Expose profiling endpoint (secure it!)
app.post('/admin/profile', async (req, res) => {
  const profiler = require('v8-profiler-next');
  profiler.startProfiling('on-demand');
  
  setTimeout(() => {
    const profile = profiler.stopProfiling();
    profile.export((error, result) => {
      fs.writeFileSync(`profile-${Date.now()}.cpuprofile`, result);
      profile.delete();
    });
  }, 30000); // Profile for 30 seconds
  
  res.json({ status: 'profiling started' });
});
```

---

## Reading Flamegraphs

### Anatomy of a Flamegraph

```
┌─────────────────────────────────────────────────────────┐
│                      main()                             │ ← Bottom: Entry point
├──────────────────┬──────────────────────────────────────┤
│   processRequest │         handleQuery                  │
├─────┬────────────┼──────────┬───────────────────────────┤
│ log │ parseJSON  │ dbQuery  │      formatResponse       │
└─────┴────────────┴──────────┴───────────────────────────┘
                                      ↑ Top: Leaf functions
```

### Key Principles

1. **X-Axis**: Alphabetical order (NOT time!)
   - Width = time spent
   - Position = alphabetical

2. **Y-Axis**: Stack depth
   - Bottom = entry point
   - Top = leaf functions (where time is actually spent)

3. **Width**: Time spent in that function
   - Wide = hot path (optimize this!)
   - Narrow = not a bottleneck

4. **Colors**: Usually random or by library
   - Some tools use colors for language/library

### How to Read

1. **Find Wide Boxes at the Top**: These are your bottlenecks
2. **Follow the Stack Down**: Understand the call path
3. **Look for Plateaus**: Wide, flat areas = single function taking lots of time
4. **Look for Towers**: Tall, narrow stacks = deep call chains (may indicate recursion issues)

### Example Analysis

```
If you see:
┌─────────────────────────────────────┐
│         JSON.parse()                │ ← 40% of time!
└─────────────────────────────────────┘

Action: Optimize JSON parsing (use streaming parser, reduce payload size)
```

---

## Common Bottlenecks

### 1. Synchronous I/O (Blocking Event Loop)

**Problem:**
```javascript
// BAD: Blocks event loop
const data = fs.readFileSync('large-file.txt');
```

**Solution:**
```javascript
// GOOD: Non-blocking
const data = await fs.promises.readFile('large-file.txt');
```

### 2. N+1 Queries

**Problem:**
```javascript
// BAD: N+1 queries
const users = await db.users.findMany();
for (const user of users) {
  user.posts = await db.posts.findMany({ where: { userId: user.id } });
}
```

**Solution:**
```javascript
// GOOD: Single query with join
const users = await db.users.findMany({
  include: { posts: true }
});
```

### 3. Inefficient Algorithms (O(n²))

**Problem:**
```python
# BAD: O(n²)
def find_duplicates(arr):
    duplicates = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                duplicates.append(arr[i])
    return duplicates
```

**Solution:**
```python
# GOOD: O(n)
def find_duplicates(arr):
    seen = set()
    duplicates = set()
    for item in arr:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)
```

### 4. JSON Parsing Large Objects

**Problem:**
```javascript
// BAD: Parse entire 100MB JSON
const data = JSON.parse(hugeJsonString);
```

**Solution:**
```javascript
// GOOD: Stream parsing
const JSONStream = require('JSONStream');
fs.createReadStream('huge.json')
  .pipe(JSONStream.parse('*'))
  .on('data', (item) => processItem(item));
```

### 5. Regular Expressions (Catastrophic Backtracking)

**Problem:**
```javascript
// BAD: Catastrophic backtracking
const regex = /(a+)+b/;
regex.test('aaaaaaaaaaaaaaaaaaaaaaaac'); // Hangs!
```

**Solution:**
```javascript
// GOOD: Atomic grouping or simpler regex
const regex = /a+b/;
```

### 6. Memory Leaks (Unreleased References)

**Problem:**
```javascript
// BAD: Event listener leak
function setupListener() {
  const data = new Array(1000000);
  element.addEventListener('click', () => {
    console.log(data.length); // Holds reference to data!
  });
}
```

**Solution:**
```javascript
// GOOD: Remove listener or avoid closure
function setupListener() {
  const length = data.length;
  const handler = () => console.log(length);
  element.addEventListener('click', handler);
  
  // Cleanup
  return () => element.removeEventListener('click', handler);
}
```

---

## Memory Leak Detection

### Signs of Memory Leaks

1. **Heap Growth Over Time**
   - Memory usage increases continuously
   - Never stabilizes

2. **High Retained Size**
   - Objects that should be garbage collected aren't

3. **Unexpected Object Counts**
   - Thousands of objects that should be few

### Detection Workflow

1. **Take Baseline Snapshot**
   ```javascript
   const v8 = require('v8');
   const snapshot1 = v8.writeHeapSnapshot();
   ```

2. **Run Workload**
   ```javascript
   // Simulate user activity
   for (let i = 0; i < 1000; i++) {
     await handleRequest();
   }
   ```

3. **Take Second Snapshot**
   ```javascript
   const snapshot2 = v8.writeHeapSnapshot();
   ```

4. **Compare in Chrome DevTools**
   - Load both snapshots
   - Use "Comparison" view
   - Look for objects that increased significantly

### Retainer Paths

**What is it?**
- Shows what's keeping an object in memory

**Example:**
```
Object → EventEmitter → listeners → closure → largeArray
```

**Action:**
- Remove event listener to free `largeArray`

---

## Profiling Workflow

### Step-by-Step Process

1. **Baseline Measurement**
   ```bash
   # Measure current performance
   autocannon -c 10 -d 30 http://localhost:3000/api/endpoint
   ```

2. **Profile with Realistic Load**
   ```bash
   # Profile while load testing
   0x app.js &
   autocannon -c 50 -d 60 http://localhost:3000/api/endpoint
   ```

3. **Identify Hot Paths (>5% of time)**
   - Open flamegraph
   - Find wide boxes
   - Note function names and percentages

4. **Optimize Top Offenders**
   - Start with biggest bottleneck
   - Make one change at a time
   - Use better algorithms, caching, async operations

5. **Re-Profile to Verify Improvement**
   ```bash
   # Measure again
   autocannon -c 10 -d 30 http://localhost:3000/api/endpoint
   ```

6. **Document Results**
   ```markdown
   ## Optimization: Replaced O(n²) loop with hash map
   - Before: 250 req/s, P95: 450ms
   - After: 800 req/s, P95: 120ms
   - Improvement: 3.2x throughput, 73% latency reduction
   ```

---

## Optimization Strategies

### 1. Caching

**Example:**
```javascript
const cache = new Map();

async function getUser(id) {
  if (cache.has(id)) {
    return cache.get(id);
  }
  
  const user = await db.users.findUnique({ where: { id } });
  cache.set(id, user);
  return user;
}
```

### 2. Algorithm Improvement

**Example:**
```python
# Before: O(n²)
def find_pairs(arr, target):
    pairs = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] + arr[j] == target:
                pairs.append((arr[i], arr[j]))
    return pairs

# After: O(n)
def find_pairs(arr, target):
    seen = set()
    pairs = []
    for num in arr:
        complement = target - num
        if complement in seen:
            pairs.append((complement, num))
        seen.add(num)
    return pairs
```

### 3. Lazy Loading

**Example:**
```javascript
// Before: Load all data upfront
const allUsers = await db.users.findMany();

// After: Load on demand
async function* getUsers() {
  let cursor = null;
  while (true) {
    const batch = await db.users.findMany({
      take: 100,
      skip: cursor ? 1 : 0,
      cursor: cursor ? { id: cursor } : undefined
    });
    if (batch.length === 0) break;
    yield* batch;
    cursor = batch[batch.length - 1].id;
  }
}
```

### 4. Batch Processing

**Example:**
```javascript
// Before: One at a time
for (const item of items) {
  await processItem(item);
}

// After: Batched
const BATCH_SIZE = 10;
for (let i = 0; i < items.length; i += BATCH_SIZE) {
  const batch = items.slice(i, i + BATCH_SIZE);
  await Promise.all(batch.map(processItem));
}
```

### 5. Asynchronous Operations

**Example:**
```javascript
// Before: Sequential
const user = await getUser(id);
const posts = await getPosts(id);
const comments = await getComments(id);

// After: Parallel
const [user, posts, comments] = await Promise.all([
  getUser(id),
  getPosts(id),
  getComments(id)
]);
```

---

## Tools Comparison

### CLI Profilers vs GUI Profilers

| Feature | CLI (py-spy, 0x) | GUI (Chrome DevTools) |
|---------|------------------|------------------------|
| **Overhead** | Low | Medium |
| **Production** | ✅ Yes | ❌ No |
| **Ease of Use** | Medium | High |
| **Visualization** | Flamegraphs | Multiple views |
| **Code Changes** | None | None |

### Production Profilers (Low Overhead)

| Tool | Language | Overhead | Cost |
|------|----------|----------|------|
| **Datadog Profiler** | Node.js, Python, Java, Go | <1% | Paid |
| **Pyroscope** | Multi-language | <2% | Open-source |
| **py-spy** | Python | <1% | Open-source |
| **0x** | Node.js | ~5% | Open-source |

### Flamegraphs vs Call Trees

| Feature | Flamegraph | Call Tree |
|---------|------------|-----------|
| **Visual** | ✅ Intuitive | ❌ Text-based |
| **Hot Paths** | ✅ Easy to spot | ❌ Harder |
| **Exact Timing** | ❌ Relative | ✅ Precise |
| **Best For** | Finding bottlenecks | Detailed analysis |

---

## Real Profiling Examples

### Example 1: Slow API Endpoint

**Problem:**
```
GET /api/users/:id/dashboard
P95 latency: 2.5 seconds
```

**Profiling:**
```bash
0x app.js &
autocannon -c 20 -d 60 http://localhost:3000/api/users/123/dashboard
```

**Flamegraph Analysis:**
```
┌─────────────────────────────────────────────────┐
│              getDashboard()                     │
├──────────────────────┬──────────────────────────┤
│   getUser()          │   getRecentActivity()    │
│   (5%)               │   (85%)                  │
├──────────────────────┼──────────────────────────┤
│                      │   db.query() x 50        │
│                      │   (N+1 query!)           │
└──────────────────────┴──────────────────────────┘
```

**Root Cause:** N+1 query in `getRecentActivity()`

**Fix:**
```javascript
// Before
async function getRecentActivity(userId) {
  const activities = await db.activity.findMany({ where: { userId } });
  for (const activity of activities) {
    activity.user = await db.user.findUnique({ where: { id: activity.userId } });
  }
  return activities;
}

// After
async function getRecentActivity(userId) {
  return await db.activity.findMany({
    where: { userId },
    include: { user: true }
  });
}
```

**Result:**
- P95 latency: 2.5s → 180ms (93% improvement)

### Example 2: Memory Leak in Long-Running Process

**Problem:**
```
Python worker process memory grows from 100MB to 2GB over 24 hours
```

**Profiling:**
```bash
# Take snapshots over time
py-spy record -o profile1.svg --pid 12345 --duration 60
# Wait 1 hour
py-spy record -o profile2.svg --pid 12345 --duration 60
```

**Memory Analysis:**
```python
import tracemalloc

tracemalloc.start()

# Run for a while
process_jobs()

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

for stat in top_stats[:10]:
    print(stat)
```

**Output:**
```
/app/worker.py:45: size=1024 MiB, count=50000, average=21 KiB
  job_results.append(result)  # Never cleared!
```

**Root Cause:** Results list never cleared

**Fix:**
```python
# Before
job_results = []

def process_job(job):
    result = expensive_operation(job)
    job_results.append(result)  # Grows forever!

# After
def process_job(job):
    result = expensive_operation(job)
    save_to_database(result)  # Don't keep in memory
```

**Result:**
- Memory stable at ~150MB (no growth)

### Example 3: High CPU Usage Investigation

**Problem:**
```
Node.js API server CPU at 90% with only 100 req/s
```

**Profiling:**
```bash
clinic doctor -- node app.js &
autocannon -c 10 -d 60 http://localhost:3000/api/search
```

**Clinic.js Output:**
```
⚠️  Detected: Expensive synchronous operations
    Function: validateInput() - 65% of CPU time
```

**Code Analysis:**
```javascript
function validateInput(text) {
  // BAD: Catastrophic backtracking
  const regex = /(a+)+b/;
  return regex.test(text);
}
```

**Fix:**
```javascript
function validateInput(text) {
  // GOOD: Simple, efficient regex
  const regex = /^[a-z0-9]+$/;
  return regex.test(text);
}
```

**Result:**
- CPU usage: 90% → 15%
- Throughput: 100 req/s → 1200 req/s

---

## Implementation

### Node.js Profiling Script

**`scripts/profile.js`:**
```javascript
const { spawn } = require('child_process');
const fs = require('fs');

async function profile(command, args, duration = 60) {
  console.log(`Profiling: ${command} ${args.join(' ')}`);
  
  // Start application with profiling
  const profiler = spawn('0x', [command, ...args]);
  
  // Wait for app to start
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  // Run load test
  console.log('Running load test...');
  const loadTest = spawn('autocannon', [
    '-c', '50',
    '-d', duration.toString(),
    'http://localhost:3000'
  ]);
  
  loadTest.stdout.on('data', (data) => {
    console.log(data.toString());
  });
  
  await new Promise(resolve => loadTest.on('close', resolve));
  
  // Stop profiler
  profiler.kill('SIGINT');
  
  console.log('Profiling complete! Check flamegraph.html');
}

// Usage
profile('node', ['app.js'], 60);
```

### Python Profiling Decorator

**`utils/profiling.py`:**
```python
import functools
import cProfile
import pstats
import io
from pyinstrument import Profiler

def profile_cpu(func):
    """Decorator to profile CPU usage of a function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        profiler = Profiler()
        profiler.start()
        
        result = func(*args, **kwargs)
        
        profiler.stop()
        profiler.print()
        
        return result
    return wrapper

def profile_memory(func):
    """Decorator to profile memory usage of a function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import tracemalloc
        
        tracemalloc.start()
        
        result = func(*args, **kwargs)
        
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        
        print(f"\n[Memory Profile] Top 10 for {func.__name__}:")
        for stat in top_stats[:10]:
            print(stat)
        
        tracemalloc.stop()
        
        return result
    return wrapper

# Usage
@profile_cpu
@profile_memory
def expensive_function():
    data = [i ** 2 for i in range(1000000)]
    return sum(data)
```

### CI/CD Integration (Performance Regression Detection)

**`.github/workflows/performance.yml`:**
```yaml
name: Performance Tests

on:
  pull_request:
    branches: [main]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run baseline benchmark
        run: |
          npm start &
          sleep 5
          npx autocannon -c 10 -d 30 http://localhost:3000 > baseline.txt
      
      - name: Checkout PR branch
        run: git checkout ${{ github.head_ref }}
      
      - name: Run PR benchmark
        run: |
          npm start &
          sleep 5
          npx autocannon -c 10 -d 30 http://localhost:3000 > pr.txt
      
      - name: Compare results
        run: |
          node scripts/compare-benchmarks.js baseline.txt pr.txt
      
      - name: Fail if regression > 10%
        run: |
          if [ $REGRESSION -gt 10 ]; then
            echo "Performance regression detected: $REGRESSION%"
            exit 1
          fi
```

**`scripts/compare-benchmarks.js`:**
```javascript
const fs = require('fs');

function parseBenchmark(file) {
  const content = fs.readFileSync(file, 'utf8');
  const match = content.match(/Req\/Sec.*?(\d+\.?\d*)/);
  return parseFloat(match[1]);
}

const baseline = parseBenchmark(process.argv[2]);
const pr = parseBenchmark(process.argv[3]);

const regression = ((baseline - pr) / baseline) * 100;

console.log(`Baseline: ${baseline} req/s`);
console.log(`PR: ${pr} req/s`);
console.log(`Regression: ${regression.toFixed(2)}%`);

process.env.REGRESSION = regression.toFixed(0);

if (regression > 10) {
  console.error('❌ Performance regression detected!');
  process.exit(1);
} else {
  console.log('✅ Performance acceptable');
}
```

---

## Summary

### Quick Reference

**Node.js:**
- **Development**: Chrome DevTools, Clinic.js
- **Production**: 0x, Datadog, Pyroscope
- **Memory**: Chrome DevTools Heap Snapshot

**Python:**
- **Development**: cProfile, line_profiler, pyinstrument
- **Production**: py-spy, Datadog
- **Memory**: memory_profiler, tracemalloc

**Key Principles:**
1. Always profile before optimizing
2. Focus on hot paths (>5% of time)
3. Measure before and after
4. Use production-safe profilers in production
5. Flamegraphs are your friend

**Common Bottlenecks:**
- Synchronous I/O
- N+1 queries
- Inefficient algorithms
- Large JSON parsing
- Regex catastrophic backtracking
- Memory leaks

**Profiling Workflow:**
1. Baseline → 2. Profile → 3. Identify → 4. Optimize → 5. Verify → 6. Document
