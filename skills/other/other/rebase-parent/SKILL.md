---
name: rebase-parent
description: Rebase the current branch onto an updated parent PR branch. Use when you have stacked PRs and the parent branch has been updated (force-pushed after its own rebase or new commits added).
---

# Rebase onto Updated Parent Branch

Rebase the current branch onto a parent branch that has been updated.

## Usage

```
/rebase-parent
/rebase-parent feature/parent-branch    # Explicit parent branch
```

## Instructions

### 1. Identify Parent Branch

If not provided, try to determine the parent:

```bash
# Get current branch
git branch --show-current

# Check PR base branch
gh pr view --json baseRefName --jq '.baseRefName'
```

If the base is `main`, this skill doesn't apply - use `/rebase-main` instead.

Ask the user to confirm the parent branch if uncertain.

### 2. Check Current State

```bash
# Check for uncommitted changes
git status --porcelain

# Get current branch
git branch --show-current
```

Stash or commit uncommitted changes before proceeding.

### 3. Fetch Latest Parent

```bash
git fetch origin {parent-branch}
```

### 4. Find the Fork Point

The tricky part with rebasing onto an updated parent is finding where your branch originally diverged. If the parent was rebased, the old base commits are gone.

```bash
# Get the merge base (may be outdated if parent was rebased)
git merge-base HEAD origin/{parent-branch}

# Count commits unique to your branch
git rev-list --count origin/{parent-branch}..HEAD
```

### 5. Perform the Rebase

Use `--onto` to rebase only your commits onto the new parent:

```bash
# Find how many commits are yours (after the original fork point)
# Then rebase those commits onto the updated parent

git rebase --onto origin/{parent-branch} $(git merge-base HEAD origin/{parent-branch}) HEAD
```

If that doesn't work cleanly (merge-base is stale), try:

```bash
# Interactive rebase to select only your commits
git rebase -i origin/{parent-branch}
```

### 6. Handle Conflicts

If conflicts occur:

1. List conflicting files: `git diff --name-only --diff-filter=U`
2. Resolve each conflict
3. Stage resolved files: `git add {file}`
4. Continue: `git rebase --continue`

If stuck, abort and ask for guidance: `git rebase --abort`

### 7. Force Push

```bash
git push --force-with-lease
```

### 8. Update PR Base (if needed)

If the PR base branch needs updating:

```bash
gh pr edit --base {parent-branch}
```

### 9. Report Result

Inform the user:
- Successfully rebased X commits onto {parent-branch}
- Conflicts resolved (if any)
- Force pushed to origin
