---
name: python
description: Python 3.11+ performance optimization guidelines (formerly python-311). This skill should be used when writing, reviewing, or refactoring Python code to ensure optimal performance patterns. Triggers on tasks involving asyncio, data structures, memory management, concurrency, loops, strings, or Python idioms.
---

# Python 3.11 Best Practices

Comprehensive performance optimization guide for Python 3.11+ applications. Contains 42 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new Python async I/O code
- Choosing data structures for collections
- Optimizing memory usage in data-intensive applications
- Implementing concurrent or parallel processing
- Reviewing Python code for performance issues

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | I/O & Async Patterns | CRITICAL | `io-` |
| 2 | Data Structure Selection | CRITICAL | `ds-` |
| 3 | Memory Optimization | HIGH | `mem-` |
| 4 | Concurrency & Parallelism | HIGH | `conc-` |
| 5 | Loop & Iteration | MEDIUM | `loop-` |
| 6 | String Operations | MEDIUM | `str-` |
| 7 | Function & Call Overhead | LOW-MEDIUM | `func-` |
| 8 | Python Idioms & Micro | LOW | `py-` |

## Table of Contents

1. [I/O & Async Patterns](references/_sections.md#1-io--async-patterns) — **CRITICAL**
   - 1.1 [Defer await Until Value Needed](references/io-defer-await.md) — CRITICAL (2-5× faster for dependent operations)
   - 1.2 [Use aiofiles for Async File Operations](references/io-aiofiles.md) — CRITICAL (prevents event loop blocking)
   - 1.3 [Use asyncio.gather() for Concurrent I/O](references/io-async-gather.md) — CRITICAL (2-10× throughput improvement)
   - 1.4 [Use Connection Pooling for Database Access](references/io-connection-pooling.md) — CRITICAL (100-200ms saved per connection)
   - 1.5 [Use Semaphores to Limit Concurrent Operations](references/io-semaphore.md) — CRITICAL (prevents resource exhaustion)
   - 1.6 [Use uvloop for Faster Event Loop](references/io-uvloop.md) — CRITICAL (2-4× faster async I/O)

2. [Data Structure Selection](references/_sections.md#2-data-structure-selection) — **CRITICAL**
   - 2.1 [Use bisect for O(log n) Sorted List Operations](references/ds-bisect-sorted.md) — CRITICAL (O(n) to O(log n) search)
   - 2.2 [Use defaultdict to Avoid Key Existence Checks](references/ds-defaultdict.md) — CRITICAL (eliminates redundant lookups)
   - 2.3 [Use deque for O(1) Queue Operations](references/ds-deque-for-queue.md) — CRITICAL (O(n) to O(1) for popleft)
   - 2.4 [Use Dict for O(1) Key-Value Lookup](references/ds-dict-for-lookup.md) — CRITICAL (O(n) to O(1) lookup)
   - 2.5 [Use frozenset for Hashable Set Keys](references/ds-frozenset-for-hashable.md) — CRITICAL (enables set-of-sets patterns)
   - 2.6 [Use Set for O(1) Membership Testing](references/ds-set-for-membership.md) — CRITICAL (O(n) to O(1) lookup)

3. [Memory Optimization](references/_sections.md#3-memory-optimization) — **HIGH**
   - 3.1 [Intern Repeated Strings to Save Memory](references/mem-intern-strings.md) — HIGH (reduces duplicate string storage)
   - 3.2 [Use __slots__ for Memory-Efficient Classes](references/mem-slots.md) — HIGH (20-50% memory reduction per instance)
   - 3.3 [Use array.array for Homogeneous Numeric Data](references/mem-array-for-numeric.md) — HIGH (4-8× memory reduction for numbers)
   - 3.4 [Use Generators for Large Sequences](references/mem-generators.md) — HIGH (100-1000× memory reduction)
   - 3.5 [Use weakref for Caches to Prevent Memory Leaks](references/mem-weak-references.md) — HIGH (prevents unbounded cache growth)

4. [Concurrency & Parallelism](references/_sections.md#4-concurrency--parallelism) — **HIGH**
   - 4.1 [Use asyncio for I/O-Bound Concurrency](references/conc-asyncio-for-io.md) — HIGH (300% throughput improvement for I/O)
   - 4.2 [Use multiprocessing for CPU-Bound Parallelism](references/conc-multiprocessing-cpu.md) — HIGH (4-8× speedup on multi-core systems)
   - 4.3 [Use Queue for Thread-Safe Communication](references/conc-queue-communication.md) — HIGH (prevents race conditions)
   - 4.4 [Use TaskGroup for Structured Concurrency](references/conc-taskgroup.md) — HIGH (prevents resource leaks on failure)
   - 4.5 [Use ThreadPoolExecutor for Blocking Calls in Async](references/conc-threadpool-blocking.md) — HIGH (prevents event loop blocking)

5. [Loop & Iteration](references/_sections.md#5-loop--iteration) — **MEDIUM**
   - 5.1 [Hoist Loop-Invariant Computations](references/loop-hoist-invariants.md) — MEDIUM (avoids N× redundant work)
   - 5.2 [Use any() and all() for Boolean Aggregation](references/loop-any-all.md) — MEDIUM (O(n) to O(1) best case)
   - 5.3 [Use dict.items() for Key-Value Iteration](references/loop-dict-items.md) — MEDIUM (single lookup vs double lookup)
   - 5.4 [Use enumerate() for Index-Value Iteration](references/loop-enumerate.md) — MEDIUM (cleaner code, avoids index errors)
   - 5.5 [Use itertools for Efficient Iteration Patterns](references/loop-itertools.md) — MEDIUM (2-3× faster iteration patterns)
   - 5.6 [Use List Comprehensions Over Explicit Loops](references/loop-comprehension.md) — MEDIUM (2-3× faster iteration)

6. [String Operations](references/_sections.md#6-string-operations) — **MEDIUM**
   - 6.1 [Use f-strings for Simple String Formatting](references/str-fstring.md) — MEDIUM (20-30% faster than .format())
   - 6.2 [Use join() for Multiple String Concatenation](references/str-join-concatenation.md) — MEDIUM (4× faster for 5+ strings)
   - 6.3 [Use str.startswith() with Tuple for Multiple Prefixes](references/str-startswith-tuple.md) — MEDIUM (single call vs multiple comparisons)
   - 6.4 [Use str.translate() for Character-Level Replacements](references/str-translate.md) — MEDIUM (10× faster than chained replace())

7. [Function & Call Overhead](references/_sections.md#7-function--call-overhead) — **LOW-MEDIUM**
   - 7.1 [Reduce Function Calls in Tight Loops](references/func-reduce-calls.md) — LOW-MEDIUM (100ms savings per 1M iterations)
   - 7.2 [Use functools.partial for Pre-Filled Arguments](references/func-partial.md) — LOW-MEDIUM (50% faster debugging via introspection)
   - 7.3 [Use Keyword-Only Arguments for API Clarity](references/func-keyword-only.md) — LOW-MEDIUM (prevents positional argument errors)
   - 7.4 [Use lru_cache for Expensive Function Memoization](references/func-lru-cache.md) — LOW-MEDIUM (avoids repeated computation)

8. [Python Idioms & Micro](references/_sections.md#8-python-idioms--micro) — **LOW**
   - 8.1 [Leverage Zero-Cost Exception Handling](references/py-zero-cost-exceptions.md) — LOW (zero overhead in happy path (Python 3.11+))
   - 8.2 [Prefer Local Variables Over Global Lookups](references/py-local-variables.md) — LOW (faster name resolution)
   - 8.3 [Use dataclass for Data-Holding Classes](references/py-dataclass.md) — LOW (reduces boilerplate by 80%)
   - 8.4 [Use Lazy Imports for Faster Startup](references/py-lazy-import.md) — LOW (10-15% faster startup)
   - 8.5 [Use match Statement for Structural Pattern Matching](references/py-match-statement.md) — LOW (reduces branch complexity)
   - 8.6 [Use Walrus Operator for Assignment in Expressions](references/py-walrus-operator.md) — LOW (eliminates redundant computations)

## References

1. [Python 3.11 Release Notes](https://docs.python.org/3/whatsnew/3.11.html)
2. [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
3. [Python Wiki - Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)
4. [Real Python - Async IO](https://realpython.com/async-io-python/)
5. [Real Python - LEGB Rule](https://realpython.com/python-scope-legb-rule/)
6. [Real Python - String Concatenation](https://realpython.com/python-string-concatenation/)
7. [Python Tutorial - Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
8. [CPython Exception Handling](https://github.com/python/cpython/blob/main/InternalDocs/exception_handling.md)
9. [DataCamp - Python Generators](https://www.datacamp.com/tutorial/python-generators)
10. [JetBrains - Performance Hacks](https://blog.jetbrains.com/pycharm/2025/11/10-smart-performance-hacks-for-faster-python-code/)
