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

## Purpose

- merge read-only evidence lanes after their join barrier
- deduplicate overlap
- produce one verified aggregate result for the coordinator

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

1. Load all input worker summaries from recorded artifact paths.
2. **Freshness check:** For each research-type summary (`summary_kind=review-research`):
   - Parse `produced_at` from envelope.
   - If older than `research_freshness_hours` (default: 1h), mark as `stale=true` and append to `warnings`.

### Phase 2: Deduplicate and Verify

1. Deduplicate findings across all worker and agent sources.
2. Reject unsupported claims (no evidence, no source reference).
3. Apply Merge Priority Rule (see below).
4. Produce one verified aggregate result.

### Phase 3: Write Summary

Emit `summary_kind=review-merge`.

Payload must include:
- `worker=ln-315`
- `status`
- `operation=merge`
- `warnings`

### Phase 4: Self-Check

1. Verify all input summaries were loaded.
2. Verify deduplication completed.
3. Record `pass=true` only after summary write.

## Merge Priority Rule

When deduplicating findings from multiple sources:
1. `code_evidence` findings take precedence over `research_claim` and `agent_inference` on the same subject.
2. If a `research_claim` contradicts `code_evidence`, keep `code_evidence` and add contradiction warning.
3. `agent_inference` findings without supporting `code_evidence` or `research_claim` are demoted to `severity=info` unless the agent provided a specific file:line reference.
4. `confidence_tier` from research cards informs merge priority: `tier_1` > `tier_2` > `tier_3`.
5. Findings without `evidence_basis` from audit workers (`summary_kind=audit-worker`) default to `code_evidence`.

## Definition of Done

- [ ] Input worker summaries loaded
- [ ] Freshness check completed
- [ ] Duplicates removed
- [ ] Unsupported findings rejected
- [ ] Merge Priority Rule applied
- [ ] `review-merge` summary written
- [ ] Self-check passed

**Version:** 1.0.0
**Last Updated:** 2026-04-10
