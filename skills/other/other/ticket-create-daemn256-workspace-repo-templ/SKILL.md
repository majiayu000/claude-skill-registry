---
name: ticket-create
description: Create a new ticket from template with optional parent link
---

# Ticket Create

Uses **Orchestrator** for ticket lifecycle. Create a ticket by selecting the appropriate template, composing the body, and filing it via the issue tracker.

**Prerequisites:** Clear understanding of what needs to be done, ticket type identified

---

## Determine Ticket Type

Resolve the user's request to a ticket type and template:

| Type    | Template            | Trigger Words                     |
| ------- | ------------------- | --------------------------------- |
| Feature | `ticket-feature.md` | "new feature", "I want..."        |
| Bug     | `ticket-bug.md`     | "file a bug", "report a defect"   |
| Task    | `ticket-task.md`    | "do X", "implement Y"             |
| Spike   | `ticket-spike.md`   | "investigate", "research"         |
| Epic    | `ticket-epic.md`    | "track a group of issues", "epic" |
| Chore   | `ticket-chore.md`   | "maintenance", "cleanup", "chore" |

Templates live in `docs/workspace/templates/`.

---

## Follow-Up Mode

If this ticket is spawned from an existing issue:

1. Add "Spawned from #<parent>" in the body's Related section
2. Include context about why this was separated
3. Inherit the parent's milestone unless explicitly reassigned
4. After creation, update the parent issue body with a link to the new ticket

---

## Compose and Draft

1. Verify this work isn't already tracked — search existing issues first
2. Read the selected template from `docs/workspace/templates/`
3. Fill the template sections based on the user's description
4. Select labels: `type:<type>` plus appropriate `area:` and `topic:` labels
5. Present the draft for approval:

**Draft format:**

- **Title:** the proposed title
- **Type:** the ticket type selected
- **Labels:** the label list
- **Parent:** the parent issue number (if follow-up mode)
- Followed by the filled template body

### ⛔ CHECKPOINT

**STOP.** Await approval of title, body content, and labels.

---

## Create

1. Write the approved body to `.tmp/scratch/issue-body.md`
2. Execute the forge's issue creation operation with:
   - **Title:** from draft
   - **Body:** from `.tmp/scratch/issue-body.md`
   - **Labels:** from draft (use labels that exist on the repo)
3. If follow-up mode: update the parent issue body with a spawn reference
4. Report the created ticket number and URL

### Output

```
## Context Anchors

- **Issue:** #<number> - <title>
- **Parent:** #<parent-number> (if follow-up mode)

## Created

- **Number:** #<number>
- **URL:** <url>
- **Labels:** <labels applied>

## Next Step

Ticket created. Set board fields and metadata as needed.

**Approval Required:** No
```

---

## Error Handling

| Error                  | Recovery                                     |
| ---------------------- | -------------------------------------------- |
| Requirements unclear   | Ask clarifying questions                     |
| Duplicate issue found  | Report the duplicate, ask whether to proceed |
| Template not found     | List available templates, ask user to pick   |
| Parent issue not found | Ask for correct parent issue number          |
