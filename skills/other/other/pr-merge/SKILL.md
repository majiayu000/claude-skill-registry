---
name: pr-merge
description: Merge a pull request with configured strategy and branch cleanup
---

# PR Merge

The Orchestrator drives this workflow. Merge an approved pull request using the configured merge strategy, clean up the branch, and update board status.

**Prerequisites:** PR is approved, CI passes (if required by profile), merge conflicts resolved.

---

## Process

1. Identify the PR to merge (by number or current branch)
2. Verify merge readiness:
   - PR is approved (per profile requirements)
   - CI checks pass (if required)
   - No merge conflicts
3. Determine merge strategy (read `project.merge-method` from `workspace.config.yaml`)
4. Present merge plan for approval

### Review Requirements by Profile

| Profile       | Reviewers | CI Required | Self-Merge | Approval Expires |
| ------------- | --------- | ----------- | ---------- | ---------------- |
| `lightweight` | 0         | No          | Yes        | Never            |
| `standard`    | 1         | Yes         | No         | On new commits   |
| `regulated`   | 2         | Yes         | No         | On new commits   |

Check `process.profile` in `workspace.config.yaml` to determine which rules apply.

### Merge Strategy

| Strategy     | When to Use                                                   |
| ------------ | ------------------------------------------------------------- |
| Merge commit | **Default.** Preserves full branch history on main            |
| Squash       | Explicit override — single-logical-change PRs only            |
| Rebase       | Explicit override — linear history, clean single-topic branch |

### Output

```markdown
## Context Anchors

- **PR:** #<pr-number> - <title>
- **Issue:** #<issue-number>
- **Strategy:** <merge method>

## Merge Plan

- PR: #<number> (<status>)
- Strategy: <merge commit | squash | rebase>
- Branch cleanup: delete remote branch after merge
- Board update: set issue to Done

## Next Step

Awaiting approval to merge.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human approves the merge.

5. Execute merge via forge operations
6. Delete remote branch (if not auto-deleted)
7. Pull main locally: `git checkout main && git pull`
8. Update board status to **Done** for the linked issue

### Board Integration

Read `workspace.config.yaml` for board field IDs.
Set issue status to Done (`board.status_options.done.option_id`).

---

## Error Handling

| Error              | Recovery                                 |
| ------------------ | ---------------------------------------- |
| Merge conflicts    | Resolve conflicts before merging         |
| CI failing         | Fix failing checks first                 |
| Approval missing   | Request review from required reviewers   |
| Branch out of date | Rebase or merge base branch into feature |
