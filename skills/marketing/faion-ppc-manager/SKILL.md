---
name: faion-ppc-manager
description: "PPC advertising: Google, Meta campaigns, optimization, reporting."
user-invocable: false
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# PPC Manager Skill (Claude)

## Overview
This skill orchestrates PPC campaigns. It is used by the `faion-ads-agent` to manage budgets, targeting, ad creatives, and performance analysis for platforms like Google Ads and Meta Ads.

## Context Discovery

### Auto-Investigation

Check these project signals to understand PPC context:

| Signal | Location | What to Look For |
|--------|----------|------------------|
| Ad accounts | Google Ads, Meta Business Suite | Active campaigns, budget, performance metrics |
| Conversion tracking | Analytics, tag manager | Pixel setup, conversion events, attribution |
| Landing pages | Website, ad destinations | Landing page quality, conversion optimization |
| Campaign docs | `.aidocs/`, `docs/ads/` | Campaign structure, targeting strategy, creative briefs |
| Budget | Financial docs, campaign settings | Total ad spend, budget allocation, CAC targets |
| Keywords | Google Ads, keyword research | Target keywords, match types, search terms |
| Audiences | Meta Ads, Google Ads | Custom audiences, lookalikes, retargeting segments |

### Discovery Questions

```yaml
question: "Which ad platform is your priority?"
header: "Ad Platform"
multiSelect: false
options:
  - label: "Google Ads"
    description: "Search, Display, Shopping, Performance Max campaigns"
  - label: "Meta Ads (Facebook/Instagram)"
    description: "Image, Video, Carousel ads with custom audiences"
  - label: "LinkedIn Ads"
    description: "B2B advertising, professional targeting"
  - label: "Multi-platform"
    description: "Cross-platform strategy, budget optimization, attribution"
```

```yaml
question: "What's your PPC maturity level?"
header: "PPC Maturity"
multiSelect: false
options:
  - label: "Starting new campaigns"
    description: "Campaign setup, conversion tracking, initial testing"
  - label: "Have running campaigns"
    description: "Optimization, A/B testing, budget allocation"
  - label: "Scaling campaigns"
    description: "Advanced bidding, retargeting, automation"
  - label: "Multi-platform expert"
    description: "Attribution modeling, cross-platform optimization, scaling"
```

```yaml
question: "What's your primary PPC goal?"
header: "PPC Goal"
multiSelect: false
options:
  - label: "Generate leads"
    description: "Lead gen campaigns, form fills, conversion optimization"
  - label: "Drive sales"
    description: "E-commerce campaigns, ROAS optimization, shopping ads"
  - label: "Build awareness"
    description: "Display campaigns, video ads, reach optimization"
  - label: "Retarget users"
    description: "Retargeting campaigns, abandoned cart, sequential messaging"
```

## Decision Tree

### Quick Reference

| If you need... | Use | File |
|----------------|-----|------|
| **Google Ads** |
| Campaign setup (Search, Display, Shopping, PMax) | Google campaign setup | ads-google-campaign-setup.md |
| Keyword research, match types | Keyword research | ads-google-keywords.md |
| RSA, ad extensions | Google creative | ads-google-creative.md |
| CTR, CPC, ROAS metrics | Google reporting | ads-google-reporting.md |
| **Meta Ads** |
| FB/IG campaign setup | Meta campaign setup | ads-meta-campaign-setup.md |
| Custom/Lookalike audiences | Meta targeting | ads-meta-targeting.md |
| Image, Video, Carousel formats | Meta creative | ads-meta-creative.md |
| CPM, CPA analysis | Meta reporting | ads-meta-reporting.md |
| **B2B/Social** |
| LinkedIn campaigns | LinkedIn ads | ads-linkedin-ads.md |
| Twitter campaigns | Twitter ads | ads-twitter-ads.md |
| **Cross-Platform** |
| Pixel/tag setup | Conversion tracking | ads-conversion-tracking.md |
| Last click, data-driven models | Attribution models | ads-attribution-models.md |
| Ad testing | A/B testing | ads-ab-testing-ads.md |
| Website visitors, cart abandoners | Retargeting | ads-retargeting.md |
| CBO, bid strategies | Budget optimization | ads-budget-optimization.md |
| GA4, Meta Business Suite | Analytics setup | ads-analytics-setup.md |

### Common Workflows

**New Campaign:** conversion-tracking → campaign-setup → creative → ab-testing → reporting
**Optimization:** reporting → budget-optimization → ab-testing → retargeting

## Methodologies
- **google-ads-basics.md**: Google Ads authentication, account structure, campaign management
- **google-ads-optimization.md**: Bidding strategies, conversion tracking, GA4 integration
- **google-ads-reporting.md**: Reporting, automation, error handling, best practices
- **facebook-ads.md**: Managing Facebook advertising campaigns.
- **instagram-ads.md**: Managing Instagram advertising campaigns.
- **meta-audience-targeting.md**: Audience targeting for Facebook & Instagram.
- Files related to ad creatives, targeting, reporting (`ads-*.md`).
- **growth-paid-acquisition.md**: Strategies for growth through paid channels.
