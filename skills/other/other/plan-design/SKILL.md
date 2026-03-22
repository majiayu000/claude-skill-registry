---
name: plan-design
description: Design an implementation approach for a single ticket.
---

# Plan Design

The Planner drives this workflow. Produce a detailed, actionable implementation plan for a single work item. The plan must be specific enough that the implementer does not need to guess at file paths, content structures, or sequencing.

---

## Phase 1: Understand the Ticket

Gather context before designing.

### Steps

1. Read the issue body and comments
2. Identify acceptance criteria and constraints
3. Read related files, prior ADRs, and architecture docs
4. Note the current state of the codebase relevant to this change

### Output

Produce a ticket summary covering: what the ticket asks for, acceptance criteria, relevant current state.

**Approval Required:** No

---

## Phase 2: Design the Approach

Produce a complete, file-level implementation plan.

### Steps

1. Identify all files to create, modify, or delete
2. For each file change, specify:
   - Exact file path
   - What to change (with enough context to locate the edit)
   - What the change should look like (new content or transformation)
3. Define the implementation sequence (what order to make changes)
4. Identify verification steps (how to confirm correctness)

### Plan Quality Criteria

- **No guessing required:** Every change specifies file path, location, and content
- **Sequenced:** Changes are ordered so each step builds on the last
- **Verifiable:** Each step has a way to confirm it worked
- **Scoped:** Only changes needed for this ticket — nothing extra

### Output

Produce an implementation plan covering: step-by-step file changes (file | action | details), verification steps, assumptions.

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human approves the plan, verification steps, and assumptions.

**Approval Required:** Yes

---

## Error Handling

| Error                         | Recovery                                                          |
| ----------------------------- | ----------------------------------------------------------------- |
| Ticket scope unclear          | Ask clarifying questions, refine acceptance criteria              |
| Multiple valid approaches     | Present top 2 options with trade-offs, recommend one              |
| Dependencies on other tickets | Note the dependency, plan the work that can proceed independently |
| Missing context               | Use `/skill:plan-research` to investigate before designing        |
