# SKILL.md-first intake category classification

## Context

GitHub discovery can find valid upstream skills that only provide `SKILL.md`.
Upstream skills are not required to ship `metadata.json`; registry metadata is a
local archive companion generated during intake.

The previous discovery path wrote every downloaded skill into `other`, then
expected later cleanup to migrate obvious categories. A broad discovery batch can
therefore create thousands of publishable but poorly classified `other` entries.

## Design

Discovery intake now classifies from the downloaded `SKILL.md` before choosing an
archive category directory.

Semantic extraction is ordered as:

1. `SKILL.md` frontmatter fields
2. `SKILL.md` body-derived description
3. source path and directory hints
4. generated metadata seed fields

The classifier uses canonical taxonomy keywords and returns an auditable decision:

- `category`
- `status`
- `method`
- `confidence`
- `reason`
- `score`
- `runner_up`
- `runner_up_score`
- `signals`
- `semantic_sources`

High- and medium-confidence matches are archived under the proposed canonical
category. Unresolved, weak, or ambiguous matches remain under `other` with an
explicit low-confidence reason.

## Non-goals

- Do not call an external LLM during publish or discovery intake.
- Do not make `other` a publish blocker.
- Do not treat category confidence as a security decision.
- Do not require upstream `metadata.json`.

## Safety invariants

- Security scanning remains fail-closed and runs before archive writes.
- Case-safe directory naming and stable-key conflict behavior remain in place.
- `other` remains a valid fallback category, but it must be explainable.
- Publish can continue when classification is unresolved.

## Expected effect

New discovery batches should no longer flood `other` simply because upstream
skills lack generated registry metadata. The remaining `other` entries should
represent genuine taxonomy gaps, weak semantic signals, or ambiguity that needs
review.
