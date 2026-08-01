---
name: finishing-a-development-branch
description: The terminal step of /feature and /sprint. Routed to once commit-gate has cleared, to decide the branch's fate — merge via PR, open a PR, or discard. Direct merge to the default branch is forbidden; every change lands through a PR. Under /sprint the skill auto-selects "open PR" and surfaces the merge decision to the user.
---

# finishing-a-development-branch

The work is committed and green. Now decide where it goes. Routed to by `/feature` and `/sprint`
after `commit-gate` clears — never before.

## Pre-flight

Read these, or STOP and surface the gap — never guess the branch name or the default branch:

- `${CLAUDE_PROJECT_DIR}/.codearbiter/CONTEXT.md` — the default-branch name and project context.
- `${CLAUDE_PROJECT_DIR}/.codearbiter/plans/<slug>.md` — the plan this branch executed, when `/feature` or `/sprint` produced one. The yardstick for "is the work complete."
- `${CLAUDE_PROJECT_DIR}/.codearbiter/last-checkpoint` — the most recent gate results; confirms `commit-gate` cleared on this branch.

`commit-gate` MUST have cleared on the current HEAD. If it has not, this skill does not run — return to it.

## Phase 1 — State assembly · gate: BLOCK

Assemble the facts the decision needs. Nothing is presented until all are in hand:

- **Branch** — the current branch name and its base. Confirm it is NOT the default branch; if HEAD is the default branch, STOP — there is nothing to finish and merge-to-default is forbidden.
- **Diff summary** — files changed, insertions/deletions, and the commit list since the base. Read it, do not paraphrase from memory.
- **Gate results** — `commit-gate` outcome and the `last-checkpoint` record. Surface any open `[NEEDS-TRIAGE]` markers left in the diff as out-of-scope findings.
- **Plan delta** — when a plan exists, state which plan items the branch satisfied and which remain open. Open items are surfaced, not hidden.

Gate: branch confirmed non-default, diff summary read, gate results and plan delta in hand.

## Phase 2 — Present terminal options · gate: STOP

Present exactly three terminal options with the Phase 1 state attached, then STOP for the choice:

1. **Open a PR** — push the branch and open a pull request against the default branch, then stop. The PR stays open; the merge happens later, by the user or reviewers.
2. **Merge via PR** — push the branch, open the PR, and once its checks are green, merge it **through the PR** so the work lands on the default branch now. Distinct from option 1: this one completes the merge. Still PR-only — no direct push to the default branch, no force-push.
3. **Discard** — abandon the branch.

Under `/feature`: STOP and let the user pick.

Under `/sprint`: auto-select **option 1 (open PR)** and surface the merge decision to the user — `/sprint`
autonomy ends at the PR boundary. It MUST NOT merge (option 2) and MUST NOT discard.

Gate: a single terminal option is chosen — by the user under `/feature`, or auto-selected as "open PR" under `/sprint`.

## Phase 3 — Execute the choice · gate: BLOCK

Carry out the chosen option, and only that one:

- **Open a PR** — push the branch and open the PR against the default branch. The reviewer path-matrix, the anti-slop PR-body composition (description citing the plan items satisfied, the gate results, the §2 conflict level of any non-obvious tradeoff), and the babysitter attach are the steps documented in the `/ca:pr` command flow (`${CLAUDE_PLUGIN_ROOT}/commands/pr.md`) — **execute those steps here; do not re-invoke `/ca:pr`** (under `/sprint` this skill is reached via `commit-gate`, without the `/pr` command ever running, so a route back would loop). Leave the PR open; the merge is not yours to take.
- **Merge via PR** — open the PR as above, confirm its checks are green, then merge it through the PR (squash or merge per project convention) so the work lands. Never push to the default branch directly, never force-push.
- **Discard** — requires explicit user confirmation naming the branch. Before discarding, verify the branch is fully pushed; if any commit is un-pushed, STOP and report exactly what would be lost — never delete un-pushed work silently. Discard proceeds only after the user confirms with that loss in view.

Gate: the chosen option completed — for open-PR a PR exists against the default branch; for merge the work landed through that PR; for discard the user confirmed against a stated loss summary.

## Phase 4 — Receipt · gate: BLOCK

The loop has been a chain of gates the user watched clear. End it on its most rewarding beat, not in
silence. Emit a tight **Receipt** — a win summary that reflects the prevention back, drawn ONLY from
the state Phase 1 already assembled plus `${CLAUDE_PROJECT_DIR}/.codearbiter/last-checkpoint`. This is
**not a fresh audit-trail crawl** — no new log scan, no `git` archaeology. If a field has no data in
hand, omit the line rather than go digging.

Report only what the assembled state supports:

- **Obligations covered** — the count of `tdd` obligations that reached `COVERED` on this branch.
- **Gates that fired and what each caught** — the gates that BLOCKed and then cleared, named with the
  specific thing caught (an untested seam, a scope-creep file set aside), not a bare gate name.
- **SMARTS decisions the user made** — the architectural forks the user resolved, one line each.
- **Secrets / regressions prevented** — credential findings and behavioral-proof mismatches the gates
  stopped before they shipped.
- **Suite time** — the wall-clock of the verifying run, from the gate results in hand.

Close with **exactly one** warm, synthesizing sentence (per the orchestrator register) that reflects
the run back — synthesized for this branch, not the register's canned example. One sentence, earned,
never on a no-op close.

Gate: the Receipt is emitted from in-hand state (no fresh crawl), and the close carries at most one
warm sentence.

## Hard rules

- MUST NOT merge directly to the default branch or force-push — every change lands through a PR.
- MUST NOT auto-merge under `/sprint`; auto-select "open PR" and surface the merge decision to the user.
- MUST NOT discard a branch without explicit user confirmation that names the branch.
- MUST NOT delete un-pushed commits silently — STOP and report the loss before any discard.
- MUST NOT run before `commit-gate` has cleared on the current HEAD.
- MUST NOT guess the branch or default-branch name — read `CONTEXT.md` or STOP.
- MUST draw the Receipt only from Phase 1 state + `last-checkpoint` — never a fresh audit-trail crawl — and never build a rolling cross-branch "saves" tally.
- MUST keep the close to at most one warm sentence; never on a no-op close.
