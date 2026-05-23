---
name: python-advanced-profiling-and-optimization
version: "1.0"
description: >
  Advanced Python profiling with cProfile, py-spy, and optimization techniques including Python 3.13 features.
  PROACTIVELY activate for: (1) CPU profiling with cProfile, (2) Flame graph generation with py-spy,
  (3) Memory optimization, (4) Async performance patterns, (5) Python 3.13 JIT and free-threaded mode.
  Triggers: "python performance", "cProfile", "py-spy", "flame graph", "memory optimization", "async performance", "JIT", "GIL"
core-integration:
  techniques:
    primary: ["systematic_analysis"]
    secondary: ["structured_evaluation"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Python Advanced Profiling and Optimization

This skill provides expert-level knowledge on profiling Python applications to identify performance bottlenecks in CPU and memory usage, and guides evaluation and application of experimental Python 3.13 features.

## CPU Profiling with cProfile

cProfile is Python's built-in deterministic profiler, measuring execution time of all functions.

### Basic Usage

```python
import cProfile
import pstats

# Profile a specific function
def main():
    # Your application code
    result = expensive_operation()
    return result

if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.enable()

    main()

    profiler.disable()

    # Print stats sorted by cumulative time
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
```

### Command-Line Profiling

```bash
# Profile entire script
python -m cProfile -o output.prof script.py

# View results
python -m pstats output.prof
# Then in pstats shell:
# sort cumtime
# stats 20
```

### Interpreting Output

```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    10000    0.156    0.000    0.234    0.000 utils.py:45(process_data)
     5000    0.089    0.000    0.089    0.000 {built-in method json.loads}
```

**Columns**:
- **ncalls**: Number of calls
- **tottime**: Total time in function (excluding subcalls)
- **percall**: tottime / ncalls
- **cumtime**: Cumulative time (including subcalls) - **Most important**
- **percall**: cumtime / ncalls

**What to look for**:
- High cumtime functions are bottlenecks
- High ncalls with moderate cumtime suggests optimization opportunity
- Built-in functions with high time may indicate data structure issues

### Context Manager for Profiling

```python
import cProfile
import pstats
from contextlib import contextmanager

@contextmanager
def profile(output_file=None):
    """Context manager for profiling code blocks"""
    profiler = cProfile.Profile()
    profiler.enable()

    try:
        yield profiler
    finally:
        profiler.disable()

        if output_file:
            profiler.dump_stats(output_file)
        else:
            stats = pstats.Stats(profiler)
            stats.sort_stats('cumulative')
            stats.print_stats(20)

# Usage
with profile('endpoint.prof'):
    process_api_request(data)
```

## Flame Graph Generation with py-spy

py-spy is a sampling profiler that can attach to running processes without code modification.

### Installation

```bash
pip install py-spy
```

### Basic Usage

```bash
# Profile running process by PID
py-spy record -o profile.svg --pid 12345

# Profile script directly
py-spy record -o profile.svg -- python script.py

# Live top-like view
py-spy top --pid 12345
```

### Reading Flame Graphs

**Flame graph structure**:
- **X-axis**: Alphabetical order (NOT time)
- **Y-axis**: Stack depth (bottom = entry point, top = deepest call)
- **Width**: Percentage of total time

**What to look for**:
- **Wide blocks**: Functions consuming most time
- **Tall stacks**: Deep call chains (may indicate recursion issues)
- **Flat plateaus**: Hot paths through code

### Profiling Production Services

```bash
# Attach to running Uvicorn/Gunicorn worker
# Find PID: ps aux | grep uvicorn
py-spy record -o api-profile.svg --pid $(pgrep -f uvicorn) --duration 30

# Profile with native extensions
py-spy record --native -o profile.svg --pid 12345
```

### Comparing Before/After

```bash
# Before optimization
py-spy record -o before.svg -- python script.py

# After optimization
py-spy record -o after.svg -- python script.py

# Compare visually or use speedscope.app
```

## Memory Optimization Techniques

Reducing memory footprint improves performance and allows scaling to more users.

### Using __slots__

For classes with fixed attributes, `__slots__` significantly reduces memory usage.

```python
# BAD: Uses __dict__ (high memory overhead)
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

# GOOD: Uses __slots__ (lower memory)
class User:
    __slots__ = ('name', 'email')

    def __init__(self, name, email):
        self.name = name
        self.email = email

# Memory savings: ~40-50% per instance
```

**When to use**: Classes with many instances (models, data structures)
**When NOT to use**: Classes needing dynamic attributes

### Generators vs Lists

Generators process data lazily, reducing memory footprint.

```python
# BAD: Loads entire dataset into memory
def get_all_users():
    users = []
    for row in db.query("SELECT * FROM users"):
        users.append(process_user(row))
    return users

total = sum(user.score for user in get_all_users())

# GOOD: Generator yields one at a time
def get_all_users():
    for row in db.query("SELECT * FROM users"):
        yield process_user(row)

total = sum(user.score for user in get_all_users())
```

**Memory savings**: Proportional to dataset size (can be orders of magnitude)

### String Concatenation

```python
# BAD: Creates new string object each iteration
result = ""
for item in items:
    result += str(item) + ","  # O(n^2) time and memory

# GOOD: Join at the end
result = ",".join(str(item) for item in items)  # O(n)
```

### Using array Module for Numeric Data

```python
# BAD: List of integers (high memory)
numbers = [1, 2, 3, 4, 5] * 100000  # ~800 KB

# GOOD: Array of integers (low memory)
import array
numbers = array.array('i', [1, 2, 3, 4, 5] * 100000)  # ~400 KB

# EVEN BETTER: NumPy for numerical computation
import numpy as np
numbers = np.array([1, 2, 3, 4, 5] * 100000)  # ~400 KB + vectorized operations
```

### Memory Profiling with memory_profiler

```bash
pip install memory-profiler
```

```python
from memory_profiler import profile

@profile
def load_data():
    data = [i for i in range(1000000)]  # Line-by-line memory usage
    processed = [x * 2 for x in data]
    return processed

if __name__ == '__main__':
    load_data()
```

Run with:
```bash
python -m memory_profiler script.py
```

### Python 3.13 Docstring Stripping

Python 3.13 supports docstring stripping to reduce memory:

```bash
# Build Python with docstring stripping
./configure --with-pydoc=no
# Or use PYTHONOPTIMIZE=2
python -OO script.py  # Strips docstrings
```

**Memory savings**: 5-10% in typical applications

## Evaluating Experimental Python 3.13 Features

Python 3.13 introduces experimental performance features that require careful evaluation.

### JIT Compiler

Python 3.13 includes an experimental JIT compiler for potential performance gains.

#### Enabling JIT

```bash
# Build Python with JIT enabled
./configure --enable-experimental-jit
make
```

Or use official Python 3.13+ with:
```bash
PYTHON_JIT=1 python script.py
```

#### When to Use JIT

**Good candidates**:
- CPU-bound workloads
- Tight loops with numeric computation
- Long-running processes
- Pure Python code (not C extensions)

**Poor candidates**:
- I/O-bound workloads
- Short-lived scripts
- Code dominated by C extensions (NumPy, etc.)

#### Benchmarking JIT

```python
import time

def cpu_intensive_task(n):
    """Pure Python computation - good JIT candidate"""
    result = 0
    for i in range(n):
        result += i * i
    return result

# Benchmark without JIT
start = time.perf_counter()
result = cpu_intensive_task(10_000_000)
print(f"Without JIT: {time.perf_counter() - start:.3f}s")

# Run again with PYTHON_JIT=1
# Expected: 5-15% improvement for CPU-bound code
```

#### Current Limitations

- **Modest gains**: 5-15% for CPU-bound code (as of Python 3.13)
- **Warm-up time**: Initial runs may be slower
- **Memory overhead**: JIT compilation uses extra memory
- **Experimental**: May have bugs, not production-ready yet

### Free-Threaded Mode (No-GIL)

Python 3.13 includes experimental support for running without the Global Interpreter Lock (GIL).

#### Enabling Free-Threaded Mode

```bash
# Build Python without GIL
./configure --disable-gil
make
```

Or use official builds:
```bash
python3.13t  # 't' suffix indicates free-threaded build
```

#### When to Use

**Good candidates**:
- CPU-bound multi-threaded workloads
- Applications with parallel computation
- Web servers handling concurrent requests
- Data processing pipelines

**Poor candidates**:
- I/O-bound workloads (already benefits from asyncio)
- Single-threaded applications
- Code relying on C extensions without thread safety

#### Critical Considerations

**C Extension Compatibility**: Most C extensions are NOT thread-safe without GIL

**Compatible**: Pure Python, some newer C extensions
**Incompatible**: NumPy, pandas, many others (as of early 2024)

Check compatibility:
```python
import sys
print(sys._is_gil_enabled())  # False if running free-threaded
```

#### Benchmarking Multi-Threading

```python
import threading
import time

def cpu_work(n):
    """CPU-intensive task"""
    result = sum(i * i for i in range(n))
    return result

def benchmark_threads(n_threads, work_size):
    start = time.perf_counter()

    threads = []
    for _ in range(n_threads):
        thread = threading.Thread(target=cpu_work, args=(work_size,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    elapsed = time.perf_counter() - start
    print(f"{n_threads} threads: {elapsed:.3f}s")

# With GIL: No speedup (may be slower due to contention)
# Without GIL: Near-linear speedup for CPU-bound work
benchmark_threads(4, 10_000_000)
```

#### Migration Strategy

1. **Profile first**: Confirm CPU-bound multi-threaded bottleneck
2. **Check dependencies**: Verify all C extensions are compatible
3. **Test thoroughly**: Free-threaded mode changes behavior
4. **Benchmark**: Measure actual performance improvement
5. **Monitor stability**: Watch for race conditions and crashes

## AsyncIO Performance Patterns

Async code can be fast or slow depending on implementation.

### Good Patterns

```python
import asyncio

# GOOD: Concurrent I/O operations
async def fetch_all_users():
    async with aiohttp.ClientSession() as session:
        tasks = [
            session.get(f'https://api.example.com/users/{i}')
            for i in range(100)
        ]
        responses = await asyncio.gather(*tasks)
        return responses

# GOOD: Using asyncio.to_thread for blocking operations
async def process_request():
    # Blocking call offloaded to thread pool
    result = await asyncio.to_thread(blocking_cpu_work, data)
    return result
```

### Anti-Patterns

```python
# BAD: Blocking the event loop
async def slow_handler():
    time.sleep(5)  # Blocks entire event loop!
    return "done"

# GOOD: Use asyncio.sleep
async def fast_handler():
    await asyncio.sleep(5)  # Yields control
    return "done"

# BAD: Not awaiting concurrent operations
async def sequential_fetches():
    result1 = await fetch_user(1)
    result2 = await fetch_user(2)  # Waits for result1 first
    return result1, result2

# GOOD: Concurrent fetches
async def parallel_fetches():
    result1, result2 = await asyncio.gather(
        fetch_user(1),
        fetch_user(2)  # Runs concurrently
    )
    return result1, result2
```

## Anti-Patterns

### Profiling I/O-Bound Code with CPU Profiler

CPU profilers show time spent in functions, not time waiting for I/O.

For I/O-bound code, use async profiling or tracing tools.

### Enabling Experimental Features Without Measurement

JIT and no-GIL modes are experimental. Always benchmark before deploying.

### Optimizing Without Profiling

"Premature optimization is the root of all evil." Profile first.

### Ignoring Profiler Overhead

cProfile adds ~1-3% overhead. For very hot loops, use py-spy instead.

### Using Lists When Generators Suffice

Loading gigabytes into memory when streaming would work.

## Optimization Checklist

- [ ] Profile with cProfile to identify slow functions
- [ ] Generate flame graphs with py-spy for visual analysis
- [ ] Use __slots__ for classes with many instances
- [ ] Replace lists with generators for large datasets
- [ ] Use array/NumPy for numeric data
- [ ] Fix string concatenation in loops (use join)
- [ ] Profile memory with memory_profiler if usage is high
- [ ] Check for blocking calls in asyncio (use asyncio.to_thread)
- [ ] Benchmark JIT if CPU-bound (Python 3.13+)
- [ ] Evaluate free-threaded mode only for multi-threaded CPU-bound workloads
- [ ] Validate C extension compatibility before disabling GIL

## Performance Targets

- **API response time**: < 100ms (p50), < 500ms (p99)
- **Memory per worker**: < 512 MB typical
- **CPU usage**: < 70% average (headroom for spikes)
- **GC pause time**: < 10ms (minimize object churn)
