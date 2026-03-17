---
name: seo-audit
description: SEO analysis of content or pages
user-invocable: true
---

You are helping the marketing team audit content for SEO performance.

Follow these steps:

### Step 1: Get the Content

Ask the user for:
- Content to audit (pasted text, file path, or URL)
- **Target keyword(s)** — primary keyword and any secondary keywords
- **Content type** — blog post, product page, landing page, or category page

### Step 2: SEO Analysis

Delegate to the seo-optimizer agent to analyze:

**On-Page Factors:**
- Title tag length and keyword placement (50-60 chars)
- Meta description quality and keyword inclusion (150-160 chars)
- H1 tag presence and keyword inclusion
- Heading hierarchy (H2-H6 structure and keyword usage)
- Keyword density and natural placement
- First paragraph keyword presence
- Image alt text (if images referenced)
- URL slug optimization

**Content Quality Signals:**
- Content length vs competitors for the target keyword
- Readability score (Flesch-Kincaid)
- Content depth and topical coverage
- Internal linking opportunities
- External reference quality

**Technical SEO:**
- Schema markup recommendations (Product, Article, FAQ)
- Canonical URL suggestions
- Open Graph and social meta tags

### Step 3: Present the Audit Report

Display:
- **SEO Score**: X/100
- **Critical issues** (blocking ranking potential)
- **Optimization opportunities** (would improve rankings)
- **Content gaps** (topics competitors cover that are missing)

For each issue, provide:
- Current state
- Recommended fix
- Priority (high/medium/low)

### Step 4: Apply Fixes

Offer to:
- Rewrite title tag and meta description
- Restructure headings for better hierarchy
- Adjust keyword placement and density
- Add internal linking suggestions
- Generate schema markup snippets

### Error Handling

- If no target keyword is provided, suggest keywords based on content analysis
- If content is too short for meaningful SEO analysis, recommend minimum length
