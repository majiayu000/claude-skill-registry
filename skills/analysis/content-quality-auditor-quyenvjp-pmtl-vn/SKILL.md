---
name: content-quality-auditor
version: "3.0.0"
description: 'This skill should be used when the user asks to "audit content quality", "EEAT score", "E-E-A-T audit", "content quality check", "CORE-EEAT audit", "helpful content assessment", "experience expertise authoritativeness trust", "how good is my content", "is my content AI-citation worthy", "content improvement plan", "helpful content update impact", or "GEO quality score". Runs the full 80-item CORE-EEAT audit across 8 dimensions: Contextual Clarity, Organization, Referenceability, Exclusivity (CORE, GEO-focused) plus Experience, Expertise, Authoritativeness, Trust (EEAT, SEO-focused). Produces a GEO Score, SEO Score, content-type weighted total, per-item pass/partial/fail, and prioritized fix plan with veto item checks. For SEO page element audits, see on-page-seo-auditor. For domain-level authority, see domain-authority-auditor.'
license: Apache-2.0
allowed-tools: WebFetch
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
metadata:
  author: aaron-he-zhu
  version: "3.0.0"
  geo-relevance: "high"
  tags:
    - seo
    - geo
    - e-e-a-t
    - helpful-content
    - content-quality
    - content-scoring
    - ai-quality
    - core-eeat
    - experience-expertise-authoritativeness-trust
    - helpful-content-update
  triggers:
    - "audit content quality"
    - "EEAT score"
    - "content quality check"
    - "CORE-EEAT audit"
    - "how good is my content"
    - "content assessment"
    - "quality score"
    - "is my content good enough to rank"
    - "EEAT check"
    - "rate my content quality"
---

# Content Quality Auditor

> Based on [CORE-EEAT Content Benchmark](https://github.com/aaron-he-zhu/core-eeat-content-benchmark). Full benchmark reference: [references/core-eeat-benchmark.md](../../references/core-eeat-benchmark.md)


> **[SEO & GEO Skills Library](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20 skills for SEO + GEO · Install all: `npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>Browse all 20 skills</summary>

**Research** · [keyword-research](../../research/keyword-research/) · [competitor-analysis](../../research/competitor-analysis/) · [serp-analysis](../../research/serp-analysis/) · [content-gap-analysis](../../research/content-gap-analysis/)

**Build** · [seo-content-writer](../../build/seo-content-writer/) · [geo-content-optimizer](../../build/geo-content-optimizer/) · [meta-tags-optimizer](../../build/meta-tags-optimizer/) · [schema-markup-generator](../../build/schema-markup-generator/)

**Optimize** · [on-page-seo-auditor](../../optimize/on-page-seo-auditor/) · [technical-seo-checker](../../optimize/technical-seo-checker/) · [internal-linking-optimizer](../../optimize/internal-linking-optimizer/) · [content-refresher](../../optimize/content-refresher/)

**Monitor** · [rank-tracker](../../monitor/rank-tracker/) · [backlink-analyzer](../../monitor/backlink-analyzer/) · [performance-reporter](../../monitor/performance-reporter/) · [alert-manager](../../monitor/alert-manager/)

**Cross-cutting** · **content-quality-auditor** · [domain-authority-auditor](../domain-authority-auditor/) · [entity-optimizer](../entity-optimizer/) · [memory-management](../memory-management/)

</details>

This skill evaluates content quality across 80 standardized criteria organized in 8 dimensions. It produces a comprehensive audit report with per-item scoring, dimension and system scores, weighted totals by content type, and a prioritized action plan.

## When to Use This Skill

- Auditing content quality before publishing
- Evaluating existing content for improvement opportunities
- Benchmarking content against CORE-EEAT standards
- Comparing content quality against competitors
- Assessing both GEO readiness (AI citation potential) and SEO strength (source credibility)
- Running periodic content quality checks as part of a content maintenance program
- After writing or optimizing content with seo-content-writer or geo-content-optimizer

## What This Skill Does

1. **Full 80-Item Audit**: Scores every CORE-EEAT check item as Pass/Partial/Fail
2. **Dimension Scoring**: Calculates scores for all 8 dimensions (0-100 each)
3. **System Scoring**: Computes GEO Score (CORE) and SEO Score (EEAT)
4. **Weighted Totals**: Applies content-type-specific weights for final score
5. **Veto Detection**: Flags critical trust violations (T04, C01, R10)
6. **Priority Ranking**: Identifies Top 5 improvements sorted by impact
7. **Action Plan**: Generates specific, actionable improvement steps

## How to Use

### Audit Content

```
Audit this content against CORE-EEAT: [content text or URL]
```

```
Run a content quality audit on [URL] as a [content type]
```

### Audit with Content Type

```
CORE-EEAT audit for this product review: [content]
```

```
Score this how-to guide against the 80-item benchmark: [content]
```

### Comparative Audit

```
Audit my content vs competitor: [your content] vs [competitor content]
```

## Data Sources

> See [CONNECTORS.md](../../CONNECTORS.md) for tool category placeholders.

**With ~~web crawler + ~~SEO tool connected:**
Automatically fetch page content, extract HTML structure, check schema markup, verify internal/external links, and pull competitor content for comparison.

**With manual data only:**
Ask the user to provide:
1. Content text, URL, or file path
2. Content type (if not auto-detectable): Product Review, How-to Guide, Comparison, Landing Page, Blog Post, FAQ Page, Alternative, Best-of, or Testimonial
3. Optional: competitor content for benchmarking

Proceed with the full 80-item audit using provided data. Note in the output which items could not be fully evaluated due to missing access (e.g., backlink data, schema markup, site-level signals).

## Instructions

When a user requests a content quality audit:

### Step 1: Preparation

```markdown
### Audit Setup

**Content**: [title or URL]
**Content Type**: [auto-detected or user-specified]
**Dimension Weights**: [loaded from content-type weight table]

#### Veto Check (Emergency Brake)

| Veto Item | Status | Action |
|-----------|--------|--------|
| T04: Disclosure Statements | ✅ Pass / ⚠️ VETO | [If VETO: "Add disclosure banner at page top immediately"] |
| C01: Intent Alignment | ✅ Pass / ⚠️ VETO | [If VETO: "Rewrite title and first paragraph"] |
| R10: Content Consistency | ✅ Pass / ⚠️ VETO | [If VETO: "Verify all data before publishing"] |
```

If any veto item triggers, flag it prominently at the top of the report and recommend immediate action before continuing the full audit.

### Step 2: CORE Audit (40 items)

Evaluate each item against the criteria in [references/core-eeat-benchmark.md](../../references/core-eeat-benchmark.md).

Score each item:
- **Pass** = 10 points (fully meets criteria)
- **Partial** = 5 points (partially meets criteria)
- **Fail** = 0 points (does not meet criteria)

```markdown
### C — Contextual Clarity

| ID | Check Item | Score | Notes |
|----|-----------|-------|-------|
| C01 | Intent Alignment | Pass/Partial/Fail | [specific observation] |
| C02 | Direct Answer | Pass/Partial/Fail | [specific observation] |
| ... | ... | ... | ... |
| C10 | Semantic Closure | Pass/Partial/Fail | [specific observation] |

**C Score**: [X]/100
```

Repeat the same table format for **O** (Organization), **R** (Referenceability), and **E** (Exclusivity), scoring all 10 items per dimension.

### Step 3: EEAT Audit (40 items)

```markdown
### Exp — Experience

| ID | Check Item | Score | Notes |
|----|-----------|-------|-------|
| Exp01 | First-Person Narrative | Pass/Partial/Fail | [specific observation] |
| ... | ... | ... | ... |

**Exp Score**: [X]/100
```

Repeat the same table format for **Ept** (Expertise), **A** (Authority), and **T** (Trust), scoring all 10 items per dimension.

See [references/item-reference.md](./references/item-reference.md) for the complete 80-item ID lookup table and site-level item handling notes.

### Step 4: Scoring & Report

Calculate scores and generate the final report:

```markdown
## CORE-EEAT Audit Report

### Overview

- **Content**: [title]
- **Content Type**: [type]
- **Audit Date**: [date]
- **Total Score**: [score]/100 ([rating])
- **GEO Score**: [score]/100 | **SEO Score**: [score]/100
- **Veto Status**: ✅ No triggers / ⚠️ [item] triggered

### Dimension Scores

| Dimension | Score | Rating | Weight | Weighted |
|-----------|-------|--------|--------|----------|
| C — Contextual Clarity | [X]/100 | [rating] | [X]% | [X] |
| O — Organization | [X]/100 | [rating] | [X]% | [X] |
| R — Referenceability | [X]/100 | [rating] | [X]% | [X] |
| E — Exclusivity | [X]/100 | [rating] | [X]% | [X] |
| Exp — Experience | [X]/100 | [rating] | [X]% | [X] |
| Ept — Expertise | [X]/100 | [rating] | [X]% | [X] |
| A — Authority | [X]/100 | [rating] | [X]% | [X] |
| T — Trust | [X]/100 | [rating] | [X]% | [X] |
| **Weighted Total** | | | | **[X]/100** |

**Score Calculation**:
- GEO Score = (C + O + R + E) / 4
- SEO Score = (Exp + Ept + A + T) / 4
- Weighted Score = Σ (dimension_score × content_type_weight)

**Rating Scale**: 90-100 Excellent | 75-89 Good | 60-74 Medium | 40-59 Low | 0-39 Poor

### N/A Item Handling

When an item cannot be evaluated (e.g., A01 Backlink Profile requires site-level data not available):

1. Mark the item as "N/A" with reason
2. Exclude N/A items from the dimension score calculation
3. Dimension Score = (sum of scored items) / (number of scored items x 10) x 100
4. If more than 50% of a dimension's items are N/A, flag the dimension as "Insufficient Data" and exclude it from the weighted total
5. Recalculate weighted total using only dimensions with sufficient data, re-normalizing weights to sum to 100%

**Example**: Authority dimension with 8 N/A items and 2 scored items (A05=8, A07=5):
- Dimension score = (8+5) / (2 x 10) x 100 = 65
- But 8/10 items are N/A (>50%), so flag as "Insufficient Data -- Authority"
- Exclude A dimension from weighted total; redistribute its weight proportionally to remaining dimensions

### Per-Item Scores

#### CORE — Content Body (40 Items)

| ID | Check Item | Score | Notes |
|----|-----------|-------|-------|
| C01 | Intent Alignment | [Pass/Partial/Fail] | [observation] |
| C02 | Direct Answer | [Pass/Partial/Fail] | [observation] |
| ... | ... | ... | ... |

#### EEAT — Source Credibility (40 Items)

| ID | Check Item | Score | Notes |
|----|-----------|-------|-------|
| Exp01 | First-Person Narrative | [Pass/Partial/Fail] | [observation] |
| ... | ... | ... | ... |

### Top 5 Priority Improvements

Sorted by: weight × points lost (highest impact first)

1. **[ID] [Name]** — [specific modification suggestion]
   - Current: [Fail/Partial] | Potential gain: [X] weighted points
   - Action: [concrete step]

2. **[ID] [Name]** — [specific modification suggestion]
   - Current: [Fail/Partial] | Potential gain: [X] weighted points
   - Action: [concrete step]

3–5. [Same format]

### Action Plan

#### Quick Wins (< 30 minutes each)
- [ ] [Action 1]
- [ ] [Action 2]

#### Medium Effort (1-2 hours)
- [ ] [Action 3]
- [ ] [Action 4]

#### Strategic (Requires planning)
- [ ] [Action 5]
- [ ] [Action 6]

### Recommended Next Steps

- For full content rewrite: use [seo-content-writer](../../build/seo-content-writer/) with CORE-EEAT constraints
- For GEO optimization: use [geo-content-optimizer](../../build/geo-content-optimizer/) targeting failed GEO-First items
- For content refresh: use [content-refresher](../../optimize/content-refresher/) with weak dimensions as focus
- For technical fixes: run `/seo:check-technical` for site-level issues
```

## Validation Checkpoints

### Input Validation
- [ ] Content source identified (text, URL, or file path)
- [ ] Content type confirmed (auto-detected or user-specified)
- [ ] Content is substantial enough for meaningful audit (≥300 words)
- [ ] If comparative audit, competitor content also provided

### Output Validation
- [ ] All 80 items scored (or marked N/A with reason)
- [ ] All 8 dimension scores calculated correctly
- [ ] Weighted total matches content-type weight configuration
- [ ] Veto items checked and flagged if triggered
- [ ] Top 5 improvements sorted by weighted impact, not arbitrary
- [ ] Every recommendation is specific and actionable (not generic advice)
- [ ] Action plan includes concrete steps with effort estimates

## Example

See [references/item-reference.md](./references/item-reference.md) for a complete scored example showing the C dimension with all 10 items, priority improvements, and weighted scoring.

## Tips for Success

1. **Start with veto items** — T04, C01, R10 are deal-breakers regardless of total score
   > These veto items are consistent with the CORE-EEAT benchmark (Section 3), which defines them as items that can override the overall score.
2. **Focus on high-weight dimensions** — Different content types prioritize different dimensions
3. **GEO-First items matter most for AI visibility** — Prioritize items tagged GEO 🎯 if AI citation is the goal
4. **Some EEAT items need site-level data** — Don't penalize content for things only observable at the site level (backlinks, brand recognition)
5. **Use the weighted score, not just the raw average** — A product review with strong Exclusivity matters more than strong Authority
6. **Re-audit after improvements** — Run again to verify score improvements and catch regressions
7. **Pair with CITE for domain-level context** — A high content score on a low-authority domain signals a different priority than the reverse; run [domain-authority-auditor](../domain-authority-auditor/) for the full 120-item picture

## Reference Materials

- [CORE-EEAT Content Benchmark](../../references/core-eeat-benchmark.md) — Full 80-item benchmark with dimension definitions, scoring criteria, and GEO-First item markers
- [references/item-reference.md](./references/item-reference.md) — All 80 item IDs in a compact lookup table + site-level item handling notes + scored example report

## Related Skills

- [domain-authority-auditor](../domain-authority-auditor/) — Domain-level CITE audit (40 items) — the sister skill for full 120-item assessment
- [seo-content-writer](../../build/seo-content-writer/) — Write content that scores high on CORE dimensions
- [geo-content-optimizer](../../build/geo-content-optimizer/) — Optimize for GEO-First items
- [content-refresher](../../optimize/content-refresher/) — Update content to improve weak dimensions
- [on-page-seo-auditor](../../optimize/on-page-seo-auditor/) — Technical on-page audit (complements this skill)
