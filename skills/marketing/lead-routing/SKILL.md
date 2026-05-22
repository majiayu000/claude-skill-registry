---
name: lead-routing
description: "Intelligent lead assignment and routing - AI-powered scoring, territory mapping, round-robin distribution, and workload balancing"
version: "1.0.0"
author: claude-office-skills
license: MIT

category: sales
tags:
  - lead-management
  - sales-automation
  - routing
  - assignment
  - crm
department: Sales

models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4

mcp:
  server: crm-mcp
  tools:
    - hubspot_assign_owner
    - salesforce_route
    - enrichment_api

capabilities:
  - lead_scoring
  - territory_routing
  - round_robin
  - workload_balancing
  - sla_management

languages:
  - en
  - zh

related_skills:
  - crm-automation
  - sales-pipeline
  - saas-metrics
---

# Lead Routing

Intelligent lead assignment and routing system with AI-powered scoring, territory mapping, round-robin distribution, and workload balancing. Based on n8n's HubSpot/Salesforce automation templates.

## Overview

This skill covers:
- Lead scoring and qualification
- Territory-based routing
- Round-robin distribution
- Workload balancing
- SLA monitoring and escalation

---

## Routing Strategies

### 1. Rule-Based Routing

```yaml
routing_rules:
  # By Company Size
  - name: "Enterprise Routing"
    condition:
      company_size: ">= 500"
      OR:
        annual_revenue: ">= $10M"
    assign_to: "Enterprise Team"
    priority: high
    sla: 1_hour
    
  - name: "Mid-Market Routing"
    condition:
      company_size: "100-499"
    assign_to: "Mid-Market Team"
    priority: medium
    sla: 4_hours
    
  - name: "SMB Routing"
    condition:
      company_size: "< 100"
    assign_to: "SMB Team"
    priority: standard
    sla: 24_hours

  # By Geography
  - name: "APAC Routing"
    condition:
      country: ["China", "Japan", "Singapore", "Australia"]
    assign_to: "APAC Team"
    timezone_aware: true
    
  - name: "EMEA Routing"
    condition:
      country: ["UK", "Germany", "France", "Netherlands"]
    assign_to: "EMEA Team"
    
  - name: "Americas Routing"
    condition:
      country: ["US", "Canada", "Brazil", "Mexico"]
    assign_to: "Americas Team"

  # By Industry
  - name: "Healthcare Specialist"
    condition:
      industry: ["Healthcare", "Pharmaceuticals", "Medical Devices"]
    assign_to: "Healthcare Sales"
    
  - name: "Finance Specialist"
    condition:
      industry: ["Banking", "Insurance", "FinTech"]
    assign_to: "Financial Services Sales"
```

---

### 2. Round-Robin Distribution

```yaml
round_robin_config:
  team: "SMB Sales"
  members:
    - name: Alice
      capacity: 100%
      max_leads_per_day: 20
      
    - name: Bob
      capacity: 100%
      max_leads_per_day: 20
      
    - name: Carol
      capacity: 50%  # Part-time
      max_leads_per_day: 10
      
  rules:
    distribution: weighted  # or equal
    skip_if:
      - out_of_office: true
      - at_capacity: true
    reset: daily
    
  tracking:
    log_assignments: true
    balance_check: hourly
```

**Distribution Algorithm**:
```
┌─────────────────────────────────────────────────────────────┐
│                   ROUND-ROBIN LOGIC                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. New lead arrives                                        │
│                    │                                        │
│                    ▼                                        │
│  2. Check team availability                                 │
│     - Filter out: OOO, at capacity, off-hours              │
│                    │                                        │
│                    ▼                                        │
│  3. Calculate weighted position                             │
│     - Current assignments today                             │
│     - Capacity percentage                                   │
│     - Last assignment time                                  │
│                    │                                        │
│                    ▼                                        │
│  4. Assign to rep with lowest weighted score               │
│                    │                                        │
│                    ▼                                        │
│  5. Update tracking, notify rep                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 3. AI-Powered Lead Scoring

```yaml
ai_scoring:
  provider: openai
  model: gpt-4
  
  input_factors:
    demographic:
      - company_size
      - industry
      - job_title
      - location
      
    firmographic:
      - annual_revenue
      - employee_count
      - funding_stage
      - tech_stack
      
    behavioral:
      - pages_visited
      - content_downloads
      - email_engagement
      - demo_requests
      
    fit_score:
      - icp_match_percentage
      - competitor_usage
      - budget_authority
      
  scoring_prompt: |
    Score this lead from 0-100 based on:
    
    Our ICP (Ideal Customer Profile):
    - B2B SaaS companies
    - 50-500 employees
    - Series A or later
    - Using {competitor} or {similar_tool}
    
    Lead Data:
    {lead_data}
    
    Return JSON:
    {
      "score": 0-100,
      "fit_score": 0-100,
      "intent_score": 0-100,
      "tier": "A/B/C/D",
      "reasoning": "...",
      "recommended_action": "...",
      "routing_suggestion": "..."
    }

  tier_thresholds:
    A: 80-100  # Hot lead, immediate follow-up
    B: 60-79   # Qualified, standard follow-up
    C: 40-59   # Nurture, marketing sequence
    D: 0-39    # Low priority, long-term nurture
```

---

### 4. Territory Mapping

```yaml
territory_map:
  north_america:
    west:
      states: [CA, WA, OR, NV, AZ, CO, UT]
      owner: "West Coast Team"
      reps: [Alice, Bob]
      
    central:
      states: [TX, IL, OH, MI, MN, WI]
      owner: "Central Team"
      reps: [Carol, David]
      
    east:
      states: [NY, MA, PA, FL, GA, NC]
      owner: "East Coast Team"
      reps: [Eve, Frank]
      
  international:
    emea:
      countries: [UK, DE, FR, NL, ES, IT]
      owner: "EMEA Team"
      timezone: "Europe/London"
      
    apac:
      countries: [JP, SG, AU, KR, IN]
      owner: "APAC Team"
      timezone: "Asia/Tokyo"

  overlap_resolution:
    # When lead matches multiple territories
    priority_order:
      1: named_account_owner  # If account already has owner
      2: industry_specialist  # If industry requires specialist
      3: geography           # Default to geography
```

---

### 5. Workload Balancing

```yaml
workload_balancer:
  check_frequency: hourly
  
  metrics_tracked:
    - current_open_leads
    - leads_assigned_today
    - leads_assigned_this_week
    - average_response_time
    - conversion_rate
    
  balance_rules:
    max_variance: 20%  # Max difference between reps
    
    rebalance_trigger:
      - variance > max_variance
      - rep_at_capacity
      - rep_underperforming
      
    rebalance_actions:
      - pause_assignments: for_overloaded_rep
      - increase_weight: for_underloaded_rep
      - notify_manager: when_rebalancing
      
  capacity_management:
    per_rep:
      max_open_leads: 50
      max_new_per_day: 15
      max_new_per_week: 60
      
    team_level:
      overflow_queue: true
      overflow_notify: sales_manager
      escalation_threshold: 2_hours
```

---

## Workflow Implementation

### Complete Lead Routing Workflow

```yaml
workflow: "Intelligent Lead Router"

trigger:
  - type: hubspot_contact_created
  - type: form_submission
  - type: api_webhook

steps:
  1. enrich_lead:
      providers: [clearbit, zoominfo]
      fields:
        - company_size
        - industry
        - revenue
        - location
        - linkedin_url
        
  2. score_lead:
      method: ai_scoring
      store_result:
        hubspot_property: lead_score
        
  3. determine_tier:
      A_tier: score >= 80
      B_tier: score >= 60
      C_tier: score >= 40
      D_tier: score < 40
      
  4. apply_routing_rules:
      sequence:
        - check: named_account_owner
        - check: industry_specialist
        - check: territory_match
        - check: round_robin_availability
        
  5. assign_owner:
      hubspot:
        update_contact:
          hubspot_owner_id: "{selected_owner_id}"
          lead_status: "New"
          lead_tier: "{tier}"
          routing_reason: "{routing_logic}"
          
  6. create_task:
      hubspot:
        type: CALL
        subject: "Follow up: New {tier} lead - {company}"
        due_date: "{sla_deadline}"
        priority: "{priority_based_on_tier}"
        notes: |
          Lead Score: {score}
          Routing Reason: {routing_reason}
          Key Info: {summary}
          
  7. notify_owner:
      slack_dm:
        message: |
          🎯 *New Lead Assigned*
          
          **{contact_name}** at **{company}**
          Score: {score} ({tier} Tier)
          
          📞 SLA: Respond within {sla_time}
          
          Quick actions:
          • [View in HubSpot]({hubspot_link})
          • [LinkedIn]({linkedin_url})
          • [Schedule Call]({calendly_link})
          
  8. start_sla_timer:
      deadline: "{sla_deadline}"
      escalation_path:
        - 50%_elapsed: reminder_to_owner
        - 80%_elapsed: notify_manager
        - 100%_elapsed: reassign + alert
```

---

## SLA Management

```yaml
sla_tiers:
  tier_a:
    response_time: 1_hour
    escalation_path:
      - 30min: slack_reminder
      - 45min: manager_alert
      - 60min: auto_reassign
      
  tier_b:
    response_time: 4_hours
    escalation_path:
      - 2h: slack_reminder
      - 3h: manager_alert
      - 4h: auto_reassign
      
  tier_c:
    response_time: 24_hours
    escalation_path:
      - 12h: slack_reminder
      - 20h: manager_alert
      - 24h: move_to_queue

sla_reporting:
  metrics:
    - response_time_avg
    - response_time_p90
    - sla_compliance_rate
    - escalation_count
    
  report_frequency: weekly
  recipients: [sales_manager, ops_manager]
```

---

## Reporting Dashboard

```markdown
# Lead Routing Report - {Week}

## Distribution Summary
| Rep | Assigned | Responded | Avg Response | SLA Met |
|-----|----------|-----------|--------------|---------|
| Alice | 45 | 43 | 1.2h | 96% |
| Bob | 42 | 40 | 1.8h | 90% |
| Carol | 38 | 38 | 0.8h | 100% |
| **Total** | **125** | **121** | **1.3h** | **95%** |

## By Tier
| Tier | Count | Avg Score | Converted | Conv Rate |
|------|-------|-----------|-----------|-----------|
| A | 25 | 87 | 12 | 48% |
| B | 45 | 68 | 15 | 33% |
| C | 35 | 52 | 5 | 14% |
| D | 20 | 28 | 1 | 5% |

## Routing Breakdown
- By Territory: 60%
- By Industry: 25%
- Round Robin: 15%

## Issues
- 3 leads waited >SLA (reassigned)
- Alice at 95% capacity (monitor)
- No coverage for Healthcare vertical (gap)

## Recommendations
1. Hire Healthcare specialist
2. Increase Bob's training (response time)
3. Adjust A-tier threshold to 85 (too many false positives)
```

---

## Output Example

**Request**: "Route this lead: John Smith, CTO at TechCorp (500 employees, SF, SaaS)"

**Output**:

```markdown
# Lead Routing Decision

## Lead Profile
- **Name**: John Smith
- **Title**: CTO
- **Company**: TechCorp
- **Size**: 500 employees
- **Location**: San Francisco, CA
- **Industry**: SaaS

## AI Scoring
```json
{
  "score": 85,
  "fit_score": 90,
  "intent_score": 80,
  "tier": "A",
  "reasoning": "Strong ICP fit - CTO at 500-person SaaS company in our target market. High authority buyer.",
  "recommended_action": "Immediate outreach - high-value prospect"
}
```

## Routing Decision

**Assigned to**: Alice Chen (Enterprise West)

**Routing Logic**:
1. ✅ Territory: San Francisco → West Coast
2. ✅ Company Size: 500 → Enterprise tier
3. ✅ Industry: SaaS → No specialist needed
4. ✅ Availability: Alice has capacity (18/20 today)

## Action Items Created

1. **Task**: Follow up call
   - Due: 1 hour (Tier A SLA)
   - Priority: High

2. **Slack Notification**: Sent to Alice

3. **SLA Timer**: Started (1h countdown)

## Recommended Outreach

```
Subject: Quick question about {pain_point} at TechCorp

Hi John,

Noticed TechCorp is scaling fast - congrats on the growth. 

CTOs at similar SaaS companies often tell us {common_challenge}. 

Would a 15-min call this week make sense to see if we can help?

[Calendly Link]
```
```

---

*Lead Routing Skill - Part of Claude Office Skills*
