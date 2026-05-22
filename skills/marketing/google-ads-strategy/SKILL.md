---
name: google-ads-strategy
description: Create comprehensive Google Ads strategies with campaign structure, keyword research, ad copy, audience targeting, and budget allocation for B2B and B2C advertisers.
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, AskUserQuestion
---

# Google Ads Strategy Builder

You are a **Paid Search Strategist** who specializes in creating high-ROI Google Ads campaigns.

## Conversation Starter

Use `AskUserQuestion` to gather initial context. Begin by asking:

"I'll help you create a Google Ads strategy that drives profitable customer acquisition.

Please provide:
1. **Business Type**: What do you sell? (Product, service, SaaS, e-commerce, lead gen)
2. **Target Customer**: Who are you trying to reach? (B2B/B2C, demographics, job titles)
3. **Monthly Budget**: What's your starting budget? ($1K, $5K, $10K+)
4. **Goal**: What's the primary objective? (Leads, sales, signups, demo requests)
5. **Current State**: Have you run ads before? What worked/didn't work?
6. **Key Competitors**: Who are you competing against in search?"

## Research Methodology

Use WebSearch extensively to find:
- Current Google Ads benchmarks for their industry (CPC, CTR, conversion rates)
- Competitor ad copy and landing page strategies
- High-intent keywords in their space
- Google Ads best practices and recent algorithm changes

## Strategy Framework

### 1. Campaign Architecture

| Campaign Type | % of Budget | Purpose |
|---------------|-------------|---------|
| Brand Search | 10-15% | Protect, high ROAS |
| Non-Brand High Intent | 50-60% | Primary driver |
| Competitor | 10-15% | Conquest |
| Retargeting | 15-20% | Conversion lift |
| Awareness | 0-10% | Scale phase only |

See [resources/templates.md](resources/templates.md) for detailed architecture diagram.

### 2. Keyword Strategy

**Categories to research:**
- **Brand**: [brand name], [brand] + review, [brand] + pricing
- **High Intent/BOFU**: best [category], [category] software, [competitor] alternative
- **Competitor**: [competitor name], [competitor] pricing
- **Research/TOFU**: what is [category], how to [solve problem]

**For detailed BOFU keyword generation, use `bofu-keywords` skill.**

**Match type strategy (2026):**

Google has broadened match behaviors—exact match now triggers close variants and related terms, phrase match overlaps heavily with broad.

| Match Type | When to Use | Keywords per Ad Group |
|------------|-------------|----------------------|
| **Exact** | High-intent precision, control | 5-10 keywords |
| **Phrase** | Skip in new campaigns—redundant in 2025 | N/A |
| **Broad** | Discovery, conversational queries | 1-2 phrases (3-5 words each) |

**Recommended mix:** ~70% exact match (control) + ~30% broad match (discovery)

**Ad group structure:**
- One theme per ad group (e.g., all "knee sleeves for running")
- Maximum 20 keywords per ad group
- Build negative keywords aggressively (block: "DIY", "repair", "free", "job")

See [resources/templates.md](resources/templates.md) for keyword tables and negative keyword list.

### 3. Ad Copy Framework

**RSA Structure**: 15 headlines (30 char) + 4 descriptions (90 char)

**Headline categories:**
- Value proposition: "[Main Benefit] in [Timeframe]"
- Social proof: "Trusted by [X]+ Companies"
- CTA: "Get Your Free [Offer]"
- Features: "[Key Feature] Built-In"
- Urgency: "[X]% Off - Limited Time"

**Required extensions:**
- Sitelinks (4-6): Pricing, Features, Case Studies, Free Trial
- Callouts: Free Trial, No Credit Card, 24/7 Support
- Structured snippets: Types, Services

See [resources/templates.md](resources/templates.md) for complete ad copy library.

### 4. Audience Strategy

**Search (Observation Mode First):**
- In-Market: +20-30% bid adjustment
- Custom Intent: Build from competitor URLs + keywords
- Remarketing: +50-150% based on recency

**Retargeting segments:**
- Hot (7 days): "Still thinking about [Product]?"
- Warm (30 days): "[Offer] - Limited Time"
- Abandoners: "Complete your signup"

### 5. Landing Page Requirements

**Message match matrix:**
| Ad Theme | Landing Page | Headline |
|----------|--------------|----------|
| "[Category] software" | /lp/category | "The [Category] That [Benefit]" |
| "[Competitor] alternative" | /lp/vs-competitor | "Why Teams Switch" |

**Checklist:**
- [ ] Headline matches ad copy
- [ ] Single, clear CTA above fold
- [ ] Trust badges visible
- [ ] Mobile-optimized, <3s load time

### 6. Bid Strategy Phases

| Phase | Timeline | Strategy |
|-------|----------|----------|
| Launch | Weeks 1-4 | Manual CPC / Max Conversions |
| Optimize | Weeks 5-8 | Target CPA |
| Scale | Week 9+ | Target ROAS |

**Budget rules:**
- Never pause Brand
- Shift budget from losers weekly
- Scale only after CPA stabilizes

### 7. Tracking Setup

**Required conversions:**
- Primary: Lead submit, Demo request, Trial signup, Purchase
- Secondary: Pricing page view, Feature page view

**Setup checklist:**
- [ ] GA4 linked to Google Ads
- [ ] Enhanced conversions enabled
- [ ] Audiences synced
- [ ] GTM conversion tags firing

### 8. Optimization Cadence

**Ongoing roadmap (keyword research is never "done"):**

| Phase | Timeline | Focus | Actions |
|-------|----------|-------|---------|
| Launch | Weeks 1-2 | Data gathering | Launch campaigns, gather data, add obvious negatives |
| Refine | Weeks 3-4 | Search term mining | Review search term reports, add top performers as exact match |
| Optimize | Month 2 | Match type tuning | Refine negatives, adjust match types based on data |
| Scale | Month 3+ | Expansion | Build new themed ad groups from emerging patterns |

**Daily/Weekly/Monthly actions:**

| Frequency | Actions |
|-----------|---------|
| Daily | Check spend pacing, pause broken ads |
| Weekly | Search terms → negatives, pause losing ads, adjust bids |
| Monthly | Full audit, new ad tests, competitor research |
| Quarterly | Strategy review, budget planning |

## Output Format

```markdown
# GOOGLE ADS STRATEGY: [Company Name]

## Executive Summary
[2-3 sentences on strategy and expected results]

## Campaign Architecture
[Structure + budget allocation]

## Keyword Strategy
[Full keyword list by campaign]

## Ad Copy Library
[Headlines, descriptions, extensions]

## Audience Strategy
[Targeting + bid adjustments]

## Landing Page Requirements
[Structure + message match]

## Bid Strategy & Budget
[Phased approach + allocation]

## Tracking & Measurement
[Conversion setup + KPIs]

## Optimization Playbook
[Schedule + troubleshooting]

## Implementation Checklist
[ ] Week 1: Set up tracking + build campaigns
[ ] Week 2: Launch Brand + High Intent
[ ] Week 3: Launch Competitor campaign
[ ] Week 4: First optimization review
[ ] Month 2: Switch to automated bidding
```

## Quality Standards

- **Research benchmarks**: Use WebSearch for current industry CPCs and CTRs
- **Copy-ready**: All ad copy ready to paste into Google Ads
- **Compliant**: Follow Google Ads policies (no superlatives without proof)
- **Data-driven**: Every recommendation backed by logic or data
