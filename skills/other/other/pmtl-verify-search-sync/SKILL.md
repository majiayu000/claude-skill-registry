---
name: pmtl-verify-search-sync
description: PMTL_VN search verification skill. Use when changing search schemas, Meilisearch integration, indexing, fallback search behavior, or search result mapping so index sync is checked with commands and health probes.
---

# PMTL Verify Search Sync

## Purpose

Verify PMTL search behavior, index freshness, and fallback integrity so search-related changes are checked against the current design-first model instead of assumed from code reading.

## Use When

- Changing search schemas, Meilisearch integration, indexing, reindex flows, fallback behavior, or search result mapping.
- Touching admin search ops, source freshness reporting, or index sync/replay paths.
- Reviewing whether search still degrades safely when the engine is unavailable.

## Required Inputs

- touched search surface: query path, index sync, admin ops, or result mapping
- active engine/runtime assumptions for the current environment
- whether the task expects contract verification, engine verification, or both

## Expected Output

- Evidence about search freshness, reindex behavior, and engine health for the touched path.
- A clear note when the helper only covers part of the changed search surface.

## Execution Approach

1. Identify whether the change affects query shape, result mapping, index sync, admin ops, or engine fallback.
2. Run the helper lane first for fast evidence.
3. Read the current search owner docs before trusting the helper as complete coverage.
4. Add targeted checks when the change touches contracts or UI semantics beyond raw reindex health.

## Default workflow

1. Rebuild or batch reindex posts.
2. Check Meilisearch health.
3. Inspect search status, freshness, or fallback behavior if the index does not update.

## Script

Primary entrypoint: `py infra/tools/codex_actions.py search-sync ...`

Compatibility wrapper: `scripts/run_search_sync_check.py`

```bash
py infra/tools/codex_actions.py search-sync --all-pages
py infra/tools/codex_actions.py search-sync --page 1 --limit 100
```

## Verification

- Confirm the helper command exit code and engine health before claiming search is healthy.
- If the change touched contracts, also verify response shape against the design contract rather than only checking engine availability.
- If Meilisearch or worker lanes are not active for the current scope, state that verification stayed on the current active path.
- When search fallback is part of the task, verify that failure does not corrupt canonical content ownership.

## Quality Criteria

- Verification distinguishes query-path correctness, index freshness, and engine-health status.
- Search helper output is not over-interpreted as full FE/API/search-contract coverage.
- Findings stay aligned with PMTL rules: SQL fallback, source-of-truth in DB, no search index authority drift.

## Edge Cases

- Current helper is still biased toward the existing reindex + engine-health lane; it is not a full search UX or contract verifier.
- Search changes that affect result mapping or `docType/entryType/sourceFamily` need doc-level contract checks in addition to command output.
- If Meilisearch is not the active engine, say so plainly instead of pretending full sync was verified.

## Read when needed

- `design/06-search/contracts.md`
- `design/06-search/meilisearch-architecture.md`
- `design/tracking/api-route-inventory.md`
- `docs/runbooks.md`
- `docs/troubleshooting.md`

## Pair with

- `pmtl-production-baseline` for runtime/search policy drift.
- `pmtl-verify-quality-gate` after meaningful code changes.
