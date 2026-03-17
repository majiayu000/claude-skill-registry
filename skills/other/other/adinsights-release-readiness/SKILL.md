---
name: adinsights-release-readiness
description: Synthesize ADinsights release readiness from router, scope, contract, docs, and optional validation checks. Use when deciding go/no-go readiness, release gate status, or pre-merge release risk.
---

# ADinsights Release Readiness

## Overview

Aggregate readiness evidence and return a gate decision packet across scope, contract integrity, tests, observability, security, and runbook/documentation readiness. This skill is advisory-first and supports optional command execution.

## Context Load Order

1. Open `AGENTS.md`.
2. Open `docs/runbooks/release-checklist.md`.
3. Open `docs/runbooks/deployment.md`.
4. Open `docs/runbooks/operations.md`.
5. Open `docs/project/api-contract-changelog.md`.
6. Open `docs/project/integration-data-contract-matrix.md`.
7. Open `references/release-gates.yaml`.

## Inputs

Primary packet inputs:

- Router packet (`--router-packet`)
- Scope packet (`--scope-packet`)
- Contract packet (`--contract-packet`)

Optional execution input:

- `--run-checks` to execute configured readiness commands.
- `--changed-files-from-git` to include diff context in documentation/compliance reasoning.

## Gate Model

Return exactly one status:

- `GATE_PASS`
- `GATE_WARN`
- `GATE_BLOCK`

Gate dimensions:

- `scope_control`
- `contract_integrity`
- `test_coverage`
- `observability`
- `security_pii_secrets`
- `runbook_ops_readiness`
- `documentation_completeness`
- `rollout_rollback_plan`

Gate dimension statuses:

- `PASS`
- `INFO` (pending evidence/action; does not escalate release status)
- `WARN`
- `BLOCK`

## Output Contract

Return a release decision packet with:

- `schema_version` (`1.1.0`)
- `release_status`
- `gate_results`
- `blocking_issues`
- `warnings`
- `pending_items`
- `required_approvers`
- `required_artifacts`
- `recommended_next_action`
- `evidence` entries (`type`, `value`, `strength`, `source`)
- `executive_summary`

## CLI Interface

Use `scripts/evaluate_release_readiness.py`:

- `--prompt "<text>" --format json|markdown`
- `--router-packet "<path>"`
- `--scope-packet "<path>"`
- `--contract-packet "<path>"`
- `--run-checks`
- `--changed-files-from-git`

One-command full-chain preflight (router -> scope -> contract -> release):

- `scripts/run_preflight_skillchain.py --prompt "<text>" --format json|markdown`
- Optional: `--path <path>` (repeatable), `--changed-file <path>` (repeatable), `--changed-files-from-git`
- Optional: `--run-checks` to execute release optional checks
- Optional: `--output-dir <dir>` to persist packet JSON files

## Default Behavior

- Synthesis-first packet evaluation.
- Optional checks only when `--run-checks` is set.
- Advisory wording only; no hard-block language.

## Maintenance

- Keep `references/release-gates.yaml` aligned with release checklist/runbooks.
- Run `scripts/validate_release_gates.py` after rules edits.
- Run `scripts/run_release_golden_tests.py` before syncing.
- Sync with `scripts/sync_to_codex_home.sh`.
