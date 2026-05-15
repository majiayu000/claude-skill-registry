# Registry Sharding and Size Guard Spec

## Status

Draft for implementation.

Tracking issues:

- Plan and spec: https://github.com/majiayu000/claude-skill-registry-core/issues/57
- Category and search shards: https://github.com/majiayu000/claude-skill-registry-core/issues/58
- Full registry shards: https://github.com/majiayu000/claude-skill-registry-core/issues/59
- Generated artifact size guard: https://github.com/majiayu000/claude-skill-registry-core/issues/60
- Workflow guard wiring: https://github.com/majiayu000/claude-skill-registry-core/issues/61
- Optional database read model: https://github.com/majiayu000/claude-skill-registry-core/issues/62

## Problem

The generated registry artifacts are approaching GitHub single-file limits and
already create large client downloads.

Current published evidence from May 14, 2026:

- `claude-skill-registry/registry.json`: 94,973,820 bytes.
- `claude-skill-registry/docs/categories/other.json`: 90,811,715 bytes.
- `claude-skill-registry/docs/search-index.json`: 50,607,336 bytes.
- `claude-skill-registry-data` repository size reported by GitHub: about 533 MB.
- Data archive tree: 228,729 `SKILL.md` files and 228,729 `metadata.json` files.
- Data archive top-heavy category: `other` has 130,804 archived skills.

GitHub rejects files above 100 MiB. The next growth cycle can make `main`
publishing fail even when discovery, download, security scan, and data pushes
are healthy.

Category-only sharding is insufficient because the `other` category alone is
near the same limit. The fix must shard both the full registry and large
category/search outputs.

## Decision

Keep `claude-skill-registry-data` as the source of truth and introduce static
generated shards in the merged `claude-skill-registry` publish artifact. The
core repo owns the generator and can rebuild the same artifacts locally, but
the public full-registry URLs must target the merged publish artifact unless
core also commits those generated files.

Do not move catalog source-of-truth storage to an external database for this
first fix.

Reasons:

- The data archive is already a public, auditable, reproducible source tree.
- The core publish pipeline can rebuild derived artifacts from `core + data`.
- A database would add credentials, migrations, availability, backup, and
  replay concerns before solving the immediate 100 MiB publish risk.
- Existing Supabase schema is for community interactions
  (`likes`, `views`, `ratings`, `comments`), not canonical catalog data.

An external database can be added later as a derived read model for server-side
search and recommendations. It must not replace the archive source of truth.

## Goals

1. Keep every generated publish artifact below 80 MiB in normal operation.
2. Fail publish before any generated file reaches 90 MiB.
3. Preserve deterministic static publishing: no runtime service is required to
   browse or consume the registry.
4. Keep a small summary endpoint for badges and automation.
5. Provide manifest-driven access for full registry consumers.
6. Keep backward compatibility for counts and light search first; full
   `registry.json` compatibility can be transitional and compressed-only.

## Non-Goals

- Do not migrate archive contents out of `claude-skill-registry-data`.
- Do not introduce a required backend service for the static website.
- Do not hand-edit generated files in `claude-skill-registry`.
- Do not solve all metadata quality or deduplication issues as part of this
  change.
- Do not require historical category names or paths to stay compatible beyond
  the existing generated artifact contract.

## Repository Routing

Follow the core-first policy:

- `claude-skill-registry-core` owns shard generation, manifests, size gates,
  docs, Pages indexes, and publish orchestration.
- `claude-skill-registry-data` continues to store archived skill bodies and
  metadata in category-at-root layout.
- `claude-skill-registry` remains a generated merged artifact. It receives
  generated shards and manifests from core publish.

## Output Contract

### Summary

Keep:

```text
registry_summary.json
```

Required fields:

```json
{
  "schema_version": 1,
  "registry_updated_at": "2026-05-14T04:20:29.516992Z",
  "total_count": 155422,
  "plugin_count": 3
}
```

This file remains the stable count/badge endpoint.

### Full Registry Manifest

Add:

```text
registry-manifest.json
```

Required fields:

```json
{
  "schema_version": 1,
  "generated_at": "2026-05-14T04:20:29.516992Z",
  "total_count": 155422,
  "plugin_count": 3,
  "shard_strategy": "sha256-install-branch-prefix",
  "shard_count": 256,
  "record_key": "install|branch",
  "provenance": {
    "core_repo": "majiayu000/claude-skill-registry-core",
    "core_sha": "...",
    "data_repo": "majiayu000/claude-skill-registry-data",
    "data_sha": "..."
  },
  "summary": "registry_summary.json",
  "shards": [
    {
      "id": "00",
      "path": "registry-shards/00.json",
      "gzip_path": "registry-shards/00.json.gz",
      "count": 612,
      "bytes": 374215,
      "gzip_bytes": 84217,
      "sha256": "..."
    }
  ],
  "plugins": {
    "path": "plugins.json",
    "count": 3
  }
}
```

### Full Registry Shards

Add:

```text
registry-shards/<00-ff>.json
registry-shards/<00-ff>.json.gz
```

Shard id is the first byte of:

```text
sha256("<install>|<branch>")
```

Each shard file shape:

```json
{
  "schema_version": 1,
  "shard": "00",
  "generated_at": "2026-05-14T04:20:29.516992Z",
  "count": 612,
  "skills": []
}
```

Records use the same full skill entry shape currently written to
`registry.json`.

### Category Manifests and Shards

Replace large single category payloads with:

```text
docs/categories/index.json
docs/categories/<category>/manifest.json
docs/categories/<category>/part-000.json
docs/categories/<category>/part-000.json.gz
```

`docs/categories/index.json` points to category manifests rather than giant
category files:

```json
{
  "updated_at": "...",
  "categories": [
    {
      "name": "other",
      "code": "oth",
      "count": 130804,
      "manifest": "categories/other/manifest.json"
    }
  ]
}
```

Category part size target:

- Target: under 10 MiB uncompressed per part.
- Hard fail: any category part above 80 MiB.
- Parting strategy: stable sort by stars descending, then name, then install;
  split after size estimation.

### Search Index Manifest

Keep first paint small:

```text
docs/search-index-lite.json
docs/search-index-lite.json.gz
```

Add shard manifest for full search:

```text
docs/search-index-manifest.json
docs/search-shards/<00-ff>.json
docs/search-shards/<00-ff>.json.gz
```

The website must load `search-index-lite.json` first. Full search can load
search shards lazily:

- Load one shard when browsing by exact install/hash.
- Load all shards only when the user explicitly requests full offline search.
- Future server-side search can replace this without changing archive storage.

## Transitional Compatibility

### `registry.json`

Phase 1 keeps a small compatibility file:

```json
{
  "version": "2.2.0",
  "updated_at": "...",
  "total_count": 155422,
  "plugin_count": 3,
  "registry_skill_count_dedup": 155422,
  "archive_skill_md_count_raw": 228729,
  "archive_metadata_count_raw": 228729,
  "manifest": "registry-manifest.json",
  "deprecated_full_payload": true,
  "message": "Full registry payload moved to registry-shards/*.json"
}
```

This intentionally stops publishing the full `skills` array in
`registry.json`. Core metadata commits may omit the `manifest` field when the
manifest and shard files are not committed in the same repo tree; the merged
publish artifact includes the pointer because it publishes those files
together.

### Compressed Full Dump

Optional transitional artifact:

```text
registry-full.json.gz
```

This artifact is for bulk consumers that need one full dump. It is not required
for the website and must also pass size checks.

## Generator Changes

### `scripts/rebuild_registry.py`

Add a shard writer path:

1. Scan archive as it does today.
2. Deduplicate using the existing `repo:path` / fallback key logic.
3. Build `registry_summary.json`.
4. Write `registry-manifest.json`.
5. Write `registry-shards/*.json` and `.json.gz`.
6. Write the small compatibility `registry.json`.
7. Optionally write `registry-full.json.gz`.

The script must remove stale shard files before writing new output.

### `scripts/build_search_index.py`

Change output generation:

1. Keep `featured.json`.
2. Keep `search-index-lite.json` as the default browser startup index.
3. Replace single large category files with category manifests and parts.
4. Add full search shards and `search-index-manifest.json`.
5. Keep stats fields for old sizes and add shard fields:
   - `registry_manifest_size_bytes`
   - `registry_shard_count`
   - `registry_largest_shard_bytes`
   - `category_largest_part_bytes`
   - `search_shard_count`
   - `search_largest_shard_bytes`

### `docs/js/app.js`

Change initial load:

1. Fetch `search-index-lite.json` first.
2. Fetch `featured.json`, `categories/index.json`, and `plugins.json` as today.
3. Do not fetch `search-index.json` on startup.
4. Show clear UI state when full search is loading.
5. Load category parts on category browsing or leaderboard expansion.

## Size Guard

Add a core script:

```text
scripts/check_generated_file_sizes.py
```

Default thresholds:

- Warning: 80 MiB.
- Failure: 90 MiB.

Inputs:

```text
--root .
--warn-mib 80
--fail-mib 90
--include registry.json
--include registry-shards
--include docs
```

Behavior:

- Recursively scan included generated paths.
- Print largest files in descending order.
- Exit non-zero if any file exceeds failure threshold.
- Emit warnings for files above warning threshold.
- Ignore `.git`, caches, and test artifacts.

Workflow placement:

- In `core/sync-data.yml`, run after registry rebuild and before data/core
  commits.
- In `core/build-index.yml`, run after index build and before Pages artifact
  upload.
- In main `publish-from-core.yml`, run after rebuilding main and before commit.

## External Database Position

External database is not the primary fix.

Allowed future use:

- Derived read model for search.
- Aggregated popularity/ranking.
- Community interactions.
- Analytics and recommendation queries.

Requirements if added:

- Rebuildable from `core + data`.
- No unique catalog data that only exists in the database.
- Idempotent upsert job keyed by stable skill id.
- Export job to static shards remains supported.
- Site can degrade to static shards when DB is unavailable.

Existing Supabase interaction tables can stay separate from catalog storage.

## Migration Plan

### Phase 0. Measurement

- Confirm current largest generated files.
- Add `docs/stats.json` fields for largest generated file and shard readiness.
- No behavior change.

### Phase 1. Size Guard

- Add `scripts/check_generated_file_sizes.py`.
- Wire it into `sync-data`, `build-index`, and main publish.
- Set fail threshold to 95 MiB for the first merge if needed, then lower to
  90 MiB after sharding lands.

### Phase 2. Registry Shards

- Implement `registry-manifest.json` and `registry-shards/*`.
- Replace full `registry.json` with the small compatibility pointer.
- Update README API docs.
- Add tests for deterministic shard assignment and stale shard cleanup.

### Phase 3. Category and Search Shards

- Split `docs/categories/<category>.json` into manifests and parts.
- Add `docs/search-index-manifest.json` and search shards.
- Change website startup to `search-index-lite.json`.
- Keep old single category files only if they stay under threshold; otherwise
  do not write them.

### Phase 4. Optional Full Dump

- Add `registry-full.json.gz` only if consumers need a one-file export.
- Document it as bulk export, not the normal API.

### Phase 5. Optional Database Read Model

- Add catalog tables only after static sharding is stable.
- Treat DB as derived and disposable.
- Keep static shards as fallback and public export path.

## Tests

Required unit tests:

- Stable shard id is deterministic for `install|branch`.
- Same skill always lands in the same shard.
- Shard manifest count equals total shard record count.
- Stale shard files are deleted before rewrite.
- Small compatibility `registry.json` does not contain `skills`.
- Category part manifest count equals total category part records.
- Size guard returns success, warning, and failure cases.

Required integration tests:

- Rebuild registry from a fixture archive and verify all manifests/shards.
- Build search index from a fixture archive with a large `other` category and
  verify category parting.
- Website startup fixture references `search-index-lite.json`, not
  `search-index.json`.

Required workflow validation:

- `python -m pytest`
- `python scripts/check_generated_file_sizes.py --root <fixture> --fail-mib 90`
- `bash -n scripts/sync_main_repo.sh`

## Done When

- No generated file in the checked publish artifact exceeds 80 MiB after a
  normal daily run.
- Publish fails before any generated file exceeds 90 MiB.
- `registry_summary.json` still reports the correct deduplicated skill count.
- `registry-manifest.json` points to all full registry shards.
- `docs/categories/index.json` points to category manifests, and `other` is no
  longer a single large JSON file.
- The website first paint does not require downloading `search-index.json`.
- `sync-data`, `build-index`, main publish, and Pages deploy succeed after the
  migration.
- Existing data archive remains the source of truth.

## Open Questions

1. Do any external consumers require the current full `registry.json` with a
   top-level `skills` array?
2. Should `registry-full.json.gz` be generated in core, main, Pages, or all
   three?
3. Should shard count be fixed at 256, or should it be manifest-configurable?
4. Should category parts target count-based splitting or byte-size splitting?
5. Should full offline browser search be an explicit button to avoid accidental
   large downloads?
