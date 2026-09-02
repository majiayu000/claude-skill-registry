---
name: finish-it-now
description: 'Use when the user says ship it now, no phases, or finish it now, or when in-scope work would otherwise be deferred to phases, rollouts, follow-up PRs, or TODOs. Implements every in-scope path in one change. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Finish it now

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user says ship it now, no phases, or finish it now, or the work would otherwise be split into phases, staged rollouts, follow-up PRs, or TODO-later remainders. |
| Authority | Reversible-local: write only the named local implementation artifacts that the ask puts in scope. Rollback is reverting this single change. |
| Side effect | All in-scope implementation paths are written in one change. The change produces no TODO, stub, placeholder, NotImplemented, or follow-up remainder. |
| Done | Every in-scope path is implemented in one change, and anything dropped is named in one line with its reason. |

## Inputs

- The ask (required): the work to ship, including every path it puts in scope.
- A phased skill or plan in play (optional): when present, its steps are collapsed into this single pass rather than executed across phases.

## Procedure

1. Execute the whole ask in one pass. No phase 1 and phase 2, no staged rollout, and no follow-up PR for work already in scope. **Done when:** the whole ask is executed in one pass.
2. Finish every opened path. Write the real implementation instead of leaving a TODO, stub, placeholder, or raised NotImplemented. **Done when:** every opened path has a real implementation.
3. When a phased skill or plan is in play, collapse it to one pass: run its steps back to back in this change and ship the result. While this posture is active it takes precedence over phase-based execution. **Done when:** any phased plan is collapsed into this change.
4. When the ask genuinely exceeds one pass, cut scope instead of deferring it. Name what was cut and why; never hand back a remainder. **Done when:** scope that cannot fit is cut and named rather than deferred.
5. Report only what shipped. Done names the code that is in the tree right now. **Done when:** the report names only code present in the tree.
## Failure and recovery
- Unshipped remainder: a TODO, stub, placeholder, NotImplemented, or phase-2/later/follow-up label is unshipped work. Recover by writing the real implementation; if that is genuinely impossible in one pass, cut scope out loud in one line rather than carry pending work.
- Scope exceeds one pass: cut scope, name what was cut and why in one line, and ship the reduced scope. Never return a deferred remainder or pretend the done predicate holds.
- Partial result: nothing is labeled done until every in-scope path is implemented. A partial change is not done and is not reported as done.

## Output
The complete change with every in-scope path implemented, plus one line naming anything cut and why if scope was reduced.
