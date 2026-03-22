---
name: plan-address-feedback
description: Address design review feedback and revise the implementation plan
---

# Plan Address Feedback

Uses **Planner**. Parse reviewer feedback on an implementation plan, revise the plan document, and verify the revision passes the Plan Quality Contract before re-review.

**Prerequisites:** Review feedback available (in conversation or linked issue comment), plan document path known

---

## Phase 1: Parse Feedback

### Categorize All Feedback Items

1. Read the complete review feedback
2. Identify the plan document being revised (path in `docs/notes/`)
3. Categorize each item:

| Category   | Definition                                   | Action      |
| ---------- | -------------------------------------------- | ----------- |
| Blocking   | Must be resolved before plan can be approved | Address now |
| Suggestion | Would improve the plan but not blocking      | Consider    |
| Nitpick    | Minor clarity improvement                    | Optional    |

4. List all blocking items explicitly before proceeding

### ⛔ CHECKPOINT

**STOP.** Confirm understanding of blocking items before revising:

- List each blocking issue and the proposed resolution
- If any blocking issue is unclear, ask for clarification before editing

---

## Phase 2: Determine Revisions

### For Each Blocking Issue

1. Identify which section of the plan the issue affects
2. Determine what specifically needs to change:
   - Missing content to add
   - Vague content to specify
   - Incorrect content to replace
3. Note the exact file path and section name

---

## Phase 3: Revise the Plan

### Update the Plan Document

1. Open the plan in `docs/notes/`
2. Address each blocking item in order
3. Address suggestions where they improve clarity without scope creep
4. Preserve all content not identified as problematic

---

## Phase 4: Verify Against Plan Quality Contract

### Re-check All Criteria

After revision, verify the plan now satisfies:

- [ ] **Problem statement** present
- [ ] **Constraints** listed
- [ ] **Scope** explicitly defined with file paths
- [ ] **Ordered steps** numbered, specific, actionable
- [ ] **AC mapping** — each AC traced to steps
- [ ] **Verification steps** — each step verifiable
- [ ] **Open assumptions** listed explicitly
- [ ] No vague verbs without specifics
- [ ] No files referenced without paths
- [ ] No ambiguous choices left for the Implementer

---

## Phase 5: Present for Re-Review

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title>
- **Plan:** <docs/notes/path>
- **Phase:** Plan Revision

## Feedback Addressed

### Blocking Issues Resolved

1. **<Issue>** — <how it was resolved>
2. **<Issue>** — <how it was resolved>

### Suggestions Incorporated

- <suggestion and what changed>

### Suggestions Deferred

- <suggestion and why deferred>

## Plan Quality Contract

- [x] Problem statement present
- [x] Constraints listed
- [x] Scope specified with file paths
- [x] Steps numbered and actionable
- [x] AC mapping complete
- [x] Verification steps included
- [x] Open assumptions listed

## Next Step

Request re-review of the revised plan.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Before presenting the revised plan for re-review:

- Confirm all blocking items from the original review are resolved
- Confirm Plan Quality Contract checklist passes
