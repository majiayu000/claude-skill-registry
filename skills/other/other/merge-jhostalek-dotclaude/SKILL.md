---
name: merge
description: Use when the user asks to merge another branch into the current branch, pull upstream changes without rebasing, or resolve merge conflicts.
argument-hint: "[target-branch] (defaults to master/main)"
---
input = $ARGUMENTS

Merge a target branch into the current feature branch. Goal: incorporate upstream changes, resolve conflicts, push cleanly. Preserves branch topology — no history rewrite.

## When to Merge (vs Rebase)

Merge when: long-lived branches, shared branches with multiple contributors, mid-work sync where rewrite risk outweighs clean history, or when the user explicitly requests merge. The merge commit documents when integration happened.

## Repo Identification

Resolve repo topology before any git operations — submodule working directories can hijack `git rev-parse`. Run `git rev-parse --show-toplevel` and `git remote -v` explicitly for each repo (parent and each submodule) using `--git-dir` / `--work-tree` flags or `-C` to avoid ambient directory confusion. Confirm which repo each shell command targets on every invocation.

## Submodule Coordination

The parent repo stores submodule SHAs — merging the parent first may reference stale submodule SHAs. Merge submodules first, then the parent. Push in the same order.

Merge a submodule only when it has its own feature branch. Submodules on detached HEAD at a pinned commit are dependencies — leave them alone.

After parent merge completes, amend the merge commit to reference the updated submodule HEAD: `git add {submodule} && git commit --amend -m "chore: merge {target} into {current-branch}"`.

## Conflict Resolution

**Heuristics:**
- **Lockfiles, migrations, config, version bumps** — accept the target branch version (latest agreed-upon state), then regenerate lockfiles if applicable.
- **Submodule pointer conflicts** — accept the target's ref (`git checkout MERGE_HEAD -- {submodule}`). The correct ref is set after the submodule merge.
- **Refactored-away code** — the target's removal wins. Rewire to the new location/API.
- **Additive conflicts** (both sides add independent code) — keep both, but verify structural integrity: run the project's formatter/parser immediately after resolution. Conflict boundaries often leave orphan closing tags, duplicate brackets, or stray blocks that grep won't catch but a parser will.

**Partial survival check:** When a resolution keeps *usage* of a symbol (component, function, import), verify the *declaration* and *import* also survived. Grep the resolved file for every feature-side symbol before continuing.

## Migration Reconciliation

Merge creates a single merge commit but does NOT execute the target's new migrations against the local database. The DB version marker still holds the old revision, so the app crashes at runtime on missing schema objects.

**Re-chain:** Update the feature migration's parent revision to point to the target's chain tip. Update any declared head tracking (if the project tracks migration head outside alembic — check project CLAUDE.md/TOOLS.md).

**Apply to local DB:** Check the DB's current migration version first. If it's already at the target's tip, only the feature migration needs applying. If it's at the feature's old pre-merge revision, stamp to the fork point first (stamp moves the pointer without executing destructive down-migrations), then upgrade.

## Flow

1. **Identify repos.** Confirm git roots, branches, remotes for parent and each submodule.
2. **Fetch target.** `git fetch origin {target}` — ensure merge base is current.
3. **Present merge plan.** Which repos, divergence (commits ahead/behind), target branch. Start after presenting.
4. **Merge submodules first**, then parent. Use `git merge origin/{target}` (merge the remote-tracking branch, not local). Resolve conflicts per heuristics above. Run formatter/parser after each conflict resolution to catch structural damage early.
5. **Amend parent merge commit** to reference updated submodule SHAs if applicable.
6. **Reconcile migrations** if any migration files were touched (re-chain + apply to local DB if running).
7. **Run quality gates** — use the project's gate commands from TOOLS.md. Run from the correct working directory for each repo.
8. **Push** — submodules first, then parent. Standard push (no force needed — merge doesn't rewrite history). Invoking `/merge` is intent to push; no additional confirmation needed.

## Merge Commit Message

Many projects enforce conventional commit format via pre-commit hooks. The default git merge message (`Merge branch 'X' into Y`) will be rejected by these hooks. Always use a conventional commit message for merge commits:

```
chore: merge {target} into {current-branch}
```

Pass the message explicitly: `git merge origin/{target} -m "chore: merge {target} into {current-branch}"`. For conflict resolutions that require a separate `git commit` after staging, use the same format. If conflicts were resolved or notable decisions made, add a brief summary to the commit body.

**Report:** repos merged, commits integrated, conflicts resolved, migration reconciliation results, quality gate results.
