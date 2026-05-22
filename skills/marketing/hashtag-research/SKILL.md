---
name: hashtag_research
description: Platform hashtag trend analysis, search volume estimation, and audience-relevant hashtag set generation
when_to_use: When finalizing social media posts that require hashtags, building a hashtag strategy for a content pillar, or researching trending hashtags for a campaign
references:
  - references/hashtag-tiers.md
  - references/platform-hashtag-rules.md
---

# Hashtag Research Skill

## Overview

This skill provides systematic hashtag research and selection for social media content: trend analysis, volume estimation, relevance scoring, and platform-specific hashtag set generation.

## Tools to Use

- **Perplexity**: Research trending hashtags, volume data, niche communities
- **Jina**: Analyze top posts for a hashtag (via Instagram/LinkedIn public search results)
- **RAG (platform_specs)**: Platform-specific hashtag rules and limits

## Platform Rules Reference

| Platform | Max Recommended | Style | Notes |
|----------|----------------|-------|-------|
| Instagram | 5–10 (optimal), 30 (max) | Mix niche + mid-tier | Place in caption or first comment |
| LinkedIn | 3–5 | Niche and professional | End of post only |
| TikTok | 5–8 | Trending + niche | Include 1–2 viral trends if relevant |
| Twitter/X | 1–2 | Trending or specific | Only when trending adds value |
| Facebook | 0–3 | Niche only | Hashtags add little organic reach |

## Hashtag Tier Classification

### Tier 1 — Micro Niche (Under 10K posts)
- Highest relevance, lowest competition
- Ideal for community building and super-targeted reach
- Examples: #SlowFoodItalia, #ArtigianatoSostenibile, #FoodStorytelling

### Tier 2 — Niche (10K–100K posts)
- Best engagement-to-reach ratio
- Still discoverable, less competitive
- Examples: #FoodPhotography, #SostenibileOggi, #BrandStorytelling

### Tier 3 — Mid-Tier (100K–500K posts)
- Good for broader discovery
- Use 2–3 per post maximum
- Examples: #Sostenibilità, #ContentMarketing, #FoodBlogger

### Tier 4 — Broad (500K–1M posts)
- Low ROI for most accounts under 10K followers
- Use sparingly (0–1 per post) — mainly for categorization
- Examples: #Food, #Marketing, #Photography

### Tier 5 — Mega (1M+ posts)
- Virtually no discoverability value unless trending
- Avoid for organic posts
- Acceptable only if part of a branded campaign

## Workflow

### Step 1 — Topic & Platform Identification

1. Identify the content topic (from the post or content brief)
2. Confirm target platform(s)
3. Identify audience language (Italian / English / bilingual)

### Step 2 — Seed Hashtag Research

Use Perplexity to find initial hashtag candidates:
```
"What are the most relevant and currently active hashtags for [topic]
on [platform] in [language/region]? Include both niche and mid-tier options."
```

Generate 15–20 candidates initially.

### Step 3 — Tier Classification

For each candidate, estimate tier based on Perplexity data or publicly available information. Classify into tiers 1–5.

### Step 4 — Relevance Scoring

Score each candidate 1–5 on:
- **Topic relevance**: How directly related to the content?
- **Audience fit**: Used by the target audience (not just any user)?
- **Community activity**: Is there an active community using this tag?

Drop any hashtag scoring below 3 on relevance.

### Step 5 — Set Construction

Build the final hashtag set using this mix:

**For Instagram (8–10 hashtags)**:
- 2–3 Tier 1 (micro niche)
- 3–4 Tier 2 (niche)
- 2–3 Tier 3 (mid-tier)
- 0–1 Tier 4 (broad)

**For LinkedIn (3–5 hashtags)**:
- 1–2 Tier 2 (niche professional)
- 2–3 Tier 3 (industry-relevant)

**For TikTok (5–8 hashtags)**:
- 2–3 Tier 1–2 (niche)
- 1–2 Tier 3 (trending if relevant)
- 1–2 viral trending tags (from Perplexity research)

### Step 6 — Trend Check

Use Perplexity to confirm:
- Any of these hashtags currently associated with negative trends/events?
- Any new trending hashtags relevant to the content topic?

Replace flagged hashtags.

### Step 7 — Generate Branded Hashtag (if applicable)

For brand-owned content, include 1 branded hashtag if the brand has one. If not, propose a branded hashtag following these rules:
- Short (1–2 words max)
- Memorable and unique
- Consistent across all platforms
- Format: `#[BrandName][Concept]` or `#[Campaign][Year]`

## Output Format

```markdown
## Hashtag Research Report

**Topic**: [content topic]
**Platform**: [platform]
**Language**: [Italian / English / Bilingual]
**Date**: [date — hashtag trends expire]

### Recommended Hashtag Set
[Ready to paste set for platform]

Example (Instagram):
#SlowFoodItalia #FoodStorytelling #CucineItaliane #ArtigianatoAlimentare
#FoodPhotography #SostenibileOggi #FoodBloggerItalia #Gastronomia
#Sostenibilità #ItaliaSostenibile

### Hashtag Detail

| Hashtag | Tier | Relevance | Notes |
|---------|------|-----------|-------|
| #SlowFoodItalia | 1 | 5/5 | Core community tag |
| #FoodStorytelling | 2 | 5/5 | Niche but active |
| #Gastronomia | 3 | 4/5 | Broad category |

### Trend Alerts
- [Any hashtags with current negative associations: none / list]
- [New trending tags to consider: none / list]

### Branded Hashtag
- [Existing: #BrandTag] OR [Proposed: #NewTag — rationale]
```

## Notes

- Hashtag data expires quickly — flag sets older than 60 days for refresh
- Never copy a competitor's entire hashtag set — differentiate at least 50%
- Italian content: mix Italian and English hashtags for maximum bilingual reach
- Platform algorithm updates may change hashtag ROI — reassess quarterly
- Avoid hashtags that are shadowbanned (can suppress reach without warning)
