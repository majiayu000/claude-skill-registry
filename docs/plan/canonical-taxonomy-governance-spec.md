# Canonical Taxonomy Governance and Migration Spec

## Problem

The archive has a clean two-level layout, but semantic category quality is still
uneven. Historical import names, broad buckets, and stale model decisions can
leave skills in categories that are not good user-facing browsing choices.

The taxonomy must be a single current contract, not a family of product-version
lines. Old category names may be useful evidence during audit, but they are not
compatibility promises and must not make legacy inputs valid publish categories.

## Goals

- Treat `taxonomy/categories.yaml` as the only current category contract.
- Keep generated classification suggestions deterministic, reviewable, and
  reproducible.
- Reject unknown or legacy categories at publish boundaries.
- Route legacy names and uncertain inputs into explicit review queues.
- Keep archive mutations separate from planning, model review, and audit.

## Non-Goals

- Do not automatically apply heuristic or model classification candidates.
- Do not directly edit generated files in the merged publish artifact.
- Do not preserve old category names as compatibility obligations.
- Do not delete skills to resolve category or directory conflicts.

## Taxonomy File Contract

`taxonomy/categories.yaml` is the source of truth for category metadata. Its
`schema_version` is only a machine-readable file-format field for parsers and
tests; it is not a public taxonomy product version.

Each category declares:

- `slug`: canonical identifier.
- `code`: compact search-index code.
- `display_name`: user-facing label.
- `keywords`: deterministic text signals used for audit scoring.
- `status`: `active`; missing status is `active`.
- `description`: inclusion rule or migration context.
- `inclusion_rule`: required user-facing boundary for active categories.
- `exclusion_rule`: required neighboring-category boundary for active categories.
- `examples`: required concrete examples for active categories.
- `parent`: optional reporting relationship.

Only `active` categories are publishable. `other` is an active fallback bucket,
but it should shrink through reviewed migrations.

Legacy names live in the top-level `legacy_migrations` map, outside the
publishable category set. Entries may define a deterministic `target` or mark
the old slug as `review_required`. Default resolution does not use legacy
mappings. Any tool that wants to inspect them must opt in explicitly and keep
the result review-only.

## Classification Boundary Rules

- Source intake should provide a canonical slug.
- Unknown category input is not silently accepted as safe.
- Legacy names are reported as migration or review items rather than silently normalized.
- Model output is accepted only when it names an active canonical category.
- Legacy categories may appear in reports, but they are not valid publish targets.

## Model-Facing Classification Contract

The residual classifier prompt treats the taxonomy file as the model's category
rulebook, not just a list of names. Its payload must include every active
category's slug, display name, inclusion rule, exclusion rule, examples, and
keywords. The model must use those boundaries before choosing a category.

The only valid model output category is a slug present in the active
`allowed_categories` payload. Broad natural labels that are not canonical
categories are invalid even when they look useful. Current blocked labels and
their canonical routing hints are:

- `automation`: route by outcome to `workflow`, `productivity`, `devops`,
  `orchestration`, `integration`, or `platform`.
- `research`: route by method or domain to `analysis`, `domains`, `product`, or
  `ai-ml`.
- `education`: route by artifact or learning outcome to
  `personal-development`, `documents`, or `domains`.
- `content`: route by content job to `writing`, `marketing`, `generation`, or
  `documents`.

If none of the canonical targets is defensible, the model may choose `other`
only as a last-resort fallback with confidence `<= 0.65`. The apply step still
rejects `other` by default, so this preserves fail-closed behavior instead of
turning uncertainty into a migration.

## Migration Plan Contract

`scripts/plan_category_migration.py` emits JSON with:

- `schema_version`, `generated_at`, `skills_dir`, `policy`, `summary`,
  `changes`, and `notes`.
- Per change: `action`, `confidence`, `review_required`, `path`, `name`,
  `current_category`, `proposed_category`, `target_path_preview`,
  `raw_sources`, `resolved_sources`, `score`, `current_score`, `signals`, and
  `reason`.

The plan is review-only. A later apply tool must recompute collision-safe
targets using the same deterministic directory rules as the archive
normalizers.

Legacy findings use `legacy_category_migration` when a deterministic target
exists and `legacy_category_review` when SKILL.md-first reclassification is
required. They are not publish-time compatibility behavior.

## Model Review Contract

`scripts/review_category_plan_with_llm.py` runs a second-pass review against an
existing migration plan. It stays separate from deterministic planning so the
base plan remains reproducible and offline.

Defaults:

- OpenAI-compatible endpoint: `https://token-plan-sgp.xiaomimimo.com/v1`.
- Model: `mimo-v2.5-pro`.
- API key source: `MIMO_API_KEY`.
- Candidate actions: `heuristic_reclassify`, `legacy_category_review`, and
  `resolve_source_conflict`.
- Selection order: `risky-first`, reviewing `low`, then `medium`, then `high`.
- Optional checkpoint: `--checkpoint-jsonl <path>` appends one JSONL row per
  completed review and `--resume` skips matching completed `review_key` values.
- Apply mode: `review-only`.

The allowed category payload contains only active canonical categories. Unknown,
inactive, malformed, or missing model outputs are kept as non-`ok` rows so
downstream migration stays fail-closed.

For residual classification, the allowed category payload also includes
inclusion rules, exclusion rules, examples, keywords, and blocked-label guidance
so MiMo is choosing from the same current category contract operators review.

Secrets must not be written to files or committed. Reports record the
environment variable name, never the API key value.

## Reclassification Batch Contract

`scripts/build_current_other_reclassification_batch.py` cuts reviewable batches
directly from the live archive instead of stale pre-migration rows. The default
scope is current `other`, but the command accepts explicit current categories
for targeted cleanup.

Each batch writes:

- `input.jsonl`: one SKILL.md-first work item per selected live archive skill.
- `manifest.json`: batch id, source archive, selection policy, artifact paths,
  summary counts, and the exact follow-up command sequence.

Each input row includes the current archive path, semantic name, description,
tags, semantic source map, content excerpt, and provenance hashes for
`SKILL.md`, `metadata.json`, and the semantic text used for review.

The manifest command sequence is:

1. Run `scripts/classify_residual_workset_with_llm.py` against `input.jsonl`.
2. Run `scripts/sample_category_classification_audit.py` to produce a
   deterministic review sample from classification output plus source context.
3. Run `scripts/apply_category_migration.py` in review-only mode to build a
   high-confidence, active-category move plan.
4. Run `scripts/audit_category_residuals.py` to explain what remains blocked
   before the next batch starts.
5. Run `scripts/build_residual_category_worksets.py` to split classification
   gaps, low-confidence rows, target-`other` rows, and inactive targets into
   explicit next-batch inputs.

This contract is intentionally batch-first. Large `other` migrations must be
split into reviewable chunks; a single blind mega-apply is not a valid publish
path.

## Apply Contract

`scripts/apply_category_migration.py` converts reviewed classification results
into a concrete directory move plan. It is separate from planning and model
review so archive mutations stay explicit.

Defaults:

- Input rows include `path`, `current_category`, `llm_category`, `confidence`,
  and `status`.
- Minimum confidence is `0.9`.
- Only active target categories are eligible unless an operator explicitly
  widens `--target-status` for a diagnostic run.
- `other` is not an eligible target unless `--allow-target-other` is passed.
- Default mode is dry-run. Only `--apply` mutates the archive.
- `--movable-only` skips blocked duplicates and fills the requested `--limit`
  with apply-ready moves.
- If classification rows include `source_sha256` or `metadata_sha256`, apply
  planning recomputes the live archive hashes and rejects stale rows whose
  source files changed since model review.

Apply mode refuses blocked plans, moves only standard
`<category>/<skill>/SKILL.md` directories, updates `metadata.json`, and never
deletes or overwrites skills to resolve conflicts.

## Residual Audit Contract

`scripts/audit_category_residuals.py` explains what remains after an apply
batch. It is report-only and must run before another migration batch is
accepted.

The residual report separates:

- `same_policy_plan_summary`: recomputed by `apply_category_migration.py` with
  the same flags.
- live archive residuals: based on source paths that still exist in the
  archive.

Residual reason buckets include low confidence, target category/status excluded
by policy, target `other`, classification status/path failures, stable-key
conflicts, source missing, current archive category filtered out, and movable
candidates under the selected policy.

## Governance Gates

Taxonomy gate:

- `scripts/check_taxonomy_governance.py` fails on schema and relationship
  errors.
- `--strict-canonical` fails if taxonomy definitions still contain non-active
  transitional categories, inbound aliases, or category-level migration targets.
- `--publish-category <slug>` fails when a publish target is unknown or legacy.
- Active categories must declare `inclusion_rule`, `exclusion_rule`, and at
  least one example.
- The default report includes canonical and noncanonical category counts so
  category cleanup progress is visible.

Source intake gate:

- `scripts/validate_sources.py` accepts only active canonical category slugs in
  curated `sources/*.json` files.
- Missing, legacy, unknown, or formatted-but-not-canonical categories are
  errors, not warnings.

Category artifact gate:

- `scripts/check_category_artifacts.py` verifies every
  `docs/categories/<category>.json` file is a small pointer.
- It fails if a pointer contains `skills`, lacks `deprecated_full_payload`,
  lacks a manifest reference, references a missing manifest, or exceeds the
  pointer size limit.
- `scripts/check_canonical_categories.py` verifies archive directories,
  metadata categories, registry shards, search docs, stats, and category
  artifacts use only active canonical categories and category codes.
- It also checks category count consistency across
  `docs/categories/index.json`, category pointers, category manifests, manifest
  part counts, category parts, and `docs/stats.json`.

## Operating Flow

1. Update category status/name semantics in core.
2. Run taxonomy governance validation.
3. Generate a review-only migration plan against the data archive.
4. Review by action, confidence, and category pair.
5. Apply only small, high-confidence batches in data PRs.
6. Run residual audit with the same policy.
7. Build residual worksets for gaps, low confidence rows, inactive targets, and
   target-`other` rows before running another model pass.
8. Reclassify worksets with checkpoints and apply only `ok`, active,
   high-confidence rows through the migration planner.
9. Publish from pinned core/data refs.
10. Re-run audit and compare `other` share, category conflicts, residual
    reasons, and plan deltas.

## Acceptance Criteria

- Docs and workflow messages describe a canonical taxonomy, not a named product
  version line.
- Historical legacy names do not silently become valid publish
  categories.
- Publish target validation fails on unknown or legacy categories.
- Model review accepts only active canonical categories.
- Residual model classification prompts include taxonomy inclusion/exclusion
  boundaries and blocked-label guidance for common noncanonical proposals.
- Migration planning still produces audited review queues for unknown and legacy
  inputs.
