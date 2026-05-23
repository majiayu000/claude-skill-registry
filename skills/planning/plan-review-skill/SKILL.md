---
name: plan-review
description: Use when about to implement a plan, when plan seems incomplete or has gaps, when unsure if tasks are feasible, or when validating spec before coding
context: fork
---

# Plan Review Skill

Two-phase review: analyze/document findings (separate agent), then apply approved changes (main context).

## Quick Reference

| Phase | Where | Why |
|-------|-------|-----|
| Phase 1: Review | Forked context (Haiku) | Cost-efficient, isolated analysis |
| Phase 2: Apply | Main context | Needs user interaction |

**Input:** Plan path (e.g., `_tasks/15-feature/02-plan.md`)
**Output:** `_plan-review.md` with findings + recommendation

## Baseline Problem (Why Separate Agent)

**Without separation:** Main agent reads plan, creates review doc, manages iterations, tracks findings → consumes significant context before user interaction even begins.

**With separation:** Skill runs in forked context with Haiku → returns summary only → main context preserved for Phase 2.

Benefits:
- **~80% context savings** in main conversation
- **~10x cost reduction** using Haiku for read-only analysis
- **Clean isolation** - analysis doesn't pollute implementation context

---

## Phase 1: Review → Forked Context (This Skill)

This skill runs in an isolated forked context using Haiku model.

**Tasks:**
1. Review the plan at `$ARGUMENTS` (the plan path provided)
2. Create `{TARGET_DIR}/_plan-review.md`
3. **Iterate (max 4)** until no NEW findings

**Assess:**
- Completeness: requirements covered? edge cases?
- Feasibility: achievable? hidden complexity? dependencies?
- Clarity: implementer can follow? specific paths? verification steps?
- YAGNI: unnecessary scope? duplication?

**Checklist:** tasks have file paths, verification steps, correct order, no scope creep.

**Categorize findings:** Critical/Important/Minor

**Commit the review:** `git commit -m "review: plan review for {PLAN_NAME}"`

**Return:** Summary only (count of findings, recommendation: Ready/Needs Revisions/Major Rework)

---

## Phase 2: Apply → Main Context

*After user approval only.* User returns to main conversation to discuss findings.

1. Apply user-approved fixes to source plan
2. Mark findings `[x]` in `_plan-review.md`
3. Commit: `git commit -m "plan: apply review feedback for {PLAN_NAME}"`
4. Update `_plan-review.md` with Resolution section (addressed/skipped)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Running Phase 1 in main context | Use this skill - it forks automatically |
| Applying fixes without user approval | STOP after Phase 1, wait for direction |
| Skipping commit after review | Commit `_plan-review.md` before presenting |
| Over-iterating (>4 rounds) | Quality gate: stop when no NEW findings |

---

## Example

```
User: /plan-review _tasks/20-e2e-testing/02-plan.md
Claude: [Skill runs in forked Haiku context]
Skill: "2 Critical, 3 Important, 1 Minor. Needs revisions."
Claude: Plan review complete. [summary] Full details: _plan-review.md
User: Address Critical and Important. Skip Minor.
Claude: [Phase 2 in main context - applies fixes]
```
