---
name: faion-smm-manager
description: "Social media: content strategy, community building, organic growth."
user-invocable: false
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# SMM Manager Skill (Claude)

## Overview
This skill orchestrates all organic social media activities. It is used by the `faion-social-agent` to develop content strategies, build communities, and grow an organic presence on various social networks.

## Context Discovery

### Auto-Investigation

Check these project signals to understand SMM context:

| Signal | Location | What to Look For |
|--------|----------|------------------|
| Social profiles | Twitter, LinkedIn, Instagram, Threads | Follower count, engagement rate, posting frequency |
| Content strategy | `.aidocs/product_docs/article-lists/` | Social content calendar, themes, messaging |
| Analytics | Platform analytics, social tools | Engagement metrics, reach, follower growth |
| Community | Discord, Slack, forums | Community size, engagement, moderation |
| Content library | Social media, content archives | Published posts, top performers, content quality |
| Brand voice | Brand guidelines, docs | Tone, messaging, visual identity |
| Competitor presence | Competitor social profiles | Competitor activity, engagement, tactics |

### Discovery Questions

```yaml
question: "Which social platform is your priority?"
header: "Social Platform"
multiSelect: false
options:
  - label: "Twitter/X"
    description: "Threads, real-time engagement, community building"
  - label: "LinkedIn"
    description: "Professional content, thought leadership, B2B networking"
  - label: "Instagram"
    description: "Visual content, Reels, Stories, organic growth"
  - label: "Threads"
    description: "Conversational content, community engagement"
```

```yaml
question: "What's your social media maturity?"
header: "SMM Maturity"
multiSelect: false
options:
  - label: "Starting from scratch"
    description: "Social media strategy, platform selection, initial content"
  - label: "Active but small following"
    description: "Growth tactics, engagement optimization, content strategy"
  - label: "Established presence"
    description: "Community building, scaling content, cross-platform"
  - label: "Large following"
    description: "Advanced tactics, community management, monetization"
```

```yaml
question: "What's your primary social goal?"
header: "Social Goal"
multiSelect: false
options:
  - label: "Grow followers"
    description: "Platform-specific growth tactics, viral content, engagement"
  - label: "Build community"
    description: "Community building, engagement, moderation, value creation"
  - label: "Drive traffic/conversions"
    description: "Traffic generation, CTA optimization, funnel integration"
  - label: "Establish thought leadership"
    description: "Content strategy, authority building, networking"
```

## Quick Reference

| If you need... | Use | File |
|----------------|-----|------|
| Overall social strategy | Social Media Strategy | growth-social-media-strategy.md |
| Grow Twitter/X audience | Twitter/X Growth | growth-twitter-x-growth.md |
| Build LinkedIn presence | LinkedIn Strategy | growth-linkedin-strategy.md |
| Grow Instagram organically | Instagram Organic Growth | growth-instagram-organic-growth.md |
| Launch on Threads | Threads Strategy | growth-threads-strategy.md |
| Build community engagement | Community Building | growth-community-building.md |

### Platform Quick Guide

| Platform | Content Type | Frequency | Methodology |
|----------|--------------|-----------|-------------|
| Twitter/X | Threads, insights, takes | 3-5x/day | growth-twitter-x-growth.md |
| LinkedIn | Long-form, insights | 1x/day | growth-linkedin-strategy.md |
| Instagram | Reels, Carousels | 1-2x/day | growth-instagram-organic-growth.md |
| Threads | Conversations, quick takes | 2-3x/day | growth-threads-strategy.md |

### Common Workflows

| Goal | Sequence |
|------|----------|
| **Social Media Launch** | 1) growth-social-media-strategy.md → 2) Platform-specific → 3) growth-community-building.md |
| **Grow Specific Platform** | 1) Platform-specific methodology → 2) growth-community-building.md → 3) Iterate |

## Methodologies
- **growth-social-media-strategy.md**: Overall social media strategy.
- **growth-community-building.md**: Strategies for building a community.
- **growth-twitter-x-growth.md**: Growing a presence on Twitter/X.
- **growth-linkedin-strategy.md**: Content and growth on LinkedIn.
- **growth-instagram-organic-growth.md**: Organic growth strategies for Instagram.
- **growth-threads-strategy.md**: Strategy for the Threads platform.
