---
name: competitor-analysis
description: Analyze competitive landscape to identify strengths, weaknesses, opportunities, and threats. Inform product strategy and positioning based on market insights.
---

# Competitor Analysis

## Overview

Systematic competitor analysis reveals market positioning, identifies competitive advantages, and informs strategic product decisions.

## When to Use

- Product strategy development
- Market entry planning
- Pricing strategy
- Feature prioritization
- Market positioning
- Threat assessment
- Investment decisions

## Instructions

### 1. **Competitor Identification**

```python
# Identify and categorize competitors

class CompetitorAnalysis:
    COMPETITOR_TYPES = {
        'Direct': 'Same market, same features',
        'Indirect': 'Different approach, same problem',
        'Adjacent': 'Related market, potential crossover',
        'Emerging': 'New entrants, potential disruptors'
    }

    def identify_competitors(self, market_segment):
        """Find all competitors"""
        return {
            'direct_competitors': [
                {'name': 'Competitor A', 'market_share': '25%', 'founded': 2015},
                {'name': 'Competitor B', 'market_share': '18%', 'founded': 2012}
            ],
            'indirect_competitors': [
                {'name': 'Different Approach A', 'method': 'AI-powered'}
            ],
            'emerging_threats': [
                {'name': 'Startup X', 'funding': '$10M Series A', 'differentiator': 'Mobile-first'}
            ]
        }

    def analyze_competitor(self, competitor):
        """Deep dive into competitor"""
        return {
            'name': competitor.name,
            'founded': competitor.founded,
            'headquarters': competitor.headquarters,
            'funding': competitor.total_funding,
            'employees': competitor.employee_count,
            'market_share': competitor.market_share,
            'target_market': competitor.segments,
            'strengths': self.identify_strengths(competitor),
            'weaknesses': self.identify_weaknesses(competitor),
            'recent_moves': self.track_recent_moves(competitor)
        }

    def identify_strengths(self, competitor):
        return {
            'product': ['Feature completeness', 'UI/UX quality', 'Performance'],
            'market': ['Brand recognition', 'Market share', 'Distribution'],
            'financial': ['Funding', 'Revenue', 'Profitability'],
            'team': ['Leadership', 'Engineering', 'Domain expertise']
        }

    def identify_weaknesses(self, competitor):
        return {
            'product': ['Missing features', 'Legacy architecture', 'Poor mobile experience'],
            'market': ['Regional limitations', 'High prices', 'Poor support'],
            'financial': ['Burn rate', 'Funding challenges', 'Profitability risk'],
            'team': ['Key departures', 'Talent gaps', 'Execution issues']
        }
```

### 2. **Competitive Matrix**

```yaml
Competitive Analysis Matrix:

Market: Project Management Tools
Analysis Date: January 2025

---

## Feature Comparison

Feature / Competitor | Our Product | Competitor A | Competitor B | Competitor C
---|---|---|---|---
Gantt Charts | Yes | Yes | No | Yes
Time Tracking | Yes | Limited | Yes | No
Mobile Apps | iOS + Android | iOS only | iOS + Android | Web only
API Available | Yes | Limited | Yes | No
Integrations | 50+ | 20+ | 80+ | 10+
Price (per user) | $8 | $10 | $6 | $15
Storage | Unlimited | 5GB | 50GB | Unlimited
Team Size Limit | None | 100 | 50 | 500
On-Premise | Yes | No | Yes | No

Score (out of 10):
  Our Product: 8.5
  Competitor A: 7.0
  Competitor B: 7.5
  Competitor C: 6.5

---

## Positioning Matrix

Performance/Capability (Y-axis) vs Price (X-axis)

Quadrant I (High Performance, High Price):
  - Competitor A: Premium positioning, enterprise focus

Quadrant II (High Performance, Low Price):
  - Our Product: Value leader
  - Competitor B: Budget competitor

Quadrant III (Low Performance, Low Price):
  - Competitor C: Basic features only

Quadrant IV (Low Performance, High Price):
  - (Empty - weak positioning)

---

## Customer Satisfaction Comparison

Metric | Our Product | Competitor A | Competitor B | Industry Avg
---|---|---|---|---
NPS (Net Promoter Score) | 48 | 42 | 35 | 40
CSAT (Satisfaction) | 4.2/5 | 3.8/5 | 4.0/5 | 3.9/5
Retention Rate | 92% | 85% | 78% | 80%
Support Response Time | 2 hours | 4 hours | 8 hours | 6 hours
Feature Adoption Rate | 65% | 45% | 50% | 52%

---

## Pricing Analysis

Our Pricing:
  Starter: $8/user/month (small teams)
  Professional: $12/user/month (growing teams)
  Enterprise: Custom pricing

Competitor Pricing:
  Competitor A: $10/user/month flat
  Competitor B: $6-$15/user/month (based on features)
  Competitor C: $15/user/month (premium positioning)

---

## Market Share & Growth

Market Size: $8.5B globally

Market Share (2024):
  Competitor A: 18% ($1.53B)
  Competitor B: 12% ($1.02B)
  Our Product: 8% ($0.68B)
  Competitor C: 5% ($0.43B)
  Others: 57% ($4.84B)

Growth Rate (YoY):
  Our Product: 35%
  Competitor A: 12%
  Competitor B: 25%
  Competitor C: 8%
  Market Average: 18%

Our Trajectory: Growing faster than competitors
```

### 3. **SWOT Analysis**

```javascript
// Comprehensive SWOT assessment

class SWOTAnalysis {
  createSWOT(company) {
    return {
      strengths: [
        'Superior mobile experience',
        'Fastest implementation (2 weeks)',
        'Best customer support (2-hour response)',
        'Advanced AI-powered automation',
        ' 95% customer retention',
        'Strong engineering team'
      ],
      weaknesses: [
        'Limited enterprise features',
        'Lower brand recognition vs competitors',
        'Smaller professional services team',
        'Limited on-premise deployment',
        'Fewer integrations than top competitor',
        'Smaller customer base (less network effects)'
      ],
      opportunities: [
        'Enterprise market (less penetrated)',
        'International expansion (5x market)',
        'AI/automation features (growing demand)',
        'Vertical-specific solutions',
        'API marketplace for partners',
        'SMB market consolidation'
      ],
      threats: [
        'Competitor A aggressively selling',
        'Free alternatives gaining traction',
        'Tech giants entering market (Google, Microsoft)',
        'Economic slowdown (budget cuts)',
        'Talent retention (headhunting)',
        'AI commoditization'
      ]
    };
  }

  strategyRecommendations(swot) {
    return {
      leverage_strengths: [
        'Market mobile-first advantage in campaigns',
        'Highlight superior support in sales',
        'Emphasize quick deployment (faster ROI)'
      ],
      address_weaknesses: [
        'Develop enterprise features roadmap',
        'Increase marketing/brand investment',
        'Expand partnerships for integrations'
      ],
      capitalize_opportunities: [
        'Launch enterprise edition (higher ACV)',
        'Plan international expansion roadmap',
        'Build AI feature suite aggressively'
      ],
      mitigate_threats: [
        'Strengthen customer lock-in (switching costs)',
        'Build ecosystem of partners',
        'Focus on customer success/retention',
        'Invest in differentiation'
      ]
    };
  }
}
```

### 4. **Competitive Insights Report**

```yaml
Competitive Intelligence Report

Prepared For: Executive Team, Product Team
Date: January 2025

---

## Executive Summary

Market Status: Moderately competitive with emerging threats
Opportunity: Underserved enterprise segment
Recommendation: Invest in enterprise features and global expansion

---

## Key Competitive Moves

This Quarter:
  - Competitor A: Released AI copilot feature
    Our Response: Advanced in AI roadmap priority

  - Competitor B: Launched free tier
    Our Response: Strengthen free tier features and conversion funnel

  - Competitor C: Acquired integration company
    Our Response: Expand API marketplace strategy

---

## Market Trends

1. AI/Automation: All competitors investing heavily
   Impact: Must innovate or lose relevance
   Timeline: Next 12 months critical

2. Vertical Solutions: Moving to industry-specific products
   Impact: Opportunity to capture niche markets
   Timeline: 6-month window to launch

3. Pricing Pressure: Race to lower entry price
   Impact: Need to emphasize value/ROI over price
   Timeline: Ongoing

4. Consolidation: Market consolidation beginning
   Impact: Opportunity for acquisition or IPO
   Timeline: 18-24 months

---

## Recommended Actions

High Priority (Next 30 days):
  1. Launch AI feature beta (response to Competitor A)
  2. Analyze free tier conversion (response to Competitor B)
  3. Identify vertical market targets

Medium Priority (Next 90 days):
  1. Develop enterprise edition
  2. Build integration marketplace
  3. Plan international expansion

Long-term (6-12 months):
  1. Position for acquisition or IPO
  2. Build ecosystem and partnerships
  3. Establish market leadership in chosen vertical
```

## Best Practices

### ✅ DO
- Analyze current and emerging competitors
- Monitor competitor activities regularly
- Understand customer perception of competition
- Use competitive insights to inform strategy
- Focus on differentiation, not just comparison
- Include market trends in analysis
- Update competitive analysis quarterly
- Share insights across organization
- Use data to back up claims
- Consider indirect competitors too

### ❌ DON'T
- Obsess over competitor pricing
- Copy competitor features blindly
- Ignore emerging threats
- Use only marketing materials for analysis
- Focus only on feature comparison
- Neglect customer feedback on competition
- Make analysis too complex
- Hide uncomfortable truths
- Change strategy based on every competitor move
- Ignore your competitive advantages

## Competitive Analysis Tips

- Use public data sources (websites, job postings, funding)
- Talk to customers about competitors
- Follow competitor social media and blogs
- Set up competitor monitoring alerts
- Review customer reviews (G2, Capterra, etc.)
- Attend industry conferences
