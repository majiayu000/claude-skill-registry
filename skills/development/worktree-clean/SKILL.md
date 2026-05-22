---
name: worktree-clean
description: Use when removing a git worktree and cleaning up its associated local branch from the main repository.
argument-hint: [worktree-path]
allowed-tools: Bash
---
worktree_path = $ARGUMENTS

Remove a local worktree and delete its associated local branch. If no argument is provided, list worktrees and ask which to remove.

## Local Only

Remote branches carry invisible state — open MRs, CI pipelines, review comments, deployment triggers — and deleting one can auto-close an MR silently. The user owns remote-branch deletions.

## Submodules

Submodule git state under `.git/worktrees/{name}/modules/{submodule}` is cleaned up with the parent worktree — no separate step.

## When Removal Resists

`git worktree remove` fails on unclean state; `git branch -d` fails on unmerged branches. Trivial leftovers (build artifacts, debug logs, already-pushed-or-merged work) justify forcing autonomously. Substantive uncommitted or unmerged work — describe what you found and let the user decide.

Run `git worktree prune` after removal to clear stale internal references.
