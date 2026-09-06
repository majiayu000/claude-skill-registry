---
name: autopilot
description: 'Use when a human has an approved delivery plan and wants the full chain run under phase gates. Not for planning, open-ended debugging, or single-step execution: use work directly.'
disable-model-invocation: true
---

# Autopilot

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A human explicitly invokes `/autopilot` with a feature description and an approved execution plan. |
| Authority | Human-gated: previews the exact target and consequence before credentials, paid actions, data-at-rest changes, publication, deployment, remote bulk mutation, or irreversible deletion, continuing only when the invocation covers that consequence; every other write is reversible local, with version control as the rollback. Pass authorized push and PR targets to `review-and-ship`; do not publish directly. |
| Side effect | Delegates implementation, simplification, review, and finalization to their respective skills; local artifacts are written by `work`, commits and PR are created by `review-and-ship`. No mutation is performed by autopilot itself. |
| Done | Return `DONE` only after the requested close-out state is observed. Otherwise return `BLOCKED` with a resumable handoff. |

## Inputs

Required: feature description, approved plan, repository, acceptance criteria, and close-out condition.

Optional: scope limits; assigned executor; target branch, remote, and PR destination; required checks; shipping instructions. Derive an omitted value only when repository evidence gives one safe, unique answer.

## Procedure

1. Parse the plan, scope, assignments, acceptance criteria, repository, required proof, shipping destination, and close-out condition. Reject contradictions and unavailable assigned executors. Done when: every required input is parsed and bound to a concrete value, contradictions are rejected with the conflicting pair named, and unavailable executors are reported; or the run stops on the first unresolvable input.
2. Confirm that the human approved the plan. If not, stop before implementation and route to planning. Done when: an approval record is confirmed; the plan was approved through plan mode or an equivalent written approval; or the run stops and routes to planning with no delegation.
3. Inspect enough repository evidence to bind the plan to exact artifacts, behavior, verification, and remote targets. Keep the campaign inside the approved scope. Done when: every plan step maps to a named repository artifact (file, directory, or remote target) and the scope boundary is stated with the artifacts inside it and the artifacts excluded from it.
4. Preview each risky consequence. Stop when authority is absent or the target is ambiguous. Done when: every credential, paid, data-at-rest, publication, deployment, remote bulk, or irreversible consequence is previewed with its exact target, or the run stops naming the absent authority or ambiguous target.
5. Delegate the bounded plan to `work` in orchestrated mode. Include acceptance criteria, constraints, repository evidence, required verifier, and the required structured return. `work` owns implementation and local verification; autopilot does not reproduce those steps. Apply the gate state machine in `references/pipeline-gates.md`: a failing work verifier gets one `strike-the-root` pass and one recheck; a second failure halts the chain. Done when: `work` returns a structured result with implementation summary and local verification passing, or the gate halts the chain with the verifier failure and diff recorded.
6. Delegate simplification to `simplify` on the completed diff. Gate: `simplify` exits `0`, `11`, or `12` with behavior preserved. Halt on exit `14` (new bloat) or `15` (mixed-concern). Done when: `simplify` returns exit `0`, `11`, or `12` with behavior preserved confirmed by its output, or the chain halts on exit `14` or `15` with the exit code and cause recorded.
7. Delegate review to `review` on the in-scope change. If critical or high findings remain, delegate one `strike-the-root` pass and re-review the changed files. Halt on residual critical or high findings. Done when: `review` returns zero critical and zero high findings on the changed files, or the chain halts with the residual findings listed.
8. Delegate finalization to `review-and-ship`. Pass the reviewed diff, explicit delegated shipping authority, branch, remote, PR destination, required checks, and shipping instructions. The finalizer owns checks, commits, publication classification, push, and PR creation or update; autopilot performs none of them. Done when: `review-and-ship` returns its report with checks green and PR created or updated (full mode) or commits made and push skipped (local-only), or the finalizer returns blocked with its reason.
9. Observe authorized close-out. Route any supported in-scope fix back through `work` in orchestrated mode, repeat affected gates, and invoke `review-and-ship` for each authorized update. Do not merge, deploy, or publish elsewhere without matching authority. Done when: the close-out condition named in the inputs is observed in repository or remote state, or the run stops for absent authority.
10. Return the terminal classification and include the finalizer report. The gate and handoff formats in `references/pipeline-gates.md` are binding. Done when: the terminal result is `DONE` with the finalizer report attached and close-out state quoted, or `BLOCKED` with the failed stage, reason, and next action named.

## Failure and recovery

Stop on a missing approved plan, contradictory input, unavailable executor, ambiguous target, absent authority, failed gate, non-converging review, rejected remote mutation, or incomplete close-out. Preserve successful in-scope work and observed remote state. Recover only mutations made by this run, using reversible repository or hosting operations; never discard unrelated work.

Return `BLOCKED` with the failed stage, exact reason, autofix result, partial artifacts, remote mutations, proof state, recovery state, and the single concrete requirement to resume. Never claim rollback, publication, or close-out without observing it.

## Output

Exactly one terminal result:

- `DONE`: delivered behavior, changed artifacts, verification evidence, branch and PR, the complete `review-and-ship` report, and observed close-out state.
- `BLOCKED`: failed stage, reason, partial result, remote state, proof and recovery status, and the next required action.
