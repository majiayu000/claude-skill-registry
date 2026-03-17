---
name: squash-commits
description: Review all changes (commits and working changes) and organize into appropriate commit granularity
disable-model-invocation: true
---

# Squash Commits

Organize all changes into well-structured commits.

## Steps

### 1. Review the current state

```bash
git status
git diff
git diff --staged
git log origin/main..HEAD --oneline
git log origin/main..HEAD
```

### 2. Analyze and determine optimal commit structure

- Group related changes across commits and working directory
- Identify logical units that should be separate commits
- Consider proper commit granularity (one logical change per commit)
- Determine which changes should be combined or split
- Decide on clear, descriptive commit messages for each logical unit

### 3. Execute the reorganization

- If there are working changes, create temporary commits or stash them
- Use interactive rebase to reorganize existing commits
- Apply working changes to appropriate commits using `git commit --amend` or as new commits
- Ensure the final commit history is clean and logical
- Show the final result after completion

This command automatically restructures commits based on optimal commit granularity without requiring user approval.
