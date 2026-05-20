---
name: performance-profiling
description: "Use when profiling CPU, memory, network performance for web apps and APIs. Covers flame graphs, language-specific profilers, benchmarking workflows, and performance regression detection."
---

# Performance Profiling

## The Rule

```
MEASURE FIRST. OPTIMIZE SECOND. MEASURE AGAIN.
```

Never optimize based on intuition. Profile, identify the bottleneck, fix it, verify the fix with numbers.

## Profiling Decision Table

| Symptom | Tool Category | What to Look For |
|---------|---------------|------------------|
| Slow response times | CPU profiler / flame graph | Hot functions, deep call stacks |
| High memory usage | Heap profiler / snapshots | Leaked objects, growing allocations |
| Memory keeps growing | Allocation tracker + GC logs | Unreleased references, finalizer queues |
| Slow page load | Network waterfall + Lighthouse | Large bundles, render-blocking resources |
| High latency variance | Distributed tracing | Slow downstream calls, queue backpressure |
| Event loop lag (Node) | Clinic.js / blocked-at | Sync I/O, CPU-heavy computation on main thread |

## Language-Specific Profilers

### Python

```bash
# CPU sampling (low overhead, attach to running process)
py-spy top --pid $PID
py-spy record -o profile.svg -- python app.py

# Deterministic profiling (higher overhead)
python -m cProfile -o stats.prof app.py
# Analyze:
import pstats
p = pstats.Stats('stats.prof')
p.sort_stats('cumulative').print_stats(20)

# Memory profiling
pip install memory_profiler
python -m memory_profiler script.py     # Line-by-line
mprof run script.py && mprof plot       # Over time

# Memory leak detection
import tracemalloc
tracemalloc.start()
# ... run code ...
snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics('lineno')[:10]:
    print(stat)
```

| Tool | Overhead | Use Case |
|------|----------|----------|
| py-spy | Low (~5%) | Production sampling, flame graphs |
| cProfile | Medium | Deterministic call counts, dev profiling |
| memory_profiler | High | Line-by-line memory attribution |
| tracemalloc | Medium | Leak detection, allocation tracing |
| scalene | Low-Med | CPU + memory + GPU combined |

### JavaScript / TypeScript

```bash
# Node.js built-in profiler
node --prof app.js
node --prof-process isolate-*.log > processed.txt

# Chrome DevTools (attach to running Node)
node --inspect app.js
# Open chrome://inspect -> Performance tab -> Record

# Clinic.js suite
npx clinic doctor -- node app.js        # Overview
npx clinic flame -- node app.js         # Flame graph
npx clinic bubbleprof -- node app.js    # Async bottlenecks

# 0x flame graphs
npx 0x app.js
```

**Browser profiling:**
- Performance tab -> Record -> Interact -> Stop -> Analyze flame chart
- Memory tab -> Heap snapshot -> Compare snapshots for leaks
- Lighthouse -> Performance audit (LCP, FID, CLS metrics)

### Go

```go
import (
    "net/http"
    _ "net/http/pprof"  // Register pprof handlers
)

func main() {
    go func() { http.ListenAndServe(":6060", nil) }()
    // ...
}
```

```bash
# CPU profile (30s default)
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
# In pprof: top, list funcName, web (SVG)

# Heap profile
go tool pprof http://localhost:6060/debug/pprof/heap

# Goroutine analysis
go tool pprof http://localhost:6060/debug/pprof/goroutine

# Execution tracer (scheduler, GC, goroutine events)
curl -o trace.out http://localhost:6060/debug/pprof/trace?seconds=5
go tool trace trace.out

# Benchmarks with profiling
go test -bench=. -cpuprofile=cpu.prof -memprofile=mem.prof
go tool pprof cpu.prof
```

### Rust

```bash
# Flame graphs via cargo-flamegraph
cargo install flamegraph
cargo flamegraph --bin myapp

# Criterion benchmarks (statistical)
# In Cargo.toml: [dev-dependencies] criterion = { version = "0.5", features = ["html_reports"] }
cargo bench

# Memory profiling with DHAT
cargo install dhat
# Annotate code with dhat::Alloc as global allocator

# Valgrind/Cachegrind (Linux)
valgrind --tool=callgrind target/release/myapp
```

## Flame Graph Interpretation

```
Reading flame graphs:
- X-axis = population of samples (NOT time sequence)
- Y-axis = stack depth (bottom = entry point, top = leaf)
- Width = proportion of total samples (wider = more CPU time)

What to look for:
1. PLATEAUS at the top -- functions that are themselves slow (no children consuming time)
2. WIDE towers -- deep call stacks that dominate CPU
3. Unexpected functions -- framework/library code you didn't expect to be hot

Action:
- Wide plateau at top → optimize that function directly
- Wide tower → consider algorithmic change or caching at a higher level
- Many narrow towers → death by a thousand cuts; consider batching
```

## Memory Profiling Patterns

### Heap Snapshot Comparison (Leak Detection)

1. Take baseline snapshot after warmup
2. Run suspected leaking operation N times
3. Take second snapshot
4. Diff: objects present in snapshot 2 but not 1 = likely leaks

### Common Leak Patterns

| Pattern | Language | Fix |
|---------|----------|-----|
| Event listener not removed | JS/TS | `removeEventListener` or `AbortController` |
| Closures capturing large scope | JS/TS/Python | Narrow closure scope, use `WeakRef` |
| Global caches without eviction | All | LRU cache with max size |
| Circular references + `__del__` | Python | `weakref`, avoid `__del__` |
| Goroutine leak (blocked channel) | Go | Context cancellation, buffered channels |
| Unbounded Vec/HashMap growth | Rust | `.shrink_to_fit()`, bounded collections |

## Benchmarking Methodology

### The Protocol

1. **Warmup**: Discard first N iterations (JIT, caches, OS scheduling)
2. **Statistical significance**: Run enough iterations for stable results (>30 samples)
3. **Isolation**: Close other apps, pin CPU frequency if possible, use dedicated CI runners
4. **Baseline**: Always compare against a known baseline, not "gut feel"
5. **Report**: Median + p95 + p99 (not just mean -- outliers matter)

### Micro-benchmark Pitfalls

| Pitfall | Problem | Mitigation |
|---------|---------|------------|
| Dead code elimination | Compiler optimizes away your benchmark | Use `std::hint::black_box` (Rust), `benchmark.DoNotOptimize` (C++), consume results |
| Constant folding | Inputs known at compile time | Use runtime-varying inputs |
| Cold cache vs warm cache | Results vary 10-100x | Explicitly warmup OR explicitly flush caches |
| GC pauses | Spikes in latency | Report percentiles, force GC between runs |
| Insufficient samples | High variance | Run until coefficient of variation < 5% |

### Framework-Specific Benchmarks

```python
# Python: pytest-benchmark
def test_sort_performance(benchmark):
    data = list(range(10000))
    random.shuffle(data)
    benchmark(sorted, data)
```

```javascript
// Node.js: tinybench
import { Bench } from 'tinybench';
const bench = new Bench({ time: 1000 });
bench.add('sort', () => { arr.sort(); });
await bench.run();
console.table(bench.table());
```

```go
// Go: built-in
func BenchmarkSort(b *testing.B) {
    for i := 0; i < b.N; i++ {
        sort.Ints(data)
    }
}
```

## CI Integration for Regression Detection

### GitHub Actions Example

```yaml
- name: Run benchmarks
  run: |
    cargo bench -- --save-baseline current

- name: Compare with main
  run: |
    git stash
    git checkout main
    cargo bench -- --save-baseline main
    git checkout -
    git stash pop
    critcmp main current --threshold 10
```

### Regression Detection Strategy

| Approach | Pros | Cons |
|----------|------|------|
| Compare against fixed baseline | Deterministic, simple | Baseline drifts, needs periodic updates |
| Compare against main branch | Always up-to-date | CI variance can cause false positives |
| Statistical comparison (criterion) | Handles variance properly | Slower (needs many samples) |
| Performance budgets (Lighthouse CI) | Clear pass/fail | Frontend-specific |

**Recommended**: Compare against main with a tolerance threshold (5-10%) to absorb CI noise.

## Common Performance Anti-Patterns

### Python
- String concatenation in loops (use `"".join()`)
- Global imports of heavy modules at module level (lazy import for CLI tools)
- `pandas.apply()` row-by-row (vectorize or use `numpy`)
- Synchronous I/O in async context

### JavaScript / TypeScript
- Re-renders from unstable references (`useMemo`, `useCallback`)
- Synchronous `JSON.parse` on large payloads (streaming parser)
- Unbatched DOM mutations (use `DocumentFragment` or framework batching)
- `Array.find()` in hot loops (use `Map`/`Set` for lookups)

### Go
- Excessive small allocations in hot path (pre-allocate slices, sync.Pool)
- String concatenation in loops (use `strings.Builder`)
- Unbuffered channels as queues (buffer appropriately)
- Reflection in hot paths (`reflect` is slow -- generate code instead)

### Rust
- Unnecessary cloning (borrow instead)
- `Vec` reallocation (pre-allocate with `Vec::with_capacity`)
- Box<dyn Trait> in hot path (monomorphize with generics)
- Debug build benchmarks (always `--release`)

## Gotchas

- Production profiling overhead varies wildly: sampling profilers (py-spy, pprof) ~5%, deterministic profilers (cProfile) ~50-200%
- Flame graphs from short runs are noisy; collect at least 10-30 seconds of samples
- Memory profiler overhead can change GC behavior and hide/create leaks
- CI benchmark machines have noisy neighbors; use dedicated runners or statistical comparison
- Browser DevTools Performance recordings include DevTools overhead itself
- Go's `pprof` heap profile shows live objects by default; use `-alloc_space` for total allocations
- Rust benchmarks MUST use `--release`; debug builds are 10-100x slower and profiling them is meaningless

## Cross-References

- **testing:load-testing-and-perf** -- load testing tools, capacity planning, SLA validation
- **testing:debugging-methodology** -- systematic debugging when profiling reveals unexpected behavior
