---
name: seo-optimizer
description: SEO optimization toolkit with scoring, keyword research, and technical SEO auditing. Use for improving search rankings, content optimization, and technical SEO fixes. Based on alirezarezvani/claude-skills.
version: 1.0.0
category: marketing
last_updated: 2026-01-19
source: https://github.com/alirezarezvani/claude-skills
related_skills:
  - content-strategy
  - competitive-analysis
  - frontend-design
---

# SEO Optimizer Skill

## Overview

This skill provides comprehensive SEO optimization capabilities including content scoring, keyword research, technical auditing, and on-page optimization. Designed for B2B technical websites targeting engineering decision-makers.

## Quick Start

1. **Audit current state** - Run technical SEO check
2. **Research keywords** - Identify target terms by funnel stage
3. **Optimize content** - Apply on-page SEO improvements
4. **Monitor scores** - Track SEO score improvements
5. **Iterate** - Continuous optimization cycle

## When to Use

- Launching new website pages
- Optimizing existing content for search
- Technical SEO audits
- Keyword research and planning
- Content gap analysis
- Competitive SEO analysis

## SEO Scoring System

### Score Components (0-100)

| Component | Weight | Measures |
|-----------|--------|----------|
| Technical | 30% | Page speed, mobile, crawlability |
| On-Page | 30% | Keywords, meta tags, structure |
| Content | 25% | Quality, length, readability |
| Authority | 15% | Links, citations, trust signals |

### Score Targets

| Score | Rating | Action |
|-------|--------|--------|
| 90-100 | Excellent | Maintain, minor tweaks |
| 75-89 | Good | Target score for new content |
| 60-74 | Needs Work | Prioritize improvements |
| Below 60 | Poor | Major revision needed |

## Keyword Research Framework

### Funnel-Based Targeting

| Funnel Stage | Intent | Keyword Types | Example |
|--------------|--------|---------------|---------|
| TOFU | Informational | "what is", "how to", "guide" | "what is fatigue analysis" |
| MOFU | Investigational | "best", "vs", "comparison" | "FEA software comparison" |
| BOFU | Transactional | "services", "consultant", "hire" | "offshore engineering consultant" |

### Keyword Selection Criteria

```markdown
## Ideal Keyword Profile
- Search volume: 500-5,000/month (sweet spot for B2B)
- Keyword difficulty: <40 (achievable ranking)
- Business relevance: High alignment with services
- Intent match: Clear user intent
- Competition: Low-medium SERP competition
```

### Keyword Clustering

Group related keywords into topic clusters:

```
Pillar: "Offshore Engineering"
├── Cluster: Structural Analysis
│   ├── "offshore platform structural analysis"
│   ├── "subsea structure design"
│   └── "jacket platform engineering"
├── Cluster: Fatigue Analysis
│   ├── "offshore fatigue assessment"
│   ├── "S-N curve analysis"
│   └── "fatigue life prediction"
└── Cluster: Standards & Compliance
    ├── "DNV offshore standards"
    ├── "API RP 2A compliance"
    └── "offshore engineering certification"
```

## On-Page SEO Checklist

### Title Tag
- [ ] Primary keyword near beginning
- [ ] 50-60 characters length
- [ ] Unique across site
- [ ] Compelling for clicks

### Meta Description
- [ ] 150-160 characters
- [ ] Contains primary keyword
- [ ] Includes call-to-action
- [ ] Unique per page

### Headings (H1-H6)
- [ ] Single H1 with primary keyword
- [ ] Logical heading hierarchy
- [ ] Keywords in H2s naturally
- [ ] Descriptive, not generic

### Content Body
- [ ] Primary keyword in first 100 words
- [ ] Keyword density 1-2%
- [ ] Related keywords (LSI) included
- [ ] 1,500+ words for pillar content
- [ ] Internal links to related pages
- [ ] External links to authoritative sources

### Images
- [ ] Descriptive file names
- [ ] Alt text with keywords
- [ ] Compressed for speed
- [ ] WebP format preferred

### URL Structure
- [ ] Short and descriptive
- [ ] Contains primary keyword
- [ ] Hyphens between words
- [ ] No parameters or IDs

## Technical SEO Audit

### Core Web Vitals

| Metric | Target | Tool |
|--------|--------|------|
| LCP (Largest Contentful Paint) | <2.5s | PageSpeed Insights |
| FID (First Input Delay) | <100ms | PageSpeed Insights |
| CLS (Cumulative Layout Shift) | <0.1 | PageSpeed Insights |

### Technical Checklist

```markdown
## Crawlability
- [ ] robots.txt properly configured
- [ ] XML sitemap submitted to GSC
- [ ] No orphan pages
- [ ] Proper canonical tags
- [ ] No redirect chains

## Indexability
- [ ] Important pages indexed
- [ ] No accidental noindex
- [ ] Proper hreflang (if multilingual)
- [ ] Structured data implemented

## Performance
- [ ] HTTPS enabled
- [ ] Mobile-responsive
- [ ] Page speed <3s
- [ ] No render-blocking resources
- [ ] Images optimized

## Architecture
- [ ] Logical URL structure
- [ ] Breadcrumb navigation
- [ ] Internal linking strategy
- [ ] Flat site architecture (<3 clicks to any page)
```

## Structured Data (Schema.org)

### Required for AceEngineer

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "AceEngineer",
  "url": "https://aceengineer.com",
  "logo": "https://aceengineer.com/assets/img/logo.png",
  "sameAs": ["https://github.com/aceengineer"],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer service",
    "email": "contact@aceengineer.com"
  }
}
```

### Additional Schema Types

| Page Type | Schema | Purpose |
|-----------|--------|---------|
| Service pages | Service | Rich snippets for services |
| Blog posts | Article | Author, date in search |
| Case studies | Case Study | Project showcase |
| Calculators | WebApplication | Tool rich results |
| FAQ | FAQPage | FAQ rich snippets |

## Content Optimization Template

```markdown
## Page: [Page Title]

### Target Keywords
- Primary: [main keyword]
- Secondary: [2-3 related keywords]
- LSI: [5-10 semantically related terms]

### Current Score: [X/100]

### Optimization Tasks
1. Title: [current] → [optimized]
2. Meta: [current] → [optimized]
3. H1: [current] → [optimized]
4. Content gaps: [missing topics]
5. Internal links: [add links to...]
6. Schema: [add/update type]

### Target Score: [Y/100]
```

## SEO Monitoring

### Weekly Checks
- [ ] Google Search Console errors
- [ ] Core Web Vitals status
- [ ] New indexed pages
- [ ] Crawl stats

### Monthly Analysis
- [ ] Keyword ranking changes
- [ ] Organic traffic trends
- [ ] Top performing pages
- [ ] Competitor movements
- [ ] Backlink profile

### Quarterly Review
- [ ] Content audit (update old content)
- [ ] Technical SEO deep dive
- [ ] Keyword strategy refresh
- [ ] Competitive analysis update

## Best Practices

### Do

1. Focus on user intent, not just keywords
2. Create comprehensive, authoritative content
3. Build topic clusters around pillars
4. Update old content regularly
5. Monitor Core Web Vitals
6. Use internal linking strategically

### Don't

1. Keyword stuff unnaturally
2. Duplicate content across pages
3. Ignore mobile experience
4. Build low-quality backlinks
5. Neglect technical SEO
6. Forget to track and measure

## Error Handling

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| Pages not indexing | Check robots.txt, noindex | Fix blocking rules |
| Ranking drops | Algorithm update, competition | Audit and improve content |
| Slow page speed | Large images, render blocking | Optimize assets |
| Low CTR | Poor title/meta | A/B test snippets |

## Metrics

| Metric | Target | Frequency |
|--------|--------|-----------|
| SEO Score | >75/100 | Per page |
| Organic traffic | +10% MoM | Monthly |
| Keyword rankings | Top 10 | Weekly |
| Core Web Vitals | All green | Weekly |
| Index coverage | >95% | Monthly |

## Related Skills

- [content-strategy](../content-strategy/SKILL.md) - Content planning
- [competitive-analysis](../competitive-analysis/SKILL.md) - Competitor SEO
- [frontend-design](../../content-design/frontend-design/SKILL.md) - Page design

---

## Version History

- **1.0.0** (2026-01-19): Initial release adapted from alirezarezvani/claude-skills
