---
name: pr-update
description: Update an existing pull request's description or metadata
---

# PR Update

Uses **Orchestrator**. Update an existing PR's title, description, labels, or other metadata.

**Prerequisites:** PR already exists and is open

---

## Process

1. Identify the PR to update (by number or current branch)
2. Determine what needs updating:
   - Title
   - Description/body
   - Labels
   - Target branch
3. Compose the updated content
4. Present changes for approval

### Output

```markdown
## Context Anchors

- **PR:** #<pr-number> - <title>
- **Issue:** #<issue-number>

## Proposed Updates

| Field   | Current         | New         |
| ------- | --------------- | ----------- |
| <field> | <current value> | <new value> |

## Next Step

Awaiting approval to update PR.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not update PR until human explicitly approves the proposed changes.

5. Execute the update via forge operations
6. Report the result

---

## Error Handling

| Error             | Recovery                   |
| ----------------- | -------------------------- |
| PR not found      | Verify PR number or branch |
| PR already closed | Cannot update closed PRs   |
| Permission denied | Check repository access    |
