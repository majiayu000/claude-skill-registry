---
name: account-based-marketing-agent
description: AI агент для ABM. Используй для автоматизации ABM кампаний и персонализации outreach.
---

# Account-Based Marketing Agent

AI-powered автоматизация и оркестрация ABM кампаний для B2B маркетинга.

## Core Capabilities

### Agent Functions

```yaml
abm_agent_capabilities:
  account_intelligence:
    - Company research automation
    - Technographic data gathering
    - Intent signal detection
    - Buying committee mapping
    - Competitive intelligence

  personalization:
    - Dynamic content generation
    - Account-specific messaging
    - Multi-stakeholder personalization
    - Journey orchestration

  campaign_automation:
    - Multi-channel coordination
    - Timing optimization
    - A/B test management
    - Budget allocation

  analytics:
    - Engagement scoring
    - Account health tracking
    - Pipeline attribution
    - ROI calculation
```

---

## Account Selection & Tiering

### ICP Scoring Model

```yaml
ideal_customer_profile:
  firmographic_criteria:
    company_size:
      tier_1: "1000+ employees"
      tier_2: "200-999 employees"
      tier_3: "50-199 employees"
      weight: 25

    industry:
      primary: ["SaaS", "FinTech", "Healthcare IT"]
      secondary: ["E-commerce", "Manufacturing"]
      weight: 20

    revenue:
      tier_1: "$100M+"
      tier_2: "$20M-$100M"
      tier_3: "$5M-$20M"
      weight: 20

  technographic_criteria:
    tech_stack_fit:
      must_have: ["Salesforce", "HubSpot"]
      nice_to_have: ["Segment", "Snowflake"]
      weight: 15

    current_solutions:
      competitor_user: "+10 points"
      legacy_system: "+5 points"
      weight: 10

  behavioral_signals:
    intent_data:
      high_intent_topics: "+15 points"
      competitor_research: "+10 points"
      weight: 10
```

### Account Tiering

```yaml
account_tiers:
  tier_1_strategic:
    count: "10-25 accounts"
    characteristics:
      - Perfect ICP fit
      - High revenue potential ($500K+ ACV)
      - Known buying intent
      - Executive relationships possible

    engagement_model:
      - Dedicated account team
      - Custom content creation
      - Executive-to-executive outreach
      - In-person events/dinners
      - Annual budget: "$10-50K per account"

  tier_2_target:
    count: "50-100 accounts"
    characteristics:
      - Strong ICP fit
      - Medium revenue potential ($100-500K ACV)
      - Some intent signals

    engagement_model:
      - Shared account resources
      - Semi-custom content
      - Multi-channel campaigns
      - Virtual events
      - Annual budget: "$2-10K per account"

  tier_3_scale:
    count: "200-500 accounts"
    characteristics:
      - Good ICP fit
      - Lower revenue potential ($25-100K ACV)

    engagement_model:
      - Automated campaigns
      - Industry-personalized content
      - Programmatic advertising
      - Annual budget: "$500-2K per account"
```

---

## Buying Committee Mapping

### Stakeholder Identification

```yaml
buying_committee:
  champion:
    role: "Day-to-day user who benefits most"
    typical_titles:
      - "Manager"
      - "Director"
      - "Team Lead"
    messaging_focus:
      - Productivity gains
      - Pain point solutions
      - Ease of implementation

  decision_maker:
    role: "Has budget authority"
    typical_titles:
      - "VP"
      - "C-level"
      - "Head of"
    messaging_focus:
      - ROI and business impact
      - Strategic alignment
      - Risk mitigation

  technical_evaluator:
    role: "Assesses technical fit"
    typical_titles:
      - "IT Director"
      - "Solutions Architect"
      - "Security Lead"
    messaging_focus:
      - Integration capabilities
      - Security and compliance
      - Technical specifications

  influencer:
    role: "Shapes opinion but doesn't decide"
    typical_titles:
      - "Consultant"
      - "Board member"
      - "Industry analyst"
    messaging_focus:
      - Industry trends
      - Competitive positioning
      - Thought leadership

  blocker:
    role: "May oppose the purchase"
    typical_titles:
      - "Procurement"
      - "Legal"
      - "Finance"
    messaging_focus:
      - Risk mitigation
      - Compliance
      - Vendor stability
```

### Contact Discovery Automation

```python
# Example: LinkedIn + Intent data enrichment
def discover_buying_committee(account_domain: str) -> dict:
    """
    Automated buying committee discovery
    """
    contacts = []

    # Step 1: LinkedIn Sales Navigator search
    linkedin_results = linkedin_api.search_people(
        company_domain=account_domain,
        titles=[
            "VP Marketing", "CMO", "Head of Marketing",
            "VP Sales", "CRO", "Head of Revenue",
            "VP IT", "CTO", "Head of Technology"
        ],
        seniority=["Director", "VP", "C-Level"]
    )

    # Step 2: Enrich with intent data
    for contact in linkedin_results:
        intent_score = intent_provider.get_contact_intent(
            email=contact.get("email"),
            topics=["marketing automation", "ABM", "sales engagement"]
        )

        contact["intent_score"] = intent_score
        contact["role_classification"] = classify_buyer_role(contact["title"])

    # Step 3: Prioritize by intent + seniority
    contacts = sorted(
        linkedin_results,
        key=lambda x: (x["intent_score"], x["seniority_rank"]),
        reverse=True
    )

    return {
        "account": account_domain,
        "buying_committee": contacts[:10],
        "champion_candidates": [c for c in contacts if c["role_classification"] == "champion"],
        "decision_makers": [c for c in contacts if c["role_classification"] == "decision_maker"]
    }
```

---

## Intent Signal Processing

### Intent Data Sources

```yaml
intent_signals:
  first_party:
    website_behavior:
      - Page visits (especially pricing, demo, comparison)
      - Time on site
      - Return visits
      - Content downloads
      - Webinar registrations

    email_engagement:
      - Open rates
      - Click-through rates
      - Reply rates
      - Forward rates

    product_signals:
      - Free trial signup
      - Feature usage
      - Support tickets
      - API calls

  third_party:
    research_intent:
      provider: "Bombora, G2, TrustRadius"
      signals:
        - Topic surge
        - Competitor research
        - Category research

    hiring_signals:
      provider: "LinkedIn, job boards"
      signals:
        - Relevant job postings
        - Team expansion
        - New leadership

    technographic_changes:
      provider: "BuiltWith, HG Insights"
      signals:
        - New tech adoption
        - Contract renewals approaching
        - Vendor changes
```

### Intent Score Calculation

```python
def calculate_account_intent_score(account_id: str) -> dict:
    """
    Multi-signal intent scoring
    """
    scores = {
        "first_party": 0,
        "third_party": 0,
        "composite": 0
    }

    # First-party signals (weight: 60%)
    website_score = get_website_engagement_score(account_id)  # 0-100
    email_score = get_email_engagement_score(account_id)       # 0-100
    product_score = get_product_engagement_score(account_id)   # 0-100

    scores["first_party"] = (
        website_score * 0.4 +
        email_score * 0.3 +
        product_score * 0.3
    )

    # Third-party signals (weight: 40%)
    topic_surge = get_bombora_topic_surge(account_id)          # 0-100
    hiring_signals = get_hiring_signal_score(account_id)       # 0-100
    tech_changes = get_technographic_change_score(account_id)  # 0-100

    scores["third_party"] = (
        topic_surge * 0.5 +
        hiring_signals * 0.3 +
        tech_changes * 0.2
    )

    # Composite score
    scores["composite"] = (
        scores["first_party"] * 0.6 +
        scores["third_party"] * 0.4
    )

    # Classify intent level
    if scores["composite"] >= 80:
        scores["intent_level"] = "hot"
        scores["recommended_action"] = "immediate_sales_outreach"
    elif scores["composite"] >= 60:
        scores["intent_level"] = "warm"
        scores["recommended_action"] = "accelerated_nurture"
    elif scores["composite"] >= 40:
        scores["intent_level"] = "engaged"
        scores["recommended_action"] = "standard_nurture"
    else:
        scores["intent_level"] = "cold"
        scores["recommended_action"] = "awareness_campaign"

    return scores
```

---

## Campaign Orchestration

### Multi-Channel Playbook

```yaml
abm_playbook:
  name: "Enterprise Account Activation"
  trigger: "Account reaches intent score >= 70"
  duration: "90 days"

  week_1_2:
    goal: "Awareness and research facilitation"
    channels:
      linkedin_ads:
        - Sponsored content to buying committee
        - Thought leadership pieces
        - Budget: "$500/account"

      display_retargeting:
        - Account-based display ads
        - Case study promotion
        - Budget: "$300/account"

      direct_mail:
        - Research report + handwritten note
        - To: Champion and Decision Maker
        - Cost: "$50/piece"

  week_3_4:
    goal: "Engagement and education"
    channels:
      email_sequence:
        - 4-email nurture sequence
        - Personalized by role
        - Content: Industry insights

      linkedin_outreach:
        - SDR connection requests
        - Value-first messaging
        - Target: 5 contacts per account

      webinar_invitation:
        - Industry-specific webinar
        - Executive speaker

  week_5_6:
    goal: "Conversion push"
    channels:
      personalized_video:
        - Custom video for champion
        - Demo of relevant features

      executive_outreach:
        - AE reaches decision maker
        - Reference customer intro

      gifting:
        - High-value gift to decision maker
        - Budget: "$100-250"

  week_7_12:
    goal: "Deal progression support"
    channels:
      sales_enablement:
        - Custom ROI calculator
        - Business case template
        - Reference calls

      expansion_content:
        - Additional stakeholder content
        - Technical documentation
        - Security questionnaire support
```

### Campaign Automation Rules

```yaml
automation_rules:
  intent_spike_response:
    trigger: "Intent score increases >20 points in 7 days"
    actions:
      - notify_account_owner
      - add_to_accelerated_sequence
      - increase_ad_spend_2x
      - create_sales_task_urgent

  champion_engagement:
    trigger: "Champion visits pricing page 2+ times"
    actions:
      - send_personalized_pricing_email
      - assign_sdr_call_task
      - add_decision_maker_to_parallel_sequence

  multi_stakeholder_activity:
    trigger: "3+ contacts from account active in 7 days"
    actions:
      - create_opportunity_if_none
      - send_team_briefing_to_ae
      - launch_full_buying_committee_sequence

  competitor_research:
    trigger: "Account researching competitor topics"
    actions:
      - send_competitive_comparison_content
      - add_to_competitive_ad_campaign
      - alert_account_owner
```

---

## Personalization Engine

### Dynamic Content Generation

```yaml
personalization_variables:
  account_level:
    - Company name
    - Industry
    - Company size
    - Recent news
    - Technology stack
    - Competitors used

  contact_level:
    - First name
    - Title/role
    - Department
    - Seniority
    - LinkedIn activity
    - Content interests

  behavioral:
    - Pages visited
    - Content downloaded
    - Emails engaged
    - Meeting history

content_templates:
  email_subject_lines:
    champion:
      - "[Company] + [Our Company]: solving [pain point]"
      - "[First name], quick question about [topic they researched]"

    decision_maker:
      - "How [Similar Company] achieved [result]"
      - "[First name], ROI of [solution category] at [Company]"

  email_body_frameworks:
    pain_point_led:
      opening: "I noticed [Company] is [signal/news/hiring]. Many [industry] companies face [pain point] when [situation]."
      bridge: "We've helped [reference company] solve this by [solution approach]."
      cta: "Worth a 15-minute call to see if we can help [Company] similarly?"

    insight_led:
      opening: "Based on [research/data point], [industry] companies are [trend]."
      bridge: "[Company] is well-positioned to [opportunity] by [approach]."
      cta: "I'd love to share how we're helping companies like [reference] capitalize on this."
```

---

## Engagement Scoring

### Account Engagement Model

```yaml
engagement_scoring:
  email_engagement:
    open: 1
    click: 3
    reply: 10
    meeting_booked: 25

  website_engagement:
    page_view: 1
    pricing_page: 5
    demo_page: 7
    feature_page: 3
    blog_post: 1
    case_study: 4

  content_engagement:
    whitepaper_download: 5
    webinar_registration: 7
    webinar_attendance: 15
    video_watch_50_percent: 3
    video_watch_100_percent: 5

  ad_engagement:
    impression: 0.01
    click: 2

  sales_engagement:
    meeting_held: 50
    proposal_sent: 75
    verbal_commit: 100

  score_thresholds:
    cold: "0-25"
    engaged: "26-50"
    marketing_qualified: "51-100"
    sales_qualified: "101+"
```

---

## Attribution & Analytics

### Multi-Touch Attribution

```yaml
attribution_models:
  first_touch:
    description: "100% credit to first interaction"
    use_case: "Understanding awareness channels"

  last_touch:
    description: "100% credit to last interaction before conversion"
    use_case: "Understanding closing channels"

  linear:
    description: "Equal credit to all touchpoints"
    use_case: "Balanced view of customer journey"

  time_decay:
    description: "More credit to recent touchpoints"
    use_case: "Focus on conversion drivers"

  position_based:
    description: "40% first, 40% last, 20% middle"
    use_case: "Balanced awareness + conversion focus"

  data_driven:
    description: "ML-based attribution"
    use_case: "Most accurate but requires volume"
```

### ABM Metrics Dashboard

```yaml
abm_metrics:
  account_coverage:
    - "% of target accounts reached"
    - "% of buying committee engaged"
    - "Average contacts engaged per account"

  engagement_metrics:
    - "Account engagement score trend"
    - "Channel engagement breakdown"
    - "Content performance by persona"

  pipeline_metrics:
    - "Target account pipeline generated"
    - "Average deal size (ABM vs non-ABM)"
    - "Win rate (ABM vs non-ABM)"
    - "Sales cycle length (ABM vs non-ABM)"

  efficiency_metrics:
    - "Cost per engaged account"
    - "Cost per opportunity"
    - "Marketing influenced pipeline"
    - "ABM ROI"
```

---

## Integration Architecture

### Tech Stack Integration

```yaml
abm_tech_stack:
  crm:
    primary: "Salesforce"
    sync:
      - Account scores
      - Contact engagement
      - Campaign membership
      - Intent signals

  marketing_automation:
    primary: "Marketo / HubSpot"
    sync:
      - Lead scoring
      - Email campaigns
      - Landing pages
      - Form submissions

  abm_platform:
    options: ["Demandbase", "6sense", "Terminus"]
    capabilities:
      - Account identification
      - Intent data
      - Advertising orchestration
      - Analytics

  sales_engagement:
    options: ["Outreach", "Salesloft"]
    sync:
      - Sequence enrollment
      - Activity logging
      - Meeting scheduling

  intent_data:
    providers: ["Bombora", "G2", "TrustRadius"]
    sync:
      - Topic surge scores
      - Research signals
      - Review activity

  enrichment:
    providers: ["ZoomInfo", "Clearbit", "Apollo"]
    data:
      - Contact information
      - Technographics
      - Firmographics
```

---

## Лучшие практики

1. **Качество важнее количества** — лучше 50 хорошо проработанных аккаунтов чем 500 поверхностных
2. **Sales и Marketing alignment** — совместное определение ICP и целевых аккаунтов
3. **Персонализация по ролям** — разный messaging для разных stakeholders
4. **Multi-channel orchestration** — координируй все каналы в единую journey
5. **Intent-based prioritization** — фокусируйся на аккаунтах с высоким intent
6. **Измеряй account engagement, не только leads** — ABM metric отличается от demand gen
7. **Content по стадиям воронки** — awareness → consideration → decision
8. **Регулярный review target accounts** — пересматривай список каждый квартал
