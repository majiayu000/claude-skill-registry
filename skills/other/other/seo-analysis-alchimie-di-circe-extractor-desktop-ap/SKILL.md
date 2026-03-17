---
name: seo_analysis
description: SEO keyword research, search intent analysis, and metadata optimization
when_to_use: When creating content that needs to rank in search engines, analyzing existing content's SEO performance, or writing meta descriptions and title tags
references:
  - references/keyword-research-guide.md
  - references/seo-metadata-templates.md
---

# SEO Analysis Skill

## Overview

This skill enables systematic SEO analysis for content creation: keyword research, search intent identification, on-page optimization, and metadata generation.

## Tools to Use

- **Perplexity**: Research keyword trends, search volumes, SERP landscape
- **Jina** (`r.jina.ai/<url>`): Extract clean text from competitor pages for analysis
- **Firecrawl**: Scrape competitor content and meta tags at scale

## Workflow

### Step 1 — Define Target Topic & Audience

1. Identify the core topic from the content brief
2. Clarify the primary audience (industry, seniority, pain points)
3. Note the content format (blog post, landing page, social caption)

### Step 2 — Keyword Research

Use Perplexity to research:
```
"What are the most searched keywords for [topic] in [industry/region]?
Include long-tail variants and related semantic terms."
```

Extract from results:
- Primary keyword (highest volume + relevance)
- 3–5 secondary keywords (semantic variants)
- 2–3 long-tail keywords (specific intent, lower competition)
- LSI (Latent Semantic Indexing) terms

### Step 3 — Search Intent Analysis

For each primary keyword, classify intent:
- **Informational**: "How does X work?" → educational content
- **Navigational**: Brand/product searches → brand content
- **Commercial**: "Best X for Y" → comparison/review content
- **Transactional**: "Buy X" → conversion-focused content

Align content format and CTA with detected intent.

### Step 4 — Competitor SERP Analysis

1. Use Jina to read top 3 ranking pages for the primary keyword
2. Identify: content length, header structure (H1/H2/H3), featured snippets
3. Find content gaps (what they cover vs. what they miss)

### Step 5 — Metadata Generation

Generate the following for each piece of content:

**Title Tag** (50–60 chars):
- Include primary keyword near the beginning
- Format: `[Primary Keyword] — [Benefit/Hook] | [Brand Name]`

**Meta Description** (120–155 chars):
- Include primary keyword naturally
- Clear value proposition + implicit CTA
- No clickbait

**URL Slug**:
- Lowercase, hyphens only, no stop words
- Include primary keyword: `/blog/[primary-keyword-slug]`

**Open Graph / Social**:
- OG Title: Can be slightly longer (60–70 chars), more engaging
- OG Description: 150–200 chars, action-oriented

### Step 6 — Content Optimization Checklist

Verify the final content includes:
- [ ] Primary keyword in H1 (exactly once)
- [ ] Primary keyword in first 100 words
- [ ] Secondary keywords distributed in H2/H3 headers
- [ ] Alt text for all images (include keyword where natural)
- [ ] Internal links to related content (2–3 minimum)
- [ ] External links to authoritative sources (1–2)
- [ ] Target word count based on SERP analysis

## Output Format

```markdown
## SEO Analysis Report

**Primary Keyword**: [keyword] | Est. Search Volume: [high/medium/low]
**Intent**: [Informational / Commercial / etc.]
**Difficulty**: [Low / Medium / High]

### Keyword Clusters
- Primary: [keyword]
- Secondary: [kw1], [kw2], [kw3]
- Long-tail: [lt1], [lt2]

### Metadata
- **Title**: [50–60 char title]
- **Meta Description**: [120–155 char description]
- **URL Slug**: /[slug]

### Content Gaps Found
- [Competitor A] misses: [topic X]
- Opportunity: [specific angle]

### Optimization Checklist
[Completed checklist]
```

## Notes

- Always verify keyword relevance against brand voice (load brand_voice skill)
- For Italian/multilingual content: research Italian-specific SERPs separately
- Seasonal keywords: flag if trend is time-sensitive
