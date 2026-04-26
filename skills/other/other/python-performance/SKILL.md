---
name: python-performance
description: 'Python performance profiling and optimization: bottleneck detection, memory tuning, benchmarking'
version: 1.9.0
globs: "**/*.py"
alwaysApply: false
category: performance
tags:
- python
- performance
- profiling
- optimization
- cProfile
- memory
tools:
- profiler-runner
- memory-analyzer
- benchmark-suite
usage_patterns:
- performance-analysis
- bottleneck-identification
- memory-optimization
- algorithm-optimization
complexity: intermediate
model_hint: standard
estimated_tokens: 1200
progressive_loading: true
modules:
- profiling-tools
- optimization-patterns
- memory-management
- benchmarking-tools
- best-practices
---
# Python Performance Optimization

Profiling and optimization patterns for Python code.

## Table of Contents

1. [Quick Start](#quick-start)

## Quick Start

```python
# Basic timing
import timeit
time = timeit.timeit("sum(range(1000000))", number=100)
print(f"Average: {time/100:.6f}s")
```
**Verification:** Run the command with `--help` flag to verify availability.

## When To Use

- Identifying performance bottlenecks
- Reducing application latency
- Optimizing CPU-intensive operations
- Reducing memory consumption
- Profiling production applications
- Improving database query performance

## When NOT To Use

- Async concurrency - use python-async
  instead
- CPU/GPU system monitoring - use conservation:cpu-gpu-performance
- Async concurrency - use python-async
  instead
- CPU/GPU system monitoring - use conservation:cpu-gpu-performance

## Modules

This skill is organized into focused modules for progressive loading:

### [profiling-tools](modules/profiling-tools.md)
CPU profiling with cProfile, line profiling, memory profiling, and production profiling with py-spy. Essential for identifying where your code spends time and memory.

### [optimization-patterns](modules/optimization-patterns.md)
Ten proven optimization patterns including list comprehensions, generators, caching, string concatenation, data structures, NumPy, multiprocessing, and database operations.

### [memory-management](modules/memory-management.md)
Memory optimization techniques including leak tracking with tracemalloc and weak references for caches. Depends on profiling-tools.

### [benchmarking-tools](modules/benchmarking-tools.md)
Benchmarking tools including custom decorators and pytest-benchmark for verifying performance improvements.

### [best-practices](modules/best-practices.md)
Best practices, common pitfalls, and exit criteria for performance optimization work. Synthesizes guidance from profiling-tools and optimization-patterns.

## Exit Criteria

- Profiled code to identify bottlenecks
- Applied appropriate optimization patterns
- Verified improvements with benchmarks
- Memory usage acceptable
- No performance regressions
