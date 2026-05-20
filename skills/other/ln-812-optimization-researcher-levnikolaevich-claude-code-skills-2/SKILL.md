---
name: ln-812-optimization-researcher
description: "Researches competitive benchmarks and generates optimization hypotheses for identified bottlenecks. Use after profiling."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-812-optimization-researcher

**Type:** L3 Worker
**Category:** 8XX Optimization

Researches competitive benchmarks, industry standards, and solution approaches for bottlenecks identified by the profiler. Generates prioritized hypotheses for the executor.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Performance map from profiler (real measurements: baseline metrics, per-step timing, bottleneck classification, optimization hints) |
| **Output** | Industry benchmarks, solution candidates, prioritized hypotheses (H1..H7) |
| **Pattern** | Research-first: competitors → industry → local codebase → solutions → hypotheses |

---

## Workflow

**Phases:** Competitive Analysis → Bottleneck-Specific Research → Local Codebase Check → Hypothesis Generation → Research Report

---

## Phase 1: Competitive Analysis

**MANDATORY READ:** Load `shared/references/research_tool_fallback.md` for MCP tool priority chain.

### Goal

Establish what "good" looks like for this type of operation. Define target metric if user did not provide one.

### Research Queries

| Goal | Query Template | Tool |
|------|---------------|------|
| Industry benchmark | `"{domain} API response time benchmark {year}"` | WebSearch |
| Competitor performance | `"{competitor_type} {operation} latency"` | WebSearch |
| Standard expectations | `"acceptable response time for {operation_type}"` | WebSearch |
| Framework-specific guidance | `"{framework} {operation} performance best practices"` | Context7 / Ref |

### Output

| Field | Description |
|-------|-------------|
| industry_benchmark | Expected performance range for this operation type |
| competitor_approaches | How top systems solve this (2-3 examples) |
| recommended_target | Suggested target metric (if user did not specify) |
| target_metrics | Per-metric quantitative targets (see below) |
| sources | URLs with dates for all findings |

### Target Metric Research

For each metric present in `performance_map.baseline`, research a quantitative target:

| Metric | Query Template | Tool |
|--------|---------------|------|
| wall_time_ms | `"{domain} API response time benchmark {year}"` | WebSearch |
| cpu_time_ms | `"{framework} handler CPU time benchmark"` | WebSearch |
| memory_peak_mb | `"{domain} API memory usage benchmark {year}"` | WebSearch |
| http_round_trips | `"{domain} API call count optimization best practice"` | WebSearch |
| io_bytes | `"{domain} file processing throughput benchmark"` | WebSearch |

**Output format:**

```yaml
target_metrics:
  wall_time_ms:
    value: 500
    source: "industry benchmark: translation APIs p95 200-500ms"
    confidence: HIGH
  http_round_trips:
    value: 2
    source: "best practice: batch API reduces N calls to 1-2"
    confidence: HIGH
  memory_peak_mb:
    value: 128
    source: "similar workload: 64-128MB typical"
    confidence: MEDIUM
```

**Confidence levels:** HIGH = benchmark found with source, MEDIUM = derived from best practices, LOW = estimated from general guidelines. Only include metrics present in the profiler baseline.

---

## Phase 2: Bottleneck-Specific Research

**MANDATORY READ:** Load [research_query_templates.md](references/research_query_templates.md) for per-type query templates.

### Research Strategy

Based on the primary bottleneck type from the profiler:

| Bottleneck Type | Research Focus |
|-----------------|---------------|
| Architecture | Batching, pipelining, parallelism, DataLoader pattern |
| I/O-Network | Connection pooling, HTTP/2, multiplexing, caching |
| I/O-DB | Query optimization, indexes, eager loading, bulk operations |
| I/O-File | Streaming, async I/O, memory-mapped files |
| CPU | Algorithm alternatives, vectorization, caching computation, OSS replacement |
| Cache | Eviction policies, cache key design, invalidation strategies, tiered caching, warm-up |
| External | Caching layer, circuit breaker, fallback strategies, provider alternatives |

### Research Protocol

```
FOR each top bottleneck (max 3):
  1. Select query templates from research_query_templates.md
  2. Execute research chain: Context7 → Ref → WebSearch (per research_tool_fallback.md)
  3. Collect solution approaches with expected impact
  4. Note technology prerequisites (libraries, infrastructure)
```

### Solution Evaluation

| Field | Description |
|-------|-------------|
| solution | Name/description of the approach |
| source | Where found (URL, docs section) |
| expected_impact | Estimated improvement (e.g., "9x reduction for N=9") |
| complexity | Low / Medium / High |
| prerequisites | What's needed (library, infrastructure, API support) |
| feasibility | HIGH / MEDIUM / LOW — based on prerequisites availability |

---

## Phase 3: Local Codebase Check

Before recommending external solutions, check if the codebase already has the capability:

| Check | How |
|-------|-----|
| Batch/bulk methods on client classes | Grep for `batch`, `bulk`, `multi` in client/service classes |
| Cache infrastructure | Grep for `redis`, `memcache`, `cache`, `@cached`, `lru_cache` |
| Connection pool configuration | Grep for `pool_size`, `max_connections`, `pool` in config |
| Async variants | Grep for `async_`, `aio`, `Async` prefix/suffix on methods |
| Unused configuration | Read client/service config for batch_size, max_connections params |

### Impact on Feasibility

| Finding | Effect |
|---------|--------|
| Batch API exists, not used | Feasibility = HIGH, Complexity = LOW |
| Cache infra exists, not configured for this path | Feasibility = HIGH, Complexity = LOW-MEDIUM |
| No existing capability, requires new library | Feasibility = MEDIUM, Complexity = MEDIUM-HIGH |
| Requires infrastructure change | Feasibility = LOW, Complexity = HIGH |

---

## Phase 4: Generate Hypotheses (3-7)

### Hypothesis Sources (Priority Order)

| Priority | Source |
|----------|--------|
| 1 | Local codebase check (unused existing capabilities — lowest risk) |
| 2 | Research findings (proven patterns from industry) |
| 3 | Optimization hints from profiler |

### Hypothesis Format

| Field | Description |
|-------|-------------|
| id | H1, H2, ... H7 |
| description | What to change and how |
| bottleneck_addressed | Which bottleneck from time map (step reference) |
| expected_impact | Estimated improvement % or multiplier |
| complexity | Low / Medium / High |
| risk | Low / Medium / High |
| files_to_modify | List of files that need changes |
| dependencies | Other hypotheses this depends on (e.g., "H2 requires H1") |
| conflicts_with | Hypotheses that become unnecessary if this one works |

### Anti-Bias Checks (mandatory before finalizing)

| Bias | Check | Example |
|------|-------|---------|
| **Removal bias** | For each "remove X" hypothesis: generate paired "optimize X" alternative | "remove alignment" → also "optimize alignment config" |
| **Industry bias** | "Industry doesn't use X" ≠ "X not needed for us". Check: does OUR product need it? | "CAT tools skip alignment" but our users need it for quality |
| **Premature conclusion** | "X is slow" ≠ "X is wrong". Slow may mean bad implementation, not wrong approach | 5.9s alignment → maybe wrong algorithm, not wrong feature |

**Rule:** Every "remove feature" hypothesis MUST have a paired "optimize feature" hypothesis.

### Fix Hierarchy (mandatory ordering)

Order hypotheses by fix level. Higher levels ALWAYS tried first:

| Level | Example | Priority |
|-------|---------|----------|
| 1. Configuration | `matching_methods="i"`, `pool_size=10` | Highest — try first |
| 2. Infrastructure | Add cache layer, scale service | |
| 3. Framework | Use framework feature (batch API, built-in cache) | |
| 4. Application code | Refactor algorithm, add optimization | |
| 5. Feature removal | Remove functionality | Lowest — last resort only |

**Red flag:** If highest-priority hypothesis is at level 4-5, re-examine: was a level 1-3 solution missed? Apply 5 Whys from root cause to verify.

### Ordering Rules

Sort by: `fix_level ASC, expected_impact DESC, complexity ASC, risk ASC`.

**Conflict detection:** If H1 (batch API) solves the N+1 problem, H3 (parallel calls) becomes unnecessary. Mark `H3.conflicts_with = ["H1"]`.

**Dependency detection:** If H2 (cache prefetch) builds on H1 (batch API), mark `H2.dependencies = ["H1"]`.

---

## Phase 5: Research Report

### Report Structure

```
research_result:
  industry_benchmark:
    metric: "response_time"
    expected_range: "200-500ms"
    source: "..."
  recommended_target: 500          # ms — alias for target_metrics.wall_time_ms.value
  target_metrics:                  # per-metric quantitative targets
    wall_time_ms: { value: 500, source: "...", confidence: HIGH }
    http_round_trips: { value: 2, source: "...", confidence: HIGH }
    memory_peak_mb: { value: 128, source: "...", confidence: MEDIUM }
  competitor_analysis:
    - name, approach, metric, source
  solution_candidates:
    - solution, source, expected_impact, complexity, feasibility
  hypotheses:
    - id, description, bottleneck_addressed, expected_impact, complexity, risk,
      files_to_modify, dependencies, conflicts_with
  local_codebase_findings:
    - "Batch API exists: AlignmentClient.batch_align() — accepts up to 50 pairs"
    - "Redis configured but not used for alignment cache"
  research_sources:
    - url, date, relevance
```

---

## Plan Mode

Read-only worker — all phases use MCP research tools (Ref, Context7, WebSearch) and code analysis only. Executes normally in Plan Mode via Skill().

---

## Error Handling

| Error | Recovery |
|-------|----------|
| All research tools fail | Use built-in knowledge with disclaimer: "no external sources verified" |
| No competitive benchmarks found | Skip industry benchmark, note "no baseline found — using general guidelines" |
| Cannot generate hypotheses | Return empty list — coordinator decides next step |
| Local codebase check finds nothing | Proceed with external research results only |

---

## References

- [research_query_templates.md](references/research_query_templates.md) — query templates per bottleneck type
- `shared/references/research_tool_fallback.md` — MCP research tool priority chain

---

## Runtime Summary Artifact

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md`

Emit an `optimization-worker` summary envelope.

Managed mode:
- `ln-810` passes deterministic `runId` and exact `summaryArtifactPath`
- write the summary to the provided `summaryArtifactPath`

Standalone mode:
- omit `runId` and `summaryArtifactPath`
- write `.hex-skills/runtime-artifacts/runs/{run_id}/optimization-worker/ln-812--{identifier}.json`

## Definition of Done

- [ ] Competitive analysis completed (industry benchmarks, competitor approaches)
- [ ] Target metrics researched per baseline metric (value, source, confidence)
- [ ] Target metric defined (user-provided or derived from research)
- [ ] Bottleneck-specific solutions researched via MCP chain
- [ ] Local codebase checked for existing unused capabilities
- [ ] 3-7 hypotheses generated, ordered by expected impact
- [ ] Dependencies and conflicts between hypotheses identified
- [ ] Research report prepared with sources
- [ ] Optimization research artifact written to the shared location

---

**Version:** 2.0.0
**Last Updated:** 2026-03-14
