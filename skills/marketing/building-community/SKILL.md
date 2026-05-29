---
name: building-community
description: Building and growing developer communities from scratch to scale
sasmp_version: "1.4.0"
version: "2.0.0"
updated: "2025-01"
bonded_agent: 02-community-builder
bond_type: PRIMARY_BOND
---

# Building Developer Communities

Create **thriving developer communities** that grow organically and deliver value.

## Skill Contract

### Parameters
```yaml
parameters:
  required:
    - community_goal: string
    - target_platform: enum[discord, slack, github, discourse]
  optional:
    - initial_size_target: integer
    - budget: float
```

### Output
```yaml
output:
  launch_plan:
    strategy: markdown
    channel_structure: array[Channel]
    success_metrics: object
```

## Community Lifecycle

```
Planning → Launch → Growth → Maturity → Scale
    ↓        ↓        ↓         ↓         ↓
 Strategy  Seed    Engage   Programs  Leaders
           Users   Content  Champions Autonomy
```

## Platform Selection

| Platform | Best For | Size | Key Feature |
|----------|----------|------|-------------|
| **Discord** | Real-time, casual | 100-50K | Roles, threads |
| **Slack** | Professional, B2B | 100-10K | Integrations |
| **GitHub Discussions** | OSS projects | Any | Code-linked |
| **Discourse** | Long-form | 1K-100K | SEO, archives |

## Launch Strategy

### Pre-Launch (4-8 weeks)
```
1. Define community purpose and values
2. Choose platform and set up structure
3. Create welcome content and guidelines
4. Recruit 20-50 founding members
5. Seed initial conversations
```

### Launch Week
```
1. Announce across channels
2. Host welcome event (AMA, office hours)
3. Personally welcome every new member
4. Start daily engagement cadence
5. Gather early feedback
```

## Growth Tactics by Stage

| Stage | Tactic | Goal |
|-------|--------|------|
| 0-100 | Personal invitations | Quality seed |
| 100-500 | Content marketing | Organic growth |
| 500-2K | Events, partnerships | Momentum |
| 2K-10K | Champion program | Scale |
| 10K+ | Self-sustaining | Autonomy |

## Engagement Programs

- **Welcome Flow**: Onboarding for new members
- **Recognition**: Badges, roles, shoutouts
- **Champions**: Ambassador program
- **Events**: Office hours, AMAs, hackathons
- **Content**: Member spotlights, tutorials

## Retry Logic

```yaml
retry_patterns:
  low_engagement:
    strategy: "Personal outreach to top 20 members"
    escalation: "AMA or exclusive event"

  member_churn:
    strategy: "Exit survey, re-engagement campaign"

  toxic_behavior:
    strategy: "Private warning, then public reminder"
```

## Failure Modes & Recovery

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| Ghost town | <5 messages/day | Seed content, personal pings |
| Toxic culture | Complaints | Enforce CoC, public statement |
| Off-topic drift | Unrelated posts | Redirect, add channels |

## Debug Checklist

```
□ Community purpose clearly stated?
□ Platform analytics configured?
□ Code of conduct visible?
□ Welcome message set up?
□ Initial content seeded?
□ Moderator coverage scheduled?
□ Recognition system active?
```

## Test Template

```yaml
test_community_building:
  unit_tests:
    - test_onboarding_flow:
        assert: "Welcome message within 1 min"

  integration_tests:
    - test_member_journey:
        assert: "First post → Reply within 24h"
```

## Success Metrics

| Metric | Target |
|--------|--------|
| Monthly Active Users | 30%+ of total |
| Messages per member | 5+ per month |
| Response time | <4 hours |
| Member retention | 80%+ at 30 days |

## Observability

```yaml
metrics:
  - total_members: integer
  - mau: integer
  - messages_per_day: integer
  - response_time_avg: duration
```

See `assets/` for community templates.
