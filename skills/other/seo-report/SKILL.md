---
name: seo-report
description: "Generate a client-facing SEO report from the latest crawl data. Produces a professional HTML report with executive summary, key metrics, top issues, and comparison charts. Trigger with 'seo report', 'generate seo report', 'client seo report', or 'seo summary'."
compatibility: claude-code-only
---

# SEO Report

Generate a professional, client-facing SEO report from Whispering Wombat crawl data. Outputs an HTML file suitable for sharing via PageDrop or email.

## Required MCP Tools

- **Whispering Wombat**: `whispering_crawls`, `whispering_issues`, `whispering_links`, `whispering_content`
- **Brain** (optional): `brain_site_get`, `brain_client_get`
- **PageDrop** (optional): For publishing shareable URL

## Input

`$ARGUMENTS` should be a domain name (e.g., `abpsychology.au`).

## Workflow

### Step 1: Get Latest Crawl

`whispering_crawls list` — find the most recent completed crawl for this domain.

If no crawl exists, inform the user and suggest running `/seo-audit {domain}` first.

### Step 2: Get Client Context

If Brain is available:
- `brain_site_get { domain }` — client name, contact, business type
- Use client name in the report header

### Step 3: Gather Report Data

Collect all data needed for the report:

1. `whispering_issues overview` — scores, status codes, response times
2. `whispering_issues summary` — issue counts by type
3. `whispering_links stats` — link health
4. `whispering_content sitemaps` — sitemap status
5. `whispering_content structure` — site depth
6. If previous crawl exists: `whispering_crawls compare` — changes

### Step 4: Generate HTML Report

Create a self-contained HTML file with inline CSS. Save to `.claude/artifacts/seo-report-{domain}-{date}.html`.

Report structure:

```html
<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <title>SEO Report: {domain}</title>
  <style>/* Inline professional styling */</style>
</head>
<body>
  <!-- Header with Jezweb branding -->
  <!-- Executive Summary (1 paragraph) -->
  <!-- Key Metrics Grid (4 cards: pages, issues, score, speed) -->
  <!-- Top 5 Issues with fix instructions -->
  <!-- Comparison with previous crawl (if available) -->
  <!-- Detailed Findings by Category -->
  <!-- Footer with date and disclaimer -->
</body>
</html>
```

Design guidelines:
- Professional, clean layout — no playful colours or emojis
- Monochrome/slate colour scheme matching Jezweb brand
- Tables for data, simple bar charts via CSS (no JS libraries)
- Print-friendly (reasonable page breaks, no fixed widths)
- Jezweb logo in header: `https://www.jezweb.com.au/wp-content/uploads/2021/11/Jezweb-Logo-White-Transparent.svg`

### Step 5: Offer to Share

After generating the HTML:
1. Show the file path to the user
2. Offer to publish via PageDrop for a shareable URL
3. If PageDrop: `pages { action: "create", content: htmlContent, slug: "seo-{domain}" }`

## Executive Summary Template

Write the executive summary as one short paragraph covering:
- Overall site health assessment (good/needs attention/critical)
- Number of pages analysed
- Most impactful finding
- Comparison trend (improving/declining/stable) if previous data exists

Example:
> "{Domain} is in good technical health with {X} pages analysed. The site scores well on core SEO fundamentals but has {N} critical issues that should be addressed — most notably {top issue}. Compared to the previous audit, the site has {improved/declined} with {N} new issues and {N} resolved."

## Notes

- Australian English throughout
- Keep language accessible — the client may not be technical
- Focus on "what to fix and why" not "what's wrong"
- Avoid jargon: "search engines can't find this page" not "noindex directive present"
- Include estimated impact: "fixing this could improve your visibility for local searches"
