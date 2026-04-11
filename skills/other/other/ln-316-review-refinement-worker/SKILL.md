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

## Purpose

- run iterative refinement after merge
- keep refinement sequential and bounded
- record refinement trace and cleanup evidence for every iteration

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
2. `PHASE_1_DRY_RUN_EXECUTOR`
3. `PHASE_2_ADVERSARIAL_REVIEWER`
4. `PHASE_3_NEW_DEV_TESTER`
5. `PHASE_4_GENERIC_QUALITY`
6. `PHASE_5_FINAL_SWEEP`
7. `PHASE_6_WRITE_SUMMARY`
8. `PHASE_7_SELF_CHECK`

## Execution Order

Refinement order is fixed:
1. `dry_run_executor`
2. `adversarial_reviewer`
3. `new_dev_tester`
4. `generic_quality`
5. `final_sweep`

No step may run in parallel with another refinement step.

## Summary

Emit `summary_kind=review-refinement`.

Payload must include:
- `worker=ln-316`
- `status`
- `operation=refinement`
- `warnings`

Prefer these fields:
- `verdict`
- `metrics`
- `decisions`
- `metadata.refinement_trace`

## Definition of Done

- [ ] All required refinement steps executed or justified as skipped
- [ ] Refinement trace recorded
- [ ] Cleanup evidence recorded for launched processes
- [ ] `review-refinement` summary written
- [ ] Self-check passed

**Version:** 1.0.0
**Last Updated:** 2026-04-10
