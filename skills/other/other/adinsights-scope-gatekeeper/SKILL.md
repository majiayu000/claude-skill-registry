---
name: adinsights-scope-gatekeeper
description: Evaluate ADinsights scope risk for AI coding sessions. Use when requests may span multiple top-level folders, require Raj/Mira escalation, touch architecture-sensitive files, or change API/data contracts and release governance.
---

# ADinsights Scope Gatekeeper

## Overview

Assess proposed or detected file scope against ADinsights guardrails, then return an advisory decision packet that includes escalation routing, folder-level tests, and scope-owned docs maintenance signals.

## Context Load Order

1. Open `AGENTS.md`.
2. Open `docs/workstreams.md`.
3. Open `docs/ops/escalation-rules.md`.
4. Open `docs/runbooks/release-checklist.md`.
5. Open `references/scope-rules.yaml`.

## Inputs and Evidence Priority

Use these inputs in this order:

1. `--changed-files-from-git` output if provided and non-empty.
2. Explicit path hints (`--changed-file` and `--path`).
3. Prompt-extracted path hints.

If no reliable path evidence exists, return `WARN_UNCLEAR_SCOPE`.

## Decision Outcomes

Return exactly one status:

- `PASS_SINGLE_SCOPE`
- `WARN_UNCLEAR_SCOPE`
- `ESCALATE_CROSS_SCOPE`
- `ESCALATE_ARCH_RISK`
- `ESCALATE_CONTRACT_RISK`

Always treat results as advisory-first; do not hard-block.
Contract risk is signal-first and delegated to contract guard for final contract classification.

## Output Contract

Return a scope packet with:

- `schema_version` (`1.1.0`)
- `scope_status`
- `touched_top_level_folders`
- `required_reviewers`
- `required_tests_by_folder`
- `required_docs_updates`
- `recommended_next_action`
- `rationale`
- `evidence` entries (`type`, `value`, `strength`, `source`)
- `contract_risk_signal`
- `contract_risk_reasons`
- `handoff_recommendations`
  - `invoke_contract_guard`
  - `invoke_release_readiness`

## Router Handoff

If a persona-router packet indicates `invoke_scope_gatekeeper=true`, run this skill before implementation planning.
When `contract_risk_signal=true`, invoke `adinsights-contract-guard` before merge planning.

## Guardrails

- Keep single-top-level-folder rule as the default path.
- Route cross-folder changes to Raj.
- Route architecture-sensitive changes to Raj + Mira.
- Use contract-risk signals only to route review/handoff; do not make final breaking-change decisions or require contract docs updates here.
- Keep recommendations aligned with AGENTS test matrix and runbooks.

## Maintenance

- Keep rules in `references/scope-rules.yaml` synchronized with AGENTS and workstream docs.
- Run `scripts/validate_scope_rules.py` after rules edits.
- Run `scripts/run_scope_golden_tests.py` before syncing.
- Sync with `scripts/sync_to_codex_home.sh`.
