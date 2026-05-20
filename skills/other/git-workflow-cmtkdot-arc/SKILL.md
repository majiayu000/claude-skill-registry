---
name: git-workflow
description: Use when performing any git operation in Arc. Defines safety rails, pre-push verification, branch naming, and session completion criteria.
invocation: agent
---

# Git Workflow

Enforce safety rails for all git operations within Arc. These rules apply to every tier (Simple, Standard, Full) and every execution mode (loop, swarm, team).

## Safety Rails

### 1. No Destructive Reset by Default

Never run `git reset --hard`, `git checkout .`, `git clean -f`, or `git restore .` without explicit user confirmation. These commands discard work that may not be recoverable. If a rollback is needed, prefer creating a new commit that reverts changes.

### 2. No Force-Push to Protected Branches

Never `git push --force` to `main`, `master`, `develop`, or any branch matching `release/*` or `hotfix/*`. Force-push rewrites shared history and can destroy teammates' work. If a rebase is needed on a protected branch, surface the issue and let the user decide.

### 3. No Automatic Rebase of Shared History

Do not rebase branches that have been pushed to a remote unless the user explicitly requests it. Rebasing shared branches rewrites commit hashes that others may depend on. Prefer merge commits for shared branches.

### 4. Pre-Push Verification

Before any push, run these checks in order:
1. **Tests** — Run the project's test suite. All tests must pass.
2. **Lint** — Run the project's linter. No errors allowed (warnings are acceptable).
3. **Typecheck** — Run the type checker if the project uses one. Zero errors.
4. **Build** — Run the build if applicable. Must succeed.

If any check fails, do not push. Fix the issue first.

### 5. Scoped and Traceable Commits

Keep commits focused on a single bead or logical change. Each commit message should reference the bead ID or task it completes. Avoid large commits that bundle unrelated changes — they make rollback and bisect difficult.

### 6. OpenSpec/Beads Sync

Keep specification artifacts in sync with code changes. When code changes complete a bead, update the bead state in the same commit or immediately after. Specification drift creates confusion about what is actually done.

## Worktree Safety Rails

### 7. No Force-Delete of Worktrees with Uncommitted Changes

Never run `git worktree remove --force` on a worktree that has uncommitted changes. Check `git status` inside the worktree first. If uncommitted changes exist, commit or stash them before removal.

### 8. Verify Gitignore Before Project-Local Creation

Before creating a project-local worktree directory (`.worktrees/`, `worktrees/`), verify it is git-ignored using `git check-ignore -q`. If not ignored, add it to `.gitignore` and commit before proceeding. External worktree directories (outside the repo) do not require this check.

### 9. Worktree Branch Naming

Worktree branches follow the `arc/<bead-id>` naming convention. Do not reuse existing branch names or create branches without the `arc/` prefix for bead worktrees.

### 10. Merge-Back with History Preservation

Merge worktree branches back into the baseline using `--no-ff` to preserve bead-scoped history in the merge graph. This ensures each bead's work is visible as a distinct merge commit for traceability and bisect.

### 11. Post-Execution Cleanup

After execution completes, remove all worktrees and prune stale references:

```bash
git worktree remove <worktree-root>/<bead-id>
git branch -d arc/<bead-id>
git worktree prune
```

Never leave worktrees behind after execution completes. Stale worktrees consume disk and create confusion about active work.

## Completion Criteria

An Arc session is not complete until:
- All exit criteria commands pass
- All changes are committed with proper messages
- Push to remote succeeds

If push cannot succeed (network issues, CI failures), the user must explicitly defer completion. Do not silently end a session with unpushed changes.

## Branch Naming

When creating branches for Arc work, use descriptive names:
- `arc/<tier>/<brief-description>` — e.g., `arc/standard/add-auth-flow`
- Include the tier to signal the expected scope of the branch

## Related Skills

- `plan-schema` defines the exit criteria that must pass before push.
- `beads-schema` defines the bead IDs referenced in commit messages.
- `worktree` defines the worktree lifecycle, directory selection, and merge-back strategy.
- All execution skills (`loop`, `swarm`, `team`) must respect these git rules.
