---
name: kai-html-presentation
description: Client-ready HTML presentation builder for Kai audit and report folders. Converts weekly audits, monthly audits, marketing reports, scorecards, findings, data-source notes, and action plans into a polished single-file HTML deck with sourced metrics, executive slides, speaker notes, and delivery-ready styling. Use when "HTML presentation", "HTML deck", "client-ready audit deck", "turn this audit into slides", "present the weekly audit", "present the monthly audit", or any request to deliver Kai reports as HTML slides.
---

# kai-html-presentation - HTML Audit Deck

Create a single-file HTML presentation from Kai audit or report artifacts. This skill is for delivery, not analysis. The audit source folder must already contain sourced findings and data gaps.

## Source Contract

Before building the deck:

1. Read the source folder's `_data-sources.md`, `_data-gaps.md`, `audit-data.json` or `kai-data.json`, and the main report files.
2. Run audit provenance lint when the source folder is an audit:

```bash
python scripts/quality_gates/audit_provenance_lint.py <source-folder> --audit-dir
```

3. Do not add new quantitative claims in the HTML deck unless the claim exists in the source artifacts with a source.
4. Put a source footer on every slide with a number.
5. Keep missing data visible. Use a "Data Gaps" slide instead of filling blanks.

## Input

Accept:

- Weekly audit folder: `workspace/audits/weekly/<YYYY-MM-DD>/`
- Monthly audit folder: `workspace/audits/monthly/<YYYY-MM>/`
- Full audit folder: `workspace/marketing-audit/`
- SEO/CRO/report folder with `_data-sources.md` and `_data-gaps.md`

If there is no clear source folder, ask for the folder path.

## Build Rules

Use `assets/audit-deck-template.html` as the starting point. Copy it to:

```text
<source-folder>/html-presentation/index.html
```

Then replace the placeholder content with real sections from the source folder.

Design rules:

- Make the first slide identify the client, audit period, data mode, and retrieval date.
- Use 8 to 14 slides for weekly audits.
- Use 10 to 18 slides for monthly audits.
- Prefer dense, readable operator slides over marketing hero pages.
- Use tables for scorecards, decisions, source inventory, and action plans.
- Use short chart-like HTML blocks for trends only when values are sourced.
- Keep text within its containers on desktop and mobile.
- Use restrained color: neutral background, dark text, one accent, and status colors.
- Avoid nested cards and decorative blobs.
- Do not hide key facts in images or screenshots.

## Required Slide Order

Weekly audit deck:

1. Title and audit scope.
2. Executive snapshot.
3. Weekly scorecard.
4. What changed this week.
5. Red and yellow flags.
6. Channel findings.
7. Conversion and lead capture.
8. Paid/content/SEO highlights when applicable.
9. This week's actions.
10. Data sources and gaps.

Monthly audit deck:

1. Title and audit scope.
2. Executive summary.
3. 30-day scorecard.
4. KPI trend summary.
5. Channel decisions.
6. Conversion and lead capture.
7. Search and AEO health.
8. Paid media and budget decision when applicable.
9. Lifecycle, retention, or reputation findings when applicable.
10. Strategic learning.
11. Next-month plan.
12. Data sources and gaps.

## Slide Structure

Each slide should use this shape:

```html
<section class="slide">
  <header>
    <p class="eyebrow">Audit period</p>
    <h2>Slide title</h2>
  </header>
  <div class="slide-body">
    <!-- source-backed content -->
  </div>
  <footer>Sources: ...</footer>
</section>
```

Use `data-mode`, `source-tier`, and `retrieved-at` labels where helpful.

## Verification

Before handoff:

1. Open the HTML locally or start a simple static server if needed.
2. Check desktop and mobile widths.
3. Confirm no placeholder text remains.
4. Confirm every number has a source footer.
5. Confirm `_data-gaps.md` is represented.
6. Confirm the deck path is listed in the final response.

## Output

Write:

```text
<source-folder>/html-presentation/index.html
```

Optionally write:

```text
<source-folder>/html-presentation/notes.md
```

Use `notes.md` only for presenter notes that should not appear on client slides.

