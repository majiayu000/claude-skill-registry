---
name: ln-316-review-refinement-worker
description: "Use when an evaluation run requires bounded iterative refinement with trace and cleanup evidence."
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

**Type:** L3 Worker
**Category:** 3XX Planning

# Review Refinement Worker

## Mandatory Read

**MANDATORY READ:** Load `references/evaluation_worker_runtime_contract.md`, `references/evaluation_summary_contract.md`, `references/refinement_trace_contract.md`, `references/cleanup_evidence_contract.md`
**MANDATORY READ:** Load `references/agents/prompt_templates/iterative_refinement.md`, `references/agents/prompt_templates/refinement_perspectives.md`
**MANDATORY READ:** Load `references/monitor_integration_pattern.md`, `references/agent_review_workflow.md` (Step: Iterative Refinement)

## Purpose

- run 2-stage refinement after merge using the non-host advisor agent via `agent_runner.mjs`
- Stage 1: 3 parallel independent advisor sessions (dry_run_executor, new_dev_tester, adversarial_reviewer)
- Stage 2: 1 sequential advisor session (final_sweep) after merging Stage 1 results
- record refinement trace and cleanup evidence for every advisor session

**Critical: refinement launches the advisor externally. Do NOT use host-native sub-agents for this phase.**

## Runtime

Runtime family:
- `evaluation-worker-runtime`

Required manifest fields:
- `identifier`
- `phase_order`
- `summary_kind=review-refinement`
- `operation=refinement`

Recommended `phase_order`:
1. `PHASE_0_CONFIG`
2. `PHASE_1_STAGE1_PARALLEL`
3. `PHASE_2_STAGE2_FINAL_SWEEP`
4. `PHASE_3_WRITE_SUMMARY`
5. `PHASE_4_SELF_CHECK`

## Refinement State Machine

### Critical: Independent Sessions

Each perspective MUST be a separate `node agent_runner.mjs --agent {advisor_agent}` invocation.
Do NOT combine multiple perspectives into a single advisor prompt or session.
Each iter{N}/ subdirectory = independent advisor process with its own PID.

### Perspective Classification

| Stage | Perspective | Execution | Purpose |
|-------|------------|-----------|---------|
| 1 | `dry_run_executor` | parallel | Catch unexecutable steps, sequencing errors |
| 1 | `new_dev_tester` | parallel | Catch implicit knowledge gaps, undefined terms |
| 1 | `adversarial_reviewer` | parallel | Catch guaranteed failures, silent corruption |
| 2 | `final_sweep` | after merge | Catch regressions and drift from Stage 1 fixes |

All 4 perspectives are MANDATORY. `generic_quality` is not included — it is covered by the Phase 2 advisor review (`review_base.md` + mode template).

### Stage 1: Parallel Specialized Reviews

1. **Build artifact:** Read current state of reviewed artifact (Story+Tasks / plan file / context docs).
2. **For EACH of 3 perspectives, in parallel:**
   a. Load perspective from `refinement_perspectives.md` matching the perspective name.
   b. Build prompt: fill `iterative_refinement.md` placeholders (`{artifact_type}`, `{artifact_content}`, `{project_context}`, `{review_perspective}`, `{iteration_number}`, `{max_iterations}`, `{previous_findings_summary}`).
   c. Save prompt to `.hex-skills/agent-review/refinement/{identifier}/iter{N}/prompt.md`
      - iter1/ = dry_run_executor
      - iter2/ = new_dev_tester
      - iter3/ = adversarial_reviewer
   d. Launch independent advisor process:
      ```
      node references/agents/agent_runner.mjs --agent {advisor_agent} \
        --prompt-file .hex-skills/agent-review/refinement/{identifier}/iter{N}/prompt.md \
        --output-file .hex-skills/agent-review/refinement/{identifier}/iter{N}/result.md \
        --cwd {project_dir}
      ```
3. **Wait for ALL 3** via runtime `sync-agent`; Claude hosts may use `Monitor` for observability (see Waiting section below).
4. **Parse results** from each completed session: extract JSON from `## Structured Data` section.
5. **Merge findings:** deduplicate by (area, issue), keep higher confidence.
6. **Classify:** HIGH (impact_percent >= 20%), MEDIUM (10-19%), LOW (< 10%).
7. **Architecture Gate** on each accepted fix: "Does this implement the correct architecture directly, without backward compatibility shims?"
8. **Apply accepted fixes.**
9. **Kill all 3 processes:** `node agent_runner.mjs --verify-dead {pid}` per session. MANDATORY on Windows.
10. **Record cleanup evidence** per `cleanup_evidence_contract.md` for each session.
11. **Build `{previous_findings_summary}`** for Stage 2.

If ALL 3 advisor sessions fail → EXIT(ERROR), skip Stage 2.
If some fail → continue with available results, record partial errors.

### Stage 2: Final Sweep

1. **Build artifact:** Read post-fix state after Stage 1.
2. **Load `final_sweep`** perspective from `refinement_perspectives.md`.
3. **Build prompt** with `{previous_findings_summary}` from Stage 1.
4. **Save prompt** to `.hex-skills/agent-review/refinement/{identifier}/iter4/prompt.md`.
5. **Launch advisor** (single independent session).
6. **Wait** via runtime `sync-agent`; Claude hosts may use `Monitor` for observability.
7. **Parse result,** apply any accepted fixes (Architecture Gate on each).
8. **Kill process,** record cleanup evidence.

### Waiting for Advisor Results (MANDATORY)

Use the active runtime `sync-agent` command before parsing or merge gates. `Monitor` is optional Claude Code observability only.

For EACH launched advisor process:

When running under Claude Code, optional observability:
```
Monitor(command="tail -f {agent_log} | grep --line-buffered -E 'Phase|ERROR|DONE'", timeout_ms=120000, description="advisor refinement {perspective_name}")
```

After each sync/monitor cycle:
- Check result file for `<!-- END_AGENT_REVIEW_RESULT -->` marker.
- Marker present → parse result, proceed.
- Marker absent, log growing → continue runtime sync or optional monitor cycle.
- Marker absent, log stale >3 min → run Liveness Protocol (see `agent_review_workflow.md`).

Do NOT use `sleep` or manual stat-polling as the primary wait mechanism.

### Process Cleanup

After each advisor call (both stages):
1. Extract `pid` from runner stdout or metadata.
2. Run `node references/agents/agent_runner.mjs --verify-dead {pid}`.
3. Record cleanup evidence per `cleanup_evidence_contract.md`.
4. CLI advisor processes can accumulate on Windows if not killed.

### Exit States

| State | Meaning |
|-------|---------|
| `COMPLETED` | Both stages done, all results merged |
| `PARTIAL_ERROR` | Stage 1 had failures but Stage 2 completed |
| `ERROR` | All Stage 1 advisor sessions failed (Stage 2 skipped) |
| `SKIPPED` | No advisor available in health check |

## Summary

Emit `summary_kind=review-refinement`.

Payload must include:
- `worker=ln-316`
- `status`
- `operation=refinement`
- `warnings`

Prefer these fields:
- `stages_completed` (int: 1 or 2)
- `exit_reason` (enum: `COMPLETED`, `PARTIAL_ERROR`, `ERROR`, `SKIPPED`)
- `applied` (int: total suggestions applied across all stages)
- `architecture_gate_rejections` (count)
- `stage1_perspectives` (list of completed perspective names)
- `stage1_failed` (list of failed perspective names)
- `metadata.refinement_trace`

## Definition of Done

- [ ] Stage 1: all 3 advisor sessions launched in parallel
- [ ] Stage 2: final_sweep launched after Stage 1 merge
- [ ] All advisors launched via `agent_runner.mjs` (not host-native sub-agents)
- [ ] Runtime `sync-agent` used for waiting; Claude Monitor is optional observability
- [ ] Refinement trace recorded per `refinement_trace_contract.md`
- [ ] Cleanup evidence recorded for all launched processes
- [ ] `review-refinement` summary written
- [ ] Self-check passed

**Version:** 2.0.0
**Last Updated:** 2026-04-13
