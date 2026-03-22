---
name: plan-phase
description: Detail one phase of a larger implementation plan
---

# Plan Phase

Uses **Planner**. Take a defined phase from a collection plan and produce a detailed task breakdown with sequencing, file-level specificity, and verification criteria.

**Prerequisites:** A phase defined by `/plan-collection` or equivalent, with listed work items

---

## Phase 1: Analyze the Phase

### Gather Phase Context

1. Read the collection plan to understand this phase's goals and constraints
2. Read the individual tickets/items assigned to this phase
3. Identify the files, systems, and patterns involved
4. Note what previous phases have changed (if not Phase 1)

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title> (collection/epic)
- **Phase:** <phase number> — <phase name>

## Phase Overview

**Goal:** <what this phase achieves>
**Items:** <ticket numbers or descriptions>
**Depends on:** <prior phases or items>

## Scope

**Files/systems affected:**

- <file or system 1>
- <file or system 2>

## Next Step

Produce the detailed task breakdown.

**Approval Required:** No
```

---

## Phase 2: Detail the Tasks

### Produce Task-Level Breakdown

For each work item in the phase:

1. Define the implementation tasks in execution order
2. For each task, specify:
   - What to do (action)
   - Where to do it (files, locations)
   - How to verify it (check)
3. Identify cross-item coordination points (shared files, ordering constraints)

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title>
- **Phase:** <phase number> — Detail

## Task Breakdown

### Item: <ticket title>

| #   | Task         | Files   | Verification    |
| --- | ------------ | ------- | --------------- |
| 1   | <what to do> | <where> | <how to verify> |
| 2   | <what to do> | <where> | <how to verify> |

### Item: <ticket title>

| #   | Task         | Files   | Verification    |
| --- | ------------ | ------- | --------------- |
| 1   | <what to do> | <where> | <how to verify> |

## Coordination Points

- <shared file or ordering constraint>

## Phase Verification

1. <how to verify the entire phase is done correctly>

## Next Step

Phase detailed. Ready for implementation.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Confirm the task breakdown is actionable before implementation begins.

---

## Error Handling

| Error                             | Recovery                                             |
| --------------------------------- | ---------------------------------------------------- |
| Task too large                    | Break into sub-tasks with their own verification     |
| Missing context from prior phases | Read the prior phase's output, verify assumptions    |
| Items conflict within the phase   | Resequence to resolve, or split into separate phases |
