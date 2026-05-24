# Derived Catalog Read Model Spec

Issue: https://github.com/majiayu000/claude-skill-registry-core/issues/62

## Position

The catalog database is optional and derived. It must never replace the data
repo or generated static artifacts as the source of truth.

Source of truth remains:

- `claude-skill-registry-core` for scripts, registry generation, search-index
  generation, security signals, and publish orchestration.
- `claude-skill-registry-data` for archived skill content and metadata.
- Static shards in the merged publish artifact for public export and fallback.

## Allowed Uses

A database read model may be used for:

- server-side search and ranking experiments
- aggregated popularity/ranking queries
- analytics and recommendation queries
- community interaction joins that do not create unique catalog facts

It must not store catalog-only data that cannot be rebuilt from core plus data.

## Data Model

Minimum tables:

- `catalog_skills`
  - `skill_id` primary key, matching `build_search_index.get_stable_id(install, branch)`
  - `install`
  - `branch`
  - `name`
  - `description`
  - `repo`
  - `path`
  - `category`
  - `tags`
  - `stars`
  - `quality_score`
  - `quality_grade`
  - `security_status`
  - `install_status`
  - `trust_score`
  - `source_content_sha256`
  - `registry_generated_at`
  - `updated_at`
- `catalog_security_decisions`
  - `skill_id`
  - `decision_id`
  - `status`
  - `reason`
  - `scanner_name`
  - `scanner_version`
  - `ruleset_sha256`
  - `source_repo`
  - `source_path`
  - `source_ref`
  - `content_sha256`
  - `scanned_at`
- `catalog_import_runs`
  - `run_id`
  - `core_sha`
  - `data_sha`
  - `registry_manifest_sha256`
  - `search_manifest_sha256`
  - `started_at`
  - `finished_at`
  - `status`

The importer may add provider-specific indexes, but not provider-specific
catalog fields that have no static-artifact equivalent.

## Idempotent Upsert

Importer input is the generated artifact set:

- `registry-manifest.json` and `registry-shards/*.json`
- `docs/search-index-manifest.json` and `docs/search-shards/*.json`
- `docs/quality-index-manifest.json` and shards
- `docs/security-index-manifest.json` and shards
- `docs/ranking-index-manifest.json` and shards
- `provenance/merge-source.json` when importing the merged publish artifact

Upsert key is `skill_id`. Re-running the same artifact set must produce the
same database rows except for import-run timestamps.

Deletes are handled by marking rows absent from the latest import as inactive,
or by replacing all rows inside a transaction after a complete import. Partial
imports must not change the active catalog view.

## Fallback Contract

The static site must load static shards first or keep an equivalent fallback
path available. If the database is unavailable, stale, or missing a record, the
site must degrade to static shards.

Required fallback checks:

- DB search unavailable: load `search-index-lite.json`, then search shards.
- DB record missing: resolve from registry/search shards by `skill_id`.
- DB security signal missing: treat as unknown, not clean.
- DB import stale relative to provenance: prefer static artifacts.

## Security And Operations

- Database credentials must be environment-provided secrets.
- Importer writes must use parameterized queries or provider SDK methods.
- Importer must fail closed on malformed generated artifacts.
- Importer must report row counts and manifest hashes for every run.
- No public endpoint may expose database credentials or service keys.

## Done When

This issue can be closed when:

- the read model is documented as derived-only
- idempotent upsert keys are defined
- static shards remain the fallback and public export path
- no unique catalog data is allowed to exist only in the database
