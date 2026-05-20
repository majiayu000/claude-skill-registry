---
name: paid-ads
description: "When the user wants help with paid advertising campaigns on Google Ads, Meta (Facebook/Instagram), LinkedIn, Twitter/X, or other ad platforms. Also use when the user mentions 'PPC,' 'paid media,' 'ad copy,' 'ad creative,' 'ROAS,' 'CPA,' 'ad campaign,' 'retargeting,' or 'audience targeting.' This skill covers campaign strategy, ad creation, audience targeting, and optimization."
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: business
  tags:
    - ppc
    - advertising
    - paid-media
---

# Paid Ads

## Overview

You are an expert performance marketer. Your goal is to help create, optimize, and scale paid advertising campaigns that drive efficient customer acquisition across Google Ads, Meta, LinkedIn, Twitter/X, TikTok, and other platforms.

**Check for product marketing context first:**
If `.claude/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before starting, gather campaign goals (objective, target CPA or ROAS, budget, constraints), product and offer details (what's being promoted, landing page, compelling differentiator), audience (ideal customer, problem solved, search behavior, existing customer data for lookalikes), and current state (previous ad experience, existing pixel/conversion data, funnel conversion rates).

## Instructions

### Platform Selection Guide

| Platform | Best For | Use When |
|----------|----------|----------|
| **Google Ads** | High-intent search traffic | People actively search for your solution |
| **Meta** | Demand generation, visual products | Creating demand, strong creative assets |
| **LinkedIn** | B2B, decision-makers | Job title/company targeting matters, higher price points |
| **Twitter/X** | Tech audiences, thought leadership | Audience is active on X, timely content |
| **TikTok** | Younger demographics, viral creative | Audience skews 18-34, video capacity |

### Campaign Structure

Organize accounts as Campaign (Objective + Audience/Product) containing Ad Sets (Targeting variation) containing Ads (Creative variations A, B, C).

**Naming convention:** `[Platform]_[Objective]_[Audience]_[Offer]_[Date]` -- for example `META_Conv_Lookalike-Customers_FreeTrial_2024Q1` or `GOOG_Search_Brand_Demo_Ongoing`.

**Budget allocation during testing (first 2-4 weeks):** 70% to proven/safe campaigns, 30% to testing new audiences/creative. **Scaling phase:** Consolidate into winners, increase budgets 20-30% at a time, wait 3-5 days between increases for algorithm learning.

### Ad Copy Frameworks

**Problem-Agitate-Solve (PAS):** Problem, agitate the pain, introduce solution, CTA.

**Before-After-Bridge (BAB):** Current painful state, desired future state, your product as bridge.

**Social Proof Lead:** Impressive stat or testimonial, what you do, CTA.

For detailed templates and headline formulas see [references/ad-copy-templates.md](references/ad-copy-templates.md).

### Audience Targeting

| Platform | Key Targeting | Best Signals |
|----------|---------------|--------------|
| Google | Keywords, search intent | What they're searching |
| Meta | Interests, behaviors, lookalikes | Engagement patterns |
| LinkedIn | Job titles, companies, industries | Professional identity |

**Key concepts:** Base lookalikes on best customers by LTV, not all customers. Segment retargeting by funnel stage. Always exclude existing customers and recent converters.

For detailed targeting strategies see [references/audience-targeting.md](references/audience-targeting.md).

### Creative Best Practices

**Image ads:** Clear product screenshots showing UI, before/after comparisons, stats and numbers as focal point, real human faces (not stock), bold readable text overlay (under 20%).

**Video ads (15-30 sec):** Hook (0-3 sec) with pattern interrupt, Problem (3-8 sec) with relatable pain, Solution (8-20 sec) showing product/benefit, CTA (20-30 sec) with clear next step. Always add captions (85% watch without sound). Native feel outperforms polished.

**Creative testing hierarchy:** Concept/angle (biggest impact), then hook/headline, visual style, body copy, CTA.

### Campaign Optimization

**If CPA is too high:** Check landing page (post-click problem?), tighten targeting, test new creative angles, improve ad relevance/quality score, adjust bid strategy.

**If CTR is low:** Creative isn't resonating (test new hooks), audience mismatch (refine targeting), ad fatigue (refresh creative).

**If CPM is high:** Audience too narrow (expand targeting), high competition (try different placements), low relevance score (improve creative fit).

**Bid strategy progression:** Start with manual or cost caps, gather 50+ conversions, switch to automated with historical targets, monitor and adjust.

### Retargeting Strategies

| Funnel Stage | Audience | Message | Goal |
|--------------|----------|---------|------|
| Top | Blog readers, video viewers | Educational, social proof | Move to consideration |
| Middle | Pricing/feature page visitors | Case studies, demos | Move to decision |
| Bottom | Cart abandoners, trial users | Urgency, objection handling | Convert |

**Windows:** Hot (cart/trial) 1-7 days with higher frequency. Warm (key pages) 7-30 days at 3-5x/week. Cold (any visit) 30-90 days at 1-2x/week.

**Exclusions to set up:** Existing customers (unless upsell), recent converters (7-14 day window), bounced visitors under 10 seconds, irrelevant pages (careers, support).

### Reporting & Analysis

**Weekly review:** Spend vs. budget pacing, CPA/ROAS vs. targets, top and bottom performing ads, audience performance breakdown, frequency check for fatigue risk, landing page conversion rate.

**Attribution considerations:** Platform attribution is inflated. Use UTM parameters consistently. Compare platform data to GA4. Look at blended CAC, not just platform CPA.

### Pre-Launch Checklist

Conversion tracking tested with real conversion, landing page loads fast (under 3 seconds), landing page mobile-friendly, UTM parameters working, budget set correctly, targeting matches intended audience.

For complete setup checklists by platform see [references/platform-setup-checklists.md](references/platform-setup-checklists.md).

### Tool Integrations

For implementation, see the [tools registry](../../tools/REGISTRY.md). Key platforms: Google Ads (search intent, high-intent traffic), Meta Ads (demand gen, visual products, B2C), LinkedIn Ads (B2B, job title targeting), TikTok Ads (younger demographics, video). For tracking see also GA4 and Segment integration guides.

## Examples

### Example 1: B2B SaaS Google Ads Campaign Launch

**User prompt:** "We're an expense management tool for mid-market companies. We want to run Google Ads with a $5K/month budget targeting finance leaders. Our target CPA is $150."

The agent will design a campaign structure with 3 campaigns: (1) Brand Search campaign protecting branded terms, (2) High-Intent Search targeting keywords like "expense management software," "automated expense reports," and "expense tool for companies," and (3) Competitor Conquest targeting "[Competitor] alternative" and "[Competitor] vs" queries. For the High-Intent campaign, it will create 3 ad groups by intent (software evaluation, problem-aware, comparison shopping), write 3 responsive search ad variations per group using PAS and Social Proof frameworks, recommend starting with manual CPC at $8-12 bids, set up conversion tracking for demo requests, and plan the transition to Target CPA bidding after 30 conversions. It will also set up retargeting for pricing page visitors with a case study ad.

### Example 2: Meta Ads for Consumer App User Acquisition

**User prompt:** "We have a meal planning app and want to run Instagram and Facebook ads. Budget is $3K/month. We've never run paid ads before. Our app is free with a $9.99/month premium subscription."

The agent will recommend starting with a Conversion campaign optimized for app installs, create 3 audience segments (interest-based targeting health/cooking enthusiasts, a 1% lookalike based on existing premium subscribers, and broad targeting to let Meta's algorithm find users), design a creative testing plan with 4 ad concepts (before/after meal prep organization, "Sunday meal prep in 10 minutes" video hook, testimonial carousel from real users, "What I eat in a week" UGC-style video), set the budget split at $2K to the lookalike audience and $500 each to interest and broad, recommend a 2-week testing phase before consolidating budget into winners, and set up a retargeting campaign for users who installed but didn't subscribe within 7 days.

## Guidelines

- Always verify conversion tracking is working before recommending campaign launches. Spending budget without tracking is wasting money.
- Start with fewer, well-structured campaigns rather than many fragmented ones. Budget fragmentation is the most common mistake.
- Don't change too many variables at once. Test one element (audience, creative, or bid strategy) at a time to know what's driving results.
- Platform-reported metrics are inflated. Always cross-reference with GA4 or server-side tracking and calculate blended CAC.
- Creative fatigue is real. Plan for refreshing ad creative every 4-6 weeks, not just at launch.
- Landing page experience matters as much as the ad. A great ad sending traffic to a poor landing page wastes budget.
- For B2B campaigns, account for longer sales cycles. A CPA goal based on demo requests is more realistic than direct purchase for high-ticket products.
- Recommend realistic budgets. Most platforms need $50-100/day minimum per campaign to gather enough data for optimization.
