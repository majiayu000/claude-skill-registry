---
name: faion-conversion-optimizer
description: "Conversion optimization: landing pages, CRO, funnels, PLG, onboarding flows."
user-invocable: false
allowed-tools: Read, Write, Edit, Task, WebSearch, AskUserQuestion, TodoWrite, Glob
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Conversion Optimizer Domain Skill

Conversion rate optimization: landing pages, funnels, free trial optimization, product-led growth, onboarding flows.

## Purpose

Orchestrates conversion optimization: landing page design, CRO tactics, funnel optimization, free trial conversion, PLG mechanics, onboarding flows.

## Context Discovery

### Auto-Investigation

Check these project signals to understand conversion optimization context:

| Signal | Location | What to Look For |
|--------|----------|------------------|
| Landing pages | Website, marketing pages | Current landing pages, conversion rates, CTA placement |
| Funnel data | Analytics, funnel reports | Conversion funnel metrics, drop-off points, bottlenecks |
| Free trial | Product, signup flow | Trial length, activation rate, trial-to-paid conversion |
| PLG mechanics | Product features, docs | Self-service signup, product-led onboarding, activation |
| Onboarding | User flows, analytics | Onboarding sequence, time-to-value, completion rates |
| A/B tests | Experiment docs, analytics | Previous CRO tests, winning variations, learnings |
| User feedback | Support tickets, surveys | Friction points, confusion, feature requests |

### Discovery Questions

```yaml
question: "What's your primary CRO goal?"
header: "CRO Goal"
multiSelect: false
options:
  - label: "Optimize landing pages"
    description: "Landing page design, copywriting, CRO tactics"
  - label: "Improve funnel conversion"
    description: "Funnel analysis, drop-off optimization, A/B testing"
  - label: "Boost free trial conversion"
    description: "Trial optimization, activation, trial-to-paid"
  - label: "Implement PLG strategy"
    description: "Product-led growth, self-service, onboarding automation"
```

```yaml
question: "What's your current conversion rate?"
header: "Conversion Baseline"
multiSelect: false
options:
  - label: "Below 1%"
    description: "Fundamental CRO, landing page redesign, messaging fix"
  - label: "1-3%"
    description: "Tactical improvements, funnel optimization, A/B testing"
  - label: "3-5%"
    description: "Advanced tactics, micro-optimizations, segmentation"
  - label: "Above 5%"
    description: "Marginal gains, sophisticated testing, personalization"
```

```yaml
question: "What type of funnel do you have?"
header: "Funnel Type"
multiSelect: false
options:
  - label: "Marketing → Sales funnel"
    description: "Lead generation, landing pages, sales handoff"
  - label: "Self-service signup"
    description: "Product-led growth, onboarding flows, activation"
  - label: "Free trial → Paid"
    description: "Trial optimization, upgrade mechanics, feature gating"
  - label: "Freemium → Premium"
    description: "PLG tactics, upgrade triggers, feature value demonstration"
```

## When to Use

| Scenario | Methodologies |
|----------|---------------|
| Landing page | growth-landing-page-design → growth-conversion-optimization |
| Free trial | growth-free-trial-optimization |
| Funnel optimization | funnel-basics-framework → funnel-tactics-basics → funnel-tactics-advanced |
| PLG strategy | plg-basics → plg-implementation-guide → plg-optimization-tactics |
| Onboarding | onboarding-flows → plg-implementation-guide |
| Community-led | community-led-growth → plg-basics |

## Methodologies (13)

### Landing Pages & CRO (3)
- growth-landing-page-design.md
- growth-conversion-optimization.md
- growth-free-trial-optimization.md

### Funnels (4)
- funnel-basics-framework.md
- funnel-basics-examples.md
- funnel-tactics-basics.md
- funnel-tactics-advanced.md

### Product-Led Growth (5)
- plg-basics.md
- plg-implementation-guide.md
- plg-metrics.md
- plg-optimization-tactics.md
- community-led-growth.md

### Onboarding (1)
- onboarding-flows.md

## References

- [landing-page.md](references/landing-page.md) - Landing page frameworks (AIDA, PAS, etc.)

## Related Skills

- faion-marketing-manager (parent orchestrator)
- faion-growth-marketer (metrics, A/B testing)
- faion-content-marketer (copywriting for landing pages)
- faion-ux-ui-designer (landing page design)

---

*Conversion Optimizer v1.0 | 13 Methodologies*
