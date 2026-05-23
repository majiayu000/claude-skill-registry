---
name: dl-paper-code-blog
description: Craft long-form, Chinese blog posts that connect deep-learning papers with their code repositories using the auto-collected bundle (materials_manifest, paper_text, figures, repo_context, lsky cache). Use this skill whenever a user provides such a bundle and wants a TL;DR, method deep dive, experiment analysis, reproduction guide, and media assets.
---

# DL Paper Code Blog

## Overview

This skill turns the standardized "paper + repo" bundle into a publish-ready article: you will read the PDF derivatives, inspect the code snapshot, fill the scaffold outline, write the final Markdown post, and keep figure assets synced with Lsky. Everything lives inside a pre-generated workspace, so the work is editorial/reporting instead of scraping.

Key ingredients live in `materials_manifest.json`, `paper/`, `code/`, `.lsky_upload_cache.json`, and `article_scaffold.md`. The `assets/article_scaffold_template.md` file can be copied whenever you need a fresh outline.

## 1. Intake the Bundle

1. **Map the workspace.** Use the checklist in [references/materials.md](references/materials.md) to understand where each artifact sits (paper text, figure crops, repo context, bibliography, cache files).
2. **Verify availability.** If the manifest references missing directories (e.g., repo not captured), pause and ask the user; otherwise continue.
3. **Prepare the scaffold.** Copy `assets/article_scaffold_template.md` into the project root (or overwrite the existing `article_scaffold.md`). This is your scratchpad for planning.

## 2. Research & Outline

Follow the phased process described in [references/workflow.md](references/workflow.md):

- **Paper deep dive:** mine `paper_text.txt`, `figures_manifest.json`, and rendered pages to capture the narrative, metrics, and figure references. Take notes directly in the scaffold.
- **Code reconnaissance:** read `code/repo_context.md` (plus `repo_manifest.json`) to understand repo layout, commands, configs, and practical pitfalls worth mentioning in the blog.
- **Extra context:** skim anything the user left in `sources/` and cite it explicitly if used.
- **Outline:** fill every `TODO` inside `article_scaffold.md` so each section already contains bullet-point evidence (source + snippet). This keeps the drafting phase deterministic and makes reviews easy.

## 3. Draft & Polish the Article

Use the structure in [references/blog_outline.md](references/blog_outline.md):

1. Metadata/title block in Chinese followed by the hero figure.
2. `## 5-minute TL;DR` with bullet proof points referencing both paper and repo.
3. Sections 1-6 covering task motivation, method storyline, training/experiments, code reproduction guide, learner takeaways, and paper-vs-code differences.
4. "References" citing the paper and any supporting DOIs/links.

Writing tips:
- Everything stays in Simplified Chinese with a friendly-but-technical tone (see [references/writing_spec.md](references/writing_spec.md) for precise requirements, including title rules, section depth, citations, and limited use of code/inline formulas).
- Target length: 5000-7000 non-whitespace characters. Use `scripts/check_article_length.py` during QA to keep output stable.
- Use `scripts/check_article_requirements.py` to enforce mechanical constraints (title/metadata, references section, ban `paper/pages`, and optionally require https image URLs after Lsky sync).
- Do a final human self-review pass with [references/self_review.md](references/self_review.md) to ensure the article "explains clearly" (no guessing, evidence-backed claims, readable structure, figure-text consistency).
- Alternate paragraphs and bullet lists so readers can skim.
- Whenever you mention a claim, cite both the PDF section (page or figure) and the repo file/command that corroborates it.
- Keep `article_scaffold.md` alongside the final `<slug>_blog.md` so reviewers can trace back to sources.

## 4. Figures & Asset Logistics

Manage visuals according to [references/figures.md](references/figures.md):

- Select 4-6 figures: one front-matter image, at least one method diagram, several experiment/ablation plots or tables.
- Draft using local cropped images from `paper/figures/` (and `paper/front_matter/`). Then run `scripts/sync_lsky_images.py` to upload via the installed `lsky-uploader` skill, update `.lsky_upload_cache.json`, and rewrite the blog Markdown to use returned URLs.
- If downstream platforms need bundled PNGs, mirror the used figures under `salad_blog_assets/images/figN.png`.
- Double-check all links resolve before handing off.

## 5. Journal Metrics (JCR + CAS)

If you need accurate journal impact factor / quartiles and CAS partitions, use the local SQLite DB generated from your Excel tables:

- Build/update DB from your Excel source: `scripts/build_journal_metrics_db.py --overwrite`
- Query by journal name or ISSN: `scripts/query_journal_metrics.py --journal "Advanced Science"`

The DB file lives at `references/journal_metrics_2025.sqlite3`. If it is missing, run `scripts/build_journal_metrics_db.py --overwrite` to generate it locally.

## Deliverables Checklist

When you finish a project, ensure the workspace contains:

- Updated `article_scaffold.md` with your filled outline.
- Final `<slug>_blog.md` (or `blog.md` if the user specified one filename) following the outline.
- Updated `.lsky_upload_cache.json` if any new figures were uploaded.
- Optional: `salad_blog_assets/images/` containing all referenced media.

Document blockers (missing repo, corrupt PDF, etc.) at the top of the blog before the TL;DR if you cannot complete a section.

## Resources

- [references/materials.md](references/materials.md) - directory map + file purposes.
- [references/workflow.md](references/workflow.md) - phased process from intake to QA.
- [references/blog_outline.md](references/blog_outline.md) - mandatory section order, tone, and formatting.
- [references/figures.md](references/figures.md) - figure selection, Lsky uploads, cache maintenance, and optional asset packaging.
- [references/writing_spec.md](references/writing_spec.md) - condensed SML prompt constraints (audience, tone, title format, length, references, image callouts).
- `lsky-uploader` skill - required for `scripts/sync_lsky_images.py` (set `LSKY_TOKEN` before running).
- `scripts/build_journal_metrics_db.py` - converts your Excel tables into a queryable SQLite DB under `references/`.
- `scripts/query_journal_metrics.py` - looks up JCR/CAS metrics for the metadata block.
- `scripts/sync_lsky_images.py` - uploads local images and rewrites Markdown links to Lsky URLs.
- `scripts/check_article_length.py` - counts characters and reports per-section breakdown.
- `scripts/check_article_requirements.py` - validates title/metadata/references and blocks forbidden figure sources.
- [references/self_review.md](references/self_review.md) - human checklist for clarity and final polish.
- [assets/article_scaffold_template.md](assets/article_scaffold_template.md) - copy this template into each project root to start outlining.
