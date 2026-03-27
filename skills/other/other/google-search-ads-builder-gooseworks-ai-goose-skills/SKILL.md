---
name: google-search-ads-builder
description: >
  End-to-end Google Search Ads campaign builder. Takes ICP + product info, performs
  keyword research via competitive analysis, builds ad group structure, generates
  headline/description variants, creates negative keyword lists, recommends bid strategy,
  and exports a campaign-ready CSV for Google Ads Editor import.
tags: [ads]
---

# Google Search Ads Builder

Build a complete Google Search Ads campaign from scratch. This skill handles everything from keyword research to ad copy to campaign structure — outputting files ready to import into Google Ads Editor.

**Core principle:** Most early-stage teams waste their first $5K on Google Ads because of bad structure. This skill builds a tight, well-organized campaign from day one: right keywords, right match types, right ad groups, right negatives.

## When to Use

- "Set up Google Search Ads for us"
- "Build a Google Ads campaign for [product]"
- "I want to start running search ads — help me set it up"
- "Create a PPC campaign structure"
- "Generate Google Ads copy for our product"

## Phase 0: Intake

1. **Product name + URL** — What are we advertising?
2. **One-line value prop** — What does it do, for whom?
3. **ICP** — Who is searching for this? (Role, pain, company stage)
4. **Monthly budget** — What are you willing to spend? (Affects structure recommendations)
5. **Goal** — Free trial sign-ups / Demo bookings / Content downloads / Direct purchase
6. **Landing pages** — URLs you'll send traffic to (or "need to create")
7. **Competitor domains** — 2-5 competitors (for keyword gap analysis)
8. **Geographic targeting** — Countries/regions
9. **Existing keywords?** — Any keywords you already know work

## Phase 1: Keyword Research

### 1A: Seed Keyword Generation

From the product description and ICP, generate 3 keyword buckets:

| Bucket | Intent | Examples |
|--------|--------|---------|
| **Problem-aware** | Searching for solutions to a pain | "how to automate outbound", "fix slow sales pipeline" |
| **Solution-aware** | Searching for a category of product | "AI SDR tool", "outbound automation software" |
| **Brand/Competitor** | Searching for you or competitors by name | "[your brand]", "[competitor] alternative" |

### 1B: Competitive Keyword Mining

Research competitor SEO keywords that indicate search ad opportunity:

```
Search: "[competitor] site:google.com/ads" OR "[competitor] PPC keywords"
Search: "[competitor]" alternative OR vs OR comparison
Search: best [product category] tools 2026
```

Also run `seo-domain-analyzer` on competitor domains to find keywords they rank for that indicate buying intent.

### 1C: Keyword Expansion

For each seed keyword, expand with:
- **Modifiers:** best, top, free, cheap, enterprise, for startups, for [role]
- **Long-tail:** "[category] for [specific use case]"
- **Question queries:** "how to [solve problem your product addresses]"
- **Comparison:** "[competitor] vs [your brand]", "[competitor] alternative"

### 1D: Keyword Scoring

| Keyword | Est. Volume | Intent Strength | Competition | Priority |
|---------|------------|----------------|-------------|----------|
| [keyword] | [H/M/L] | [High/Med/Low] | [H/M/L] | [1-5] |

**Priority scale:**
- **5** = High intent + medium competition (sweet spot)
- **4** = High intent + high competition (important but expensive)
- **3** = Medium intent + low competition (good for budget stretch)
- **2** = Low intent + low competition (awareness only)
- **1** = Skip — too broad or irrelevant

## Phase 2: Campaign Structure

### 2A: Ad Group Design

Group keywords by theme and intent. Each ad group = one tight topic.

**Structure template:**

```
Campaign: [Product Name] — Search
├── Ad Group: [Problem Keyword Theme 1]
│   ├── Keywords (5-15 per group)
│   └── Ads (3 responsive search ads)
├── Ad Group: [Problem Keyword Theme 2]
├── Ad Group: [Solution Category]
├── Ad Group: [Competitor Alternatives]
│   ├── "[Competitor A] alternative"
│   ├── "[Competitor B] alternative"
│   └── "best [category] alternative"
└── Ad Group: [Brand]
    └── "[Your brand name]" (defense)
```

**Rules:**
- Max 15 keywords per ad group
- All keywords in an ad group should share a theme
- Each ad group gets its own landing page (if possible)
- Use a mix of match types: Exact [keyword] for high-intent, Phrase "keyword" for discovery

### 2B: Match Type Strategy

| Keyword Type | Recommended Match | Reason |
|-------------|-------------------|--------|
| Brand terms | Exact | Protect — don't waste spend on broad |
| High-intent solution | Exact + Phrase | Capture precisely, discover adjacent |
| Competitor terms | Exact + Phrase | Control the narrative |
| Problem-aware | Phrase + Broad (with negatives) | Cast wider net for top-of-funnel |

## Phase 3: Ad Copy Generation

### Per Ad Group: 3 Responsive Search Ads

Each RSA needs:
- **15 headlines** (max 30 chars each)
- **4 descriptions** (max 90 chars each)

### Headline Framework (15 per ad group)

| Slot | Purpose | Example |
|------|---------|---------|
| 1-3 | **Keyword match** — Include the search term | "AI Outbound Automation" |
| 4-5 | **Value prop** — Primary benefit | "10x Your Pipeline in 30 Days" |
| 6-7 | **Social proof** — Credibility | "Trusted by 500+ B2B Teams" |
| 8-9 | **Differentiation** — Why you vs alternatives | "No-Code Setup in 5 Minutes" |
| 10-11 | **CTA** — Action driver | "Start Free Trial Today" |
| 12-13 | **Offer/Urgency** — Incentive | "Free 14-Day Trial" |
| 14-15 | **Trust/Risk reversal** — Remove friction | "No Credit Card Required" |

### Description Framework (4 per ad group)

| Slot | Purpose | Example |
|------|---------|---------|
| 1 | **Feature-benefit** — What + so what | "Automate personalized outbound emails so your team closes more deals without the manual work." |
| 2 | **Pain-agitate** — Problem + solution | "Tired of reps spending 4 hours on prospecting? Our AI handles it in minutes." |
| 3 | **Social proof + CTA** | "Join 500+ growth teams. Start your free trial — no credit card needed." |
| 4 | **Differentiator + CTA** | "Unlike legacy tools, [Product] works out of the box. See it in action — book a 15-min demo." |

## Phase 4: Negative Keywords

### Universal Negatives (Apply to all campaigns)

```
free (if not freemium)
jobs, careers, hiring, salary
tutorial, course, certification, learn
review, reddit, quora (if not desired)
login, support, help desk
download, open source (if not applicable)
```

### Category-Specific Negatives

Based on keyword research, add terms that would waste spend — searches related to your keywords but with wrong intent.

## Phase 5: Bid Strategy Recommendation

| Budget Range | Recommended Strategy | Reason |
|-------------|---------------------|--------|
| < $1K/mo | Manual CPC or Max Clicks | Need data first — don't let Google optimize on nothing |
| $1K-5K/mo | Max Conversions (after 30+ conversions) | Enough data for Google's algo |
| $5K+/mo | Target CPA or Target ROAS | Optimize for efficiency at scale |

**First 2 weeks:** Always start with Manual CPC or Max Clicks with a daily budget cap. Collect data before switching to automated bidding.

## Phase 6: Output Format

### 6A: Campaign Strategy Doc

```markdown
# Google Search Ads Campaign — [Product Name] — [DATE]

## Campaign Overview
- **Goal:** [Conversions / Demos / Trials]
- **Monthly budget:** $[X]
- **Geographic targeting:** [Countries]
- **Bid strategy (start):** [Manual CPC / Max Clicks]
- **Bid strategy (after 30 conversions):** [Max Conversions / Target CPA]

## Campaign Structure
[Visual tree of campaigns → ad groups]

## Keywords by Ad Group

### Ad Group: [Name]
**Landing page:** [URL]
| Keyword | Match Type | Priority |
|---------|-----------|----------|
| [keyword] | Exact | High |
| [keyword] | Phrase | Medium |

### Ad Group: [Name 2]
...

## Ad Copy

### Ad Group: [Name]
**RSA 1:**
Headlines: [list of 15]
Descriptions: [list of 4]

**RSA 2:** ...
**RSA 3:** ...

## Negative Keywords
[Grouped list]

## Bid & Budget Recommendations
[Strategy + daily budget recommendation]

## Launch Checklist
- [ ] Verify landing pages load and track conversions
- [ ] Set up conversion tracking (Google Tag / GA4)
- [ ] Confirm geographic targeting
- [ ] Set daily budget cap
- [ ] Review ad extensions (sitelinks, callouts, structured snippets)
- [ ] Enable search term report review (weekly)
```

### 6B: Google Ads Editor Import CSV

Generate a CSV file importable into Google Ads Editor:

```csv
Campaign,Ad Group,Keyword,Match Type,Max CPC,Final URL,Headline 1,Headline 2,Headline 3,Description 1,Description 2
```

Save strategy doc to `clients/<client-name>/ads/google-search-campaign-[YYYY-MM-DD].md`.
Save CSV to `clients/<client-name>/ads/google-ads-import-[YYYY-MM-DD].csv`.

## Cost

| Component | Cost |
|-----------|------|
| Keyword research (web search) | Free |
| Competitor SEO analysis | ~$0.10-0.50 (Apify, if using seo-domain-analyzer) |
| Ad copy generation | Free (LLM reasoning) |
| CSV generation | Free |
| **Total** | **Free-$0.50** |

## Tools Required

- **web_search** — for keyword research and competitor analysis
- **fetch_webpage** — for landing page review
- **Optional:** `seo-domain-analyzer` for competitor keyword data

## Trigger Phrases

- "Set up Google Search Ads for [product]"
- "Build a PPC campaign"
- "Create Google Ads for our product"
- "I need search ad keywords and copy"
- "Generate a Google Ads Editor import file"
