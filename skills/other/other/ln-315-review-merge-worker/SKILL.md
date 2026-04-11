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

## Summary

Emit `summary_kind=review-merge`.

Payload must include:
- `worker=ln-315`
- `status`
- `operation=merge`
- `warnings`

## Definition of Done

- [ ] Input worker summaries loaded
- [ ] Duplicates removed
- [ ] Unsupported findings rejected
- [ ] `review-merge` summary written
- [ ] Self-check passed

**Version:** 1.0.0
**Last Updated:** 2026-04-10
