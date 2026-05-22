---
name: search-ad-keyword-architect
description: >
  Deep keyword research for paid search. Analyzes competitor SEO keywords, review language,
  Reddit/community terminology, and existing site content to build a keyword architecture:
  branded vs non-branded, funnel stage mapping, match type recommendations, and estimated
  competition tiers. Use before building a Google Ads campaign or to audit an existing one.
tags: [seo]
---

# Search Ad Keyword Architect

Build a comprehensive keyword architecture for paid search campaigns. Goes beyond basic keyword lists by organizing terms into a strategic framework: funnel stages, intent buckets, match types, and competitive density tiers.

**Core principle:** Bad keyword strategy is the #1 reason startups waste money on Google Ads. This skill builds the strategic foundation before you write a single ad.

## When to Use

- "Do keyword research for our Google Ads"
- "What keywords should we bid on?"
- "Build a keyword strategy for paid search"
- "Audit our existing keyword list"
- "Find high-intent keywords in our space"

## Phase 0: Intake

1. **Product name + URL** — What are we advertising?
2. **Product category** — How would a buyer search for this? (e.g., "sales automation", "AI writing tool")
3. **ICP** — Target buyer role, company stage, pain points
4. **Competitor domains** — 3-5 competitors
5. **Monthly PPC budget** — Affects aggressiveness of recommendations
6. **Existing keywords?** — Currently bidding on anything?
7. **Known converting keywords?** — Any existing performance data

## Phase 1: Keyword Universe Building

### 1A: Competitor SEO Keyword Mining

For each competitor, research their organic keyword rankings:

```bash
# If seo-domain-analyzer available:
python3 skills/seo-domain-analyzer/scripts/analyze_domain.py \
  --domain <competitor_domain> \
  --output json
```

Also web search:
```
Search: site:<competitor_domain> [product category keywords]
Search: <competitor> SEO keywords ranking
Search: <competitor> top pages organic traffic
```

Extract keywords with buying intent — skip informational-only terms.

### 1B: Review & Community Language Mining

The exact language buyers use matters more than what marketers think they search:

**Reviews:**
```bash
python3 skills/review-scraper/scripts/scrape_reviews.py \
  --product "<your product>" \
  --product "<competitor>" \
  --platforms g2,capterra \
  --output json
```

Extract phrases like:
- "I was looking for a [term] that could..."
- "We switched from [X] because we needed..."
- "Best [term] for [use case]"

**Reddit:**
```bash
python3 skills/reddit-scraper/scripts/scrape_reddit.py \
  --query "best <category> tool OR software OR platform" \
  --sort relevance \
  --time year \
  --limit 30
```

**Hacker News:**
```bash
python3 skills/hacker-news-scraper/scripts/scrape_hn.py \
  --query "<product category>" \
  --type story \
  --limit 20
```

### 1C: Your Site Content Audit

```bash
python3 skills/site-content-catalog/scripts/catalog_site.py \
  --url <your_website> \
  --output json
```

Identify:
- Pages that could serve as landing pages
- Keywords your content already ranks for (leverage in ads)
- Gaps — search terms you're not covering

### 1D: Search Suggest & Related Terms

```
Search: "[category] tool" → note Google autocomplete suggestions
Search: "[category] software for [ICP role]"
Search: "[pain point] solution"
Search: "how to [problem your product solves]"
```

## Phase 2: Keyword Architecture

### 2A: Funnel Stage Mapping

Organize all keywords by buyer journey stage:

| Stage | Intent Signal | Example Keywords | Bid Priority |
|-------|--------------|-----------------|-------------|
| **Problem-aware** | Searching for solutions to a pain | "how to scale outbound without hiring SDRs" | Medium — educational intent |
| **Solution-aware** | Searching for a category | "AI SDR tool", "outbound automation platform" | High — comparing options |
| **Product-aware** | Searching for specific products | "[competitor] alternative", "[competitor] vs" | Very high — close to purchase |
| **Most-aware** | Searching for your brand | "[your brand]", "[your brand] pricing" | Must-have — defend brand |

### 2B: Intent Classification

| Intent Type | Ad Group Strategy | Landing Page Strategy |
|-------------|------------------|---------------------|
| **Transactional** ("buy", "pricing", "free trial") | Aggressive bid, exact match | Direct product/pricing page |
| **Commercial** ("best", "top", "vs", "alternative") | Strong bid, exact + phrase | Comparison or feature page |
| **Informational** ("how to", "what is", "guide") | Low bid or skip — save for SEO | Blog/resource (if targeting) |
| **Navigational** (brand searches) | Must-bid, exact match | Homepage or brand LP |

### 2C: Competitive Density Assessment

For top 30 keywords, estimate competition level:

| Density | Signal | Strategy |
|---------|--------|----------|
| **Low** | Few ads showing, no big brands | Bid aggressively — first mover advantage |
| **Medium** | Some competitors, not saturated | Bid strategically — differentiate with copy |
| **High** | Major players dominating | Bid selectively — long-tail variants, exact match only |
| **Very high** | Big ad budgets, position 1-4 locked | Avoid head-on — focus on long-tail or competitor terms |

### 2D: Match Type Matrix

| Keyword | Exact [keyword] | Phrase "keyword" | Broad keyword | Recommendation |
|---------|----------------|-----------------|---------------|---------------|
| [keyword 1] | ✓ | ✓ | ✗ | Start exact, expand to phrase after data |
| [keyword 2] | ✓ | ✗ | ✗ | Exact only — too broad in phrase |
| [keyword 3] | ✓ | ✓ | ✓ | All match types — high-volume, need coverage |

## Phase 3: Negative Keyword Architecture

### Category Negatives

```
[Industry]-specific terms that share words with your keywords but wrong intent
```

### Intent Negatives

```
jobs, careers, hiring, salary, internship
free, open source, download (if not applicable)
tutorial, course, certification, how to become
login, support, help, documentation
review, reddit, quora, forum (if not desired)
```

### Competitor Brand Negatives (Optional)

If not running competitor campaigns, negative-match competitor brand names to prevent waste.

## Phase 4: Output Format

```markdown
# Keyword Architecture — [Product Name] — [DATE]

## Research Summary
- Sources analyzed: [competitor SEO, reviews, Reddit, HN, site audit]
- Total keywords discovered: [N]
- After dedup + filtering: [N]
- Recommended for campaign: [N]

---

## Keyword Universe by Funnel Stage

### Most-Aware (Brand Defense)
| Keyword | Match Type | Est. Volume | Competition | Priority |
|---------|-----------|------------|-------------|----------|
| [keyword] | Exact | [H/M/L] | Low | Must-have |

### Product-Aware (Competitor Capture)
| Keyword | Match Type | Est. Volume | Competition | Priority |
...

### Solution-Aware (Category)
...

### Problem-Aware (Top of Funnel)
...

---

## Recommended Ad Group Structure

| Ad Group | Theme | Keywords | Match Types | Landing Page |
|----------|-------|----------|------------|-------------|
| [Name] | [Theme] | [N] keywords | [Exact + Phrase] | [URL] |

---

## Negative Keyword Lists

### Campaign-Level Negatives
[List]

### Ad Group-Level Negatives
[Per ad group]

---

## Competitive Density Map

| Keyword Theme | Your Position | Top Competitors Bidding | Density | Recommendation |
|--------------|--------------|------------------------|---------|---------------|
| [Theme] | [Not bidding / Bidding] | [Names] | [H/M/L] | [Bid / Skip / Long-tail] |

---

## Quick Wins (Start Here)

Top 10 keywords to launch with — highest intent, manageable competition:

| # | Keyword | Match Type | Intent | Competition | Why |
|---|---------|-----------|--------|-------------|-----|
| 1 | [keyword] | Exact | Transactional | Medium | [Reason] |
...

---

## Budget Allocation Recommendation

| Funnel Stage | % of Budget | Reasoning |
|-------------|------------|-----------|
| Brand defense | [X%] | Protect brand searches |
| Competitor capture | [X%] | High-intent, ready to switch |
| Solution-aware | [X%] | Category buyers — highest volume |
| Problem-aware | [X%] | Only if budget allows |
```

Save to `clients/<client-name>/ads/keyword-architecture-[YYYY-MM-DD].md`.

## Cost

| Component | Cost |
|-----------|------|
| SEO domain analyzer (per competitor) | ~$0.10-0.30 (Apify) |
| Review scraper | ~$0.10-0.30 (Apify) |
| Reddit scraper | ~$0.05-0.10 (Apify) |
| HN scraper | Free |
| Site content catalog | Free-$0.10 |
| Analysis | Free (LLM reasoning) |
| **Total for 3 competitors** | **~$0.50-1.50** |

## Tools Required

- **Apify API token** — `APIFY_API_TOKEN` env var
- **Upstream skills:** `seo-domain-analyzer`, `review-scraper`, `reddit-scraper`, `hacker-news-scraper`, `site-content-catalog`
- **web_search** — for keyword discovery

## Trigger Phrases

- "Do keyword research for Google Ads"
- "What keywords should we bid on?"
- "Build a keyword architecture for [product]"
- "Find high-intent search keywords"
- "Audit our PPC keyword strategy"
