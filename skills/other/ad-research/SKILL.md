---
name: ad-research
description: Research competitor ads using Meta Ad Library, Google Ads Transparency Center, and TikTok Creative Center. Analyze creative patterns, hooks, offers, and landing pages.
---

# /ad-research — The Competitive Intelligence Analyst

Research what your competitors (or industry leaders) are running for ads. Scrapes Meta Ad Library, Google Ads Transparency Center, and TikTok Creative Center. Analyzes creative patterns, hooks, offers, and landing page strategies.

## Arguments

Required:
- **competitor**: Company name, domain, or Facebook Page name
- **platform**: meta | google | tiktok | all

Optional:
- **--industry**: Industry vertical for broader research (e.g., "legal services", "SaaS", "ecommerce")
- **--count**: Number of ads to analyze (default: 10)

Example: `/ad-research "Smith & Associates Law" meta`
Example: `/ad-research kaicalls.com all`
Example: `/ad-research --industry "AI SaaS" meta --count 20`

## The Skill

### Step 1: Identify Ad Library URLs

Map the competitor to the correct ad library:

**Meta Ad Library:**
- URL: `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&q={competitor}`
- Shows: All active ads for a page, including creatives, text, and launch dates
- Access: Public, no login required

**Google Ads Transparency Center:**
- URL: `https://adstransparency.google.com/?search={competitor}`
- Shows: All ads run by an advertiser, including text/display/video
- Access: Public, no login required

**TikTok Creative Center:**
- URL: `https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/en`
- Shows: Top-performing ads by industry, filterable by region/period
- Access: Public, no login required

### Step 2: Gather Ad Data

If `/browse` is available (gstack installed), use the browser to scrape:

```
$B navigate "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&q={competitor}"
$B snapshot -i
```

Extract from each ad:
- **Ad text** (primary text, headline, description)
- **Creative type** (image, video, carousel)
- **CTA button** text
- **Launch date** (how long has this ad been running? Long-running = likely profitable)
- **Platform** (Facebook, Instagram, Messenger, Audience Network)

If `/browse` is NOT available:
Tell user the URLs to visit manually, and offer to analyze screenshots or pasted ad text.

### Step 3: Analyze Creative Patterns

For each ad collected, classify:

```
AD ANALYSIS MATRIX
═══════════════════════════════════════

Competitor: {name}
Platform:   {platform}
Ads found:  {N} active

CREATIVE PATTERNS:
┌──────────────────┬──────┬────────────────────────────┐
│ Pattern          │ Count│ Examples                    │
├──────────────────┼──────┼────────────────────────────┤
│ Hook type        │      │                            │
│   Pain point     │  4   │ "Tired of missed calls?"   │
│   Social proof   │  3   │ "500+ firms trust us"      │
│   Data/stat      │  2   │ "0.4s average answer time" │
│   Question       │  1   │ "What if you never..."     │
├──────────────────┼──────┼────────────────────────────┤
│ Offer type       │      │                            │
│   Free trial     │  5   │ "14-day free trial"        │
│   Demo           │  3   │ "Book a demo"              │
│   Discount       │  2   │ "50% off first month"      │
├──────────────────┼──────┼────────────────────────────┤
│ Creative format  │      │                            │
│   UGC video      │  4   │ Testimonial-style          │
│   Product demo   │  3   │ Screen recording           │
│   Static image   │  2   │ Bold text + product shot   │
│   Carousel       │  1   │ Feature breakdown          │
├──────────────────┼──────┼────────────────────────────┤
│ CTA              │      │                            │
│   Learn More     │  4   │                            │
│   Sign Up        │  3   │                            │
│   Get Started    │  2   │                            │
│   Book Now       │  1   │                            │
└──────────────────┴──────┴────────────────────────────┘
```

### Step 4: Longevity Analysis

Ads that have been running for 30+ days are likely profitable. Flag them:

```
LONG-RUNNING ADS (likely profitable):
  1. [62 days] "Stop losing clients to voicemail" — UGC video, Free trial CTA
  2. [45 days] "Law firms save 12 hours/week" — Data-led, Demo CTA
  3. [38 days] "What if every call was answered?" — Question hook, Learn More

RECENTLY LAUNCHED (testing phase):
  4. [3 days] "New: AI legal receptionist" — Product announcement
  5. [1 day] "Limited offer: 60% off" — Discount test
```

### Step 5: Strategic Recommendations

Based on the analysis, recommend:

```
RECOMMENDATIONS:
═══════════════

1. HOOKS TO STEAL (adapted, not copied):
   - Pain point hooks dominate (4/10 ads) — their audience responds to loss aversion
   - Adapt: "{Your version of their most common hook}"

2. CREATIVE FORMAT TO TEST:
   - UGC video is their strongest format (4/10, longest running)
   - You should test: testimonial-style UGC showing your product in use

3. OFFER GAP:
   - They're not running any comparison or "vs" content
   - Opportunity: "{Your product} vs {competitor}" comparison ad

4. MESSAGING THEY'RE AVOIDING:
   - No price transparency in any ad (all push to demo/trial)
   - Potential differentiator: transparent pricing in ad copy

5. LANDING PAGE PATTERNS:
   - {N} ads point to dedicated landing pages (not homepage)
   - {N} use social proof above the fold
   - {N} have video on the landing page
```

### Step 6: Generate Counter-Ads

Offer to generate ad copy that counters their positioning:

"Want me to generate ad copy that exploits these gaps? Run `/ad-copy {platform} {site} \"{angle based on gap}\"` with these insights baked in."

## Ad Library Quick Reference

| Library | URL | What You Can See | Limitations |
|---------|-----|-----------------|-------------|
| Meta Ad Library | facebook.com/ads/library | All active ads, creative, text, dates, platforms, spend ranges | No performance data (no CTR, no conversions) |
| Google Transparency | adstransparency.google.com | Search/display/video ads by advertiser | No performance data, limited to verified advertisers |
| TikTok Creative Center | ads.tiktok.com/business/creativecenter | Top-performing ads by industry | Industry-level, not competitor-specific |
| LinkedIn Ad Library | linkedin.com/ad-library | Ads by company or keyword | Limited search, no creative download |
| Twitter/X Ad Transparency | twitter.com/transparency | Political ads only | Very limited for commercial ads |

## Error Handling

- **/browse unavailable**: Provide direct URLs for manual research, offer to analyze pasted content
- **Competitor not found**: Suggest alternative search terms (parent company, brand name vs legal name)
- **No active ads**: "No active ads found for {competitor}. They may not be running ads on {platform}, or using a different page/account name."

## Chain State

**Standalone:** Does not require prior chain steps
**Feeds into:** `/ad-copy` (with competitive insights), `/content-ideas` (content gaps from competitor messaging)
