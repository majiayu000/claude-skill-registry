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
**MANDATORY READ:** Load `../ln-310-multi-agent-validator/references/context_review_pipeline.md`, `../ln-310-multi-agent-validator/references/penalty_points.md`
**MANDATORY READ:** Load `../ln-310-multi-agent-validator/references/structural_validation.md`, `../ln-310-multi-agent-validator/references/standards_validation.md`, `../ln-310-multi-agent-validator/references/solution_validation.md`, `../ln-310-multi-agent-validator/references/workflow_validation.md`, `../ln-310-multi-agent-validator/references/quality_validation.md`, `../ln-310-multi-agent-validator/references/dependency_validation.md`, `../ln-310-multi-agent-validator/references/cross_reference_validation.md`, `../ln-310-multi-agent-validator/references/risk_validation.md`, `../ln-310-multi-agent-validator/references/premortem_validation.md`, `../ln-310-multi-agent-validator/references/traceability_validation.md`

## Purpose

- apply accepted low-risk repairs using the 11-group systematic validation structure
- keep repairs separate from aggregation and approval
- record cleanup evidence if background tools are launched

## Mode Gate

- `mode=story`: full 11-group repair using findings from ln-312
- `mode=plan_review|context`: apply accepted corrections only (max 5 corrections per `../ln-310-multi-agent-validator/references/context_review_pipeline.md` Compare & Correct Safety Rules)

## 11-Group Validation Structure (mode=story)

The checklists below are mandatory inputs loaded above. Use the table only as the routing map for applying them.

| # | Group | Criteria | Checklist |
|---|-------|----------|-----------|
| 1 | Structural | #1-#4, #23-#24 | `../ln-310-multi-agent-validator/references/structural_validation.md` |
| 2 | Standards | #5 | `../ln-310-multi-agent-validator/references/standards_validation.md` |
| 3 | Solution | #6, #21, #28 | `../ln-310-multi-agent-validator/references/solution_validation.md` |
| 4 | Workflow | #7-#13 | `../ln-310-multi-agent-validator/references/workflow_validation.md` |
| 5 | Quality | #14-#15 | `../ln-310-multi-agent-validator/references/quality_validation.md` |
| 6 | Dependencies | #18-#19/#19b | `../ln-310-multi-agent-validator/references/dependency_validation.md` |
| 7 | Cross-Reference | #25-#26 | `../ln-310-multi-agent-validator/references/cross_reference_validation.md` |
| 8 | Risk | #20 | `../ln-310-multi-agent-validator/references/risk_validation.md` |
| 9 | Pre-mortem | #27 | `../ln-310-multi-agent-validator/references/premortem_validation.md` |
| 10 | Verification | #22 | `../ln-310-multi-agent-validator/references/traceability_validation.md` |
| 11 | Traceability | #16-#17, #17b-#17c | `../ln-310-multi-agent-validator/references/traceability_validation.md` |

## Repair Rules

- Zero out penalty points only when the defect is actually repaired (not just acknowledged).
- Use `FLAGGED` only when human judgment is required and auto-fix cannot safely continue.
- Maximum penalty per `../ln-310-multi-agent-validator/references/penalty_points.md` (do not hardcode).
- Test strategy section may exist but remain empty.
- Apply auto-fix actions exactly as specified in each checklist's "Auto-fix actions" column.

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
2. `PHASE_1_LOAD_FINDINGS`
3. `PHASE_2_GROUP_STRUCTURAL` (#1-#4, #23-#24)
4. `PHASE_3_GROUP_STANDARDS_SOLUTION` (#5, #6, #21, #28)
5. `PHASE_4_GROUP_WORKFLOW_QUALITY` (#7-#15)
6. `PHASE_5_GROUP_DEPS_XREF` (#18-#19/#19b, #25-#26)
7. `PHASE_6_GROUP_RISK_PREMORTEM` (#20, #27)
8. `PHASE_7_GROUP_VERIFICATION_TRACE` (#22, #16-#17, #17b-#17c)
9. `PHASE_8_VERIFY_LOCAL_RESULT`
10. `PHASE_9_WRITE_SUMMARY`
11. `PHASE_10_SELF_CHECK`

## Summary

Emit `summary_kind=review-repair`.

Payload must include:
- `worker=ln-314`
- `status`
- `operation=repair`
- `warnings`

Prefer these fields when available:
- `penalty_before` (from ln-312 findings)
- `penalty_after` (after repairs)
- `flagged_items` (list of items requiring human judgment)
- `coverage_summary` (AC coverage percentage)
- `groups_processed` (count)

## Definition of Done

- [ ] Findings loaded from ln-312
- [ ] All 11 groups processed (mode=story) or accepted corrections applied (mode=plan_review|context)
- [ ] Penalty before/after tracked
- [ ] FLAGGED items recorded
- [ ] Local verification completed
- [ ] Cleanup evidence recorded when needed
- [ ] `review-repair` summary written
- [ ] Self-check passed

**Version:** 1.0.0
**Last Updated:** 2026-04-10
