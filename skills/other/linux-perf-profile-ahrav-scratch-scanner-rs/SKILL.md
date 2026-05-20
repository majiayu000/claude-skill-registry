---
name: linux-perf-profile
description: Deep Linux perf profiling — PMU counters, topdown analysis, flamegraphs, and annotated hotspot drill-down on ARM/Graviton
---

# Linux Perf Profiling

Deep hardware-level performance analysis using Linux `perf` on this ARM (Neoverse V1 / Graviton3) system. Goes beyond Criterion benchmarks to explain *why* code is slow using PMU counters, topdown decomposition, cache/TLB analysis, and annotated disassembly.

## When to Use

- Criterion benchmarks show a regression but the cause is unclear
- You need to understand *where cycles are spent* inside a hot function
- Investigating cache misses, branch mispredictions, TLB pressure, or stall cycles
- Comparing two builds at the microarchitectural level
- Generating flamegraphs for visual hotspot identification
- After `/bench-compare` finds a regression and you need to explain it

## Prerequisites

Ensure a release build with debug info exists:

```bash
RUSTFLAGS="-C target-cpu=native -C debuginfo=2" cargo build --release
```

The `-C debuginfo=2` flag is critical — it enables `perf annotate` to map samples back to Rust source lines without impacting optimization.

## Profiling Modes

Use the mode that matches your investigation. Modes are ordered from broadest to most focused.

---

### Mode 1: Topdown Overview

Get a high-level breakdown of where cycles are going: frontend stalls, backend stalls, or retiring useful work.

```bash
perf stat -e cpu_cycles,inst_retired,stall_frontend,stall_backend,stall_backend_mem,br_mis_pred_retired \
  ./target/release/scanner-rs ../linux 2>&1
```

**Derived metrics to compute:**

| Metric | Formula | Healthy | Investigate |
|--------|---------|---------|-------------|
| IPC | `inst_retired / cpu_cycles` | > 2.0 | < 1.0 |
| Frontend bound % | `stall_frontend / cpu_cycles × 100` | < 10% | > 20% |
| Backend bound % | `stall_backend / cpu_cycles × 100` | < 30% | > 40% |
| Backend memory % | `stall_backend_mem / cpu_cycles × 100` | < 15% | > 25% |
| Branch mispredict rate | `br_mis_pred_retired / br_retired × 100` | < 1% | > 3% |

**Interpretation guide:**

- **High frontend stalls** → icache misses, large code footprint, bad branch targets. Check iTLB and L1i below.
- **High backend stalls** → waiting on data. Drill into cache/TLB (Mode 3).
- **High backend memory stalls** → specifically memory-bound. Check L2/LLC misses.
- **Low IPC + low stalls** → instruction mix issue (too many µops per instruction, long-latency ops).

---

### Mode 2: Hotspot Sampling + Flamegraph

Record samples and identify which functions consume the most cycles.

#### 2a. Record

```bash
perf record -g --call-graph dwarf,32768 -F 4999 \
  ./target/release/scanner-rs ../linux
```

Flags explained:
- `-g --call-graph dwarf,32768` — DWARF-based unwinding (works with Rust, unlike frame pointers). 32KB stack dump covers deep async stacks.
- `-F 4999` — ~5000 samples/sec. Use a prime number to avoid aliasing with periodic code.

#### 2b. Report (interactive)

```bash
perf report --no-children --sort=dso,symbol --percent-limit=1.0
```

- `--no-children` shows self time only (not cumulative call-tree cost).
- `--percent-limit=1.0` hides noise below 1%.

#### 2c. Report (text, for Claude analysis)

```bash
perf report --no-children --sort=symbol --percent-limit=0.5 --stdio 2>&1 | head -80
```

Pipe the output here for analysis.

#### 2d. Flamegraph

```bash
perf script | inferno-collapse-perf | inferno-flamegraph > flamegraph.svg
```

If `inferno` is not installed: `cargo install inferno`. Alternatively:

```bash
perf script > perf.script
# Then use https://www.speedscope.app/ — drag-and-drop perf.script
```

---

### Mode 3: Cache & TLB Drill-Down

When topdown shows backend/memory stalls, measure the cache hierarchy.

```bash
perf stat -e l1d_cache,l1d_cache_refill,l1d_cache_lmiss_rd,l2d_cache,l2d_cache_refill,l2d_cache_lmiss_rd,dtlb_walk,itlb_walk,mem_access \
  ./target/release/scanner-rs ../linux 2>&1
```

**Derived metrics:**

| Metric | Formula | Healthy | Investigate |
|--------|---------|---------|-------------|
| L1d miss rate | `l1d_cache_refill / l1d_cache × 100` | < 5% | > 10% |
| L1d → L2 miss rate | `l1d_cache_lmiss_rd / l1d_cache_refill × 100` | < 30% | > 50% |
| L2 miss rate | `l2d_cache_refill / l2d_cache × 100` | < 10% | > 20% |
| L2 → LLC/DRAM rate | `l2d_cache_lmiss_rd / l2d_cache_refill × 100` | < 20% | > 40% |
| dTLB miss rate | `dtlb_walk / mem_access × 100` | < 0.5% | > 2% |
| iTLB miss rate | `itlb_walk / l1i_cache × 100` | < 0.1% | > 1% |

**Common patterns in this codebase:**

- **High L1d misses** → check struct layout, false sharing in concurrent paths, random-access patterns in `TimingWheel` or `SetAssociativeCache`.
- **High L2 misses** → working set exceeds L2 (256KB/core on Graviton3). Consider data partitioning or reducing struct sizes.
- **High dTLB walks** → large heap allocations scattered across pages. Consider hugepages or arena allocation.
- **High iTLB walks** → code bloat from monomorphization or heavy inlining. Check generic instantiation count.

---

### Mode 4: Branch Analysis

When topdown shows frontend stalls or branch misprediction issues.

```bash
perf stat -e br_pred,br_mis_pred,br_retired,br_mis_pred_retired,inst_retired \
  ./target/release/scanner-rs ../linux 2>&1
```

**Derived metrics:**

| Metric | Formula | Healthy | Investigate |
|--------|---------|---------|-------------|
| Speculative mispredict % | `br_mis_pred / br_pred × 100` | < 2% | > 5% |
| Retired mispredict % | `br_mis_pred_retired / br_retired × 100` | < 1% | > 3% |
| Branch density | `br_retired / inst_retired × 100` | < 20% | > 30% |

To find which branches are mispredicting:

```bash
perf record -e br_mis_pred_retired -c 1000 -g --call-graph dwarf \
  ./target/release/scanner-rs ../linux
perf report --stdio --percent-limit=1.0 2>&1 | head -60
```

---

### Mode 5: Annotated Source (Per-Line Costs)

Once you've identified a hot function from Mode 2, drill into it at the source-line level.

```bash
perf annotate --symbol=<function_name> --stdio 2>&1
```

For a specific event:

```bash
perf record -e l1d_cache_refill -c 10000 --call-graph dwarf \
  ./target/release/scanner-rs ../linux
perf annotate --symbol=<function_name> --stdio 2>&1
```

This shows the percentage of samples on each source line / assembly instruction. Look for:
- Lines consuming > 20% of function samples
- Unexpected memory loads (possible bounds checks)
- Spilled registers (function too complex for register allocator)

---

### Mode 6: A/B Comparison

Compare two builds at the hardware counter level to explain a Criterion regression.

#### Step 1: Baseline counters

```bash
git stash push -m "changes"
RUSTFLAGS="-C target-cpu=native -C debuginfo=2" cargo build --release
perf stat -r 3 -e cpu_cycles,inst_retired,stall_frontend,stall_backend,stall_backend_mem,l1d_cache_refill,l2d_cache_refill,br_mis_pred_retired \
  ./target/release/scanner-rs ../linux 2>&1 | tee /tmp/perf-baseline.txt
```

#### Step 2: Changed counters

```bash
git stash pop
RUSTFLAGS="-C target-cpu=native -C debuginfo=2" cargo build --release
perf stat -r 3 -e cpu_cycles,inst_retired,stall_frontend,stall_backend,stall_backend_mem,l1d_cache_refill,l2d_cache_refill,br_mis_pred_retired \
  ./target/release/scanner-rs ../linux 2>&1 | tee /tmp/perf-after.txt
```

#### Step 3: Diff analysis

Compare the two files and compute deltas. Focus on:
- Did cycle count increase? If so, did IPC drop or did instruction count increase?
- If IPC dropped, which stall category increased?
- If instructions increased, was it branch density or memory ops?

---

### Mode 7: Lock Contention & Scheduling

For diagnosing contention in async/concurrent code paths.

```bash
perf stat -e context-switches,cpu-migrations,page-faults \
  -e sdt_libpthread:mutex_entry,sdt_libpthread:mutex_acquired \
  ./target/release/scanner-rs ../linux 2>&1
```

For scheduling latency:

```bash
perf sched record ./target/release/scanner-rs ../linux
perf sched latency --sort max 2>&1 | head -30
```

---

## Event Groups for Copy-Paste

Pre-built event sets tuned for this system (ARM Neoverse V1, armv8_pmuv3).

**Multiplexing note**: This virtualized Graviton3 environment exposes ~3 simultaneous hardware counters. Do **not** use `{}` group pinning syntax — it will fail with `<not supported>`. Instead, pass events as a comma-separated list and let `perf stat` multiplex automatically. The kernel time-shares counters and scales results; the `(XX.XX%)` annotation next to each counter shows what fraction of runtime it was active. With workloads running ≥1 second, scaled values are reliable. For maximum accuracy on critical ratios, use `-r 3` (repeat 3x) and keep groups small (3-4 events).

### Set: Topdown

```
cpu_cycles,inst_retired,stall_frontend,stall_backend,stall_backend_mem,br_mis_pred_retired
```

### Set: L1 Cache

```
l1d_cache,l1d_cache_refill,l1d_cache_lmiss_rd,l1i_cache,l1i_cache_refill,l1i_cache_lmiss
```

### Set: L2 Cache + TLB

```
l2d_cache,l2d_cache_refill,l2d_cache_lmiss_rd,dtlb_walk,itlb_walk,mem_access
```

### Set: Branches

```
br_pred,br_mis_pred,br_retired,br_mis_pred_retired,inst_retired,cpu_cycles
```

### Set: Instruction Mix

```
inst_retired,inst_spec,op_retired,op_spec,cpu_cycles,stall
```

### Set: Backend Memory

```
stall_backend,stall_backend_mem,l1d_cache_lmiss_rd,l2d_cache_lmiss_rd,mem_access,cpu_cycles
```

### Precision set (3 events, no multiplexing)

When you need exact ratios without scaling, use ≤3 events:

```
cpu_cycles,inst_retired,stall_backend
```

---

## Output Format

Report findings using this structure:

```markdown
## Perf Profile: [target / scenario]

### Environment
- CPU: ARM Neoverse V1 (Graviton3), 16 cores
- Build: `RUSTFLAGS="-C target-cpu=native -C debuginfo=2"` release
- Target: [repo or benchmark name]

### Topdown Summary

| Metric | Value | Assessment |
|--------|-------|------------|
| IPC | X.XX | [good/investigate] |
| Frontend bound | X.X% | [ok/high] |
| Backend bound | X.X% | [ok/high] |
| Backend memory | X.X% | [ok/high] |
| Branch mispredict | X.X% | [ok/high] |

### Hotspots (top 5 by self%)

| Rank | Symbol | Self % | Module | Likely Cause |
|------|--------|--------|--------|--------------|
| 1 | func_name | XX.X% | scanner_rs | [explanation] |

### Cache Hierarchy (if relevant)

| Level | Accesses | Misses | Miss Rate | Assessment |
|-------|----------|--------|-----------|------------|
| L1d | X.XXB | X.XXM | X.X% | [ok/high] |
| L2 | X.XXM | X.XXM | X.X% | [ok/high] |

### Root Cause Analysis

[Narrative explaining what the numbers mean for this specific code. Connect
PMU data to source-level patterns. Reference specific lines/functions.]

### Recommendations

1. **[Issue]** at `file:line` — [specific fix with rationale tied to PMU data]
   - Expected impact: [which metric should improve and by roughly how much]
   - Validate: `perf stat -e <relevant_events> ...`

### Validation Plan

[Commands to re-run after applying fixes to confirm improvement]
```

## Caveats

- **Multiplexing**: This virtualized environment supports ~3 simultaneous counters. `perf stat` multiplexes automatically — the `(XX.XX%)` annotation shows sampling duty cycle. With ≥1s workloads, scaled values are reliable. Never use `{}` group pinning.
- **DWARF unwinding cost**: `--call-graph dwarf` adds ~5-15% overhead to the profiled process. For tight latency measurements, use `perf stat` instead of `perf record`.
- **Kernel symbols**: Some symbols may show as `[kernel.kallsyms]`. These are kernel-side costs (syscalls, page faults). If they dominate, investigate I/O patterns or memory allocation.
- **Inlining**: Heavily inlined functions may not appear as separate symbols. Use `perf annotate` on the caller to see inlined code.
- **Async runtimes**: Tokio worker threads share names. Use `-t` (per-thread) recording to separate them if needed: `perf record -t <tid>`.

## Related Skills

- `/bench-compare` — Criterion before/after measurement (use first to detect regressions)
- `/perf-regression` — Full regression workflow with acceptance criteria
- `/performance-analyzer` — Static code analysis for perf anti-patterns
- `/rust-hotspot-finder` — Classify hotspots by risk before profiling
