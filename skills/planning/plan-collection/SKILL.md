---
name: plan-collection
description: Plan a batch of related work items with phasing and dependencies.
---

# Plan Collection

The Planner drives this workflow. Plan a group of related work items — decompose a large goal into sequenced phases with explicit dependencies, then define the individual tickets for each phase.

---

## Phase 1: Decompose Into Work Items

Break the goal into distinct, trackable items.

### Steps

1. Read the epic/goal description and acceptance criteria
2. Identify all distinct work items needed to achieve the goal
3. For each work item, define: title, one-line description, type (feature/task/chore/bug), rough scope (S/M/L)
4. Identify dependencies between items

### Output

Produce a work item table: # | title | type | size | dependencies.

### ⛔ CHECKPOINT

**STOP.** Confirm the work item decomposition is correct and complete before phasing.

**Approval Required:** Yes

---

## Phase 2: Organize Into Phases

Group items into deliverable phases.

### Steps

1. Group items into implementation phases based on:
   - Dependency ordering (dependencies first)
   - Logical cohesion (related changes together)
   - Risk reduction (high-risk items early for fast feedback)
2. Each phase should be independently deliverable
3. Define what "done" looks like for each phase

### Output

Produce a phased plan covering: per-phase goal, items, dependencies, and done criteria; plus a dependency graph (text representation).

### ⛔ CHECKPOINT

**STOP.** Confirm phasing and sequencing before proceeding.

**Approval Required:** Yes

---

## Error Handling

| Error                        | Recovery                                                 |
| ---------------------------- | -------------------------------------------------------- |
| Scope too large to decompose | Break into sub-goals first, plan each separately         |
| Circular dependencies        | Refactor items to break the cycle, flag for human review |
| Items overlap                | Merge overlapping items or clarify boundaries            |
| Phase boundaries unclear     | Ask human for priority guidance to drive sequencing      |
