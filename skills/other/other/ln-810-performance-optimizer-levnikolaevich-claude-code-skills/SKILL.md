---
name: ln-810-performance-optimizer
description: "Multi-cycle performance optimization with profiling and bottleneck analysis. Use when optimizing application performance."
disable-model-invocation: true
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

**Type:** L2 Domain Coordinator
**Category:** 8XX Optimization

# Performance Optimizer

Runtime-backed multi-cycle optimization coordinator. Profiles, researches, validates, and executes optimization hypotheses until target reached, plateau detected, or budget exhausted.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `target` | Yes | endpoint, function, or pipeline to optimize |
| `observed_metric` | Yes | current performance problem |
| `target_metric` | No | user or research-derived target |
| `max_cycles` | No | default `3` |

## Purpose & Scope

- Detect whether optimization is the right tool
- Run iterative cycles: `profile -> gate -> research -> target -> context -> validate -> execute`
- Preserve optimization artifacts under `.hex-skills/optimization/{slug}/` and runtime state under `.hex-skills/optimization/runtime/runs/{run_id}/`
- Resume deterministically from the last checkpointed phase
- Keep cycle summaries machine-readable

## Runtime Contract

**MANDATORY READ:** Load `shared/references/ci_tool_detection.md`
**MANDATORY READ:** Load `shared/references/coordinator_runtime_contract.md`, `shared/references/optimization_runtime_contract.md`, `shared/references/coordinator_summary_contract.md`

Runtime CLI:

```bash
node shared/scripts/optimization-runtime/cli.mjs start --slug {slug} --manifest-file .hex-skills/optimization/{slug}/manifest.json
node shared/scripts/optimization-runtime/cli.mjs status --slug {slug}
node shared/scripts/optimization-runtime/cli.mjs record-worker-result --payload '{...}'
node shared/scripts/optimization-runtime/cli.mjs record-summary --payload '{...}'
node shared/scripts/optimization-runtime/cli.mjs record-cycle --payload '{...}'
node shared/scripts/optimization-runtime/cli.mjs checkpoint --phase PHASE_8_EXECUTE --payload '{...}'
node shared/scripts/optimization-runtime/cli.mjs advance --to PHASE_9_CYCLE_BOUNDARY
```

## Runtime Layout

Runtime state is run-scoped, while optimization artifacts stay slug-scoped:

```text
.hex-skills/optimization/
  runtime/active/ln-810/{slug}.json
  runtime/runs/{run_id}/manifest.json
  runtime/runs/{run_id}/state.json
  runtime/runs/{run_id}/checkpoints.json
  runtime/runs/{run_id}/history.jsonl
  runtime-artifacts/runs/{run_id}/optimization-coordinator/ln-810--{slug}.json
  runtime-artifacts/runs/{run_id}/optimization-worker/{worker}--{child_identifier}.json
  {slug}/context.md
  {slug}/ln-814-log.tsv
```

## Workflow

### Phase 0: Preflight

1. Validate:
   - target identifiable
   - observed metric provided
   - git clean state
   - test infrastructure exists
2. Detect stack and optional service topology.
3. Derive slug.
4. Build manifest with:
   - `slug`
   - `target`
   - `observed_metric`
   - `target_metric`
   - `execution_mode`
   - `cycle_config`
5. Start runtime and checkpoint `PHASE_0_PREFLIGHT`.

### Phase 1: Parse Input

1. Normalize the problem statement.
2. Set or defer `target_metric`.
3. Checkpoint `PHASE_1_PARSE_INPUT`.

### Phase 2: Profile

1. Compute deterministic child metadata:
   - `identifier=ln-811--{slug}--cycle-{current_cycle}`
   - child `run_id`
   - exact `summaryArtifactPath=.hex-skills/runtime-artifacts/runs/{parent_run_id}/optimization-worker/ln-811--{slug}--cycle-{current_cycle}.json`
2. Checkpoint `PHASE_2_PROFILE` with `child_run`.
3. Invoke `ln-811-performance-profiler` with the child `runId` and exact `summaryArtifactPath`.
4. Read the emitted `optimization-worker` summary envelope from the exact artifact path.
5. Record the worker summary with `record-worker-result`.

### Phase 3: Wrong Tool Gate

Evaluate profiler output:

| Gate | Meaning | Action |
|------|---------|--------|
| `PROCEED` | optimization work is justified | continue |
| `CONCERNS` | measurements usable but imperfect | continue with warning |
| `BLOCK` | wrong tool, already optimized, or infrastructure-bound | aggregate and exit |
| `WAIVED` | user overrides `BLOCK` | continue with explicit waiver |

Rules:
- cycle 1 `BLOCK` -> finish as diagnostic result
- cycle 2+ `BLOCK` due to `already_optimized` or `within_industry_norm` -> finish as successful stop

Checkpoint `PHASE_3_WRONG_TOOL_GATE` with:
- `gate_verdict`
- `stop_reason` when blocked
- `final_result` when terminal

### Phase 4: Research

1. Compute deterministic child metadata for `ln-812`.
2. Checkpoint `PHASE_4_RESEARCH` with `child_run`.
3. Invoke `ln-812-optimization-researcher` with the child `runId` and exact `summaryArtifactPath`.
4. Read and record the emitted `optimization-worker` summary envelope.
5. If no hypotheses remain, stop after aggregate/report.

### Phase 5: Set Target

1. Resolve target metric:
   - user-specified target wins
   - otherwise use research target with confidence
   - otherwise default to 50% improvement
2. Checkpoint `PHASE_5_SET_TARGET` with `target_metric`.

### Phase 6: Write Context

1. Build `.hex-skills/optimization/{slug}/context.md`.
2. Include:
   - problem statement
   - performance map
   - target metrics
   - hypotheses and conflicts
   - local codebase findings
   - previous cycles
3. Checkpoint `PHASE_6_WRITE_CONTEXT` with `context_file`.

### Phase 7: Validate Plan

1. Compute deterministic child metadata for `ln-813`.
2. Checkpoint `PHASE_7_VALIDATE_PLAN` with `validation_verdict` and `child_run`.
3. Invoke `ln-813-optimization-plan-validator` with the child `runId` and exact `summaryArtifactPath`.
4. Read and record the emitted `optimization-worker` summary envelope.
5. If verdict is `NO_GO`, pause runtime until user resolves or waives.

### Phase 8: Execute

`execution_mode=execute`:

1. Compute deterministic child metadata for `ln-814`.
2. Checkpoint `PHASE_8_EXECUTE` with `child_run`.
3. Invoke `ln-814-optimization-executor` with the child `runId` and exact `summaryArtifactPath`.
4. Read and record the emitted `optimization-worker` summary envelope.

`execution_mode=plan_only`:

1. Do not run `ln-814`.
2. Checkpoint `PHASE_8_EXECUTE` as `skipped_by_mode`.

### Phase 9: Cycle Boundary

1. Record the cycle summary with `record-cycle`.
2. Evaluate stop conditions:
   - target met
   - plateau
   - max cycles reached
   - no new hypotheses
3. If continuing:
   - merge previous branch when needed
   - increment `current_cycle`
   - checkpoint `PHASE_9_CYCLE_BOUNDARY`
   - advance back to `PHASE_2_PROFILE`
4. If stopping:
   - checkpoint `PHASE_9_CYCLE_BOUNDARY` with `stop_reason`
   - advance to `PHASE_10_AGGREGATE`

### Phase 10: Aggregate

1. Aggregate all cycle summaries from runtime state.
2. Compute cumulative improvement.
3. Checkpoint `PHASE_10_AGGREGATE`.

### Phase 11: Report

1. Produce final report with:
   - per-cycle summary
   - cumulative improvement
   - final result
   - gap analysis when target not met
2. Checkpoint `PHASE_11_REPORT` with:
   - `report_ready=true`
   - `final_result`
3. Record the `optimization-coordinator` summary envelope with `record-summary`.
4. Complete runtime only after the report checkpoint and coordinator summary exist.

## Worker Invocation (MANDATORY)

| Phase | Worker | Purpose |
|-------|--------|---------|
| 2 | `ln-811-performance-profiler` | Build measured performance map |
| 4 | `ln-812-optimization-researcher` | Research hypotheses and targets |
| 7 | `ln-813-optimization-plan-validator` | Validate feasibility via runtime-backed review |
| 8 | `ln-814-optimization-executor` | Execute optimization strike and bisect |

```javascript
Skill(skill: "ln-811-performance-profiler")
Skill(skill: "ln-812-optimization-researcher")
Agent(... Skill(skill: "ln-813-optimization-plan-validator"))
Agent(... Skill(skill: "ln-814-optimization-executor"))
```

## TodoWrite format (mandatory)

```
- Start ln-810 runtime (pending)
- Run profiler and record summary (pending)
- Apply Wrong Tool Gate (pending)
- Run researcher and record summary (pending)
- Set target metric (pending)
- Write optimization context (pending)
- Validate plan and record summary (pending)
- Execute or skip by mode (pending)
- Record cycle boundary (pending)
- Aggregate results and write final report (pending)
```

## Critical Rules

- Runtime state is the optimization orchestration SSOT.
- Worker outputs are consumed only through summary JSON artifacts.
- `plan_only` is a first-class execution mode, not an informal branch.
- `NO_GO` from `ln-813` must pause runtime until explicitly resolved.
- Cycle history lives in runtime state, not in chat memory.
- A terminal diagnostic result is still a valid `DONE` orchestration outcome.

## Definition of Done

- [ ] Runtime started and preflight/input checkpoints recorded
- [ ] Profiler and researcher summaries recorded deterministically
- [ ] Wrong Tool Gate result checkpointed
- [ ] Target metric and context file checkpointed
- [ ] Validator summary recorded; `NO_GO` handled via `PAUSED` when needed
- [ ] Executor summary recorded or `skipped_by_mode` checkpointed
- [ ] Cycle boundary recorded for every completed cycle
- [ ] Aggregate and final report checkpoints recorded
- [ ] Runtime completed with final result and resume-free terminal state

## Phase 12: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `optimization-coordinator`. Run after phases complete. Output to chat using the `optimization-coordinator` format.

## Reference Files

- `shared/references/coordinator_runtime_contract.md`
- `shared/references/optimization_runtime_contract.md`
- `shared/references/coordinator_summary_contract.md`
- `../ln-811-performance-profiler/SKILL.md`
- `../ln-812-optimization-researcher/SKILL.md`
- `../ln-813-optimization-plan-validator/SKILL.md`
- `../ln-814-optimization-executor/SKILL.md`

---
**Version:** 3.0.0
**Last Updated:** 2026-03-15
