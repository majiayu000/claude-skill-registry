---
name: tribunal
description: The deep, rarely-convened whole-codebase audit lane. Routed to when the user invokes $ca-tribunal. Seven gated phases — cost/model, map, roster dispatch, triage, report, approval+filing, telemetry. Costs on the order of millions of tokens; proceeds only after the user acknowledges the estimate; never a required gate; nothing filed or sent without explicit authorization.
---

# tribunal

The deepest, most expensive review codeArbiter offers — convened rarely, on demand, never as a gate. Routed to when the user invokes `$ca-tribunal`. Eleven specialist lenses judge the codebase; every finding persists to its own file (plus append-only triage/run logs) under a run dir that survives compaction and disconnects, so the run resumes from disk.

## Pre-flight

Read these, or STOP and surface the gap — never guess a command or a path:

- `<project-root>/.codearbiter/tech-stack.md` — stack, async model, concurrency primitives, test/lint/secrets commands, and, when documented, the tracker command. Stop if the test/lint/secrets commands are missing; do not guess.
- `<project-root>/.codearbiter/CONTEXT.md` — the `stage:` maturity value and domain vocabulary.
- `<project-root>/.codearbiter/coding-standards.md` — the conventions lenses judge against.
- `<project-root>/.codearbiter/security-controls.md` — trust boundaries, approved crypto/secret stores; feeds the appsec and secrets lenses. Absent on some repos — proceed without the security lenses' control-file checks if so.
- A git repository must be present.
- The reference set under `${CLAUDE_PLUGIN_ROOT}/routines/tribunal/references/` — each is cited at its phase, loaded on demand. Do not preload them.

## Phase 0 — Cost, model & resume · gate: STOP

This lane is expensive. Orient and get explicit go-ahead before dispatching anything.

- **Resume check.** Scan `.codearbiter/reports/` for the most recent run dir matching the current scope-slug, any date — never just today's. If none, skip to sizing. If found, check completion: incomplete (no `report-written` event in its `run.jsonl`) means either resumable or stale, judged by that run dir's latest `run.jsonl` timestamp. A run whose `run.jsonl` carries `run-aborted` is terminal — never offered for resume; a fresh run starts. Younger than 7 days → recover position with the cheap cursor scan in `references/schemas.md` (grep the last `wave-triaged`, do not read finding bodies) and offer to resume at the first un-triaged wave instead of restarting; skip the estimate. Older than 7 days → STOP and ask the user to resume anyway or start fresh — the codebase may have drifted under the findings, and stale-tree findings must not silently merge with fresh ones. Complete → start a fresh run.
- **Abandon.** If the user tells the orchestrator to abandon the run, log a `run-aborted` event to `run.jsonl` before stopping.
- **Cost acknowledgment.** Size the job, compute the token band, recommend the model (highest-reasoning available, high effort), and offer the cost-control levers. Present the band plainly; nothing dispatches until the user acknowledges it and confirms the model.
- Establish `RUN_ID` = `<UTC-date>-<scope-slug>` on a fresh run; create `.codearbiter/reports/<run-id>/`; open `run.jsonl`. On resume, reuse the existing `RUN_ID` as-is — the date is the run's creation date and never changes on resume.
- Procedure: `references/cost-and-models.md` — load now.

Gate: the user has acknowledged the estimated cost and confirmed the model. An unacknowledged run does not pass.

## Phase 1 — Map + judgment overlay · gate: BLOCK

Map before reviewing; the map decides what gets scrutiny.

- Produce the inventory (inline, or on a large repo dispatch the optional cheap mappers per `references/cost-and-models.md`): file tree, language breakdown, entry points/routes, core-logic and shared-utility locations, dependency and integration surface. Write `inventory.md`.
- Apply the judgment overlay in `references/ai-markers.md`: risk-rank directories (untrusted input, money, auth, PII, churn = highest), mark trust boundaries, record AI-authorship markers and an iteration-depth estimate. High-marker / high-iteration areas carry a scrutiny boost and a small severity prior.
- Choose the active lenses — the full roster minus any whose concern is absent from scope (no migrations → drop the migration lens). Record launched/skipped as `run.jsonl` events.
- Choose the wave partition — the default in `references/cost-and-models.md`, or a repartition for cause — and record it in the `run-started` event (`references/schemas.md`); resume reads this recorded partition, never re-derives it.

Gate: `inventory.md` written with the risk/boundary/marker overlay, and the active-lens set recorded.

## Phase 2 — Roster dispatch (dual output: finding files + summary) · gate: BLOCK

Dispatch the active lenses in the wave partition recorded at Phase 1 (default in `references/cost-and-models.md`) at the concurrency from `references/cost-and-models.md` (≤5 in flight). Give each agent only its scope slice, on the model/effort from `references/cost-and-models.md`; the agent itself reads its own mandate (`references/lenses/<lens>.md`) and the finding contract (`references/finding-record.md`), and loads neither the other lenses' mandates nor the orchestrator schemas. The orchestrator reads `references/finding-record.md` to read findings at triage, and consults a lens mandate only to adjudicate that lens's finding.

- Each `tribunal-*` agent writes each finding to its own file `findings/<lens>/<finding-id>.json` the moment it is found — one file per finding, never a batched write at the end (write contract: `references/finding-record.md`).
- **Evidence-or-drop.** Every finding cites a concrete `path:line` and the minimal snippet. An absence claim — "no handler", "no teardown", "missing validation" — requires reading the whole unit, never a truncated window.
- Specialists never dispatch further subagents. Update each wave's status in `run.jsonl` as it flushes.
- When a lens's summary returns, record a `lens-completed` event in `run.jsonl` with `surface_seen`/`findings`/`model` taken from the agent's summary, plus `tokens` when the orchestrator can observe that lens's spend.
- **Codex usage receipt.** If the current host has no subagent dispatch capability and a lens must run inline, record `tokens_status: unavailable` and `tokens_reason: host-usage-unsupported`. If dispatch succeeds but returns no usable thread ID, record `tokens_status: unavailable` and `tokens_reason: host-result-missing`. Otherwise capture the returned agent thread ID on the `lens-launched` event. After that lens completes, resolve the installed plugin root from this routine's own loaded `SKILL.md` path (ordinary shell calls do not inherit a plugin-root environment variable) and run `hooks/tribunal-usage.py observe --thread-id <agent-thread-id>`. The helper reads only metadata and cumulative token-count events from the exact agent session. On `status: observed`, copy its integer `tokens` and component `token_usage`, set `tokens_status: observed`, and copy `source` as `tokens_source` into `lens-completed`. On `status: unavailable`, omit `tokens`, set `tokens_status: unavailable`, and copy `reason` as `tokens_reason`; never turn a parser or capability failure into an unexplained omission. Codex session JSONL is explicitly not a stable extension interface, so this recovery remains best-effort and every changed-format path must degrade to a reason, not block the tribunal.

Gate: every active lens has flushed its `findings/<lens>/` files, and each wave's status is recorded.

## Phase 3 — Triage & per-wave planning · gate: BLOCK

Triage per wave from disk as soon as it flushes; do not wait for the whole run.

- **Calibrate independently.** Set `final_severity`/`final_confidence` from the evidence yourself — the lens's values are provisional input; every critical/high carries a `counter_argument`.
- **Decide per finding, logged.** Each finding gets one decision from the vocabulary, appended as one line to `triage.jsonl`. Below the confidence gate after calibration → `investigate` (medium/low) or `decision-required` (critical/high) — never dropped silently.
- **Plan the wave.** Write `plans/phase-<n>.md` for its kept (`keep`/`combine`) work.
- Procedure: `references/triage.md` — load now.

Gate: every wave's findings triaged into `triage.jsonl` and a `plans/phase-<n>.md` written for its kept work.

## Phase 4 — Report · gate: BLOCK

Regenerate `report.md` and `manifest.yaml` from the two logs per `references/report.md` — projections, never hand-authored. Task-list-structured (not prose): findings grouped by **calibrated** severity then type, each with id, `path:line`, one-line description, remediation shape, triage decision, and a link to its phase plan; `decision-required` in its own section; a launched/skipped-lens summary; an investigate appendix. Apply `${CLAUDE_PLUGIN_ROOT}/includes/anti-slop-design/` (`core` + `medium-documents`) to the prose.

State plainly that critical/high are blocking-severity findings — work that should block shipping the affected code — but that this lane is not itself a gate and blocks nothing.

Gate: `report.md` regenerated from the logs and presented. No issues created.

## Phase 5 — Approval & issue filing · gate: BLOCK

Findings become GitHub issues only on explicit selection and authorization. Silence or ambiguity → file nothing; "looks good" is not authorization.

- **Dedup first.** Skip findings already carrying an `issue_ref` in `triage.jsonl`, then dedup against the tracker — this lane reruns over time and will re-find the same issues.
- **Default is hand-off.** Write and print `issue-commands.sh`; execute only on explicit approval, writing each `issue_ref` back into `triage.jsonl`.
- Findings file as GitHub issues, never `open-tasks.md` — a periodic-review finding must survive PR abandonment.
- Procedure: `references/issue-filing.md` — load now.

Gate: either `issue-commands.sh` written and printed, or — on approval — issues filed with the id→result table and `issue_ref` recorded. Nothing filed without explicit selection; no duplicates against the tracker.

## Phase 6 — Telemetry · gate: STOP

Optional, opt-in KPI feedback to refine the skill and the estimator — off by default, sent only on explicit per-run authorization.

- **Scrub.** The payload is aggregates and per-lens exposure counts only — no code, paths, or finding text; no repo identity unless the user adds `--tag`.
- **Show before send.** Write the payload to the run dir and show it in full; state plainly that it posts publicly to the codeArbiter repo. Default: hand the user the ready command; post only on explicit approval.
- Procedure: `references/telemetry.md` — load now.

Gate: the payload is shown, and it is either handed to the user as a command or — on approval — posted. No telemetry leaves without per-run authorization.

## Hard rules

- MUST NOT proceed past Phase 0 without the user acknowledging the estimated token cost — this lane can cost millions of tokens.
- MUST NOT edit, refactor, format, or commit project code — writes are confined to `.codearbiter/reports/<run-id>/` until the filing gate.
- MUST NOT act as a required gate or block a merge, commit, or other workflow — critical/high are blocking-severity findings, not a pipeline halt.
- MUST NOT record a finding without a concrete `path:line` and a minimal evidence snippet.
- MUST NOT assert an absence without reading the whole relevant unit — partial-window absence claims do not pass.
- MUST NOT let a lens's provisional severity/confidence stand as final — calibrate at triage; every critical/high carries a `counter_argument`.
- MUST NOT mutate the append-only logs — `manifest.yaml`, `report.md`, and `plans/` are regenerated from them, never hand-edited.
- MUST NOT file an issue below the confidence gate or without explicit selection and authorization; findings file as GitHub issues, never `open-tasks.md`.
- MUST NOT create a duplicate issue — skip findings carrying an `issue_ref`, and dedup against the tracker by `dedup_key`/title before filing.
- MUST NOT author or scaffold an ADR — `decision-required` findings file as a discussion issue; ADRs are authored only via `$ca-adr` with user attribution.
- MUST NOT send telemetry without explicit per-run authorization, and MUST NOT include code, file paths, finding text, or repo identity (absent an explicit `--tag`) in the payload — KPI aggregates only.
- MUST NOT guess the test, lint, or secrets-scan command — read `tech-stack.md` or STOP. For the tracker: use `tech-stack.md` if it documents one; else default to `gh issue create` on a GitHub origin; else STOP.
- MUST NOT dispatch a subagent from within a dispatched specialist — only the orchestrator dispatches.
