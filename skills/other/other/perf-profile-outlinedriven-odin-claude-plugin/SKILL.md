---
name: perf-profile
description: Hotspot detection and performance root-cause analysis — flamegraph interpretation, allocation tracking, latency profiling, regression measurement. Use when a workload misses its latency, throughput, or memory budget; when a benchmark regresses; or before optimizing any hot path (no optimization without a profile).
---

Performance is a contract with reality. Intuition about hot paths is wrong more often than right. Capture, locate, hypothesize, optimize, re-measure, prove the regression with a benchmark — then defend the win with an invariant.

## When to Apply / NOT

Apply: latency or throughput SLO violation; memory pressure (RSS growth, GC churn); benchmark regression; pre-optimization scoping; cold-start vs steady-state cost split; cache locality / branch-prediction concerns.

NOT apply: defect with wrong outputs; architectural redesign; micro-optimization without budget pressure; untested code (write tests first).

## Anti-patterns

- **Optimize without profile**: intuition-driven changes.
- **Single-run benchmarks**: variance dominates. Use `hyperfine --warmup 3 --min-runs 10`.
- **Profile in debug build**: optimizer-disabled binaries lie.
- **Confuse flat profile with call-graph**: self-time vs total-time tell different stories.
- **Ignoring tail latency**: p50 stays flat while p99 explodes.
- **Cherry-picking the win**: re-measure end-to-end.
- **Allocation blind spot**: CPU profiler hides GC.
- **Forgetting the regression guard**.

## Workflow (language-neutral)

1. **Define budget** — restate target metric: latency p95 < X ms, throughput > Y rps, RSS < Z MB.
2. **Establish baseline** — run unoptimized workload under `hyperfine` plus profiler. Save raw artifacts.
3. **Capture profile** — sampled CPU profile → flamegraph; allocation profile if memory-bound; latency histogram for tail.
4. **Locate hotspot** — top self-time function or widest plateau. Cross-check with allocation profile.
5. **Hypothesize** — one falsifiable claim with predicted delta.
6. **Optimize minimally** — smallest change targeting the hypothesis.
7. **Re-profile** — capture same metric; differential flamegraph.
8. **Prove the win** — `hyperfine 'baseline' 'optimized' --warmup 3 --min-runs 10`.
9. **Guard the win** — add CI benchmark with regression bound.

## Reading Flamegraphs

- **Wide plateau on top**: hot self-time function — primary target.
- **Narrow towers**: deep call chains — examine for over-abstraction.
- **Repeated motifs**: same callee under many parents — candidate for inlining or caching.
- **Missing frames**: rebuild with `-fno-omit-frame-pointer` / `RUSTFLAGS=-C force-frame-pointers=yes`.
- **Differential flamegraph (`hotspot --diff`)**: red = added cost, blue = removed.

## Parallel Tooling

| Family | CPU sampling | Memory / alloc | Differential / benchmark |
|---|---|---|---|
| Systems (C/C++/Rust) | `perf record` + `flamegraph`, `samply`, `valgrind --tool=callgrind` | `valgrind --tool=massif`, `heaptrack`, `dhat` | `hyperfine`, `criterion`, `iai-callgrind` |
| Python | `py-spy record`, `scalene`, `cProfile` + `snakeviz` | `scalene` (memory mode), `tracemalloc`, `memray` | `pytest-benchmark`, `hyperfine` |
| Go | `go tool pprof` (cpu profile), `runtime/pprof` | `go tool pprof` (heap), `runtime.MemStats` | `go test -bench -benchmem`, `benchstat` |
| Java/Kotlin | `async-profiler`, JFR (`jcmd JFR.start`) | JFR allocation events, Eclipse MAT on heap dump | JMH, `hyperfine` |
| JavaScript/TypeScript | Chrome DevTools, `node --prof`, `clinic flame` | Chrome heap snapshot, `clinic doctor` | `tinybench`, `mitata`, `hyperfine` |
| OCaml | `landmarks`, `magic-trace` | `memtrace` + `memtrace-viewer`, `Statmemprof` | `bechamel`, `core_bench`, `hyperfine` |

Use `procs` (not `ps`). Use `bat -P -p -n` (not `cat`). Use `difft` (not `diff`). Use `hyperfine` (not `time`).

## Constitutional Rules

1. **No optimization without a profile**.
2. **One hypothesis per iteration**.
3. **Re-measure end-to-end**.
4. **Variance-aware comparison** with `hyperfine --warmup --min-runs`.
5. **Guard every win** in CI bench.
6. **Correctness first** — keep TDD green.
