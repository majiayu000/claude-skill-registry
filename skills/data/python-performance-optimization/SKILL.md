---
name: python-performance-optimization
description: Python performance optimization patterns using profiling, algorithmic improvements, and acceleration techniques. Use when optimizing slow Python code, reducing memory usage, or improving application throughput and latency.
---

# Python Performance Optimization

Expert guidance for profiling, optimizing, and accelerating Python applications through systematic analysis, algorithmic improvements, efficient data structures, and acceleration techniques.

## When to Use This Skill

- Code runs too slowly for production requirements
- High CPU usage or memory consumption issues
- Need to reduce API response times or batch processing duration
- Application fails to scale under load
- Optimizing data processing pipelines or scientific computing
- Reducing cloud infrastructure costs through efficiency gains
- Profile-guided optimization after measuring performance bottlenecks

## Core Concepts

**The Golden Rule**: Never optimize without profiling first. 80% of execution time is spent in 20% of code.

**Optimization Hierarchy** (in priority order):
1. **Algorithm complexity** - O(n²) → O(n log n) provides exponential gains
2. **Data structure choice** - List → Set for lookups (10,000x faster)
3. **Language features** - Comprehensions, built-ins, generators
4. **Caching** - Memoization for repeated calculations
5. **Compiled extensions** - NumPy, Numba, Cython for hot paths
6. **Parallelism** - Multiprocessing for CPU-bound work

**Key Principle**: Algorithmic improvements beat micro-optimizations every time.

## Quick Reference

Load detailed guides for specific optimization areas:

| Task | Load reference |
| --- | --- |
| Profile code and find bottlenecks | `skills/python-performance-optimization/references/profiling.md` |
| Algorithm and data structure optimization | `skills/python-performance-optimization/references/algorithms.md` |
| Memory optimization and generators | `skills/python-performance-optimization/references/memory.md` |
| String concatenation and file I/O | `skills/python-performance-optimization/references/string-io.md` |
| NumPy, Numba, Cython, multiprocessing | `skills/python-performance-optimization/references/acceleration.md` |

## Optimization Workflow

### Phase 1: Measure
1. **Profile with cProfile** - Identify slow functions
2. **Line profile hot paths** - Find exact slow lines
3. **Memory profile** - Check for memory bottlenecks
4. **Benchmark baseline** - Record current performance

### Phase 2: Analyze
1. **Check algorithm complexity** - Is it O(n²) or worse?
2. **Evaluate data structures** - Are you using lists for lookups?
3. **Identify repeated work** - Can results be cached?
4. **Find I/O bottlenecks** - Database queries, file operations

### Phase 3: Optimize
1. **Improve algorithms first** - Biggest impact
2. **Use appropriate data structures** - Set/dict for O(1) lookups
3. **Apply caching** - `@lru_cache` for expensive functions
4. **Use generators** - For large datasets
5. **Leverage NumPy/Numba** - For numerical code
6. **Parallelize** - Multiprocessing for CPU-bound tasks

### Phase 4: Validate
1. **Re-profile** - Verify improvements
2. **Benchmark** - Measure speedup quantitatively
3. **Test correctness** - Ensure optimizations didn't break functionality
4. **Document** - Explain why optimization was needed

## Common Optimization Patterns

### Pattern 1: Replace List with Set for Lookups
```python
# Slow: O(n) lookup
if item in large_list:  # Bad

# Fast: O(1) lookup
if item in large_set:   # Good
```

### Pattern 2: Use Comprehensions
```python
# Slower
result = []
for i in range(n):
    result.append(i * 2)

# Faster (35% speedup)
result = [i * 2 for i in range(n)]
```

### Pattern 3: Cache Expensive Calculations
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def expensive_function(n):
    # Result cached automatically
    return complex_calculation(n)
```

### Pattern 4: Use Generators for Large Data
```python
# Memory inefficient
def read_file(path):
    return [line for line in open(path)]  # Loads entire file

# Memory efficient
def read_file(path):
    for line in open(path):  # Streams line by line
        yield line.strip()
```

### Pattern 5: Vectorize with NumPy
```python
# Pure Python: ~500ms
result = sum(i**2 for i in range(1000000))

# NumPy: ~5ms (100x faster)
import numpy as np
result = np.sum(np.arange(1000000)**2)
```

## Common Mistakes to Avoid

1. **Optimizing before profiling** - You'll optimize the wrong code
2. **Using lists for membership tests** - Use sets/dicts instead
3. **String concatenation in loops** - Use `"".join()` or `StringIO`
4. **Loading entire files into memory** - Use generators
5. **N+1 database queries** - Use JOINs or batch queries
6. **Ignoring built-in functions** - They're C-optimized and fast
7. **Premature optimization** - Focus on algorithmic improvements first
8. **Not benchmarking** - Always measure improvements quantitatively

## Decision Tree

**Start here**: Profile with cProfile to find bottlenecks

**Hot path is algorithm?**
- Yes → Check complexity, improve algorithm, use better data structures
- No → Continue

**Hot path is computation?**
- Numerical loops → NumPy or Numba
- CPU-bound → Multiprocessing
- Already fast enough → Done

**Hot path is memory?**
- Large data → Generators, streaming
- Many objects → `__slots__`, object pooling
- Caching needed → `@lru_cache` or custom cache

**Hot path is I/O?**
- Database → Batch queries, indexes, connection pooling
- Files → Buffering, streaming
- Network → Async I/O, request batching

## Best Practices

1. **Profile before optimizing** - Measure to find real bottlenecks
2. **Optimize algorithms first** - O(n²) → O(n) beats micro-optimizations
3. **Use appropriate data structures** - Set/dict for lookups, not lists
4. **Leverage built-ins** - C-implemented built-ins are faster than pure Python
5. **Avoid premature optimization** - Optimize hot paths identified by profiling
6. **Use generators for large data** - Reduce memory usage with lazy evaluation
7. **Batch operations** - Minimize overhead from syscalls and network requests
8. **Cache expensive computations** - Use `@lru_cache` or custom caching
9. **Consider NumPy/Numba** - Vectorization and JIT for numerical code
10. **Parallelize CPU-bound work** - Use multiprocessing to utilize all cores

## Resources

- **Python Performance**: https://wiki.python.org/moin/PythonSpeed
- **cProfile**: https://docs.python.org/3/library/profile.html
- **NumPy**: https://numpy.org/doc/stable/user/absolute_beginners.html
- **Numba**: https://numba.pydata.org/
- **Cython**: https://cython.readthedocs.io/
- **High Performance Python** (Book by Gorelick & Ozsvald)
