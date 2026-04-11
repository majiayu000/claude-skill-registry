---
name: ln-313-review-docs-worker
description: "Use when an evaluation run needs review-driven documentation updates and a structured documentation summary."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root.

**Type:** L3 Worker
**Category:** 3XX Planning

# Review Docs Worker

## Mandatory Read

**MANDATORY READ:** Load `shared/references/evaluation_worker_runtime_contract.md`, `shared/references/evaluation_summary_contract.md`

## Purpose

- create missing review-required docs
- update existing docs with validated changes only
- keep documentation work separate from merge and repair

## Runtime

Runtime family:
- `evaluation-worker-runtime`

Required manifest fields:
- `identifier`
- `phase_order`
- `summary_kind=review-docs`
- `operation=docs`

Recommended `phase_order`:
1. `PHASE_0_CONFIG`
2. `PHASE_1_RESOLVE_DOC_TARGETS`
3. `PHASE_2_APPLY_DOC_CHANGES`
4. `PHASE_3_WRITE_SUMMARY`
5. `PHASE_4_SELF_CHECK`

## Workflow

1. Resolve the exact documentation targets.
2. Apply only validated doc changes.
3. Record created and updated paths in the summary metadata.
4. Avoid mixing documentation generation with code repair.

## Summary

Emit `summary_kind=review-docs`.

Payload must include:
- `worker=ln-313`
- `status`
- `operation=docs`
- `warnings`

## Definition of Done

- [ ] Documentation targets resolved
- [ ] Documentation changes applied or justified as skipped
- [ ] `review-docs` summary written
- [ ] Self-check passed

**Version:** 1.0.0
**Last Updated:** 2026-04-10
