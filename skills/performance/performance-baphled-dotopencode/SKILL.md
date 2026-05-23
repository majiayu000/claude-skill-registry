---
name: performance
description: Go performance optimisation, profiling, and writing efficient code
category: Performance Profiling
---

# Skill: performance

## What I do

I teach Go performance: measure first with benchmarks and pprof, identify bottlenecks with data, then optimise allocations, concurrency, and algorithms. Never optimise without profiling evidence.

## When to use me

- Investigating slow endpoints or high memory usage
- Writing benchmarks to measure before/after performance
- Profiling CPU, memory, or goroutine contention with pprof
- Reducing allocations in hot paths
- Choosing between performance trade-offs (memory vs CPU, latency vs throughput)

## Core principles

1. **Measure first** — Never optimise without benchmark data; intuition is usually wrong
2. **Profile, don't guess** — Use pprof to find the actual bottleneck, not the suspected one
3. **Allocations dominate** — In Go, reducing allocations often gives the biggest wins
4. **Benchmark before and after** — Every optimisation must show measurable improvement
5. **Readability over micro-optimisation** — Only sacrifice clarity for proven, significant gains

## Patterns & examples

**Writing benchmarks:**
```go
func BenchmarkProcess(b *testing.B) {
    data := setupTestData()
    b.ResetTimer() // exclude setup from measurement

    for i := 0; i < b.N; i++ {
        process(data)
    }
}

// Run: go test -bench=BenchmarkProcess -benchmem -count=5
// Output: BenchmarkProcess-8  50000  23456 ns/op  1024 B/op  12 allocs/op
```

**Profiling with pprof:**
```bash
# CPU profile
go test -cpuprofile=cpu.prof -bench=.
go tool pprof -http=:8080 cpu.prof

# Memory profile
go test -memprofile=mem.prof -bench=.
go tool pprof -http=:8080 mem.prof

# In running server (import _ "net/http/pprof")
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
```

**Allocation reduction techniques:**
```go
// ❌ Allocates new slice every call
func collect(items []Item) []string {
    var names []string
    for _, item := range items {
        names = append(names, item.Name)
    }
    return names
}

// ✅ Pre-allocate with known capacity
func collect(items []Item) []string {
    names := make([]string, 0, len(items))
    for _, item := range items {
        names = append(names, item.Name)
    }
    return names
}

// ✅ Reuse buffers with sync.Pool
var bufPool = sync.Pool{
    New: func() any { return new(bytes.Buffer) },
}

func process(data []byte) string {
    buf := bufPool.Get().(*bytes.Buffer)
    defer bufPool.Put(buf)
    buf.Reset()
    buf.Write(data)
    return buf.String()
}
```

**String building:**
```go
// ❌ O(n²) — allocates new string each iteration
result := ""
for _, s := range items {
    result += s
}

// ✅ O(n) — single allocation
var b strings.Builder
b.Grow(estimatedSize) // optional pre-allocation
for _, s := range items {
    b.WriteString(s)
}
result := b.String()
```

**Common bottleneck locations:**

| Symptom | Likely cause | Tool |
|---------|-------------|------|
| High CPU | Hot loop, excessive computation | `go tool pprof` CPU profile |
| High memory | Allocation churn, large caches | `go tool pprof` heap profile |
| High latency | Blocking I/O, lock contention | `go tool trace` |
| Goroutine growth | Leaks, unbounded spawning | `pprof/goroutine` |

## Anti-patterns to avoid

- ❌ **Premature optimisation** — Optimising code without profiling data; wastes time, hurts readability
- ❌ **Micro-benchmarks in isolation** — Benchmarking a function that's called once; focus on hot paths
- ❌ **Ignoring `benchmem`** — CPU speed matters less than allocation count in GC-heavy workloads
- ❌ **`sync.Pool` everywhere** — Only helps for frequently allocated, short-lived objects; adds complexity
- ❌ **Caching without eviction** — Unbounded caches leak memory; always set a size limit or TTL


## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Performance-Profiling/Performance.md`

## Related skills

- `benchmarking` - Detailed benchmark methodology and comparison
- `profiling` - Deep-dive into pprof, trace, and flame graphs
- `concurrency` - Goroutine scheduling and contention profiling
- `golang` - Idiomatic Go patterns that are inherently efficient
