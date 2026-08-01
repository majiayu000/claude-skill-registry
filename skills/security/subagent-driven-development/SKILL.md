---
name: subagent-driven-development
description: The implementation engine. Routed to by /sprint (full plan, autonomous) and by executing-plans (scoped batch, checkpoint-gated). One fresh subagent per task — test-first via tdd — followed by spec-compliance review, quality review, and fresh-run verification. No single context accumulates drift, and nothing is accepted on a subagent's word.
---

# subagent-driven-development

One task, one fresh subagent, two reviews, proof on a fresh run. Routed to by `/sprint` (full plan,
autonomous) and by `executing-plans` (one batch at a time, with human checkpoints between batches).
The loop processes tasks in dependency order and never trusts a self-report.

## Pre-flight

Read these, or STOP and surface the gap — never guess scope, command, or obligation:

- `${CLAUDE_PROJECT_DIR}/.codearbiter/CONTEXT.md` — the `stage:` frontmatter (the maturity value) and project context.
- `${CLAUDE_PROJECT_DIR}/.codearbiter/plans/<slug>.md` — the approved plan. Each task carries an exact path set and a verification command. This is the task source.
- `${CLAUDE_PROJECT_DIR}/.codearbiter/specs/<slug>.md` — the approved spec. Each task's obligation traces to it. The spec-compliance review measures against it.
- `${CLAUDE_PROJECT_DIR}/.codearbiter/tech-stack.md` — build, test, and verification invocations; file layout; the scope-to-author mapping.
- `${CLAUDE_PROJECT_DIR}/.codearbiter/security-controls.md` — only when a task touches a security boundary (auth, crypto, secrets, a trust boundary).

**Optional `scope` parameter:** when invoked by `executing-plans`, a list of task IDs is passed. The
loop processes only those tasks (in their internal dependency order). When `scope` is absent (the
`/sprint` path), the loop processes the full plan from first unblocked task to last.

## Phase 1 — Task selection · gate: BLOCK

Pull the next unblocked task from the plan in dependency order. When a `scope` was passed, restrict
selection to tasks in that list. A task is one verifiable unit of work with a path set, a spec
obligation, and a verification command.

- Confirm every dependency task is `ACCEPTED` before selecting.
- Confirm no unresolved `[CONFIRM-NN]` blocks the task. One that does halts the loop — see Hard rules.

Gate: exactly one task selected, dependency-clean, with its spec obligation and verification command in hand.

## Phase 2 — Implementation dispatch · gate: BLOCK

**Farm path (when `<slug>.plan.json` exists alongside the `.md` plan):** skip the subagent dispatch
loop below and follow `${CLAUDE_PLUGIN_ROOT}/skills/subagent-driven-development/references/farm-dispatch.md`.
The farm path replaces only the *authoring* step for the plan's tasks (cheap Zen workers under hard
gates instead of premium subagents); it does **not** replace review — every task the farm reports green
is still routed through Phases 3–5 before acceptance. The cost arbitrage is in who *writes* the code,
never in whether it is *reviewed*. In brief: select a model (canary-probe with a cache→websearch
fallback ladder), dispatch `tools/farm.js`, honor a circuit-breaker abort as a hard-gate STOP, then for
each result either accept-after-Phases-3–5 (green) or re-dispatch via premium Phase 2 (escalate).
Results stream to `.farm/farm-results.jsonl` and are consumed in completion order — Phase 3 + Phase 5
per green task as it lands, Phase 4 still the once-per-scope barrier (reconcile against `farm-report.json`
on abort). The reference has the full step-by-step.

---

**Normal path (no `plan.json`):** dispatch ONE fresh subagent for the selected task — `backend-author`, `frontend-author`, or
`infra-author` by the scope mapping in `tech-stack.md`
(`${CLAUDE_PLUGIN_ROOT}/agents/<name>.md`). A fresh context per task is the whole point: no carried-over
assumptions, no accumulated drift.

The subagent works test-first by routing through the `tdd` skill — no implementation code before
`tdd` Phase 1. Brief it with the task's path set, its spec obligation, and its verification command.
Nothing else from prior tasks leaks in.

Gate: the subagent reports `tdd` complete — all six phases green. A `tdd` BLOCK halts the loop; do not
re-dispatch around it.

## Phase 3 — Spec-compliance review · gate: BLOCK

Did the change satisfy the task's obligation? Measure the result against the spec line the task
traces to — not against whether tests merely pass.

- Every acceptance claim in the task's obligation is met by the change.
- Scope is clean: nothing implemented beyond the task; nothing required by it omitted.
- Out-of-scope work the subagent noticed is recorded with an inline `[NEEDS-TRIAGE]` marker — never
  acted on inside this task.

Gate: the obligation is fully satisfied and scope is clean. A shortfall returns the task to Phase 2
with a corrective brief.

## Phase 4 — Quality review (once per scope) · gate: BLOCK

Runs ONCE per scope — after every task in the current scope has cleared Phase 3 and Phase 5 — over
the **combined diff** of the scope, not per 2–5-minute task. Per-task review at that granularity
costs more context than the work and catches nothing the batch diff doesn't; the batch boundary is
where review pays. (A scope of one task reviews that task's diff — same rule, degenerate case.)

Dispatch the reviewers applicable to what the combined diff touches, then `finding-triage`
(`${CLAUDE_PLUGIN_ROOT}/agents/finding-triage.md`) to classify every finding by severity. Select
reviewers by the diff, not blanket — dispatching an irrelevant reviewer wastes a context:

- `security-reviewer` (`${CLAUDE_PLUGIN_ROOT}/agents/security-reviewer.md`) — any security-relevant path (authn/authz, deploy, CI, trust boundary).
- `auth-crypto-reviewer` (`${CLAUDE_PLUGIN_ROOT}/agents/auth-crypto-reviewer.md`) — auth, crypto, key, or secret changes.
- `dependency-reviewer` (`${CLAUDE_PLUGIN_ROOT}/agents/dependency-reviewer.md`) — `package.json` / lockfile / base-image changes.
- `migration-reviewer` (`${CLAUDE_PLUGIN_ROOT}/agents/migration-reviewer.md`) — DB migration add/modify.

(Do NOT dispatch `grader` or `scout` — they are INTERNAL to `decision-variance` and must never be
dispatched here.) If the change touches none of the above domains, the quality bar is `tdd`'s own gates
plus `coverage-auditor` (already run in `tdd` Phase 4) — record that and proceed.

- A security CRITICAL finding halts the loop — see Hard rules.
- A HIGH finding returns the offending task(s) — attributed by file — to Phase 2; the scope's
  quality review re-runs over the corrected combined diff.
- MEDIUM and LOW findings are recorded; the user decides whether they block.

Gate: no CRITICAL, no HIGH across the scope's combined diff. Nothing in the scope is `ACCEPTED`
until this passes.

## Phase 5 — Verification · gate: BLOCK

Verification-before-completion: apply the shared fresh-run discipline in
`${CLAUDE_PLUGIN_ROOT}/includes/fresh-verification.md`, with **the task's verification command from the
plan** as the target. Run it yourself in a clean invocation; do not accept a logged result from Phase 2.
A non-zero exit, or output that does not demonstrate the obligation, returns the task to Phase 2.

Gate: the verification command exits clean and its output demonstrates the obligation. Only then.

## Phase 6 — Accept and advance · gate: BLOCK

Mark the task `ACCEPTED` only when its spec-compliance review and fresh verification passed AND the
scope's Phase 4 quality review passed.
Record acceptance **in the plan file itself** — set the task's `status` cell in
`.codearbiter/plans/<slug>.md` to `ACCEPTED` the moment it is accepted, plus any `[NEEDS-TRIAGE]`
markers and the `.codearbiter/` audit trail. The plan's status column is the pipeline's resume
ledger: an interrupted run is re-entered at the first non-`ACCEPTED` task, and an acceptance that
lives only in conversation context is lost to the interruption.

- Tasks remain in the current scope → return to Phase 1.
- **Scoped invocation** (`scope` was passed by `executing-plans`): all scoped tasks `ACCEPTED` → signal
  batch complete and return to `executing-plans`. Do NOT hand to `commit-gate`; the caller owns that decision.
- **Full-plan invocation** (no `scope`, i.e. `/sprint`): plan complete → hand the branch to
  `commit-gate`, then to the caller's finishing step. The loop does not commit on its own authority.

Gate: every task in the current scope `ACCEPTED`, the suite green, ready for the caller's next step.

## Hard rules

- MUST dispatch a fresh subagent per task — never reuse one context across tasks.
- MUST NOT write implementation code before the task's `tdd` Phase 1 completes.
- MUST accept a task only when both reviews pass AND verification passes on a fresh run.
- MUST NOT accept a task on a subagent's self-report — run the verification command and read its exit code.
- MUST halt and surface to the user on a `tdd` BLOCK, a security CRITICAL finding, or an unresolved `[CONFIRM-NN]` inside the loop — and on a `commit-gate` failure at the finish handoff — even under `/sprint`. These never auto-proceed.
- MUST NOT commit — hand the accepted branch to `commit-gate`.
- MUST mark out-of-scope findings with an inline `[NEEDS-TRIAGE]` marker and never act on them inside the task.
- MUST NOT invoke `farm.js` before writing `meta.model` into `plan.json` (or setting `FARM_MODEL`) — the dispatcher fails loudly otherwise.
- MUST NOT skip model selection (Step 1) when `FARM_MODEL` is not set — exhaust the canary→cache→websearch fallback ladder before BLOCKing; never blind-invoke with an unknown model id.
- MUST route every green farm task through Phases 3–5 before acceptance — the farm replaces authoring, never review. A cheap model gets the same scrutiny as a premium subagent, not less.
- MUST treat a single task's drift/gaming/tampered-test escalation as model incapacity (re-dispatch via premium Phase 2); raise `[CONFIRM-NN]` and HALT only when multiple tasks drift onto the same out-of-scope path (a real spec gap).
- MUST treat a `farm.js` circuit-breaker abort (`aborted: true`) as a hard-gate STOP — surface to the user; do not silently re-dispatch the whole slice to premium.
- MUST NOT dispatch `grader` or `scout` in Phase 4 — they are INTERNAL to `decision-variance`.
