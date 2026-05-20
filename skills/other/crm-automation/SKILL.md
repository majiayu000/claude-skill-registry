---
name: crm-automation
description: "CRM workflow automation for HubSpot, Salesforce, Pipedrive - lead management, deal tracking, and multi-CRM synchronization"
version: "1.0.0"
author: claude-office-skills
license: MIT

category: sales
tags:
  - crm
  - hubspot
  - salesforce
  - automation
  - lead-management
department: Sales

models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - gpt-4
    - gpt-4o

mcp:
  server: crm-mcp
  tools:
    - hubspot_create_contact
    - hubspot_update_deal
    - salesforce_query
    - pipedrive_sync
    - enrichment_api

capabilities:
  - lead_capture
  - deal_tracking
  - pipeline_management
  - multi_crm_sync
  - automated_outreach

languages:
  - en
  - zh

related_skills:
  - lead-routing
  - sales-pipeline
  - email-drafter
  - proposal-writer
---

# CRM Automation

Automate CRM workflows for HubSpot, Salesforce, and Pipedrive including lead management, deal tracking, pipeline automation, and multi-CRM synchronization. Based on n8n workflow templates.

## Overview

This skill covers:
- Lead capture and enrichment automation
- Deal stage progression workflows
- Multi-CRM data synchronization
- Automated follow-up sequences
- Sales analytics and reporting

---

## Core Workflow Patterns

### 1. Lead Capture → Enrichment → Assignment

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Lead Source │───▶│ Enrich Data │───▶│ Score Lead  │───▶│ Route to    │
│ (Form/API)  │    │ (Clearbit)  │    │ (AI/Rules)  │    │ Sales Rep   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                                │
                         ┌─────────────┐    ┌─────────────┐    │
                         │ Start       │◀───│ Create in   │◀───┘
                         │ Sequence    │    │ CRM         │
                         └─────────────┘    └─────────────┘
```

**n8n Configuration**:
```yaml
workflow: "Lead Capture to CRM"

trigger:
  - type: webhook
    event: form_submission
    source: [website, landing_page, calendly]

steps:
  1. capture_lead:
      fields: [email, name, company, phone, source]
  
  2. enrich_data:
      provider: clearbit
      lookup_by: email
      append: [company_size, industry, title, linkedin]
  
  3. score_lead:
      model: ai_scoring  # or rule-based
      factors:
        - company_size: {1-50: 10, 51-200: 20, 201+: 30}
        - industry_fit: {high: 30, medium: 20, low: 10}
        - title_seniority: {c-level: 30, director: 20, manager: 10}
      threshold: 50  # MQL threshold
  
  4. route_lead:
      rules:
        - if: score >= 80 AND industry == "tech"
          assign_to: "Enterprise Team"
        - if: score >= 50
          assign_to: "SMB Team"
        - else:
          assign_to: "Marketing Nurture"
  
  5. create_in_crm:
      platform: hubspot
      object: contact
      properties:
        email: "{email}"
        firstname: "{first_name}"
        company: "{company}"
        lead_score: "{score}"
        lead_source: "{source}"
  
  6. start_sequence:
      if: score >= 50
      sequence: "New Lead Welcome"
      delay: 1_hour
```

---

### 2. Deal Stage Automation

```yaml
workflow: "Deal Stage Progression"

trigger:
  - type: hubspot_deal_updated
    property: dealstage

stages:
  appointment_scheduled:
    actions:
      - create_task: "Prepare for meeting"
        due: 1_day_before_meeting
      - notify_slack: "#sales-pipeline"
      - update_property: last_activity_date
  
  qualified_to_buy:
    actions:
      - create_task: "Send proposal"
        due: 3_days
      - notify_manager: true
      - add_to_forecast: true
  
  presentation_scheduled:
    actions:
      - create_task: "Prepare demo environment"
      - send_reminder: 1_hour_before
      - log_activity: "Presentation scheduled"
  
  contract_sent:
    actions:
      - set_close_date: 14_days_from_now
      - create_task: "Follow up on contract"
        due: 7_days
      - notify_legal: if amount > 50000
  
  closed_won:
    actions:
      - notify_slack: "#wins"
      - trigger_onboarding: true
      - update_forecast: remove
      - celebrate: confetti  # Slack celebration
  
  closed_lost:
    actions:
      - log_loss_reason: required
      - add_to_nurture: true
      - schedule_reengagement: 90_days
```

---

### 3. Multi-CRM Synchronization

```yaml
workflow: "HubSpot + Salesforce + Pipedrive Sync"

sync_rules:
  contacts:
    master: hubspot
    sync_to: [salesforce, pipedrive]
    frequency: real_time
    fields:
      - email (unique_key)
      - name
      - company
      - phone
      - owner
    conflict_resolution: most_recent_wins
    deduplication: 
      provider: openai
      similarity_threshold: 0.85
  
  deals:
    master: salesforce
    sync_to: [hubspot, pipedrive]
    frequency: every_15_minutes
    field_mapping:
      salesforce.Opportunity.Amount → hubspot.deal.amount
      salesforce.Opportunity.CloseDate → hubspot.deal.closedate
      salesforce.Opportunity.StageName → hubspot.deal.dealstage
  
  activities:
    aggregate_to: google_sheets
    types: [calls, emails, meetings, notes]
    columns: [date, contact, type, summary, outcome]
```

**n8n Implementation**:
```javascript
// Multi-CRM Sync Node
{
  "nodes": [
    {
      "name": "Get HubSpot Contacts",
      "type": "n8n-nodes-base.hubspot",
      "parameters": {
        "operation": "getAll",
        "limit": 100,
        "additionalFields": {
          "propertiesToInclude": ["email", "firstname", "lastname", "company"]
        }
      }
    },
    {
      "name": "Get Salesforce Contacts",
      "type": "n8n-nodes-base.salesforce",
      "parameters": {
        "operation": "getAll",
        "sobject": "Contact"
      }
    },
    {
      "name": "Deduplicate with OpenAI",
      "type": "n8n-nodes-base.openAi",
      "parameters": {
        "operation": "message",
        "model": "gpt-4",
        "prompt": "Compare these contacts and identify duplicates: {{$json}}"
      }
    },
    {
      "name": "Sync to Master Sheet",
      "type": "n8n-nodes-base.googleSheets",
      "parameters": {
        "operation": "append",
        "sheetId": "your-sheet-id"
      }
    }
  ]
}
```

---

## Lead Scoring Model

### Rule-Based Scoring

```yaml
lead_score_rules:
  demographic:
    job_title:
      - C-Level|VP|Director: +30
      - Manager|Head: +20
      - Individual Contributor: +10
    
    company_size:
      - 1-50: +10
      - 51-200: +20
      - 201-1000: +25
      - 1000+: +30
    
    industry:
      - Technology|SaaS: +30
      - Finance|Healthcare: +25
      - Manufacturing|Retail: +15
  
  behavioral:
    website_visits:
      - 1-2: +5
      - 3-5: +10
      - 6+: +20
    
    content_downloads:
      - Whitepaper: +15
      - Case Study: +20
      - Pricing Page: +25
    
    email_engagement:
      - Opened: +5
      - Clicked: +10
      - Replied: +20

thresholds:
  - MQL: 50
  - SQL: 75
  - Hot Lead: 90
```

### AI-Based Scoring

```yaml
ai_scoring_model:
  provider: openai
  prompt: |
    Score this lead from 0-100 based on:
    - Fit with our ICP (ideal customer profile)
    - Buying intent signals
    - Budget authority
    - Timeline urgency
    
    Lead Data: {lead_data}
    ICP: B2B SaaS companies, 50-500 employees, Series A+
    
    Return JSON: {"score": X, "reasoning": "...", "next_action": "..."}
```

---

## Automated Sequences

### Sequence 1: New Lead Welcome

```yaml
sequence: "New Lead Welcome"
trigger: lead_created AND score >= 50

steps:
  - day_0:
      type: email
      template: "welcome_intro"
      subject: "Welcome to {Company} - Here's what's next"
  
  - day_2:
      type: email
      template: "value_prop"
      subject: "How {Similar_Company} achieved {Result}"
      condition: not_replied
  
  - day_4:
      type: task
      action: "LinkedIn connection request"
      assign_to: owner
  
  - day_7:
      type: email
      template: "case_study"
      subject: "Quick case study for {Lead_Company}"
      condition: not_replied
  
  - day_10:
      type: email
      template: "meeting_request"
      subject: "15 min to discuss {Pain_Point}?"
      include: calendly_link
  
  - day_14:
      type: task
      action: "Phone call attempt"
      assign_to: owner
      condition: not_responded
```

### Sequence 2: Deal Follow-Up

```yaml
sequence: "Proposal Follow-Up"
trigger: deal_stage == "contract_sent"

steps:
  - day_3:
      type: email
      template: "contract_check_in"
      subject: "Any questions about the proposal?"
  
  - day_7:
      type: task
      action: "Phone call - contract follow-up"
  
  - day_10:
      type: email
      template: "deadline_reminder"
      subject: "Pricing valid until {deadline}"
      condition: not_responded
  
  - day_14:
      type: alert
      notify: sales_manager
      message: "Deal stuck in contract stage"
```

---

## Integration Recipes

### Recipe 1: Calendly → HubSpot

```yaml
trigger: calendly.booking_created

actions:
  1. search_contact:
      hubspot.search: email == calendly.invitee_email
  
  2. create_or_update:
      if: contact_exists
        hubspot.update_contact:
          last_meeting_booked: calendly.start_time
      else:
        hubspot.create_contact:
          email: calendly.invitee_email
          firstname: calendly.invitee_name
          lifecycle_stage: "salesqualifiedlead"
  
  3. create_meeting:
      hubspot.create_engagement:
        type: MEETING
        scheduled_time: calendly.start_time
        title: calendly.event_name
  
  4. notify:
      slack.send:
        channel: "#sales"
        message: "Meeting booked: {name} at {time}"
```

### Recipe 2: LinkedIn → HubSpot

```yaml
trigger: linkedin.connection_accepted

actions:
  1. enrich:
      linkedin.get_profile: connection_id
  
  2. create_contact:
      hubspot.create:
        email: linkedin.email
        firstname: linkedin.first_name
        lastname: linkedin.last_name
        jobtitle: linkedin.title
        company: linkedin.company
        linkedin_url: linkedin.profile_url
        lead_source: "LinkedIn"
  
  3. add_to_sequence:
      if: title contains ["CEO", "CTO", "VP"]
      sequence: "LinkedIn C-Level Outreach"
```

---

## Reporting Templates

### Weekly Sales Report

```markdown
# Sales Pipeline Report - Week {week_number}

## Pipeline Summary
| Stage | Deals | Value | Change |
|-------|-------|-------|--------|
| New | 15 | $150K | +5 |
| Qualified | 8 | $120K | +2 |
| Proposal | 5 | $85K | -1 |
| Negotiation | 3 | $45K | +1 |
| **Total Pipeline** | **31** | **$400K** | **+7** |

## This Week's Activity
- New leads: 45
- Meetings held: 12
- Proposals sent: 4
- Deals closed: 2 ($35K)

## Team Performance
| Rep | Meetings | Proposals | Closed |
|-----|----------|-----------|--------|
| Alice | 5 | 2 | 1 |
| Bob | 4 | 1 | 1 |
| Carol | 3 | 1 | 0 |

## Forecast
- Commit: $45K (3 deals)
- Best Case: $85K (5 deals)
- Pipeline: $400K (31 deals)

## Actions Needed
- [ ] Follow up on 3 stale deals (>14 days no activity)
- [ ] Schedule demo for Enterprise Lead X
- [ ] Send revised proposal to Company Y
```

---

## Best Practices

### Data Hygiene

```yaml
data_hygiene_rules:
  - deduplicate: weekly
    method: email_match + company_fuzzy_match
  
  - validate_emails: on_create
    action: remove_invalid
  
  - enrich_missing: daily
    fields: [company, title, linkedin]
  
  - archive_stale: monthly
    criteria: no_activity > 180_days
    action: move_to_archive
```

### Security

```yaml
security_practices:
  - api_keys: rotate_quarterly
  - access_control: role_based
  - audit_log: all_changes
  - pii_handling: encrypt_at_rest
  - gdpr_compliance: consent_tracking
```

---

*CRM Automation Skill - Part of Claude Office Skills*
