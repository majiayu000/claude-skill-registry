---
name: plan-phase
description: Detail one phase of a larger implementation plan.
---

# Plan Phase

The Planner drives this workflow. Take a defined phase from a collection plan and produce a detailed task breakdown with sequencing, file-level specificity, and verification criteria.

---

## Phase 1: Analyze the Phase

Gather context for this specific phase.

### Steps

1. Read the collection plan to understand this phase's goals and constraints
2. Read the individual tickets/items assigned to this phase
3. Identify the files, systems, and patterns involved
4. Note what previous phases have changed (if not Phase 1)

### Output

Produce a phase overview covering: goal, items, dependencies on prior phases, files/systems affected.

**Approval Required:** No

---

## Phase 2: Detail the Tasks

Produce a task-level breakdown for each work item.

### Steps

For each work item in the phase:

1. Define the implementation tasks in execution order
2. For each task, specify:
   - What to do (action)
   - Where to do it (files, locations)
   - How to verify it (check)
3. Identify cross-item coordination points (shared files, ordering constraints)

### Output

Produce a task breakdown covering: per-item task table (# | task | files | verification), coordination points, phase verification steps.

### ⛔ CHECKPOINT

**STOP.** Confirm the task breakdown is actionable before implementation begins.

**Approval Required:** Yes

---

## Error Handling

| Error                             | Recovery                                             |
| --------------------------------- | ---------------------------------------------------- |
| Task too large                    | Break into sub-tasks with their own verification     |
| Missing context from prior phases | Read the prior phase's output, verify assumptions    |
| Items conflict within the phase   | Resequence to resolve, or split into separate phases |
