## Repository Policy (Core-First)
- **Core repo is the source of truth** for scripts, workflows, index generation, site outputs, and pipeline docs.
- **Data repo** stores the archived skill tree in category-at-root layout: `<category>/<skill>/SKILL.md` + `<category>/<skill>/metadata.json`.
- **Main repo** is a merged publishing artifact (`core + data`). During publish, the archive is mirrored under `main/skills/**`.
- If behavior or docs conflict across repos, follow **core** implementation and sync others to match.

## Repo Identity Map
- `claude-skill-registry-core`: authority repo for discovery, download, dedupe, security scan, registry generation, search-index generation, Pages, and publish orchestration.
- `claude-skill-registry-data`: archive repo for the heavy skill contents and archive-specific metadata.
- `claude-skill-registry`: merged publish artifact for browsing and compatibility consumers.

## Edit Routing
- If a task touches discovery, download, dedupe, security scan, registry generation, search-index generation, Pages, or dispatch/publish logic, edit `claude-skill-registry-core`.
- If a task touches archived skill bodies, archive-only metadata, or archive README counts/layout, edit `claude-skill-registry-data` or let `core` workflows update it.
- If a task touches merged-artifact packaging that is intentionally main-owned, edit `claude-skill-registry`.
- In `main`, do **not** directly edit generated outputs such as `skills/**`, `registry.json`, `registry_summary.json`, `docs/search-index.json`, `docs/stats.json`, `docs/categories/**`, or pipeline scripts mirrored from `core`.

## Publish Contract
- Canonical flow: `core sync-data -> data commit -> core metadata commit -> core build-index -> main publish-from-core`.
- `main` should use `provenance/merge-source.json` to identify the exact `core_sha` and `data_sha` that produced the current merged artifact.
- If `core` and `main` disagree, treat `core` as authoritative and re-publish `main` instead of patching generated files in place.
- Main-owned workflow exceptions are intentionally excluded by `core/scripts/sync_main_repo.sh`; today that is `.github/workflows/publish-from-core.yml`, `.github/workflows/metadata-compliance.yml`, and the deprecated `.github/workflows/sync-data.yml`.

## Case-Conflict Policy (Core Implementation)
- The filesystem is case-insensitive for many users. **No paths may differ only by case**.
- Use `normalize_name()` and `ensure_unique_dir()` for all skill directory creation.
- Directory conflict suffix policy must match `scripts/utils.py`:
  - Prefer repo suffix: `{name}-{owner}-{repo}` (via `get_repo_suffix()`).
  - Fallback when repo suffix is unavailable: `{name}-{short-hash}`.
  - If needed, append numeric disambiguators: `-2`, `-3`, ...
- Reuse an existing directory when the metadata key resolves to the same skill.
- Do **not** remove skills to resolve conflicts; **rename** with suffixes instead.

## Non-Compatibility Rule
- Backward compatibility for historical directory names is **not required**.
- Prefer deterministic, conflict-free paths aligned with core scripts.
