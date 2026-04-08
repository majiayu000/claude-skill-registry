---
name: ln-811-performance-profiler
description: "Profiles runtime performance with CPU, memory, and I/O metrics. Use when measuring bottlenecks before optimization."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-811-performance-profiler

**Type:** L3 Worker
**Category:** 8XX Optimization

Runtime profiler that executes the optimization target, measures multiple metrics (CPU, memory, I/O, time), instruments code for per-function breakdown, and produces a standardized performance map from real data.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Problem statement: target (file/endpoint/pipeline) + observed metric |
| **Output** | Performance map (multi-metric, per-function), suspicion stack, bottleneck classification |
| **Pattern** | Discover test → Baseline run → Static analysis → Deep profile → Performance map → Report |

---

## Workflow

**Phases:** Test Discovery → Baseline Run → Static Analysis → Deep Profile → Performance Map → Report

---

## Phase 0: Test Discovery/Creation

**MANDATORY READ:** Load `shared/references/ci_tool_detection.md` for test framework detection.
**MANDATORY READ:** Load `shared/references/benchmark_generation.md` for auto-generating benchmarks when none exist.

Find or create commands that exercise the optimization target. Two outputs: `test_command` (profiling/measurement) and `e2e_test_command` (functional safety gate).

### Step 1: Discover test_command

| Priority | Method | Action |
|----------|--------|--------|
| 1 | User-provided | User specifies test command or API endpoint |
| 2 | Discover existing E2E test | Grep test files for target entry point (stop at first match) |
| 3 | Create test script | Generate per `shared/references/benchmark_generation.md` to `.hex-skills/optimization/{slug}/profile_test.sh` |

**E2E discovery protocol** (stop at first match):

| Priority | Method | How |
|----------|--------|-----|
| 1 | Route-based search | Grep e2e/integration test files for entry point route |
| 2 | Function-based search | Grep for entry point function name |
| 3 | Module-based search | Grep for import of entry point module |

**Test creation** (if no existing test found):

| Target Type | Generated Script |
|-------------|-----------------|
| API endpoint | `curl -w "%{time_total}" -o /dev/null -s {endpoint}` |
| Function | Stack-specific benchmark per `shared/references/benchmark_generation.md` |
| Pipeline | Full pipeline invocation with test input |

### Step 2: Discover e2e_test_command

If `test_command` came from E2E discovery (Step 1 priority 2): `e2e_test_command = test_command`.

Otherwise, run E2E discovery protocol again (same 3-priority table) to find a separate functional safety test.

If not found: `e2e_test_command = null`, log: `WARNING: No e2e test covers {entry_point}. Full test suite serves as functional gate.`

### Output

| Field | Description |
|-------|-------------|
| `test_command` | Command for profiling/measurement |
| `e2e_test_command` | Command for functional safety gate (may equal test_command, or null) |
| `e2e_test_source` | Discovery method: user / route / function / module / none |

---

## Phase 1: Baseline Run (Multi-Metric)

Run `test_command` with system-level profiling. Capture simultaneously:

| Metric | How to Capture | When |
|--------|---------------|------|
| Wall time | `time` wrapper or test harness | Always |
| CPU time (user+sys) | `/usr/bin/time -v` or language profiler | Always |
| Memory peak (RSS) | `/usr/bin/time -v` (Max RSS) or `tracemalloc` / `process.memoryUsage()` | Always |
| I/O bytes | `/usr/bin/time -v` or structured logs | If I/O suspected |
| HTTP round-trips | Count from structured logs or application metrics | If network I/O in call graph |
| GPU utilization | `nvidia-smi --query-gpu` | Only if CUDA/GPU detected in stack |

### Baseline Protocol

| Parameter | Value |
|-----------|-------|
| Runs | 3 |
| Metric | Median |
| Warm-up | 1 discarded run |
| Output | `baseline` — multi-metric snapshot |

---

## Phase 2: Static Analysis → Instrumentation Points

**MANDATORY READ:** Load [bottleneck_classification.md](references/bottleneck_classification.md)

Trace call chain from code + build suspicion stack. **Purpose:** guide WHERE to instrument in Phase 3.

### Step 1: Trace Call Chain

Starting from entry point, trace depth-first (max depth 5). At each step, READ the full function body.

**Cross-service tracing:** If `service_topology` is available from coordinator and a step makes an HTTP/gRPC call to another service whose code is accessible:

| Situation | Action |
|-----------|--------|
| HTTP call to service with code in submodule/monorepo | Follow into that service's handler: resolve route → trace handler code (depth resets to 0 for the new service) |
| HTTP call to service without accessible code | Classify as External, record latency estimate |
| gRPC/message queue to known service | Same as HTTP — follow into handler if code accessible |

Record `service: "{service_name}"` on each step to track which service owns it. The performance_map `steps` tree can span multiple services.

**Depth-First Rule:** If code of the called service is accessible — ALWAYS profile INSIDE. NEVER classify an accessible service as "External/slow" without profiling its internals. "Slow" is a symptom, not a diagnosis.

**5 Whys for each bottleneck:** Before reporting a bottleneck, chain "why?" until you reach config/architecture level:
1. "What is slow?" → alignment service (5.9s) 2. "Why?" → 6 pairs × ~1s each 3. "Why ~1s per pair?" → O(n²) mwmf computation 4. "Why O(n²)?" → library default, not production config 5. "Why default?" → `matching_methods` not configured → **root cause = config**

### Step 2: Classify & Suspicion Scan

For each step, classify by type (CPU, I/O-DB, I/O-Network, I/O-File, Architecture, External, Cache) and scan for performance concerns.

Suspicion checklist (**minimum, not limitation**):

| Category | What to Look For |
|----------|-----------------|
| Connection management | Client created per-request? Missing pooling? Missing reuse? |
| Data flow | Data read multiple times? Over-fetching? Unnecessary transforms? |
| Async patterns | Sync I/O in async context? Sequential awaits without data dependency? |
| Resource lifecycle | Unclosed connections? Temp files? Memory accumulation in loop? |
| Configuration | Hardcoded timeouts? Default pool sizes? Missing batch size config? |
| Redundant work | Same validation at multiple layers? Same data loaded twice? |
| Architecture | N+1 in loop? Batch API unused? Cache infra unused? Sequential-when-parallel? |
| *(open)* | Anything else spotted — checklist does not limit findings |

### Step 2b: Suspicion Deduplication

**MANDATORY READ:** Load `shared/references/output_normalization.md`

After generating suspicions across all call chain steps, normalize and deduplicate per §1-§2:
- Normalize suspicion descriptions (replace specific values with placeholders)
- Group identical suspicions across different steps → merge into single entry with `affected_steps: [list]`
- Example: "Missing connection pooling" found in steps 1.1, 1.2, 1.3 → one suspicion with `affected_steps: ["1.1", "1.2", "1.3"]`

### Step 3: Verify & Map to Instrumentation Points

```
FOR each suspicion:
  1. VERIFY: follow code to confirm or dismiss
  2. VERDICT: CONFIRMED → map to instrumentation point | DISMISSED → log reason
  3. For each CONFIRMED suspicion, identify:
     - function to wrap with timing
     - I/O call to count
     - memory allocation to track
```

### Profiler Selection (per stack)

| Stack | Non-invasive profiler | Invasive (if non-invasive insufficient) |
|-------|----------------------|----------------------------------------|
| Python | `py-spy`, `cProfile` | `time.perf_counter()` decorators |
| Node.js | `clinic`, `--prof` | `console.time()` wrappers |
| Go | `pprof` (built-in) | Usually not needed |
| .NET | `dotnet-trace` | `Stopwatch` wrappers |
| Rust | `cargo flamegraph` | `std::time::Instant` |

**Stack detection:** per `shared/references/ci_tool_detection.md`.

---

## Phase 3: Deep Profile

### Profiler Hierarchy (escalate as needed)

| Level | Tool Examples | What It Shows | When to Use |
|-------|--------------|---------------|-------------|
| 1 | `py-spy`, `cProfile`, `pprof`, `dotnet-trace` | Function-level hotspots | Always — first pass |
| 2 | `line_profiler`, per-line timing | Line-level timing in hotspot function | Hotspot function found but cause unclear |
| 3 | `tracemalloc`, `memory_profiler` | Per-line memory allocation | Memory metrics abnormal in baseline |

### Step 1: Non-Invasive Profiling (preferred)

Run `test_command` with Level 1 profiler to get per-function breakdown without code changes.

### Step 2: Escalation Decision

After Level 1 profiler run, evaluate result against suspicion stack from Phase 2:

| Profiler Result | Action |
|-----------------|--------|
| Hotspot function identified, time breakdown confirms suspicions | DONE — proceed to Phase 4 |
| Hotspot identified but internal cause unclear (CPU vs I/O inside one function) | Escalate to Level 2 (line-level timing) |
| Memory baseline abnormal (peak or delta) | Escalate to Level 3 (memory profiler) |
| Multiple suspicions unresolved — profiler granularity insufficient | Go to Step 3 (targeted instrumentation) |
| Profiler unavailable or overhead > 20% of wall time | Go to Step 3 (targeted instrumentation) |

### Stop Conditions (Profiler Escalation)

| Condition | Action |
|-----------|--------|
| Hotspot identified with clear cause | STOP — proceed to Performance Map |
| All 3 profiler levels exhausted | STOP — build map from best available data |
| Instrumentation breaks tests | STOP — revert instrumentation, use non-invasive data only |
| Profiler overhead > 20% of wall time | STOP — skip to targeted instrumentation |

### Step 3: Targeted Instrumentation (proactive)

Add timing/logging along the call stack at instrumentation points identified in Phase 2 Step 3:

```
1. FOR each CONFIRMED suspicion without measured data:
     Add timing wrapper around target function/I/O call
     Add counter for I/O round-trips if network/DB suspected
     (cross-service: instrument in the correct service's codebase)
2. Re-run test_command (3 runs, median)
3. Collect per-function measurements from logs
4. Record list of instrumented files (may span multiple services)
```

| Instrumentation Type | When | Example |
|---------------------|------|---------|
| Timing wrapper | Always for unresolved suspicions | `time.perf_counter()` around function call |
| I/O call counter | Network or DB bottleneck suspected | Count HTTP requests, DB queries in loop |
| Memory snapshot | Memory accumulation suspected | `tracemalloc.get_traced_memory()` before/after |

**KEEP instrumentation in place.** The executor reuses it for post-optimization per-function comparison, then cleans up after strike. Report `instrumented_files` in output.

---

## Phase 4: Build Performance Map

Standardized format — feeds into `.hex-skills/optimization/{slug}/context.md` for downstream consumption.

```yaml
performance_map:
  test_command: "uv run pytest tests/automated/e2e/test_example.py -s"
  baseline:
    wall_time_ms: 7280
    cpu_time_ms: 850
    memory_peak_mb: 256
    memory_delta_mb: 45
    io_read_bytes: 1200000
    io_write_bytes: 500000
    http_round_trips: 13
  steps:                          # service field present only in multi-service topology
    - id: "1"
      function: "process_job"
      location: "app/services/job_processor.py:45"
      service: "api"             # optional — which service owns this step
      wall_time_ms: 7200
      time_share_pct: 99
      type: "function_call"
      children:
        - id: "1.1"
          function: "translate_binary"
          wall_time_ms: 7100
          type: "function_call"
          children:
            - id: "1.1.1"
              function: "tikal_extract"
              service: "tikal"   # cross-service: code traced into submodule
              wall_time_ms: 2800
              type: "http_call"
              http_round_trips: 1
            - id: "1.1.2"
              function: "mt_translate"
              service: "mt-engine"
              wall_time_ms: 3500
              type: "http_call"
              http_round_trips: 13
  bottleneck_classification: "I/O-Network"
  bottleneck_detail: "13 sequential HTTP calls to MT service (3500ms)"
  top_bottlenecks:
    - step: "1.1.2", type: "I/O-Network", share: 48%
    - step: "1.1.1", type: "I/O-Network", share: 38%
```

---

## Phase 5: Report

### Report Structure

```
profile_result:
  entry_point_info:
    type: <string>                     # "api_endpoint" | "function" | "pipeline"
    location: <string>                 # file:line
    route: <string|null>               # API route (if endpoint)
    function: <string>                 # Entry point function name
  performance_map: <object>            # Full map from Phase 4
  bottleneck_classification: <string>  # Primary bottleneck type
  bottleneck_detail: <string>          # Human-readable description
  top_bottlenecks:
    - step, type, share, description
  optimization_hints:                  # CONFIRMED suspicions only (Phase 2)
    - hint with evidence
  suspicion_stack:                     # Full audit trail (confirmed + dismissed)
    - category: <string>
      location: <string>
      description: <string>
      verdict: <string>               # "confirmed" | "dismissed"
      evidence: <string>
      verification_note: <string>
  e2e_test:
    command: <string|null>             # E2E safety test command (from Phase 0)
    source: <string>                   # user / route / function / module / none
  instrumented_files: [<string>]       # Files with active instrumentation (empty if non-invasive only)
  wrong_tool_indicators: []            # Empty = proceed, non-empty = exit
```

### Wrong Tool Indicators

| Indicator | Condition |
|-----------|-----------|
| `external_service_no_alternative` | 90%+ measured time in external service, no batch/cache/parallel path |
| `within_industry_norm` | Measured time within expected range for operation type |
| `infrastructure_bound` | Bottleneck is hardware (measured via system metrics) |
| `already_optimized` | Code already uses best patterns (confirmed by suspicion scan) |

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Cannot resolve entry point | Block: "file/function not found at {path}" |
| Test command fails on unmodified code | Block: "test fails before profiling — fix test first" |
| Profiler not available for stack | Fall back to invasive instrumentation (Phase 3 Step 2) |
| Instrumentation breaks tests | Revert immediately: `git checkout -- .` |
| Call chain too deep (> 5 levels) | Stop at depth 5, note truncation |
| Cannot classify step type | Default to "Unknown", use measured time |
| No I/O detected (pure CPU) | Classify as CPU, focus on algorithm profiling |

---

## References

- [bottleneck_classification.md](references/bottleneck_classification.md) — classification taxonomy
- [latency_estimation.md](references/latency_estimation.md) — latency heuristics (fallback for static-only mode)
- `shared/references/ci_tool_detection.md` — stack/tool detection
- `shared/references/benchmark_generation.md` — benchmark templates per stack

---

## Runtime Summary Artifact

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md`

Emit an `optimization-worker` summary envelope.

Managed mode:
- `ln-810` passes deterministic `runId` and exact `summaryArtifactPath`
- write the summary to the provided `summaryArtifactPath`

Standalone mode:
- omit `runId` and `summaryArtifactPath`
- write `.hex-skills/runtime-artifacts/runs/{run_id}/optimization-worker/ln-811--{identifier}.json`

## Definition of Done

- [ ] Test command discovered or created for optimization target
- [ ] E2E safety test discovered (or documented as unavailable)
- [ ] Baseline measured: wall time, CPU, memory (3 runs, median)
- [ ] Call graph traced and function bodies read
- [ ] Suspicion stack built: each suspicion verified and mapped to instrumentation point
- [ ] Deep profile completed (non-invasive preferred, invasive if needed)
- [ ] Instrumented files reported (cleanup deferred to executor)
- [ ] Performance map built in standardized format (real measurements)
- [ ] Top 3 bottlenecks identified from measured data
- [ ] Wrong tool indicators evaluated from real metrics
- [ ] optimization_hints contain only CONFIRMED suspicions with measurement evidence
- [ ] Report prepared with measured findings
- [ ] Optimization profile artifact written to the shared location

---

**Version:** 3.0.0
**Last Updated:** 2026-03-15
