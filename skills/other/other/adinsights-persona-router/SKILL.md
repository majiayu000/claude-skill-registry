---
name: adinsights-persona-router
description: Simulate ADinsights owner personas for planning and review workflows. Use when asked for persona simulation, workstream review, owner-style planning, backlog gap review, dependency analysis, or cross-stream escalation guidance tied to ADinsights docs.
---

# ADinsights Persona Router

## Overview

Route ADinsights planning and review requests to the right persona profile, then generate a structured report using repo-defined ownership, tests, and escalation rules. Keep source-of-truth in repo docs and avoid inventing personas, scopes, or contracts.

## Recontext Load Order

1. Open `AGENTS.md`.
2. Open `docs/ops/doc-index.md`.
3. Open `docs/workstreams.md`.
4. Open `docs/project/phase0-backlog-validation.md`.
5. Open `docs/project/phase0-simulated-reviews.md`.
6. Open `docs/project/feature-ownership-map.md`.
7. Open `docs/project/phase1-execution-backlog.md` when task status matters.

## Persona Catalog

Load `references/persona-catalog.yaml` and use it as the canonical list of:

- Persona identity and role.
- Scope ownership and review focus.
- Required tests and doc links.
- Escalation behavior.

## Router Resolution Rules

Resolve persona in this exact order:

1. Explicit persona mention by name (`Maya`, `Lina`, `Raj`, etc.).
2. Explicit stream/workstream ID (`S1`, `Stream 4`, etc.).
3. Folder path hint (`backend/analytics`, `frontend/src`, `dbt/`, etc.).
4. Domain keyword hint (`airbyte`, `dbt`, `snapshot`, `frontend`, etc.).
5. Ask a clarification question only if unresolved after steps 1-4.

If a request spans multiple top-level folders, route to cross-stream behavior and apply Raj/Mira escalation guidance.

### Confidence and Conflict Handling

- Base scores: explicit persona `1.00`, explicit stream `0.90`, folder `0.80`, keyword `0.60`.
- Penalties: `-0.20` per strong conflict, `-0.15` for cross-stream ambiguity.
- Use `confidence_policy` from `references/persona-catalog.yaml`:
  - `auto_resolve_min: 0.75`
  - `clarify_min: 0.55`
- Return `action=clarify` when confidence is low and risk is high (conflicts/cross-stream).

## Operating Mode

- Default mode: planning/review simulation.
- Do not default to code-writing roleplay.
- Simulate owner reasoning, then return action-ready findings tied to real docs/tests.
- CLI entrypoint: `scripts/persona_router.py`.
  - `--mode resolve|preflight`
  - `--format json|markdown`
  - `--path <path>` (repeatable)
  - `--changed-file <path>` (repeatable)
  - `--changed-files-from-git` (optional)

## Output Contract

Default output is a **decision packet** with:

- `schema_version` (`2.1.0`)
- `selected_persona`
- `backup_persona`
- `resolved_by`
- `confidence`
- `conflict_flags`
- `touched_streams`
- `required_tests`
- `docs_to_open`
- `escalation_decision`
- `recommended_report_template`
- `clarifying_question` (only when needed)
- `downstream_recommendations`
  - `invoke_scope_gatekeeper` (`true` when cross-stream or low confidence)
  - `invoke_contract_guard` (`true` when contract-sensitive prompt/path hints are present)
  - `invoke_release_readiness` (`true` only when release/go-live intent is explicit)
- `evidence` entries (`type`, `value`, `strength`, `source`)
- `decision_trace` explainability string

For backward compatibility, the top-level `invoke_scope_gatekeeper` mirrors `downstream_recommendations.invoke_scope_gatekeeper`.

## Handoff Policy

- Persona router remains advisory-only and never hard-blocks.
- Scope concerns are delegated to `adinsights-scope-gatekeeper`.
- Contract validation is delegated to `adinsights-contract-guard`.
- Final go/no-go advisory is delegated to `adinsights-release-readiness`.

Use the templates in `references/report-templates.md`:

- Phase 0 backlog simulation template.
- Implementation planning template.
- Cross-stream escalation template.

## Guardrails

- Preserve tenant isolation and RLS assumptions from `AGENTS.md`.
- Never expose user-level PII; keep analytics aggregated.
- Never log or suggest logging secrets/tokens.
- Keep changes scoped to one top-level folder unless Raj/Mira escalation path is explicit.
- Use the canonical per-folder tests from `docs/workstreams.md` and `docs/ops/testing-cheat-sheet.md`.

## Maintenance

- Keep persona records in `references/persona-catalog.yaml` synchronized with `docs/workstreams.md`.
- Run `scripts/validate_persona_catalog.py` after catalog edits.
- Use `scripts/run_router_golden_tests.py` to verify routing behavior against golden cases.
- Use `scripts/smoke_resolve_persona.py "your prompt"` for backward-compatible smoke checks.
- Run `scripts/sync_to_codex_home.sh` to sync this repo source-of-truth to `$HOME/.codex/skills/adinsights-persona-router/`.
