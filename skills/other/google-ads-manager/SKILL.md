---
name: google-ads-manager
description: "Google Ads campaign management - campaign setup, keyword research, bid optimization, and performance reporting"
version: "1.0.0"
author: claude-office-skills
license: MIT

category: marketing
tags:
  - google-ads
  - ppc
  - sem
  - advertising
  - keywords
department: Marketing

models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4

mcp:
  server: ads-mcp
  tools:
    - google_ads_create
    - google_ads_report
    - keyword_planner

capabilities:
  - campaign_creation
  - keyword_research
  - ad_copy_generation
  - bid_optimization
  - performance_reporting

languages:
  - en
  - zh

related_skills:
  - ads-copywriter
  - saas-metrics
  - landing-page
---

# Google Ads Manager

Comprehensive Google Ads campaign management including campaign setup, keyword research, ad copy generation, bid optimization, and performance reporting.

## Overview

This skill covers:
- Campaign structure and setup
- Keyword research and grouping
- Ad copy creation (RSA format)
- Bidding strategy selection
- Performance analysis and optimization

---

## Campaign Structure

### Account Hierarchy

```
Account
├── Campaign 1: Brand
│   ├── Ad Group: Brand Terms
│   │   ├── Keywords: [brand name], [brand + product]
│   │   └── Ads: 3-5 RSAs
│   └── Ad Group: Brand + Competitor
│       ├── Keywords: [brand vs competitor]
│       └── Ads: 3-5 RSAs
│
├── Campaign 2: Non-Brand - Search
│   ├── Ad Group: Product Category A
│   │   ├── Keywords: [category keywords]
│   │   └── Ads: 3-5 RSAs
│   ├── Ad Group: Product Category B
│   └── Ad Group: Problem/Solution
│
├── Campaign 3: Competitor
│   ├── Ad Group: Competitor A
│   └── Ad Group: Competitor B
│
└── Campaign 4: Performance Max
    └── Asset Groups: [Images, Videos, Headlines, Descriptions]
```

### Campaign Setup Template

```yaml
campaign:
  name: "[Product] - Search - Non-Brand"
  type: SEARCH
  budget: 
    amount: 100  # daily
    delivery: STANDARD
  
  bidding:
    strategy: TARGET_CPA  # or MAXIMIZE_CONVERSIONS
    target_cpa: 50
    
  targeting:
    locations: [US, CA, UK]
    languages: [en]
    audiences: 
      - in_market: "Business Software"
      - custom_intent: "project management tools"
    
  networks:
    search: true
    display: false
    partners: false
    
  schedule:
    days: [MON, TUE, WED, THU, FRI]
    hours: "8:00-20:00"
    timezone: "America/New_York"
    
  ad_rotation: OPTIMIZE
  
  negative_keywords:
    campaign_level:
      - free
      - cheap
      - download
      - jobs
      - salary
```

---

## Keyword Research

### Keyword Categories

```yaml
keyword_types:
  brand:
    examples: ["[brand name]", "[brand] login", "[brand] pricing"]
    intent: navigational
    expected_cpc: low
    priority: high
    
  competitor:
    examples: ["[competitor] alternative", "[competitor] vs"]
    intent: commercial
    expected_cpc: medium-high
    priority: medium
    
  product:
    examples: ["project management software", "task tracking tool"]
    intent: commercial
    expected_cpc: high
    priority: high
    
  problem:
    examples: ["how to manage remote team", "track project deadlines"]
    intent: informational/commercial
    expected_cpc: medium
    priority: medium
    
  long_tail:
    examples: ["best project management tool for small teams"]
    intent: commercial
    expected_cpc: medium
    priority: high (high intent)
```

### Keyword Research Process

```yaml
research_steps:
  1. seed_keywords:
      sources:
        - brainstorm: core product terms
        - competitor: analyze competitor ads
        - customer: survey/interview terms
        - support: common questions
        
  2. expand_with_tools:
      google_keyword_planner:
        - get_ideas: from seed keywords
        - filter: by volume, competition, CPC
        
      other_tools:
        - semrush: competitor keywords
        - ahrefs: organic keywords to target
        - answerthepublic: question keywords
        
  3. group_keywords:
      method: SKAG or themed groups
      max_per_group: 15-20
      criteria: same intent, similar landing page
      
  4. match_types:
      broad_match: discovery, high volume
      phrase_match: balanced reach/relevance
      exact_match: high intent, control
      
  5. negative_keywords:
      identify: irrelevant search terms
      levels: campaign, ad group, account
```

### Keyword Grouping Example

```yaml
ad_group: "Project Management Software"
theme: product_category

keywords:
  exact_match:
    - [project management software]
    - [project management tool]
    - [pm software]
    
  phrase_match:
    - "project management software"
    - "best project management"
    - "project tracking software"
    
  broad_match:
    - project management platform
    - team project software

negative_keywords:
  - free
  - open source
  - template
  - excel
  - certification
```

---

## Ad Copy Framework

### Responsive Search Ad (RSA) Structure

```yaml
rsa_requirements:
  headlines:
    count: 15 (min 3)
    max_chars: 30
    pin_strategy:
      position_1: keyword/benefit headline
      position_2: value prop/differentiator
      position_3: CTA
      
  descriptions:
    count: 4 (min 2)
    max_chars: 90
    
  display_path:
    parts: 2
    max_chars: 15 each
```

### Headline Templates by Category

```yaml
headline_templates:
  keyword_headlines: # Pin to Position 1
    - "{Keyword} Software"
    - "Best {Keyword} Tool"
    - "#1 {Keyword} Platform"
    - "{Keyword} for Teams"
    
  benefit_headlines:
    - "Save 10+ Hours/Week"
    - "Boost Productivity 40%"
    - "Manage Projects Easily"
    - "Never Miss Deadlines"
    
  trust_headlines:
    - "Trusted by 50,000+ Teams"
    - "4.8★ on G2 & Capterra"
    - "Award-Winning Software"
    - "Enterprise-Grade Security"
    
  cta_headlines: # Pin to Position 3
    - "Start Free Trial"
    - "Try Free for 14 Days"
    - "Get Started Today"
    - "Request a Demo"
    
  urgency_headlines:
    - "Limited Time: 30% Off"
    - "Special Offer Ends Soon"
    - "Save Now - Act Fast"
    
  differentiator_headlines:
    - "No Credit Card Needed"
    - "Set Up in 2 Minutes"
    - "Cancel Anytime"
    - "All-in-One Solution"
```

### Description Templates

```yaml
description_templates:
  benefit_focused:
    - "Streamline your workflow with our all-in-one project management platform. Trusted by 50,000+ teams worldwide."
    - "Save 10+ hours per week with automated task tracking, team collaboration, and real-time reporting. Try free!"
    
  feature_focused:
    - "Kanban boards, Gantt charts, time tracking, and team chat in one powerful platform. Start your free trial today."
    
  social_proof:
    - "Join 50,000+ teams who've transformed their productivity. Rated 4.8/5 on G2. No credit card required."
    
  urgency:
    - "Limited time: Get 30% off annual plans. All features included. Start your 14-day free trial now!"
```

---

## Bidding Strategies

### Strategy Selection Guide

```yaml
bidding_strategies:
  maximize_conversions:
    use_when:
      - new_campaign: true
      - goal: volume
      - budget: flexible
    pros: easy setup, google optimization
    cons: no cost control
    
  target_cpa:
    use_when:
      - conversion_history: 30+ conversions/month
      - goal: efficiency
      - known_cpa_target: true
    pros: cost control, predictable
    cons: may limit volume
    
  target_roas:
    use_when:
      - ecommerce: true
      - conversion_value_tracking: enabled
      - goal: roi_optimization
    pros: revenue-focused
    cons: needs value data
    
  maximize_clicks:
    use_when:
      - goal: traffic
      - new_campaign: awareness
    pros: simple, good for testing
    cons: no conversion focus
    
  manual_cpc:
    use_when:
      - full_control: needed
      - small_budget: true
      - testing: keywords
    pros: granular control
    cons: time-intensive

bid_adjustments:
  device:
    mobile: -20% to +30%
    tablet: -10% to +10%
  
  location:
    high_value_cities: +20%
    low_value_areas: -30%
    
  schedule:
    business_hours: +15%
    off_hours: -25%
    
  audience:
    remarketing: +50%
    in_market: +20%
```

---

## Performance Reporting

### Key Metrics Dashboard

```markdown
# Google Ads Performance Report - {Date Range}

## Campaign Summary
| Campaign | Spend | Clicks | Conv | CPA | ROAS |
|----------|-------|--------|------|-----|------|
| Brand | $500 | 1,200 | 80 | $6.25 | 15x |
| Non-Brand | $3,000 | 2,500 | 45 | $66.67 | 3.2x |
| Competitor | $800 | 600 | 12 | $66.67 | 2.8x |
| **Total** | **$4,300** | **4,300** | **137** | **$31.39** | **5.1x** |

## Key Metrics
- **CTR**: 3.2% (benchmark: 2%)  ✅
- **Conv Rate**: 3.2% (benchmark: 3%)  ✅
- **Avg CPC**: $1.00
- **Quality Score Avg**: 7.2/10

## Top Performing Keywords
| Keyword | Clicks | Conv | CPA | QS |
|---------|--------|------|-----|-----|
| [brand name] | 800 | 60 | $5 | 9 |
| project management software | 300 | 15 | $40 | 7 |
| best pm tool for teams | 150 | 12 | $35 | 8 |

## Underperforming (Action Needed)
| Keyword | Spend | Conv | CPA | Action |
|---------|-------|------|-----|--------|
| free project tool | $200 | 0 | - | Pause |
| pm software download | $150 | 1 | $150 | Pause |

## Recommendations
1. ⬆️ Increase budget on Brand campaign (CPA $6.25)
2. ⏸️ Pause 5 keywords with $0 conversions
3. 📝 Test new ad copy (current CTR below benchmark)
4. 🎯 Add "free" to negative keywords
```

### Optimization Checklist

```yaml
weekly_tasks:
  - review_search_terms:
      action: add negatives, find new keywords
      
  - check_quality_scores:
      action: improve <6 QS keywords
      
  - review_ad_performance:
      action: pause low CTR ads
      
  - adjust_bids:
      action: increase for high performers
      
monthly_tasks:
  - competitor_analysis:
      check: new competitors, messaging
      
  - landing_page_review:
      check: conversion rate by page
      
  - audience_review:
      check: add new audiences, remove poor performers
      
  - budget_reallocation:
      check: move budget to top performers
```

---

## Output Example

**Request**: "Create a Google Ads campaign structure for a CRM software"

**Output**:

```markdown
# Google Ads Campaign Structure - CRM Software

## Campaign 1: Brand

**Budget**: $50/day
**Bidding**: Maximize Conversions

### Ad Group: Brand Terms
**Keywords**:
- [acme crm]
- [acme crm login]
- [acme crm pricing]

**Headlines**:
1. Acme CRM - Official Site
2. Trusted by 10,000+ Teams
3. Start Your Free Trial
...

---

## Campaign 2: Non-Brand Search

**Budget**: $200/day
**Bidding**: Target CPA ($75)

### Ad Group: CRM Software
**Keywords**:
- [crm software]
- [best crm software]
- "crm for small business"

**Headlines**:
1. Best CRM Software 2026
2. Close 40% More Deals
3. Try Free for 14 Days
...

### Ad Group: Sales Software
**Keywords**:
- [sales management software]
- [sales tracking tool]
...

### Ad Group: Problem/Solution
**Keywords**:
- "how to track sales leads"
- "manage customer relationships"
...

---

## Campaign 3: Competitor

**Budget**: $100/day
**Bidding**: Target CPA ($90)

### Ad Group: Salesforce Alternative
**Keywords**:
- [salesforce alternative]
- [salesforce vs]
- "cheaper than salesforce"

**Headlines**:
1. Salesforce Alternative
2. 50% Lower Cost
3. Switch in 1 Day
...

---

## Negative Keywords (Account Level)
- free
- jobs
- salary
- certification
- tutorial
- open source

---

## Estimated Performance
| Campaign | Est. Clicks | Est. Conv | Est. CPA |
|----------|-------------|-----------|----------|
| Brand | 1,500 | 150 | $8 |
| Non-Brand | 2,000 | 25 | $80 |
| Competitor | 800 | 10 | $100 |
```

---

*Google Ads Manager Skill - Part of Claude Office Skills*
