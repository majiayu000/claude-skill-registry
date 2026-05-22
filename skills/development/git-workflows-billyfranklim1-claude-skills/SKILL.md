---
name: git-workflows
description: Advanced git operations beyond add/commit/push. Use when rebasing, bisecting bugs, using worktrees, recovering with reflog, resolving merge conflicts, cherry-picking across branches, or working with monorepos.
---

# Git Workflows

Advanced git operations for real-world development.

## Interactive Rebase

```bash
git rebase -i HEAD~5
git rebase -i main
# Commands: pick / reword / edit / squash / fixup / drop
git commit --fixup=a1b2c3d
git rebase -i --autosquash main
git rebase --abort
```

## Bisect

```bash
git bisect start
git bisect bad
git bisect good v1.2.0
git bisect good / bad  # per commit
git bisect reset
git bisect run ./test-for-bug.sh
```

## Worktree

```bash
git worktree add ../myproject-hotfix hotfix/urgent-fix
git worktree add ../myproject-feature -b feature/new-thing
git worktree list
git worktree remove ../myproject-hotfix
git worktree prune
```

## Reflog

```bash
git reflog
git reflog show feature/my-branch
git reset --hard ghi789
git branch recovered-branch abc123
git reset --hard HEAD@{2}
```

## Cherry-Pick

```bash
git cherry-pick abc123
git cherry-pick abc123 def456 ghi789
git cherry-pick --no-commit abc123
git remote add upstream https://github.com/other/repo.git
git fetch upstream
git cherry-pick upstream/main~3
git cherry-pick --continue
git cherry-pick --abort
```

## Conflict Resolution

```bash
git checkout --ours path/to/file.ts && git add path/to/file.ts
git checkout --theirs path/to/file.ts && git add path/to/file.ts
git show :1:path/to/file.ts   # base
git show :2:path/to/file.ts   # ours
git show :3:path/to/file.ts   # theirs
```

## Stash Patterns

```bash
git stash push -m "WIP: refactoring auth flow"
git stash push -m "partial stash" -- src/auth.ts
git stash push -u -m "with untracked"
git stash branch new-feature stash@{0}
```

## Tags and Releases

```bash
git tag -a v1.2.0 -m "Release 1.2.0"
git push origin v1.2.0
git push origin --tags
git tag -d v1.2.0
git push origin --delete v1.2.0
```

## Log Archaeology

```bash
git log -S "function oldName" --oneline
git log -G "TODO.*hack" --oneline
git log --follow --oneline -- src/new-name.ts
git blame -L 50,70 src/auth.ts
git blame -w src/auth.ts
```

## Tips

- `git rebase -i` is the single most useful advanced git command.
- Never rebase commits pushed to a shared branch.
- `git reflog` is your safety net — commits recoverable within 90 days.
- Enable `rerere` globally: `git config --global rerere.enabled true`
- `git stash push -m "description"` is much better than bare `git stash`.
- Worktrees are cheaper than multiple clones — they share `.git` storage.
