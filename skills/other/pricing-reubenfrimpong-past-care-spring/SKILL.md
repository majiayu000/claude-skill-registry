---
name: pricing
description: PastCare pricing model, calculations, and tier information. Use when discussing pricing, subscription tiers, GHS/USD conversion, billing amounts, or marketing materials that mention prices.
user-invocable: false
---

# PastCare Pricing Model

## Pricing Formula (CRITICAL)

**GHS Price = ceil(USD Price × Exchange Rate)**

- Exchange rate is set by SUPERADMIN (default: 12.00)
- Always round UP using ceiling function (`Math.ceil()`)
- USD prices are the BASE prices stored in the system
- GHS is calculated dynamically based on current exchange rate

### Calculation Example
```
USD Price: $5.99
Exchange Rate: 12.00
Calculation: ceil(5.99 × 12) = ceil(71.88) = 72
GHS Price: GHS 72
```

## Current Tier Pricing

| Tier | Members | USD (Base) | GHS (at 12.00 rate) |
|------|---------|------------|---------------------|
| **Small** | 1-200 | $5.99 | GHS 72 |
| **Standard** | 201-500 | $9.99 | GHS 120 |
| **Professional** | 501-1000 | $13.99 | GHS 168 |
| **Enterprise** | 1001+ | $17.99 | GHS 216 |

### Calculation Breakdown
| Tier | USD × Rate | Ceiling | GHS |
|------|------------|---------|-----|
| Small | 5.99 × 12 = 71.88 | ceil(71.88) | **72** |
| Standard | 9.99 × 12 = 119.88 | ceil(119.88) | **120** |
| Professional | 13.99 × 12 = 167.88 | ceil(167.88) | **168** |
| Enterprise | 17.99 × 12 = 215.88 | ceil(215.88) | **216** |

## Billing Intervals

| Interval | Discount (USD) | Discount (GHS at 12.00) |
|----------|----------------|-------------------------|
| Monthly | $0 | GHS 0 |
| Quarterly | $1.50 off | GHS 18 off |
| Biannual | $4.50 off | GHS 54 off |
| Annual | $12.00 off | GHS 144 off |

## Key Business Rules

1. **NO FREE PLAN** - Subscription required from day 1
2. **All tiers have IDENTICAL features** - Only member limit differs
3. **Partnership codes** - Only way to grant free access (admin-controlled)
4. **GHS primary display** - USD shown as secondary reference
5. **Exchange rate configurable** - SUPERADMIN can update rate

## When Exchange Rate Changes

If SUPERADMIN changes the exchange rate, recalculate GHS prices:

```java
// Backend calculation
BigDecimal ghsPrice = usdPrice.multiply(exchangeRate)
    .setScale(0, RoundingMode.CEILING);
```

```typescript
// Frontend calculation
const ghsPrice = Math.ceil(usdPrice * exchangeRate);
```

## Contact Information

- **Support Email**: pastcareapp@gmail.com
- **Phone/WhatsApp**: +233 24 674 8016
- **Website**: www.pastcare.app
- **Register URL**: www.pastcare.app/register

## Tagline

**"Stop Counting. Start Caring."**

## Files to Update When Pricing Changes

If USD base prices or exchange rate changes, update these files:
- `PRICING_MODEL_REVISED.md`
- `CLAUDE.md` (Pricing Model section)
- `MARKETING_STRATEGY.md`
- `marketing/pastcare-one-pager.html`
- `marketing/outreach-messages.md`
- Database: `congregation_pricing_tiers` table
