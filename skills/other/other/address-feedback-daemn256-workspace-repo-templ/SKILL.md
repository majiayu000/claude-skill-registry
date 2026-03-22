---
name: address-feedback
description: Address and implement review feedback on a pull request
---

# Address Feedback

Uses **Implementer**. Parse review feedback, plan changes, and implement them with approval at each step. Ensures feedback is addressed systematically without introducing unrelated changes.

**Prerequisites:** Review feedback available, PR context (branch, changes)

---

## Phase 1: Parse Feedback

### Gather and Categorize

1. Read all review comments
2. Categorize each item by type:
   - **Blocking** — Must address before merge
   - **Suggestion** — Non-blocking improvement
   - **Nitpick** — Style preference, optional
   - **Question** — May not require code change
3. Identify exact file locations and planned actions
4. Present in structured table

### Output

```markdown
## Context Anchors

- **PR:** #<number> - <title>
- **Phase:** 1 — Parse Feedback
- **Feedback items:** <count>

## Feedback Analysis

| #   | Type       | Location    | Summary   | Planned Action |
| --- | ---------- | ----------- | --------- | -------------- |
| 1   | Blocking   | <file:line> | <summary> | <action>       |
| 2   | Suggestion | <file:line> | <summary> | <action>       |

## Next Step

Confirm understanding of feedback before implementing.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human explicitly approves:

- Feedback categorization is correct
- Planned actions are appropriate
- Priority order is agreed

---

## Phase 2: Implement Changes

### Address Each Item

1. Work through items by priority (Blocking first)
2. Make focused changes per item
3. Run the workspace's build and test commands (read from `workspace.config.yaml`) after each change
4. Report progress per item

### Output

```markdown
## Context Anchors

- **PR:** #<number> - <title>
- **Phase:** 2 — Implement Changes
- **Item:** <N of total>

## Progress

| #   | Item      | Status         | Notes           |
| --- | --------- | -------------- | --------------- |
| 1   | <summary> | ✅ Done        | <what changed>  |
| 2   | <summary> | 🔄 In Progress | <current state> |

## Verification

- [ ] Build passes
- [ ] Tests pass

## Next Step

<Continue to next item or proceed to report>

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP** after each significant change. Await approval before proceeding to the next item.

---

## Phase 3: Report

### Summarize and Prepare Commit

1. List all changes made per feedback item
2. Run the workspace's build and test commands (read from `workspace.config.yaml`)
3. Prepare commit message:

   ```
   git commit -m "fix(<scope>): address review feedback

   <body listing changes per item>"
   ```

### Output

```markdown
## Context Anchors

- **PR:** #<number> - <title>
- **Phase:** 3 — Report

## Changes Summary

| #   | Feedback Item | Resolution      | Files Modified |
| --- | ------------- | --------------- | -------------- |
| 1   | <summary>     | <what was done> | <files>        |

## Verification Block

- [x] Build passes
- [x] Tests pass (<counts>)
- [x] All blocking items addressed

## Next Step

Awaiting approval to commit changes.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not commit until human explicitly approves:

- All changes are correct
- No unintended modifications
- Commit message is appropriate

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
