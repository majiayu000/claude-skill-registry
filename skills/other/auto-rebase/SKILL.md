---
name: auto-rebase
description: Rebase feature branches onto target, resolve conflicts, and keep PRs up-to-date with force-push
category: Git
---

# Skill: auto-rebase

## What I do
Automate rebasing feature branches onto their target branch (typically `next`), resolving conflicts, and force-pushing to keep PRs current. Works with both regular branches and git worktrees.

## When to use me
- PR shows "Not up to date" with target branch
- Before pushing review feedback fixes to avoid merge conflicts
- Before merging as a pre-merge checklist step
- After target branch has received new commits
- When CI fails due to branch divergence

## Core principles
1. **Always rebase, never merge** — Keep linear history.
2. **Use `--force-with-lease`** — Never bare `--force` as this protects against overwriting others' pushes.
3. **Rebase onto remote target** — Always `git fetch` first, then rebase onto `origin/{target}` rather than a local branch.
4. **Worktree-aware** — When using a bare repo with worktrees, fetch in the correct worktree context.
5. **Test after rebase** — Always verify tests pass after rebasing before pushing.

## Patterns & examples

**Standard rebase workflow:**
```bash
# Determine target branch from PR
TARGET=$(gh pr view {PR} --json baseRefName -q '.baseRefName')

# Fetch latest and rebase
git fetch origin $TARGET
git rebase origin/$TARGET

# Verify nothing broke
make test
make vet

# Force-push with lease (safe force)
git push --force-with-lease
```

**Rebase with conflict resolution:**
```bash
git fetch origin next
git rebase origin/next

# If conflicts occur:
# 1. Fix conflicts in affected files
# 2. Stage resolved files: git add <file>
# 3. Continue: git rebase --continue
# 4. If stuck: git rebase --abort (start over)
```

**Worktree-specific rebase (bare repo setup):**
```bash
# In a worktree like /home/user/Projects/Repo/feature-branch
git fetch origin next
git rebase origin/next
git push --force-with-lease
```

**Automated rebase check (before push):**
```bash
# Check if branch is behind target
BEHIND=$(git rev-list --count HEAD..origin/next)
if [ "$BEHIND" -gt "0" ]; then
    echo "Branch is $BEHIND commits behind next — rebasing..."
    git rebase origin/next
fi
```

## Anti-patterns to avoid
- ❌ `git merge origin/next` — Creates merge commits and non-linear history.
- ❌ `git push --force` — Can overwrite collaborator's pushes; use `--force-with-lease`.
- ❌ Rebasing without fetching — Rebases onto a stale local branch.
- ❌ Pushing without testing after rebase — Rebase can introduce subtle failures.
- ❌ Rebasing shared/public branches (main, next) — Only rebase feature branches.

## KB Reference
`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Git/Auto Rebase.md`

## Related skills
- `git-advanced` — Advanced git operations including rebasing
- `git-master` — Commit strategy and history management
- `create-pr` — PR creation workflow that sets up clean branches
- `pre-merge` — Final validation that includes rebase check
- `respond-to-review` — Review response workflow that includes rebasing
