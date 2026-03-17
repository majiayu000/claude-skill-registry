---
name: performance-profiling
description: Automatically applies when profiling Python performance. Ensures proper use of profiling tools, async profiling, benchmarking, memory analysis, and optimization strategies.
category: observability
---

# Performance Profiling Patterns

When profiling Python applications, follow these patterns for effective performance analysis.

**Trigger Keywords**: profiling, performance, benchmark, optimization, cProfile, line_profiler, memory_profiler, async profiling, bottleneck, CPU profiling

**Agent Integration**: Used by `performance-engineer`, `backend-architect`, `optimization-engineer`

## ✅ Correct Pattern: CPU Profiling

```python
import cProfile
import pstats
from pstats import SortKey
from typing import Callable
from functools import wraps


def profile_function(output_file: str = None):
    """
    Decorator to profile function execution.

    Args:
        output_file: Optional file to save profile data
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            profiler = cProfile.Profile()
            profiler.enable()

            try:
                result = func(*args, **kwargs)
                return result
            finally:
                profiler.disable()

                # Print stats
                stats = pstats.Stats(profiler)
                stats.sort_stats(SortKey.CUMULATIVE)
                stats.print_stats(20)  # Top 20 functions

                # Save to file
                if output_file:
                    stats.dump_stats(output_file)

        return wrapper
    return decorator


# Usage
@profile_function(output_file="profile.stats")
def process_data(data: List[Dict]):
    """Process data with profiling."""
    result = []
    for item in data:
        processed = expensive_operation(item)
        result.append(processed)
    return result


# Analyze saved profile
def analyze_profile(stats_file: str):
    """Analyze saved profile data."""
    stats = pstats.Stats(stats_file)

    print("\n=== Top 20 by cumulative time ===")
    stats.sort_stats(SortKey.CUMULATIVE)
    stats.print_stats(20)

    print("\n=== Top 20 by internal time ===")
    stats.sort_stats(SortKey.TIME)
    stats.print_stats(20)

    print("\n=== Top 20 by call count ===")
    stats.sort_stats(SortKey.CALLS)
    stats.print_stats(20)
```

## Line-by-Line Profiling

```python
from line_profiler import LineProfiler


def profile_lines(func: Callable) -> Callable:
    """
    Decorator for line-by-line profiling.

    Usage:
        @profile_lines
        def my_function():
            ...

        my_function()
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = LineProfiler()
        profiler.add_function(func)
        profiler.enable()

        try:
            result = func(*args, **kwargs)
            return result
        finally:
            profiler.disable()
            profiler.print_stats()

    return wrapper


# Usage
@profile_lines
def process_items(items: List[str]) -> List[str]:
    """Process items with line profiling."""
    result = []

    for item in items:
        # Each line's execution time is measured
        cleaned = item.strip().lower()
        if len(cleaned) > 5:
            processed = expensive_transform(cleaned)
            result.append(processed)

    return result


# Alternative: Profile specific functions
def detailed_profile():
    """Profile multiple functions."""
    lp = LineProfiler()

    # Add functions to profile
    lp.add_function(function1)
    lp.add_function(function2)
    lp.add_function(function3)

    # Run with profiling
    lp.enable()
    main_function()
    lp.disable()

    lp.print_stats()
```

## Memory Profiling

```python
from memory_profiler import profile as memory_profile
import tracemalloc


@memory_profile
def memory_intensive_function():
    """
    Profile memory usage.

    Requires: pip install memory-profiler
    """
    data = []

    for i in range(1000000):
        data.append(i * 2)

    return data


# Tracemalloc for detailed memory tracking
def track_memory_detailed():
    """Track memory allocations in detail."""
    tracemalloc.start()

    # Code to profile
    data = memory_intensive_function()

    # Get current memory usage
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory: {current / 1024 / 1024:.2f} MB")
    print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")

    # Get top memory allocations
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    print("\n=== Top 10 memory allocations ===")
    for stat in top_stats[:10]:
        print(stat)

    tracemalloc.stop()


# Context manager for memory tracking
class MemoryTracker:
    """Context manager to track memory usage."""

    def __enter__(self):
        tracemalloc.start()
        self.start_memory = tracemalloc.get_traced_memory()[0]
        return self

    def __exit__(self, *args):
        current, peak = tracemalloc.get_traced_memory()
        self.memory_used = current - self.start_memory
        self.peak_memory = peak
        tracemalloc.stop()

        print(f"Memory used: {self.memory_used / 1024 / 1024:.2f} MB")
        print(f"Peak memory: {self.peak_memory / 1024 / 1024:.2f} MB")


# Usage
with MemoryTracker() as tracker:
    result = memory_intensive_function()

print(f"Total memory: {tracker.memory_used / 1024 / 1024:.2f} MB")
```

## Async Profiling

```python
import asyncio
import time
from typing import Coroutine


class AsyncProfiler:
    """Profile async function execution."""

    def __init__(self):
        self.timings = {}

    async def profile(self, name: str, coro: Coroutine):
        """
        Profile async coroutine.

        Args:
            name: Profile label
            coro: Coroutine to profile

        Returns:
            Coroutine result
        """
        start = time.perf_counter()

        try:
            result = await coro
            duration = time.perf_counter() - start

            self.timings[name] = {
                "duration": duration,
                "status": "success"
            }

            return result

        except Exception as e:
            duration = time.perf_counter() - start

            self.timings[name] = {
                "duration": duration,
                "status": "error",
                "error": str(e)
            }

            raise

    def print_stats(self):
        """Print profiling statistics."""
        print("\n=== Async Profile Stats ===")
        print(f"{'Function':<30} {'Duration':>10} {'Status':>10}")
        print("-" * 52)

        for name, stats in sorted(
            self.timings.items(),
            key=lambda x: x[1]["duration"],
            reverse=True
        ):
            duration = stats["duration"]
            status = stats["status"]
            print(f"{name:<30} {duration:>10.4f}s {status:>10}")


# Usage
async def main():
    profiler = AsyncProfiler()

    # Profile async operations
    users = await profiler.profile(
        "fetch_users",
        fetch_users_from_db()
    )

    orders = await profiler.profile(
        "fetch_orders",
        fetch_orders_from_api()
    )

    result = await profiler.profile(
        "process_data",
        process_data(users, orders)
    )

    profiler.print_stats()

    return result


# Decorator version
def profile_async(name: str = None):
    """Decorator to profile async functions."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            func_name = name or func.__name__
            start = time.perf_counter()

            try:
                result = await func(*args, **kwargs)
                duration = time.perf_counter() - start

                print(f"{func_name}: {duration:.4f}s")

                return result

            except Exception as e:
                duration = time.perf_counter() - start
                print(f"{func_name}: {duration:.4f}s (error)")
                raise

        return wrapper
    return decorator


@profile_async("fetch_users")
async def fetch_users():
    """Fetch users with profiling."""
    await asyncio.sleep(0.5)
    return ["user1", "user2"]
```

## Benchmarking

```python
import timeit
from typing import Callable, List, Dict
from statistics import mean, stdev


class Benchmark:
    """Benchmark function performance."""

    def __init__(self, iterations: int = 1000):
        self.iterations = iterations
        self.results: Dict[str, List[float]] = {}

    def run(self, name: str, func: Callable, *args, **kwargs):
        """
        Run benchmark for function.

        Args:
            name: Benchmark name
            func: Function to benchmark
            *args, **kwargs: Function arguments
        """
        times = []

        for _ in range(self.iterations):
            start = time.perf_counter()
            func(*args, **kwargs)
            duration = time.perf_counter() - start
            times.append(duration)

        self.results[name] = times

    def compare(self, name1: str, name2: str):
        """Compare two benchmarks."""
        times1 = self.results[name1]
        times2 = self.results[name2]

        mean1 = mean(times1)
        mean2 = mean(times2)

        improvement = ((mean1 - mean2) / mean1) * 100

        print(f"\n=== Comparison: {name1} vs {name2} ===")
        print(f"{name1}: {mean1*1000:.4f}ms ± {stdev(times1)*1000:.4f}ms")
        print(f"{name2}: {mean2*1000:.4f}ms ± {stdev(times2)*1000:.4f}ms")
        print(f"Improvement: {improvement:+.2f}%")

    def print_stats(self):
        """Print all benchmark statistics."""
        print("\n=== Benchmark Results ===")
        print(f"{'Name':<30} {'Mean':>12} {'Std Dev':>12} {'Min':>12} {'Max':>12}")
        print("-" * 80)

        for name, times in self.results.items():
            mean_time = mean(times) * 1000
            std_time = stdev(times) * 1000
            min_time = min(times) * 1000
            max_time = max(times) * 1000

            print(
                f"{name:<30} "
                f"{mean_time:>10.4f}ms "
                f"{std_time:>10.4f}ms "
                f"{min_time:>10.4f}ms "
                f"{max_time:>10.4f}ms"
            )


# Usage
bench = Benchmark(iterations=1000)

# Benchmark different implementations
bench.run("list_comprehension", lambda: [i*2 for i in range(1000)])
bench.run("map_function", lambda: list(map(lambda i: i*2, range(1000))))
bench.run("for_loop", lambda: [i*2 for i in range(1000)])

bench.print_stats()
bench.compare("list_comprehension", "map_function")


# Using timeit module
def benchmark_with_timeit():
    """Benchmark with timeit module."""

    # Setup code
    setup = """
from mymodule import function1, function2
data = list(range(10000))
"""

    # Benchmark function1
    time1 = timeit.timeit(
        "function1(data)",
        setup=setup,
        number=1000
    )

    # Benchmark function2
    time2 = timeit.timeit(
        "function2(data)",
        setup=setup,
        number=1000
    )

    print(f"function1: {time1:.4f}s")
    print(f"function2: {time2:.4f}s")
    print(f"Speedup: {time1/time2:.2f}x")
```

## Performance Testing

```python
import pytest
from typing import Callable


def test_performance(
    func: Callable,
    max_duration_ms: float,
    iterations: int = 100
):
    """
    Test function performance.

    Args:
        func: Function to test
        max_duration_ms: Maximum allowed duration in ms
        iterations: Number of iterations
    """
    durations = []

    for _ in range(iterations):
        start = time.perf_counter()
        func()
        duration = (time.perf_counter() - start) * 1000
        durations.append(duration)

    avg_duration = mean(durations)

    assert avg_duration < max_duration_ms, (
        f"Performance regression: {avg_duration:.2f}ms > {max_duration_ms}ms"
    )


# Pytest performance tests
@pytest.mark.performance
def test_api_response_time():
    """Test API response time is under 100ms."""

    def api_call():
        response = requests.get("http://localhost:8000/api/users")
        return response.json()

    test_performance(api_call, max_duration_ms=100.0, iterations=50)


@pytest.mark.performance
def test_database_query_time():
    """Test database query time is under 50ms."""

    def db_query():
        return db.query(User).filter(User.status == "active").all()

    test_performance(db_query, max_duration_ms=50.0, iterations=100)
```

## ❌ Anti-Patterns

```python
# ❌ Using print() for timing
start = time.time()
result = expensive_function()
print(f"Took {time.time() - start}s")  # Not precise!

# ✅ Better: Use proper profiling
@profile_function()
def expensive_function():
    ...


# ❌ Single measurement
time = timeit.timeit(func, number=1)  # Not reliable!

# ✅ Better: Multiple iterations
times = [timeit.timeit(func, number=1) for _ in range(100)]
avg_time = mean(times)


# ❌ Not profiling before optimizing
# Just guessing where the bottleneck is

# ✅ Better: Profile first, then optimize
@profile_function()
def identify_bottleneck():
    ...


# ❌ Profiling in production without limits
profiler.enable()  # Runs forever!

# ✅ Better: Time-limited profiling
import signal
profiler.enable()
signal.alarm(60)  # Stop after 60 seconds
```

## Best Practices Checklist

- ✅ Profile before optimizing (measure, don't guess)
- ✅ Use appropriate profiling tool (cProfile, line_profiler)
- ✅ Profile memory usage for memory-intensive code
- ✅ Use async profiling for async code
- ✅ Benchmark different implementations
- ✅ Run multiple iterations for reliability
- ✅ Track performance over time
- ✅ Set performance budgets in tests
- ✅ Profile in realistic conditions
- ✅ Focus on hot paths first
- ✅ Document performance characteristics
- ✅ Use sampling for production profiling

## Auto-Apply

When profiling performance:
1. Use cProfile for CPU profiling
2. Use line_profiler for line-by-line analysis
3. Use memory_profiler for memory tracking
4. Profile async code with AsyncProfiler
5. Benchmark alternatives with Benchmark class
6. Add performance tests with time limits
7. Focus on hot paths identified by profiling

## Related Skills

- `monitoring-alerting` - For production metrics
- `query-optimization` - For database performance
- `async-await-checker` - For async patterns
- `pytest-patterns` - For performance testing
