---
name: ca-cleanup
description: Finish an already-merged branch — classify the leftover artifacts, return to a fast-forwarded default checkout, and delete the merged local branch. Every discard confirmed per item; ancestry proven, never assumed.
argument-hint: (none)
---

# $ca-cleanup — post-merge branch transition

Your PR merged. You are still standing on the branch, with build output, worktree
residue, and scratch files around you. This command owns the ordinary walk back:
prove the branch actually landed, decide what the leftovers are, get to a clean
fast-forwarded default checkout, and drop the merged local branch.

It exists because nothing else owned it. `$ca-standup` is daily hygiene and
deliberately never touches the current branch or the default one;
`$ca-chore` takes docs, dependency bumps, and reverts. Issue #308 recorded
what the gap produced: a routine cleanup routed to `$ca-chore`, which
refused it, and then to `$ca-override` — a bypass invented to cover missing
coverage. This is that coverage.

## Routes to

The `post-merge-cleanup` skill (`${CLAUDE_PLUGIN_ROOT}/routines/post-merge-cleanup/SKILL.md`),
which owns the ancestry proof, the artifact classification, and the per-item
confirmations.

## When NOT to use

- The branch has NOT merged yet → `$ca-pr` (`finishing-a-development-branch`)
  owns the terminal decision; come back here after it lands.
- Daily start-of-day hygiene across *other* branches and worktrees →
  `$ca-standup`.
- A read-only look at what is dirty → `$ca-status`.
- Uncommitted work you want to keep → `$ca-commit`. This command never
  commits for you.

## Hard gate

- MUST prove the current branch is an ancestor of the **fetched** default branch
  before anything is deleted. An unproven or unfetched ancestry STOPs — a branch
  that only *looks* merged is not merged.
- MUST classify every dirty or untracked artifact as **unique**, **redundant**,
  or **superseded**, and MUST NOT discard a unique or unclassifiable one without
  explicit per-item confirmation naming it.
- MUST confirm each removal individually — no batched yes, no implied yes.
- MUST reach the default branch with a clean working tree, and MUST fast-forward
  with `--ff-only` only — never a merge commit, never a rebase, never a reset
  that discards work.
- MUST NOT force-delete a branch, force-push, delete a remote branch, or write to
  the default branch.
- MUST NOT require `$ca-override`. This is ordinary lifecycle work; if it
  cannot proceed, the reason is a stated gate, not a bypass.
