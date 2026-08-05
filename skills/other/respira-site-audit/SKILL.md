---
name: respira-site-audit
description: Use when asked to audit, score, or health-check a WordPress site or page. Runs SEO, AEO, readability, accessibility, performance, RankMath, and Core Web Vitals analyzers and presents a unified report with prioritised fixes.
metadata:
  short-description: Full site health check across SEO, AEO, accessibility, readability, and performance
  version: 1.1.0
  updated_at: 2026-05-17
  respira_min_version: 7.1.0
---

# Respira Site Audit

## Common Mistakes

| Mistake | Correct approach |
|---|---|
| Running analyzers without knowing which page to audit | Always confirm the target. Site-wide (all public pages) or a specific page URL or ID. |
| Reporting raw analyzer output without prioritising | Group findings by severity (CRITICAL, WARNING, SUGGESTION) and surface quick wins first. |
| Running all analyzers in sequence when only one is needed | Match the analyzer to the question. If the user asks about SEO only, run `respira_analyze_seo` and skip the rest. |
| Skipping `respira_get_builder_info` before reporting element-level issues | Builder type affects which fixes are possible. Elementor, Divi 4, Divi 5, Bricks, Beaver, and Oxygen all have different fix paths. |
| Treating AEO and SEO as interchangeable | SEO targets search rankings. AEO targets AI-generated answers. Both analyzers cover different signals and you usually want both. |
| Not checking whether the page is published before auditing | Drafts and private pages may produce incomplete results. Confirm `status: publish` first. |
| Using `extract_builder_content` when you only need structure | Use `respira_get_page_outline` for the "what is on this page" read. It is lighter and includes the primary heading per row. |

## Inputs

- Target: a specific page URL, page ID, or "the whole site".
- Scope: which analyzers to run. Default is all eight.
- Output format: a summary for the user, or JSON for a CI / CD pipeline.

## Workflow

### Single-page audit

1. `respira_get_site_context`. Confirm site URL, active SEO plugin (RankMath, Yoast, AIOSEO, SEOPress), active builder, WooCommerce presence.
2. `respira_get_builder_info`. Note builder type for element-level fix recommendations.
3. `respira_get_page_outline` if the structure needs to be discussed.
4. Run analyzers in parallel where possible:
   - `respira_analyze_seo`. Title, meta description, headings, internal links, canonical.
   - `respira_analyze_aeo`. Structured content, FAQ schema, answer-box signals.
   - `respira_analyze_readability`. Flesch score, sentence length, passive voice.
   - `respira_analyze_performance`. Load time, image sizes, render-blocking resources.
   - `respira_scan_page_accessibility`. WCAG 2.1 AA violations, alt text, contrast.
   - `respira_analyze_images`. Per-image weight, format, oversize-by-X factor.
   - `respira_check_structured_data`. Schema.org presence per page.
   - `respira_get_core_web_vitals`. CrUX-backed LCP, INP, CLS where available.
5. Aggregate findings by severity: CRITICAL → WARNING → SUGGESTION.
6. Build a prioritised fix list: quick wins first (alt text, missing meta) before structural changes.
7. Report: headline score per area plus top 3 fixes per area.

### Site-wide audit

1. `respira_list_pages` with `status: publish`. Collect all published page IDs.
2. For each page, or a representative sample, run the single-page workflow above.
3. Aggregate into a site-level summary: worst-performing pages, most common issue types, overall score bands.

### RankMath / Yoast integration

If RankMath, Yoast, AIOSEO, or SEOPress is active (visible in `respira_get_site_context`):

- `respira_analyze_rankmath` reads RankMath's own focus keyword scores and suggestions.
- Use these scores alongside `respira_analyze_seo` for a richer picture. Don't run them as alternatives.
- `respira_check_seo_issues` returns the active SEO plugin's own issue feed.

## Rules

- Always run `respira_get_site_context` first. Plugin presence (RankMath, Yoast, WooCommerce, ACF, WPML) changes which tools are relevant.
- Severity taxonomy: every finding must be CRITICAL (broken or missing, hurts rankings or UX), WARNING (suboptimal, addressable), or SUGGESTION (optional improvement).
- Do not recommend changes that bypass the builder. For element-level SEO fixes (alt text, heading hierarchy), use `respira_find_element` plus `respira_update_element` after confirming the builder.
- For accessibility fixes, prefer `respira_apply_accessibility_fixes` over manual element edits where the tool covers the finding.
- Performance findings are informational. Do not modify theme files or plugins to address them. Surface the issue and recommend the appropriate plugin or hosting action.
- For WPML-active sites, the audit is per-language. Pass the `lang` parameter to scope the run.

## Verification

After applying a fix:

1. Re-run the analyzer that flagged the issue.
2. Confirm the finding no longer appears at the same severity level.
3. For SEO fixes, note that index refresh and ranking changes are delayed. Tell the user.

For site-wide audits, re-audit the 3 worst-performing pages after fixes to confirm score movement.

## Escalation

Stop and ask the user if:

- The site has more than 200 published pages and the request is "audit the whole site". Confirm how many pages to sample.
- A CRITICAL finding requires a structural change (no H1 on any page, no `<html lang>` attribute). These often need theme or plugin changes beyond Respira's scope.
- `respira_analyze_performance` returns LCP > 4s or CLS > 0.25. Flag as high priority and ask whether to involve a developer.
- The site is on a multi-site network and the audit target wasn't specified. Confirm whether the run is per-subsite or network-wide.

## Example

Goal: audit the homepage for SEO and AEO readiness.

```
1. respira_get_site_context        → WordPress 6.9, RankMath active, Elementor 3.21
2. respira_get_builder_info        → Elementor, supported
3. respira_analyze_seo             → CRITICAL: no meta description | WARNING: 3 images missing alt
4. respira_analyze_aeo             → WARNING: no FAQ schema | SUGGESTION: add HowTo schema
5. respira_analyze_rankmath        → Focus keyword score: 62/100, improve keyword density
6. respira_scan_page_accessibility → WARNING: 2 buttons have no accessible label
7. respira_get_core_web_vitals     → LCP 2.8s (needs improvement), INP 180ms (good), CLS 0.05 (good)

Report:
  CRITICAL  → Add meta description (missing entirely)
  CRITICAL  → Add alt text to 3 hero images
  WARNING   → Add FAQ schema block for AEO (AI answer-box eligibility)
  WARNING   → 2 buttons need aria-label for screen readers
  WARNING   → LCP at 2.8s, target sub-2.5s by deferring the hero video
  SUGGESTION → Increase focus keyword density from 0.4% to 0.8%
```
