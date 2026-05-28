---
name: review-plan
description: Review a proposed design or implementation plan before implementation
---

# Review Plan

Uses **Reviewer**. Evaluate a design document or implementation plan against ticket requirements and the Plan Quality Contract. Produce structured feedback and a verdict.

**Prerequisites:** Plan document path or content, ticket requirements and acceptance criteria available

---

## Phase 1: Gather Context

### Understand What Is Being Reviewed

1. Locate the plan document (check `docs/notes/` for `*ticket-<N>*` if path not provided)
2. Read the linked ticket — title, body, acceptance criteria, constraints
3. Note the ticket scope: what is in scope vs. out of scope

---

## Phase 2: Evaluate the Plan

### Apply Plan Quality Contract

Evaluate the plan against each criterion:

**The plan MUST contain:**

- [ ] **Problem statement** — Is it clear what is being solved and why?
- [ ] **Constraints** — Are non-negotiable requirements listed?
- [ ] **Scope** — Is there an explicit list of files, sections, or components in scope?
- [ ] **Ordered steps** — Are steps numbered, specific, and actionable with file paths?
- [ ] **AC mapping** — Is each acceptance criterion traced to one or more steps?
- [ ] **Verification steps** — Can the Implementer confirm each step is done?
- [ ] **Open assumptions** — Are unresolved questions listed explicitly?

**The plan MUST NOT:**

- [ ] Use vague verbs ("update", "improve", "handle") without specifying exactly what
- [ ] Reference files without providing the path
- [ ] Leave multiple approaches open for the Implementer to choose
- [ ] Skip verification steps
- [ ] Omit acceptance criteria mapping

### Completeness Assessment

Answer these questions:

1. **Is the plan detailed enough for an Implementer to execute without guessing?**
2. **Are file locations, expected changes, and verification steps specified?**
3. **Are there gaps, unstated assumptions, or overlooked risks?**

---

## Phase 3: Produce Feedback

### Structure and Present

1. Determine verdict (Approve, Request Changes)
2. List blocking issues (gaps that would cause the Implementer to guess or fail)
3. List suggestions (improvements that would increase clarity or coverage)
4. Note positive observations (well-structured sections, thorough coverage)

### Output

```markdown
## Context Anchors

- **Reviewing:** <plan document path>
- **Type:** Design
- **Issue:** #<number> - <title>

## Summary

<One paragraph overall assessment of plan quality and readiness>

## Blocking Issues

1. **[Section] <Issue>**
   - Problem: <what's missing or unclear>
   - Suggestion: <what would fix it>

## Suggestions

1. **[Section] <Suggestion>**
   - Current: <what it says now>
   - Suggested: <what would be clearer>

## Positive Notes

- <well-structured or thorough sections>

## Verdict

APPROVE | REQUEST_CHANGES

## Next Step

<If REQUEST_CHANGES: "Address feedback and revise the plan">
<If APPROVE: "Plan is ready for implementation">

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not post review until verified:

- All Plan Quality Contract criteria reviewed
- Blockers are genuinely blocking (not style preferences)
- Feedback is specific and actionable
