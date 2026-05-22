---
name: benchmark-functions
description: "Measure function performance and compare implementations. Use when optimizing critical code paths."
mcp_fallback: none
category: analysis
tier: 2
user-invocable: false
---

# Benchmark Functions

Systematically measure function execution time, memory usage, and performance characteristics to identify optimization opportunities.

## When to Use

- Comparing different algorithm implementations
- Measuring performance before/after optimization
- Profiling SIMD vs scalar implementations
- Establishing performance baselines for CI/CD

## Quick Reference

```bash
# Python benchmarking with timeit
python3 -m timeit -s 'import module' 'module.function(args)' -n 1000 -r 5

# Mojo benchmarking with built-in timing
mojo run benchmark_script.mojo
```

## Workflow

1. **Set up benchmarks**: Create timing harness with warm-up iterations
2. **Run measurements**: Execute function multiple times, record timing
3. **Collect statistics**: Calculate mean, median, std deviation
4. **Compare baselines**: Compare against previous implementations
5. **Identify bottlenecks**: Pinpoint functions needing optimization

## Output Format

Benchmark report:

- Function name and parameters tested
- Execution time statistics (mean, median, min, max)
- Memory usage (if applicable)
- Comparison to baseline (improvement percentage)
- Iterations and sample size used

## References

- See `profile-code` skill for detailed performance profiling
- See `suggest-optimizations` skill for improvement strategies
- See CLAUDE.md > Performance for Mojo optimization guidelines
