---
name: profile-code
description: "Measure execution time and memory usage of code. Use when analyzing performance characteristics."
mcp_fallback: none
category: analysis
tier: 2
user-invocable: false
---

# Profile Code

Use profiling tools to measure CPU time, memory allocation, and identify performance bottlenecks in code.

## When to Use

- Finding performance bottlenecks
- Measuring CPU vs memory tradeoffs
- Understanding where code spends most time
- Optimizing hot code paths

## Quick Reference

```bash
# Python CPU profiling with cProfile
python3 -m cProfile -s cumulative script.py | head -30

# Memory profiling
pip install memory-profiler
python3 -m memory_profiler script.py

# Detailed call graph
pip install graphviz
python3 -m pstats /tmp/profile.prof
```

## Workflow

1. **Select profiler**: Choose appropriate tool (cProfile for CPU, memory_profiler for memory)
2. **Run with instrumentation**: Execute code with profiling enabled
3. **Capture metrics**: Record timing and memory data
4. **Analyze output**: Identify top time consumers and memory hogs
5. **Report findings**: Document bottlenecks with before/after context

## Output Format

Profiling report:

- Top functions by execution time
- Call count for each function
- Memory allocation per function
- Call graph/call tree
- Percentage of total time/memory per function
- Recommendations for optimization

## References

- See `suggest-optimizations` skill for improvement recommendations
- See `benchmark-functions` skill for measuring improvements
- See CLAUDE.md > Performance for optimization guidelines
