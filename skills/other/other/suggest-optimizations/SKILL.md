---
name: suggest-optimizations
description: "Identify performance optimization opportunities. Use when improving code efficiency."
mcp_fallback: none
category: analysis
tier: 2
user-invocable: false
---

# Suggest Optimizations

Analyze code and profile data to recommend optimization strategies for improving performance and resource usage.

## When to Use

- Performance-critical code paths identified in profiling
- Reducing execution time for hot functions
- Lowering memory usage
- Planning SIMD or vectorization strategies

## Quick Reference

```bash
# Identify optimization opportunities
# 1. Profile to find bottlenecks
# 2. Analyze algorithmic complexity
# 3. Check for unnecessary operations
# 4. Evaluate data structure choices
# 5. Consider SIMD/vectorization

# Profile Python code
python3 -m cProfile -s cumulative script.py | head -20
```

## Workflow

1. **Profile critical paths**: Identify functions consuming most time/memory
2. **Analyze algorithms**: Check time/space complexity, look for inefficiencies
3. **Examine data structures**: Verify optimal data structure choices
4. **Consider caching**: Identify repeated computations
5. **Propose optimizations**: List specific changes with expected impact

## Output Format

Optimization recommendation:

- Bottleneck identified (function, line number)
- Current performance (time/memory)
- Root cause analysis
- Recommended optimization technique
- Expected improvement (percentage or time estimate)
- Implementation difficulty (low/medium/high)

## References

- See `benchmark-functions` skill for measuring improvements
- See `profile-code` skill for detailed profiling
- See CLAUDE.md > Mojo for SIMD optimization patterns
