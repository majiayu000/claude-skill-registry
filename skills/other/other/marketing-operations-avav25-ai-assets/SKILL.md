---
name: marketing-operations
description: Marketing operations knowledge base — MARKETING.md setup template, social media and email channel playbooks, trend research methodology, content calendar patterns, and recurring task definitions. Use when initializing marketing strategy, creating social media posts, drafting email campaigns, researching trends, or reviewing marketing analytics. Provides templates, platform-specific best practices, and quality checklists.
---

# Marketing Operations

Systematic marketing operations skill with strategy setup templates, channel-specific playbooks, and recurring task frameworks. Supports the `/marketing` workflow with reusable knowledge and templates.

## When to Use

- Initializing marketing strategy for a project (MARKETING.md creation)
- Creating social media posts for X/Twitter, LinkedIn, Reddit
- Drafting email campaigns and newsletters
- Researching trends and content opportunities
- Planning community engagement
- Reviewing and adjusting marketing strategy
- Setting up a content calendar

## When NOT to Use

- Writing blog posts (use `/blog-post` workflow with `content-creation` skill)
- SEO audits (use `/seo-review` workflow)
- Landing page design (use `/ui-ux-design` workflow)
- Technical documentation (use `/docs` workflow)

## Key Concepts

### Marketing Strategy Hierarchy

```
Mission (why we exist)
  └── Positioning (who we serve, what we offer, why us)
        └── Messaging Framework (value prop, pillars, proof points)
              └── Channel Strategy (where we show up)
                    └── Content Pillars (what we talk about)
                          └── Tactical Plan (what we do daily/weekly/monthly)
                                └── Content Calendar (specific tasks and dates)
```

### Channel Selection Framework

Evaluate each channel on three dimensions before committing:

| Dimension | Question |
|---|---|
| **Audience fit** | Is our ICP active here? Can we reach them? |
| **Resource fit** | Can we sustain the required publishing cadence? |
| **Content fit** | Does our content type work on this platform? |

**Rule**: Better to do 2 channels well than 5 channels poorly. Start with 1-2 high-fit channels and expand only after consistent execution.

### Content Pillar Model

Define 3-5 content pillars aligned with:

1. **ICP pain points** — problems your audience actively searches for
2. **Product strengths** — areas where your product genuinely excels
3. **Industry expertise** — topics where you have unique knowledge or data
4. **Trending intersections** — emerging topics that connect to your product

Each piece of content should map to exactly one pillar. Track pillar distribution to avoid over-indexing on one topic.

### Measurement Framework

| Level | Metrics | Review Cadence |
|---|---|---|
| **Vanity** (awareness) | Impressions, followers, page views | Weekly (track, don't optimize for) |
| **Engagement** | Likes, comments, shares, click-through rate | Weekly |
| **Pipeline** | Signups, leads, demo requests, email subscribers | Weekly |
| **Revenue** | Conversions, MRR impact, CAC, LTV | Monthly |

**Rule**: Optimize for pipeline and revenue metrics. Use vanity metrics only as leading indicators.

## Resources

- **`marketing-setup-template.md`** — Complete MARKETING.md template with all sections for strategy initialization
- **`channel-playbooks.md`** — Platform-specific playbooks for X/Twitter, LinkedIn, Reddit, email, and community engagement

## Integration

- **Follows rules**: `marketing-strategist` guidance for strategy and positioning, `content-designer` guidance for copy and social posts, and `content-writer` guidance for blog and email content
- **Used by workflows**: `/marketing` (primary), `/blog-post` (marketing context), `/docs` (public-facing content)
- **Companion skills**: `content-creation` skill (AI content tools, image generation, content briefs)