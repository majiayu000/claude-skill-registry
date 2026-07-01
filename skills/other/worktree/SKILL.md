---
name: worktree
description: Set up isolated git worktrees — create a new branch for fresh work, or attach a worktree to an existing branch/PR/commit. Use when starting isolated work or isolating an existing ref; detects existing isolation first.
argument-hint: "[optional: ref to isolate, or new-branch-name]"
---

# Worktree Isolation

`Op: extend` — adds harness-aware git worktree setup for isolated branches and refs.

Ensure the current work happens in an isolated workspace without disturbing the main checkout. Most harnesses create a worktree by default at session start, so the common case is that isolation already exists — detect that first and do not create a redundant one.

Order: detect existing isolation → prefer a native worktree tool → fall back to plain git. Never create a worktree the harness cannot see.

## Modes

- **New work (default).** No specific ref named — create a fresh branch from the base branch.
- **Isolate an existing ref.** Caller names a ref to work on in isolation — a PR head, branch, or commit. Attach the worktree to that ref instead of creating a new branch.

Hard rule for isolate-an-existing-ref: a branch can be checked out in only one worktree at a time. If the named ref is already checked out elsewhere, report the path and let the caller act (work there in place; or, only if a clean separate tree is essential, create a detached worktree at the same commit). Never put one branch in two worktrees.

## Step 0: Detect existing isolation

Before creating anything, check whether the current directory is already a linked worktree. Compare the resolved absolute git dir against the resolved absolute common git dir:

```bash
git rev-parse --absolute-git-dir
(cd "$(git rev-parse --git-common-dir)" && pwd -P)
```

If equal, this is a normal checkout — continue to Step 1.

If they differ, you are in a linked worktree or a submodule. Distinguish:

```bash
git rev-parse --show-superproject-working-tree
```

- Non-empty output → submodule; treat as normal checkout and continue to Step 1.
- Empty output → already in an isolated worktree. Report the worktree path (`git rev-parse --show-toplevel`) and current branch. Do not create another worktree. In new-work mode, continue here. In isolate-an-existing-ref mode, check that ref out here unless it is already the current branch.

## Step 1: Prefer the harness's native worktree tool

If the harness provides a native worktree primitive — for example Claude Code's `EnterWorktree`, a `/worktree` command, or a `--worktree` flag — use it and stop. Native tools place, track, and clean up the worktree so the harness can manage it. A behind-the-back `git worktree add` creates phantom state the harness cannot see, navigate to, or clean up.

## Step 2: Git fallback

Only when there is no native tool and Step 0 found no existing isolation.

1. Run from the repo root: `cd "$(git rev-parse --show-toplevel)"`.
2. Choose a meaningful branch name from the work description. Pick a base branch (default: origin's default branch, else `main`).
3. Ensure `.worktrees/` is gitignored before creating anything: `git check-ignore -q .worktrees/` (with trailing slash). If not ignored, add `.worktrees/` to `.gitignore`.
4. Best-effort refresh the base branch: `git fetch origin <from-branch>`. Non-fatal.
5. Create the worktree:
   - New work: `git worktree add -b <branch-name> .worktrees/<branch-name> origin/<from-branch>` (fall back to local `<from-branch>` if origin ref missing).
   - Isolate existing ref: for branch/tag, `git worktree add .worktrees/<slug> <target-ref>`. For PR: `git fetch origin pull/<n>/head:pr-<n>` then `git worktree add .worktrees/pr-<n> pr-<n>`. If the ref is already checked out elsewhere, follow the already-checked-out rule.
6. Switch into it: `cd .worktrees/<branch-name>`.

If `git worktree add` fails with a sandbox or permission error, report the failure and ask the user for a blocking decision (work in current checkout vs stop). Only work in the current checkout on explicit confirmation.

## Other worktree operations

Use git directly:

```bash
git worktree list
git worktree remove .worktrees/<branch>
cd .worktrees/<branch>
cd "$(git rev-parse --show-toplevel)"
```

## When to create a worktree

Create one only when not already isolated and a separate workspace is needed:

- Reviewing a PR while keeping the current checkout free.
- Running multiple features in parallel without branch-switching overhead.

Do not create a worktree for single-task work that can happen on a branch in the current checkout, and never when Step 0 shows you are already in one.

## Integration

`/work` and `/review` offer this skill as an option. When the user selects "worktree" in those flows, run Step 0 first: if already isolated, proceed in place; otherwise create one (native tool preferred) with a meaningful branch name derived from the work description.

## Troubleshooting

**"Worktree already exists"**: switch to it (`cd .worktrees/<branch>`) or remove it (`git worktree remove .worktrees/<branch>`) before recreating.

**"Cannot remove worktree: it is the current worktree"**: `cd` out first, then remove.
