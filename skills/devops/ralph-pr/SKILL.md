---
name: ralph-pr
description: Use this skill to create a PR for a completed task
---

Your job is to create a pull request for a completed task.

## Arguments

This skill receives the same arguments as other ralph-* skills:
- `<scopes-path>` - Path to the SCOPES.yml file
- `<task-id>` - ID of the task that was just completed

## Workflow

1. Read the SCOPES.yml file
2. Find the task with the given ID
3. Get the task's milestone to determine the base branch (`base_branch`)
4. Generate the task branch name: `task-<id>-<slugified-title>`
5. Ensure all changes are committed and pushed to the task branch
6. Create a PR using `gh pr create`:
   - Title: Task title from SCOPES.yml
   - Base: The milestone's `base_branch`
   - Body should include:
     - Reference to the issue: `Closes #<github_issue>`
     - Summary of what was implemented
     - The acceptance criteria from the task
7. Report the PR URL

## PR Format

```
## Summary
<Brief description of what was implemented>

## Acceptance Criteria
- [x] Criterion 1
- [x] Criterion 2
...

Closes #<github_issue>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Merging PRs

**IMPORTANT:** When merging PRs, always use **squash and merge**. Never use regular merge or rebase.

```bash
gh pr merge <pr-number> --squash --delete-branch
```

This keeps the main branch history clean with one commit per task.

## Example

For Task 2 "Define theme constants" in Milestone 1 (base: main):
- Branch: `task-2-define-theme-constants`
- PR: `task-2-define-theme-constants` → `main`
- Title: "Define theme constants and design tokens"
- Body references: `Closes #2`
- Merge: `gh pr merge --squash --delete-branch`
