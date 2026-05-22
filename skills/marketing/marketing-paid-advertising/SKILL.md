---
name: marketing-paid-advertising
description: Paid advertising strategy for Google, Meta, TikTok, LinkedIn - campaign structure, bidding, audiences, creative, measurement, and budget allocation.
---

# PAID ADVERTISING — CAMPAIGN OS (OPERATIONAL)

Built as a **no-fluff execution skill** for paid acquisition across Google, Meta, TikTok, and LinkedIn.

**Structure**: Core paid advertising fundamentals first. Platform-specific tactics in dedicated sections. AI automation in clearly labeled "Optional: AI / Automation" sections.

---

## Modern Best Practices (January 2026)

- Google Ads: https://support.google.com/google-ads/
- Meta Business Help: https://www.facebook.com/business/help
- TikTok Ads Manager: https://ads.tiktok.com/help/
- LinkedIn Campaign Manager: https://business.linkedin.com/marketing-solutions

---

## When to Use This Skill

- **New campaigns**: Structure, audiences, bidding, creative strategy
- **Scaling spend**: Budget allocation, ROAS targets, diminishing returns
- **Platform selection**: Which channels for which goals
- **Creative strategy**: Ad formats, hooks, testing frameworks
- **Measurement**: Attribution, incrementality, cross-platform tracking

---

## Core: Platform Selection Matrix

| Platform | Best For | Avg CPL (B2B) | Avg CPL (B2C) | Targeting Strength |
|----------|----------|---------------|---------------|-------------------|
| **Google Search** | High intent, ready-to-buy | $30-80 | $15-40 | Intent-based |
| **Google Display** | Awareness, retargeting | $10-30 | $5-15 | Contextual |
| **Meta (FB/IG)** | B2C, visual products, awareness | $20-60 | $5-25 | Interest/behavior |
| **LinkedIn** | B2B, enterprise, high ACV | $50-150 | N/A | Professional |
| **TikTok** | Gen Z/Millennial, viral potential | $15-40 | $3-15 | Interest/behavior |
| **YouTube** | Education, demos, brand | $20-50 | $8-20 | Intent + interest |

### Platform Selection Decision Tree

```text
HIGH INTENT (ready to buy)?
├─ YES → Google Search (always include)
│        └─ Add branded terms + competitor terms
└─ NO → What's your goal?
         ├─ Awareness/Brand → Meta, TikTok, YouTube
         ├─ B2B/Enterprise → LinkedIn, Google Search
         ├─ E-commerce → Meta, Google Shopping, TikTok
         └─ App installs → Meta, TikTok, Google UAC
```

---

## Core: Campaign Structure Framework

### Google Ads Structure

```text
ACCOUNT
├─ Campaign 1: Brand (Search)
│   ├─ Ad Group: Exact brand terms
│   └─ Ad Group: Brand + product
│
├─ Campaign 2: Non-Brand (Search)
│   ├─ Ad Group: Pain/problem keywords
│   ├─ Ad Group: Solution keywords
│   └─ Ad Group: Competitor keywords
│
├─ Campaign 3: Retargeting (Display)
│   ├─ Ad Group: Site visitors (7d)
│   ├─ Ad Group: Site visitors (30d)
│   └─ Ad Group: Cart abandoners
│
└─ Campaign 4: Performance Max (if applicable)
    └─ Asset group by product/service line
```

### Meta Ads Structure

```text
ACCOUNT
├─ Campaign 1: Prospecting (Conversions)
│   ├─ Ad Set: Lookalike 1% (customers)
│   ├─ Ad Set: Interest targeting
│   └─ Ad Set: Broad targeting (Advantage+)
│
├─ Campaign 2: Retargeting (Conversions)
│   ├─ Ad Set: Website visitors (7d)
│   ├─ Ad Set: Engaged (video/page 30d)
│   └─ Ad Set: Cart abandoners
│
└─ Campaign 3: Testing (CBO or ABO)
    ├─ Ad Set: Creative test A
    ├─ Ad Set: Creative test B
    └─ Ad Set: Creative test C
```

---

## Core: Bidding Strategy Guide

| Strategy | When to Use | Risk Level | Best For |
|----------|-------------|------------|----------|
| **Manual CPC** | New campaigns, learning | Low | Control freaks, testing |
| **Target CPA** | Stable conversion history | Medium | Lead gen, consistent volume |
| **Target ROAS** | E-commerce, known value | Medium | Revenue optimization |
| **Maximize Conversions** | Volume priority | High | Scale quickly, less control |
| **Maximize Clicks** | Traffic/awareness | Low | Brand campaigns |

### Bidding Decision Tree

```text
CONVERSION HISTORY?
├─ <50 conversions/month → Manual CPC or Max Clicks
├─ 50-100 conversions → Target CPA (start conservative)
└─ >100 conversions → Target CPA/ROAS (optimize for efficiency)

BUDGET CONSTRAINED?
├─ YES → Manual CPC or Target CPA (strict)
└─ NO → Maximize Conversions (let algorithm spend)
```

### Do (Bidding)

- Start with manual/conservative bids to gather data
- Set realistic CPA/ROAS targets based on unit economics
- Allow 2-4 weeks for learning phase before judging
- Use bid adjustments for device, location, time

### Avoid (Bidding)

- Changing bids daily (resets learning)
- Setting unrealistic CPA targets (algorithm won't spend)
- Using ROAS bidding without accurate conversion values
- Ignoring seasonality effects on performance

---

## Core: Audience Strategy

### Google Audiences

| Audience Type | Description | Use Case |
|---------------|-------------|----------|
| **In-Market** | Actively researching/buying | Prospecting |
| **Affinity** | Long-term interests | Awareness |
| **Custom Intent** | Your keywords, competitor URLs | Prospecting |
| **Remarketing** | Your site visitors | Retargeting |
| **Customer Match** | Email list upload | Lookalikes, exclusion |
| **Similar** | Lookalikes of your lists | Prospecting |

### Meta Audiences

| Audience Type | Description | Best Practice |
|---------------|-------------|---------------|
| **Lookalike 1%** | Most similar to source | Highest quality |
| **Lookalike 1-3%** | Moderate similarity | Volume + quality |
| **Interest** | Based on behavior/pages | Test broadly |
| **Custom** | Site visitors, engagers | Retargeting |
| **Advantage+** | AI-optimized broad | Let Meta find |

### Audience Strategy Framework

```text
FUNNEL STAGE
├─ Top (Awareness)
│   ├─ Google: In-Market, Affinity, Display
│   ├─ Meta: Broad, Interest, Lookalike 1-5%
│   └─ TikTok: Interest, Hashtag
│
├─ Middle (Consideration)
│   ├─ Google: Custom Intent, Search
│   ├─ Meta: Lookalike 1-2%, Engaged visitors
│   └─ TikTok: Custom audiences, Retargeting
│
└─ Bottom (Decision)
    ├─ Google: Brand Search, RLSA
    ├─ Meta: Retargeting 7-14d, Cart abandoners
    └─ All: Email list retargeting
```

---

## Core: Creative Strategy

### Ad Format Selection

| Format | Platform | Best For | CPM Range |
|--------|----------|----------|-----------|
| **Responsive Search** | Google | High intent | $1-5 |
| **Image (static)** | Meta, Display | Simple message | $3-10 |
| **Carousel** | Meta, LinkedIn | Multiple products/features | $5-12 |
| **Video (15-30s)** | All | Engagement, brand | $8-20 |
| **UGC-style** | Meta, TikTok | Authenticity | $5-15 |
| **Document** | LinkedIn | B2B thought leadership | $10-25 |

### Creative Testing Framework

**Test ONE variable at a time:**

```text
Week 1-2: Hook Test
├─ Creative A: Pain hook ("Tired of...")
├─ Creative B: Result hook ("Get X in Y days")
└─ Creative C: Social proof hook ("Join 10,000+")

Week 3-4: Format Test (winner hook)
├─ Creative A: Static image
├─ Creative B: Video (15s)
└─ Creative C: Carousel

Week 5-6: CTA Test (winner format)
├─ Creative A: "Start Free Trial"
├─ Creative B: "Book a Demo"
└─ Creative C: "See Pricing"
```

### Creative Best Practices by Platform

**Google Search:**
- Include keywords in headlines
- Use all 15 headlines, 4 descriptions
- Pin important messages to positions 1-2
- Include numbers, urgency, benefits

**Meta:**
- First 3 seconds = hook (video)
- Native/UGC style outperforms polished
- 1:1 for feed, 9:16 for stories/reels
- Text: <125 chars primary, 40 headline

**TikTok:**
- Native TikTok aesthetic (not ads)
- Hook in first 1 second
- Creator/UGC content performs best
- Trending sounds can boost reach

**LinkedIn:**
- Professional tone, specific value
- Document ads for thought leadership
- Video: talking head with captions
- Longer copy acceptable (pain + solution)

---

## Core: Budget Allocation Framework

### Budget by Funnel Stage

| Stage | % of Budget | Goal |
|-------|-------------|------|
| **Brand** | 10-20% | Protect brand terms, low CPL |
| **Prospecting** | 40-60% | New customer acquisition |
| **Retargeting** | 20-30% | Convert warm audiences |
| **Testing** | 10-15% | New creative/audience tests |

### Budget Allocation by Platform

**Starter Budget ($5-10k/month):**
```text
Google Search (brand + non-brand): 60%
Meta (prospecting + retargeting): 30%
Testing budget: 10%
```

**Growth Budget ($10-50k/month):**
```text
Google Search: 40%
Meta: 35%
TikTok or LinkedIn: 15%
Testing: 10%
```

**Scale Budget ($50k+/month):**
```text
Google (Search + PMax + YouTube): 35%
Meta: 30%
TikTok: 15%
LinkedIn (if B2B): 10%
Testing: 10%
```

### Diminishing Returns Detection

| Signal | What It Means | Action |
|--------|---------------|--------|
| CPL increasing >20% | Audience saturation | Expand audiences, add channels |
| Frequency >3 (Meta) | Ad fatigue | New creative, expand audience |
| Impression share <80% | Budget limited | Increase budget or narrow targeting |
| CTR declining | Creative fatigue | Test new hooks, formats |

---

## Quick Reference

| Task | Template | Location |
|------|----------|----------|
| Campaign setup | Campaign structure template | `templates/campaign-structure.md` |
| Budget planning | Budget allocation worksheet | `templates/budget-allocation.md` |
| Creative brief | Ad creative brief | `templates/creative-brief.md` |
| A/B testing | Creative test plan | `templates/creative-test-plan.md` |
| Performance review | Weekly/monthly review | `templates/performance-review.md` |

---

## Decision Tree (Campaign Triage)

```text
CPL too high?
├─ Check audience size → Too narrow = expand; too broad = tighten
├─ Check creative CTR → Below 1% = new creative needed
├─ Check landing page CVR → Below 2% = landing page issue (see marketing-cro)
└─ Check bid strategy → May need to increase bids or change strategy

ROAS below target?
├─ Check conversion tracking → Missing conversions = attribution issue
├─ Check audience quality → Low quality = tighten targeting
├─ Check offer → Weak offer = test new value prop
└─ Check funnel → Leaky funnel = fix downstream conversion

Volume too low?
├─ Check budget → Daily budget limiting impressions
├─ Check bid → Bids too low to win auctions
├─ Check audience → Audience too narrow
└─ Check creative → Low relevance score/quality score
```

---

## Operational SOPs

### Campaign Launch SOP

1. **Pre-launch (Day -7 to -1)**
   - Define KPIs: CPL target, ROAS target, volume goals
   - Build audiences: custom, lookalike, remarketing
   - Create campaign structure per framework
   - Upload creative assets (3-5 variants minimum)
   - Set up conversion tracking and verify
   - Configure UTM parameters

2. **Launch (Day 0)**
   - Start with conservative bids (20% below target CPA)
   - Enable all ad sets/ad groups
   - Set daily budget caps
   - Document baseline metrics

3. **Learning Phase (Day 1-14)**
   - DO NOT make major changes
   - Monitor for errors only (disapprovals, tracking issues)
   - Document performance daily

4. **Optimization (Day 14+)**
   - Pause underperformers (>2x CPA target)
   - Increase budget on winners (+20% increments)
   - Launch creative tests
   - Expand audiences gradually

### Weekly Review SOP

**Monday (30 minutes):**
- Pull weekly metrics: spend, CPL, ROAS, conversions
- Compare to targets and previous week
- Identify top 3 actions for the week

**Thursday (15 minutes):**
- Mid-week check on pacing
- Pause any disasters (>3x CPA)
- Note creative fatigue signals

### Monthly Review SOP

1. **Performance Summary**
   - Spend vs budget
   - CPL/CPA by campaign, platform
   - ROAS by campaign, platform
   - Conversion volume and quality

2. **Audience Insights**
   - Best performing audiences
   - Audiences to exclude
   - New audience opportunities

3. **Creative Insights**
   - Top performing creatives
   - Fatigue indicators
   - Next month's test plan

4. **Budget Reallocation**
   - Shift budget from losers to winners
   - Adjust platform mix based on results
   - Plan next month's tests

---

## Metrics & KPIs

### Primary Metrics

| Metric | Definition | Target Range |
|--------|------------|--------------|
| **CPL** | Cost per lead | Industry dependent |
| **CPA** | Cost per acquisition | < LTV/3 |
| **ROAS** | Revenue / Ad spend | > 3:1 for e-com |
| **CAC** | Full acquisition cost | < LTV/3 |

### Secondary Metrics

| Metric | Definition | Watch For |
|--------|------------|-----------|
| **CTR** | Clicks / Impressions | <1% = creative issue |
| **CVR** | Conversions / Clicks | <2% = landing issue |
| **Frequency** | Avg impressions/user | >3 = fatigue |
| **Quality Score** | Google relevance | <6 = improve relevance |
| **Relevance Score** | Meta relevance | <5 = improve relevance |

---

## Platform-Specific Guides

### Google Ads Specifics

See [resources/google-ads-guide.md](resources/google-ads-guide.md)

### Meta Ads Specifics

See [resources/meta-ads-guide.md](resources/meta-ads-guide.md)

### TikTok Ads Specifics

See [resources/tiktok-ads-guide.md](resources/tiktok-ads-guide.md)

### LinkedIn Ads Specifics

See [resources/linkedin-ads-guide.md](resources/linkedin-ads-guide.md)

---

## Templates

| Template | Purpose |
|----------|---------|
| [campaign-structure.md](templates/campaign-structure.md) | Campaign hierarchy template |
| [budget-allocation.md](templates/budget-allocation.md) | Budget planning worksheet |
| [creative-brief.md](templates/creative-brief.md) | Ad creative specification |
| [creative-test-plan.md](templates/creative-test-plan.md) | A/B testing framework |
| [performance-review.md](templates/performance-review.md) | Weekly/monthly review template |

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Changing bids daily** | Resets algorithm learning | Wait 2-4 weeks |
| **Too many audiences** | Splits budget, no learnings | 3-5 audiences max |
| **Single creative** | No testing, quick fatigue | 3-5 variants minimum |
| **No negative keywords** | Wasted spend on irrelevant | Build negatives weekly |
| **Ignoring Quality Score** | Higher CPCs, lower reach | Improve relevance |
| **Platform FOMO** | Spreading too thin | Master 1-2 platforms first |
| **No exclusions** | Showing to existing customers | Exclude converters |

---

## Optional: AI / Automation

> **Note**: Core paid advertising fundamentals above work without AI. This section covers optional automation capabilities.

### AI-Powered Features

| Feature | Platform | Use Case |
|---------|----------|----------|
| **Performance Max** | Google | Full-funnel automation |
| **Advantage+** | Meta | Automated targeting |
| **Smart Campaigns** | TikTok | Automated optimization |
| **Value-Based Bidding** | All | Bid on predicted LTV |

### When to Use AI Features

```text
HAVE 100+ conversions/month?
├─ YES → Consider Performance Max, Advantage+
└─ NO → Stick to manual campaigns for control

CLEAR CONVERSION VALUES?
├─ YES → Value-based bidding can optimize for revenue
└─ NO → Use CPA bidding instead
```

---

## Related Skills

- [marketing-leads-generation](../marketing-leads-generation/SKILL.md) — Lead capture and nurture
- [marketing-cro](../marketing-cro/SKILL.md) — Landing page optimization
- [marketing-content-strategy](../marketing-content-strategy/SKILL.md) — Content for ads
- [startup-go-to-market](../startup-go-to-market/SKILL.md) — Channel strategy

---

## Usage Notes (Claude)

- Stay operational: return campaign structures, budgets, creative specs
- Include platform-specific requirements (sizes, specs, limits)
- Always recommend starting conservative and scaling
- Cite current platform documentation when possible
- Do not invent benchmark data; use ranges or state "varies by industry"
