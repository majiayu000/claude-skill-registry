---
name: ad-creative-intelligence
description: >
  Scrape competitor ads from Meta and Google ad libraries, cluster by hook/angle/format,
  and surface new creative directions your team hasn't tested. Chains meta-ad-scraper
  and google-ad-scraper. Use when a marketing team wants to understand the competitive
  ad landscape before launching a campaign, or wants fresh creative inspiration from
  what's already working in the market.
tags: [ads]
---

# Ad Creative Intelligence

Scrape competitor ads from Meta and Google, then analyze creative patterns — hooks, formats, angles, CTAs — to find directions you haven't tried and identify what's resonating in the market.

**Core principle:** The best ad creative teams don't guess. They start with evidence from what's already working, then differentiate.

## When to Use

- "What ads are my competitors running?"
- "Find new creative angles for our paid campaigns"
- "What hooks are working in [our space]?"
- "I want to audit the ad landscape before we launch"
- "What format — video, image, carousel — is dominant in our category?"

## Phase 0: Intake

1. Competitor names and website domains (e.g., `apollo.io`, `clay.run`)
2. Your own domain (to optionally include for self-audit comparison)
3. Channels to cover: Meta only, Google only, or both? (default: both)
4. Time range: active ads only (default) or historical?
5. What's your product category? (helps with analysis framing)

## Phase 1: Scrape Meta Ads

Run `meta-ad-scraper` for each competitor:

```bash
python3 skills/meta-ad-scraper/scripts/scrape_meta_ads.py \
  --domain <competitor_domain> \
  --output json
```

Collect per ad:
- Ad copy (headline + body text)
- Visual description / media type (image, video, carousel)
- CTA button text
- Landing page URL
- Estimated run time (active duration proxy)
- Platforms (Facebook, Instagram, etc.)

## Phase 2: Scrape Google Ads

Run `google-ad-scraper` for each competitor:

```bash
python3 skills/google-ad-scraper/scripts/scrape_google_ads.py \
  --domain <competitor_domain> \
  --output json
```

Collect per ad:
- Headline variants (up to 3)
- Description lines
- Ad type (search, display, YouTube)
- Landing page URL

## Phase 3: Cluster & Analyze

After collecting all ads, perform structured analysis:

### Hook Pattern Clustering

Group all ad headlines/openers by hook type:

| Hook Type | Pattern | Example |
|-----------|---------|---------|
| **Fear/Loss** | Risk of missing out or falling behind | "Your competitors are already using AI SDRs" |
| **Outcome** | Direct result promise | "10x your pipeline in 30 days" |
| **Question** | Challenges current assumption | "Still doing outbound manually?" |
| **Social proof** | Names customers or numbers | "Join 500+ B2B teams using [product]" |
| **Contrarian** | Challenges conventional wisdom | "Cold email isn't dead. Your copy is." |
| **Empathy** | Validates their pain | "We know SDR ramp time is brutal" |
| **Product-led** | Feature as hook | "[Feature] is live — see what's new" |

Count how many ads per competitor use each hook type. This reveals their primary messaging strategy.

### Format Distribution

| Format | Meta | Google |
|--------|------|--------|
| Static image | [N] | N/A |
| Video | [N] | [N] |
| Carousel | [N] | N/A |
| Search text | N/A | [N] |
| Display banner | N/A | [N] |

### CTA Taxonomy

List all unique CTAs found. Common patterns:
- Urgency: "Start free", "Try now", "Get started today"
- Low-friction: "See how it works", "Watch demo", "Learn more"
- Outcome: "Book a demo", "Get your free audit", "Calculate your ROI"

### Landing Page Analysis

For top-traffic ads (those running longest), note:
- What angle does the landing page reinforce?
- Is the LP general or campaign-specific?
- What's the primary conversion goal?

## Phase 4: Gap Analysis & Recommendations

Identify:

1. **Angles nobody is running** — Hook types absent from competitor ads = white space
2. **Overcrowded angles** — If everyone leads with "save time", avoid it or be more specific
3. **Format opportunities** — If no one is running video in your space, it may stand out
4. **Underutilized proof** — Are competitors avoiding specific proof points you could own?
5. **CTA patterns to test** — What CTAs do the longest-running ads use?

## Phase 5: Output Format

```markdown
# Ad Creative Intelligence Report — [DATE]

## Coverage
- Competitors analyzed: [list]
- Meta ads collected: [N]
- Google ads collected: [N]

---

## Meta Ad Analysis

### Hook Distribution
| Hook Type | [Comp1] | [Comp2] | [Comp3] |
|-----------|---------|---------|---------|
| Fear/Loss | 40% | 10% | 0% |
| Outcome | 30% | 50% | 60% |
...

### Top Performing Ads (Longest Running)
**[Competitor] — [Ad Title/Hook]**
> [Ad copy excerpt]
- Format: [type]
- CTA: [text]
- Running since: [date]
- Why it likely works: [analysis]

---

## Google Ad Analysis

### Headline Patterns
[Top headline structures with examples]

### Most Common CTAs
[ranked list]

---

## Creative Gap Analysis

### Angles Nobody Is Running
1. [Angle] — Why it could work for you: [reasoning]
2. [Angle] — ...

### Overcrowded Angles (Avoid or Differentiate)
- [Angle] — [N] of [N] competitors use this

### Format White Space
- [Format] is not being used by competitors on [platform]

---

## Recommended Creative Experiments

### Experiment 1: [Name]
- Platform: [Meta/Google]
- Format: [type]
- Hook angle: [type]
- Proposed headline: "[headline]"
- Proposed body: "[copy]"
- Why test this: [rationale]

### Experiment 2: ...
```

Save to `clients/<client-name>/intelligence/ad-creative-intel-[YYYY-MM-DD].md`.

## Cost

| Component | Cost |
|-----------|------|
| Meta ad scraper (per competitor) | ~$0.20-0.50 (Apify) |
| Google ad scraper (per competitor) | ~$0.20-0.50 (Apify) |
| **Total for 3 competitors** | **~$1-3** |

## Tools Required

- **Apify API token** — `APIFY_API_TOKEN` env var
- **Upstream skills:** `meta-ad-scraper`, `google-ad-scraper`

## Trigger Phrases

- "What ads are [competitor] running?"
- "Audit the ad landscape for [product category]"
- "Run ad creative intel for [client]"
- "Find new paid ad angles we haven't tried"
