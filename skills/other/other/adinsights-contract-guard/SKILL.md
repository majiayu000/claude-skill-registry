---
name: adinsights-contract-guard
description: Detect and classify ADinsights API/data/integration contract risk for planning and review. Use when prompts or file changes touch serializers, API schemas, dbt models, Airbyte connector schemas, or contract documentation updates.
---

# ADinsights Contract Guard

## Overview

Classify contract-impact risk for a proposed change and return an advisory contract decision packet with required docs, tests, reviewers, and next actions. This skill owns contract classification; scope gatekeeper only emits contract risk signals.

## Context Load Order

1. Open `AGENTS.md`.
2. Open `docs/project/api-contract-changelog.md`.
3. Open `docs/project/integration-data-contract-matrix.md`.
4. Open `docs/runbooks/release-checklist.md`.
5. Open `references/contract-rules.yaml`.
6. Open `references/contract-surfaces.md` when classification is ambiguous.

## Inputs and Evidence Priority

Use evidence in this order:

1. `--changed-files-from-git` output if enabled and non-empty.
2. Explicit paths from `--changed-file`.
3. Path hints from router/scope packets.
4. Prompt-extracted path hints.
5. Prompt semantic hints (keywords only).

## Decision Outcomes

Return exactly one contract status:

- `PASS_NO_CONTRACT_CHANGE`
- `WARN_POSSIBLE_CONTRACT_CHANGE`
- `ESCALATE_CONTRACT_CHANGE_REQUIRES_DOCS`
- `ESCALATE_BREAKING_CHANGE`

## Strictness Model

- Default/local mode is advisory (`exit 0`).
- `--ci-strict` remains backward-compatible and maps to strict level `breaking_only`.
- `--ci-strict-level breaking_only` returns non-zero for `ESCALATE_BREAKING_CHANGE`.
- `--ci-strict-level breaking_or_missing_docs` returns non-zero for both `ESCALATE_BREAKING_CHANGE` and `ESCALATE_CONTRACT_CHANGE_REQUIRES_DOCS`.

## Output Contract

Return a contract decision packet with:

- `schema_version` (`1.0.0`)
- `contract_status`
- `breaking_change_detected`
- `contract_surfaces_touched`
- `required_docs_updates`
- `required_reviewers`
- `required_tests`
- `rationale`
- `evidence` entries (`type`, `value`, `strength`, `source`)
- `next_actions`

## CLI Interface

Use `scripts/evaluate_contract.py`:

- `--prompt "<text>" --format json|markdown`
- `--changed-file "<path>"` (repeatable)
- `--changed-files-from-git`
- `--router-packet "<path-to-json>"`
- `--scope-packet "<path-to-json>"`
- `--ci-strict`
- `--ci-strict-level breaking_only|breaking_or_missing_docs`

## Guardrails

- Contract guard is advisory unless CI strict mode is explicitly enabled.
- Never suppress required contract docs updates for touched contract surfaces.
- Keep PII/secrets guidance aligned with `AGENTS.md`.

## Maintenance

- Keep `references/contract-rules.yaml` aligned with API/data contract docs.
- Run `scripts/validate_contract_rules.py` after rules edits.
- Run `scripts/run_contract_golden_tests.py` before syncing.
- Sync with `scripts/sync_to_codex_home.sh`.
