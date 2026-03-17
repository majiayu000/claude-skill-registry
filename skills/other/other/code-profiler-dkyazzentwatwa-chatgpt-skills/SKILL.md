---
name: code-profiler
description: Use when asked to profile Python code performance, identify bottlenecks, measure execution time, or analyze function call statistics.
---

# Code Profiler

Analyze Python code performance, identify bottlenecks, and optimize execution with comprehensive profiling tools.

## Purpose

Performance analysis for:
- Bottleneck identification
- Function execution time measurement
- Memory usage profiling
- Call graph visualization
- Optimization validation

## Features

- **Time Profiling**: Measure function execution times
- **Line-by-Line Analysis**: Profile each line of code
- **Call Statistics**: Function call counts and cumulative time
- **Memory Profiling**: Track memory allocation and usage
- **Flamegraph Visualization**: Visual call stack analysis
- **Comparison**: Before/after optimization comparison

## Quick Start

```python
from code_profiler import CodeProfiler

# Profile function
profiler = CodeProfiler()
profiler.profile_function(my_function, args=(arg1, arg2))
profiler.print_stats(top=10)

# Profile script
profiler.profile_script('script.py')
profiler.export_report('profile_report.html')
```

## CLI Usage

```bash
# Profile Python script
python code_profiler.py script.py

# Profile with line-by-line analysis
python code_profiler.py script.py --line-by-line

# Export HTML report
python code_profiler.py script.py --output report.html
```
