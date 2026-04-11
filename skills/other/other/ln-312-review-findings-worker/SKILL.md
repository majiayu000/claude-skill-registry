---
name: ln-312-review-findings-worker
description: "Use when an evaluation coordinator needs normalized findings from target artifacts and research evidence."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root.

**Type:** L3 Worker
**Category:** 3XX Planning

# Review Findings Worker

## Mandatory Read

**MANDATORY READ:** Load `shared/references/evaluation_worker_runtime_contract.md`, `shared/references/evaluation_summary_contract.md`

## Purpose

- analyze the target artifact or diff
- convert evidence into normalized findings
- avoid narrative-only review output

## Runtime

Runtime family:
- `evaluation-worker-runtime`

Required manifest fields:
- `identifier`
- `phase_order`
- `summary_kind=review-findings`
- `operation=findings`

Recommended `phase_order`:
1. `PHASE_0_CONFIG`
2. `PHASE_1_LOAD_TARGET`
3. `PHASE_2_ANALYZE`
4. `PHASE_3_NORMALIZE_FINDINGS`
5. `PHASE_4_WRITE_SUMMARY`
6. `PHASE_5_SELF_CHECK`

## Workflow

### Phase 0: Config

Load runtime manifest, target identifiers, and any linked research artifact paths.

### Phase 1: Load Target

Load only the target artifacts needed for the review scope.

### Phase 2: Analyze

1. Inspect correctness, architecture, standards, and execution risks.
2. Cross-check claims against provided research evidence when present.

### Phase 3: Normalize Findings

Each finding should prefer structured fields such as:
- `id`
- `severity`
- `category`
- `subject`
- `evidence`
- `recommendation`

### Phase 4: Write Summary

Emit `summary_kind=review-findings`.

Payload must include:
- `worker=ln-312`
- `status`
- `operation=findings`
- `warnings`

### Phase 5: Self-Check

1. Remove duplicates.
2. Remove unsupported claims.
3. Record `pass=true` only after summary write.

## Definition of Done

- [ ] Target artifact loaded
- [ ] Findings normalized
- [ ] Unsupported claims removed
- [ ] `review-findings` summary written
- [ ] Self-check passed

**Version:** 1.0.0
**Last Updated:** 2026-04-10
