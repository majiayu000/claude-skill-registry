---
name: ln-315-review-merge-worker
description: "Use when an evaluation run must merge research, findings, documentation, and repair outputs into one verified result."
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

**Type:** L3 Worker
**Category:** 3XX Planning

# Review Merge Worker

## Mandatory Read

**MANDATORY READ:** Load `references/evaluation_worker_runtime_contract.md`, `references/evaluation_summary_contract.md`

## Purpose

- merge read-only evidence lanes after their join barrier
- deduplicate overlap against prior review history
- produce one verified aggregate result for the coordinator

## Wait/Patience Protocol

This worker does not launch agents. It consumes worker summaries and existing agent result artifacts after the evaluation runtime barrier. Do not mark an agent failed from elapsed time alone; accept only the runtime's resolved status or result metadata as the completion signal.

## Agent Finding Verification

For every agent suggestion:
- treat transport, auth, permission, timeout-without-output, or tool-missing results as operator evidence, not domain findings
- verify supported claims against code, docs, tests, runtime logs, or worker summaries before accepting
- reject unsupported, stale, duplicate, or architecture-shim suggestions
- never rewrite runner-owned result files

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
2. Load agent findings from all launched external agents.
3. Load `.hex-skills/agent-review/review_history.md` for prior review entries.

### Phase 2: Deduplicate and Verify

1. Deduplicate current findings against:
   - own analysis
   - worker findings
   - agent findings
   - prior review history
2. For each agent suggestion: independently verify per the Agent Finding Verification policy.
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
