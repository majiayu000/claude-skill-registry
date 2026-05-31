---
name: ecommerce-seller-info
description: "Extract seller or merchant profile data from marketplace platform seller pages. Returns seller name, rating, review count, positive feedback percentage, joined date, and return policy. Works on Amazon seller pages, eBay seller pages, and any e-commerce site with seller profiles. Use when: seller information, merchant profile, seller rating, marketplace seller data, seller details, vendor profile, store information, seller feedback, merchant rating, seller review count, get seller info, ebay seller page, amazon seller profile, marketplace vendor analysis, seller research."
---

# E-commerce — Seller Info

> Seller/merchant profile URL → seller name, rating, review count, feedback, joined date, return policy

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract seller profile information from marketplace platform seller or storefront pages using JSON-LD structured data and platform-specific DOM patterns.

## Prerequisites

- Target browser is open and connected
- No login required for public seller profile pages

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. Use the bash tool for execution.

### DOM: Extract seller profile from current seller page

Navigate to the seller profile URL first, then extract:

```bash
eval "$(python scripts/extract-seller.py)"
```

Output example:
```json
{
  "url": "https://www.amazon.com/shops/seller/A1234567890",
  "name": "TechGadgets Store",
  "description": "Premium electronics accessories since 2015",
  "rating": 4.8,
  "review_count": 12450,
  "positive_feedback_pct": "98% positive feedback",
  "joined": "Member since: January 2015",
  "return_policy": "30-day returns accepted",
  "image": null,
  "_platform": "amazon"
}
```

### Composite: Amazon seller URL patterns

Amazon seller pages follow these URL patterns:

| Seller page type | URL |
|-----------------|-----|
| Seller storefront | `https://www.amazon.com/shops/{seller_id}` |
| Seller feedback (from product page) | Click "Sold by {seller_name}" link on a product page |
| Third-party seller ratings | `https://www.amazon.com/gp/seller/{seller_id}/ref=dp_byline_sr` |

To find a seller from a product page:
1. Navigate to product page → `wait stable`
2. `eval "document.querySelector('#sellerProfileTriggerId, #merchant-info a')?.href"` to get the seller URL
3. `navigate {seller_url}` → `wait stable`
4. `eval "$(python scripts/extract-seller.py)"`

### Composite: eBay seller URL patterns

| Seller page type | URL |
|-----------------|-----|
| eBay seller storefront | `https://www.ebay.com/str/{seller_username}` |
| eBay seller feedback | `https://www.ebay.com/usr/{seller_username}` |

To find seller from an eBay listing:
1. Navigate to eBay item page → `wait stable`
2. `eval "document.querySelector('.x-sellercard-atf__data a[href*=\"/usr/\"]')?.href"` to get seller URL
3. Navigate and extract

## Success Criteria

`result.name != null`

## Known Limitations

- Amazon seller pages may require navigating from `https://www.amazon.com` first on fresh sessions to avoid bot detection
- eBay seller pages may require navigating from `https://www.ebay.com` first
- Seller description and return policy availability depends on whether the seller has filled in their profile
- Rating scale differs by platform: Amazon uses 1–5 stars, eBay uses percentage of positive feedback; both are preserved in their native format

## Execution Efficiency

- **Batch orchestration**: Loop through seller URLs serially; add 1–2 second intervals between navigations
- **Test before batch execution**: Test with 1–2 sellers before running the full batch
- **Error resumption**: Save results item by item; on failure, resume from the breakpoint

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/ecommerce-scraper-ecommerce-seller-info.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions; adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`
