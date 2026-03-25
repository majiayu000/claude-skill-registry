---
name: ln-810-performance-optimizer
description: "Multi-cycle performance optimization with profiling and bottleneck analysis. Use when optimizing application performance."
disable-model-invocation: true
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-810-performance-optimizer

**Type:** L2 Domain Coordinator
**Category:** 8XX Optimization

Iterative diagnostic pipeline for performance optimization. Profiles the full request stack, classifies bottlenecks, researches industry solutions, and tests optimization hypotheses in multiple cycles — each cycle discovers and addresses different bottlenecks as fixing the dominant one reveals the next (Amdahl's law).

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | `target` (endpoint/function/pipeline) + `observed_metric` (e.g., "6300ms response time") + optional `target_metric` + optional `max_cycles` (default 3) |
| **Output** | Optimized code with verification proof, or diagnostic report with recommendations |
| **Workers** | ln-811 (profiler) → ln-812 (researcher) → ln-813 (plan validator) → ln-814 (executor) |
| **Flow** | Phases 0-1 once, then Phases 2-8 loop up to `max_cycles` times, Phases 9-11 once |

---

## Workflow

**Phases:** Pre-flight → Parse Input → **CYCLE [** Profile → Wrong Tool Gate → Research → Set Target → Write Context → Validate Plan → Execute → Cycle Boundary **]** → Collect → Report → Meta-Analysis

---

## Phase 0: Pre-flight Checks

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| Target identifiable | Yes | Block: "specify file, endpoint, or pipeline to optimize" |
| Observed metric provided | Yes | Block: "specify what metric is slow (e.g., response time, throughput)" |
| Git clean state | Yes | Block: "commit or stash changes first" |
| Test infrastructure | Yes | Block: "tests required for safe optimization" |
| Stack detection | Yes | Detect via ci_tool_detection.md |
| Service topology | No | Detect multi-service architecture (see below) |
| State file | No | If `.hex-skills/optimization/{slug}/state.json` exists → resume from last completed gate |

**MANDATORY READ:** Load `shared/references/ci_tool_detection.md` for test/build detection.

### Service Topology Detection

Detect if optimization target spans multiple services with accessible code:

| Signal | How to Detect | Result |
|--------|--------------|--------|
| Git submodules | `git submodule status` — non-empty output | List of service paths |
| Monorepo | `ls` for `services/`, `packages/`, `apps/` directories with independent package files | List of service paths |
| Docker Compose | `docker-compose.yml` / `compose.yml` — map service names to build contexts | List of service paths + ports |
| Workspace config | `pnpm-workspace.yaml`, Cargo workspace, Go workspace | List of module paths |

**Output:** `service_topology` — map of service names to code paths. Pass to ln-811 for cross-service tracing.

If single-service (no signals): `service_topology = null` — standard single-codebase profiling.

### State Persistence

Save `.hex-skills/optimization/{slug}/state.json` after each phase completion. Enables resume on interruption.

```json
{
  "target": "src/api/endpoint.py::handler",
  "slug": "endpoint-handler",
  "cycle_config": { "max_cycles": 3, "plateau_threshold": 5 },
  "current_cycle": 1,
  "cycles": [
    {
      "cycle": 1,
      "status": "done",
      "baseline": { "wall_time_ms": 6300 },
      "final": { "wall_time_ms": 3800 },
      "improvement_pct": 39.7,
      "target_met": false,
      "bottleneck": "I/O-Network: 13 sequential HTTP calls",
      "hypotheses_applied": ["H1", "H2"],
      "branch": "optimize/ln-814-align-endpoint-c1-20260315"
    }
  ],
  "phases": {
    "0_preflight": { "status": "done", "ts": "2026-03-15T10:00:00Z" },
    "2_profile": { "status": "done", "ts": "2026-03-15T10:05:00Z", "worker": "ln-811" },
    "8_execute": { "status": "pending" }
  }
}
```

**Phase status values:** `pending` → `running` → `done` | `failed`

Update state BEFORE and AFTER each phase. For Agent-delegated phases (7, 8): set `running` before launch, `done`/`failed` after Agent returns.

On startup: if `.hex-skills/optimization/{slug}/state.json` exists, ask user: "Resume from cycle {current_cycle}, phase {last incomplete}?" or "Start fresh?"

Phases are **per-cycle** — reset at each cycle boundary. `current_cycle` + phases tells the exact resumption point.

---

## Cycle Management

| Parameter | Default | Description |
|-----------|---------|-------------|
| max_cycles | 3 | Maximum optimization cycles |
| plateau_threshold | 5 | Minimum improvement % to continue to next cycle |

Each cycle: Profile → Gate → Research → Target → Context → Validate → Execute.
Each cycle naturally discovers different bottlenecks (fixing dominant reveals next per Amdahl's law).

### Stop Conditions (evaluated after each cycle)

| Condition | Action |
|-----------|--------|
| `target_met` | STOP — target reached |
| improvement < `plateau_threshold` % | STOP — plateau detected |
| `cycle == max_cycles` | STOP — budget exhausted |
| ln-812 returns 0 hypotheses | STOP — no further optimization found |

### Between Cycles

```
1. Collect cycle results (improvement, branch, hypotheses applied)
2. Merge cycle branch: git merge {cycle_branch} --no-edit
3. Record cycle summary in state.json
4. Run /compact to compress conversation context
5. Display: ═══ CYCLE {N}/{max} ═══ Previous: {bottleneck} → {improvement}%
6. Reset phase statuses in state.json for new cycle
```

If merge has conflicts → BLOCK: report partial results, user resolves manually.

---

## Phase 1: Parse Input

Parse user input into structured problem statement:

| Field | Source | Example |
|-------|--------|---------|
| target | User-specified | `src/api/alignment.py::align_endpoint`, `/api/v1/align`, `alignment pipeline` |
| observed_metric | User-specified | `{ value: 6300, unit: "ms", type: "response_time" }` |
| target_metric | User-specified OR Phase 5 | `{ value: 500, unit: "ms" }` or null |
| max_cycles | User-specified OR default | 3 |
| audit_report | Optional | Path to ln-650 output (additional hints for profiler) |

If `target_metric` not provided by user, defer to Phase 5 (after research establishes industry benchmark).

### Generate slug

Derive `{slug}` from target for per-task isolation: sanitize to `[a-z0-9_-]`, max 50 chars.

| Target | Slug |
|--------|------|
| `src/api/alignment.py::align_endpoint` | `align-endpoint` |
| `test_idml_structure_preserved` | `test-idml-structure-preserved` |
| `/api/v1/translate` | `api-v1-translate` |

All artifacts go to `.hex-skills/optimization/{slug}/`: `context.md`, `state.json`, `ln-814-log.tsv`, `profile_test.sh`.

---

## CYCLE LOOP: Phases 2-8

```
FOR cycle = 1 to max_cycles:

  IF cycle > 1:
    1. Merge previous cycle branch: git merge {previous_branch} --no-edit
    2. /compact — compress conversation context
    3. Display cycle header:
       ═══ CYCLE {cycle}/{max_cycles} ═══
       Previous: {bottleneck} → {improvement}% improvement
       Remaining gap: {current_metric} vs target {target_metric}
    4. Reset phases in state.json
    5. Update current_cycle in state.json

  Phase 2: Profile
  Phase 3: Wrong Tool Gate
  Phase 4: Research
  Phase 5: Set Target (cycle 1 only — persists across cycles)
  Phase 6: Write Context
  Phase 7: Validate Plan
  Phase 8: Execute

  CYCLE BOUNDARY: evaluate stop conditions (see below)
```

---

## Phase 2: Profile — DELEGATE to ln-811

**Do NOT trace code, read function bodies, or profile yourself. INVOKE the profiler skill.**

**Invoke:** `Skill(skill: "ln-811-performance-profiler")`

**Pass:** problem statement from Phase 1 + audit_report path (if provided).

On cycle 2+: pass same problem statement. ln-811 re-profiles the now-optimized code — test_command is rediscovered, new baseline measured, new bottlenecks found.

ln-811 will: discover/create test → run baseline (multi-metric) → static analysis + suspicion stack → instrument → build performance map.

**Receive:** performance_map, suspicion_stack, optimization_hints, wrong_tool_indicators, e2e_test info.

---

## Phase 3: Wrong Tool Gate (4-Level Verdict)

Evaluate profiler results using structured verdict (adapted from ln-500 quality gate model).

| Verdict | Condition | Action |
|---------|-----------|--------|
| **PROCEED** | `wrong_tool_indicators` empty, measurements stable | Continue to Phase 4 (research) |
| **CONCERNS** | Measurement variance > 20% OR baseline unstable OR partial metrics only | Continue with warning — note uncertainty in context file |
| **BLOCK** | `external_service_no_alternative` OR `infrastructure_bound` OR `already_optimized` OR `within_industry_norm` | See below |
| **WAIVED** | User explicitly overrides BLOCK ("try anyway") | Continue despite indicators — log user override |

### BLOCK on Cycle 2+

On cycle 2+, `already_optimized` or `within_industry_norm` is a **SUCCESS signal** — previous cycles brought performance to acceptable level. Break the cycle loop and proceed to Phase 9 (Final Report).

### BLOCK Diagnostics

| Indicator | Diagnostic Message |
|-----------|-------------------|
| `external_service_no_alternative` | "Bottleneck is {service} latency ({X}ms). Recommend: negotiate SLA / switch provider / add cache layer." |
| `within_industry_norm` | "Current performance ({X}ms) is within industry norm ({Y}ms). No optimization needed." |
| `infrastructure_bound` | "Bottleneck is infrastructure ({detail}). Recommend: scaling / caching / CDN." |
| `already_optimized` | "Code already uses optimal patterns. Consider infrastructure scaling." |

**Exit format:** Always provide diagnostic report with performance_map — the profiling data is valuable regardless of verdict.

---

## Phase 4: Research — DELEGATE to ln-812

**Do NOT research benchmarks or generate hypotheses yourself. INVOKE the researcher skill.**

**Invoke:** `Skill(skill: "ln-812-optimization-researcher")`

**Context available:** performance_map from Phase 2 (in shared conversation).

On cycle 2+: provide in conversation context before invoking: `"Previously applied hypotheses (exclude from research): {list with descriptions}. Research NEW bottlenecks only."` This is natural Skill() conversation, not structural coupling — ln-812 remains standalone-invocable.

ln-812 will: competitive analysis → target metrics → bottleneck-specific research → local codebase check → generate hypotheses H1..H7.

**Receive:** industry_benchmark, target_metrics, hypotheses (H1..H7 with conflicts_with), local_codebase_findings, research_sources.

If ln-812 returns 0 hypotheses → STOP: no further optimization found. Proceed to Phase 9.

---

## Phase 5: Set Target Metric

**Cycle 1 only.** Target is set once and persists across all cycles. What changes between cycles is the *baseline* (each cycle's final becomes next cycle's baseline).

### Multi-Metric Target Resolution

```
FOR each metric in target_metrics from ln-812:
  IF user provided target for this metric → use
  ELIF ln-812 target_metrics[metric].confidence in [HIGH, MEDIUM] → use
  ELSE → baseline × 0.5 (50% default)
```

Primary metric (for stop condition) = metric type from `observed_metric` (what user complained about).

### Backwards-Compatible Single Target

| Situation | Action |
|-----------|--------|
| User provided `target_metric` | Use as primary target |
| User did not provide; ln-812 found target_metrics | Use `target_metrics.{primary_metric_type}` |
| Neither available | Set to 50% improvement as default target |

---

## Phase 6: Write Optimization Context

Serialize diagnostic results from Phases 2-5 into structured context.

- **Normal mode:** write `.hex-skills/optimization/{slug}/context.md` in project root — input for ln-813/ln-814
- **Plan mode:** write same structure to plan file (file writes restricted) → call ExitPlanMode

Context file is **overwritten each cycle** — it is a transient handoff to workers. Cycle history lives in `state.json` and experiment log (`ln-814-log.tsv`).

**Context file structure:**

| Section | Source | Content |
|---------|--------|---------|
| Problem Statement | Phase 1 | target, observed_metric, target_metric |
| Performance Map | ln-811 | Full performance_map (real measurements: baseline, per-step metrics, bottleneck classification) |
| Suspicion Stack | ln-811 | Confirmed + dismissed suspicions with evidence |
| Industry Benchmark | ln-812 | expected_range, source, recommended_target |
| Target Metrics | ln-812 | Structured per-metric targets with confidence |
| Hypotheses | ln-812 | Table: ID, description, bottleneck_addressed, expected_impact, complexity, risk, files_to_modify, conflicts_with |
| Dependencies/Conflicts | ln-812 | H2 requires H1; H3 conflicts with H1 (used by ln-814 for contested vs uncontested triage) |
| Local Codebase Findings | ln-812 | Batch APIs, cache infra, connection pools found in code |
| Test Command | ln-811 | Command used for profiling (reused for post-optimization measurement) |
| E2E Test | ln-811 | E2E safety test command + source (functional gate for executor) |
| Instrumented Files | ln-811 | List of files with active instrumentation (ln-814 cleans up after strike) |
| Previous Cycles | state.json | Per-cycle summary: cycle number, bottleneck, improvement %, hypotheses applied |

### Worker Delegation Strategy

| Worker | Tool | Rationale |
|--------|------|-----------|
| ln-811 | Skill() | Needs problem_statement from conversation. First heavy worker — context clean |
| ln-812 | Skill() | Needs performance_map from ln-811 conversation output. Context still manageable (~11K) |
| ln-813 | Agent() | Reads ALL input from context.md on disk. Zero conversation dependency. Isolated context prevents degradation |
| ln-814 | Agent() | Reads ALL input from context.md on disk. Zero conversation dependency. Heaviest worker benefits most from fresh context |

Phase 6 (Write Context) is the natural handoff boundary: shared context → isolated context.

---

## Phase 7: Validate Plan — DELEGATE to ln-813 (Isolated Context)

**Do NOT validate the plan yourself. INVOKE the plan validator via Agent for context isolation.**

**Invoke:**
```
Agent(description: "Validate optimization plan",
     prompt: "Execute worker.

Step 1: Invoke worker:
  Skill(skill: \"ln-813-optimization-plan-validator\")

CONTEXT:
{\"slug\": \"{slug}\", \"context_file\": \".hex-skills/optimization/{slug}/context.md\"}",
     subagent_type: "general-purpose")
```

Update `state.json`: set phase `7_validate` status to `running` before launch.

ln-813 will: agent review (Codex + Gemini) + own feasibility check → GO/GO_WITH_CONCERNS/NO_GO.

**Receive (from Agent return):** verdict (GO/GO_WITH_CONCERNS/NO_GO), corrections_applied count, hypotheses_removed list, concerns.

After Agent returns — re-read `.hex-skills/optimization/{slug}/context.md` for applied corrections. Update `state.json`: set phase `7_validate` to `done` or `failed`.

| Verdict | Action |
|---------|--------|
| GO | Proceed to Phase 8 |
| GO_WITH_CONCERNS | Proceed with warnings logged |
| NO_GO | Present issues to user. Ask: proceed (WAIVE) or stop |

---

## Phase 8: Execute — DELEGATE to ln-814 (Isolated Context)

**In Plan Mode:** SKIP this phase. Context file from Phase 6 IS the plan. Call ExitPlanMode.

**Do NOT implement optimizations yourself. INVOKE the executor via Agent for context isolation.**

**Invoke:**
```
Agent(description: "Execute optimization strike",
     prompt: "Execute worker.

Step 1: Invoke worker:
  Skill(skill: \"ln-814-optimization-executor\")

CONTEXT:
{\"slug\": \"{slug}\", \"context_file\": \".hex-skills/optimization/{slug}/context.md\"}",
     subagent_type: "general-purpose")
```

Update `state.json`: set phase `8_execute` status to `running` before launch.

ln-814 will: read context → create worktree → strike-first (apply all) → test → measure → bisect if needed → report.

**Receive (from Agent return):** branch, baseline, final, total_improvement_pct, target_met, strike_result, hypotheses_applied, hypotheses_removed, files_modified.

After Agent returns — read `.hex-skills/optimization/{slug}/ln-814-log.tsv` for experiment details. Update `state.json`: set phase `8_execute` to `done` or `failed`.

---

## Cycle Boundary (after Phase 8)

### Step 1: Collect Cycle Results

Verify Agent workers completed successfully:

| Worker | Check | On failure |
|--------|-------|------------|
| ln-813 | Agent returned text containing verdict keyword (GO/NO_GO/GO_WITH_CONCERNS) | Set phase `7_validate` to `failed`, report to user |
| ln-814 | Agent returned text with baseline + final metrics | Set phase `8_execute` to `failed`, report partial results |

Extract from ln-814:

| Field | Description |
|-------|-------------|
| branch | Worktree branch with optimizations |
| baseline | Original measurement |
| final | Measurement after optimizations |
| total_improvement_pct | Overall improvement |
| target_met | Whether target metric was reached |
| strike_result | `clean` / `bisected` / `failed` |
| hypotheses_applied | IDs applied in strike |
| hypotheses_removed | IDs removed during bisect (with reasons) |
| contested_results | Per-group: alternatives tested, winner, measurement |
| files_modified | All changed files |

### Step 2: Record Cycle Summary

Save to `state.json.cycles[]`:

```json
{
  "cycle": 1,
  "status": "done",
  "baseline": { "wall_time_ms": 6300 },
  "final": { "wall_time_ms": 3800 },
  "improvement_pct": 39.7,
  "target_met": false,
  "bottleneck": "I/O-Network: 13 sequential HTTP calls",
  "hypotheses_applied": ["H1", "H2"],
  "branch": "optimize/ln-814-align-endpoint-c1-20260315"
}
```

### Step 3: Evaluate Stop Conditions

| Check | Result | Action |
|-------|--------|--------|
| `target_met == true` | SUCCESS | Break → Phase 9 with "TARGET MET on cycle {N}" |
| `improvement_pct < plateau_threshold` | PLATEAU | Break → Phase 9 with "PLATEAU on cycle {N}: {improvement}% < {threshold}%" |
| `cycle == max_cycles` | BUDGET | Break → Phase 9 with "MAX CYCLES reached ({N}/{max})" |
| None of the above | CONTINUE | Proceed to next cycle (merge → compact → Phases 2-8) |

---

## Phase 9: Aggregate Results

Collect results across ALL completed cycles from `state.json.cycles[]` and `ln-814-log.tsv`.

Compute:
- Total improvement: `(original_baseline - final_of_last_cycle) / original_baseline × 100`
- Per-cycle gains: array of improvement percentages
- Cumulative hypotheses applied/removed across all cycles

---

## Phase 10: Final Report

### Cycle Summary Table

```
| Cycle | Bottleneck | Baseline | Final | Improvement | Hypotheses | Branch |
|-------|------------|----------|-------|-------------|------------|--------|
| 1 | I/O-Network (13 HTTP) | 6300ms | 3800ms | 39.7% | H1,H2 | opt/...-c1 |
| 2 | CPU (O(n^2) alignment) | 3800ms | 1200ms | 68.4% | H1,H3 | opt/...-c2 |
| 3 | I/O-File (temp files) | 1200ms | 480ms | 60.0% | H1 | opt/...-c3 |
| **Total** | | **6300ms** | **480ms** | **92.4%** | | |

Target: 500ms → Achieved: 480ms ✓ TARGET MET (cycle 3)
```

### Per-Cycle Detail

For each cycle, include:

| Section | Content |
|---------|---------|
| Problem | Original target + observed metric |
| Diagnosis | Bottleneck type + detail from profiler |
| Target | User-provided or research-derived (same across cycles) |
| Result | Final metric + improvement % + strike result |
| Optimizations Applied | Hypotheses applied: id, description |
| Optimizations Removed | Hypotheses removed during bisect: id, reason |
| Contested Alternatives | Per-group: alternatives tested, winner, measurement delta |

### If Target Not Met

Include gap analysis from last cycle's ln-814:
- What was achieved (cumulative improvement %)
- Remaining bottlenecks from latest time map
- Infrastructure/architecture recommendations beyond code changes
- Stop reason: plateau / max_cycles / no hypotheses

### Branches

List all cycle branches for user review. Final branch contains all optimizations.

---

## Phase 11: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `optimization-coordinator`.

---

## Error Handling

### Per-Phase Errors

| Phase | Error | Recovery |
|-------|-------|----------|
| 2 (Profile) | Cannot trace target | Report "cannot identify code path for {target}" |
| 3 (Gate) | Wrong tool exit (cycle 1) | Report diagnosis + recommendations, do NOT proceed |
| 3 (Gate) | Wrong tool exit (cycle 2+, ALREADY_OPTIMIZED) | SUCCESS — break to Phase 9 |
| 4 (Research) | No solutions found | Report bottleneck but "no known optimization pattern for {type}" |
| 4 (Research) | 0 hypotheses (cycle 2+) | STOP — no further optimization. Proceed to Phase 9 |
| 7 (Validate) | NO_GO verdict | Present issues to user, offer WAIVE or stop |
| 8 (Execute) | All hypotheses fail | Report profiling + research as diagnostic value |
| 8 (Execute) | Worker timeout | Report partial results |
| Cycle boundary | Merge conflict | BLOCK: report partial results, list completed cycles |

### Fatal Errors

| Error | Action |
|-------|--------|
| Target not resolvable | Block: "cannot find {target} in codebase" |
| No test infrastructure | Block: "tests required for safe optimization" |
| Dirty git state | Block: "commit or stash changes first" |

---

## Plan Mode Support: Phased Gate Pattern

Alternates between plan mode (approval gates) and execution.

```
GATE 1 — Plan profiling (cycle 1 only)
  Plan Mode: Phase 0-1 (preflight, parse input)
  → Present: what will be profiled, which test, which metrics, max_cycles
  → ExitPlanMode (user approves profiling)

EXECUTE 1 — Run profiling (cycle 1)
  Phase 2: Skill("ln-811") — runtime profiling (needs Bash)
  Phase 3: Wrong Tool Gate (evaluate real measurements)
  → If wrong tool → EXIT with diagnostic

GATE 2 — Plan research & execution (cycle 1 only)
  EnterPlanMode: present performance_map to user
  Phase 4: Skill("ln-812") — research (read-only, runs in plan mode)
  Phase 5: Set target metric (multi-metric)
  Phase 6: Write context file
  → Present: hypotheses, target metrics, execution plan, max_cycles
  → ExitPlanMode (user approves strike + cycle loop)

EXECUTE 2+ — Validate + Execute + Loop
  Phase 7: Agent("ln-813") — plan review in ISOLATED context (GO/NO_GO)
  Phase 8: Agent("ln-814") — strike execution in ISOLATED context
  [Cycle boundary → merge → /compact]
  Phase 2-8 (cycle 2, auto-continue)
  [Cycle boundary → merge → /compact]
  Phase 2-8 (cycle 3, auto-continue)
  Phase 9-11: Aggregate, report, meta-analysis
```

Cycles 2+ auto-continue — user already approved optimization goal. Stop conditions protect against waste.

---

## References

- `../ln-811-performance-profiler/SKILL.md` (profiler worker)
- `../ln-812-optimization-researcher/SKILL.md` (researcher worker)
- `../ln-813-optimization-plan-validator/SKILL.md` (plan validator worker)
- `../ln-814-optimization-executor/SKILL.md` (executor worker)
- `shared/references/ci_tool_detection.md` (tool detection)
- `shared/references/meta_analysis_protocol.md` (meta-analysis)

---

**TodoWrite format (mandatory):**
```
- Invoke ln-811-performance-profiler (in_progress)
- Invoke ln-812-optimization-researcher (pending)
- Write optimization context (pending)
- Invoke ln-813-optimization-plan-validator (pending)
- Invoke ln-814-optimization-executor (pending)
- Aggregate results + report (pending)
```

## Worker Invocation (MANDATORY)

| Phase | Worker | Context |
|-------|--------|---------|
| 2 | ln-811-performance-profiler | Shared (Skill tool) — runtime profiling, baseline measurement |
| 4 | ln-812-optimization-researcher | Shared (Skill tool) — competitive analysis, hypothesis generation |
| 7 | ln-813-optimization-plan-validator | Isolated (Agent tool) — reads context.md, agent review + feasibility |
| 8 | ln-814-optimization-executor | Isolated (Agent tool) — reads context.md, strike execution + bisect |

**All workers:** ln-811/ln-812 via Skill tool (shared context); ln-813/ln-814 via Agent tool (isolated context, reads from disk).

---

## Definition of Done

- [ ] Input parsed into structured problem statement (target, metric, max_cycles)
- [ ] Multi-cycle loop executed (up to max_cycles or until stop condition)
- [ ] Each cycle: profiled → gated → researched → validated → executed
- [ ] Target metrics established from ln-812 research (multi-metric)
- [ ] Context compacted between cycles (`/compact`)
- [ ] Previous cycle branches merged before re-profiling
- [ ] Cycle summary table in final report (per-cycle + cumulative)
- [ ] All cycle branches listed for user review
- [ ] Stop condition documented (target_met / plateau / max_cycles / no hypotheses)
- [ ] Meta-analysis completed with cycle metrics

---

**Version:** 3.0.0
**Last Updated:** 2026-03-15
