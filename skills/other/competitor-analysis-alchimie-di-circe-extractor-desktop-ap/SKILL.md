---
name: competitor_analysis
description: Market gap analysis and competitor content benchmarking for strategic positioning
when_to_use: When validating a content idea against the competitive landscape, identifying market gaps, or benchmarking content quality and engagement before publishing
references:
  - references/competitor-matrix-template.md
  - references/gap-analysis-framework.md
---

# Competitor Analysis Skill

## Overview

This skill enables systematic competitor content analysis: identifying who is winning in the space, what content they produce, engagement patterns, and uncovered opportunities for differentiation.

## Tools to Use

- **Perplexity**: Research competitor rankings, engagement metrics, content themes
- **Firecrawl**: Scrape competitor content pages, extract article structure and copy
- **Jina**: Clean content extraction from competitor URLs for comparison
- **RAG (competitors)**: Brand's pre-indexed competitor intelligence

## Workflow

### Step 1 — Define Competitive Landscape

1. Query RAG (competitors) for known competitors in the brand's space
2. Use Perplexity to supplement: "Who are the top 5 content publishers in [niche] in [market]?"
3. Classify competitors by type:
   - **Direct**: Same product/service, same audience
   - **Indirect**: Different product, same audience need
   - **Aspirational**: Larger brand, same values/positioning

### Step 2 — Content Audit (Top Competitors)

For each of the top 3 direct competitors:

1. Use Firecrawl to crawl their blog/social pages
2. Extract and record:
   - Content formats used (articles, videos, carousels, etc.)
   - Publishing frequency
   - Top performing topics (by social shares/engagement)
   - Tone and voice characteristics
   - CTA patterns

3. Use Jina to read their 3 best-performing pieces (if URLs are available)

### Step 3 — Gap Analysis

Compare competitor content coverage vs. brand content:

**Content Topics**:
- Topics they cover well → competitive territory (differentiate or go deeper)
- Topics they cover poorly → opportunity (own the narrative)
- Topics they don't cover → white space (first-mover advantage)

**Format Gaps**:
- Formats they underutilize: identify which formats perform best in the niche but are underused by competitors

**Audience Gaps**:
- Audience segments they ignore or underserve
- Geographic or demographic gaps

### Step 4 — Engagement Benchmarking

Research competitor engagement using Perplexity:
```
"What are typical engagement rates for [content type] in [industry] on [platform]?
What makes top-performing posts in this space stand out?"
```

Establish benchmarks for:
- Average likes/shares/comments for the content type
- Engagement rate ranges (low/average/high)
- Posting frequency patterns

### Step 5 — Differentiation Recommendations

Based on findings, generate 3 differentiation angles:

1. **Topic angle**: Unique topic or sub-topic competitors haven't addressed
2. **Format angle**: Better format for the same topic (video vs. article, etc.)
3. **Positioning angle**: Different brand perspective on the same subject

### Step 6 — Competitive Threat Assessment

Rate the content idea vs. competitors:
- **Red**: Direct competition with a stronger player — reconsider
- **Yellow**: Competitive territory but differentiable — proceed with differentiation
- **Green**: Underserved space — proceed with confidence

## Output Format

```markdown
## Competitor Analysis Report

**Topic**: [content idea being validated]
**Analysis Date**: [date]

### Competitive Landscape
| Competitor | Type | Content Focus | Posting Freq. | Engagement |
|-----------|------|--------------|--------------|------------|
| [Name A]  | Direct | [themes] | [X/week] | [High/Med/Low] |
| [Name B]  | Indirect | [themes] | [X/week] | [High/Med/Low] |

### Content Gaps Identified
- **Topic gaps**: [list]
- **Format gaps**: [list]
- **Audience gaps**: [list]

### Differentiation Opportunities
1. [Angle 1]
2. [Angle 2]
3. [Angle 3]

### Recommendation
**Status**: [🟢 Green / 🟡 Yellow / 🔴 Red]
**Rationale**: [1–2 sentences]
**Suggested angle**: [specific differentiation]
```

## Notes

- Cross-reference with brand_voice skill for positioning alignment
- Update RAG (competitors) knowledge base when significant new insights are found
- For Italian market: focus on local competitors, not just global ones
