---
name: benchmarking
description: Go benchmarking for measuring and optimising code performance
category: Performance Profiling
---

# Skill: benchmarking

## What I do

I provide Go-specific benchmarking expertise to measure and optimise code performance. I focus on writing reliable benchmarks using the `testing` package and analysing results to identify bottlenecks.

## When to use me

- When comparing the performance of multiple implementations
- When verifying the impact of an optimisation
- When identifying hotspots in performance-critical code paths

## Core principles

1. **Isolation**: Run benchmarks in a stable environment to minimise noise.
2. **Reliability**: Use `b.ResetTimer()` to exclude setup overhead and `b.ReportAllocs()` to track memory allocations.
3. **Statistical significance**: Use tools like `benchstat` to compare results across multiple runs.
4. **Realistic data**: Use representative input sizes to avoid misleading results from small or trivial datasets.

## Patterns & examples

**Standard benchmark function:**
```go
func BenchmarkProcessData(b *testing.B) {
    data := setupTestData()
    b.ResetTimer()
    b.ReportAllocs()

    for i := 0; i < b.N; i++ {
        ProcessData(data)
    }
}
```

**Table-driven benchmark:**
```go
func BenchmarkAlgorithm(b *testing.B) {
    benchmarks := []struct {
        name string
        size int
    }{
        {"Small", 10},
        {"Medium", 100},
        {"Large", 1000},
    }
    for _, bm := range benchmarks {
        b.Run(bm.name, func(b *testing.B) {
            data := generateData(bm.size)
            b.ResetTimer()
            for i := 0; i < b.N; i++ {
                Algorithm(data)
            }
        })
    }
}
```

**Comparing results:**
Use `go test -bench . -count 5 > old.txt` and `go test -bench . -count 5 > new.txt`, then run `benchstat old.txt new.txt` to see the percentage change.

## Anti-patterns to avoid

- ❌ **Looping manually**: Always use `b.N` for the loop count. Hardcoding iterations leads to unreliable timing.
- ❌ **Compiler optimisations**: Ensure the result of the function under test is used (e.g., assigned to a package-level variable) to prevent the compiler from eliding the call.
- ❌ **Ignoring allocations**: High memory allocation counts often indicate performance issues that timing alone might miss.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Performance-Profiling/Benchmarking.md`

## Related skills

- `profiling`: For deep dives into where time or memory is spent
- `performance`: General optimisation principles and techniques
- `golang`: For idiomatic Go patterns and standard library usage
