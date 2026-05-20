---
name: plan-design
description: Design an implementation approach for a single ticket
---

# Plan Design

Uses **Planner**. Produce a detailed, actionable implementation plan for a single work item. The plan should be specific enough that the implementer does not need to guess at file paths, content structures, or sequencing.

**Prerequisites:** Researched problem space (use `/plan-research` first if needed), clear ticket scope

---

## Phase 1: Understand the Ticket

### Gather Context

1. Read the issue body and comments
2. Identify acceptance criteria and constraints
3. Read related files, prior ADRs, and architecture docs
4. Note the current state of the codebase relevant to this change

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title>
- **Phase:** 1 — Understand

## Ticket Summary

<What this ticket asks for>

## Acceptance Criteria

- <criterion 1>
- <criterion 2>

## Current State

<Relevant codebase context>

## Next Step

Design the implementation approach.

**Approval Required:** No
```

---

## Phase 2: Design the Approach

### Produce Implementation Plan

1. Identify all files to create, modify, or delete
2. For each file change, specify:
   - Exact file path
   - What to change (with enough context to locate the edit)
   - What the change should look like (new content or transformation)
3. Define the implementation sequence (what order to make changes)
4. Identify verification steps (how to confirm correctness)

### Plan Quality Contract

Every implementation plan MUST contain:

- **Problem statement** — What is being solved and why
- **Constraints** — Non-negotiable requirements that bound the solution
- **Scope** — Explicit list of files, sections, or components in scope
- **Ordered steps** — Numbered, specific, actionable steps with file paths
- **Acceptance criteria mapping** — Each AC traced to one or more steps
- **Verification steps** — How the Implementer can confirm each step is done
- **Open assumptions** — Listed explicitly for Orchestrator to resolve

A plan MUST NOT:

- Use vague verbs: "update", "improve", "handle", "adjust" without specifying what exactly
- Reference files without providing the path
- Leave multiple approaches open for the Implementer to choose
- Skip verification steps
- Omit acceptance criteria mapping

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title>
- **Phase:** 2 — Design

## Implementation Plan

### Step 1: <description>

**File:** <path>
**Action:** Create | Modify | Delete
**Details:** <specific content or transformation>

### Step 2: <description>

**File:** <path>
**Action:** Create | Modify | Delete
**Details:** <specific content or transformation>

## Verification Steps

1. <how to verify step 1>
2. <how to verify step 2>

## Assumptions

- <assumption needing confirmation>

## Next Step

Awaiting approval to proceed with implementation.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human approves:

- Implementation plan is correct and complete
- Verification steps are sufficient
- Assumptions are confirmed or adjusted

---

## Error Handling

| Error                         | Recovery                                                          |
| ----------------------------- | ----------------------------------------------------------------- |
| Ticket scope unclear          | Ask clarifying questions, refine acceptance criteria              |
| Multiple valid approaches     | Present top 2 options with trade-offs, recommend one              |
| Dependencies on other tickets | Note the dependency, plan the work that can proceed independently |
| Missing context               | Use `/plan-research` to investigate before designing              |
