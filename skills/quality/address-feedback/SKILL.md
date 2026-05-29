---
name: address-feedback
description: Address and implement review feedback on a pull request.
---

# Address Feedback

The Implementer drives this workflow. Parse review feedback, plan changes, and implement them with approval at each step.

**Prerequisites:** Review feedback (what was requested), access to codebase, PR context (branch, changes).

---

## Phase 1: Parse Feedback

Extract and categorize specific requested changes.

### Steps

1. Read all review comments
2. Categorize by type (Blocking, Suggestion, Nitpick, Question)
3. Identify exact locations and planned actions
4. Summarize in a structured table

### Output

```markdown
## Context Anchors

- **PR:** #<number> - <title>
- **Feedback items:** <count>

## Feedback Analysis

| #   | Type     | Feedback  | Location    | Planned Action   |
| --- | -------- | --------- | ----------- | ---------------- |
| 1   | Blocking | <summary> | <file:line> | <planned change> |

## Next Step

Confirm understanding of feedback before implementing.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human confirms understanding of feedback.

---

## Phase 2: Implement Changes

Address each feedback item by priority.

### Steps

1. Work through items by priority (Blocking first)
2. Make focused changes per item
3. Verify each change by running the workspace's build and test commands (read from `workspace.config.yaml`)
4. Report progress per item

### ⛔ CHECKPOINT

**STOP.** Checkpoint after each significant change.

---

## Phase 3: Report

Summarize changes made and prepare for re-review.

### Steps

1. List all changes made per feedback item
2. Run build and tests
3. Prepare commit message

### Output

```markdown
## Context Anchors

- **PR:** #<number> - <title>
- **Feedback items addressed:** <count>

## Changes Made

| #   | Feedback  | Change Made     | Verified |
| --- | --------- | --------------- | -------- |
| 1   | <summary> | <what was done> | ✅       |

## Verification Block

- [x] Build passes
- [x] Tests pass

## Next Step

Approve to commit changes.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Await approval to commit.

---

## Feedback Type Handling

| Type           | Approach                                           |
| -------------- | -------------------------------------------------- |
| **Blocking**   | Must address before merge                          |
| **Suggestion** | Implement if reasonable, otherwise explain why not |
| **Nitpick**    | Optional, can discuss or accept                    |
| **Question**   | Provide answer, may not require code change        |

---

## Error Handling

| Error                                  | Recovery                               |
| -------------------------------------- | -------------------------------------- |
| Ambiguous feedback                     | Ask for clarification                  |
| Conflicting feedback items             | Flag conflict, ask for resolution      |
| Feedback requires architectural change | Escalate, don't implement unilaterally |
| Tests fail after change                | Report failure, seek guidance          |
