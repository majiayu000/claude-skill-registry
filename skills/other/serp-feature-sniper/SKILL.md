---
name: serp-feature-sniper
description: >
  Analyze SERP features per keyword (featured snippets, PAA, video carousels,
  knowledge panels, image packs) and produce optimized content structures to win
  them. Identifies which features are winnable, who currently holds them, and
  exactly how to format your content to steal them.
tags: [seo]
---

# SERP Feature Sniper

Most SEO content targets "page 1" generically. But the real estate that drives clicks — featured snippets, People Also Ask boxes, video carousels, image packs — follows specific formatting rules. This skill analyzes what SERP features exist for your keywords, who holds them, and builds content structures optimized to take them.

**Core principle:** A featured snippet isn't won by accident. It's won by formatting a specific answer in a specific way (paragraph, list, table) that matches what Google expects. This skill reverse-engineers the format Google wants, then tells your writer exactly how to structure their content.

## When to Use

- "How do I win featured snippets for these keywords?"
- "What SERP features can we target?"
- "Optimize our content for PAA boxes"
- "Which of our pages could win SERP features with small changes?"
- "SERP feature audit for our keyword list"

## Tool Enhancement (Optional)

SERP feature analysis is dramatically better with real-time SERP data showing exactly which features appear, who holds them, and what content format they use.

### Agent Prompt to User

> "I can analyze SERP features and build content structures to win them. For the most accurate results — seeing exactly which features appear on each SERP and who currently holds them — I'd recommend connecting a SERP data API."
>
> **Recommended: SerpAPI** (100 free searches/month, $50/month for 5,000)
> - Sign up at serpapi.com → get API key
> - Set `SERPAPI_KEY` env var
>
> **Alternatives that also work:**
> - **Serper.dev** (2,500 free searches, then $50/month for 50K) → set `SERPER_API_KEY`
> - **DataForSEO SERP** (pay-per-use, ~$0.01/search) → set `DATAFORSEO_LOGIN` + `DATAFORSEO_PASSWORD`
> - **ValueSERP** (free tier available) → set `VALUESERP_API_KEY`
>
> "Want to use one of these, or should I proceed with baseline mode? Baseline uses web search to identify SERP features — still produces strong optimization plans, but with less precise feature detection and holder identification."

### Mode Selection

- **Enhanced mode** — Real SERP API data per keyword: exact features present, current feature holders, snippet content/format, PAA questions and their current answers, related searches. Enables precise "here's exactly what to write to steal this snippet" guidance.
- **Baseline mode** — Uses `web_search` to analyze SERPs, `fetch_webpage` to study current feature holders. Feature detection is based on search result patterns. Still produces excellent optimization plans — the content structuring and formatting guidance doesn't change.

## Phase 0: Intake

1. **Keywords** — List of target keywords (1-100)
2. **Your site URL** — So we can check if you already hold any features
3. **Existing content URLs** — Pages you want to optimize for features (optional — if blank, we focus on new content)
4. **Priority features** — Any specific features you care about? (featured snippets, PAA, video, images, all?)
5. **Content format flexibility** — Can you add tables, lists, images, videos, or are you limited to text?
6. **Tool preference** — Enhanced mode with SERP API, or baseline? (see Tool Enhancement above)

## Phase 1: SERP Feature Audit

### Enhanced Mode (SerpAPI / Serper / DataForSEO)

For each keyword, query the SERP API:

```
# SerpAPI example
GET https://serpapi.com/search?q={keyword}&api_key={key}&num=10
```

Extract per keyword:
- **Featured snippet** — Present? Type (paragraph/list/table)? Current holder? Snippet content?
- **People Also Ask** — Questions listed? How many? Current answers?
- **Video carousel** — Present? Sources (YouTube, other)?
- **Image pack** — Present? Source pages? Alt text patterns?
- **Knowledge panel** — Present? Source? Editable?
- **Local pack** — Present? (skip if not relevant)
- **Shopping results** — Present? (skip if not relevant)
- **Top stories** — Present? Sources?
- **Site links** — Who has them?
- **FAQ rich results** — Who has them?

### Baseline Mode

For each keyword, use `web_search`:
- Analyze result format for feature indicators
- Check for "Featured snippet from..." patterns
- Note PAA boxes that appear
- Spot-check 3-5 results via `fetch_webpage` for schema markup

## Phase 2: Feature Holder Analysis

For each keyword with winnable features, analyze the current holder:

### 2A: Featured Snippet Analysis

Fetch the current snippet holder's page via `fetch_webpage`:

- **Content format** — Paragraph (40-60 words), numbered list, bulleted list, or table?
- **Placement on page** — Where is the snippet content within the page structure?
- **Heading structure** — What H2/H3 triggers the snippet?
- **Answer directness** — Does the answer start immediately after the heading?
- **Page authority** — Domain rating, page age
- **Vulnerabilities** — Is the answer outdated? Too long? Missing context? Poorly formatted?

### 2B: PAA Analysis

For each PAA question:
- **Current answer source** — Which page answers it?
- **Answer format** — Paragraph, list, or table?
- **Answer length** — How many words?
- **Answer quality** — Comprehensive or thin?
- **Your coverage** — Do you already answer this on your site?

### 2C: Rich Result Analysis

Check current top 5 pages for:
- **FAQ schema** — Present? How many Q&A pairs?
- **HowTo schema** — Present? Step count?
- **Review schema** — Present? Rating?
- **Article schema** — Present? Type?
- **Breadcrumb schema** — Present?

## Phase 3: Winnability Assessment

Score each keyword × feature combination:

| Factor | Weight | Description |
|--------|--------|-------------|
| **Feature exists** | Required | No feature = nothing to win |
| **Current holder weakness** | 30% | Outdated, thin, poorly formatted = easier to steal |
| **Your domain authority** | 25% | Need minimum authority to compete |
| **Content format match** | 20% | Can you produce the format Google wants? |
| **Effort to create/modify** | 15% | New content vs. quick edit to existing page |
| **Traffic value** | 10% | Search volume × CTR boost from feature |

**Winnability tiers:**
- **High (70-100):** Weak current holder + you have authority + low effort → prioritize
- **Medium (40-69):** Competitive but achievable → include in content plan
- **Low (0-39):** Strong holder or feature doesn't exist → deprioritize

## Phase 4: Optimization Blueprints

For each winnable feature, produce specific formatting guidance:

### Featured Snippet Blueprint

```markdown
## Keyword: [target keyword]
**Current holder:** [URL] | **Format:** [paragraph/list/table]
**Winnability:** [High/Medium/Low]

### How to Win This Snippet

**Target heading:** Use this exact H2:
> ## [Heading that triggers the snippet — matches query intent]

**Answer format:** [Paragraph / Numbered list / Bulleted list / Table]

**If paragraph snippet:**
- Write a 40-60 word direct answer immediately after the H2
- Start with "[Keyword] is..." or "The [keyword] refers to..."
- Include the target keyword in the first sentence
- Be more precise and current than the current holder

**If list snippet:**
- Use a numbered or bulleted list of 5-8 items
- Each item should be 10-20 words
- Start each item with a strong verb or noun
- Include the complete list (not truncated)

**If table snippet:**
- Use a clean HTML/markdown table with 3-5 columns
- Include column headers that match the query dimensions
- Fill all cells with actual data (no blanks)
- Keep to 4-8 rows

**Content to write:**
[Specific paragraph/list/table draft optimized for snippet capture]

**Page placement:** Place this within the top 30% of page content
```

### PAA Optimization Blueprint

```markdown
## PAA Questions to Target

### Q: [Question 1]
**Current answer:** [summary] from [source]
**Your optimized answer:**
- H2: "[Question phrased as heading]"
- Answer: [50-80 word direct answer]
- Format: [paragraph/list]
- Include: [specific details to be more comprehensive than current answer]

### Q: [Question 2]
...
```

### Schema Markup Blueprint

```markdown
## Recommended Schema

### FAQ Schema
Add to page: [URL]
```json
{
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Question]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer]"
      }
    }
  ]
}
```

### HowTo Schema (if applicable)
[Step-by-step schema with estimated time and tools]
```

## Phase 5: Output

```markdown
# SERP Feature Sniper Report — [Site/Client] — [DATE]

## Executive Summary
- Keywords analyzed: [N]
- Keywords with winnable features: [N] ([%])
- High-priority targets: [N] featured snippets, [N] PAA boxes, [N] rich results
- Estimated CTR uplift if features won: [X]% average

---

## Feature Landscape

| Keyword | Volume | Featured Snippet | PAA | Video | Images | Rich Results | Your Status |
|---------|--------|-----------------|-----|-------|--------|-------------|-------------|
| [kw1] | [vol] | ✓ Paragraph — [holder] | ✓ 4 Qs | ✗ | ✓ | FAQ | Not ranking |
| [kw2] | [vol] | ✓ List — [holder] | ✓ 6 Qs | ✓ | ✗ | None | #5 |
| [kw3] | [vol] | ✗ | ✓ 3 Qs | ✗ | ✗ | HowTo | #3 |

---

## Priority Actions

### Tier 1: Quick Wins (existing pages, minor edits)
| Page | Keyword | Feature | Action Required | Effort |
|------|---------|---------|----------------|--------|
| [URL] | [kw] | Featured snippet | Add [format] answer under H2 "[heading]" | 30 min |
| [URL] | [kw] | FAQ rich result | Add FAQ schema with [N] Q&As | 15 min |

### Tier 2: Content Updates (existing pages, significant edits)
| Page | Keyword | Feature | Action Required | Effort |
|------|---------|---------|----------------|--------|
| [URL] | [kw] | Featured snippet | Restructure [section] as [format] | 2 hours |

### Tier 3: New Content Needed
| Keyword | Feature | Content Type | Blueprint Reference |
|---------|---------|-------------|-------------------|
| [kw] | Featured snippet + PAA | [type] | See Brief #[N] |

---

## Detailed Blueprints

### Blueprint 1: [Keyword]
[Full optimization blueprint per Phase 4]

### Blueprint 2: [Keyword]
...

---

## Schema Markup Checklist
- [ ] Add FAQ schema to [URL] — [N] Q&A pairs
- [ ] Add HowTo schema to [URL] — [N] steps
- [ ] Add Article schema to [URL] — [type]
- [ ] Validate all schema at search.google.com/test/rich-results

---

## Monitoring Plan
- Re-check SERP features monthly for target keywords
- Track feature wins/losses in [tool]
- Re-optimize if feature is lost or format changes
```

Save to `clients/<client-name>/seo/serp-feature-report-[YYYY-MM-DD].md`.

## Cost

| Component | Cost |
|-----------|------|
| SerpAPI (enhanced, per keyword) | ~$0.01-0.05 per keyword |
| Serper.dev (enhanced, per keyword) | ~$0.001 per keyword |
| Page fetches (feature holders) | ~$0.01-0.03 per keyword |
| SEO domain analyzer | ~$0.10-0.20 |
| Analysis | Free (LLM reasoning) |
| **Total per keyword (baseline)** | **~$0.03-0.08** |
| **Total per keyword (enhanced)** | **~$0.05-0.12** |
| **Batch of 50 keywords (baseline)** | **~$1.50-4.00** |
| **Batch of 50 keywords (enhanced)** | **~$2.50-6.00** |

## Tools Required

- **Upstream skills:** `seo-domain-analyzer`, `fetch_webpage`, `web_search`
- **Optional (enhanced):** SerpAPI (`SERPAPI_KEY`), Serper.dev (`SERPER_API_KEY`), DataForSEO (`DATAFORSEO_LOGIN` + `DATAFORSEO_PASSWORD`), or ValueSERP (`VALUESERP_API_KEY`)

## Scheduling

For ongoing SERP feature monitoring:
- Run monthly against target keyword list
- Compare with previous month's report to detect feature changes
- Flag new features appearing and features lost
- Schedule: First Monday of each month

## Trigger Phrases

- "How do I win featured snippets?"
- "SERP feature audit for our keywords"
- "Optimize our content for rich results"
- "Which pages can win SERP features?"
- "Steal featured snippets from competitors"
- "PAA optimization plan"
