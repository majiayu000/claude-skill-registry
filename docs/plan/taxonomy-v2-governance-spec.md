# Taxonomy v2 Governance and Migration Spec

## Problem

The archive now has a clean two-level layout, but semantic category quality is
still uneven. The first post-layout audit found 229,302 standard-layout skills,
76 categories, 131,935 skills in `other`, and 6,766 reviewable reclassification
candidates. Category names also mix stable user-facing buckets with historical
or import-derived buckets such as `test`, `docs`, `specialized-testing`, and
`utility`.

The next step must not be a blind bulk move. Category changes affect published
URLs, search filters, install discovery, and downstream consumers. Every
category change needs a reproducible reason and a review path.

## Goals

- Make `taxonomy/categories.yaml` the versioned source of truth for category
  names, aliases, status, parent relationships, and deprecation targets.
- Keep generated classification suggestions deterministic and reviewable.
- Separate category-name governance from per-skill reclassification.
- Prevent regressions where legacy category compatibility files grow back into
  large full-payload JSON.
- Leave the data archive untouched until a migration plan is reviewed.

## Non-Goals

- Do not automatically apply the 6,766 heuristic candidates.
- Do not directly edit generated files in the merged main artifact.
- Do not delete skills to resolve category or directory conflicts.
- Do not require historical metadata compliance cleanup as part of this work.

## Taxonomy v2 Schema

`taxonomy/categories.yaml` uses `schema_version: 2`.

Each category keeps the existing fields:

- `slug`: stable canonical identifier.
- `code`: compact search-index code.
- `display_name`: user-facing label.
- `aliases`: accepted inbound names that resolve to the canonical slug.
- `keywords`: deterministic text signals used for audit scoring.

Taxonomy v2 adds governance fields:

- `status`: `active`, `review`, or `deprecated`. Missing status defaults to
  `active`.
- `description`: user-facing inclusion rule.
- `parent`: optional parent category for review and reporting.
- `migrate_to`: required when `status: deprecated`; points to an active or
  review category.

Status meaning:

- `active`: stable enough for new skills.
- `review`: allowed but suspicious, broad, or still under naming review.
- `deprecated`: existing archive entries may remain temporarily, but migration
  plans should propose `migrate_to`.

## Migration Plan Contract

`scripts/plan_category_migration.py` emits JSON with:

- `schema_version`
- `generated_at`
- `skills_dir`
- `policy`
- `summary`
- `changes`
- `notes`

Each change contains:

- `action`: `taxonomy_deprecation`, `normalize_alias`,
  `resolve_source_conflict`, or `heuristic_reclassify`.
- `confidence`: `high`, `medium`, or `low`.
- `review_required`: boolean.
- `path`, `name`, `current_category`, `proposed_category`.
- `target_path_preview`: non-authoritative preview for human review.
- `raw_sources`: directory/metadata/frontmatter values.
- `resolved_sources`: taxonomy-normalized source values.
- `score`, `current_score`, `signals`, and `reason` where applicable.

The plan is review-only. A later apply tool must recompute collision-safe
targets using the same deterministic directory rules as the existing archive
normalizers.

## Confidence Rules

- `high`: declared taxonomy deprecation, or heuristic score at least 4 with a
  strong delta, or `other` to a strong keyword target.
- `medium`: clear target, but not enough evidence for high confidence.
- `low`: weak signal or conflicting category sources.

High confidence does not mean auto-apply. It means the item is suitable for a
small reviewed migration batch.

## Governance Gates

Taxonomy gate:

- `scripts/check_taxonomy_governance.py` fails on schema and relationship
  errors.
- It warns on broad active names, missing descriptions, long compact codes, and
  deprecated categories that still attract keywords.
- CI runs the gate in the Python test workflow.

Category artifact gate:

- `scripts/check_category_artifacts.py` verifies every
  `docs/categories/<category>.json` compatibility file is a small pointer.
- It fails if a pointer contains `skills`, lacks `deprecated_full_payload`, lacks
  a manifest reference, references a missing manifest, or exceeds the pointer
  size limit.
- Build and publish paths run the gate after search/category index generation.

## Operating Flow

1. Update taxonomy status/name semantics in core.
2. Run taxonomy governance validation.
3. Generate a review-only migration plan against the data archive.
4. Review by action, confidence, and category pair.
5. Apply only small, high-confidence batches in data PRs.
6. Publish main from pinned core/data refs.
7. Re-run audit and compare `other` share, category conflicts, and plan deltas.

## Acceptance Criteria

- Current taxonomy loads as schema v2 and has no governance errors.
- Deprecated categories can produce migration targets without changing current
  resolution behavior.
- A migration plan can be generated without modifying the archive.
- The plan reports deprecations, aliases, source conflicts, heuristic
  reclassifications, confidence bands, and category pair counts.
- Generated category artifacts are guarded so legacy category JSON files remain
  pointer-only.
