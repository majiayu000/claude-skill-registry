---
name: influencer-marketing
description: Эксперт по influencer-маркетингу. Используй для работы с инфлюенсерами, UGC и creator partnerships.
---

# Influencer Marketing Expert

Strategic expertise in building and managing influencer marketing programs.

## Core Competencies

### Strategy
- Influencer identification and vetting
- Partnership alignment with brand
- Campaign planning and execution
- Platform selection
- Budget allocation

### Relationship Management
- Outreach and negotiation
- Contract management
- Creative briefing
- Relationship nurturing
- Long-term partnerships

### Execution
- Campaign management
- Content review and approval
- Amplification strategy
- Performance tracking
- Compliance and disclosure

## Influencer Tiers

| Tier | Followers | Engagement | Cost Range | Best For |
|------|-----------|------------|------------|----------|
| Nano | 1K-10K | 5-10% | $50-500 | Authenticity, niche |
| Micro | 10K-100K | 3-5% | $500-5K | Niche targeting |
| Macro | 100K-1M | 1-3% | $5K-50K | Scale, reach |
| Mega | 1M+ | <1% | $50K+ | Mass awareness |

### Tier Selection Framework

```yaml
Choose Nano/Micro when:
  - Budget is limited
  - Authenticity is priority
  - Niche audience targeting
  - High engagement needed
  - Long-term relationships desired

Choose Macro/Mega when:
  - Brand awareness is goal
  - Mass reach required
  - Product launch campaigns
  - Celebrity association valuable
  - Budget allows for scale
```

## Platform Expertise

### Instagram

```yaml
Best For:
  - Lifestyle, fashion, beauty
  - Visual products
  - B2C brands

Content Formats:
  - Feed posts (highest permanence)
  - Stories (24h, high engagement)
  - Reels (algorithm boost, reach)
  - Lives (real-time engagement)

Key Metrics:
  - Reach and impressions
  - Saves and shares
  - Story replies
  - Profile visits
  - Link clicks (Stories)

Typical Rates:
  - Nano: $50-250/post
  - Micro: $250-1,000/post
  - Macro: $1,000-10,000/post
  - Mega: $10,000+/post
```

### TikTok

```yaml
Best For:
  - Gen Z and Millennials
  - Trend-driven products
  - Entertainment value
  - Viral potential

Content Formats:
  - Native videos (15s-3min)
  - Duets and stitches
  - TikTok Lives
  - TikTok Shop integration

Key Metrics:
  - Video views
  - Watch time/completion rate
  - Shares
  - Comments
  - Follower growth

Typical Rates:
  - Nano: $25-200/video
  - Micro: $200-2,500/video
  - Macro: $2,500-25,000/video
  - Mega: $25,000+/video
```

### YouTube

```yaml
Best For:
  - In-depth product content
  - Tutorials and reviews
  - Long-form storytelling
  - Search discovery

Content Formats:
  - Dedicated videos
  - Integrations (30-90s)
  - Shorts (≤60s)
  - Live streams

Key Metrics:
  - Views
  - Watch time
  - CTR on cards/links
  - Subscriber growth
  - Comments

Typical Rates:
  - Micro: $1,000-5,000/integration
  - Macro: $5,000-50,000/video
  - Mega: $50,000+/video
```

### LinkedIn

```yaml
Best For:
  - B2B products/services
  - Thought leadership
  - Professional audience
  - Enterprise targeting

Content Formats:
  - Text posts with images
  - Articles
  - Videos (native)
  - Document carousels

Key Metrics:
  - Impressions
  - Engagement rate
  - Profile views
  - Lead generation

Typical Rates:
  - Micro: $500-2,000/post
  - Macro: $2,000-10,000/post
```

## Campaign Types

### Product Seeding

```yaml
Description: Send free product for organic review
Investment: Product cost only
Control: Low - authentic reactions
Timeline: 2-4 weeks for content

Best Practices:
  - Personalize outreach
  - No content requirements
  - Build relationship first
  - Accept honest feedback
  - Track organic mentions
```

### Sponsored Content

```yaml
Description: Paid posts with disclosure
Investment: Fee + product
Control: Medium - briefed content
Timeline: 2-6 weeks campaign

Best Practices:
  - Clear brief but creative freedom
  - FTC/ASA compliant disclosures
  - Multiple rounds of review
  - Usage rights negotiation
  - Exclusivity terms
```

### Brand Ambassador

```yaml
Description: Long-term partnership
Investment: Retainer + performance
Control: High - ongoing relationship
Timeline: 3-12 month contracts

Best Practices:
  - Thorough vetting process
  - Clear exclusivity terms
  - Regular check-ins
  - Performance bonuses
  - Content calendar planning
```

### Affiliate/Performance

```yaml
Description: Commission-based partnership
Investment: Revenue share (10-30%)
Control: Low - performance motivated
Timeline: Ongoing

Best Practices:
  - Competitive commission rates
  - Quality tracking links
  - Real-time reporting
  - Tiered incentives
  - Long cookie windows
```

## Influencer Vetting

### Evaluation Criteria

```python
def evaluate_influencer(profile):
    """Score potential influencer partners."""

    score = 0
    max_score = 100

    # Engagement quality (25 points)
    engagement_rate = profile['engagements'] / profile['followers']
    if engagement_rate > 0.05:
        score += 25
    elif engagement_rate > 0.03:
        score += 15
    elif engagement_rate > 0.01:
        score += 10

    # Audience authenticity (25 points)
    if profile['fake_follower_rate'] < 0.10:
        score += 25
    elif profile['fake_follower_rate'] < 0.20:
        score += 15

    # Content quality (20 points)
    score += profile['content_quality_score'] * 2  # 1-10 scale

    # Brand alignment (15 points)
    if profile['category'] in BRAND_CATEGORIES:
        score += 10
    if profile['values_alignment']:
        score += 5

    # Audience demographics match (15 points)
    demo_match = calculate_demo_overlap(profile['audience'], TARGET_AUDIENCE)
    score += demo_match * 15

    return {
        'influencer': profile['handle'],
        'score': score,
        'recommendation': 'strong' if score > 75 else 'moderate' if score > 50 else 'weak'
    }
```

### Red Flags

```yaml
Avoid If:
  - Engagement rate below 1%
  - Sudden follower spikes (bought followers)
  - Generic/bot comments
  - No brand collaborations history
  - Past controversial content
  - Fake engagement pods
  - Doesn't disclose partnerships
  - Unrealistic promises
```

## Campaign Brief Template

```yaml
Campaign Overview:
  brand: "[Brand Name]"
  product: "[Product/Service]"
  campaign_name: "[Campaign Name]"
  timeline: "[Start - End Date]"

Objectives:
  primary: "[Awareness/Consideration/Conversion]"
  kpis:
    - "[Metric 1]: [Target]"
    - "[Metric 2]: [Target]"

Target Audience:
  demographics: "[Age, Gender, Location]"
  psychographics: "[Interests, Values, Behaviors]"

Key Messages:
  must_include:
    - "[Key benefit 1]"
    - "[Key benefit 2]"
  avoid:
    - "[Competitor mentions]"
    - "[Specific claims]"

Content Requirements:
  platform: "[Platform]"
  format: "[Post/Story/Video]"
  quantity: "[Number of posts]"
  hashtags: "[Required hashtags]"
  mentions: "@[brand_handle]"
  disclosure: "#ad #sponsored"

Creative Direction:
  tone: "[Authentic, Fun, Professional]"
  visual_style: "[Description]"
  do_examples: "[Links to good examples]"
  dont_examples: "[What to avoid]"

Approval Process:
  steps:
    1. Submit concept/draft
    2. Brand review (48h)
    3. Revisions if needed
    4. Final approval
    5. Post within window

Deliverables:
  - Raw content files
  - Platform analytics (48h post)
  - Usage rights for [X months]
```

## Measurement Framework

### Campaign Metrics

| Metric | Formula | Purpose |
|--------|---------|---------|
| CPM | Cost / Impressions × 1000 | Cost efficiency |
| CPE | Cost / Engagements | Engagement efficiency |
| EMV | Earned Media Value | PR-equivalent value |
| ROAS | Revenue / Spend | Sales efficiency |
| Brand Lift | Survey-based | Awareness impact |
| Sentiment | Positive / Total | Brand perception |

### ROI Calculation

```python
def calculate_campaign_roi(campaign):
    """Calculate influencer campaign ROI."""

    total_cost = sum([
        campaign['influencer_fees'],
        campaign['product_cost'],
        campaign['agency_fees'],
        campaign['paid_amplification']
    ])

    # Direct revenue (tracked conversions)
    direct_revenue = campaign['attributed_sales']

    # Estimated earned media value
    emv = (
        campaign['impressions'] * 0.005 +  # CPM equivalent
        campaign['engagements'] * 0.50     # CPE equivalent
    )

    # Total value
    total_value = direct_revenue + emv

    return {
        'total_cost': total_cost,
        'direct_revenue': direct_revenue,
        'emv': emv,
        'total_value': total_value,
        'roi': (total_value - total_cost) / total_cost * 100,
        'roas': direct_revenue / total_cost
    }
```

## Contract Essentials

```yaml
Key Terms to Include:
  Scope:
    - Deliverables and quantities
    - Platforms and formats
    - Timeline and deadlines
    - Exclusivity period

  Compensation:
    - Fee structure (flat, performance, hybrid)
    - Payment terms (50/50, net 30)
    - Bonus triggers
    - Expense coverage

  Rights:
    - Content ownership
    - Usage rights duration
    - Platforms for repurposing
    - Whitelisting/boosting rights

  Requirements:
    - FTC disclosure compliance
    - Approval process
    - Revision limits
    - Analytics reporting

  Protection:
    - Morality clause
    - Termination conditions
    - Non-disparagement
    - Indemnification
```

## Лучшие практики

1. **Authenticity first** — выбирайте по fit, не только по reach
2. **Long-term relationships** — амбассадоры эффективнее разовых постов
3. **Creative freedom** — дайте инфлюенсерам их голос
4. **Clear disclosure** — FTC compliance обязателен
5. **Performance tracking** — уникальные ссылки и коды
6. **Diversification** — mix разных тиров и платформ
