---
name: pr-abort
description: Close a pull request without merging and clean up
---

# PR Abort

Uses **Orchestrator**. Close a pull request without merging, clean up the branch, and communicate the reason.

**Prerequisites:** PR exists and is open, decision made not to merge

---

## Process

1. Identify the PR to close (by number or current branch)
2. Determine the reason for aborting:
   - Superseded by another approach
   - No longer needed (requirements changed)
   - Blocked and abandoned
   - Experiment concluded
3. Present close plan for approval

### Output

```markdown
## Context Anchors

- **PR:** #<pr-number> - <title>
- **Issue:** #<issue-number>

## Abort Plan

- PR: #<number>
- Reason: <reason for closing>
- Branch cleanup: <delete | keep> remote branch
- Issue action: <close | reopen with new approach | return to backlog>

## Next Step

Awaiting approval to close PR.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not close the PR until human explicitly approves.

4. Close the PR via forge operations with a comment explaining the reason
5. Delete or keep the remote branch (per approval)
6. Update issue status as appropriate (per approval)

---

## Error Handling

| Error             | Recovery                 |
| ----------------- | ------------------------ |
| PR not found      | Verify PR number         |
| PR already closed | No action needed         |
| PR already merged | Cannot abort a merged PR |
