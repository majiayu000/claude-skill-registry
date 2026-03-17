---
name: ads-management
description: Activate for paid advertising campaigns on Google Ads, Meta Ads, LinkedIn Ads, TikTok Ads. Includes ad copywriting, audience targeting, budget optimization, A/B testing, and ROAS tracking. Used by ads-specialist and campaign-manager agents.
license: MIT
---

# Ads Management

Paid advertising campaign creation, optimization, and performance tracking.

## When to Use

- Paid ad campaign creation
- Ad copywriting
- Audience targeting setup
- Budget optimization
- A/B testing strategy
- ROAS/CPA tracking
- Platform-specific ads

## Core Capabilities

### Platform Specifications
Load: `references/platform-specs.md`

### Ad Copy Templates
Load: `references/ad-copy-templates.md`

### Audience Targeting
Load: `references/audience-targeting.md`

### Optimization Playbook
Load: `references/optimization-playbook.md`

## Quick Reference

| Platform | Ad Types | Min Budget |
|----------|----------|------------|
| Google | Search, Display, Video | $10/day |
| Meta | Feed, Stories, Reels | $5/day |
| LinkedIn | Sponsored, Message | $10/day |
| TikTok | In-Feed, TopView | $20/day |

**Key Metrics:** CTR, CVR, CPC, CPM, ROAS, CPA

## Workflow

### Campaign Setup
1. Define objective (awareness/traffic/conversions)
2. Set budget and schedule
3. Create audience segments
4. Write ad copy variations
5. Design creatives
6. Set up tracking pixels
7. Launch and monitor

### Optimization Cycle
1. Review performance (daily)
2. Pause underperformers
3. Scale winners
4. Test new variations
5. Adjust bids/budgets

## Output Format

```markdown
## Ad Campaign: [Name]

**Platform:** [Google/Meta/etc.]
**Objective:** [Conversions/Traffic/etc.]
**Budget:** $[X]/day
**Audience:** [Targeting details]

### Ad Copy
Headline: [text]
Description: [text]
CTA: [button text]

### Targeting
[Audience specs]
```

## Report Output

**Activate:** `assets-organizing` skill for report file paths

Ads reports go to `assets/reports/ads/{date}-{platform}-report.md`

## Skill Dependencies

**Related Skills:** creativity, assets-organizing (report organization)

## Best Practices

1. Start small, scale winners
2. Test one variable at a time
3. Audience > Creative > Copy
4. Track conversions, not clicks
5. Negative keywords/exclusions matter
