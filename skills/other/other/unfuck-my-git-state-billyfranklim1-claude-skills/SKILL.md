---
name: unfuck-my-git-state
description: Diagnose and recover broken Git state and worktree metadata with a staged, low-risk recovery flow. Use when Git reports detached HEAD, phantom worktree locks, orphaned entries, missing refs, or branch operations fail.
---

# unfuck-my-git-state

Recover a repo without making the blast radius worse.

## Core Rules

1. Snapshot first. Do not "just try stuff."
2. Prefer non-destructive fixes before force operations.
3. Treat `.git/` as production data until backup is taken.
4. Use `git symbolic-ref` before manually editing `.git/HEAD`.
5. After each fix, run verification before proceeding.

## Playbook A: Orphaned Worktree Metadata

Symptoms: `git worktree list` shows a path that no longer exists; invalid or zero hashes.

```bash
git worktree list --porcelain
git worktree prune -v
git worktree list --porcelain
```

If stale entries remain, back up `.git/` and remove the specific stale folder under `.git/worktrees/<name>`, then rerun prune.

## Playbook B: Phantom Branch Lock

Symptoms: `git branch -d` fails with "already used by worktree".

```bash
git worktree list --porcelain
```

Find the worktree using that branch, switch that worktree to another branch or detach HEAD there, then retry.

## Playbook C: Detached or Contradictory HEAD

Symptoms: `git status` says detached HEAD unexpectedly.

```bash
git symbolic-ref -q HEAD || true
git reflog --date=iso -n 20
git switch <known-good-branch>
# or create rescue branch:
git switch -c rescue/$(date +%Y%m%d-%H%M%S)
```

## Playbook D: Missing or Broken Refs

Symptoms: `unknown revision`, `not a valid object name`, `cannot lock ref`.

```bash
git fetch --all --prune
git show-ref --verify refs/remotes/origin/<branch>
git branch -f <branch> origin/<branch>
git switch <branch>
```

## Last Resort: Manual HEAD Repair

Only after backup of `.git/`.

```bash
git show-ref --verify refs/heads/<branch>
git symbolic-ref HEAD refs/heads/<branch>
# fallback:
echo "ref: refs/heads/<branch>" > .git/HEAD
```

## Verification Gate (Must Pass)

- `git status` exits cleanly with no fatal errors.
- `git symbolic-ref -q HEAD` matches intended branch.
- `git worktree list --porcelain` has no missing paths and no zero hashes.
- `git fsck --no-reflogs --full` has no new critical errors.

## Escalation Path

```bash
tar -czf git-metadata-backup-$(date +%Y%m%d-%H%M%S).tar.gz .git
# Clone fresh from remote, recover with reflog + cherry-pick
```
