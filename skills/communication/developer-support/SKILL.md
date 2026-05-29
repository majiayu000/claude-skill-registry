---
name: developer-support
description: Developer support systems including forums, office hours, and FAQ management
sasmp_version: "1.4.0"
version: "2.0.0"
updated: "2025-01"
bonded_agent: 06-developer-advocate
bond_type: SECONDARY_BOND
---

# Developer Support

Build **effective support systems** that help developers succeed and scale.

## Skill Contract

### Parameters
```yaml
parameters:
  required:
    - support_type: enum[question, bug, feature, escalation]
    - context: string
  optional:
    - urgency: enum[low, medium, high, critical]
    - channel: enum[forum, discord, ticket, office_hours]
```

### Output
```yaml
output:
  response:
    answer: string
    resources: array[Link]
    follow_up: array[Action]
```

## Support Channels

| Channel | Response Time | Best For |
|---------|---------------|----------|
| Docs/FAQ | Instant | Self-service |
| Forum/Discord | 4-24 hours | Community Q&A |
| Office Hours | Scheduled | Complex issues |
| Support Tickets | 24-48 hours | Bugs/urgent |

## Support Tier Model

```
Tier 0: Self-Service
├── Documentation
├── FAQ
├── Knowledge Base
└── Search

Tier 1: Community
├── Forums
├── Discord/Slack
└── Stack Overflow

Tier 2: DevRel Team
├── Office Hours
├── Direct Outreach
└── Webinars

Tier 3: Engineering
├── Bug Reports
├── Feature Requests
└── Architecture Reviews
```

## Office Hours Best Practices

### Format
- Weekly or bi-weekly
- 30-60 minutes
- Open Q&A or themed topics
- Record for those who can't attend

### Running Sessions
1. **Start on time** - Respect schedules
2. **Screen share** - Show, don't just tell
3. **Take notes** - Action items to follow up
4. **Be honest** - "I'll find out" is OK

## FAQ Management

### Creating Effective FAQs
```markdown
Q: How do I authenticate with the API?

A: You can authenticate using API keys or OAuth 2.0:

**API Keys** (simplest)
curl -H "Authorization: Bearer YOUR_API_KEY" ...

**OAuth 2.0** (for user data)
[See our OAuth guide →](/docs/oauth)

Related: [Authentication errors](/docs/errors#auth)
```

### FAQ Sources
- Support tickets (recurring issues)
- Community questions
- Search queries
- User feedback

## Retry Logic

```yaml
retry_patterns:
  unresolved_question:
    strategy: "Escalate to specialist"

  user_frustrated:
    strategy: "Personal outreach, expedite"

  recurring_issue:
    strategy: "Create FAQ, update docs"
```

## Failure Modes & Recovery

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| Slow response | >24h wait | Prioritize, apologize |
| Wrong answer | User correction | Fix, thank user |
| No resolution | Multiple back-forth | Escalate |

## Debug Checklist

```
□ Problem clearly understood?
□ Docs checked first?
□ Similar issues in history?
□ Reproducible steps?
□ Workaround available?
□ Escalation path clear?
```

## Test Template

```yaml
test_developer_support:
  unit_tests:
    - test_response_time:
        assert: "<24h for community"
    - test_answer_accuracy:
        assert: "Solves problem"

  integration_tests:
    - test_escalation_flow:
        assert: "Reaches specialist"
```

## Support Metrics

| Metric | Target |
|--------|--------|
| Response time | <24 hours |
| Resolution rate | >80% |
| CSAT score | >4.0/5 |
| Ticket deflection | >60% |

## Observability

```yaml
metrics:
  - tickets_resolved: integer
  - response_time_avg: duration
  - csat_score: float
  - deflection_rate: float
```

See `assets/` for support templates.
