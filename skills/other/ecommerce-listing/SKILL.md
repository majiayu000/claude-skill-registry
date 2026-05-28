---
name: ecommerce-listing
description: "Extract product list from any e-commerce category page, search results page, or keyword search with filters. Returns paginated product arrays with URL, name, price, currency, image, rating, review count per item. Supports URL input, keyword search, and site-scoped search with filters: price range, brand, category, minimum rating, in-stock only, and sort order. Works on Amazon, eBay, Walmart, Shopify collections, WooCommerce shops, Google Shopping, and any public product listing page. Use when: category listing, product search results, ecommerce search, search for products, filter products by price, list products from a site, price range filter, brand filter, keyword search with filters, scrape product list, product catalog extraction, get all products from category, bulk product URLs, product list scraping, category page scraper, search results scraper, multi-page product extraction."
---

# E-commerce — Product Listing

> Category/search URL or keyword + filters → paginated product list (URL, name, price, image, rating per item)

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract a structured list of products from any e-commerce category, search results, or keyword search page, with support for price/brand/rating filters and multi-page pagination.

## Prerequisites

- Target browser is open and connected
- No login required for public listing pages

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. Use the bash tool for execution.

### DOM: Extract product list from current page

Navigate to the listing/search page first, then extract:

```bash
eval "$(python scripts/extract-listing.py --max-results 20)"
```

Parameters:
- `--max-results`: max items to return per page, default 20

Output example:
```json
{
  "count": 20,
  "items": [
    {
      "url": "https://www.amazon.com/dp/B09WNK39JN",
      "name": "Amazon Echo Pop",
      "price": 39.99,
      "currency": "USD",
      "image": "https://m.media-amazon.com/images/I/...jpg",
      "rating": 4.7,
      "review_count": 103789,
      "asin": "B09WNK39JN"
    }
  ]
}
```

### DOM: Get next page URL

After extracting a page, get the URL to navigate to for the next page:

```bash
eval "$(python scripts/extract-listing-next-page.py)"
```

Output example:
```json
{"next_url": "https://www.amazon.com/s?k=headphones&page=2", "has_next": true, "method": "amazon"}
```

When `has_next` is false, pagination is complete.

### Composite: Keyword search with filters → product list

**Step 1 — Build search URL with filters:**

Construct the URL based on target site and desired filters using the patterns below, then navigate:

**Amazon** (`amazon.com`):
```
https://www.amazon.com/s?k={keyword_urlencoded}&s={sort}&rh={filter_params}
```
- Sort (`s`): `price-asc-rank` | `price-desc-rank` | `review-rank` | `date-desc-rank` (omit for relevance)
- Price filter: append `p_36:{min_cents}-{max_cents}` to `rh` (dollars × 100, e.g. $50–$200 → `p_36:5000-20000`)
- Rating filter: append `avg_customer_review:four-and-above` | `three-and-above` | `two-and-above` to `rh`
- In-stock: append `p_n_availability:1248801011` to `rh`
- Multiple `rh` values: comma-separate (e.g. `rh=p_36:5000-20000,avg_customer_review:four-and-above`)

**eBay** (`ebay.com`):
```
https://www.ebay.com/sch/i.html?_nkw={keyword_urlencoded}&_udlo={min_price}&_udhi={max_price}&_sop={sort_num}
```
- Sort: `12`=BestMatch | `15`=PriceLow | `16`=PriceHigh | `24`=NewlyListed

**Walmart** (`walmart.com`):
```
https://www.walmart.com/search?q={keyword_urlencoded}&min_price={min}&max_price={max}&sort={sort}
```
- Sort: `best_match` | `price_low` | `price_high` | `rating_high`

**Google Shopping** (cross-site, no `--site`):
```
https://www.google.com/search?tbm=shop&q={keyword_urlencoded}&tbs=p_ord:{sort}
```
- Sort: `rv`=relevance | `pd`=price ascending | `prd`=price descending

**Any site with `--site`** (generic):
```
https://{site}/search?q={keyword_urlencoded}
```

**Step 2 — Navigate and extract:**
1. `navigate {constructed_url}` → `wait stable`
2. `eval "$(python scripts/extract-listing.py --max-results {n})"`

**Step 3 — Paginate (repeat until done):**
1. `eval "$(python scripts/extract-listing-next-page.py)"`
2. If `has_next` is true: `navigate {next_url}` → `wait stable` → re-run extract-listing.py
3. If `has_next` is false: stop

## Pagination

**URL Pagination**: `extract-listing-next-page.py` detects `rel=next` link, platform-specific pagination controls, and URL page parameters. Returns `next_url` for navigation.

**DOM Pagination**: For sites with load-more buttons (some Shopify themes):
1. `state` to find "Load more" or "Show more" button
2. `click <index>` → `wait stable` → re-run `extract-listing.py`
3. Termination: button no longer present, or item count stops increasing

## Success Criteria

`result.count >= 1 AND items[0].url != null`

## Known Limitations

- Amazon: direct navigation may trigger bot detection on fresh sessions — navigate from `https://www.amazon.com` first
- eBay listing pages may require navigating from `https://www.ebay.com` first
- Google Shopping results have complex SPA structure and may have reduced accuracy; prefer direct site search when `--site` is specified
- Filter URL parameters are site-specific; unsupported filter parameters are silently ignored by some sites
- Shopify themes vary widely; if the generic DOM strategies miss items, check if the page has JSON-LD ItemList or Product array in page source

## Execution Efficiency

- **Batch orchestration**: Loop through pages serially within a single session; add 1–2 second intervals between page navigations
- **Test before batch execution**: Test with 1 page before running multi-page extraction
- **Error resumption**: Record page number; on failure, resume from the last successful page

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/ecommerce-scraper-ecommerce-listing.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions; adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`
