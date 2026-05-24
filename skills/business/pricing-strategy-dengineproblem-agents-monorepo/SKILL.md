---
name: pricing-strategy
description: Эксперт по ценообразованию. Используй для pricing models, value-based pricing и monetization strategies.
---

# Pricing Strategy Expert

Strategic expertise in SaaS pricing, monetization models, and value-based pricing.

## Pricing Models

```yaml
pricing_models:
  per_user:
    description: "Charge per active user/seat"
    pros: ["Predictable revenue", "Easy to understand"]
    cons: ["Can limit adoption", "Encourages seat sharing"]
    best_for: "Collaboration tools, CRM"
    examples: "Slack, Salesforce"

  usage_based:
    description: "Charge based on consumption"
    pros: ["Low barrier to entry", "Fair value exchange"]
    cons: ["Revenue unpredictability", "Complex billing"]
    best_for: "API services, infrastructure"
    examples: "AWS, Twilio, Stripe"

  tiered:
    description: "Feature-based plan tiers"
    pros: ["Clear upgrade path", "Natural segmentation"]
    cons: ["Complexity risk", "Feature arbitrage"]
    best_for: "Most B2B SaaS"
    examples: "HubSpot, Zoom"

  freemium:
    description: "Free tier with paid upgrades"
    pros: ["Viral growth potential", "Product-led growth"]
    cons: ["Conversion challenges", "Free user costs"]
    best_for: "PLG companies"
    examples: "Dropbox, Notion"
```

## Value-Based Pricing

### Research Methods

```yaml
pricing_research:
  van_westendorp:
    questions:
      - "At what price would this be too cheap?"
      - "At what price would this be a bargain?"
      - "At what price would this be expensive?"
      - "At what price would this be too expensive?"

  conjoint_analysis:
    purpose: "Understand feature value trade-offs"
    output: "Willingness to pay per feature"

  customer_interviews:
    questions:
      - "How do you currently solve this problem?"
      - "What would you pay for [benefit]?"
      - "What budget do you have for this?"
```

## Tier Design

```yaml
tier_structure:
  free:
    purpose: "Acquisition, product trial"
    includes: "Core functionality, limited usage"

  starter:
    target: "Individual users, small teams"
    features: "Core + basic analytics"

  professional:
    target: "Growing teams"
    features: "Advanced features, integrations"

  enterprise:
    target: "Large organizations"
    features: "Custom, security, SLA, dedicated support"
```

## Psychological Pricing

```yaml
pricing_psychology:
  anchoring: "Show highest price first"
  charm_pricing: "$99 instead of $100"
  price_framing: "$3/day vs $90/month"
  bundling: "Bundle price < sum of parts"
  annual_discount: "15-20% for annual payment"
```

## Metrics

```yaml
pricing_metrics:
  arpu: "MRR / Active Users"
  arpa: "MRR / Active Accounts"
  price_realization: "Actual Price / List Price (target >90%)"
  discount_rate: "Average discount given (target <15%)"
```

## Лучшие практики

1. **Value first** — цена на основе ценности для клиента
2. **Segment pricing** — разные сегменты = разная готовность платить
3. **Test everything** — данные важнее интуиции
4. **Annual contracts** — стимулируйте годовые контракты
5. **Simple packaging** — сложность убивает конверсию
6. **Regular reviews** — пересматривайте цены ежегодно
