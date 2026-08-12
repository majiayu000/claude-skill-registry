# Canonical Bundled Asset Backfill

Tracks #259. The archive audit originated in #260 and now uses
`scripts/audit_skill_assets.py`; secure downloads and application use
`scripts/backfill_skill_assets.py` and the production sync downloader.

## Problem

The historical archive often stores only `SKILL.md` and `metadata.json`, even
when the skill references scripts, templates, or reference documents. Measured
against the 2026-04-21 snapshot of 227,820 skills:

| Metric | Value |
|---|---|
| Pure-markdown skills (no local file references) | 48.2% |
| Claimed-EXEC candidates (>=100 stars, deduped by repo+dir) | 348 |
| Verified to ship executable assets upstream | 79 (57 repos) |
| Verified to ship docs/template assets only | 53 |
| Claim is false — upstream dir is SKILL.md-only | 109 (31%) |
| Upstream deleted or moved within ~3 months of archiving | 106 (30%) |

The missing files are the least regenerable part of a skill, while stale or
incorrect file claims are currently indistinguishable from verified archives.
A one-time fetch is insufficient because upstream paths also decay.

## Constraints

- The existing category-at-root archive is canonical:
  `<category>/<skill>/SKILL.md` plus `metadata.json` and bundled files.
- No parallel `curated/` tree, duplicate skill identity, or compatibility alias
  is created.
- A backfill uses only the exact repo, `SKILL.md` path, and source branch already
  recorded in the archive. The branch is resolved to an immutable commit SHA
  before any file is downloaded.
- Downloads reuse the production allowlist, size/count limits, security scanner,
  naming rules, and metadata generation.
- The default backfill mode validates a complete batch in temporary storage.
  `--apply` is explicit and replaces canonical directories only after every
  target passes validation.
- Bundled files are distributed but never executed by this pipeline.

## Canonical Metadata

After a successful backfill, the existing `metadata.json` is preserved and the
production downloader refreshes these fields:

```json
{
  "repo": "acme/tools",
  "path": "skills/alpha/SKILL.md",
  "github_branch": "main",
  "github_commit_sha": "<40-character commit sha>",
  "assets_verified_at": "2026-08-01T00:00:00Z",
  "asset_liveness": "live",
  "assets_liveness_checked_at": "2026-08-08T00:00:00Z",
  "assets_liveness_sha": "<current 40-character branch-head sha>",
  "archive_mode": "directory",
  "bundled_files": ["scripts/run.py", "references/guide.md"]
}
```

`bundled_files` must exactly match the regular files present below the canonical
skill directory, excluding `SKILL.md` and `metadata.json`. An empty or truncated
bundle is a failed backfill, not a successful skill-md-only refresh.

`github_commit_sha` and `assets_verified_at` describe the immutable archived
snapshot and are never refreshed by liveness checks. The `assets_liveness_*`
fields describe the latest successful upstream observation. Transient GitHub/API
errors leave the previous observation unchanged and appear only in the run report.

## Delivery Phases

### Phase 1 — inventory and deterministic targets

1. Audit actual archive files rather than trusting metadata declarations.
2. Report claim, local verdict, archive mode, metadata mismatch, ambiguous stable
   keys, and candidate counts.
3. Emit exact-path JSONL targets only for unambiguous, currently asset-free
   canonical archives that claim assets and meet the configured star floor.

### Phase 2 — secure pinned backfill

1. Resolve the archive's recorded branch to an immutable GitHub commit SHA.
2. Download the exact declared `SKILL.md` path and allowed sibling assets through
   the production downloader and security scanner.
3. Reject missing, empty, truncated, mismatched, symlinked, or changed targets.
4. Validate the whole batch in temporary storage; on `--apply`, preserve existing
   metadata and atomically replace canonical directories with batch rollback.
5. Emit a structured report for downloader, validation, application, and recovery
   failures.

### Phase 3 — continuous liveness verification

1. Recheck the pinned source identity on a schedule without deleting archived
   files when upstream moves or disappears.
2. Record live, moved, gone, and verification-error outcomes without presenting
   stale checks as fresh successes.
3. Fail the workflow when decay exceeds the configured threshold.

The existing weekly `full` sync profile performs this check before committing
data-repository changes. The gate fails when more than 35% of targets are
`partial`, `moved`, or `gone`, when more than 10% have upstream verification
errors, or when no verified targets are found. Local validation and metadata
apply/rollback errors always fail regardless of percentage; the 10% tolerance
applies only to transient upstream verification errors. Its structured report is
retained as the `asset-liveness-report` workflow artifact.

### Phase 4 — registry and search visibility

1. Surface verified asset state and liveness from canonical metadata in registry
   records and the search index.
2. Expose verified asset/liveness facets and rank verified-live records above
   otherwise equal unverified records.
3. Down-rank only; do not hide or remove pure-markdown skills.

Registry records and the full/lite search records publish `asset_state`,
`asset_liveness`, `bundled_file_count`, immutable verification SHA/time, and
latest liveness SHA/time only when the declared bundle exactly matches regular
files in the canonical archive directory. Invalid or incomplete claims publish
no asset fields. Compact search shards use `a` for `asset_state` and `l` for
`asset_liveness`.

Ranking applies no bonus: verified-live records have a zero asset penalty,
while otherwise equal records without live evidence receive a small down-rank.
Pure-markdown and decayed skills remain present in every generated catalog.

## Failure Behavior

- Missing or invalid repo/path/branch metadata fails closed.
- Commit resolution, listing, download, security scan, or bundle-limit failures
  produce a failed target and no partial canonical archive.
- If the destination changes after targets are generated, the batch is rejected.
- Any failed swap attempts to restore every previously replaced directory; an
  incomplete recovery reports the retained backup paths.
- Registry/search generation must omit asset claims it cannot validate rather
  than manufacture defaults.

## Done When

- The inventory reports actual archive state and emits deterministic exact-path
  targets without case-only conflicts or duplicate stable keys.
- Backfills record an immutable commit SHA, preserve existing metadata, and make
  `bundled_files` exactly match the canonical directory.
- Empty/truncated bundles, stale targets, scanner exceptions, and swap failures
  are covered by tests and fail without silent degradation.
- Scheduled liveness verification has completed against real upstream movement.
- Registry/search surfaces verified asset and liveness state without creating a
  second archive root.
- Every new script meets the repository's coverage and changed-line gates.

## Open Questions

1. The star floor controls API and archive growth; lowering it below 100 requires
   an explicit capacity decision.
2. Full-directory redistribution makes upstream license handling more important
   than archiving `SKILL.md` alone; license policy remains a release gate.
3. Threshold changes from the initial 35% decay / 10% error policy require an
   explicit capacity and incident-response decision.
