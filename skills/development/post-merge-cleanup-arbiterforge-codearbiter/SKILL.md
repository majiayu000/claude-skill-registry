---
name: post-merge-cleanup
description: Finish an already-merged branch. Proves the branch is an ancestor of the fetched default, classifies leftover artifacts as unique / redundant / superseded, returns to a clean --ff-only default checkout, and deletes the merged local branch — every discard confirmed per item. Routed to by /ca-cleanup.
---

# post-merge-cleanup

The walk back from a merged PR. Routed to by `/ca-cleanup`.

The work has landed on the default branch. What is left is local: the branch you
are standing on, and whatever the run left in the tree. This skill returns you to
a clean, fast-forwarded default checkout without losing anything you have not
explicitly agreed to lose.

**It is ordinary lifecycle work and never needs `/ca-override`.** When it
cannot proceed, it names the gate that stopped it. Issue #308 recorded the
alternative: with no owner for this transition, the routing loop reached for
`/ca-chore`, then for `/ca-override` — a bypass manufactured to cover a
coverage hole.

## Pre-flight

Read this, or STOP and surface the gap — never guess the default-branch name:

- `<project-root>/.codearbiter/CONTEXT.md` — the default-branch name.

If HEAD is already the default branch, there is no transition to make. Report the
dirty state read-only and exit; branch pruning across *other* branches belongs to
`/ca-standup`.

## Phase 1 — Prove the merge · gate: BLOCK

A branch that looks merged is not merged. Establish it against the network, not
against a stale local ref:

1. `git fetch` the remote holding the default branch. A fetch that fails STOPs —
   an unfetched comparison proves nothing.
2. Confirm the current branch is an **ancestor** of the fetched default
   (`git merge-base --is-ancestor HEAD origin/<default>`). This is the test that
   matters, and it is deliberately not `: gone]` upstream state: a squash-merged
   branch whose remote still exists is fully contained in the default branch and
   is safe to delete, while a `: gone]` branch whose commits never landed is not.
3. Report the proof as a fact — the default branch, the fetched SHA, and that
   HEAD is contained in it.

If HEAD is **not** an ancestor, STOP. Name the un-landed commits and route to
`/ca-pr`; nothing is deleted here.

Gate: the remote is fetched and HEAD is proven an ancestor of the fetched default
branch — or the skill has stopped.

## Phase 2 — Classify the residue · gate: BLOCK

List every dirty tracked change, every untracked file, and every stash reachable
from this branch. Classify each into exactly one of three, and say *why* for each:

- **Redundant** — byte-identical to content already on the default branch, or a
  regenerated build artifact whose generator is committed and rerunnable. Safe to
  remove because removing it loses no information.
- **Superseded** — an earlier form of something the merged PR already landed in a
  better shape. Name what supersedes it.
- **Unique** — anything else. This is the default: an artifact that cannot be
  proven redundant or superseded IS unique. Uncertainty classifies as unique, not
  as redundant.

Present the classification before touching anything. A file whose class you
cannot establish is reported as unique with the reason you could not classify it.

Gate: every dirty, untracked, and stashed artifact carries a class and a stated
reason, with unclassifiable items counted as unique.

## Phase 3 — Resolve the residue · gate: STOP

Per item, in the order Phase 2 listed them. Never batch:

- **Unique** — offer to keep it: `/ca-commit` it on this branch before the
  transition, move it aside, or leave it in place and stop the cleanup. It is
  discarded only if the user explicitly confirms *that item by name*, with the
  Phase 2 reasoning in view.
- **Redundant / superseded** — offer removal, one confirmation each, stating what
  it is and why it is safe. Declining leaves it exactly where it is.

A stash is never dropped here. Stashes are reported with `git stash show` as the
suggested next step, the same report-and-route contract `/ca-standup` holds.

If anything the user chose to keep would block the checkout, STOP and say so
rather than removing it anyway. A blocked checkout is a fine outcome; a silent
discard is not.

Gate: every item is resolved by an explicit per-item decision, and the working
tree is clean enough to check out the default branch — or the skill has stopped
with the blocker named.

## Phase 4 — Transition · gate: BLOCK

Only after Phase 3 leaves the tree safe:

1. Check out the default branch, then **verify the checkout actually happened**
   (`git branch --show-current`). A checkout silently fails when another worktree
   holds the branch, and every step after this one would otherwise run against
   the wrong branch.
2. Fast-forward with `--ff-only`. A divergence means the default branch moved in
   a way this skill will not reconcile: report it and stop. Never a merge commit,
   never a rebase, never a reset.

Gate: HEAD is confirmed on the default branch by re-read, and the fast-forward
either succeeded or was reported as a refused divergence.

## Phase 5 — Delete the merged local branch · gate: STOP

Offer deletion of the now-merged local branch, with the Phase 1 ancestry proof
restated. One confirmation, naming the branch.

- `git branch -d` only. Never `-D`: the safety check is the point, and if `-d`
  refuses, the ancestry proof and the refusal disagree — report both and stop.
- The **remote** branch is never touched. If the user wants it gone, that is
  theirs to do or the platform's auto-delete-on-merge to do.

Declining leaves the branch in place. That is a normal outcome, not a failure.

Gate: the branch is deleted only after an explicit confirmation naming it, via
`-d`, with the remote untouched.

## Phase 6 — Receipt

One short summary: what landed, what was removed, what was kept, and where HEAD
is now. State declines as declines — a cleanup the user stopped halfway is a
correct outcome reported plainly, not an error.

## Hard rules

- MUST fetch and prove `HEAD` is an ancestor of the fetched default branch before
  any deletion. MUST NOT infer merge state from a `: gone]` upstream alone.
- MUST classify every artifact, and MUST treat anything not provably redundant or
  superseded as unique.
- MUST NOT discard a unique or unclassifiable artifact without an explicit
  confirmation naming that item.
- MUST confirm every removal and the branch deletion individually — no batched or
  implied yes.
- MUST re-read the current branch after checkout before acting on it.
- MUST use `--ff-only`, and MUST NOT merge, rebase, or reset to reach the default
  branch.
- MUST use `git branch -d`, never `-D`; MUST NOT delete a remote branch,
  force-push, or write to the default branch.
- MUST NOT drop a stash — report and route, as `/ca-standup` does.
- MUST NOT route to `/ca-override` when blocked. Name the gate instead.
