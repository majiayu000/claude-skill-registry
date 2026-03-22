---
name: ticket-comment
description: Add a structured comment to a ticket
---

# Ticket Comment

Uses **Orchestrator** for ticket lifecycle. Add a structured comment to an existing ticket for progress updates, status changes, or decision records.

**Prerequisites:** Ticket number, comment content or context for composing one

---

## Comment Types

| Type       | When to Use                         | Format                              |
| ---------- | ----------------------------------- | ----------------------------------- |
| Progress   | Work milestone reached              | Status summary + what's next        |
| Decision   | Design choice made during work      | Decision + rationale + alternatives |
| Blocker    | Work blocked by external dependency | What's blocked + what can unblock   |
| Completion | Work finished, ready for next phase | Summary of what was done            |

---

## Steps

1. Determine the comment type based on context
2. Compose the comment using the appropriate format
3. Present the draft for approval

### ⛔ CHECKPOINT

**STOP.** Await approval of the comment.

4. Execute the forge's comment operation on the issue

### Output

```
## Context Anchors

- **Issue:** #<number> - <title>

## Commented

- **Type:** <comment type>

## Next Step

Comment added.

**Approval Required:** No
```

---

## Error Handling

| Error           | Recovery                |
| --------------- | ----------------------- |
| Issue not found | Verify the issue number |
| Comment unclear | Ask for clarification   |
