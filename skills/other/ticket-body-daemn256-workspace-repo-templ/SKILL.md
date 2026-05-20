---
name: ticket-body
description: Update a ticket's description or body content
---

# Ticket Body

Uses **Orchestrator** for ticket lifecycle. Update the body/description of an existing ticket while preserving its structure.

**Prerequisites:** Ticket number, knowledge of what needs to change

---

## Steps

1. Read the current issue body via the forge's read operation
2. Identify the section(s) to update
3. Compose the updated body, preserving sections that shouldn't change
4. Present the changes for approval — show what's changing and the full updated body

### ⛔ CHECKPOINT

**STOP.** Await approval of the body changes.

5. Write the updated body to `.tmp/scratch/issue-body.md`
6. Execute the forge's issue update operation with the new body

### Output

```
## Context Anchors

- **Issue:** #<number> - <title>

## Updated

- **Sections changed:** <list of sections modified>

## Next Step

Ticket body updated.

**Approval Required:** No
```

---

## Error Handling

| Error                 | Recovery                                     |
| --------------------- | -------------------------------------------- |
| Issue not found       | Verify the issue number                      |
| Section not found     | Show available sections, ask which to update |
| Body format corrupted | Present the full body for manual review      |
