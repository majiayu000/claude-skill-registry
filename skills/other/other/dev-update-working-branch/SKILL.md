---
name: dev-update-working-branch
description: Update the current working branch with the latest main. Fetches origin/main, updates local main, and merges main into the current branch.
user-invokable: true
---

Update the current working branch with the latest changes from main.
Fetches `origin/main`, fast-forwards local `main`, and merges `main`
into the current feature branch.

## When to use

- Before pushing fixes during `/dev-review-pr` when the branch is behind
- Before running `/dev-resolve-feedback` (must update before resolving)
- Any time GitHub shows the branch is behind main
- Before creating a PR to minimize merge conflicts

## Workflow

### 1. Verify on a feature branch

```bash
BRANCH=$(git branch --show-current)
```

If on `main`, report "Already on main — use `git pull` instead" and stop.

Check for uncommitted or untracked changes:

```bash
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

If the output is non-empty, report "Uncommitted changes detected — commit
or stash before updating" and stop. This catches tracked modifications,
staged changes, and untracked files (which can cause "would be overwritten
by merge" errors).

### 2. Fetch and update local main

```bash
git fetch origin main
git branch -f main origin/main
```

This updates local `main` to match `origin/main` without switching
branches. The `-f` flag forces the update (safe because we are not on
`main`).

### 3. Merge main into the current branch

```bash
git merge main --no-edit
```

If there are merge conflicts, report them and stop — the user must
resolve manually.

### 4. Report result

```text
Updated <branch-name> with latest main.
- Fetched origin/main
- Local main updated to <commit>
- Merged into <branch-name>
- <N> new commits from main

Push when ready: git push
```

If the merge was a no-op (already up to date), report that instead.

## What it does NOT do

- It does NOT push — the user decides when to push
- It does NOT switch to main — stays on the current branch
- It does NOT rebase (merge preserves history and avoids force-push)
- It does NOT resolve conflicts — reports them for manual resolution

## Safety

- Refuses to run if on `main` (nothing to merge into)
- Refuses to run if there are uncommitted changes (merge would fail)
- Uses merge, not rebase, so no force-push is needed
- Does not modify remote state
