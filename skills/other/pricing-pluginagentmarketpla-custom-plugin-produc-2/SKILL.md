---
name: pricing
version: "2.0.0"
description: Product pricing strategies, monetization models, and revenue optimization for SaaS and digital products.
sasmp_version: "1.3.0"
bonded_agent: 01-strategy-vision
bond_type: PRIMARY_BOND
parameters:
  - name: pricing_model
    type: string
    enum: [freemium, subscription, usage_based, tiered, perpetual]
    required: true
  - name: target_segment
    type: string
    enum: [smb, mid_market, enterprise, consumer]
retry_logic:
  max_attempts: 3
  backoff: exponential
logging:
  level: info
  hooks: [start, complete, error]
---

# Pricing Skill

Develop effective pricing strategies and monetization models. Master value-based pricing, tier design, and revenue optimization.

## Pricing Models

### Freemium

```
Free Tier:
- Basic features
- Limited usage (100/month)
- Community support

Paid Tier ($X/month):
- All features
- Unlimited usage
- Priority support
```

**Metrics:**
- Free-to-paid conversion: 2-5%
- Time to convert: 7-30 days

### Subscription (SaaS)

| Tier | Monthly | Annual | Features |
|------|---------|--------|----------|
| Starter | $29 | $290 | Basic |
| Pro | $99 | $990 | + Analytics |
| Business | $299 | $2990 | + API |
| Enterprise | Custom | Custom | + SLA |

### Usage-Based

```
Pricing Formula:
Base fee + (Usage × Per-unit rate)

Example (API):
$49 base + ($0.001 × API calls)
```

## Pricing Strategy

### Value-Based Pricing

**Formula:**
```
Your Price = (Customer Value Delivered) × (Capture Rate)

Example:
Customer saves $100K/year with your product
You capture 10% = $10K/year price
```

### Price Sensitivity Analysis

**Van Westendorp Method:**
1. At what price is this too expensive?
2. At what price is this too cheap?
3. At what price is this expensive but worth it?
4. At what price is this a bargain?

## Unit Economics

### Key Metrics

```
LTV = ARPU × Gross Margin % / Churn %

Example:
$100 ARPU × 80% GM / 5% churn = $1,600 LTV

CAC Target: LTV/3 = $533 max CAC
Payback: 12 months max
```

### Revenue Forecasting

```
Month | New MRR | Churn | Net New | Total MRR
------|---------|-------|---------|----------
1     | $10K    | $0    | $10K    | $10K
2     | $10K    | $0.5K | $9.5K   | $19.5K
3     | $12K    | $1K   | $11K    | $30.5K
...
```

## Troubleshooting

### Yaygın Hatalar & Çözümler

| Hata | Olası Sebep | Çözüm |
|------|-------------|-------|
| Low conversion | Price too high | A/B test lower price |
| High churn | Wrong segment | Re-segment, adjust ICP |
| Revenue flat | No upsell path | Add expansion revenue |
| Margin low | Cost structure | Optimize, raise prices |

### Debug Checklist

```
[ ] LTV/CAC ratio > 3 mi?
[ ] Payback period < 12mo mu?
[ ] Gross margin > 70% mi?
[ ] Pricing tested with customers mi?
[ ] Competitor pricing analyzed mi?
```

### Recovery Procedures

1. **Low Conversion** → Price sensitivity research
2. **High Churn** → Customer exit interviews
3. **Flat Revenue** → Upsell/expansion strategy

## Learning Outcomes

- Design effective pricing models
- Calculate unit economics
- Analyze price sensitivity
- Optimize monetization
- Forecast revenue impact
