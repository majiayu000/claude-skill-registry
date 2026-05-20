---
name: clean-all
description: Delete all non-main branches (local + remote) and prune stale refs
user-invocable: true
disable-model-invocation: true
---
Clean up all branches except main, locally and remotely.

1. Run `git remote prune origin` to remove stale remote tracking refs.
2. Delete all local branches except `main`: `git branch | grep -v "main" | xargs git branch -D`
3. Delete all remote branches except `main`: `git branch -r | grep -v "origin/main\|origin/HEAD" | sed 's|origin/||' | xargs -I{} git push origin --delete {}`
4. Remove any `.claude/worktrees/*` directories: `git worktree remove` each, then delete leftover empty dirs.
5. Verify with `git branch -a` and `ls .claude/worktrees/` — only `main` should remain.
6. Report summary: how many local branches, remote branches, and worktrees were cleaned up.

If everything is already clean, just say so.
