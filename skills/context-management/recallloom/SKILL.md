---
name: recallloom
description: Use when a task involves continuing a project, restoring project context, maintaining file-based project memory, updating current-state summaries, or recording meaningful progress across sessions. Works best for long-horizon, file-based projects and supports research writing, product document collaboration, software project coordination, and broader cross-functional project continuity.
---

# RecallLoom

RecallLoom is a portable context harness for session-based agents.

It provides a lightweight file model for project continuity across sessions without requiring heavy infrastructure.

The goal is not to remember everything. The goal is to keep the right project state durable, readable, and recoverable across sessions.

## Package Scope

This file is the agent-facing entrypoint for the installable `recallloom/` skill package.

Install and trigger this package through your host agent's normal skill discovery flow.
RecallLoom itself does not require a custom host-specific launcher inside the package.
The package may still ship optional native wrapper templates for supported hosts.

This installable package is intentionally kept lean.
Human-facing repository landing pages and marketing docs may exist upstream, but they are not bundled into the installed skill directory.

In the source repository, `README.md` and `README.en.md` are concise public
front doors, `README.zh-CN.md` is the compatibility entry, `INDEX.md` is the
full map, and `USAGE.md` is the operator guide.
Those files describe the same helper contract as this installed package
entrypoint rather than defining a second logic set.

For package inventory, protocol details, and helper-script behavior, rely on the files that ship inside the package itself:

- `managed-assets.json`
- `package-metadata.json`
- `references/file-contracts.md`
- `references/operation-playbooks.md`
- `references/package-support-policy.md`
- `references/protocol.md`

## Package Facts

<!-- RecallLoom metadata sync start: package-metadata -->
- package version: `0.4.3`
- protocol version: `1.0`
- supported protocol versions:
  - `1.0`
<!-- RecallLoom metadata sync end: package-metadata -->

## Runtime Assumptions

<!-- RecallLoom metadata sync start: runtime-assumptions -->
- Python 3.10 or newer
- supported workspace languages:
  - `en`
  - `zh-CN`
- supported bridge targets:
  - `AGENTS.md`
  - `CLAUDE.md`
  - `GEMINI.md`
  - `.github/copilot-instructions.md`
<!-- RecallLoom metadata sync end: runtime-assumptions -->

## Package Support Gate

RecallLoom package support is separate from project sidecar protocol compatibility.

- Helpers MUST perform the package-support check and MUST NOT write support state into project `.recallloom/`.
- If support is `readonly_only`, mutating helpers MUST block while diagnostic and read-only helpers MAY continue.
- If support is `diagnostic_only`, only diagnostic helpers SHOULD continue.
- If support is `unknown_offline`, diagnostic and read-only actions MAY continue, but mutating actions MUST block until support can be verified.
- Blocked actions MUST return the shared failure contract with `blocked_reason: package_support_blocked` and a `package_support` object. See `references/package-support-policy.md`.

## Public Surface And Required Checks

- Public package and release surfaces MUST stay limited to files a user needs to install, understand, and operate the package.
- Public surfaces MUST NOT include copied project memory, generated runtime output, machine-local data, maintainer-only working files, or material that is not required by the installable package.
- Public CI and required checks MAY validate repository contents and metadata.
- Required-check wording MUST NOT present repository checks as proof of a user's local workspace state, host behavior, or sidecar trust status.

## Non-Invasive Defaults And UX Gates

- Core install and daily use MUST NOT require or auto-install hooks, daemons, watchers, MCP/plugin enforcement, host adapters, telemetry/metrics, or remote payload transmission.
- Native command wrappers are opt-in convenience entrypoints over the same dispatcher, not a required enforcement layer.
- Ordinary docs/source/planning edits outside the managed sidecar stay silent allow or low-friction unless they affect provenance-sensitive RecallLoom state.
- Managed sidecar or provenance-impacting actions surface one of `allow`, `warn`, `ask`, or `block` in helper readiness output when provenance state is relevant.
- `warn` is for low-risk structural-only or readable legacy states and should stay brief; repeated same-session low-risk warnings should be cooldown-friendly.
- `ask` is for legacy review / repair import or reviewed imported baseline actions and requires explicit operator confirmation before higher-risk writes.
- `block` is non-waivable for forged markers, detected receipt/store inconsistency, direct `state.json` / `config.json` edits, privacy violations, and any state classified as `inconsistent_or_tampered_evidence`.
- Do not present remote services, host memory, plugins, MCP, hooks, or wrappers as authority for local helper evidence.
- Receipt-backed mutation is limited to dispatcher-issued managed-file writes, daily-log appends to the current latest cursor, and post-append summary sync. Archive apply and bridge apply remain preview-only until those surfaces gain their own receipt support.

## Write Protocol Red Lines

- Managed sidecar writes MUST use helper scripts. Do not bypass them with blind file replacement, blind patching, or hand-built sidecar files.
- Daily-log writes MUST use `append_daily_log_entry.py` or dispatcher `append`. Do not handwrite `daily-log-entry` markers.
- Overwrite-style managed files MUST use revision-aware helper commits. Do not handwrite `file-state` markers.
- `STORAGE_ROOT/state.json` and `STORAGE_ROOT/config.json` MUST NOT be hand-edited during normal operation.
- Protocol `1.0` daily-log counters are file-local: `entry-seq` is `1..N` within one daily log and canonical `entry-id` is `entry-{entry_seq}`. Do not treat either as globally unique.
- Keep `state.json.daily_logs.entry_count` as `entry_count`; it means the entry marker count in the latest active daily log, not a global cumulative count.
- If a helper write fails, diagnose, fix, retry, then surface the helper failure contract if it still cannot complete.
- Damaged-sidecar recovery MUST use the canonical recovery proposal/review/promotion helpers and `validate_context.py`; do not hand-edit managed markers, `state.json`, `config.json`, receipts, or helper-evidence stores.

## When To Use It

Use RecallLoom when you need to:

- continue an existing project after a pause
- restore project context from maintained files
- maintain current-state project memory
- record meaningful milestone progress
- reduce context drift across sessions or tools

Typical triggers include:

- continue this project
- restore project context
- pick up where we left off
- rl-init
- update the project memory
- record today’s progress
- prepare a clean next-step handoff inside the maintained project files

## First Attach Behavior

On first explicit invocation in a project, RecallLoom should not assume the workspace is already initialized.

The correct flow is:

1. detect whether a valid RecallLoom sidecar already exists
2. if it exists, continue normally without making initialization into extra ceremony
3. if it does not exist, explain that the project is not initialized yet and ask whether initialization should be performed
4. if the user explicitly confirms, or directly says `rl-init`, run the standard initialization action
5. if the environment cannot provide Python `3.10+`, stop with a blocked runtime result instead of hand-building a sidecar

`rl-init` SHOULD mean: initialize the sidecar, validate the workspace, and return next recommended actions. Treat it as a stable high-level action name even when the host does not expose native slash commands.

## Current Action Surface

For the current package line, the stable operator-facing wrapper targets are:

- `rl-init`
- `rl-resume`
- `rl-status`
- `rl-validate`

`rl-init` is the primary operator-friendly first-attach action name.
The others are operator-facing stable action names that can be interpreted by the host agent or mapped into native custom commands when the host supports that surface.
`rl-bridge` remains the canonical dispatcher/helper action label for bridge work, but this package line does not promise a universal native wrapper or deterministic first-hop routing for that label.
Natural language remains the default public phrasing for these actions.

The dispatcher command surface also includes `quick-summary`, `append`, `write`, and `sync-current-state-after-append`.
Use `quick-summary` for current-state snapshots, `append --entry-json` for milestone logging, `write --type ... --source-file <prepared-file> --dry-run` or `write --type ... --stdin --dry-run` before typed managed-file writes, and `sync-current-state-after-append --stdin --input-format json` only after preflight allows `post_append_summary_sync`.
These dispatcher additions are optional for existing `v0.3.4` projects and do not change sidecar protocol `1.0`.

Native wrappers for `rl-init`, `rl-resume`, `rl-status`, and `rl-validate`
are convenience entrypoints only. They must delegate to the same dispatcher and
must not replace natural-language restore requests, bypass helpers, or create a
host-specific product logic copy.

## Initialized-Project Restore Contract

When a host or agent sees a generic initialized-project restore request:

1. check for a valid RecallLoom sidecar before broad skill fan-out
2. if the sidecar is valid, route into the normal RecallLoom fast path
3. let broader memory or workflow systems participate only when the sidecar is missing, conflicting, clearly insufficient, or the user explicitly asks for deeper review

For the current package line, `rl-resume` is the single stable operator-facing action name for that initialized-project restore checkpoint.
Natural-language restore requests are still the primary public path.
Do not invent a manual sidecar fallback or a host-local restore alias that is not backed by the package contract.

## Public Interaction Rules

RecallLoom should default to user task language, not implementation language.

- Prefer “initialize”, “restore”, “import existing project reality”, “continue”, and “record progress”.
- Do not lead with helper names, section keys, or the `coldstart` label unless the user is explicitly doing operator/debug work.
- Keep the first response result-first and action-light: one clear next move is better than exposing routing details.
- Do not invent a manual sidecar fallback when runtime requirements are missing; surface the blocked state and stop.
- This is not hand-building a sidecar; it is the packaged restore and helper contract.

## Fast And Deep Paths

RecallLoom should treat fast path as the default interaction mode.

- Fast path: smallest trustworthy source set, shortest interaction, lowest interruption cost.
- Deep path: only when sources conflict, source coverage is insufficient, risk is too high for a direct recommendation, or the user explicitly asks for deeper review.
- Host-memory inputs remain opt-in and hint-only; their presence should bias the agent toward explicit review instead of silent promotion.

Resume mode selection:

- Use ambient `resume` or `status` when the next agent needs the normal tiered read-plan guidance before deciding what to read.
- Use `resume --fast` when current-state orientation is enough and the next safe move can be chosen from `state.json` plus `rolling_summary.md`.
- Use `resume --full` when stable framing, source-of-truth routing, or project-local `update_protocol.md` guidance is needed before action.
- Keep daily-log evidence on demand through `query_continuity.py`; fast and full resume modes should not expand into daily logs by default.

## Core File Model

RecallLoom uses three primary memory layers:

- `STORAGE_ROOT/context_brief.md`: stable project framing
- `STORAGE_ROOT/rolling_summary.md`: overwrite-style current-state snapshot
- `STORAGE_ROOT/daily_logs/YYYY-MM-DD.md`: append-only milestone evidence
- `STORAGE_ROOT/config.json`: machine-readable workspace settings
- `STORAGE_ROOT/state.json`: machine-readable sidecar state for concurrency-aware helpers
- `STORAGE_ROOT/update_protocol.md`: recommended project-local override layer for read and write behavior

File responsibilities in one sentence:

- `context_brief.md` explains what this project is and how it should be approached.
- `rolling_summary.md` explains what is true right now.
- `daily_logs/` explain what happened at milestone level.
- `config.json` keeps storage and language settings stable.
- `state.json` tracks workspace revision and helper-visible sidecar state.
- `update_protocol.md`, when present, can narrow or strengthen the default read/write rules for this specific project.

`STORAGE_ROOT` is either `PROJECT_ROOT/.recallloom/` or `PROJECT_ROOT/recallloom/`. Exactly one valid storage root MAY exist; if both exist, stop instead of guessing.

Machine-readable markers, not heading labels, are the normative file contract. Protocol `1.0` supports workspace languages `en` and `zh-CN`. See `references/file-contracts.md`.

## Minimum Cold-Start Flow

1. Find the project root.
2. Read `STORAGE_ROOT/config.json`.
3. Read `STORAGE_ROOT/state.json`.
4. Read `STORAGE_ROOT/rolling_summary.md`.
5. If `STORAGE_ROOT/update_protocol.md` exists, surface it before expanding beyond the minimum continuity set.
6. Read `STORAGE_ROOT/context_brief.md` only when the current task needs framing, scope, source-of-truth, or phase context that the summary does not already cover.
7. Read the latest active daily log only when milestone evidence, workday judgment, or external-writer reconciliation requires it.
8. Run a quick freshness check before trusting older context or before a major write.

Cold start should restore and judge first.
It should not automatically continue `next_step` or execute project work just because continuity files were read.

See `references/operation-playbooks.md` for the full flow.

## Current Read-Side Helpers

Three read-side helpers matter here:

- `preflight_context_check.py`: revision-aware freshness review before formal writes; returns handoff-first digests, suggested read targets, write-tier guidance, and trust/drift state.
- `summarize_continuity_status.py`: ambient continuity status surface on the same freshness baseline; returns the same digest family plus shared workday-state and trust/drift guidance.
- `query_continuity.py`: read-only continuity recall surface; returns answer-first recall with `answer`, supporting citations, and a risk/freshness note. It also returns hits, token estimate, budget hint, freshness/conflict state, trust/drift state, an output variant label, and override review targets. Daily-log citations include explicit `date` values, current-state files win ties, and the context window stays bounded.

All attach-safe continuity text returned through these read-side surfaces is expected to respect the shared attached-text scan rules.

## Minimum Write Rules

- Before choosing a write target, read `STORAGE_ROOT/update_protocol.md` if it exists.
- `current_state` changes usually target `rolling_summary.md`.
- `stable_rule` changes usually target `context_brief.md`.
- `milestone_evidence` usually targets the daily log.
- Do not update context files for trivial reads or minor edits with no durable change.

Default exits before any write should stay explicit:

- `no_write` is a normal successful result
- `merge_current_state` updates `rolling_summary.md`
- `append_milestone` appends to the daily log
- `confirm` and `blocked` stop automatic writes rather than guessing

Read-side trust notes:

- `sidecar_trust_state` stays in helper JSON, not in protocol `1.0`
- `state.json.provenance` may store local provenance markers such as `structurally_valid`, `review_imported_baseline`, or `helper_evidenced` after a receipt-finalized helper write; helper JSON still owns operational `provenance_state` routing
- Legacy sidecars without baseline metadata are readable, but write readiness must route through review / repair import before mutating helper writes
- `structurally_valid` and `review_imported_baseline` mean structural/readiness evidence only and MUST NOT be treated as `helper_evidenced`
- Receipt-backed provenance is only claimed after dispatcher-backed receipt finalization writes the optional local receipt store and updates provenance metadata; structural validation alone MUST NOT output `helper_evidenced`
- Default `rl-validate` / `validate_context.py` remains structural and does not read the optional receipt store. Receipt-store validation is explicit: use `--require-provenance` with exactly one scope flag, `--changed-only` or `--full`.
- `continuity_drift_risk_level` is a review signal, not proof that the sidecar is damaged
- `allowed_operation_level` and `write_readiness` help hosts route low-risk read vs review-first vs write-after-preflight flows

Project-local overrides MAY narrow read order, write order, or archive behavior, but they do not replace the core file contract.

## Agent Layered Write Judgment

Before writing continuity content, the agent should make the layer decision itself. Helpers can provide safe write context and static write-tier guidance, but they must not replace agent judgment about what the content means.

Use this quick check before editing managed files:

1. Is there a new durable fact, or is `no_write` the right result?
2. If writing is needed, is the main content `stable_rule`, `current_state`, or `milestone_evidence`?
3. Does the event span multiple layers, so it needs a `multi_layer_split`?
4. Is the same fact already present, so the right action is merge instead of duplicate?
5. Is the layer uncertain enough to `defer` or `confirm` rather than guess?

Layer defaults:

- `stable_rule`: long-lived workflow rules, source-of-truth routing, project boundaries, or recovery facts. Default target: `context_brief.md`.
- `current_state`: what is true now, including current phase, active risks, active judgments, and next steps. Default target: `rolling_summary.md`.
- `milestone_evidence`: completed validations, approvals, releases, accepted decisions, or other durable evidence. Default target: daily log.
- `no_write`, `defer`, and `confirm` are valid outcomes when nothing durable changed, the discussion is unstable, or the boundary needs explicit approval.

When more than one layer is valid, split different facts across layers and do not duplicate the same sentence.

For the detailed rules, conflict order, self-review template, and anonymized calibration cases, see `references/operation-playbooks.md`.

For protocol `1.0`, `update_protocol.md` is a human-reviewed override layer; helpers surface it but do not automatically execute its natural-language rules.

RecallLoom prefers the smallest valid write set. The agent decides what should change and prepares content; helpers decide whether the write is still safe to apply.

When generating workspace files, prefer the user's workspace language when it is supported by protocol `1.0` (`en`, `zh-CN`).

## When Not To Update Context

Do not update context files just because:

- you performed a cold start
- you answered a short question with no durable project change
- you explored without reaching a stable conclusion
- you made wording-only edits

The protocol is designed to reduce noise, not to turn every session into documentation work.

## Profiles

RecallLoom provides four profiles:

- `profiles/general-project-continuity.md`
- `profiles/research-writing.md`
- `profiles/product-doc-collaboration.md`
- `profiles/software-project-coordination.md`

Profiles refine emphasis, evidence handling, and drift risk. Use `general-project-continuity.md` by default; switch to a specialized profile only when the project shape is a high-confidence match.

## What RecallLoom Does Not Try To Be

RecallLoom does not try to be:

- a general-purpose memory server
- a full agent execution runtime
- a replacement for platform-specific instruction files
- a heavy autonomous coding framework

It is the project continuity layer, not the whole agent stack.

## Where To Read More

- `references/protocol.md`
- `references/file-contracts.md`
- `references/operation-playbooks.md`
- `references/anti-patterns.md`
- `references/profiles.md`

## License

This package is released under Apache License 2.0.
