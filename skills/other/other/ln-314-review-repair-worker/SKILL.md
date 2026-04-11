---
name: ln-314-review-repair-worker
description: "Use when accepted findings require bounded repair changes and a structured repair summary."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root.

**Type:** L3 Worker
**Category:** 3XX Planning

# Review Repair Worker

## Mandatory Read

**MANDATORY READ:** Load `shared/references/evaluation_worker_runtime_contract.md`, `shared/references/evaluation_summary_contract.md`, `shared/references/cleanup_evidence_contract.md`

## Purpose

- apply accepted low-risk repairs
- keep repairs separate from aggregation and approval
- record cleanup evidence if background tools are launched

## Runtime

Runtime family:
- `evaluation-worker-runtime`

Required manifest fields:
- `identifier`
- `phase_order`
- `summary_kind=review-repair`
- `operation=repair`

Recommended `phase_order`:
1. `PHASE_0_CONFIG`
2. `PHASE_1_LOAD_ACCEPTED_REPAIRS`
3. `PHASE_2_APPLY_REPAIRS`
4. `PHASE_3_VERIFY_LOCAL_RESULT`
5. `PHASE_4_WRITE_SUMMARY`
6. `PHASE_5_SELF_CHECK`

## Summary

Emit `summary_kind=review-repair`.

Payload must include:
- `worker=ln-314`
- `status`
- `operation=repair`
- `warnings`

## Definition of Done

- [ ] Accepted repairs loaded
- [ ] Repairs applied or explicitly rejected
- [ ] Local verification completed
- [ ] Cleanup evidence recorded when needed
- [ ] `review-repair` summary written
- [ ] Self-check passed

**Version:** 1.0.0
**Last Updated:** 2026-04-10
