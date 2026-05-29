---
name: customer-support-builder
description: Build scalable customer support systems including help centers, chatbots, ticketing systems, and self-service knowledge bases. Use when designing support infrastructure, reducing support load, improving customer satisfaction, or scaling support without linear hiring.
license: Complete terms in LICENSE.txt
---

# Customer Support Builder

Build scalable customer support systems that grow with your product without requiring linear hiring increases.

## Core Principle

**Support should scale sub-linearly with users.** As you grow from 100 to 10,000 users, support volume shouldn't increase 100x. Good self-service systems can keep support needs growing at only 10-20x while user base grows 100x.

## Support Maturity Model

### Stage 1: Founder-Led (0-100 users)

- Founders answer every question personally
- Learn what users actually struggle with
- Document FAQs manually
- **Key Metric**: Response time < 2 hours

### Stage 2: Documented (100-1,000 users)

- Comprehensive knowledge base
- Email support with templates
- Basic FAQ section
- **Key Metric**: 30% self-service rate

### Stage 3: Self-Service (1,000-10,000 users)

- Searchable help center
- Contextual in-app help
- Automated responses for common issues
- **Key Metric**: 60% self-service rate

### Stage 4: Scaled (10,000+ users)

- AI-powered chatbots
- Community forums
- Video tutorials
- Proactive support (detect issues before tickets)
- **Key Metric**: 80% self-service rate

## Knowledge Base Architecture

### Content Structure

```
Help Center
├── Getting Started
│   ├── Quick Start Guide (< 5 min)
│   ├── Account Setup
│   └── First Steps Tutorial
├── Core Features
│   ├── Feature A Guide
│   ├── Feature B Guide
│   └── Feature C Guide
├── Troubleshooting
│   ├── Common Errors
│   ├── Performance Issues
│   └── Integration Problems
├── Account & Billing
│   ├── Pricing Plans
│   ├── Billing Issues
│   └── Account Management
└── API & Integrations
    ├── API Documentation
    ├── Webhooks
    └── Integration Guides
```

### Article Template

```markdown
# [Clear, Searchable Title]

**Time to complete**: 3 minutes
**Difficulty**: Beginner/Intermediate/Advanced

## Problem

One-sentence description of what this solves.

## Solution

Step-by-step instructions with screenshots.

1. **Step 1**: Clear action
   - Screenshot/GIF
   - Expected result

2. **Step 2**: Next action
   - Screenshot/GIF
   - Expected result

## Troubleshooting

- Problem: X → Solution: Y
- Problem: A → Solution: B

## Related Articles

- [Article 1](#)
- [Article 2](#)
```

## Support Channels

### Email Support

**Setup**:

```yaml
Primary: support@company.com
Routing:
  - billing@company.com → Billing team
  - api@company.com → Engineering
  - hello@company.com → General inquiries
SLA:
  - Critical: 2 hours
  - High: 8 hours
  - Normal: 24 hours
  - Low: 48 hours
```

**Email Templates**:

```markdown
# Welcome Email

Subject: Welcome to [Product]! Here's how to get started

Hi [Name],

Welcome! Here's what to do first:

1. Complete setup: [Link]
2. Try this tutorial: [Link]
3. Join our community: [Link]

Need help? Reply to this email or check our help center: [Link]

[Your Name]
```

```markdown
# Issue Resolved

Subject: [Ticket #123] Resolved - [Issue Title]

Hi [Name],

Good news! Your issue is resolved.

**What we did**:
[Clear explanation]

**What you should see**:
[Expected result]

**If the problem returns**:
[Troubleshooting steps]

Was this helpful? [Yes] [No]

[Your Name]
```

### Chat Support

**In-App Chat Widget**:

```javascript
// Intercom, Drift, Crisp example
<script>
window.intercomSettings = {
  app_id: "YOUR_APP_ID",
  // Custom attributes
  email: user.email,
  user_id: user.id,
  created_at: user.createdAt,
  plan: user.plan,
  // Show relevant help articles
  help_center: {
    search_enabled: true
  }
};
</script>
```

**Chat SLA**:

- Business hours: 5-minute response
- After hours: Email auto-response
- Expected resolution: 1-3 messages

### Chatbot (AI-Powered)

**Decision Tree**:

```
User message →
  ├── Can answer with KB article? → Send article
  ├── Simple factual question? → AI answers
  ├── Complex issue? → Route to human
  └── Angry/escalated? → Priority human routing
```

**Implementation**:

```python
def handle_support_message(message, user_context):
    # 1. Search knowledge base
    kb_results = search_kb(message, top_k=3)

    if kb_results[0].score > 0.85:
        return {
            'type': 'article',
            'article': kb_results[0],
            'confidence': 'high'
        }

    # 2. Try AI response with context
    ai_response = generate_response(
        message=message,
        kb_context=kb_results,
        user_history=user_context
    )

    if ai_response.confidence > 0.8:
        return {
            'type': 'ai_response',
            'response': ai_response.text,
            'sources': kb_results
        }

    # 3. Route to human
    return {
        'type': 'human_handoff',
        'priority': calculate_priority(message, user_context),
        'suggested_agent': route_to_specialist(message)
    }
```

## Ticket Management

### Ticketing System Schema

```typescript
interface Ticket {
  id: string
  status: 'new' | 'open' | 'pending' | 'resolved' | 'closed'
  priority: 'low' | 'normal' | 'high' | 'critical'
  category: string // 'billing', 'technical', 'feature', etc.
  subject: string
  description: string
  requester: User
  assignee?: Agent
  tags: string[]
  created_at: Date
  updated_at: Date
  resolved_at?: Date
  first_response_at?: Date
  satisfaction_rating?: 1 | 2 | 3 | 4 | 5
}
```

### Auto-Routing Rules

```yaml
Routing Rules:
  - Condition: subject contains "billing" OR "payment"
    Action: Assign to billing-team
    Priority: high

  - Condition: user.plan == "enterprise"
    Action: Assign to enterprise-team
    Priority: high
    SLA: 2 hours

  - Condition: subject contains "API" OR "webhook"
    Action: Assign to engineering
    Tag: 'api-issue'

  - Condition: sentiment == "angry"
    Action: Priority routing
    Priority: critical
    Notify: support-manager
```

### Ticket Lifecycle

```
New → Open → Pending → Resolved → Closed
       ↓              ↑
       ← Reopen ←
```

**Status Definitions**:

- **New**: Just created, not yet viewed
- **Open**: Agent working on it
- **Pending**: Waiting for customer response
- **Resolved**: Solution provided, awaiting confirmation
- **Closed**: Issue confirmed resolved or auto-closed after 7 days

## Self-Service Tools

### Interactive Troubleshooters

```javascript
// Example: Connection troubleshooter
const troubleshooter = {
  start: {
    question: 'What problem are you experiencing?',
    options: [
      { text: "Can't connect", next: 'check_connection' },
      { text: 'Slow performance', next: 'check_performance' },
      { text: 'Error message', next: 'check_error' }
    ]
  },
  check_connection: {
    question: 'Can you access our website?',
    options: [
      { text: 'Yes', next: 'browser_check' },
      { text: 'No', action: 'show_status_page' }
    ]
  },
  browser_check: {
    question: 'Clear your browser cache and try again.',
    options: [
      { text: 'It worked!', action: 'problem_solved' },
      { text: 'Still not working', action: 'contact_support' }
    ]
  }
}
```

### In-App Guidance

```javascript
// Contextual help tooltips
const helpTooltips = {
  '/dashboard': {
    first_visit: {
      title: 'Welcome to your dashboard!',
      steps: [
        '1. View your key metrics here',
        "2. Click 'Add Widget' to customize",
        '3. Need help? Click the ? icon'
      ]
    }
  },
  '/settings/billing': {
    always_show: {
      payment_methods: 'We accept Visa, Mastercard, and AmEx',
      billing_cycle: 'Changes take effect next billing cycle'
    }
  }
}
```

## Support Metrics

### Key Metrics to Track

```typescript
interface SupportMetrics {
  // Response metrics
  first_response_time: {
    p50: number // median
    p90: number // 90th percentile
    p99: number
  }

  // Resolution metrics
  avg_resolution_time: number
  tickets_resolved_first_contact: number

  // Volume metrics
  tickets_created_today: number
  tickets_open: number
  tickets_overdue: number

  // Quality metrics
  customer_satisfaction_score: number // 1-5
  net_promoter_score: number // -100 to 100

  // Efficiency metrics
  self_service_rate: number // % resolved without ticket
  deflection_rate: number // % answered by KB/bot
  cost_per_ticket: number
}
```

### Target Benchmarks

```yaml
Excellent Support:
  first_response_time_p90: '< 2 hours'
  resolution_time_avg: '< 24 hours'
  self_service_rate: '> 70%'
  csat: '> 4.5/5'
  nps: '> 50'

Good Support:
  first_response_time_p90: '< 4 hours'
  resolution_time_avg: '< 48 hours'
  self_service_rate: '> 50%'
  csat: '> 4.0/5'
  nps: '> 30'
```

## Scaling Strategy

### Support Team Structure

```
Support Organization (at scale):

Support Manager (1)
├── Knowledge Base Lead (1)
│   └── Technical Writers (2-3)
├── Chat Support (Tier 1) (5-10)
│   ├── Handle 80% of issues
│   └── Escalate complex cases
├── Email Support (Tier 2) (3-5)
│   ├── Handle escalations
│   └── Complex troubleshooting
└── Specialist Support (Tier 3) (2-3)
    ├── API/Technical issues
    └── Enterprise customers
```

### When to Hire Support Staff

**Rule of Thumb**:

- 0-500 users: Founders handle it
- 500-2,000 users: 1 support person
- 2,000-5,000 users: 2-3 support people
- 5,000-20,000 users: 5-8 support people
- 20,000+ users: Build a team

**Better metric**: Support load

- Hire when: > 50 tickets/day or > 10 concurrent chats
- Each agent can handle: ~30-40 tickets/day or 8-10 chats/day

## Tools & Software

### Recommended Stack

**Ticketing**: Zendesk, Intercom, Help Scout, Freshdesk
**Knowledge Base**: GitBook, Notion, Confluence, Document360
**Chat**: Intercom, Drift, Crisp
**Chatbot AI**: OpenAI, Anthropic Claude, Dialogflow
**Community**: Discourse, Circle, Slack/Discord
**Analytics**: Mixpanel, Amplitude (for in-app behavior)

### Integration Example

```javascript
// Unified support API
class SupportSystem {
  async createTicket(data) {
    const ticket = await zendesk.createTicket(data)
    await analytics.track('support_ticket_created', {
      ticket_id: ticket.id,
      category: data.category,
      user_id: data.user_id
    })
    return ticket
  }

  async trackKBArticleView(article_id, user_id) {
    await analytics.track('kb_article_viewed', {
      article_id,
      user_id
    })

    // If user doesn't create ticket after viewing,
    // article was helpful (deflection)
  }
}
```

## Proactive Support

### Detect Issues Before Tickets

```javascript
// Monitor for patterns
async function detectPotentialIssues() {
  // Error spike detection
  const errorRate = await getErrorRate('last_hour')
  if (errorRate > 2 * avgErrorRate) {
    await notifySupport('Error spike detected')
    await displayStatusMessage("We're investigating an issue...")
  }

  // User struggle detection
  const strugglingUsers = await detectStrugglingUsers({
    criteria: ['repeated_failed_actions', 'long_time_on_page', 'back_and_forth_clicks']
  })

  if (strugglingUsers.length > 0) {
    await offerProactiveHelp(strugglingUsers)
  }
}
```

### Health Score Monitoring

```typescript
interface CustomerHealth {
  user_id: string
  health_score: number // 0-100
  signals: {
    usage_frequency: 'increasing' | 'stable' | 'declining'
    feature_adoption: number
    support_tickets_recent: number
    last_login: Date
    payment_status: 'current' | 'overdue'
  }
}

// Reach out proactively when health score drops
if (customer.health_score < 40) {
  await sendProactiveOutreach({
    type: 'check_in',
    message: "Haven't seen you in a while. Need help with anything?"
  })
}
```

## Quick Start Checklist

### Week 1: Foundation

- [ ] Set up support email (support@)
- [ ] Create basic FAQ (top 10 questions)
- [ ] Install chat widget
- [ ] Document known issues

### Week 2-3: Knowledge Base

- [ ] Choose KB platform
- [ ] Create getting started guide
- [ ] Document all features
- [ ] Add screenshots/GIFs
- [ ] Create troubleshooting section

### Week 4: Automation

- [ ] Set up auto-responders
- [ ] Create email templates
- [ ] Configure routing rules
- [ ] Add chatbot (basic)

### Ongoing

- [ ] Review ticket themes weekly
- [ ] Update KB based on common questions
- [ ] Track self-service rate
- [ ] Survey customer satisfaction
- [ ] Optimize response times

## Common Pitfalls

❌ **Building KB before having users**: Write docs based on actual questions, not assumptions
❌ **Over-automating too early**: Humans learn patterns; automate after seeing 50+ tickets on same topic
❌ **Poor search**: If users can't find answers, they'll submit tickets
❌ **No feedback loop**: Track which articles users view before submitting tickets
❌ **Ignoring mobile**: 40% of users will access support on mobile

## Success Criteria

You have great support when:

- ✅ 70%+ of users find answers without contacting support
- ✅ First response time < 2 hours during business hours
- ✅ Customer satisfaction > 4.5/5
- ✅ Support costs grow slower than user base
- ✅ Support team can focus on complex issues, not repetitive questions
