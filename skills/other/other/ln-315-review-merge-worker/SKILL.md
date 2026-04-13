---
name: ln-315-review-merge-worker
description: "Use when an evaluation run must merge research, findings, documentation, and repair outputs into one verified result."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root.

**Type:** L3 Worker
**Category:** 3XX Planning

# Review Merge Worker

## Mandatory Read

**MANDATORY READ:** Load `shared/references/evaluation_worker_runtime_contract.md`, `shared/references/evaluation_summary_contract.md`
**MANDATORY READ:** Load `shared/references/agent_delegation_pattern.md` (Critical Verification + Background Execution sections)

## Purpose

- merge read-only evidence lanes after their join barrier
- deduplicate overlap against prior review history
- produce one verified aggregate result for the coordinator

## Wait/Patience Protocol

Codex typically takes 10-20 minutes. Do NOT skip or declare an agent failed based on elapsed time. Only the Liveness Protocol in `agent_delegation_pattern.md` determines failure.

## Runtime

Runtime family:
- `evaluation-worker-runtime`

Required manifest fields:
- `identifier`
- `phase_order`
- `summary_kind=review-merge`
- `operation=merge`

Recommended `phase_order`:
1. `PHASE_0_CONFIG`
2. `PHASE_1_LOAD_WORKER_RESULTS`
3. `PHASE_2_DEDUPLICATE_AND_VERIFY`
4. `PHASE_3_WRITE_SUMMARY`
5. `PHASE_4_SELF_CHECK`

## Workflow

### Phase 1: Load Worker Results

1. Load all input worker summaries (ln-311, ln-312, ln-313, ln-314).
2. Load agent findings from external agents (Codex, Gemini).
3. Load `.hex-skills/agent-review/review_history.md` for prior review entries.

### Phase 2: Deduplicate and Verify

1. Deduplicate current findings against:
   - own analysis
   - worker findings
   - agent findings
   - prior review history
2. For each agent suggestion: independently verify per `agent_delegation_pattern.md` Critical Verification criteria.
3. Mark each suggestion `AGREE` or `REJECT`.
4. **Architecture Gate:** Before accepting any AGREE'd suggestion, verify: "Does this implement the correct architecture directly, without backward compatibility shims or legacy workarounds?" If a suggestion introduces unnecessary compat layers, convert AGREE to REJECT.
5. Reject unsupported findings.

### Phase 3: Write Summary

Emit `summary_kind=review-merge`.

Payload must include:
- `worker=ln-315`
- `status`
- `operation=merge`
- `warnings`

Prefer these fields when available:
- `merge_summary.accepted_count`
- `merge_summary.rejected_count`
- `merge_summary.dedup_removed`
- `merge_summary.architecture_gate_rejections`

Save updated review summary to `.hex-skills/agent-review/review_history.md`.

### Phase 4: Self-Check

1. Verify deduplication completed.
2. Verify architecture gate applied to all AGREE'd suggestions.
3. Record `pass=true` only after summary write.

## Definition of Done

- [ ] Input worker summaries loaded
- [ ] Agent results loaded and verified per Critical Verification
- [ ] Duplicates removed (against findings + review history)
- [ ] Architecture Gate applied to all accepted suggestions
- [ ] Review summary saved to `review_history.md`
- [ ] `review-merge` summary written
- [ ] Self-check passed

**Version:** 1.0.0
**Last Updated:** 2026-04-10
