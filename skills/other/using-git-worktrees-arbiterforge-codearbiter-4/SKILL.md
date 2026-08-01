---
name: using-git-worktrees
description: OPTIONAL per-task isolation for autonomous parallel work. Routed to only on explicit opt-in by subagent-driven-development or dispatching-parallel-agents, so parallel units mutate files without colliding. Stands up one worktree per unit, works it in isolation, then integrates each unit back onto the caller's working branch for the caller's single commit-gate + finishing-a-development-branch exit. Never on the default path; it does not bypass a gate or finish per unit.
---

# using-git-worktrees

OPTIONAL. Per-task filesystem isolation for parallel agent work — opt-in only, never the default path.
Routed to by `subagent-driven-development` and `dispatching-parallel-agents` when, and only when, the
caller requests isolation. If no isolation is requested, this skill does not run; parallel units share
the working tree under their own discipline.

Isolation is convenience, not soul. It lets concurrent units edit files without collision. It changes
nothing about the gates — the consolidated work still clears `commit-gate` and the single
`finishing-a-development-branch` terminal step, run by the caller. What it MUST NOT do is multiply
that terminal step into one PR per unit.

## Pre-flight

Read these, or STOP and surface the gap — never guess:

- `${CLAUDE_PROJECT_DIR}/.codearbiter/CONTEXT.md` — confirm the repo is a git repo and the base/working branch.

Confirm the caller passed an explicit isolation opt-in AND the parallel unit list (from `plans/<slug>.md`). Absent either, do not stand up worktrees.

## Phase 1 — Provision · gate: BLOCK

Stand up one worktree per parallel unit. For each unit, create a worktree on a fresh branch off the
current base, under a dedicated parent directory outside the main working tree
(e.g. `../.codearbiter-worktrees/<slug>`):

- One worktree, one branch, one unit. Never share a worktree across units.
- Branch name MUST be unique and traceable to its unit's task ID.
- Record each worktree path and branch in a dedicated manifest `${CLAUDE_PROJECT_DIR}/.codearbiter/.worktrees.json` (gitignored scratch — NOT the `open-tasks.md` backlog) so a crash leaves no untracked isolation.

Gate: every unit has a distinct worktree on a distinct branch, all rooted at the same clean base, all
recorded. A reused branch or a missing record does not pass.

## Phase 2 — Isolated work · gate: BLOCK

Each parallel unit works entirely inside its own worktree. Dispatch is unchanged — the caller still
dispatches its author and reviewer agents; they simply operate on the isolated path.

- A unit MUST NOT read or write outside its assigned worktree.
- A unit MUST NOT touch `main` or any other unit's branch.
- All implementation inside a worktree still flows through `tdd` — isolation is not a TDD bypass.

Gate: each unit's work is contained to its own worktree, with no cross-worktree or base-branch writes.

## Phase 3 — Fold back · gate: BLOCK

Integrate each isolated unit's work back onto the caller's single working branch — do NOT finish each
unit on its own. Per unit, in order:

1. Confirm the unit was accepted by the caller (its per-task review and verification passed in
   `subagent-driven-development`, or its result cleared the funnel in `dispatching-parallel-agents`).
   An unaccepted unit does not fold back.
2. Integrate its branch onto the caller's working branch (merge or rebase), resolving any conflict
   here, in the open. Never integrate onto `main` or the default branch.

The consolidated working branch then takes the caller's normal single exit — ONE `commit-gate` pass
and ONE `finishing-a-development-branch` decision, run by the caller, not per unit. This skill
integrates; it never opens N PRs or finishes N branches. A unit that cannot integrate cleanly is
surfaced as a conflict for resolution — never force-merged, never dropped silently.

Gate: every accepted unit integrated onto the caller's working branch with conflicts resolved; no
per-unit PR or finish was opened.

## Phase 4 — Teardown · gate: BLOCK

Remove every worktree this skill created, prune its administrative metadata, and clear the manifest at
`${CLAUDE_PROJECT_DIR}/.codearbiter/.worktrees.json`. A unit whose branch was integrated onto the
working branch (Phase 3) has its worktree torn down; an unaccepted or abandoned unit's worktree and
branch are removed together.

Gate: zero worktrees created by this skill remain, and the manifest is empty. An orphaned worktree is a failure.

## Hard rules

- MUST NOT run on the default path — isolation requires an explicit caller opt-in.
- MUST NOT share a worktree or a branch across parallel units.
- MUST NOT let a unit read or write outside its assigned worktree, or touch `main`.
- MUST NOT open a per-unit PR or run `finishing-a-development-branch` per unit — integrate accepted units onto the caller's working branch, which takes the single `commit-gate` + finishing exit.
- MUST NOT leave an orphaned worktree behind — every worktree this skill creates is torn down before the skill returns.
