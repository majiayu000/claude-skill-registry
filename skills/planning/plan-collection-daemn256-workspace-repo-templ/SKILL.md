---
name: plan-collection
description: Plan a batch of related work items with phasing and dependencies
---

# Plan Collection

Uses **Planner**. Plan a group of related work items — decompose a large goal into sequenced phases with explicit dependencies, then define the individual tickets for each phase.

**Prerequisites:** A defined goal or epic, understanding of the target scope

---

## Phase 1: Decompose Into Work Items

### Break Down the Goal

1. Read the epic/goal description and acceptance criteria
2. Identify all distinct work items needed to achieve the goal
3. For each work item, define:
   - Title and one-line description
   - Type (feature, task, chore, bug)
   - Rough scope (small, medium, large)
4. Identify dependencies between items

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title> (epic/goal)
- **Phase:** 1 — Decompose

## Work Items

| #   | Title   | Type   | Size  | Dependencies |
| --- | ------- | ------ | ----- | ------------ |
| 1   | <title> | <type> | S/M/L | None         |
| 2   | <title> | <type> | S/M/L | #1           |
| 3   | <title> | <type> | S/M/L | None         |

## Next Step

Organize into phases.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Confirm the work item decomposition is correct and complete before phasing.

---

## Phase 2: Organize Into Phases

### Define Phase Boundaries

1. Group items into implementation phases based on:
   - Dependency ordering (dependencies first)
   - Logical cohesion (related changes together)
   - Risk reduction (high-risk items early for fast feedback)
2. Each phase should be independently deliverable
3. Define what "done" looks like for each phase

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title>
- **Phase:** 2 — Organize

## Implementation Phases

### Phase 1: <name>

**Goal:** <what this phase achieves>
**Items:** #1, #3
**Done when:** <acceptance criteria for the phase>

### Phase 2: <name>

**Goal:** <what this phase achieves>
**Items:** #2, #4
**Depends on:** Phase 1
**Done when:** <acceptance criteria for the phase>

## Dependency Graph

<text representation of item/phase dependencies>

## Next Step

Plan approved. Use `/plan-phase` to detail each phase, or create tickets directly.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Confirm phasing and sequencing before proceeding.

---

## Error Handling

| Error                        | Recovery                                                 |
| ---------------------------- | -------------------------------------------------------- |
| Scope too large to decompose | Break into sub-goals first, plan each separately         |
| Circular dependencies        | Refactor items to break the cycle, flag for human review |
| Items overlap                | Merge overlapping items or clarify boundaries            |
| Phase boundaries unclear     | Ask human for priority guidance to drive sequencing      |
