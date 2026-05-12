---
name: tidy-git
description: Mechanical git repo hygiene. Prunes stale remote-tracking refs, deletes merged local branches (with confirmation), and reports stashes, untracked files, and unpushed work. Never touches remote state. Safe by default — destructive operations require explicit operator approval.
model: opus
---

# Tidy-Git - Mechanical Repo Hygiene

Cleans up local git state that accumulates over time: remote-tracking refs for branches that no longer exist upstream, local branches that have already been merged, stale worktree references. Surfaces (without acting on) other state worth knowing about: stashes, untracked files, branches with no upstream, branches ahead of upstream, local-only tags.

**Scope of action:** local repo only. The skill never pushes, never force-pushes, never deletes anything on the remote. It also never deletes unmerged work, never deletes the current branch, never deletes the main branch.

**Reversibility note:** branches deleted by this skill can be recovered from `git reflog` for ~90 days. Tags and stashes are not deleted by this skill (the user makes those calls).

## Philosophy

**Tidy, not review.** The user invoked `/tidy-git` because they want cleanup, not analysis. The skill defaults to *doing* the safe operations rather than presenting findings for approval. Operator approval is required only for the borderline-safe operations (merged-branch deletion) where a preview is genuinely useful.

**Find→fix seam stays small.** This skill exists in the `/tidy-*` namespace because the seam between "detect a stale ref" and "delete it" is essentially zero. Adding a review-and-approve step for every mechanical operation would turn a 5-second cleanup into a 5-minute interactive session.

**Boundary respected: local only.** Repo hygiene that touches the remote (e.g., deleting remote branches, force-pushing to clean up history) is out of scope. Those operations have non-local effects and warrant explicit per-action operator decisions, not bundled into a "tidy" workflow.

## Workflow Overview

```
┌──────────────────────────────────────────────────────┐
│                    TIDY-GIT                          │
├──────────────────────────────────────────────────────┤
│  1. Detect repo context (main branch, current        │
│     branch, remote)                                  │
│  2. Run zero-risk auto-operations                    │
│     ├─ Prune remote-tracking refs                    │
│     └─ Prune stale worktree refs                     │
│  3. Inventory borderline-safe operations             │
│     └─ Merged local branches (excluding main +       │
│        current)                                      │
│  4. Inventory informational state                    │
│     ├─ Stashes (with age)                            │
│     ├─ Branches with no upstream                     │
│     ├─ Branches ahead of upstream                    │
│     ├─ Local-only tags                               │
│     └─ Untracked files                               │
│  5. Present preview + confirm for branch deletion    │
│  6. Execute approved deletions                       │
│  7. Final summary                                    │
└──────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Detect Repo Context

Run the following checks before any cleanup:

- **Is this a git repo?** `git rev-parse --is-inside-work-tree`. If not, abort cleanly.
- **What is the main branch?** Try in order: `git symbolic-ref refs/remotes/origin/HEAD` (the canonical answer if `origin/HEAD` is set), then check for `main`, then `master`. If none detected, ask the user.
- **What is the current branch?** `git branch --show-current`. Note for safety checks.
- **Is the working tree clean?** Not a blocker, but worth noting in the summary — it's informational state.

Record the main branch and current branch for safety checks in later steps. These two branches are never deleted by this skill.

### 2. Run Zero-Risk Auto-Operations

These operations remove only *references* — they never delete commits, objects, or files. Run without operator confirmation; they cannot lose work.

**2a. Prune remote-tracking refs.**

```
git remote prune origin
```

Removes local refs under `refs/remotes/origin/` for branches that no longer exist on the remote. Record the count removed.

If the project has multiple remotes, prune each one in turn.

**2b. Prune stale worktree refs.**

```
git worktree prune
```

Removes references to worktrees whose directories have already been deleted from disk. Does not touch worktrees that still exist. Record the count removed.

### 3. Inventory Borderline-Safe Operations

#### Merged local branches

Identify local branches that have been fully merged into the main branch:

```
git branch --merged <main-branch>
```

**Exclude from the list:**
- The main branch itself
- The current branch (`git branch --show-current`)
- Any branch passed as a `--keep` argument by the user (future extension)

For each remaining branch, also record:
- Last commit SHA (so the user can recover via reflog if they regret the delete)
- Last commit date and message (for the preview)
- Whether the branch has an upstream (informational)

**Caveat to surface in the preview:** `git branch --merged` only detects branches whose tip commit is reachable from the main branch. Branches that were merged via *squash-merge* or *rebase-merge* will NOT show up here — their tip commit is different from anything on main. Those branches will surface in step 4's "branches ahead of upstream" category, where the user can decide.

### 4. Inventory Informational State

These are reported but never modified by the skill.

**4a. Stashes.** `git stash list --date=relative`. Record count and the list. Stashes are never deleted by this skill — the user decides if they want to drop or apply.

**4b. Branches with no upstream.** `git for-each-ref --format='%(refname:short) %(upstream)' refs/heads/` and filter for empty upstream. These are local branches that have never been pushed (or whose upstream was deleted without removing the local branch). Surface as informational — they might be intentional local-only work or forgotten branches.

**4c. Branches ahead of upstream.** For each branch with an upstream, check `git rev-list --count <branch>@{u}..<branch>`. If non-zero, the branch has commits not on the remote. Report each with the count of commits ahead. Useful for spotting forgotten pushes.

**4d. Local-only tags.** Compare `git tag` against `git ls-remote --tags origin` (or the configured remote). Tags present locally but not remotely are local-only. These may be intentional backups (e.g., `pre-rebase-backup-*`) and are reported without action. Surface them so the operator can review and drop manually if desired.

**4e. Untracked files.** `git status --porcelain` and filter for untracked. Report count and a representative sample (cap at 10 names; collapse the rest). Not deleted by this skill — `/pre-compact` handles session-trash cleanup with judgment; this skill stays out of that lane.

### 5. Present Preview + Confirm

If step 3 found merged branches eligible for deletion, present them and ask for confirmation:

```
## Branch deletion preview

The following local branches are fully merged into <main> and are
safe to delete. Their SHAs are preserved in git reflog for ~90 days
if you need to recover.

  feat/old-feature        (last commit: 2026-04-15, sha 4a3b2c1)
  fix/typo-readme         (last commit: 2026-04-22, sha 9f8e7d6)
  feat/old-experiment     (last commit: 2026-03-08, sha 1a2b3c4)

Delete all? Select specific? Keep all?
```

Use `AskUserQuestion`. Default to "delete all" since the operator invoked the skill expecting cleanup.

**Three responses:**
- **Delete all** — proceed to step 6 with the full list.
- **Select specific** — operator picks a subset; proceed to step 6 with the selection.
- **Keep all** — skip step 6 and proceed to the summary.

**If step 3 found no merged branches:** skip directly to the summary. No preview needed.

### 6. Execute Approved Deletions

For each approved branch:

```
git branch -d <branch-name>
```

Use the **lowercase `-d`** (safe delete) — it refuses to delete a branch that isn't actually merged. This guards against rare cases where step 3's `--merged` check returns a false positive (e.g., a branch was merged-then-reset locally). If `-d` fails, surface the error and skip that branch; do **not** fall back to `-D`.

Record each successful deletion (branch name + SHA) for the summary.

### 7. Final Summary

```
## Tidy-Git Complete

### Cleaned
- Pruned N stale remote-tracking refs (origin)
- Pruned M stale worktree refs
- Deleted K merged local branches:
  - feat/old-feature (sha 4a3b2c1)
  - fix/typo-readme (sha 9f8e7d6)

### Recoverable
- Deleted branches are in git reflog for ~90 days:
  `git reflog | grep <branch-name>` then `git branch <name> <sha>`

### Worth Reviewing (no action taken)
- Stashes: N (oldest from 2026-02-12)
  `git stash list` to inspect; `git stash drop <stash@{N}>` to delete
- Local-only branches with no upstream: M
  feat/wip-thing, fix/local-experiment
- Branches ahead of upstream: K
  feat/almost-done (3 commits ahead of origin/feat/almost-done)
- Local-only tags: J
  pre-rebase-backup-2026-05-11
- Untracked files: I (sample below; see `git status` for full list)
  /tmp/scratch.txt, PROJECT_PROGRESS.md, debug.log
```

If any of the auto-operations failed (e.g., `git remote prune` errored because there's no remote configured), report the failure inline and continue with the rest of the workflow.

## Safety Invariants

The skill must never:

- Delete the main branch.
- Delete the current branch.
- Use `git branch -D` (force delete) on any branch, ever. If `-d` fails, the branch stays.
- Run `git push`, `git push --force`, `git push --delete`, or any other operation that affects the remote.
- Run `git stash drop`, `git stash clear`, or otherwise discard stashes.
- Run `git tag -d` on any tag. (Local-only tags are reported, not deleted.)
- Run `git clean` to remove untracked files. (Untracked files are reported, not deleted; `/pre-compact` handles session-trash with judgment.)
- Run `git gc`, `git gc --aggressive`, or `git prune` on the object database. Git's `gc --auto` runs when needed.

These invariants are categorical. The skill does not offer flags or options to override them — if the user wants any of these operations, they invoke `git` directly.

## Abort Conditions

**Abort the workflow:**
- Not in a git repository.
- Repository is mid-operation (mid-rebase, mid-merge, mid-cherry-pick) — surface this and stop. The user should resolve the in-progress operation first.
- User interrupts.

**Do NOT abort for:**
- No remote configured (skip the prune step, continue).
- No worktrees (skip the worktree prune step, continue).
- Empty inventory (every category empty is a valid outcome — report "nothing to clean" and exit).
- Individual `git branch -d` failures (skip the branch, continue with the rest).

## Example Session

```
> /tidy-git

Detected: main branch = "master", current = "feat/wip-thing"

Pruning remote-tracking refs... 4 removed (feat/old-1, feat/old-2,
  feat/old-3, fix/merged-pr).
Pruning worktree refs... 0 removed.

Inventory:
- Merged local branches: 3 (eligible for deletion)
- Stashes: 2 (oldest from 2026-02-12, message: "wip: trying caching")
- Branches with no upstream: 1 (feat/wip-thing)
- Branches ahead of upstream: 0
- Local-only tags: 1 (pre-rebase-backup-2026-05-11)
- Untracked files: 7 (incl. /tmp/scratch.txt, PROJECT_PROGRESS.md)

## Branch deletion preview

The following local branches are fully merged into master and safe
to delete. SHAs preserved in git reflog for ~90 days.

  feat/old-feature      (2026-04-15, sha 4a3b2c1)
  fix/typo-readme       (2026-04-22, sha 9f8e7d6)
  feat/old-experiment   (2026-03-08, sha 1a2b3c4)

Delete all?
> Yes

Deleting feat/old-feature... done (sha 4a3b2c1).
Deleting fix/typo-readme... done (sha 9f8e7d6).
Deleting feat/old-experiment... done (sha 1a2b3c4).

## Tidy-Git Complete

### Cleaned
- Pruned 4 stale remote-tracking refs (origin)
- Deleted 3 merged local branches

### Recoverable
- `git reflog | grep <branch-name>` then `git branch <name> <sha>`

### Worth Reviewing (no action taken)
- Stashes: 2 (oldest from 2026-02-12)
  `git stash list` to inspect; `git stash drop <stash@{N}>` to delete
- Local-only branches with no upstream: 1 (feat/wip-thing)
- Local-only tags: 1 (pre-rebase-backup-2026-05-11)
- Untracked files: 7
  /tmp/scratch.txt, PROJECT_PROGRESS.md, debug.log, ... (4 more)
  Run `git status` for the full list.
```
