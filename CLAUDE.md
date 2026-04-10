# CLAUDE.md

This project is a three-repo split. Before editing anything, identify which repo you are in and route the change to the owner repo instead of patching generated outputs in the wrong place.

## Repo Map
- `claude-skill-registry-core`: source of truth for discovery, download, dedupe, security scanning, registry/search-index generation, Pages, and publish orchestration.
- `claude-skill-registry-data`: archive repo. Canonical layout is `<category>/<skill>/SKILL.md` + `<category>/<skill>/metadata.json` at category folders in the repo root.
- `claude-skill-registry`: merged publish artifact. It is rebuilt from pinned `core_sha` + `data_sha`; it is not where canonical pipeline behavior should be invented.

## How To Decide Where To Edit
- Touch `core` for workflows, scripts, pipeline docs, registry/search-index generation, Pages behavior, or publish orchestration.
- Touch `data` for archived skill bodies, archive-only README/counts, or fixes to files that exist only in the archive.
- Touch `main` only for main-owned wiring that `core/scripts/sync_main_repo.sh` intentionally excludes from sync. Current exceptions are `.github/workflows/publish-from-core.yml`, `.github/workflows/metadata-compliance.yml`, and `.github/workflows/sync-data.yml` (deprecated stub).

## Generated vs Owned Files In Main
Treat these as generated in `main` and do not hand-edit them:
- `skills/**`
- `registry.json`
- `registry_summary.json`
- `docs/search-index.json`
- `docs/stats.json`
- `docs/categories/**`
- pipeline scripts copied from `core`

## Publish Flow
1. `core/.github/workflows/sync-data.yml` discovers/downloads skills and updates `data`.
2. `core` rebuilds registry metadata and commits its own outputs.
3. `core/.github/workflows/build-index.yml` rebuilds site/search artifacts and deploys Pages.
4. `core` dispatches `main/.github/workflows/publish-from-core.yml` with pinned `core_sha` and `data_sha`.
5. `main` rebuilds the merged artifact from those pinned refs and records them in `provenance/merge-source.json`.

## Conflict Resolution
- If `core` and `main` disagree, trust `core` and re-publish `main`.
- If `data` README counts differ from reality, fix the updater in `core` rather than manually editing numbers in multiple repos.
- If local checkouts disagree with GitHub, verify remote branch heads first; remote `main` is the operational source of truth.
