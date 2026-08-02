---
name: web-ppt-template-distiller
description: Score and distill high-quality online PPT or presentation template preview pages into reusable paired gpt-image2-ppt style Markdown and layout JSON. Use when the user wants to mine, select, rate, filter, or distill web PPT templates from sites such as Slidesgo without downloading PPTX files, especially when only visually strong templates should be converted into styles.
---

# Web PPT Template Distiller

## Workflow

Use this skill when converting online presentation template previews into reusable style prompts.

Run the bundled script first. Do not distill every candidate blindly.

```bash
python <skill-root>/scripts/score_and_distill.py \
  --url https://slidesgo.com/theme/modern-business-proposal \
  --style-id modern-business-proposal \
  --name "Modern Business Proposal"
```

The script performs this workflow:

1. Extract public preview images from explicit template detail URLs.
2. Score template quality and write `quality_report.json`.
3. Distill only if `total_score >= --min-score` and `decision == accept`.
4. Optionally run a low-cost one-cover validation.
5. In closed-loop mode, revise the profile from structured failures and validate again.
6. Record progress, dedupe keys, scores, decisions, rounds, and output paths in SQLite.

Every successful distillation writes one executable pair: `<style-id>.md` plus
`<style-id>.layouts.json`. Markdown is the human/model-facing rendering; the JSON profile is
authoritative and the layout sidecar is the machine-facing runtime input. Never emit or promote a
Markdown-only style. All automatic modes request the complete reusable-profile grammar and pass the
same structural contract before writing this pair; `--validate-style` and `--closed-loop` change
visual validation depth, not profile richness or runtime format.

Default staged style directory:

```bash
.ppt-template-distill/staged_styles
```

Keep all intermediate distillation artifacts in the current working directory. Copy a style into the target `gpt-image2-ppt-skills/styles/` directory only after the user explicitly reviews and approves it.

## Selection Rules

Use a conservative quality gate.

- Accept only templates with a coherent visual system, multiple useful slide types, clear hierarchy, stable 16:9 previews, and reusable layout language.
- Reject templates that are generic, visually noisy, low resolution, mostly screenshots, watermark-heavy, inconsistent across pages, or dependent on copyrighted/recognizable illustrations that cannot be abstracted.
- Never copy original images, icons, photos, logos, characters, watermarks, or source text into the final style file.
- Distill abstract rules only: palette, grid, typography mood, spacing, image treatment, decorative vocabulary, and page-type layouts.

For the detailed rubric, read `references/quality_rubric.md` when adjusting thresholds or interpreting scores.

## Commands

Dry-run candidate image extraction:

```bash
python <skill-root>/scripts/score_and_distill.py \
  --url <template-url> \
  --dry-run
```

Score only, without distilling:

```bash
python <skill-root>/scripts/score_and_distill.py \
  --url <template-url> \
  --score-only
```

Batch visually related templates:

```bash
python <skill-root>/scripts/score_and_distill.py \
  --input urls.txt \
  --style-id my-distilled-style \
  --name "My Distilled Style" \
  --min-score 78
```

Use `--force-distill` only when the user explicitly wants a marginal candidate distilled despite the score.

Batch independent styles, one URL per style:

```bash
python <skill-root>/scripts/score_and_distill.py \
  --input urls.txt \
  --batch-one-per-url \
  --limit 100 \
  --resume \
  --min-score 78
```

For a low-cost one-pass smoke validation, add `--validate-style`. With no role override it generates one cover, and only a hard rejection blocks the staged style pair. It requires `OPENAI_API_KEY` plus `VISION_*`. Add `--validation-roles ...` only when you explicitly want a larger one-pass check. This changes validation depth, not the output format.

For the full repair loop, use:

```bash
python <skill-root>/scripts/score_and_distill.py \
  --url <template-url> \
  --style-id <style-id> \
  --name "<Style Name>" \
  --closed-loop \
  --max-validation-rounds 2 \
  --min-validation-score 82 \
  --min-page-score 74
```

`--closed-loop` implies multi-page validation. Each failed-but-repairable round writes a diagnostic report, asks the vision model to revise the complete profile, and generates the validation pages again. Keep the round cap small because every round generates one image per selected role. Read `references/closed-loop-validation.md` when changing roles, thresholds, report fields, or terminal-state behavior.

Before any paid validation image, the distiller checks the reusable-profile contract and permits at most two complete-profile structural repairs by default. Missing source evidence, canonical roles, routing, capacity, evidence mapping, or the required metrics plus table/timeline data coverage stops the run before image generation if the repairs still fail. Tune with `--max-profile-repairs`; keep the cap small because each repair is a multimodal call, even though it does not generate a slide image.

To resume a previously repaired profile without repeating extraction or distillation, pass its JSON
back through the same contract gate:

```bash
--profile-json <work-dir>/<style-id>/style_profile.json --resume
```

Validation images are cached by role. For an intermittently unavailable image endpoint, configure a
small outer retry window around the generator's built-in quick retries:

```bash
DISTILL_IMAGE_RETRY_ROUNDS=4 DISTILL_IMAGE_RETRY_DELAY_SECS=45 \
python <skill-root>/scripts/score_and_distill.py ...
```

Do not use retries to weaken a gate or regenerate pages that already succeeded. If a later repair
round cannot finish, the loop records `generation-failed` and retains the prior champion; if the
first round cannot finish, the run remains failed/review-only and publishes nothing.

Closed-loop publication is monotonic: round 1 establishes a champion; later rounds replace it only when weak roles improve by the configured delta, successful sentinel roles stay within the regression budget, copying risk does not worsen, and text accuracy passes. The final output uses the champion round, not automatically the latest attempt. Tune only when justified:

```bash
--min-round-improvement 3 \
--max-role-regression 2 \
--min-text-accuracy 90
```

For reusable roles, prefer multiple content-routed archetypes instead of one universal composition. `layout_bank.<role>` may use a compact single-archetype object or a list of archetypes. Each archetype should include `id`, `composition`, `zones`, `content_capacity`, machine-readable `routing`, `evidence_pages`, anchors, variants, and avoid rules. Both authoring forms compile into the same flat runtime layout list.

Before promoting a broadly reusable style, run the held-out generalization suite. It keeps the standard cover/section/content/metrics cases, adds comparison and mixed table+timeline content, and sends every case through the same production router used by `generate_ppt.py`:

```bash
--closed-loop --validation-suite generalization
```

Keep the standard suite for cheaper iteration. Use the generalization suite for pilot migration and final promotion; a pass on only the fixed metrics case does not establish reusable data-layout coverage.

When upgrading an installed style, include its paired Markdown as a baseline. The tool first requires
the new candidate to pass closed-loop validation, then renders the installed and candidate styles
from identical held-out cases and performs one pairwise visual comparison. Publication additionally
requires aggregate net improvement, bounded per-role fit/readability regression, low copying risk,
and candidate text accuracy above the configured threshold:

```bash
--closed-loop \
--validation-suite generalization \
--baseline-style <gpt-image2-ppt-skills>/styles/<style-id>.md
```

If the pairwise migration gate fails, keep the installed style unchanged and write the new result as
`review-candidate.md` plus its sidecar. Inspect `evaluations/migration-comparison.json` before any
manual override.

For a provenance-backed installed library, use the resumable batch migrator. It converts legacy
relative preview paths to absolute cached paths, seeds each old profile through the current contract,
and records each style as `promoted`, `review`, or `failed`. By default it only stages promoted pairs;
add `--publish` to back up and replace an installed pair after its same-prompt gate passes:

```bash
python <skill-root>/scripts/batch_migrate_styles.py \
  --styles-dir <gpt-image2-ppt-skills>/styles \
  --provenance-dir <source-workspace>/.ppt-template-distill/provenance \
  --migration-root <source-workspace>/.ppt-template-distill/migrations/<run-id> \
  --audit-json <audit-report.json> \
  --publish
```

The batch report is rewritten after every style, so interruption is safe. A zero child-process exit
code alone is not success: only `evaluations/migration-comparison.json` with `promoted=true` and a
complete staged pair can be published. Re-running skips promoted styles and retries review/failed
styles from cached profiles and role images. A transient image-service outage pauses the queue at the
current style with exit code 75 instead of spending requests on the remaining library; rerun the same
command to resume. Use `--continue-on-transient` only for an intentional endpoint-isolation test.

When the image endpoint is unavailable, prepare legacy structure without publishing or generating
slides:

```bash
python <skill-root>/scripts/batch_migrate_styles.py ... --prepare-only
```

This writes `style_profile.json` and a workdir-only `prepared-candidate.md + .layouts.json` when the
old profile has enough ordered evidence. Profiles with ambiguous preview-to-role coverage remain
`needs-vision`. Add `--repair-with-vision` to inspect only those ambiguous previews and repair their
profile contract; this still does not stage or publish them. Every prepared candidate must later run
the full generalization and same-prompt migration gate.

Override the standard role set only when the template has a justified specialty:

```bash
--validation-roles cover,section,content,data,comparison,closing
```

Resume and avoid repeated work:

```bash
python <skill-root>/scripts/score_and_distill.py \
  --input urls.txt \
  --style-id my-distilled-style \
  --resume
```

Inspect prior work:

```bash
python <skill-root>/scripts/score_and_distill.py --list-state
```

Audit an installed distilled-style library against cached provenance before bulk promotion:

```bash
python <skill-root>/scripts/audit_style_library.py \
  --styles-dir <gpt-image2-ppt-skills>/styles \
  --provenance-dir <ppt-distill-workdir>/.ppt-template-distill/provenance \
  --output library-audit.json
```

The audit flags missing layout routing, missing source-evidence mapping, truncated summaries, and roles that lack multiple archetypes. It is read-only and does not promote or rewrite styles.

After changing the compiler or gates, run the bundled deterministic smoke tests before any paid image generation:

```bash
python <skill-root>/scripts/self_test.py
```

Use `--refresh` to re-fetch and re-score a URL that already has a completed state record.

## Vision Model

If these variables exist, the script uses a multimodal OpenAI-compatible chat completions endpoint for taste scoring and style extraction:

```bash
VISION_BASE_URL=...
VISION_API_KEY=...
VISION_MODEL_NAME=...
```

Without `VISION_*`, the script still runs deterministic extraction and heuristic scoring. If a template passes, it writes a manual `distill_prompt.md` for a multimodal agent to complete.

## Output Review

After running, inspect:

- `.ppt-template-distill/distill_state.sqlite`: durable state for resume, dedupe, status, scores, and source hashes.
- `quality_report.json`: score, decision, reasons, image count, metrics.
- `source_manifest.json`: source URLs and selected preview images.
- `style_profile.json`: structured design tokens, layout system, image treatment, iconography, chart style, page-type rules, and provenance summary.
- paired `<style-id>.md` and `<style-id>.layouts.json`: every successful automatic distillation emits both; the sidecar is a TemplateProfile-compatible layout bank consumed directly by `generate_ppt.py`.
- The generated Markdown and sidecar are adapted as `source_kind=distilled-style` into the same RuntimeProfile contract used by strict template cloning; the sidecar remains image-independent and portable.
- `validation_report.json`: latest normalized multi-page evaluation and gate decision.
- `evaluations/round-NN/`: candidate profile, candidate style, generated role pages, and report for each validation round.
- `evaluations/summary.json`: terminal status, round count, selected roles, and latest report.
- `evaluations/summary.json` also records `champion_round`, the selected champion report, and the last attempted report when it was rolled back.
- `evaluations/baseline/` and `evaluations/migration-comparison.json`: same-prompt old/new renders and the deterministic net-improvement gate when `--baseline-style` is used.
- staged `.ppt-template-distill/staged_styles/<style-id>.md` plus its `.layouts.json` sidecar, if automatic distillation ran.
- `distill_prompt.md`, if no vision model was configured.

Report rejected templates clearly. Do not produce a style file for source-quality rejection or high-copying-risk validation rejection. A style that reaches the round cap without passing is written only as `review-candidate.md` plus `review-candidate.layouts.json` inside its provenance work directory with `validation_review`; never promote it into the repository `styles/` directory without human review.

Read `references/distilled-profile-schema.md` when changing profile fields or renderer contracts. Treat the JSON profile as authoritative and render Markdown from it; do not maintain two independently edited representations.

## Limits

Do not promise uninterrupted crawling. Websites may change HTML, robots rules, rate limits, or terms. Prefer explicit user-provided URLs, low request rates, cached state, and graceful stop/resume behavior.
