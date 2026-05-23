---
name: personal-branding
description: Building and maintaining a personal brand in the developer community
sasmp_version: "1.4.0"
version: "2.0.0"
updated: "2025-01"
bonded_agent: 06-developer-advocate
bond_type: SECONDARY_BOND
---

# Personal Branding for DevRel

Build a **recognizable personal brand** that amplifies your DevRel impact.

## Skill Contract

### Parameters
```yaml
parameters:
  required:
    - brand_element: enum[identity, voice, presence, network]
    - platforms: array[string]
  optional:
    - audit_existing: boolean
    - target_persona: string
```

### Output
```yaml
output:
  brand_strategy:
    identity_guide: object
    content_voice: object
    platform_priorities: array[Platform]
```

## Brand Components

### Identity
```
Name + Avatar + Bio + Voice = Brand Identity
  ↓       ↓       ↓      ↓
Consistent across all platforms
```

### Bio Formula
```
[Role] at [Company] | [Expertise] | [Personality]

Examples:
"Developer Advocate @Stripe | API design enthusiast | Coffee-powered coder ☕"
"Senior DevRel @Vercel | Making React deployment simple | Speaker | Dog dad 🐕"
```

## Platform Presence

### Consistency Checklist
- [ ] Same handle across platforms
- [ ] Recognizable avatar/headshot
- [ ] Consistent bio theme
- [ ] Link to primary platform
- [ ] Same color scheme (if applicable)

### Platform Priorities

| Platform | Priority | Focus |
|----------|----------|-------|
| Twitter/X | High | Daily engagement |
| LinkedIn | High | Professional credibility |
| GitHub | High | Code credibility |
| YouTube | Medium | Tutorial authority |
| Blog | Medium | Long-form SEO |
| Newsletter | Medium | Owned audience |

## Content Voice

### Finding Your Voice
```
Technical + Personality + Values = Your Voice

Examples:
- Technical + Humor = "Here's a bug I spent 6 hours on... 🤦"
- Technical + Teaching = "Let me break this down step by step..."
- Technical + Opinion = "Hot take: You don't need Kubernetes"
```

### Voice Guidelines
| Do | Don't |
|----|-------|
| Be authentic | Copy others' style |
| Share failures | Only show wins |
| Give opinions | Be controversial for clicks |
| Help others | Only self-promote |

## Networking Strategy

### Building Genuine Connections
1. **Engage first**: Comment on their content
2. **Add value**: Share useful insights
3. **Be patient**: Relationships take time
4. **Follow through**: Deliver on promises

### Key Relationships
- Peers in DevRel
- Developers you serve
- Industry analysts
- Conference organizers
- Media/journalists

## Maintaining Your Brand

### Daily Habits
- Post/share content
- Engage with others
- Answer questions
- Stay informed

### Weekly Review
- Check analytics
- Review feedback
- Plan next week
- Update content calendar

## Retry Logic

```yaml
retry_patterns:
  low_visibility:
    strategy: "Increase posting frequency"
    fallback: "Engage more with others"

  inconsistent_presence:
    strategy: "Batch content creation"
    fallback: "Focus on fewer platforms"

  negative_perception:
    strategy: "Address feedback directly"
    fallback: "Pivot messaging"
```

## Failure Modes & Recovery

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| Brand confusion | Mixed messaging | Clarify positioning |
| Low engagement | Declining metrics | Refresh content strategy |
| Burnout | Reduced output | Batch work, take breaks |

## Debug Checklist

```
□ Identity consistent across platforms?
□ Bio clearly communicates value?
□ Voice authentic and distinctive?
□ Posting cadence sustainable?
□ Engaging with community regularly?
□ Analytics being reviewed?
```

## Test Template

```yaml
test_personal_branding:
  unit_tests:
    - test_brand_consistency:
        assert: "Same across all platforms"
    - test_voice_authenticity:
        assert: "Unique and recognizable"

  integration_tests:
    - test_audience_growth:
        assert: "Consistent follower increase"
```

## Observability

```yaml
metrics:
  - followers_total: integer
  - engagement_rate: float
  - brand_mentions: integer
  - inbound_connections: integer
```

See `assets/` for networking templates.
