---
name: walmart-category-listing
description: "Walmart category page scraper: input a walmart.com browse or category URL with optional page number, extract paginated product listings with itemId, url, title, brand, image, price, wasPrice, rating, reviewCount, availability, seller info, fulfillmentBadge, and classType. Use when user mentions walmart category, walmart browse page, walmart category listing, scrape walmart category, walmart department scrape, walmart category URL, browse walmart categories, walmart category products, walmart category page scraper, walmart browse scraper, extract walmart category items, walmart filtered category, walmart subcategory products, walmart browse items, walmart department listing, walmart catalog browse, walmart aisle scraper. Also applies to collecting products from a specific walmart category URL with filters applied (e.g. filtered category URLs copied from the browser), scraping all items from a walmart browse section, category-scoped price monitoring on walmart, and parent category crawling where subcategory URLs are enumerated first."
---

# Walmart — Category Listing

> category URL + page → paginated product list from walmart.com browse/category page

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract product listings from any Walmart category or browse page URL, returning structured item data with pricing, rating, availability, and seller info.

## Prerequisites

- Target category page is open in the browser: `https://www.walmart.com/browse/{category-slug}/{category-ids}?page={page}`

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### DOM: extract product listing from current category page

Navigate to the target category URL first, then extract. Category URLs may include filter parameters copied from the browser.

1. `navigate "{category_url}?page={page}"` — if the URL already has query params, use `&page={page}` instead
2. `wait stable`
3. `eval "$(python scripts/extract-listing.py)"`

URL format examples:
- `https://www.walmart.com/browse/home/?page=1`
- `https://www.walmart.com/browse/auto-tires/brake-pads/91083_1074765_9038935_4582920?page=1`
- `https://www.walmart.com/cp/1149374?page=2` (category ID URL)
- With filters: `https://www.walmart.com/browse/electronics/laptops?minPrice=500&maxPrice=1000&page=1`

Output example:
```json
{
  "pageType": "BrowsePage",
  "query": null,
  "currentPage": 1,
  "totalCount": 60010,
  "maxPage": 25,
  "itemCount": 51,
  "items": [
    {
      "itemId": "2830965432",
      "url": "https://www.walmart.com/ip/Product-Name/2830965432",
      "title": "Product title here",
      "brand": "Brand Name",
      "image": "https://i5.walmartimages.com/seo/product.jpeg",
      "price": 19.99,
      "priceString": "$19.99",
      "wasPrice": 24.99,
      "rating": 4.5,
      "reviewCount": 1234,
      "availability": "IN_STOCK",
      "availabilityText": "In stock",
      "sellerName": "Walmart.com",
      "sellerType": null,
      "fulfillmentBadge": null,
      "classType": "REGULAR",
      "shortDescription": null
    }
  ]
}
```

Error response (when extraction fails or wrong page):
```json
{"error": true, "message": "No searchResult in __NEXT_DATA__. Ensure the page is fully loaded at the correct search URL."}
```

## Pagination

**URL Pagination**: Append `?page={N}` (or `&page={N}` if URL has existing query params) to the category URL. Increment page by 1 each iteration. Termination: `page > maxPage` (from response `maxPage` field) OR `itemCount === 0`. Note: Walmart caps category browsing at `maxPage` pages (up to 25 for broad categories).

## Success Criteria

`itemCount >= 1` AND `items[0].itemId` is non-null AND `items[0].url` starts with `https://www.walmart.com/ip/`

## Known Limitations

- Walmart limits category pagination to at most ~25 pages regardless of total result count
- `brand` field is null for many items in listing pages (available in product detail)
- `wasPrice` is null unless the item has an active markdown/rollback
- Heavily filtered category URLs (applied from browser) are directly usable — paste as-is and append `?page=N`

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through pages serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Add 1–2 second intervals between page navigations. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/walmart-scraper-walmart-category-listing.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what URLs were scraped or how many results were returned — those are task outputs, not experience.
