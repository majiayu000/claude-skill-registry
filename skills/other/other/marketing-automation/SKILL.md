---
name: marketing-automation
description: Эксперт по автоматизации маркетинга. Используй для настройки HubSpot, Marketo, email sequences, lead scoring и workflows.
---

# Marketing Automation Expert

Deep expertise in marketing automation strategy and implementation across major MarTech platforms.

## Core Platforms

### Platform Comparison

| Platform | Best For | Price Range | Complexity |
|----------|----------|-------------|------------|
| HubSpot | SMB to Enterprise | $$$-$$$$ | Medium |
| Marketo | Enterprise B2B | $$$$ | High |
| Pardot | Salesforce users | $$$$ | Medium-High |
| ActiveCampaign | SMB | $-$$ | Low-Medium |
| Eloqua | Enterprise | $$$$$ | High |
| Mailchimp | Small business | $-$$ | Low |

### Selection Criteria

```yaml
platform_selection:
  considerations:
    budget:
      - "License cost per user/contact"
      - "Implementation costs"
      - "Ongoing maintenance"
      - "Training requirements"

    technical_fit:
      - "CRM integration capabilities"
      - "API availability"
      - "Data migration complexity"
      - "Security requirements"

    business_needs:
      - "Email volume"
      - "Workflow complexity"
      - "Reporting depth"
      - "Multi-channel needs"
      - "Personalization requirements"
```

## Lead Scoring Framework

### Scoring Model Design

```yaml
lead_scoring_model:
  overview:
    purpose: "Prioritize leads for sales follow-up"
    threshold: 100 # MQL threshold
    decay: "Reduce 10 points after 30 days of inactivity"

  behavioral_scoring:
    high_intent:
      - action: "Request demo"
        points: 50
        category: "Bottom funnel"

      - action: "Pricing page visit"
        points: 30
        category: "Bottom funnel"

      - action: "Case study download"
        points: 25
        category: "Middle funnel"

    engagement:
      - action: "Email open"
        points: 1
        max_per_day: 3

      - action: "Email click"
        points: 3
        max_per_day: 5

      - action: "Webinar registration"
        points: 15

      - action: "Webinar attendance"
        points: 25

      - action: "Blog visit"
        points: 1
        max_per_day: 5

      - action: "Content download"
        points: 10

    negative_signals:
      - action: "Unsubscribe"
        points: -30

      - action: "Email bounce"
        points: -20

      - action: "Spam complaint"
        points: -100

      - action: "30 days no engagement"
        points: -10

  demographic_scoring:
    company_size:
      - range: "1-10"
        points: 5
      - range: "11-50"
        points: 10
      - range: "51-200"
        points: 15
      - range: "201-1000"
        points: 20
      - range: "1000+"
        points: 25

    job_title:
      - level: "C-Level"
        points: 25
      - level: "VP"
        points: 20
      - level: "Director"
        points: 15
      - level: "Manager"
        points: 10
      - level: "Individual Contributor"
        points: 5

    industry:
      - industry: "Target industry"
        points: 20
      - industry: "Adjacent industry"
        points: 10
      - industry: "Non-target"
        points: 0

    geography:
      - region: "Primary market"
        points: 15
      - region: "Secondary market"
        points: 10
      - region: "Tertiary market"
        points: 5
```

### Lead Grading

```yaml
lead_grading:
  grades:
    A:
      description: "Ideal customer profile match"
      criteria:
        - "Decision maker title"
        - "Target company size"
        - "Target industry"
        - "Target geography"

    B:
      description: "Good fit with minor gaps"
      criteria:
        - "3 of 4 ICP criteria met"
        - "Or influencer at A company"

    C:
      description: "Moderate fit"
      criteria:
        - "2 of 4 ICP criteria met"
        - "Or adjacent market"

    D:
      description: "Poor fit"
      criteria:
        - "1 or fewer ICP criteria"
        - "Or disqualifying factors"

  sales_routing:
    A1_A2: "Immediate sales follow-up"
    A3_B1: "Sales follow-up within 24 hours"
    B2_B3: "Nurture then sales handoff"
    C_any: "Continue nurturing"
    D_any: "Exclude from sales"
```

## Email Nurture Programs

### Welcome Series

```yaml
welcome_sequence:
  name: "New Subscriber Welcome"
  trigger: "Form submission - Newsletter signup"
  duration: "2 weeks"

  emails:
    - email: 1
      timing: "Immediately"
      subject: "Welcome to [Company]! Here's what to expect"
      content:
        - "Thank you message"
        - "What they'll receive"
        - "Quick win resource"
        - "Social proof"
      cta: "Download [Quick Win Resource]"

    - email: 2
      timing: "Day 2"
      subject: "The #1 challenge [personas] face"
      content:
        - "Pain point identification"
        - "How you solve it"
        - "Brief case study"
      cta: "Read full case study"

    - email: 3
      timing: "Day 4"
      subject: "How [Company] helps [target outcome]"
      content:
        - "Product/service overview"
        - "Key benefits"
        - "Customer results"
      cta: "See how it works"

    - email: 4
      timing: "Day 7"
      subject: "[First Name], here's your exclusive resource"
      content:
        - "High-value gated content"
        - "Exclusive to subscribers"
        - "Addresses key challenge"
      cta: "Download now"

    - email: 5
      timing: "Day 10"
      subject: "Questions? We're here to help"
      content:
        - "Invite questions"
        - "Offer personalized help"
        - "Contact options"
      cta: "Schedule a call"

    - email: 6
      timing: "Day 14"
      subject: "What would you like to learn about?"
      content:
        - "Preference center"
        - "Topic selection"
        - "Frequency options"
      cta: "Update preferences"

  exit_conditions:
    - "Demo requested"
    - "Sales conversation started"
    - "Unsubscribe"
```

### Lead Nurture Program

```yaml
lead_nurture:
  name: "MQL Nurture"
  trigger: "Lead score reaches 50 but below 100"
  goal: "Move to MQL (score 100+)"

  tracks:
    awareness:
      qualification: "Score 50-69"
      content_focus: "Educational, industry trends"
      cadence: "2 emails per week"

      sequence:
        - "Industry trend report"
        - "How-to guide"
        - "Expert webinar invite"
        - "Comparison guide"
        - "Quiz/assessment"

    consideration:
      qualification: "Score 70-89"
      content_focus: "Solution-oriented, use cases"
      cadence: "2-3 emails per week"

      sequence:
        - "Use case deep dive"
        - "ROI calculator"
        - "Product webinar invite"
        - "Customer case study"
        - "Feature comparison"

    decision:
      qualification: "Score 90-99"
      content_focus: "Conversion-focused"
      cadence: "3 emails per week"

      sequence:
        - "Free trial offer"
        - "Demo scheduling"
        - "Competitive comparison"
        - "Implementation guide"
        - "Limited time offer"

  personalization:
    by_industry:
      - "Industry-specific case studies"
      - "Relevant statistics"
      - "Industry terminology"

    by_role:
      - "Role-specific benefits"
      - "Relevant features"
      - "Peer testimonials"

    by_behavior:
      - "Recently viewed content"
      - "Download history"
      - "Website activity"
```

### Re-engagement Campaign

```yaml
reengagement_campaign:
  name: "Win-Back Campaign"
  trigger: "No email engagement for 90 days"

  sequence:
    - email: 1
      timing: "Day 0"
      subject: "We miss you, [First Name]!"
      content:
        - "Acknowledge absence"
        - "Highlight what's new"
        - "Compelling offer"
      cta: "See what's new"

    - email: 2
      timing: "Day 5"
      subject: "Is this goodbye?"
      content:
        - "Direct question about interest"
        - "Easy opt-down option"
        - "Best content highlight"
      cta: "Stay subscribed"

    - email: 3
      timing: "Day 10"
      subject: "Last chance: Special offer inside"
      content:
        - "Final outreach"
        - "Exclusive offer"
        - "Clear value proposition"
      cta: "Claim offer"

    - email: 4
      timing: "Day 15"
      subject: "Goodbye for now"
      content:
        - "Friendly farewell"
        - "Easy re-subscribe option"
        - "Social follow alternative"
      cta: "Keep me subscribed"

  outcomes:
    engaged: "Return to regular nurture"
    clicked_stay: "Reset engagement timer"
    unsubscribed: "Remove from lists"
    no_action: "Move to sunset list"
```

## Automation Workflows

### Lead Routing Workflow

```yaml
lead_routing_workflow:
  name: "New Lead Assignment"
  trigger: "Form submission"

  steps:
    - step: 1
      action: "Data enrichment"
      details: "Enrich with Clearbit/ZoomInfo"
      wait: "30 seconds"

    - step: 2
      action: "Lead scoring"
      details: "Calculate initial score"

    - step: 3
      action: "Lead grading"
      details: "Assign A-D grade"

    - step: 4
      action: "Check for existing account"
      branch:
        yes: "Route to account owner"
        no: "Continue to territory routing"

    - step: 5
      action: "Territory assignment"
      logic:
        - condition: "Geography"
          assignment: "Regional rep"
        - condition: "Company size"
          assignment: "SMB vs Enterprise team"
        - condition: "Industry"
          assignment: "Vertical specialist"

    - step: 6
      action: "Create task"
      details: "Follow-up task for assigned rep"
      sla:
        A_grade: "15 minutes"
        B_grade: "2 hours"
        C_grade: "24 hours"

    - step: 7
      action: "Notification"
      details: "Email + Slack alert to rep"

    - step: 8
      action: "Add to sequence"
      details: "Start appropriate nurture track"
```

### Lifecycle Stage Automation

```yaml
lifecycle_automation:
  stages:
    subscriber:
      entry_criteria: "Email opt-in only"
      automation:
        - "Welcome email series"
        - "Newsletter enrollment"
      exit_to: "Lead"

    lead:
      entry_criteria: "Additional form submission OR score > 20"
      automation:
        - "Lead enrichment"
        - "Add to nurture program"
        - "Sync to CRM"
      exit_to: "MQL"

    mql:
      entry_criteria: "Score >= 100 OR demo request"
      automation:
        - "Sales alert"
        - "Task creation"
        - "Pause marketing emails"
        - "Add to sales sequence"
      exit_to: "SQL"

    sql:
      entry_criteria: "Sales qualified in CRM"
      automation:
        - "Update nurture track"
        - "Trigger sales materials"
        - "Notify customer success"
      exit_to: "Opportunity"

    opportunity:
      entry_criteria: "Deal created in CRM"
      automation:
        - "Pause outbound marketing"
        - "Enable deal-stage emails"
        - "Trigger proposal materials"
      exit_to: "Customer OR Closed Lost"

    customer:
      entry_criteria: "Deal won"
      automation:
        - "Welcome/onboarding sequence"
        - "Remove from prospect lists"
        - "Add to customer nurture"
        - "Trigger CS handoff"

    closed_lost:
      entry_criteria: "Deal lost"
      automation:
        - "Return to nurture"
        - "Schedule follow-up (90 days)"
        - "Lost deal survey"
```

### Event/Webinar Automation

```yaml
webinar_workflow:
  name: "Webinar Registration Flow"

  pre_event:
    registration:
      - "Confirmation email (immediate)"
      - "Calendar invite"
      - "Add to webinar list"
      - "Update lead score (+15)"

    reminders:
      - timing: "1 week before"
        content: "Webinar details + agenda"

      - timing: "1 day before"
        content: "Reminder + calendar link"

      - timing: "1 hour before"
        content: "Starting soon + join link"

  post_event:
    attendees:
      timing: "2 hours after"
      sequence:
        - email: 1
          subject: "Thanks for joining! Here's the recording"
          content: "Recording + slides + resources"

        - email: 2
          timing: "+2 days"
          subject: "Diving deeper on [topic]"
          content: "Related content + next steps"

        - email: 3
          timing: "+5 days"
          subject: "Ready to [desired action]?"
          content: "CTA for demo/trial"

      scoring: "+25 points"

    no_shows:
      timing: "2 hours after"
      sequence:
        - email: 1
          subject: "Sorry we missed you! Recording inside"
          content: "Recording link + highlights"

        - email: 2
          timing: "+3 days"
          subject: "5 key takeaways from [webinar]"
          content: "Summary + recording"

      scoring: "+5 points (registered but didn't attend)"
```

## Email Best Practices

### Template Standards

```yaml
email_standards:
  technical:
    width: "600px max"
    images: "Alt text required, max 40% image"
    links: "UTM parameters on all links"
    preview_text: "Custom for each email"
    unsubscribe: "Clear and easy to find"

  content:
    subject_line:
      length: "30-50 characters"
      personalization: "Use when natural"
      avoid: "ALL CAPS, excessive punctuation, spam triggers"

    body:
      length: "50-200 words for nurture"
      paragraphs: "2-3 sentences max"
      cta: "Single clear CTA preferred"
      personalization:
        - "First name in greeting"
        - "Company name when relevant"
        - "Industry-specific content"

  testing:
    required:
      - "Preview in major email clients"
      - "Mobile rendering check"
      - "Link validation"
      - "Personalization token check"
      - "Spam score check"

    a_b_testing:
      variables:
        - "Subject lines"
        - "Send times"
        - "CTA copy/design"
        - "From name"

      sample_size: "15-20% minimum per variant"
      significance: "95% confidence level"
```

### Deliverability

```yaml
deliverability:
  authentication:
    required:
      - "SPF record configured"
      - "DKIM signing enabled"
      - "DMARC policy set"

    recommended:
      - "Dedicated sending IP"
      - "Custom tracking domain"

  list_hygiene:
    practices:
      - "Double opt-in for new subscribers"
      - "Regular bounce removal"
      - "Sunset inactive contacts (180 days)"
      - "Re-engagement before removal"

    metrics_to_monitor:
      - metric: "Bounce rate"
        target: "<2%"
        action: "Remove bounced immediately"

      - metric: "Spam complaint rate"
        target: "<0.1%"
        action: "Review content and list source"

      - metric: "Unsubscribe rate"
        target: "<0.5%"
        action: "Review frequency and relevance"

  sending_practices:
    - "Warm up new IPs gradually"
    - "Consistent sending volume"
    - "Avoid sudden volume spikes"
    - "Send during business hours"
```

## Performance Metrics

### KPI Benchmarks

```yaml
benchmarks:
  email_metrics:
    open_rate:
      benchmark: "20-30%"
      factors: "Subject line, sender reputation, timing"

    click_rate:
      benchmark: "2-5%"
      factors: "Content relevance, CTA clarity"

    click_to_open:
      benchmark: "10-15%"
      factors: "Content quality, email design"

    unsubscribe_rate:
      benchmark: "<0.5%"
      threshold: "Action if >1%"

    bounce_rate:
      benchmark: "<2%"
      hard_bounce: "Remove immediately"
      soft_bounce: "3 attempts then remove"

  automation_metrics:
    nurture_conversion:
      benchmark: "5-15%"
      definition: "% completing nurture goal"

    mql_rate:
      benchmark: "2-5%"
      definition: "% of leads becoming MQL"

    sql_conversion:
      benchmark: "20-30%"
      definition: "% of MQLs becoming SQL"

    velocity:
      benchmark: "Varies by industry"
      definition: "Time through funnel stages"

  deliverability_metrics:
    delivery_rate:
      target: ">95%"

    inbox_placement:
      target: ">90%"

    sender_score:
      target: ">80"
```

### Reporting Dashboard

```yaml
reporting:
  executive_dashboard:
    metrics:
      - "Total leads generated"
      - "MQL volume"
      - "Marketing-sourced pipeline"
      - "Marketing-influenced revenue"

    timeframes:
      - "Week over week"
      - "Month over month"
      - "Quarter over quarter"

  operational_dashboard:
    email_performance:
      - "Sends, opens, clicks by campaign"
      - "Top performing emails"
      - "A/B test results"

    automation_performance:
      - "Active contacts per program"
      - "Completion rates"
      - "Goal conversions"

    lead_flow:
      - "New leads by source"
      - "Stage progression"
      - "Lead score distribution"

    database_health:
      - "List growth rate"
      - "Engagement trends"
      - "Deliverability metrics"
```

## CRM Integration

### Salesforce Integration

```yaml
salesforce_integration:
  sync_settings:
    direction: "Bi-directional"
    frequency: "Real-time for key actions"

    objects_synced:
      leads:
        fields:
          - "All standard fields"
          - "Score"
          - "Grade"
          - "Last activity date"
          - "Lead source detail"

      contacts:
        fields:
          - "All standard fields"
          - "Engagement score"
          - "Last email activity"

      accounts:
        fields:
          - "Standard fields"
          - "Account score"
          - "Engagement metrics"

      opportunities:
        sync: "Pull into marketing platform"
        purpose: "Attribution reporting"

      campaigns:
        sync: "Bi-directional"
        purpose: "Track marketing influence"

  automation_triggers:
    from_crm:
      - "Lead status change → Update nurture"
      - "Opportunity created → Pause marketing"
      - "Deal closed won → Start customer journey"
      - "Deal closed lost → Re-engage workflow"

    to_crm:
      - "MQL threshold → Create task"
      - "High-value action → Alert"
      - "Score change → Update field"
      - "New lead → Create record"
```

## Лучшие практики

1. **Segment everything** — персонализированные nurture paths по сегментам
2. **Score behavior AND fit** — комбинируйте behavioral и demographic scoring
3. **Respect preferences** — предлагайте preference center
4. **Test continuously** — A/B тестируйте subject lines, CTAs, timing
5. **Clean your lists** — регулярная гигиена базы критична для deliverability
6. **Align with sales** — согласуйте MQL критерии и handoff процесс с продажами
