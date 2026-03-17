---
name: spec-analyze
description: Check consistency and alignment between spec.md, plan.md, and project/tasks.md — detect drift and mismatches
triggers: [analyze spec, consistency check, alignment, drift, spec vs plan, are specs aligned, spec mismatch]
context_cost: low
---

# Spec Analyze Skill

## Goal
Verify that the three core planning artifacts — PRD.md/spec.md, plan.md, and project/tasks.md — are fully aligned. Detect any requirements that have no implementation plan, any plan items with no tasks, and any tasks with no requirement.

## Steps

1. **Load all three artifacts**
   - Read PRD.md (or spec.md) — get all EARS requirements
   - Read plan.md (or PLAN.md) — get all implementation phases and decisions
   - Read project/tasks.md — get all atomic tasks with their status

2. **Check Requirement → Plan coverage**
   For each EARS requirement in PRD.md:
   - Does plan.md have at least one item addressing this requirement?
   - Are there requirements with no corresponding plan entry?
   - Flag: `[UNCOVERED] Requirement: "WHEN user resets password THE SYSTEM SHALL..." — no plan entry`

3. **Check Plan → Task coverage**
   For each implementation phase/item in plan.md:
   - Does project/tasks.md have at least one task for this plan item?
   - Are there plan items with no corresponding tasks?
   - Flag: `[NO_TASKS] Plan item: "Implement email verification" — 0 tasks in project/tasks.md`

4. **Check Task → Requirement traceability**
   For each task in project/tasks.md:
   - Can this task be traced back to a requirement in PRD.md?
   - Are there tasks that don't correspond to any stated requirement (scope creep)?
   - Flag: `[ORPHAN_TASK] Task: "Add admin dashboard" — no corresponding requirement`

5. **Check status consistency**
   - Are there tasks marked DONE for requirements that haven't been approved yet?
   - Are there tasks IN_PROGRESS while a dependency task is still TODO?
   - Are there DONE tasks that don't have corresponding test coverage?

6. **Check EARS syntax compliance**
   - Scan all requirements for vague language: "should", "might", "user-friendly", "fast"
   - Flag: `[VAGUE] "The API should be fast" — not a testable requirement. Rewrite with measurable criterion.`

7. **Generate alignment report**
   ```markdown
   ## Spec Alignment Report

   ### Coverage: Requirements → Plan
   - COVERED: [N] requirements
   - UNCOVERED: [N] requirements (listed below)

   ### Coverage: Plan → Tasks
   - COVERED: [N] plan items
   - NO_TASKS: [N] plan items (listed below)

   ### Orphan Tasks (no requirement)
   - [list any tasks with no corresponding requirement]

   ### EARS Compliance Issues
   - [list vague requirements]

   ### Status Inconsistencies
   - [list any status conflicts]

   ### Verdict
   ALIGNED: [YES/NO]
   Blocking issues: [count]
   Recommended actions: [list]
   ```

8. **If mismatches found**: present to human and ask which artifact should be updated
   - If requirement missing from plan: "Should I add this to plan.md?"
   - If task has no requirement: "Should I add a requirement to PRD.md or remove this task?"

## Constraints
- This skill reads artifacts only — it does NOT modify them without explicit instruction
- After human decision, re-run the analysis to confirm alignment
- Run this skill whenever any of the three artifacts changes

## Output Format
Alignment report in markdown with categorized findings and clear ALIGNED: YES/NO verdict.
