---
name: competitor-ad-teardown
description: >
  Deep-dive analysis of a competitor's ad strategy. Scrapes their Meta + Google ads,
  reverse-engineers their funnel (ad → landing page → CTA), identifies positioning bets,
  and produces a strategic teardown. Goes beyond ad-creative-intelligence by analyzing
  the full conversion path and strategic intent behind each campaign.
tags: [ads]
---

# Competitor Ad Teardown

Go deeper than surface-level ad monitoring. Take a single competitor and reverse-engineer their entire paid strategy: what they're running, where they're sending traffic, what they're testing, what's working, and where they're vulnerable.

**Core principle:** A competitor's ad portfolio is a window into their growth strategy. Long-running ads reveal what converts. New ads reveal what they're testing. Landing pages reveal their positioning bets. This skill reads all the signals.

## When to Use

- "Tear down [competitor]'s ad strategy"
- "What's [competitor] spending their ad budget on?"
- "Reverse-engineer [competitor]'s paid funnel"
- "How is [competitor] positioning themselves in ads?"
- "Deep competitive ad analysis on [competitor]"

## Phase 0: Intake

1. **Competitor name + domain** — Who are we tearing down?
2. **Your product** — For comparison framing
3. **Channels** — Meta, Google, or both? (default: both)
4. **Depth level:**
   - **Standard:** Ad scrape + landing page analysis
   - **Deep:** Standard + historical comparison + funnel reconstruction
5. **Known competitor landing pages?** — Any URLs you've seen in their ads

## Phase 1: Ad Collection

### 1A: Meta Ad Library Scrape

```bash
python3 skills/meta-ad-scraper/scripts/scrape_meta_ads.py \
  --domain <competitor_domain> \
  --output json
```

For each ad, capture:
- Ad copy (headline + primary text)
- Visual type (image / video / carousel)
- CTA button
- Landing page URL
- Active duration (first seen → still running or stopped)
- Platforms (Facebook, Instagram, Audience Network)
- Ad variations (A/B tests — same landing page, different creative)

### 1B: Google Ads Transparency Scrape

```bash
python3 skills/google-ad-scraper/scripts/scrape_google_ads.py \
  --domain <competitor_domain> \
  --output json
```

For each ad:
- Headline variants
- Description lines
- Ad type (Search / Display / YouTube / Shopping)
- Landing page URL (from display URL)
- Geographic targeting (if visible)

## Phase 2: Landing Page Analysis

For each unique landing page URL found in ads:

```
Fetch: [landing_page_url]
```

Extract:
- **Hero headline** — Does it match the ad promise?
- **Subheadline** — Value prop expansion
- **Primary CTA** — What action are they driving? (Demo / Free trial / Sign up / Download)
- **Social proof** — Logos, testimonials, case study metrics
- **Pricing visibility** — Is pricing shown or hidden?
- **Form fields** — How much info do they ask for?
- **Page type** — General homepage / dedicated LP / feature page / use-case page
- **Message match score** — How well does the LP deliver on the ad's promise? (1-10)

## Phase 3: Strategic Analysis

### 3A: Campaign Clustering

Group all ads into logical campaigns by:
- **Landing page destination** — Ads pointing to the same URL = same campaign
- **Messaging theme** — Similar copy angles = same strategic bet
- **Audience signal** — Different copy for different personas

### 3B: Per-Campaign Analysis

For each campaign cluster:

| Dimension | Analysis |
|-----------|----------|
| **Strategic intent** | What is this campaign trying to achieve? (Awareness / Lead gen / Free trial / Competitive displacement) |
| **Target persona** | Who is this ad speaking to? (Role, pain, stage) |
| **Positioning bet** | What market position are they claiming? |
| **Hook strategy** | Fear / Outcome / Social proof / Contrarian / Product-led |
| **Conversion path** | Ad → LP → CTA → [Demo call / Free trial / Content download] |
| **Longevity signal** | How long has this been running? (Longer = likely working) |
| **A/B tests detected** | Multiple creatives to same LP = active testing |

### 3C: Budget Allocation Inference

Based on ad volume and platform distribution, estimate where they're concentrating spend:

| Platform | Ad Count | % of Total | Estimated Focus |
|----------|----------|-----------|-----------------|
| Meta (Facebook) | [N] | [X%] | [Awareness / Retargeting] |
| Meta (Instagram) | [N] | [X%] | [Visual / younger audience] |
| Google Search | [N] | [X%] | [Bottom-funnel capture] |
| Google Display | [N] | [X%] | [Awareness / retargeting] |
| YouTube | [N] | [X%] | [Education / awareness] |

### 3D: Historical Comparison (Deep Mode)

If Web Archive data exists for their landing pages:
- Has their positioning changed in the last 6-12 months?
- What campaigns did they retire? (Possible losers)
- What campaigns have they scaled up? (Possible winners)

### 3E: Vulnerability Analysis

Identify weaknesses in their ad strategy:

| Vulnerability Type | Description |
|-------------------|-------------|
| **Message-LP mismatch** | Ad promises one thing, LP delivers another |
| **Single-persona dependency** | All ads target the same persona — missing segments |
| **Platform concentration** | Heavy on one platform, absent from others |
| **No social proof** | Ads or LPs lack credibility markers |
| **Weak CTA** | Asking for too much too soon (demo before value) |
| **Generic positioning** | Claims anyone could make — not differentiated |
| **Stale creative** | Same ads running unchanged for months — fatigue risk |

## Phase 4: Output Format

```markdown
# Competitor Ad Teardown: [Competitor Name] — [DATE]

Domain: [competitor.com]
Channels analyzed: [Meta, Google]
Total ads found: [N] (Meta: [N], Google: [N])
Unique landing pages: [N]
Estimated active campaigns: [N]

---

## Executive Summary

[3-5 sentence summary: What is this competitor doing with paid ads? What's working? Where are they vulnerable?]

---

## Campaign Breakdown

### Campaign 1: [Inferred Campaign Name]
- **Ads in cluster:** [N]
- **Platform(s):** [Meta / Google / Both]
- **Strategic intent:** [Awareness / Lead gen / Competitive displacement / etc.]
- **Target persona:** [Description]
- **Hook strategy:** [Type]
- **Landing page:** [URL]
  - Hero: "[Headline text]"
  - CTA: "[Button text]"
  - Message match: [Score/10]
- **Longevity:** [First seen date → status]
- **A/B tests detected:** [Yes/No — what they're testing]

**Sample ad:**
> **Headline:** [text]
> **Body:** [text]
> **CTA:** [button]
> **Format:** [Image/Video/Carousel]

**Assessment:** [1-2 sentences — is this working? Why/why not?]

### Campaign 2: ...

---

## Funnel Map

```
[Ad: Hook/Angle] → [LP: /landing-page-url] → [CTA: Book Demo]
                                               ↓
[Ad: Different angle] → [LP: /same-or-different] → [CTA: Free Trial]
```

---

## Budget Allocation Estimate

| Platform | Share | Focus Area |
|----------|-------|-----------|
| [Platform] | [X%] | [Intent] |

---

## What's Working (Long-Running Ads)

| Ad | Platform | Running Since | Why It Likely Works |
|----|----------|--------------|-------------------|
| [Headline excerpt] | [Platform] | [Date] | [Analysis] |

---

## Vulnerability Report

### 1. [Vulnerability]
**Evidence:** [What we observed]
**Your opportunity:** [How to exploit this gap]

### 2. ...

---

## Recommended Counter-Plays

### Counter-Play 1: [Name]
- **Target their weakness:** [Which vulnerability]
- **Your ad angle:** [Hook]
- **Platform:** [Where to run]
- **LP strategy:** [What your landing page should emphasize]

### Counter-Play 2: ...
```

Save to `clients/<client-name>/ads/competitor-teardown-[competitor]-[YYYY-MM-DD].md`.

## Cost

| Component | Cost |
|-----------|------|
| Meta ad scraper | ~$0.20-0.50 (Apify) |
| Google ad scraper | ~$0.20-0.50 (Apify) |
| Landing page fetching | Free |
| Web Archive lookup (deep mode) | Free |
| Analysis | Free (LLM reasoning) |
| **Total** | **~$0.40-1.00** |

## Tools Required

- **Apify API token** — `APIFY_API_TOKEN` env var
- **Upstream skills:** `meta-ad-scraper`, `google-ad-scraper`
- **fetch_webpage** — for landing page analysis

## Trigger Phrases

- "Tear down [competitor]'s ads"
- "What's [competitor] running on Meta/Google?"
- "Reverse-engineer [competitor]'s paid funnel"
- "Deep ad analysis on [competitor]"
- "Find weaknesses in [competitor]'s ad strategy"
