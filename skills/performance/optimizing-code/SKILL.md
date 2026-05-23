---
name: optimizing-code
description: Improve code performance without changing behavior. Use when code fails latency/throughput requirements. Covers profiling, caching, and algorithmic optimization.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Optimizing Code

## The Optimization Hat

When optimizing, you improve **performance** without changing **behavior**. Always measure before and after.

## Golden Rules

1. **Measure First**: Never optimize without a benchmark
2. **Profile Before Guessing**: Find the actual bottleneck
3. **Optimize the Right Thing**: Focus on the critical path
4. **Measure After**: Verify the optimization worked

## Workflows

- [ ] **Benchmark**: Establish baseline performance metrics
- [ ] **Profile**: Identify the actual bottleneck
- [ ] **Hypothesize**: What optimization will help?
- [ ] **Implement**: Make the change
- [ ] **Measure**: Verify improvement
- [ ] **Document**: Record the optimization and results

## Common Optimizations

### Algorithm Complexity
- Replace O(n²) with O(n log n) or O(n)
- Use appropriate data structures (Set for lookups, Map for key-value)

### Caching
```typescript
// Memoization
const cache = new Map<string, Result>();

function expensiveCalculation(input: string): Result {
  if (cache.has(input)) {
    return cache.get(input)!;
  }
  const result = /* expensive work */;
  cache.set(input, result);
  return result;
}
```

### Database Queries
- Add indexes for frequently queried columns
- Avoid N+1 queries (use eager loading)
- Use pagination for large result sets

### Memory
- Avoid creating unnecessary objects in loops
- Use streaming for large files
- Release references when done

## Profiling Tools

```bash
# Node.js
node --prof app.js
node --prof-process isolate-*.log

# Python
python -m cProfile -s cumtime script.py

# Go
go test -bench=. -cpuprofile=cpu.prof
go tool pprof cpu.prof
```

## Anti-Patterns to Avoid

- Premature optimization (no benchmark)
- Micro-optimizations (negligible impact)
- Optimizing cold paths
- Sacrificing readability for minor gains
