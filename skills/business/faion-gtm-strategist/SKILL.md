---
name: faion-gtm-strategist
description: "GTM strategy: product launches, positioning, pricing, partnerships, customer success."
user-invocable: false
allowed-tools: Read, Write, Edit, Task, WebSearch, AskUserQuestion, TodoWrite, Glob
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# GTM Strategist Domain Skill

Go-to-market strategy, product launches, market positioning, pricing, partnerships, customer success operations.

## Purpose

Orchestrates GTM activities: market entry, product launches, positioning strategy, pricing models, partnership programs, customer success, and operational legal/financial aspects.

## Context Discovery

### Auto-Investigation

Check these project signals to understand GTM context:

| Signal | Location | What to Look For |
|--------|----------|------------------|
| GTM docs | `.aidocs/product_docs/gtm-manifest/` | Existing GTM strategy, target market, positioning |
| Launch plans | `.aidocs/backlog/`, `.aidocs/todo/` | Features ready for launch, product milestones |
| Content calendar | `.aidocs/product_docs/article-lists/` | Content strategy, announcement timing |
| Analytics | `docs/`, `README.md` | Current metrics, user data, conversion rates |
| Pricing | `README.md`, API docs | Current pricing model, subscription tiers |
| Partnerships | `docs/partners/`, `.aidocs/` | Existing partnerships, affiliate programs |
| Customer success | `docs/support/`, knowledge base | CS operations, metrics, support channels |

### Discovery Questions

```yaml
question: "What's your primary GTM goal?"
header: "GTM Goal"
multiSelect: false
options:
  - label: "Launch new product"
    description: "Product Hunt, Hacker News, press coverage, initial positioning"
  - label: "Enter new market"
    description: "Market positioning, pricing strategy, competitive analysis"
  - label: "Build partnerships"
    description: "Partnership strategy, affiliate programs, integration ecosystem"
  - label: "Scale customer success"
    description: "CS operations, metrics, upselling, churn prevention"
```

```yaml
question: "What's your launch timeline?"
header: "Launch Stage"
multiSelect: false
options:
  - label: "Planning (3+ months)"
    description: "Strategy, positioning, pricing, partnerships"
  - label: "Pre-launch (1-3 months)"
    description: "Press outreach, content prep, community building"
  - label: "Launch week"
    description: "Product Hunt, Hacker News, press coverage execution"
  - label: "Post-launch"
    description: "Customer success, metrics tracking, optimization"
```

```yaml
question: "What's your business model?"
header: "Business Model"
multiSelect: false
options:
  - label: "SaaS subscription"
    description: "Subscription models, MRR optimization, churn prevention"
  - label: "Freemium/PLG"
    description: "Free trial optimization, activation, conversion funnels"
  - label: "One-time purchase"
    description: "Pricing strategy, upselling, cross-selling"
  - label: "Marketplace/Platform"
    description: "Partnership strategy, affiliate programs, revenue share"
```

## When to Use

| Scenario | Methodologies |
|----------|---------------|
| Product launch | growth-gtm-strategy → growth-product-hunt-launch → growth-hacker-news-launch |
| Market positioning | growth-brand-positioning → growth-gtm-strategy |
| Pricing strategy | ops-pricing-strategy → ops-subscription-models |
| Partnership program | ops-partnership-strategy → growth-affiliate-marketing |
| Customer success | ops-customer-success-basics → ops-customer-success-metrics |
| Platform launch | growth-product-hunt-launch, growth-hacker-news-launch, growth-indiehackers-strategy |
| Press & PR | growth-press-coverage → growth-influencer-marketing |
| Outreach | growth-cold-outreach → growth-influencer-marketing |
| Annual planning | ops-annual-planning-process → ops-annual-planning-templates |
| Legal/compliance | ops-legal-basics → ops-legal-compliance |
| Financial planning | ops-financial-basics → ops-financial-planning |
| Tax compliance | ops-tax-basics → ops-tax-compliance |

## Methodologies (26)

### GTM & Launch (6)
- growth-gtm-strategy.md
- growth-brand-positioning.md
- growth-product-hunt-launch.md
- growth-hacker-news-launch.md
- growth-indiehackers-strategy.md
- growth-app-store-optimization.md

### Pricing & Business Model (4)
- ops-pricing-strategy.md
- ops-subscription-models.md
- ops-financial-basics.md
- ops-financial-planning.md

### Press & Outreach (3)
- growth-press-coverage.md
- growth-cold-outreach.md
- growth-influencer-marketing.md

### Partnerships (2)
- ops-partnership-strategy.md
- growth-affiliate-marketing.md

### Planning (2)
- ops-annual-planning-process.md
- ops-annual-planning-templates.md

### Customer Success (4)
- ops-customer-success-basics.md
- ops-customer-success-metrics.md
- ops-customer-support.md
- ops-upselling-cross-selling.md

### Legal & Compliance (5)
- ops-legal-basics.md
- ops-legal-compliance.md
- ops-legal-compliance-checklist.md
- ops-tax-basics.md
- ops-tax-compliance.md

## References

- [gtm-strategy.md](references/gtm-strategy.md) - GTM planning, positioning, launch
- [growth-operations.md](references/growth-operations.md) - Operations, pricing, partnerships

## Related Skills

- faion-marketing-manager (parent orchestrator)
- faion-content-marketer (content for GTM)
- faion-growth-marketer (metrics, experiments)
- faion-researcher (market research)
- faion-product-manager (product positioning)

---

*GTM Strategist v1.0 | 26 Methodologies*
