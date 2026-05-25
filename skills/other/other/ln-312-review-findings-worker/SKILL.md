---
name: ln-312-review-findings-worker
description: "Use when an evaluation coordinator needs normalized findings from target artifacts and research evidence."
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

**Type:** L3 Worker
**Category:** 3XX Planning

# Review Findings Worker

## Mandatory Read

**MANDATORY READ:** Load `references/evaluation_worker_runtime_contract.md`, `references/evaluation_summary_contract.md`
**MANDATORY READ:** Load `../ln-310-multi-agent-validator/references/phase2_research_audit.md`, `../ln-310-multi-agent-validator/references/penalty_points.md`
**MANDATORY READ:** Load `../ln-310-multi-agent-validator/references/premortem_validation.md`, `../ln-310-multi-agent-validator/references/cross_reference_validation.md`

## Purpose

- analyze the target artifact or diff
- convert evidence into normalized findings
- for `mode=story`: calculate penalty points across 30 criteria per `phase2_research_audit.md`
- for `mode=plan_review`: evaluate criteria #5, #6, #21, #28 only (no penalty accumulation)
- avoid narrative-only review output

## Mode Gate

- `mode=story`: full pipeline — pre-mortem, cross-reference, penalty points across 30 criteria, build fix plan
- `mode=plan_review`: applicability check, stack detection, evaluate criteria #5 (standards), #6 (library versions), #21 (alternatives), #28 (library features) only, normalize findings without penalty accumulation

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
3. `PHASE_2_PREMORTEM` (mode=story, complexity >= Medium)
4. `PHASE_3_CROSS_REFERENCE` (mode=story, multi-story Epic)
5. `PHASE_4_CRITERIA_AUDIT`
6. `PHASE_5_PENALTY_CALCULATION` (mode=story only)
7. `PHASE_6_NORMALIZE_FINDINGS`
8. `PHASE_7_WRITE_SUMMARY`
9. `PHASE_8_SELF_CHECK`

## Workflow

### Phase 0: Config

Load runtime manifest, target identifiers, and any linked research artifact paths.

### Phase 1: Load Target

Load only the target artifacts needed for the review scope.

### Phase 2: Pre-mortem (mode=story)

Execute pre-mortem analysis per `premortem_validation.md`:
1. Skip for trivial Stories (1-2 tasks, no external deps, known tech).
2. Execute for Stories with complexity >= Medium (3+ tasks, external deps, or unfamiliar tech).
3. Tigers (evidence-based risks) feed Risk criterion #20 — add to risk table BEFORE penalty calc.
4. Elephants (unstated assumptions) feed Assumptions criterion #24 — add with `[pre-mortem]` tag, Confidence=LOW.
5. Paper Tigers (fears without evidence) — document and dismiss.
6. Include pre-mortem table in audit report.

### Phase 3: Cross-Reference (mode=story)

Execute cross-reference analysis per `cross_reference_validation.md`:
1. Skip if Epic has only 1 Story or all siblings Done/Canceled.
2. Load sibling Stories via `list_issues(project=Epic.id)`.
3. Check AC overlap (#25): structured traceability first, keyword fallback advisory-only.
4. Check task duplication (#26): structured match primary.
5. Include cross-reference findings in audit report.

### Phase 4: Criteria Audit

1. `mode=story`: evaluate all 30 criteria against Story/Tasks per `phase2_research_audit.md` Auto-Fix Actions Reference.
2. `mode=plan_review`: evaluate criteria #5, #6, #21, #28 only (standards + solution groups).
3. Cross-check claims against provided research evidence when present.

### Phase 5: Penalty Calculation (mode=story)

1. Assign penalty points per violation using severity levels from `phase2_research_audit.md` (CRITICAL=10, HIGH=5, MEDIUM=3, LOW=1).
2. Apply multiple-violation rules per `penalty_points.md` Calculation Rules.
3. Calculate total penalty points.
4. Build fix plan for each violation.
5. Format penalty audit table per `penalty_points.md` Report Format.

### Phase 6: Normalize Findings

Each finding should prefer structured fields such as:
- `id`
- `severity`
- `category`
- `subject`
- `evidence`
- `recommendation`

### Phase 7: Write Summary

Emit `summary_kind=review-findings`.

Payload must include:
- `worker=ln-312`
- `status`
- `operation=findings`
- `warnings`

Prefer these fields when available:
- `findings`
- `metrics.penalty_total` (mode=story)
- `metrics.criteria_violated` (list of criterion numbers)
- `metrics.fix_plan` (array of {criterion, action, severity})
- `metrics.premortem_summary` (when executed)
- `metrics.cross_reference_summary` (when executed)

### Phase 8: Self-Check

1. Remove duplicates.
2. Remove unsupported claims.
3. Verify penalty calculation matches `penalty_points.md` rules (mode=story).
4. Record `pass=true` only after summary write.

## Definition of Done

- [ ] Target artifact loaded
- [ ] Pre-mortem executed or justified as skipped (mode=story)
- [ ] Cross-reference executed or justified as skipped (mode=story)
- [ ] Criteria audit completed (30 for story, #5/#6/#21/#28 for others)
- [ ] Penalty points calculated and fix plan built (mode=story)
- [ ] Findings normalized
- [ ] Unsupported claims removed
- [ ] `review-findings` summary written
- [ ] Self-check passed

**Version:** 1.0.0
**Last Updated:** 2026-04-10
