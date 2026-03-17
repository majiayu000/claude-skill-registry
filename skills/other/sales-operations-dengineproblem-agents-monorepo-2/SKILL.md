---
name: sales-operations
description: Эксперт Sales Ops. Используй для процессов продаж, CRM, forecasting и sales analytics.
---

# Sales Operations Expert

Operational excellence in sales process design, systems administration, and analytics.

## Sales Process Design

```yaml
sales_stages:
  stage_0_prospecting:
    name: "Prospecting"
    owner: "SDR"
    probability: "0%"
    activities:
      - "Account research"
      - "Contact identification"
      - "Initial outreach"
    exit_criteria:
      - "Meeting scheduled"
      - "Interest confirmed"
    required_fields:
      - "Lead source"
      - "ICP score"

  stage_1_discovery:
    name: "Discovery"
    owner: "AE"
    probability: "10%"
    activities:
      - "Discovery call"
      - "Needs assessment"
      - "Stakeholder mapping"
    exit_criteria:
      - "Pain identified and quantified"
      - "Budget range confirmed"
      - "Timeline established"
      - "Key stakeholders identified"
    required_fields:
      - "Primary contact"
      - "Problem statement"
      - "Budget range"
      - "Expected close date"

  stage_2_qualification:
    name: "Qualification"
    owner: "AE"
    probability: "25%"
    activities:
      - "MEDDIC completion"
      - "Technical fit assessment"
      - "Champion development"
    exit_criteria:
      - "MEDDIC 80% complete"
      - "Technical requirements documented"
      - "Champion identified"
      - "Competition mapped"
    required_fields:
      - "Decision criteria"
      - "Decision process"
      - "Competitors"
      - "Champion name"

  stage_3_demo:
    name: "Demo/Evaluation"
    owner: "AE + SE"
    probability: "50%"
    activities:
      - "Product demonstration"
      - "Technical deep dive"
      - "POC/trial if needed"
    exit_criteria:
      - "Demo completed successfully"
      - "Technical approval received"
      - "Positive feedback documented"
    required_fields:
      - "Demo date"
      - "Attendees"
      - "Technical requirements"
      - "POC scope (if applicable)"

  stage_4_proposal:
    name: "Proposal"
    owner: "AE"
    probability: "75%"
    activities:
      - "Proposal creation"
      - "Pricing presentation"
      - "Contract review"
    exit_criteria:
      - "Proposal delivered"
      - "Pricing discussed"
      - "No major objections"
    required_fields:
      - "Proposal sent date"
      - "Proposed amount"
      - "Contract terms"
      - "Discount (if any)"

  stage_5_negotiation:
    name: "Negotiation"
    owner: "AE"
    probability: "90%"
    activities:
      - "Term negotiation"
      - "Legal review"
      - "Final approvals"
    exit_criteria:
      - "Terms agreed"
      - "Legal approved"
      - "Signature pending"
    required_fields:
      - "Final contract"
      - "Expected signature date"
      - "Approvers"

  stage_6_closed_won:
    name: "Closed Won"
    probability: "100%"
    required_fields:
      - "Signed contract"
      - "Start date"
      - "Implementation owner"
```

## CRM Management

```yaml
crm_administration:
  data_model:
    objects:
      lead:
        purpose: "Pre-qualified prospects"
        key_fields:
          - "Name, Company, Email"
          - "Lead source"
          - "Lead score"
          - "Status"
        lifecycle: "Create → Qualify → Convert to Contact/Opp"

      contact:
        purpose: "Individual people"
        key_fields:
          - "Name, Title, Email"
          - "Account relationship"
          - "Role in deals"
        relationships: "Account, Opportunities"

      account:
        purpose: "Companies"
        key_fields:
          - "Name, Industry, Size"
          - "ICP score"
          - "Owner"
          - "Tier"
        relationships: "Contacts, Opportunities"

      opportunity:
        purpose: "Potential deals"
        key_fields:
          - "Name, Amount, Stage"
          - "Close date"
          - "Probability"
          - "Owner"
        relationships: "Account, Contacts, Products"

  data_hygiene:
    rules:
      duplicate_prevention:
        - "Email uniqueness on Contacts"
        - "Domain matching for Accounts"
        - "Automated merge suggestions"

      required_fields:
        - "Enforce by stage"
        - "Validation rules"
        - "Picklist standardization"

      data_quality:
        - "Weekly duplicate reports"
        - "Monthly enrichment updates"
        - "Quarterly data audits"

  automation_rules:
    lead_routing:
      criteria:
        - "Territory (geography)"
        - "Company size"
        - "Lead score"
        - "Round robin for overflow"
      sla: "5 minutes to assignment"

    opportunity_creation:
      trigger: "Lead converted"
      actions:
        - "Create opportunity"
        - "Copy MEDDIC fields"
        - "Assign to AE"
        - "Create tasks"

    stage_progression:
      validation:
        - "Required fields complete"
        - "Exit criteria met"
        - "Manager approval (if needed)"
```

## Forecasting

```yaml
forecast_methodology:
  categories:
    commit:
      definition: "Will close this period"
      confidence: ">90%"
      criteria:
        - "Verbal yes"
        - "Contract in legal"
        - "No blockers"
      weighting: "100%"

    best_case:
      definition: "Could close with effort"
      confidence: "60-90%"
      criteria:
        - "Proposal accepted"
        - "Negotiating terms"
        - "Timeline aligned"
      weighting: "70%"

    pipeline:
      definition: "May close this period"
      confidence: "30-60%"
      criteria:
        - "Active evaluation"
        - "Budget confirmed"
        - "Possible timeline"
      weighting: "40%"

    upside:
      definition: "Low probability this period"
      confidence: "<30%"
      criteria:
        - "Early stage"
        - "Timeline uncertain"
        - "Budget not confirmed"
      weighting: "10%"

  forecast_calculation:
    weighted: |
      Forecast =
        (Commit × 100%) +
        (Best Case × 70%) +
        (Pipeline × 40%) +
        (Upside × 10%)

    coverage: |
      Coverage Ratio = Total Pipeline / Quota
      Target: 3-4x coverage

  forecast_cadence:
    weekly:
      - "Rep submits forecast (Monday)"
      - "Manager review (Tuesday)"
      - "Leadership call (Wednesday)"
      - "Update actions (Thursday-Friday)"

    monthly:
      - "Week 1: Forecast accuracy review"
      - "Week 2: Mid-month adjust"
      - "Week 3: Final push planning"
      - "Week 4: Close month"

  accuracy_metrics:
    calculation: "Actual / Forecast"
    targets:
      acceptable: "85-115%"
      good: "90-110%"
      excellent: "95-105%"
    tracking: "Month over month trend"
```

## Pipeline Analytics

```yaml
pipeline_metrics:
  volume:
    total_pipeline: "Sum of all open opportunities"
    new_pipeline: "Created this period"
    pipeline_growth: "(Current - Previous) / Previous"

  velocity:
    formula: |
      (# Opps × Win Rate × Avg Deal Size) / Sales Cycle
    components:
      opportunities: "Count of qualified opps"
      win_rate: "Won / (Won + Lost)"
      deal_size: "Average closed won"
      cycle_time: "Days from creation to close"

  conversion:
    stage_conversion: "Moved to next stage / Started in stage"
    lead_to_opp: "Opportunities / Leads"
    opp_to_won: "Won / All closed"

  quality:
    average_deal_size: "Sum(Amount) / Count(Won)"
    discount_rate: "Average discount given"
    sales_cycle: "Average days to close"

pipeline_analysis:
  by_segment:
    - "By rep/team"
    - "By territory"
    - "By product"
    - "By source"

  trending:
    - "Pipeline created over time"
    - "Stage velocity trends"
    - "Win rate by cohort"
    - "Deal size trends"

  health_checks:
    - "Aging deals (no activity 14+ days)"
    - "Stalled opportunities"
    - "Close date slippage"
    - "Coverage by segment"
```

## Deal Desk Operations

```yaml
deal_desk:
  approval_matrix:
    standard_deal:
      criteria: "Within guidelines"
      approver: "AE manager"
      turnaround: "Same day"

    non_standard_pricing:
      criteria: "10-20% discount"
      approver: "Sales Director"
      turnaround: "24 hours"

    strategic_deal:
      criteria: ">20% discount or custom terms"
      approver: "VP Sales + Finance"
      turnaround: "48 hours"

    enterprise_deal:
      criteria: ">$100K or multi-year"
      approver: "CRO"
      turnaround: "48-72 hours"

  pricing_guidelines:
    discount_authority:
      ae: "Up to 10%"
      manager: "Up to 15%"
      director: "Up to 20%"
      vp: "Up to 25%"
      cro: "Unlimited"

    discount_justification:
      required_for:
        - "Any discount >10%"
        - "Custom payment terms"
        - "Multi-year deals"
      documentation:
        - "Competitive pressure"
        - "Strategic value"
        - "Reference potential"

  contract_management:
    templates:
      - "Standard subscription"
      - "Enterprise license"
      - "Professional services"
      - "NDA"
      - "MSA + Order Form"

    legal_review:
      standard: "Pre-approved, no review"
      modified: "1-2 business days"
      custom: "3-5 business days"

    signature_process:
      - "DocuSign/PandaDoc"
      - "Automated routing"
      - "Counter-signature SLA"
      - "Contract storage"
```

## Performance Analytics

```yaml
sales_dashboards:
  executive:
    metrics:
      - "Revenue vs target"
      - "Pipeline coverage"
      - "Win rate trend"
      - "Forecast accuracy"
      - "Headcount vs plan"
    refresh: "Daily"

  manager:
    metrics:
      - "Team attainment"
      - "Rep pipeline health"
      - "Activity metrics"
      - "Deal progression"
      - "Coaching opportunities"
    refresh: "Daily"

  individual:
    metrics:
      - "Personal attainment"
      - "Pipeline status"
      - "Activity tracking"
      - "Deal stages"
      - "Commission forecast"
    refresh: "Real-time"

rep_performance:
  quota_attainment:
    calculation: "Closed Won / Quota"
    targets:
      ramp: "50% (months 1-3)"
      full: "100%"
      stretch: "120%"

  activity_metrics:
    calls: "Dials per day"
    meetings: "Meetings held"
    proposals: "Proposals sent"
    demos: "Demos delivered"

  quality_metrics:
    win_rate: "Won / All closed"
    avg_deal_size: "Revenue / Won deals"
    sales_cycle: "Days to close"
    discount_rate: "Average discount"

  leading_indicators:
    pipeline_coverage: "Pipeline / Remaining quota"
    opportunity_creation: "New opps per month"
    stage_progression: "Velocity through stages"
```

## Territory & Quota

```yaml
territory_management:
  models:
    geographic:
      basis: "Region, country, state"
      pros: "Simple, clear ownership"
      cons: "Uneven potential"

    named_accounts:
      basis: "Specific account list"
      pros: "Focus on key accounts"
      cons: "Coverage gaps"

    segment:
      basis: "Company size, industry"
      pros: "Specialization"
      cons: "Complexity"

    hybrid:
      basis: "Combination of above"
      pros: "Balanced coverage"
      cons: "Administration overhead"

  balancing:
    factors:
      - "Total addressable market"
      - "Account potential"
      - "Historical performance"
      - "Rep capacity"
      - "Travel requirements"

    metrics:
      - "Accounts per rep"
      - "Potential revenue"
      - "Win rate by territory"

quota_setting:
  methodology:
    bottom_up:
      calculation: "Sum of rep quotas"
      basis: "Territory potential"

    top_down:
      calculation: "Company target / Reps"
      basis: "Growth objectives"

    blended:
      calculation: "Average of both"
      adjustments: "Territory factors"

  factors:
    - "Historical performance"
    - "Territory potential"
    - "Market growth"
    - "Product launches"
    - "Ramp time"
    - "Seasonality"

  quota_types:
    bookings: "New ARR"
    revenue: "Recognized revenue"
    pipeline: "Pipeline generated"
    activity: "Meetings, demos"
```

## Лучшие практики

1. **Process before tools** — определи процесс, потом автоматизируй
2. **Data quality first** — мусор на входе = мусор на выходе
3. **Inspect what you expect** — регулярные ревью pipeline
4. **Forecast accuracy focus** — точность > оптимизм
5. **Enable, don't police** — помогай продавать, не усложняй
6. **Continuous improvement** — итерации на основе данных
