---
name: suede-ship
description: "Canonical Suede shipping DAG: scout, multi-lens research, gap critic, lane plan with explicit file ownership, disjoint parallel build, dual-lens review, adversarial refute, integration gate, and release verification. Use for any nontrivial change to a repo that touches more than one file or surface and deserves roughly fifty agents of surgical, research-heavy fan-out. Halts on a blocking hazard (a real secret in a tracked file, a live process holding a target worktree) or a lane collision rather than plowing through. Reads production; never deploys. NOT FOR: high-volume, well-specified work that splits into independent worker-sized tasks (use suede-codex-fleet, which bills to the OpenAI subscription instead); findings-only review with no code change (use suede-code-review); CI and branch-protection wiring (use suede-ci-gate)."
---

# Suede Ship

The canonical Suede DAG. One prompt in, one shipped change out, with about fifty
agents in between arranged as a graph rather than a chain.

Invoke the workflow bundled at `skills/suede-ship/workflows/suede-ship.js`. If
you keep a personal copy, `~/.claude/workflows/suede-ship.js` works the same way.

## Choose this or the fleet first

`suede-ship` is the surgical instrument and it is the expensive one. Roughly
fifty agents (about fifty-four when `deploys` is true), research-heavy and
front-loaded, billed to the Claude limit.

If the job is actually high-volume, well-specified, and splits into independent
worker-sized tasks (content batches, test generation, bulk refactors), say so
and offer [`suede-codex-fleet`](../suede-codex-fleet/SKILL.md) instead. That runs
on the OpenAI subscription and costs nothing against the Claude limit. Brute
force beats surgery when the work is genuinely parallel and shallow.

## Parse the invocation

The argument is free-form. Extract:

- **repo** — required. An absolute path. Resolve a bare name against `~/code/<name>`.
  If no repo is named and the cwd is inside a git repo, use that repo's root.
- **scope** — required. What to change, in the user's own words, kept verbatim
  where possible. Do not compress it into a slogan; the planner decomposes it
  into lanes and the detail is what makes lanes separable.
- **deploys** — true if the repo has a `vercel.json`, a platform project link, or
  a known live URL. Check rather than assume.
- **liveUrl** — the production URL if you know it or can read it from
  `vercel.json`, `package.json`, or the README. Optional; the release verifier
  discovers it otherwise.
- **vault** — optional absolute path to an external decision store (a synced
  notes vault, an ADR archive, a handoff directory). Omitted by default. When
  present, the prior-decisions lens reads it as context, never as source truth.

If **scope** is missing, ask for it. Do not invent a change to a production
repo. This workflow writes code.

## State the cost before launching

This is Claude-model fan-out against the weekly limit. Say so in one line before
the call, so the spend is a decision rather than a surprise.

## Launch

```
Workflow({
  scriptPath: "skills/suede-ship/workflows/suede-ship.js",
  args: { repo, scope, deploys, liveUrl, vault }
})
```

Pass `args` as a real object. If the harness stringifies it the script recovers,
but an object is correct.

## The graph

Nine phases, parallel wherever the edges are not real:

1. **Scout** — fetch origin, dirty files, worktrees, deploy-time landmines. Manifest only.
2. **Research** — multi-modal sweep. Each lens searches a different way and is blind
   to the others, because one angle never finds everything. Every claim carries a
   `file:line`, sha, PR, or doc url.
3. **Gaps** — a completeness critic names what went unread, then one bounded fill round.
4. **Plan** — the lane map, with explicit file ownership. High effort by design.
5. **Build** — disjoint lanes, each pipelined straight into its own review.
6. **Refute** — adversarial verifiers, refute-by-default, majority kills the finding.
7. **Gate** — a real barrier: typecheck, build, and tests on the integrated worktree.
8. **Release** — adversarial release verification: config drift, public surface,
   irreversibility, live baseline.
9. **Handoff** — the evidence record: changed files, commands run, verification, caveats.

## While it runs

Do not predict results or narrate progress you cannot see. The workflow returns a
notification when it completes; `/workflows` shows live progress.

## When it returns

Report faithfully, including the failure shapes:

- `halted: true, reason: "blocking hazard at scout"` — a real secret in a tracked
  file, or a live process holding a worktree this run would touch. Name the hazard.
- `halted: true, reason: "lane collision"` — the lane map claimed a protected dirty
  file, gave one file two owners, or hit a file held by a **live** sibling worktree.
  Report the collisions. The fix is a re-plan, not a retry.
- Completed — lead with `shipVerdict` and `gatePassed`, then confirmed findings, then
  `crossWorktree` overlap (files this work will need rebasing against other branches),
  then `droppedConstraints` (what the skeptic rejected) and `unread`.

Naming what went unread is most of the honesty.

## Verdict is advisory

The `shipVerdict` changes what you report, never what you do. The single exception
is live production exposure the verifier observed independent of this change, such
as a real secret or an unauthenticated `200` that should not exist. That goes to the
user immediately.

**Do not claim `deployed`, `verified live`, or `released`.** This workflow only reads
production. Those states require a deploy that has not happened.

## Iterating

Edit the script and re-invoke with the same `scriptPath`. Add
`resumeFromRunId: "<run id>"` to replay unchanged agents from cache. Changing an
agent's prompt or schema re-runs that agent and everything downstream of it.
