---
name: Zendesk Automation
description: Automate customer support workflows with Zendesk ticket management, routing, and analytics
version: 1.0.0
author: Claude Office Skills
category: support
tags:
  - zendesk
  - helpdesk
  - tickets
  - customer-support
  - automation
department: support
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: helpdesk-mcp
  tools:
    - zendesk_create_ticket
    - zendesk_update_ticket
    - zendesk_search
    - zendesk_macros
capabilities:
  - Ticket creation and routing
  - Auto-response generation
  - SLA monitoring
  - Agent assignment
input:
  - Support requests
  - Ticket data
  - Customer information
  - Priority criteria
output:
  - Ticket responses
  - Routing decisions
  - Performance reports
  - SLA dashboards
languages:
  - en
  - zh
related_skills:
  - slack-workflows
  - customer-success
  - intercom-automation
---

# Zendesk Automation

Comprehensive skill for automating Zendesk support workflows and ticket management.

## Core Workflows

### 1. Ticket Triage Pipeline

```
INCOMING TICKET FLOW:
┌─────────────────┐
│  New Ticket     │
└────────┬────────┘
         ▼
┌─────────────────┐
│  AI Analysis    │
│  - Intent       │
│  - Sentiment    │
│  - Urgency      │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Categorize     │
│  - Type         │
│  - Product      │
│  - Skill needed │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Route & Assign │
│  - Team         │
│  - Agent        │
│  - Priority     │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Auto-Response  │
│  (if applicable)│
└─────────────────┘
```

### 2. Routing Rules

```yaml
routing_rules:
  - name: billing_issues
    conditions:
      - field: subject
        contains: ["billing", "invoice", "charge", "refund", "payment"]
      - field: tags
        includes: ["billing"]
    actions:
      - set_group: billing_team
      - set_priority: high
      - add_tags: ["billing_routed"]
  
  - name: technical_support
    conditions:
      - field: subject
        contains: ["error", "bug", "not working", "crash"]
      - field: product
        equals: "software"
    actions:
      - set_group: tech_support
      - set_priority: normal
      - add_tags: ["technical"]
  
  - name: enterprise_escalation
    conditions:
      - field: organization
        tier: enterprise
      - field: priority
        equals: urgent
    actions:
      - set_group: enterprise_team
      - set_priority: urgent
      - notify: slack_channel
```

### 3. Priority Matrix

| Customer Tier | Issue Type | Response SLA | Resolution SLA |
|--------------|------------|--------------|----------------|
| Enterprise | Critical | 15 minutes | 4 hours |
| Enterprise | High | 1 hour | 8 hours |
| Business | Critical | 1 hour | 8 hours |
| Business | Normal | 4 hours | 24 hours |
| Standard | All | 8 hours | 48 hours |

## Auto-Response Templates

### Common Issue Responses

```yaml
auto_responses:
  password_reset:
    trigger:
      keywords: ["password", "reset", "forgot", "login"]
    response: |
      Hi {{ticket.requester.name}},
      
      I understand you're having trouble accessing your account. 
      Here's how to reset your password:
      
      1. Go to {{settings.login_url}}/forgot-password
      2. Enter your email address
      3. Check your inbox for the reset link
      4. Create a new password
      
      If you don't receive the email within 5 minutes, 
      please check your spam folder.
      
      Let me know if you need any further assistance!
    
    actions:
      - add_tags: ["auto_replied", "password_reset"]
      - set_status: pending

  shipping_inquiry:
    trigger:
      keywords: ["shipping", "tracking", "delivery", "order status"]
    response: |
      Hi {{ticket.requester.name}},
      
      Thanks for reaching out about your order!
      
      I've looked up your recent order and here's the status:
      {{#if order.tracking_number}}
      - Order #: {{order.id}}
      - Status: {{order.status}}
      - Tracking: {{order.tracking_number}}
      - Estimated Delivery: {{order.estimated_delivery}}
      {{else}}
      Your order is being processed and tracking information 
      will be available within 24 hours.
      {{/if}}
      
      Is there anything else I can help with?
```

## Ticket Management

### Macro Library

```yaml
macros:
  - name: request_more_info
    actions:
      - add_comment: |
          Thank you for contacting us. To better assist you, 
          could you please provide:
          1. Your account email
          2. Steps to reproduce the issue
          3. Any error messages you're seeing
          4. Screenshots if possible
      - set_status: pending
      - add_tags: ["awaiting_info"]

  - name: escalate_to_engineering
    actions:
      - add_internal_note: "Escalated to engineering team"
      - set_group: engineering
      - set_priority: high
      - add_tags: ["escalated", "engineering"]
      - notify: engineering_slack

  - name: close_resolved
    actions:
      - add_comment: |
          I'm glad we could resolve this for you! 
          
          If you have any other questions, feel free to 
          reach out anytime. We're here to help.
          
          Have a great day!
      - set_status: solved
      - add_tags: ["resolved"]
```

### Bulk Operations

```yaml
bulk_actions:
  - name: close_stale_tickets
    schedule: "0 0 * * *"  # Daily
    conditions:
      - status: pending
      - last_update_days: 7
    actions:
      - add_comment: "Closing due to no response. Please reopen if needed."
      - set_status: solved
      - add_tags: ["auto_closed"]

  - name: escalate_breaching_sla
    schedule: "*/15 * * * *"  # Every 15 min
    conditions:
      - sla_breach_in_minutes: 30
    actions:
      - set_priority: urgent
      - notify: team_lead
      - add_tags: ["sla_at_risk"]
```

## SLA Management

### SLA Policies

```yaml
sla_policies:
  - name: enterprise_sla
    conditions:
      organization_tag: enterprise
    targets:
      first_reply:
        urgent: 15  # minutes
        high: 60
        normal: 240
      resolution:
        urgent: 240
        high: 480
        normal: 1440

  - name: standard_sla
    conditions:
      default: true
    targets:
      first_reply:
        urgent: 60
        high: 240
        normal: 480
      resolution:
        urgent: 480
        high: 1440
        normal: 2880
```

### SLA Dashboard

```
SLA PERFORMANCE - THIS WEEK
═══════════════════════════════════════

First Reply SLA:
Enterprise  ████████████████████ 98% ✓
Business    ██████████████████░░ 94% ✓
Standard    █████████████████░░░ 89% ⚠

Resolution SLA:
Enterprise  ████████████████████ 96% ✓
Business    █████████████████░░░ 91% ✓
Standard    ████████████████░░░░ 85% ⚠

TICKETS AT RISK:
┌──────────┬──────────┬───────────┐
│ Ticket   │ Customer │ Time Left │
├──────────┼──────────┼───────────┤
│ #45231   │ Acme Corp│ 12 min    │
│ #45198   │ TechStart│ 28 min    │
│ #45156   │ DataFlow │ 45 min    │
└──────────┴──────────┴───────────┘
```

## AI-Powered Features

### Sentiment Analysis

```yaml
sentiment_analysis:
  enabled: true
  actions:
    negative:
      - add_tags: ["negative_sentiment"]
      - set_priority: +1  # Increase priority
      - notify: team_lead
    
    frustrated:
      - add_tags: ["frustrated_customer"]
      - route_to: senior_agents
      - add_internal_note: "Customer appears frustrated"
```

### Intent Detection

```yaml
intent_detection:
  categories:
    - name: billing_inquiry
      keywords: ["charge", "invoice", "refund", "bill"]
      confidence_threshold: 0.8
    
    - name: technical_issue
      keywords: ["error", "bug", "broken", "crash"]
      confidence_threshold: 0.75
    
    - name: feature_request
      keywords: ["wish", "would be nice", "suggest", "feature"]
      confidence_threshold: 0.7
    
    - name: cancellation
      keywords: ["cancel", "stop", "end subscription"]
      confidence_threshold: 0.85
      actions:
        - route_to: retention_team
        - set_priority: high
```

## Integration Workflows

### Slack Integration

```yaml
slack_integration:
  notifications:
    - trigger: new_urgent_ticket
      channel: "#support-urgent"
      message: "🚨 New urgent ticket: {{ticket.subject}}"
    
    - trigger: sla_warning
      channel: "#support-alerts"
      message: "⚠️ Ticket #{{ticket.id}} approaching SLA breach"
    
    - trigger: negative_csat
      channel: "#support-feedback"
      message: "📉 Low CSAT received for ticket #{{ticket.id}}"
```

### JIRA Integration

```yaml
jira_integration:
  sync_rules:
    - zendesk_tag: bug_confirmed
      create_jira:
        project: DEV
        issue_type: Bug
        priority_map:
          urgent: Highest
          high: High
          normal: Medium
        sync_fields:
          - description
          - attachments
        link_back: true
```

## Analytics & Reporting

### Key Metrics

```
SUPPORT METRICS DASHBOARD
═══════════════════════════════════════

Volume:
Today's Tickets: 156 (+12% vs avg)
Open Tickets: 234
Backlog: 45

Performance:
Avg First Reply: 42 min (target: 60 min) ✓
Avg Resolution: 4.2 hrs (target: 8 hrs) ✓
One-Touch Resolution: 34%

Satisfaction:
CSAT Score: 4.6/5.0 ⭐
NPS: +45
Response Quality: 92%

Agent Performance:
┌────────────┬────────┬──────────┬──────┐
│ Agent      │ Solved │ Avg Time │ CSAT │
├────────────┼────────┼──────────┼──────┤
│ Sarah      │ 28     │ 3.1 hrs  │ 4.8  │
│ Mike       │ 25     │ 3.5 hrs  │ 4.7  │
│ Lisa       │ 22     │ 4.0 hrs  │ 4.6  │
└────────────┴────────┴──────────┴──────┘
```

## Best Practices

1. **Quick First Response**: Acknowledge tickets quickly, even if resolution takes longer
2. **Use Macros Wisely**: Personalize templated responses
3. **Tag Consistently**: Enable better routing and reporting
4. **Monitor SLAs**: Set up alerts before breaches
5. **Capture Feedback**: Send CSAT surveys after resolution
6. **Regular Training**: Update agents on common issues
