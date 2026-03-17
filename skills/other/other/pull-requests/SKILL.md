---
name: pull-requests
description: Use this skill for pull request workflows - creating PRs (branch, commit, push, open), reviewing PRs (code quality, test coverage, issue fixing), or merging PRs (CI checks, merge, cleanup). Handles the complete PR lifecycle via gh CLI. Triggers included, "create PR", "open PR", "review PR", "merge PR".
---

# Pull Request Workflows

This skill handles the complete PR lifecycle. Based on context and user intent, follow the appropriate workflow.

## Context

- Current git status: !`git status`
- Current branch: !`git branch --show-current`
- PR state (if exists): !`GH_PAGER= gh pr view --json number,title,state 2>/dev/null || echo "No PR for current branch"`
- Arguments: $ARGUMENTS

## Workflow Selection

**Determine which workflow to use based on context:**

### Use Creating Workflow when:
- User asks to "create a PR", "open a PR", "push for review"
- On a feature branch with uncommitted or unpushed changes
- No PR exists for the current branch

→ See `./creating-workflow.md`

### Use Reviewing Workflow when:
- User asks to "review PR", "check code quality", "run review"
- PR exists and is open
- Want to run code review agents before merge

→ See `./reviewing-workflow.md`

### Use Merging Workflow when:
- User asks to "merge PR", "complete PR", "finalize changes"
- PR exists, is reviewed, and ready for merge
- Need to run final CI checks and merge

→ See `./merging-workflow.md`

## Quick Reference

| Intent      | Workflow  | Key Actions                                                 |
| ----------- | --------- | ----------------------------------------------------------- |
| "Create PR" | Creating  | Branch → Commit → Push → `gh pr create`                     |
| "Review PR" | Reviewing | Identify PR → Run review agents → Fix issues → Update state |
| "Merge PR"  | Merging   | CI checks → Confirm ready → `gh pr merge` → Checkout main   |
