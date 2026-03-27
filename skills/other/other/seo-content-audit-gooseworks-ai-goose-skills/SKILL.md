---
name: seo-content-audit
description: >
  Comprehensive SEO footprint analysis that orchestrates site-content-catalog,
  seo-domain-analyzer, and brand-voice-extractor into a single deep-dive report.
  Catalogs all content, pulls real SEO metrics, runs competitor analysis, builds
  topic/keyword and content-type gap matrices, extracts brand voice, and produces
  a prioritized recommendations report. The complete SEO audit for any company.
tags: [seo]
---

# SEO Content Audit

The complete SEO footprint analysis. Orchestrates three granular skills — content cataloging, SEO metrics, and brand voice extraction — into a comprehensive audit with competitive gap matrices and prioritized recommendations.

## Quick Start

```
Run an SEO content audit for [company]. Website: [url]. Competitors: [list].
```

Or with a client context file:
```
Run an SEO content audit for [client]. Use context at clients/[client]/context.md.
```

## Inputs

| Input | Required | Source |
|-------|----------|--------|
| **Company name** | Yes | User provides or `clients/<client>/context.md` |
| **Company domain** | Yes | User provides or context file |
| **Seed competitors** | Recommended | User provides 2-5; system discovers more |
| **Target keywords** | Optional | User provides; system also auto-discovers |
| **Client context file** | Optional | `clients/<client>/context.md` for ICP, positioning |

## Cost

| Component | Est. Cost |
|-----------|-----------|
| Content catalog (target) | ~$0-0.50 (free unless Apify fallback needed) |
| Semrush data (target) | ~$0.10 |
| Ahrefs data (target) | ~$0.10 |
| Google rank checks (~30 keywords) | ~$0.06 |
| Competitor Semrush data (3-5 competitors) | ~$0.30-0.50 |
| Content catalog (competitors, lighter) | ~$0-1.00 |
| Brand voice extraction | Free (WebFetch) |
| **Total typical audit** | **~$1-3** |

## Step-by-Step Process

### Phase 1: Context & Setup

1. **Load context:** If `clients/<client>/context.md` exists, read it for company info, known competitors, positioning
2. **Gather basics:** Company name, domain, seed competitors, target keywords
3. **Create output directory:** `clients/<client>/research/`

### Phase 2: Content Inventory

Run `site-content-catalog` for the target domain:

```bash
python3 skills/site-content-catalog/scripts/catalog_content.py \
  --domain "[domain]" \
  --deep-analyze 20 \
  --output "clients/[client]/research/content-inventory.json" \
  --markdown "clients/[client]/research/content-inventory.md"
```

This produces:
- Full page catalog (every URL, title, date, type, topic cluster)
- Content grouped by type and topic
- Publishing cadence analysis

### Phase 3: SEO Performance Data

Run `seo-domain-analyzer` for the target domain:

```bash
python3 skills/seo-domain-analyzer/scripts/analyze_domain.py \
  --domain "[domain]" \
  --competitors "[comma-separated competitors]" \
  --keywords "[comma-separated keywords]" \
  --output "clients/[client]/research/seo-profile.json" \
  --markdown "clients/[client]/research/seo-profile.md"
```

This produces:
- Domain authority, traffic estimates, keyword count
- Backlink profile (DR, referring domains)
- Keyword ranking positions for target keywords
- Auto-discovered competitors from keyword overlap
- Competitor domain metrics for comparison

### Phase 4: Competitor Content Analysis

For each competitor (3-5 max), run a lighter content catalog:

```bash
# For each competitor domain:
python3 skills/site-content-catalog/scripts/catalog_content.py \
  --domain "[competitor]" \
  --output "clients/[client]/research/competitor-[name]-content.json"
```

We only need:
- Content type breakdown (how many blog posts, case studies, comparisons, etc.)
- Topic clusters (what topics they cover)
- Publishing cadence (how often they publish)

No deep analysis needed for competitors.

### Phase 5: Build Gap Matrices

Using data from Phases 2-4, build two matrices:

#### A) Topic/Keyword Gap Matrix

Cross-reference the target's keyword rankings and content topics against competitors:

```markdown
| Topic / Keyword | [Target] | [Comp 1] | [Comp 2] | [Comp 3] | Gap? |
|-----------------|----------|----------|----------|----------|------|
| cloud cost optimization | #4, 3 posts | #1, 12 posts | #2, 8 posts | #7, 5 posts | Partial |
| aws savings plans | No content | #3, 4 posts | No content | #1, 6 posts | YES |
| finops best practices | 1 post, not ranking | #5, 3 posts | #2, 7 posts | — | YES |
```

For each topic/keyword:
- Does the target have content? How much?
- Does the target rank for it? What position?
- Which competitors rank? How much content do they have?
- Is this a gap? (target has no/weak content, competitors are strong)

**How to build this:**
1. Collect all unique topic clusters from target + all competitors
2. For each topic, count content pieces per company
3. Cross-reference with keyword ranking data (from Phase 3)
4. Flag gaps where competitors have coverage and target doesn't

#### B) Content Type Gap Matrix

Compare what types of content each company produces:

```markdown
| Content Type | [Target] | [Comp 1] | [Comp 2] | [Comp 3] | Gap? |
|-------------|----------|----------|----------|----------|------|
| Blog posts | 89 | 156 | 112 | 45 | Volume gap |
| Comparison pages | 0 | 12 | 8 | 3 | YES |
| Case studies | 5 | 22 | 15 | 8 | Weak |
| Glossary / educational | 0 | 45 | 0 | 30 | YES |
| Integration pages | 12 | 34 | 28 | 15 | Partial |
| ROI calculator / tools | 0 | 1 | 2 | 0 | Opportunity |
| Webinars / video | 3 | 18 | 12 | 6 | Weak |
```

**How to build this:**
1. Use the content type classifications from all content catalogs
2. Count per type per company
3. Flag types where target is at zero or significantly behind competitors

### Phase 6: Brand Voice Extraction

Run `brand-voice-extractor` on the target's top content:

1. From the content inventory (Phase 2), select 10-15 of the best blog posts
   - Prioritize: most recent, longest, most diverse topics
2. WebFetch each page and analyze the writing
3. Produce brand voice guidelines (see brand-voice-extractor SKILL.md for full process)

### Phase 7: Synthesis & Report

Combine all findings into the final report. Save to `clients/<client>/research/seo-content-audit.md`.

---

## Output Template

```markdown
# SEO Content Audit: [Company Name]

**Date:** YYYY-MM-DD
**Domain:** [domain]
**Competitors analyzed:** [list]
**Data sources:** [Semrush (via Apify), Ahrefs (via Apify), Google SERP, sitemap crawl, RSS]

---

## Executive Summary

[3-5 sentences. Overall SEO health assessment. Biggest strength. Biggest gap.
Most important recommendation. How they compare to competitors overall.]

---

## 1. Content Inventory

### Overview
- **Total pages cataloged:** X
- **Blog posts:** X
- **Landing pages:** X
- **Case studies:** X
- **Comparison pages:** X
- **Other:** X

### Content by Topic Cluster
| Topic | Posts | % of Content | Most Recent |
|-------|-------|-------------|-------------|
| [Topic 1] | X | X% | YYYY-MM-DD |
| ... |

### Publishing Cadence
- **Average:** X posts/month
- **Trend:** [increasing/decreasing/stable]
- **Most recent publish:** YYYY-MM-DD
- **Unique authors:** X

### Content Depth Assessment
[From deep analysis of top 20 pages: average word count, funnel stage distribution,
how many have CTAs, internal linking patterns]

---

## 2. SEO Performance

### Domain Metrics
| Metric | [Target] | Industry Benchmark* |
|--------|----------|-------------------|
| Authority Score (Semrush) | X/100 | |
| Domain Rating (Ahrefs) | X/100 | |
| Monthly Organic Traffic | ~X | |
| Organic Keywords | X | |
| Backlinks | X | |
| Referring Domains | X | |

### Top Performing Pages
| # | URL | Est. Traffic | Top Keyword | Position |
|---|-----|-------------|-------------|----------|
| 1 | ... | ... | ... | ... |

### Keyword Rankings
| Keyword | Position | URL | Gap? |
|---------|----------|-----|------|
| [keyword 1] | #X | [url] | |
| [keyword 2] | Not ranking | — | YES |

### Backlink Profile
- Domain Rating: X/100
- Referring Domains: X
- Top linking sites: [list]
- Notable: [any insights about link profile quality]

---

## 3. Competitor Comparison

### Domain Metrics Comparison
| Metric | [Target] | [Comp 1] | [Comp 2] | [Comp 3] |
|--------|----------|----------|----------|----------|
| Authority Score | | | | |
| Organic Traffic | | | | |
| Keywords | | | | |
| Blog Posts | | | | |
| Content Types | | | | |

### Topic/Keyword Gap Matrix
| Topic / Keyword | [Target] | [Comp 1] | [Comp 2] | [Comp 3] | Gap? |
|-----------------|----------|----------|----------|----------|------|
| [topic 1] | X posts, #Y | ... | ... | ... | |
| ... |

### Content Type Gap Matrix
| Content Type | [Target] | [Comp 1] | [Comp 2] | [Comp 3] | Gap? |
|-------------|----------|----------|----------|----------|------|
| Blog posts | X | X | X | X | |
| Comparison pages | X | X | X | X | |
| Case studies | X | X | X | X | |
| ... |

---

## 4. Gaps & Opportunities

### Critical Gaps (High Impact, Act Now)
1. **[Gap]:** [Description. What competitors have that target doesn't.
   Estimated search volume / traffic opportunity. Difficulty to address.]
2. ...

### Content Type Opportunities
1. **[Missing content type]:** [Why it matters. What competitors are doing.
   Estimated effort to create.]
2. ...

### Quick Wins (Low Effort, Immediate Impact)
1. **[Quick win]:** [What to do. Expected impact.]
2. ...

### Keyword Opportunities
| Keyword | Est. Search Volume | Competitor Positions | Difficulty | Priority |
|---------|-------------------|---------------------|------------|----------|
| ... |

---

## 5. Brand Voice Profile

### Voice Summary
[2-3 sentence summary of their writing voice]

### Tone
| Dimension | Position |
|-----------|----------|
| Formality | [e.g., Professional-casual] |
| Authority | [e.g., Expert/teacher] |
| Humor | [e.g., None] |
| Directness | [e.g., Very direct] |

### Writing Guidelines
**Do:**
- [Guideline 1]
- [Guideline 2]

**Don't:**
- [Anti-pattern 1]
- [Anti-pattern 2]

[Link to full brand voice profile at clients/<client>/research/brand-voice.md]

---

## 6. Recommendations (Prioritized)

### Tier 1: High Impact, Do First
1. **[Recommendation]**
   - What: [specific action]
   - Why: [evidence from audit]
   - Expected impact: [traffic/ranking improvement]
   - Effort: [Low/Medium/High]

2. ...

### Tier 2: Medium Impact, Plan For
1. ...

### Tier 3: Long-term Strategic
1. ...

---

## Appendix

### A. Full Content Catalog
[Link to content-inventory.md]

### B. Complete SEO Profile
[Link to seo-profile.md]

### C. Brand Voice Guidelines
[Link to brand-voice.md]

### D. Raw Data
- Content inventory JSON: `clients/[client]/research/content-inventory.json`
- SEO profile JSON: `clients/[client]/research/seo-profile.json`
- Competitor content JSONs: `clients/[client]/research/competitor-*.json`
```

---

## Tips

- **Run Phases 2-3 in parallel.** Content cataloging and SEO metrics are independent — run them simultaneously to save time.
- **Start with 3 competitors, not 5.** More competitors = more Apify costs. Start small, add more if the initial analysis shows gaps.
- **The gap matrices are the most valuable output.** Focus your analysis effort there. They directly feed into content strategy recommendations.
- **Brand voice is optional but valuable.** If you're pressed for time, skip it. But if this feeds into content creation or outreach, it's worth the 10 minutes.
- **Update quarterly.** SEO landscapes shift. Re-run the audit every quarter to track progress and discover new gaps.
- **Combine with AEO visibility** for a complete organic search picture — traditional SEO + AI answer engine coverage.
- **The free fallback works.** If Apify is unavailable, the scripts fall back to web search probes. You get less precise data but still a useful audit.

## Dependencies

- Python 3.8+ with `requests`
- `APIFY_API_TOKEN` env var (for full analysis; partial free fallback without)
- Skills: `site-content-catalog`, `seo-domain-analyzer`, `brand-voice-extractor`
- Web fetch capability (for brand voice extraction and content deep analysis)
