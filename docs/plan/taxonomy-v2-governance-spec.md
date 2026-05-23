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

## LLM Review Contract

`scripts/review_category_plan_with_llm.py` can run a bounded second-pass review
against an existing migration plan. It is intentionally separate from
`plan_category_migration.py` so deterministic planning remains reproducible and
offline.

Defaults:

- OpenAI-compatible endpoint: `https://token-plan-sgp.xiaomimimo.com/v1`.
- Model: `mimo-v2.5-pro`.
- API key source: `MIMO_API_KEY`.
- Candidate actions: `heuristic_reclassify` and `resolve_source_conflict`.
- Selection order: `risky-first`, reviewing `low`, then `medium`, then `high`.
- Optional checkpoint: `--checkpoint-jsonl <path>` appends one JSONL row per
  completed review and `--resume` skips matching completed `review_key` values.
- Apply mode: `review-only`.

The review report contains:

- `schema_version`, `generated_at`, `source_plan`, `model`, `base_url`,
  `policy`, `summary`, `reviews`, and `notes`.
- Per review: candidate path/name/action, current category, heuristic proposed
  category, model proposed category, model confidence, decision, parse status,
  reason, evidence, and a stable `review_key`.
- `decision`: `agree`, `override`, or `uncertain`.
- `parse_status`: `ok`, `invalid_json`, `unknown_category`,
  `invalid_confidence`, or `api_error`.

Secrets must not be written to files or committed. The report records the
environment variable name, never the API key value. API errors are represented
as `uncertain` review rows so failed model calls are visible in the audit trail.
Checkpoint rows are append-only audit records. Malformed checkpoint lines are
ignored for resume and counted in `malformed_checkpoint_row_count`.

## Confidence Rules

- `high`: declared taxonomy deprecation, or heuristic score at least 4 with a
  strong delta, or `other` to a strong keyword target.
- `medium`: clear target, but not enough evidence for high confidence.
- `low`: weak signal or conflicting category sources.

High confidence does not mean auto-apply. It means the item is suitable for a
small reviewed migration batch.

## Apply Contract

`scripts/apply_category_migration.py` converts reviewed classification results
into a concrete directory move plan. It is separate from planning and LLM review
so archive mutations stay explicit.

Defaults:

- Input is a classification JSONL with `path`, `current_category`,
  `llm_category`, `confidence`, and `status`.
- Minimum confidence is `0.9`.
- Only active target categories are eligible unless `--target-status` expands
  the allow-list.
- `other` is not an eligible target unless `--allow-target-other` is passed.
- Default mode is dry-run. Only `--apply` mutates the archive.
- `--movable-only` can be used for execution batches that should skip blocked
  duplicates and fill the requested `--limit` with apply-ready moves.

The apply plan records:

- `operation`: `move` or a blocked operation such as `blocked_existing_key`.
- `source_skill`, `target_skill`, source/current/target categories.
- `confidence`, stable metadata `key`, repo suffix context, and reason.

Apply mode:

- refuses plans containing blocked moves;
- moves only standard `<category>/<skill>/SKILL.md` directories;
- updates `metadata.json` with the new `category` and `dir_name`;
- never deletes or overwrites skills to resolve conflicts.

## Residual Audit Contract

`scripts/audit_category_residuals.py` explains what remains after an apply
batch. It is report-only and must run before deciding whether another migration
batch is safe.

The residual report separates two views:

- `same_policy_plan_summary`: recomputed by `apply_category_migration.py` with
  the same flags, proving whether the selected policy still has apply-ready
  moves or blocked duplicates.
- current archive residuals: based on source paths that still exist in the
  archive, so rows that point at old pre-migration paths are counted as source
  missing instead of being treated as live `other` skills.

The report records:

- archive category counts and scoped archive counts;
- source state counts (`exists`, `missing`, or non-standard path);
- mutually exclusive primary reason counts;
- overlapping blocker reason counts;
- target category/status distributions and bounded representative examples.
- optional stable-key conflict details via `--conflict-detail-limit`, including
  source/target paths, metadata identity fields, SKILL content hashes, and
  equality flags.

Residual reason buckets include low confidence, target category/status excluded
by policy, target `other`, classification status/path failures, stable-key
conflicts, source missing, current archive category filtered out, and movable
candidates under the selected policy.

Stable-key conflict details are diagnostic only. Matching stable keys are not
enough to delete or merge archive entries; a follow-up cleanup must first prove
whether the source and target SKILL bodies are identical or intentionally
different.

## Stable-Key Duplicate Cleanup Contract

`scripts/plan_stable_key_duplicate_cleanup.py` consumes a residual report that
was generated with `--conflict-detail-limit`. It is the only approved automatic
cleanup path for stable-key conflicts.

Defaults:

- Input is a residual report with `details.stable_key_conflicts`.
- Default mode is dry-run. Only `--apply` removes source directories.
- Source and target `SKILL.md` hashes must match.
- Metadata identity fields must match unless
  `--allow-metadata-identity-drift` is explicitly passed after review.
- Apply mode re-reads the source and target hashes before deleting anything.

The cleanup plan records `remove_duplicate` operations only. It never rewrites,
renames, merges, or overwrites skills. Non-identical conflicts remain residuals
for manual or model-assisted review.

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
6. Run the residual audit with the same policy to prove what remains and why.
7. Publish main from pinned core/data refs.
8. Re-run audit and compare `other` share, category conflicts, residual
   reasons, and plan deltas.

## Acceptance Criteria

- Current taxonomy loads as schema v2 and has no governance errors.
- Deprecated categories can produce migration targets without changing current
  resolution behavior.
- A migration plan can be generated without modifying the archive.
- The plan reports deprecations, aliases, source conflicts, heuristic
  reclassifications, confidence bands, and category pair counts.
- A residual audit can explain post-apply live leftovers separately from
  already-moved classification rows.
- Generated category artifacts are guarded so legacy category JSON files remain
  pointer-only.
