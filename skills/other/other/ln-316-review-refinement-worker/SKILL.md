---
name: ln-316-review-refinement-worker
description: "Use when an evaluation run requires bounded iterative refinement with trace and cleanup evidence."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root.

**Type:** L3 Worker
**Category:** 3XX Planning

# Review Refinement Worker

## Mandatory Read

**MANDATORY READ:** Load `shared/references/evaluation_worker_runtime_contract.md`, `shared/references/evaluation_summary_contract.md`, `shared/references/refinement_trace_contract.md`, `shared/references/cleanup_evidence_contract.md`
**MANDATORY READ:** Load `shared/agents/prompt_templates/iterative_refinement.md`, `shared/agents/prompt_templates/refinement_perspectives.md`
**MANDATORY READ:** Load `shared/references/monitor_integration_pattern.md`, `shared/references/agent_review_workflow.md` (Step: Iterative Refinement)

## Purpose

- run iterative refinement after merge using **Codex** (external agent via `agent_runner.mjs`)
- keep refinement sequential and bounded
- record refinement trace and cleanup evidence for every iteration

**Critical: refinement launches Codex externally. Do NOT use Claude Agent() sub-agents.**

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
2. `PHASE_1_ITERATION_LOOP`
3. `PHASE_2_WRITE_SUMMARY`
4. `PHASE_3_SELF_CHECK`

## Perspective Order

Iteration order matches `refinement_perspectives.md`:
1. `generic_quality` (iter 1)
2. `dry_run_executor` (iter 2)
3. `new_dev_tester` (iter 3)
4. `adversarial_reviewer` (iter 4)
5. `final_sweep` (iter 5)

No step may run in parallel with another refinement step.

## Codex Iteration Loop (max 5 iterations)

For each iteration:

1. **Build artifact:** Read current state of reviewed artifact (Story+Tasks / plan file / context docs).
2. **Select perspective:** Load from `refinement_perspectives.md` matching the iteration number.
3. **Build prompt:** Fill `iterative_refinement.md` placeholders (`{artifact_type}`, `{artifact_content}`, `{project_context}`, `{review_perspective}`, `{iteration_number}`, `{max_iterations}`, `{previous_findings_summary}`).
4. **Save prompt:** `.hex-skills/agent-review/refinement/{identifier}/iter{N}/prompt.md`
5. **Launch Codex:**
   ```
   node shared/agents/agent_runner.mjs --agent codex \
     --prompt-file .hex-skills/agent-review/refinement/{identifier}/iter{N}/prompt.md \
     --output-file .hex-skills/agent-review/refinement/{identifier}/iter{N}/result.md \
     --cwd {project_dir}
   ```
6. **Monitor (observation only):**
   ```
   Monitor(command="tail -f {agent_log} | grep --line-buffered -E 'Phase|ERROR|DONE'",
           timeout_ms=1800000,
           description="codex refinement iter {N}")
   ```
   Fallback: if Monitor unavailable, use `Bash(run_in_background=true)`.
7. **Wait:** Minimum 1 minute between checks. Result ready when file has `<!-- END_AGENT_REVIEW_RESULT -->` marker.
8. **Parse result:** Extract JSON from `## Structured Data` section.
9. **Architecture Gate:** Before applying each accepted fix, verify: "Does this implement the correct architecture directly, without backward compatibility shims?" Reject fixes that introduce compat layers.
10. **Kill after parse:** Extract pid, run `node shared/agents/agent_runner.mjs --verify-dead {pid}`. MANDATORY on Windows. Never kill before result accepted.
11. **Evaluate exit criteria** (in order):
    a. Codex failed/timed out → exit: `ERROR`
    b. 2 consecutive perspectives returned APPROVED → exit: `CONVERGED`
    c. `iteration == 5` → exit: `MAX_ITER`
    d. Current perspective APPROVED or all-LOW → proceed to next
    e. Any MEDIUM/HIGH suggestions → apply accepted fixes, proceed to next
12. **Build `{previous_findings_summary}`** for next iteration.

### Bounded Cheap Lane

After iteration 1: if no HIGH severity findings AND max remaining risk = LOW, exit with `CONVERGED_LOW_IMPACT`. This prevents wasting Codex calls on low-risk artifacts.

### Fresh Session Rule

NEVER use `--resume-session` in refinement. Each iteration = new Codex session in its own `iter{N}/` subdirectory. Phase 2 session data pollutes context window.

### Process Cleanup

After each Codex call:
1. Extract `pid` from runner stdout or metadata.
2. Run `node shared/agents/agent_runner.mjs --verify-dead {pid}`.
3. Record cleanup evidence per `cleanup_evidence_contract.md`.
4. Codex processes accumulate on Windows if not killed.

## Summary

Emit `summary_kind=review-refinement`.

Payload must include:
- `worker=ln-316`
- `status`
- `operation=refinement`
- `warnings`

Prefer these fields:
- `iterations` (int: actual count completed)
- `exit_reason` (enum: `CONVERGED`, `CONVERGED_LOW_IMPACT`, `MAX_ITER`, `ERROR`, `SKIPPED`)
- `applied` (int: total suggestions applied across all iterations)
- `architecture_gate_rejections` (count)
- `metadata.refinement_trace`

## Definition of Done

- [ ] All required refinement steps executed or justified as skipped
- [ ] Codex launched via `agent_runner.mjs` (not Claude sub-agents)
- [ ] Refinement trace recorded per `refinement_trace_contract.md`
- [ ] Cleanup evidence recorded for launched processes
- [ ] `review-refinement` summary written
- [ ] Self-check passed

**Version:** 1.0.0
**Last Updated:** 2026-04-10
