---
name: faion-seo-manager
description: "SEO: on-page, off-page, technical optimization for organic visibility."
user-invocable: false
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# SEO Manager Skill (Claude)

## Overview
This skill orchestrates all SEO activities, from keyword research to technical optimization, ensuring content is discoverable and ranks high on search engines. It is designed to be used by Claude agents.

## Context Discovery

### Auto-Investigation

Check these project signals to understand SEO context:

| Signal | Location | What to Look For |
|--------|----------|------------------|
| SEO keywords | `.aidocs/product_docs/seo/` | Target keywords, search volume, ranking positions |
| Site audit | SEO tools, analytics | Technical issues, broken links, page speed, Core Web Vitals |
| Content | Website, blog | Existing content, topical coverage, content gaps |
| Backlinks | SEO tools, analytics | Link profile, domain authority, referring domains |
| Schema markup | Page source, structured data | Rich snippets, schema types, implementation |
| Site structure | Sitemap, internal links | URL structure, navigation, internal linking |
| Analytics | Google Search Console, GA4 | Organic traffic, click-through rates, rankings |

### Discovery Questions

```yaml
question: "What's your primary SEO focus?"
header: "SEO Focus"
multiSelect: false
options:
  - label: "Technical SEO audit"
    description: "Site foundation, Core Web Vitals, schema markup, crawlability"
  - label: "On-page optimization"
    description: "Content optimization, keyword targeting, topical authority"
  - label: "Link building"
    description: "Backlink acquisition, outreach, link quality improvement"
  - label: "AI search optimization (GEO/AEO)"
    description: "Google AI Overviews, zero-click search, answer optimization"
```

```yaml
question: "What's your SEO maturity level?"
header: "SEO Maturity"
multiSelect: false
options:
  - label: "New site (no SEO)"
    description: "SEO fundamentals, technical foundation, basic optimization"
  - label: "Basic SEO implemented"
    description: "Content optimization, link building, topical authority"
  - label: "Established SEO presence"
    description: "Advanced tactics, AI optimization, competitive positioning"
  - label: "SEO leader in niche"
    description: "Cutting-edge strategies, GEO/AEO, maintaining dominance"
```

```yaml
question: "What SEO issues are most urgent?"
header: "SEO Priorities"
multiSelect: true
options:
  - label: "Technical issues"
    description: "Broken links, slow pages, mobile issues, crawl errors"
  - label: "Content gaps"
    description: "Missing topical coverage, keyword opportunities"
  - label: "Link profile"
    description: "Low authority, few backlinks, toxic links"
  - label: "AI search visibility"
    description: "Not appearing in AI Overviews, zero-click optimization"
```

## Decision Tree

| If you need... | Use | File |
|----------------|-----|------|
| **Technical SEO** |
| Site audit, foundation | growth-seo-fundamentals | growth-seo-fundamentals.md |
| AI search optimization | technical-seo-for-ai | technical-seo-for-ai.md |
| Core Web Vitals | growth-seo-fundamentals | growth-seo-fundamentals.md |
| **On-Page SEO** |
| Content optimization | growth-seo-fundamentals | growth-seo-fundamentals.md |
| Topical authority | topical-authority | topical-authority.md |
| Keyword research | growth-seo-fundamentals | growth-seo-fundamentals.md |
| **Off-Page SEO** |
| Link building | growth-seo-link-building | growth-seo-link-building.md |
| **AI Search (GEO/AEO)** |
| Google AI Overviews | google-ai-overviews-optimization | google-ai-overviews-optimization.md |
| Zero-click search | zero-click-search-adaptation | zero-click-search-adaptation.md |
| Multi-platform SEO | seo | seo.md |

**Priority:**
- Quick wins: Fix broken links, optimize titles/meta, fix duplicates
- Foundation: Technical audit, site structure, mobile, speed, schema
- Long-term: Content, links, topical authority, AI visibility

**Common Sequences:**
- New site: fundamentals → technical-seo-for-ai → topical-authority → link-building
- AI readiness: technical-seo-for-ai → google-ai-overviews → zero-click-search

## Methodologies
- **seo.md**: Core SEO principles.
- **growth-seo-fundamentals.md**: Fundamentals of SEO for growth.
- **growth-seo-link-building.md**: Strategies for acquiring backlinks.
- **technical-seo-for-ai.md**: Technical SEO for AI-driven search.
- **topical-authority.md**: Building topical authority.
- **google-ai-overviews-optimization.md**: Optimizing for Google's AI Overviews.
- **zero-click-search-adaptation.md**: Adapting to zero-click search results.
