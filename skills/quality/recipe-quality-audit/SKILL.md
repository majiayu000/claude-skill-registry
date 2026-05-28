---
name: recipe-quality-audit
description: >-
  Audit NVCA recipe quality: check file inventory, metadata schema, field-to-replacement
  coverage, ambiguous keys, smart quotes, test fixtures, and fill quality. Produces a
  structured scorecard per recipe with maturity tier classification. Use when user says
  "audit recipe quality," "check recipe coverage," "recipe scorecard," or "NVCA recipe
  quality."
license: MIT
compatibility: >-
  Internal skill for the open-agreements development workflow.
  Requires local CLI and repository access.
metadata:
  author: open-agreements
  version: "0.1.0"
catalog_group: Developer Workflows
catalog_order: 10
---

# recipe-quality-audit

Audit a single NVCA recipe's quality and produce a structured scorecard.

## Security model

- This skill operates on **local repository files only** — no network access required.
- Source document downloads (Tier 2 checks) use `ensureSourceDocx()` which fetches from known template source URLs only.
- No credentials or API keys are needed.

## Usage

Run the audit for a specific recipe:
```
Audit the recipe: nvca-certificate-of-incorporation
```

Or audit all recipes:
```
Audit all NVCA recipes and update the quality tracker
```

## Checks

### Tier 1: Structural (no source download needed)

| # | Check | How |
|---|-------|-----|
| S1 | File inventory | Does recipe have metadata.yaml, replacements.json, clean.json? Optional: computed.json, normalize.json, selections.json |
| S2 | Metadata schema valid | Run existing `validateRecipeMetadata()` from `src/core/metadata.ts` |
| S3 | Field-to-replacement coverage | For each field in metadata, is there a replacement key referencing `{field_name}`? |
| S4 | Ambiguous keys | Flag replacement keys < 8 chars without context qualifier (e.g., `[name]`, `[its]`) |
| S5 | Smart quote coverage | Keys with apostrophes should have smart-quote variants (or patcher normalizes — check patcher has normalizeQuotes) |
| S6 | Source SHA present | `source_sha256` in metadata.yaml |
| S7 | Test fixture exists | `integration-tests/fixtures/{recipe-id}-*.json` exists |

### Tier 2: Behavioral (requires source download)

| # | Check | How |
|---|-------|-----|
| B1 | Source download + scan | Count all `\[[_A-Z]` prefixed bracket patterns in source (underscore-fill or capitalized placeholders) |
| B2 | Replacement coverage ratio | (keys with match in source) / (total bracket patterns). Target: >80% |
| B3 | Unmatched underscore patterns | `[___+]` patterns in source not in replacements.json |
| B4 | Clean effectiveness | After clean, no footnotes, no "Note to Drafter", no preamble |

### Tier 3: Fill quality (requires fill run)

| # | Check | How |
|---|-------|-----|
| F1 | Default-only fill | Fill with defaults, run verifyOutput, count blank placeholders |
| F2 | Full-values fill | Fill with all fields from test fixture, assert all verify checks pass |
| F3 | Formatting anomaly count | Check 8 from verifier (single-char underlined runs) |
| F4 | Zero-match replacement keys | Keys that existed in replacements.json but matched nothing in the source |

## Output: Quality Scorecard

```json
{
  "recipe_id": "nvca-voting-agreement",
  "maturity": "beta",
  "scores": { "structural": "6/7", "behavioral": "3/4", "fill": "0/4", "total": "9/15" },
  "checks": [
    { "id": "S1", "name": "File inventory", "passed": true, "details": "metadata.yaml, replacements.json, clean.json present" },
    { "id": "S7", "name": "Test fixture exists", "passed": false, "details": "No fixture matching integration-tests/fixtures/nvca-voting-agreement-*.json" }
  ],
  "field_coverage": { "metadata_fields": 14, "replacement_refs": 10, "uncovered": 4 },
  "recommendations": [
    "Add test fixture for fill testing (S7)",
    "Add replacement keys for 4 uncovered fields (S3)"
  ]
}
```

## Maturity Tiers

- **scaffold**: metadata-only, can't fill
- **beta**: has replacements + clean, score < 11/15 OR no test fixture
- **production**: score >= 11/15 AND has test fixture AND has computed.json (if conditional sections exist in source)

## Workflow

When running the audit:

1. Read `content/recipes/QUALITY_TRACKER.md` for current state
2. Run Tier 1 checks (always possible)
3. Run Tier 2 checks if source document is available (use `ensureSourceDocx()`)
4. Run Tier 3 checks if a test fixture exists
5. Compute scorecard and maturity tier
6. Output the scorecard as JSON
7. Update the quality tracker if requested

## Implementation Notes

- Use `validateRecipeMetadata()` from `src/core/metadata.ts` for S2
- Use `ensureSourceDocx()` from `src/core/recipe/downloader.ts` for B1-B4
- Use `runRecipe()` from `src/core/recipe/index.ts` for F1-F4
- Bracket pattern detection uses `\[[_A-Z]` prefix to avoid counting citations and legal references
- Zero-match keys come from `PatchResult.zeroMatchKeys` returned by the patcher
- Cross-reference zero-match keys with `cleanConfig.removeRanges` and `cleanConfig.removeParagraphPatterns` to suppress expected zero-matches
