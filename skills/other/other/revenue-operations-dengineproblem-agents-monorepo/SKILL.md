---
name: revenue-operations
description: Эксперт RevOps. Используй для GTM стратегий, процессов продаж, CRM систем и revenue метрик.
---

# Revenue Operations Expert

Strategic expertise in aligning sales, marketing, and customer success to optimize the entire revenue engine.

## RevOps Framework

```yaml
revenue_engine:
  flow: "Marketing → SDR → AE → CS → Expansion"

  stages:
    marketing:
      input: "Traffic/Leads"
      output: "MQLs"
      metrics: ["MQL Volume", "CPL", "Channel Mix"]

    sdr:
      input: "MQLs"
      output: "SQLs"
      metrics: ["Conversion Rate", "Response Time", "Meeting Rate"]

    ae:
      input: "SQLs"
      output: "Closed Won"
      metrics: ["Win Rate", "ACV", "Sales Cycle"]

    cs:
      input: "Customers"
      output: "Retained Revenue"
      metrics: ["NRR", "Churn", "NPS"]

    expansion:
      input: "Existing Customers"
      output: "Upsell/Cross-sell"
      metrics: ["Expansion Revenue", "Attach Rate"]

core_principles:
  - "Single source of truth for data"
  - "Process standardization across teams"
  - "Technology enablement"
  - "Predictable revenue growth"
```

## GTM Strategy

```yaml
gtm_motions:
  sales_led:
    characteristics:
      - "High-touch sales process"
      - "Enterprise focus"
      - "Complex products"
    metrics:
      cac: "$10,000-50,000"
      sales_cycle: "90-180 days"
      acv: "$50,000+"
    team_structure:
      - "SDRs (outbound focus)"
      - "AEs (closers)"
      - "SEs (technical support)"
      - "CSMs (post-sale)"

  product_led:
    characteristics:
      - "Self-service onboarding"
      - "Freemium or free trial"
      - "Product drives conversion"
    metrics:
      cac: "$500-2,000"
      sales_cycle: "7-30 days"
      acv: "$1,000-20,000"
    team_structure:
      - "Growth team"
      - "Product specialists"
      - "Customer success (scaled)"

  hybrid:
    characteristics:
      - "PLG for SMB"
      - "Sales-assisted for Enterprise"
      - "Multiple price points"
    metrics:
      smb_cac: "$1,000-5,000"
      enterprise_cac: "$20,000+"
```

## Revenue Metrics

```yaml
core_metrics:
  bookings:
    arr: "Annual Recurring Revenue"
    mrr: "Monthly Recurring Revenue"
    tcv: "Total Contract Value"
    acv: "Annual Contract Value"
    formula:
      arr: "Sum of all annual contract values"
      mrr: "ARR / 12"

  growth:
    net_new_arr: "New logos + Expansion - Churn"
    nrr: "(Starting ARR + Expansion - Churn) / Starting ARR"
    gross_retention: "(Starting ARR - Churn) / Starting ARR"
    targets:
      nrr: ">110%"
      gross_retention: ">90%"

  efficiency:
    cac: "Sales & Marketing Spend / New Customers"
    ltv: "ARPU × Gross Margin × Customer Lifetime"
    ltv_cac: "LTV / CAC"
    cac_payback: "CAC / (ARPU × Gross Margin)"
    targets:
      ltv_cac: ">3:1"
      cac_payback: "<18 months"

  velocity:
    pipeline_velocity: |
      (# Opportunities × Win Rate × ACV) / Sales Cycle Days
    sales_cycle: "Days from SQL to Close"
    stage_conversion: "Opportunities moving to next stage"
```

## Process Design

### Lead Management

```yaml
lead_process:
  lead_sources:
    inbound:
      - "Website forms"
      - "Content downloads"
      - "Demo requests"
      - "Free trial signups"
    outbound:
      - "SDR prospecting"
      - "ABM campaigns"
      - "Events"
      - "Partner referrals"

  lead_scoring:
    demographic:
      company_size:
        enterprise: 30
        mid_market: 20
        smb: 10
      title:
        c_level: 25
        vp: 20
        director: 15
        manager: 10
      industry:
        target_vertical: 20
        adjacent: 10
        other: 0

    behavioral:
      demo_request: 50
      pricing_page: 30
      content_download: 10
      email_open: 5
      website_visit: 2

    threshold:
      mql: 50
      sql: 80

  routing:
    enterprise: "Named AE"
    mid_market: "Territory-based"
    smb: "Round robin"
    inbound: "5 minute response SLA"
```

### Opportunity Management

```yaml
opportunity_stages:
  stage_1_discovery:
    name: "Discovery"
    probability: "10%"
    exit_criteria:
      - "Pain identified"
      - "Budget confirmed"
      - "Timeline established"
    required_fields:
      - "Primary contact"
      - "Problem statement"
      - "Estimated deal size"

  stage_2_qualification:
    name: "Qualification"
    probability: "25%"
    exit_criteria:
      - "MEDDIC complete"
      - "Technical fit confirmed"
      - "Champion identified"
    required_fields:
      - "Decision criteria"
      - "Decision process"
      - "Competition"

  stage_3_demo:
    name: "Demo/Evaluation"
    probability: "50%"
    exit_criteria:
      - "Demo completed"
      - "Positive feedback"
      - "Next steps agreed"
    required_fields:
      - "Demo date"
      - "Attendees"
      - "Follow-up actions"

  stage_4_proposal:
    name: "Proposal"
    probability: "75%"
    exit_criteria:
      - "Proposal delivered"
      - "Pricing discussed"
      - "Contract reviewed"
    required_fields:
      - "Proposal sent date"
      - "Final pricing"
      - "Contract terms"

  stage_5_negotiation:
    name: "Negotiation"
    probability: "90%"
    exit_criteria:
      - "Terms agreed"
      - "Legal approved"
      - "Signature pending"
    required_fields:
      - "Final contract"
      - "Expected close date"

  closed_won:
    probability: "100%"
    required_fields:
      - "Contract signed"
      - "Start date"
      - "Implementation plan"
```

### MEDDIC Framework

```yaml
meddic:
  metrics:
    question: "What business results are you trying to achieve?"
    required: true
    examples:
      - "Increase revenue by 20%"
      - "Reduce costs by $500K"
      - "Improve efficiency by 30%"

  economic_buyer:
    question: "Who has budget authority?"
    required: true
    attributes:
      - "Budget holder"
      - "Final decision maker"
      - "Can approve without escalation"

  decision_criteria:
    question: "How will you evaluate solutions?"
    required: true
    categories:
      - "Technical requirements"
      - "Business requirements"
      - "Commercial terms"

  decision_process:
    question: "What is your evaluation process?"
    required: true
    elements:
      - "Steps to decision"
      - "Timeline"
      - "Stakeholders involved"

  identify_pain:
    question: "What problem are you solving?"
    required: true
    depth:
      - "Business impact"
      - "Personal impact"
      - "Urgency"

  champion:
    question: "Who will advocate internally?"
    required: true
    criteria:
      - "Has influence"
      - "Has access to EB"
      - "Wants you to win"
```

## Tech Stack Architecture

```yaml
tech_stack:
  core_systems:
    crm:
      tool: "Salesforce / HubSpot"
      purpose: "System of record"
      integrations: ["All revenue tools"]

    marketing_automation:
      tool: "Marketo / HubSpot / Pardot"
      purpose: "Lead nurture, scoring"
      integrations: ["CRM", "Website", "Email"]

    sales_engagement:
      tool: "Outreach / SalesLoft"
      purpose: "Sequences, cadences"
      integrations: ["CRM", "Email", "Calendar"]

    revenue_intelligence:
      tool: "Gong / Chorus"
      purpose: "Call recording, insights"
      integrations: ["CRM", "Calendar", "Video"]

  supporting_tools:
    data_enrichment:
      - "ZoomInfo"
      - "Clearbit"
      - "Apollo"

    analytics_bi:
      - "Tableau"
      - "Looker"
      - "Mode"

    cpq:
      - "Salesforce CPQ"
      - "DealHub"
      - "PandaDoc"

    customer_success:
      - "Gainsight"
      - "ChurnZero"
      - "Totango"

  integration_patterns:
    native: "Preferred when available"
    middleware: "Workato, Tray.io, Zapier"
    custom: "APIs for complex logic"
```

## Forecasting

```yaml
forecast_methodology:
  categories:
    commit:
      definition: "Will close this period"
      confidence: ">90%"
      criteria:
        - "Verbal commitment"
        - "Contract in legal"
        - "No blockers"

    best_case:
      definition: "Could close with effort"
      confidence: "60-90%"
      criteria:
        - "Proposal accepted"
        - "Active negotiation"
        - "Timeline aligned"

    pipeline:
      definition: "May close this period"
      confidence: "30-60%"
      criteria:
        - "In evaluation"
        - "Budget confirmed"
        - "Timeline possible"

  weighted_pipeline:
    formula: "Sum(Deal Value × Stage Probability)"
    adjustments:
      - "Historical win rates by rep"
      - "Deal age penalties"
      - "Competition presence"

  forecast_accuracy:
    target: "Within 10% of actual"
    measurement: "Commit vs Closed Won"
    cadence: "Weekly review"
```

## Capacity Planning

```yaml
capacity_model:
  sdr:
    activities_per_day:
      calls: 60
      emails: 100
      linkedin: 30
    output_per_month:
      meetings: 15
      sqls: 10
    quota: "$150K pipeline/month"
    ramp_time: "3 months"

  ae:
    capacity:
      active_opportunities: 25
      new_per_month: 8
    quota: "$1.2M ARR/year"
    ramp_time: "6 months"
    average_deal_size: "$50K"
    win_rate: "25%"

  cs:
    book_size:
      smb: "150 accounts"
      mid_market: "50 accounts"
      enterprise: "15 accounts"
    nrr_target: "115%"

  headcount_planning:
    formula: |
      Required Reps =
        (Revenue Target / Quota) ×
        (1 / (1 - Attrition Rate)) ×
        (1 + Ramp Adjustment)
    example:
      revenue_target: "$20M"
      quota: "$1M"
      attrition: "20%"
      ramp_factor: "1.25"
      required_reps: "31"
```

## Reporting Dashboard

```yaml
executive_dashboard:
  weekly_metrics:
    - "Pipeline created"
    - "Meetings booked"
    - "Deals won/lost"
    - "Forecast update"

  monthly_metrics:
    - "Bookings vs target"
    - "NRR"
    - "Win rate trends"
    - "Sales cycle analysis"

  quarterly_metrics:
    - "ARR growth"
    - "CAC trends"
    - "Capacity utilization"
    - "Funnel conversion"

sales_dashboard:
  individual_metrics:
    - "Pipeline coverage"
    - "Activity metrics"
    - "Stage progression"
    - "Deal velocity"

  team_metrics:
    - "Leaderboard"
    - "Quota attainment"
    - "Win/loss analysis"
```

## Process Optimization

```yaml
optimization_areas:
  lead_response:
    current: "30 min average"
    target: "<5 min"
    impact: "2x conversion"
    solution: "Auto-routing + alerts"

  pipeline_coverage:
    current: "2.5x"
    target: "4x"
    impact: "Forecast accuracy"
    solution: "SDR capacity + ABM"

  win_rate:
    current: "22%"
    target: "30%"
    impact: "+36% bookings"
    solution: "Deal qualification + coaching"

  sales_cycle:
    current: "120 days"
    target: "90 days"
    impact: "+33% velocity"
    solution: "Multi-threading + mutual action plans"
```

## Лучшие практики

1. **Single source of truth** — CRM как единый источник данных
2. **Process before tools** — сначала процесс, потом автоматизация
3. **Data hygiene** — качество данных критично
4. **Cross-functional alignment** — Sales + Marketing + CS
5. **Predictable forecasting** — accuracy >90%
6. **Continuous optimization** — итерации на основе данных
