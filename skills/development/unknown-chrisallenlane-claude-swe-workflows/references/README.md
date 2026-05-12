# /tidy-git — Mechanical Repo Hygiene

## Overview

The `/tidy-git` skill cleans up local git state that accumulates over time. It runs zero-risk operations automatically, asks before deleting merged local branches, and reports (without acting on) other state worth knowing about — stashes, untracked files, unpushed work, local-only tags.

The skill is in the `/tidy-*` namespace because the find→fix seam is small: detecting a stale remote-tracking ref and removing it is essentially one operation. Adding a review-and-approve step for every mechanical detail would turn a 5-second cleanup into a 5-minute interactive session. The skill therefore *defaults to action* on safe categories; operator approval is reserved for the borderline-safe operations where a preview is genuinely useful (merged-branch deletion).

**Scope:** local repo only. The skill never pushes, never force-pushes, never deletes anything on the remote. It also never deletes unmerged work, the current branch, or the main branch. It never `gc`s. It never `git clean`s. It never drops stashes or local tags.

**Key benefits:**
- One pass replaces several manual commands (`git remote prune`, `git worktree prune`, listing merged branches, scanning stashes, comparing tags).
- Surfaces forgotten state the user wouldn't think to look for (orphaned stashes, branches with no upstream, local-only tags).
- Categorical safety invariants prevent destructive defaults — no escape hatches.
- Reversibility-friendly: branches deleted by the skill are recoverable from `git reflog` for ~90 days.

## When to Use

**Use `/tidy-git` for:**
- After a release or major merge, when feature branches have piled up.
- Before a long-running session, to start from a clean baseline.
- When `git branch` shows more than you can mentally track.
- As a periodic hygiene pass (e.g., monthly, or whenever the repo feels cluttered).

**Don't use `/tidy-git` for:**
- Remote-side cleanup (deleting remote branches, pruning the remote tag set) — use the platform UI or `git push --delete` explicitly.
- Rewriting history (force-push, interactive rebase to clean up commits) — use the underlying git commands explicitly, never automated.
- Removing untracked files (`git clean`) — the skill reports them but does not delete.
- Dropping stashes — the skill reports them but does not delete.

**Rule of thumb:** if the action affects only local refs and is reversible from the reflog, `/tidy-git` handles it. If the action affects the remote, history, or unrecoverable local state, run the underlying git command yourself.

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ /tidy-git Workflow                                              │
└─────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  1. DETECT REPO CONTEXT                      │
 │  ────────────────────────────────────────    │
 │  • Confirm git repo                          │
 │  • Detect main branch (origin/HEAD → main →  │
 │    master → ask user)                        │
 │  • Detect current branch                     │
 │  • Note working-tree state (info only)       │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  2. ZERO-RISK AUTO-OPERATIONS                │
 │  ────────────────────────────────────────    │
 │  • git remote prune <remote>                 │
 │  • git worktree prune                        │
 │  (these remove only refs, never commits)     │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  3. INVENTORY BORDERLINE-SAFE OPERATIONS     │
 │  ────────────────────────────────────────    │
 │  Merged local branches (excluding main +     │
 │  current); record SHAs for reflog recovery   │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  4. INVENTORY INFORMATIONAL STATE            │
 │  ────────────────────────────────────────    │
 │  • Stashes (age + message)                   │
 │  • Branches with no upstream                 │
 │  • Branches ahead of upstream                │
 │  • Local-only tags                           │
 │  • Untracked files (sample of 10)            │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  5. PREVIEW + CONFIRM BRANCH DELETION        │
 │  ────────────────────────────────────────    │
 │  Show merged branches with SHA / date /      │
 │  last commit message.                        │
 │  Operator: delete all / select / keep all    │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  6. EXECUTE APPROVED DELETIONS               │
 │  ────────────────────────────────────────    │
 │  git branch -d <name>  (safe, never -D)      │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  7. FINAL SUMMARY                            │
 │  ────────────────────────────────────────    │
 │  • Cleaned (counts + recovery hint)          │
 │  • Worth reviewing (informational state)     │
 └──────────────────────────────────────────────┘
```

## The Three Action Tiers

The skill's defining design choice is the three-tier action model. Every operation falls into exactly one tier:

### Tier 1 — Zero-risk: just do it

These operations remove only *references*. They cannot lose commits, objects, or files. They run without operator confirmation because there is nothing to confirm.

| Operation                                | Command                       | What it removes                                              |
|------------------------------------------|-------------------------------|--------------------------------------------------------------|
| Prune stale remote-tracking refs         | `git remote prune <remote>`   | Local refs under `refs/remotes/<remote>/` for branches that no longer exist on the remote |
| Prune stale worktree refs                | `git worktree prune`          | References to worktrees whose directories are already gone   |

### Tier 2 — Borderline-safe: preview, confirm, then do

Operations that delete *references with associated commits*. Reversible from the reflog (90 days), but worth previewing.

| Operation                          | Command                            | Safety                                                       |
|------------------------------------|------------------------------------|--------------------------------------------------------------|
| Delete merged local branch         | `git branch -d <name>` (lowercase) | `-d` refuses to delete if the branch isn't actually merged; this guards against rare `--merged` false positives. No `-D` fallback. |

### Tier 3 — Real loss risk: report only

State that *might* warrant cleanup, but the cleanup is judgment-laden or hard to reverse. The skill reports these so the operator can decide; it never acts on them.

| Category                         | Why report-only                                                                        |
|----------------------------------|----------------------------------------------------------------------------------------|
| Stashes                          | A stash is by definition undecided work; auto-dropping violates reversibility          |
| Branches with no upstream        | May be intentional local-only work or forgotten branches; operator knows which         |
| Branches ahead of upstream       | Forgotten pushes — operator decides whether to push, abandon, or keep working          |
| Local-only tags                  | Often intentional backups (e.g., `pre-rebase-backup-*`) — operator knows the intent    |
| Untracked files                  | `git clean` is destructive and context-dependent; `/pre-compact` handles session-trash |

## Why `--merged` Doesn't Catch Everything

The Tier-2 merged-branch detection uses `git branch --merged <main>`. This catches branches whose tip commit is reachable from the main branch — i.e., branches merged via plain merge or fast-forward.

**It does NOT catch:**
- **Squash-merged branches.** GitHub's "Squash and merge" creates a *new* commit on main with a different SHA. The original branch's tip is not reachable from main, so `--merged` misses it.
- **Rebase-merged branches.** Rebasing changes the SHAs. Same problem.

These branches surface in the "Branches ahead of upstream" informational category instead. The operator sees them with their per-branch commit count and decides — typically deleting them manually with `git branch -D` after confirming the work is on main.

The skill deliberately does *not* try to be smart about squash/rebase detection. Heuristics (e.g., "the branch's tree matches a commit on main") produce false positives, and a wrong delete on a squash-merge-looking branch could lose work that was never actually merged. Reporting these informationally and letting the operator decide is safer.

## Recovery from a Wrong Delete

Branches deleted by `/tidy-git` are recoverable from the reflog for ~90 days (the default `gc.reflogExpire`). The final summary always includes the deleted branch SHAs for exactly this reason.

To recover:

```
git reflog | grep <branch-name>
# or, if the branch SHA was captured in the summary:
git branch <branch-name> <sha>
```

If the reflog has already been pruned (the branch was deleted >90 days ago or `git gc` was run with reduced `gc.reflogExpire`), the work may be unrecoverable through normal means. This is why `/tidy-git` uses `-d` (safe) rather than `-D` (force) — the skill won't let you delete an unmerged branch by accident, where reflog recovery would be more critical.

## Safety Invariants (Categorical)

These are categorical, not configurable. The skill does not offer flags to override them. If the user wants any of these operations, they invoke `git` directly:

- Never delete the main branch.
- Never delete the current branch.
- Never use `git branch -D` (force delete).
- Never run `git push`, `git push --force`, `git push --delete`, or any operation affecting the remote.
- Never run `git stash drop` or `git stash clear`.
- Never run `git tag -d`.
- Never run `git clean` to remove untracked files.
- Never run `git gc` (Git's `gc --auto` handles object-database maintenance when needed).

The principle: a "tidy" skill must be safer than the underlying `git` commands it composes. If the user wants destructive operations, the friction of typing the command yourself is the safety mechanism.

## Tips for Effective Use

1. **Run after every merge to master.** The merge creates a flurry of stale state: the feature branch is now mergeable to nothing, the remote may have deleted its copy, the local upstream tracking ref points at nothing useful. One `/tidy-git` pass cleans all of it.

2. **Don't fight the report-only categories.** If `/tidy-git` reports 8 untracked files in your repo, the right next step is `git status` or `/pre-compact`, not running `/tidy-git` again expecting different behavior. The categories are deliberately different tiers.

3. **The "branches ahead of upstream" report catches forgotten pushes.** A common pattern: feature branch is merged via squash-merge on GitHub, but locally the branch still has its original (non-squashed) commits, which are "ahead of upstream" on the now-deleted-but-still-tracked remote. That's the signal that the branch should be deleted manually with `-D`.

4. **Keep the backup-tag convention.** Tags like `pre-rebase-backup-2026-05-11` are valuable safety nets during destructive operations. `/tidy-git` reports them as local-only-tags rather than deleting them because they're often deliberate. Drop them yourself with `git tag -d` once the underlying operation is verified successful.

5. **Stash hygiene is a separate exercise.** `/tidy-git` reports your stash list; it never drops. If you have stashes older than a few weeks, take a few minutes to review them — most are probably abandoned, but the few that aren't are worth recovering. `git stash list --date=relative` and `git stash show -p stash@{N}` are the underlying commands.

## Example Session

See the [SKILL.md](../SKILL.md#example-session) for a full worked example.

## Edge Cases and Failure Modes

**No remote configured.** The `git remote prune` step is skipped with an informational note. The rest of the workflow continues.

**Multiple remotes configured.** Each remote is pruned in turn. The summary reports the count per remote.

**Repo is mid-rebase / mid-merge / mid-cherry-pick.** The skill aborts cleanly and asks the user to resolve the in-progress operation first. Repo hygiene during a half-applied operation is unsafe.

**`origin/HEAD` is not set.** The main-branch detection falls back to checking for `main`, then `master`, then asks the user. To avoid the prompt in future runs, set the symbolic ref:

```
git remote set-head origin <main-branch-name>
```

**Detached HEAD.** The current-branch detection returns empty. The skill treats this as "no current branch to protect" and proceeds normally — though if you're in detached HEAD because of a checkout, the in-progress work is more relevant than the cleanup. Consider whether `/tidy-git` is the right thing to be doing right now.

**No merged branches.** Tier 2 is skipped entirely; no preview prompt. The summary still reports Tier 1 cleanups and Tier 3 informational state.

**Operator declines all deletions ("Keep all").** Tier 2 commits no changes; only Tier 1 cleanups land. The summary reflects this honestly — "0 merged branches deleted."

**`git branch -d` fails on a branch in the preview list.** Surface the failure inline (e.g., "feat/foo: branch is not fully merged — skipping"), continue with the rest of the list, and note the skip in the summary. Never fall back to `-D`.
