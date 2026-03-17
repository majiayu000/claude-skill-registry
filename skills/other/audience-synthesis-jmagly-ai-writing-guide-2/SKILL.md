# audience-synthesis

Synthesize audience insights from multiple data sources into unified personas and segments.

## Triggers

- "analyze audience"
- "build personas"
- "segment audience"
- "who is our target"
- "audience insights"
- "customer profile"

## Purpose

This skill creates comprehensive audience understanding by:
- Aggregating data from multiple sources
- Building data-driven personas
- Creating behavioral segments
- Identifying growth opportunities
- Recommending targeting strategies

## Behavior

When triggered, this skill:

1. **Gathers audience data**:
   - Analytics demographics
   - CRM customer data
   - Social audience insights
   - Survey/research data
   - Purchase behavior

2. **Identifies patterns**:
   - Demographic clusters
   - Behavioral segments
   - Value tiers
   - Engagement patterns

3. **Builds personas**:
   - Synthesize data into archetypes
   - Document motivations and pain points
   - Map customer journey
   - Identify content preferences

4. **Creates segments**:
   - Behavioral segmentation
   - Value-based segmentation
   - Engagement segmentation
   - Lifecycle segmentation

5. **Generates recommendations**:
   - Targeting strategies
   - Content recommendations
   - Channel preferences
   - Growth opportunities

## Data Sources

### First-Party Data

```yaml
first_party:
  analytics:
    source: Google Analytics, Mixpanel
    data:
      - demographics
      - interests
      - behavior
      - conversion_paths

  crm:
    source: Salesforce, HubSpot
    data:
      - customer_attributes
      - purchase_history
      - lifetime_value
      - engagement_history

  email:
    source: Mailchimp, Klaviyo
    data:
      - email_engagement
      - preferences
      - segments

  product:
    source: Product analytics
    data:
      - feature_usage
      - retention
      - activation
```

### Second-Party Data

```yaml
second_party:
  social:
    source: Instagram, LinkedIn, Twitter
    data:
      - follower_demographics
      - engagement_patterns
      - content_preferences

  advertising:
    source: Meta, Google, LinkedIn
    data:
      - audience_overlap
      - conversion_audiences
      - lookalike_performance

  partnerships:
    source: Partner data shares
    data:
      - co-marketing audiences
      - industry benchmarks
```

### Third-Party Data

```yaml
third_party:
  research:
    source: Industry reports, surveys
    data:
      - market_size
      - industry_trends
      - competitor_audiences

  enrichment:
    source: Clearbit, ZoomInfo
    data:
      - firmographics
      - technographics
      - intent_signals
```

## Persona Template

```markdown
# Persona: [Name]

## Overview

| Attribute | Value |
|-----------|-------|
| Name | Tech-Savvy Tara |
| Role | Marketing Manager |
| Age Range | 28-35 |
| Experience | 5-8 years |
| Company Size | 50-200 employees |
| Industry | SaaS, Tech |

## Demographics

### Professional
- **Title**: Marketing Manager, Growth Lead
- **Seniority**: Mid-level
- **Department**: Marketing, Growth
- **Reports to**: CMO, VP Marketing
- **Team size**: 2-5 direct reports

### Personal
- **Education**: Bachelor's, Marketing/Business
- **Location**: Urban, tech hubs
- **Income**: $75-100K
- **Tech adoption**: Early adopter

## Psychographics

### Goals
1. Prove marketing ROI to leadership
2. Automate repetitive tasks
3. Stay ahead of industry trends
4. Advance career to director level

### Challenges
1. Limited budget vs. big ambitions
2. Lack of technical resources
3. Proving attribution across channels
4. Keeping up with platform changes

### Motivations
- **Achiever**: Wants measurable results
- **Learner**: Values staying current
- **Collaborator**: Seeks team success
- **Efficiency-seeker**: Hates wasted time

### Fears
- Falling behind competitors
- Wasting budget on ineffective campaigns
- Not having data to support decisions
- Missing key industry shifts

## Behavior

### Content Consumption
- **Formats**: Podcasts, newsletters, Twitter
- **Topics**: Marketing trends, case studies, how-tos
- **Sources**: Marketing Brew, HubSpot Blog, industry Twitter
- **Time**: Morning commute, lunch breaks

### Purchase Behavior
- **Research**: Extensive (4-6 week cycle)
- **Influencers**: Peers, G2 reviews, case studies
- **Decision factors**: ROI proof, ease of use, integrations
- **Barriers**: Price, implementation time, approval process

### Channel Preferences
| Channel | Preference | Best For |
|---------|------------|----------|
| Email | High | Nurture, updates |
| LinkedIn | High | Professional content |
| Webinars | Medium | Deep dives |
| Twitter | Medium | News, trends |
| Phone | Low | Only when ready |

## Customer Journey

### Awareness
- **Trigger**: Frustration with current tools
- **Actions**: Google search, ask peers, browse LinkedIn
- **Content**: Blog posts, social proof, thought leadership

### Consideration
- **Trigger**: Identified potential solutions
- **Actions**: Demo requests, free trials, case study reviews
- **Content**: Comparison guides, ROI calculators, webinars

### Decision
- **Trigger**: Validated fit, secured budget
- **Actions**: Negotiate, involve stakeholders, trial
- **Content**: Pricing details, implementation guides, success stories

### Retention
- **Trigger**: Ongoing value demonstration
- **Actions**: Feature adoption, support engagement
- **Content**: Best practices, new features, community

## Messaging

### Value Props That Resonate
1. "Save 10 hours per week on reporting"
2. "Prove ROI to your leadership in one click"
3. "Join 5,000+ marketers who increased conversions 40%"

### Objection Handlers
| Objection | Response |
|-----------|----------|
| "Too expensive" | ROI payback in 3 months |
| "No time to implement" | Live in 2 hours, not weeks |
| "Current tool works" | Missing these 3 key features |

### Tone & Voice
- Professional but approachable
- Data-driven with clear examples
- Empathetic to time constraints
- Action-oriented

## Targeting

### Ideal Channels
1. LinkedIn (professional context)
2. Email (direct, personalized)
3. Podcast ads (captive attention)
4. Industry events (high-intent)

### Lookalike Indicators
- HubSpot/Mailchimp users
- Marketing conference attendees
- Marketing podcast subscribers
- G2 reviewer profiles

### Exclusions
- Enterprise (100K+ employees)
- Agencies (different needs)
- Non-marketing roles

## Data Sources

- Analytics: 45% of traffic matches profile
- CRM: 2,340 customers in segment
- Survey: 2023 customer research (n=500)
- Social: LinkedIn follower analysis
```

## Segmentation Framework

```yaml
segmentation_types:
  behavioral:
    name: Behavioral Segments
    dimensions:
      - engagement_level: [highly_active, active, passive, dormant]
      - feature_usage: [power_user, standard, limited]
      - purchase_frequency: [frequent, occasional, one_time]
    use_cases:
      - Lifecycle marketing
      - Retention campaigns
      - Upsell targeting

  value_based:
    name: Value Segments
    dimensions:
      - ltv_tier: [platinum, gold, silver, bronze]
      - revenue_potential: [high, medium, low]
      - expansion_likelihood: [likely, possible, unlikely]
    use_cases:
      - Resource allocation
      - Account prioritization
      - Pricing strategies

  demographic:
    name: Demographic Segments
    dimensions:
      - company_size: [enterprise, mid_market, smb, startup]
      - industry: [tech, finance, healthcare, retail, etc]
      - geography: [region, country, city_tier]
    use_cases:
      - Content personalization
      - Sales territory planning
      - Localization

  psychographic:
    name: Psychographic Segments
    dimensions:
      - buying_style: [innovator, pragmatist, conservative]
      - decision_process: [solo, committee, consensus]
      - risk_tolerance: [risk_taker, calculated, risk_averse]
    use_cases:
      - Message positioning
      - Sales approach
      - Content tone
```

## Audience Synthesis Report

```markdown
# Audience Synthesis Report

**Date**: 2025-12-08
**Scope**: Full audience analysis
**Data Sources**: 6 platforms, 2 research studies

## Executive Summary

### Audience Composition

| Segment | % of Total | Revenue % | Growth YoY |
|---------|------------|-----------|------------|
| Power Users | 15% | 45% | +22% |
| Regular Users | 35% | 35% | +8% |
| Occasional Users | 30% | 15% | -5% |
| At-Risk | 20% | 5% | -15% |

### Key Insights

1. **High-value concentration**: 15% of users drive 45% of revenue
2. **Growth opportunity**: Mid-market segment growing fastest (+18%)
3. **Retention risk**: 20% of audience showing disengagement signals
4. **Channel shift**: Mobile usage up 35%, desktop flat

## Persona Summary

### Primary Personas

| Persona | % of Audience | LTV | Acquisition Cost |
|---------|---------------|-----|------------------|
| Tech-Savvy Tara | 35% | $2,400 | $180 |
| Enterprise Ed | 20% | $12,000 | $1,200 |
| Startup Sam | 25% | $600 | $45 |
| Agency Amy | 20% | $1,800 | $220 |

### Persona Details

[Link to full persona documents]

## Segment Analysis

### By Engagement Level

```
Highly Active ████████████████ 25%
Active        ████████████████████████ 35%
Passive       ████████████████ 25%
Dormant       ██████████ 15%
```

### By Company Size

```
Enterprise  ████████ 12%
Mid-Market  ████████████████████ 28%
SMB         ████████████████████████████ 42%
Startup     ████████████████ 18%
```

### By Industry

| Industry | Users | Growth | Opportunity |
|----------|-------|--------|-------------|
| Tech/SaaS | 35% | +15% | Maintain |
| Finance | 18% | +25% | Expand |
| Healthcare | 12% | +8% | Monitor |
| Retail | 15% | +5% | Optimize |
| Other | 20% | +3% | Evaluate |

## Growth Opportunities

### 1. Finance Vertical Expansion
- **Opportunity**: Growing 25% YoY, only 18% of current base
- **Recommendation**: Develop finance-specific content and case studies
- **Estimated impact**: +$500K ARR

### 2. Power User Amplification
- **Opportunity**: Power users have 4x referral rate
- **Recommendation**: Launch referral program targeting power users
- **Estimated impact**: +200 customers/quarter

### 3. At-Risk Win-Back
- **Opportunity**: 20% of users showing disengagement
- **Recommendation**: Automated re-engagement campaign
- **Estimated impact**: Save $150K ARR churn

## Targeting Recommendations

### Lookalike Audiences

| Source Audience | Platform | Expected ROAS |
|-----------------|----------|---------------|
| Power Users | Meta | 3.5x |
| Recent Converters | Google | 2.8x |
| High LTV | LinkedIn | 2.2x |

### Exclusion Recommendations

- Current customers (all platforms)
- Competitors' employees
- Students/job seekers
- Non-target geographies

### Channel Allocation

| Persona | Primary Channel | Secondary | Budget % |
|---------|-----------------|-----------|----------|
| Tech-Savvy Tara | LinkedIn | Email | 40% |
| Enterprise Ed | Events | LinkedIn | 25% |
| Startup Sam | Content/SEO | Twitter | 20% |
| Agency Amy | Partner | Email | 15% |

## Action Items

1. [ ] Build finance vertical content series
2. [ ] Launch power user referral program
3. [ ] Deploy at-risk re-engagement automation
4. [ ] Update lookalike audiences with Q4 data
5. [ ] Create persona-specific landing pages

## Data Quality Notes

- CRM data 94% complete
- Analytics sampling at 95% confidence
- Survey margin of error: ±4%
- Social data limited to organic followers
```

## Usage Examples

### Full Audience Analysis

```
User: "Analyze our audience"

Skill executes:
1. Pull data from all sources
2. Identify patterns and segments
3. Build/update personas
4. Generate recommendations

Output:
"Audience Analysis Complete

Total Addressable: 45,000 users
Active: 32,000 (71%)

Key Segments:
1. Power Users (15%): High LTV, expansion ready
2. Growing Mid-Market (+18% YoY)
3. At-Risk (20%): Needs re-engagement

Top Personas:
- Tech-Savvy Tara (35%): Your core user
- Enterprise Ed (20%): Highest LTV ($12K)
- Startup Sam (25%): Highest volume, lowest LTV

Growth Opportunities:
1. Finance vertical: +25% growth, underserved
2. Power user referrals: 4x rate potential
3. At-risk save: $150K ARR protection

Report: .aiwg/marketing/audience/synthesis-2025-12.md"
```

### Build Specific Persona

```
User: "Build persona for enterprise buyers"

Skill creates:
- Aggregate enterprise customer data
- Identify common patterns
- Build comprehensive persona

Output:
"Enterprise Persona: 'Enterprise Ed'

Profile:
- Role: VP/Director level
- Company: 500-5000 employees
- Budget: $50K+ annual
- Decision: 3-6 month cycle

Key Insights:
- Values: Security, support, scalability
- Concerns: Implementation risk, vendor stability
- Content: Case studies, ROI calculators, demos
- Channel: Events, direct outreach, LinkedIn

Persona saved: .aiwg/marketing/personas/enterprise-ed.md"
```

## Integration

This skill uses:
- `data-pipeline`: Source marketing data
- `project-awareness`: Context for analysis
- `artifact-metadata`: Track audience artifacts

## Agent Orchestration

```yaml
agents:
  analysis:
    agent: marketing-analyst
    focus: Data analysis and pattern identification

  research:
    agent: market-researcher
    focus: External research and enrichment

  strategy:
    agent: positioning-specialist
    focus: Targeting and positioning recommendations
```

## Configuration

### Persona Defaults

```yaml
persona_config:
  max_personas: 5
  refresh_frequency: quarterly
  data_requirements:
    - min_sample_size: 100
    - required_sources: 3+
    - recency: <90_days
```

### Segmentation Rules

```yaml
segmentation_rules:
  min_segment_size: 5%
  max_segments: 10
  required_dimensions:
    - engagement
    - value
    - lifecycle
```

## Output Locations

- Personas: `.aiwg/marketing/personas/`
- Segments: `.aiwg/marketing/segments/`
- Synthesis reports: `.aiwg/marketing/audience/`
- Data sources: `.aiwg/marketing/data/audience/`

## References

- Persona templates: templates/marketing/persona-template.md
- Segmentation guide: docs/segmentation-guide.md
- Data sources: .aiwg/marketing/config/data-sources.yaml
