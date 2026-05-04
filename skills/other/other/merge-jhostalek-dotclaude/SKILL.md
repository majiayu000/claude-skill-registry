---
name: merge
description: Use when the user asks to merge another branch into the current branch, pull upstream changes without rebasing, or resolve merge conflicts.
argument-hint: "[target-branch] (defaults to master/main)"
---
input = $ARGUMENTS

Merge a target branch into the current feature branch.

## Repo Identification

Submodule working directories hijack `git rev-parse` through ambient-directory inference. Resolve topology explicitly with `-C <path>` (or `--git-dir` / `--work-tree`) on every invocation for parent and each submodule.

## Submodule Coordination

Merge submodules first so the parent merge references current pointers; push in the same order. After the parent merge completes, amend it to capture updated submodule HEADs:

```
git add {submodule} && git commit --amend -m "chore: merge {target} into {current-branch}"
```

Merge a submodule only when it has its own feature branch. Submodules on detached HEAD at a pinned commit are dependencies — leave them alone.

Use `git merge origin/{target}` (remote-tracking ref, not local branch).

## Conflict Resolution

- **Lockfiles, migrations, config, version bumps** — accept the target version (latest agreed state), then regenerate lockfiles.
- **Submodule pointer conflicts** — accept the target's ref (`git checkout MERGE_HEAD -- {submodule}`); the correct ref is set after the submodule merge.
- **Refactored-away code** — target's removal wins; rewire to the new location/API.
- **Additive conflicts** (both sides add independent code) — keep both, then run the project's formatter/parser. Conflict boundaries leave orphan closing tags, duplicate brackets, and stray blocks that grep misses but a parser catches.

**Partial survival:** when a resolution keeps *usage* of a symbol, verify the *declaration* and *import* also survived. Grep the resolved file for every feature-side symbol before continuing.

## Migration Reconciliation

Merge produces a merge commit but does NOT execute the target's new migrations against the local database. The DB version marker still holds the old revision — the app crashes at runtime on missing schema objects.

**Re-chain:** update the feature migration's parent revision to point to the target's chain tip. Update declared head tracking if the project tracks migration head outside alembic (check project CLAUDE.md/TOOLS.md).

**Re-ID if non-monotonic.** Re-pointing `down_revision` alone is not sufficient. If the feature's own revision ID is now ≤ any upstream ID in the new chain, the chain violates monotonic-timestamp rules and silently breaks any DB already stamped at that ID — alembic reports head, skips the inserted middle, app crashes on missing columns. Fix: generate a fresh `date +%Y%m%d%H%M%S`, update `revision: str = …` inside the file, rename the file to match, update project head tracking.

**Verify chain:** run `alembic history` and confirm revision IDs are non-decreasing along the chain.

**Apply to local DB:**
- DB at target's tip → only the feature migration needs applying.
- DB at feature's old pre-merge revision → stamp to the fork point (stamp moves the pointer without executing destructive down-migrations), then upgrade.
- DB stamped at the feature revision but upstream migrations between fork and feature were inserted later → re-running the feature crashes. Stamp back to the fork point, `upgrade <last-upstream-rev>` (not `head`), then `stamp <feature-rev>`.

## Merge Commit Message

Pre-commit hooks often reject the default `Merge branch 'X' into Y`. Use conventional commit format and pass it explicitly:

```
git merge origin/{target} -m "chore: merge {target} into {current-branch}"
```

Same format for follow-up `git commit` after staging conflict resolutions. Notable decisions go in the commit body.

## Execution

Announce the merge plan before starting — repos involved, divergence (commits ahead/behind), target branch. Invoking `/merge` is intent to push; no confirmation needed after the plan. Run `/qg` from each repo's working directory before pushing.

**Report:** repos merged, commits integrated, conflicts resolved, migration reconciliation, gate results.
