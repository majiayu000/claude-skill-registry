---
name: ecommerce-reviews
description: "Extract customer reviews from any e-commerce product page or reviews page. Returns reviewer name, star rating, date, review title, review body, verified purchase status, and helpful votes per review. Works on Amazon, WooCommerce, Shopify, and any site with standard review markup. Supports pagination for multi-page review sections. Use when: product reviews, customer feedback, review scraping, get reviews, sentiment analysis data, review extraction, customer ratings, extract customer opinions, product feedback, user reviews, review mining, bulk review collection, review analysis, scrape ratings and comments, ecommerce review data."
---

# E-commerce — Product Reviews

> Product URL → paginated customer reviews (reviewer, rating, date, title, body, verified, helpful votes)

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract customer reviews from any publicly accessible e-commerce product or reviews page using a multi-strategy approach (JSON-LD Review → Amazon DOM → WooCommerce DOM → generic microdata → generic CSS patterns).

## Prerequisites

- Target browser is open and connected
- No login required for public review pages

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. Use the bash tool for execution.

### DOM: Extract reviews from current page

Navigate to the product/reviews page first, then extract:

```bash
eval "$(python scripts/extract-reviews.py --max-reviews 20)"
```

Parameters:
- `--max-reviews`: max reviews to return per page, default 20

Output example:
```json
{
  "count": 20,
  "reviews": [
    {
      "reviewer": "John D.",
      "rating": 5.0,
      "date": "Reviewed in the United States on May 15, 2026",
      "title": "Great product, exactly as described",
      "body": "I've been using this for two weeks and it works perfectly...",
      "verified": true,
      "helpful_votes": 42
    }
  ]
}
```

### Composite: Product URL → reviews with sort and pagination

**Step 1 — Navigate to reviews page:**

| Platform | Reviews URL pattern |
|----------|---------------------|
| Amazon | `https://www.amazon.com/product-reviews/{ASIN}?sortBy=recent` (most recent) or `sortBy=helpful` |
| Amazon (from product page) | Scroll to reviews section or click "See all reviews" link, `wait stable` |
| WooCommerce | Product page URL with `#reviews` anchor; reviews are inline on the page |
| Shopify | Reviews are typically inline on the product page |
| Generic | Navigate to product URL; reviews section is usually below product info |

**Step 2 — Extract reviews:**
```bash
eval "$(python scripts/extract-reviews.py --max-reviews 20)"
```

**Step 3 — Paginate (Amazon):**
Amazon review pages support URL pagination:
- Most recent sort: `https://www.amazon.com/product-reviews/{ASIN}?sortBy=recent&pageNumber={page}`
- Helpful sort: `https://www.amazon.com/product-reviews/{ASIN}?sortBy=helpful&pageNumber={page}`

For each page: `navigate {reviews_url_with_page}` → `wait stable` → re-run extract-reviews.py

Termination: when `count` returns 0, or no new reviews appear compared to prior page.

## Pagination

**URL Pagination (Amazon)**: Increment `pageNumber` parameter in the reviews URL. Start from 1.

**DOM Pagination (WooCommerce/generic)**: Look for a "Next" pagination link on the reviews section. Use `eval "$(python ../ecommerce-listing/scripts/extract-listing-next-page.py)"` to detect it, then navigate.

Termination: `has_next` is false, or `count` is 0.

## Success Criteria

`result.count >= 1 AND reviews[0].body != null`

## Known Limitations

- Amazon: navigate from `https://www.amazon.com` first on fresh sessions to avoid bot detection
- JSON-LD reviews are often limited to a small subset (3–5 reviews) even when hundreds exist; use the Amazon-specific URL for full review extraction
- WooCommerce and Shopify review data depends on which review plugin is installed; body extraction may be null if a non-standard plugin is used
- Review dates may be locale-formatted strings rather than ISO dates depending on the site's configuration

## Execution Efficiency

- **Batch orchestration**: Loop through review pages serially; add 1–2 second intervals between navigations
- **Test before batch execution**: Test with page 1 before running multi-page extraction
- **Error resumption**: Record page number; on failure, resume from last successful page

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/ecommerce-scraper-ecommerce-reviews.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions; adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`
