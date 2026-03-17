---
name: code-optimizer
description: Analyzes and optimizes code for better performance, memory usage, and efficiency. Use when code is slow, memory-intensive, or inefficient. Supports Python and Java optimization including execution speed improvements, memory reduction, database query optimization, and I/O efficiency. Provides before/after examples with detailed explanations of why optimizations work, complexity analysis, and measurable performance improvements.
---

# Code Optimizer

Improve code performance, memory usage, and efficiency through systematic optimization.

## Core Capabilities

This skill helps optimize code by:

1. **Analyzing performance bottlenecks** - Identifying slow or inefficient code
2. **Suggesting optimizations** - Providing concrete improvements with examples
3. **Explaining trade-offs** - Describing benefits and potential drawbacks
4. **Measuring impact** - Estimating performance gains
5. **Preserving correctness** - Ensuring optimizations don't change behavior

## Optimization Workflow

### Step 1: Identify Optimization Opportunities

Analyze code to find performance bottlenecks.

**Look for:**
- Nested loops (O(n²) or worse complexity)
- Repeated expensive operations
- Inefficient data structures
- Unnecessary object creation
- Database N+1 queries
- Blocking I/O operations
- Memory leaks or excessive allocation

**Quick Analysis Questions:**
- What is the time complexity? Can it be reduced?
- Are there repeated calculations that could be cached?
- Is the right data structure being used?
- Are there unnecessary copies or allocations?
- Can operations be batched or parallelized?

### Step 2: Categorize the Optimization

Determine the type of optimization needed.

**Execution Speed:**
- Algorithm optimization (better complexity)
- Loop optimization
- Caching/memoization
- Lazy evaluation
- Parallel processing

**Memory Usage:**
- Reduce object creation
- Use generators/streams instead of lists
- Clear references to enable garbage collection
- Use appropriate data structures
- Avoid memory leaks

**Database Operations:**
- Query optimization (indexes, joins)
- Batch operations
- Connection pooling
- Caching
- Reduce round trips

**I/O Operations:**
- Buffering
- Async/non-blocking I/O
- Batch requests
- Compression
- Caching

### Step 3: Propose Optimization with Examples

Provide before/after code with clear explanations.

**Optimization Template:**

```markdown
## Optimization: [Brief Description]

### Before (Inefficient)
```[language]
[original code]
```

**Issues:**
- Issue 1: [Problem description]
- Issue 2: [Problem description]

**Complexity:** O([complexity])
**Performance:** [estimated time/memory]

### After (Optimized)
```[language]
[optimized code]
```

**Improvements:**
- Improvement 1: [What changed]
- Improvement 2: [What changed]

**Complexity:** O([new complexity])
**Performance:** [estimated time/memory]
**Gain:** [X% faster / Y% less memory]

### Why This Works

[Detailed explanation of the optimization]

### Trade-offs

**Pros:**
- [Benefit 1]
- [Benefit 2]

**Cons:**
- [Drawback 1, if any]
- [Drawback 2, if any]

### When to Use

- Use when: [scenario]
- Avoid when: [scenario]
```

### Step 4: Measure and Validate

Ensure optimization actually improves performance.

**Measurement Techniques:**

**Python:**
```python
import time
import memory_profiler

# Time measurement
start = time.time()
result = function()
elapsed = time.time() - start
print(f"Elapsed: {elapsed:.4f}s")

# Memory measurement
from memory_profiler import profile

@profile
def function():
    # Code to profile
    pass
```

**Java:**
```java
// Time measurement
long start = System.nanoTime();
result = function();
long elapsed = System.nanoTime() - start;
System.out.println("Elapsed: " + elapsed / 1_000_000 + "ms");

// Memory measurement
Runtime runtime = Runtime.getRuntime();
long before = runtime.totalMemory() - runtime.freeMemory();
result = function();
long after = runtime.totalMemory() - runtime.freeMemory();
System.out.println("Memory used: " + (after - before) / 1024 + "KB");
```

**Validation Checklist:**
- ✓ Correctness: Output matches original
- ✓ Performance: Measurable improvement
- ✓ Memory: Reduced allocation or leaks fixed
- ✓ Maintainability: Code remains readable
- ✓ Edge cases: Handles all inputs correctly

## Common Optimizations

### Python Optimizations

#### 1. Use List Comprehensions Over Loops

```python
# Before: O(n) with overhead
numbers = []
for i in range(1000):
    if i % 2 == 0:
        numbers.append(i * 2)

# After: O(n) faster execution
numbers = [i * 2 for i in range(1000) if i % 2 == 0]

# Gain: 2-3x faster
```

#### 2. Use Generators for Large Sequences

```python
# Before: O(n) memory
def get_numbers(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result

numbers = get_numbers(1000000)  # Uses ~8MB memory

# After: O(1) memory
def get_numbers(n):
    for i in range(n):
        yield i ** 2

numbers = get_numbers(1000000)  # Uses minimal memory

# Gain: 99% less memory for large n
```

#### 3. Use Built-in Functions

```python
# Before: Slower
total = 0
for num in numbers:
    total += num

# After: Faster (C implementation)
total = sum(numbers)

# Gain: 10-20x faster for large lists
```

#### 4. Avoid Repeated Lookups

```python
# Before: Repeated lookups
for i in range(len(data)):
    process(data[i])

# After: Single lookup
for item in data:
    process(item)

# Or with enumerate
for i, item in enumerate(data):
    process(item)

# Gain: Faster iteration, more Pythonic
```

#### 5. Use Sets for Membership Testing

```python
# Before: O(n) per lookup
items = [1, 2, 3, 4, 5, ...]  # Large list
if x in items:  # O(n) lookup
    do_something()

# After: O(1) per lookup
items = {1, 2, 3, 4, 5, ...}  # Set
if x in items:  # O(1) lookup
    do_something()

# Gain: 100x faster for large collections
```

See `references/python_optimizations.md` for comprehensive Python optimization patterns.

### Java Optimizations

#### 1. Use StringBuilder for String Concatenation

```java
// Before: O(n²) - creates n strings
String result = "";
for (int i = 0; i < 1000; i++) {
    result += i + ",";  // Creates new string each time
}

// After: O(n) - single buffer
StringBuilder result = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    result.append(i).append(",");
}
String output = result.toString();

// Gain: 100x faster for large loops
```

#### 2. Use Appropriate Collection Types

```java
// Before: Wrong data structure
List<Integer> numbers = new ArrayList<>();
numbers.contains(42);  // O(n) lookup

// After: Right data structure
Set<Integer> numbers = new HashSet<>();
numbers.contains(42);  // O(1) lookup

// Gain: 1000x faster for large collections
```

#### 3. Avoid Unnecessary Object Creation

```java
// Before: Creates objects in loop
for (int i = 0; i < 1000; i++) {
    String key = new String("key" + i);  // Unnecessary
    map.put(key, value);
}

// After: Reuse or use literals
for (int i = 0; i < 1000; i++) {
    String key = "key" + i;  // String interning
    map.put(key, value);
}

// Gain: Less GC pressure, faster
```

#### 4. Use Primitive Collections

```java
// Before: Autoboxing overhead
List<Integer> numbers = new ArrayList<>();
for (int i = 0; i < 1000000; i++) {
    numbers.add(i);  // Boxing int to Integer
}

// After: Primitive arrays or specialized libraries
int[] numbers = new int[1000000];
for (int i = 0; i < 1000000; i++) {
    numbers[i] = i;  // No boxing
}

// Or use TIntArrayList from Trove
TIntArrayList numbers = new TIntArrayList();

// Gain: 50% less memory, faster access
```

See `references/java_optimizations.md` for comprehensive Java optimization patterns.

### Database Optimizations

#### 1. Fix N+1 Query Problem

```python
# Before: N+1 queries
users = User.query.all()  # 1 query
for user in users:
    posts = user.posts.all()  # N queries
    process(posts)

# After: Single query with join
users = User.query.options(
    joinedload(User.posts)
).all()  # 1 query
for user in users:
    posts = user.posts  # Already loaded
    process(posts)

# Gain: 100x faster for large datasets
```

#### 2. Add Indexes

```sql
-- Before: Full table scan O(n)
SELECT * FROM users WHERE email = 'user@example.com';

-- After: Index lookup O(log n)
CREATE INDEX idx_users_email ON users(email);
SELECT * FROM users WHERE email = 'user@example.com';

-- Gain: 1000x faster for large tables
```

#### 3. Batch Operations

```python
# Before: N round trips
for item in items:
    db.execute("INSERT INTO table VALUES (?)", (item,))
    db.commit()

# After: Single batch
db.executemany("INSERT INTO table VALUES (?)",
               [(item,) for item in items])
db.commit()

# Gain: 10-100x faster
```

See `references/database_optimizations.md` for comprehensive database optimization patterns.

### I/O Optimizations

#### 1. Use Buffered I/O

```python
# Before: Unbuffered (many system calls)
with open('file.txt', 'r') as f:
    for line in f:
        process(line.strip())

# After: Buffered reading
with open('file.txt', 'r', buffering=8192) as f:
    for line in f:
        process(line.strip())

# Gain: 10x faster for small lines
```

#### 2. Batch API Calls

```python
# Before: N API calls
for user_id in user_ids:
    user = api.get_user(user_id)  # 100 calls
    process(user)

# After: Batch API call
users = api.get_users_batch(user_ids)  # 1 call
for user in users:
    process(user)

# Gain: 100x faster (network latency)
```

## Optimization Process

### 1. Profile Before Optimizing

**Python Profiling:**
```bash
# Time profiling
python -m cProfile -s cumulative script.py

# Line-by-line profiling
pip install line_profiler
kernprof -l -v script.py

# Memory profiling
pip install memory_profiler
python -m memory_profiler script.py
```

**Java Profiling:**
```bash
# JVM profiling with VisualVM
jvisualvm

# Or Java Flight Recorder
java -XX:+UnlockCommercialFeatures -XX:+FlightRecorder \
     -XX:StartFlightRecording=duration=60s,filename=recording.jfr \
     MyApp
```

### 2. Focus on Hot Paths

Optimize the 20% of code that takes 80% of time.

**Find Hot Paths:**
- Profile to find slowest functions
- Measure actual execution time
- Focus on code executed frequently
- Ignore code executed rarely

### 3. Measure Impact

Compare before and after:

```python
import timeit

# Before
before = timeit.timeit(
    'old_function(data)',
    setup='from module import old_function, data',
    number=1000
)

# After
after = timeit.timeit(
    'new_function(data)',
    setup='from module import new_function, data',
    number=1000
)

improvement = (before - after) / before * 100
print(f"Improvement: {improvement:.1f}%")
```

### 4. Maintain Readability

Don't sacrifice code clarity for minor gains.

**Good Optimization:**
```python
# Clear and fast
users = [u for u in all_users if u.is_active]
```

**Bad Optimization:**
```python
# Obscure for minimal gain
users = list(filter(lambda u: u.is_active, all_users))
```

## Best Practices

1. **Profile first** - Don't guess, measure
2. **Focus on bottlenecks** - Optimize hot paths only
3. **Preserve correctness** - Test thoroughly after optimizing
4. **Document trade-offs** - Explain why optimization is worth it
5. **Measure improvements** - Quantify performance gains
6. **Consider maintainability** - Don't make code unreadable
7. **Use appropriate tools** - Profilers, benchmarks, load tests
8. **Think about complexity** - O(n²) to O(n log n) matters more than micro-optimizations
9. **Cache wisely** - Balance memory vs. computation
10. **Avoid premature optimization** - Optimize when proven necessary

## Resources

- **`references/python_optimizations.md`** - Comprehensive Python optimization techniques and patterns
- **`references/java_optimizations.md`** - Comprehensive Java optimization techniques and patterns
- **`references/database_optimizations.md`** - Database query and schema optimization strategies

## Quick Reference

| Optimization Type | Python | Java | Impact |
|------------------|--------|------|--------|
| Algorithm complexity | Use better algorithm | Use better algorithm | High |
| Data structures | set/dict for lookup | HashMap/HashSet | High |
| String building | join() or f-strings | StringBuilder | High |
| Generators | yield | Stream API | Medium (memory) |
| Caching | @lru_cache | ConcurrentHashMap | Medium-High |
| Batching | Batch DB/API calls | Batch operations | High |
| Indexing | Use dict/set | Add DB indexes | High |
| Lazy evaluation | Generators | Streams/Suppliers | Medium |
