---
name: amazon-search-listing
description: "Amazon search and category listing scraper: extract product listings from any Amazon search results page, keyword search URL, or category browse page and return per-item cards (asin, title, url, image, price, listPrice, stars, reviewCount, badges, isAmazonChoice, isBestSeller, isSponsored, delivery, boughtInPast, positionIndex) plus pagination state (currentPage, hasNextPage, nextPageUrl, totalResultsApprox). Works across all Amazon regional TLDs (amazon.com, amazon.co.uk, amazon.de, amazon.co.jp, amazon.in, amazon.fr, amazon.ca, amazon.com.au, amazon.it, amazon.es, amazon.com.mx, amazon.com.br, amazon.nl, amazon.se, amazon.sg, amazon.ae, amazon.sa, amazon.pl, amazon.tr, amazon.eg). Use when user mentions Amazon, amazon.com, Amazon SERP, Amazon search results, Amazon keyword search, Amazon category page, Amazon subcategory URL, scrape Amazon listings, extract Amazon search, Amazon product cards, Amazon browse page, Amazon /s URL, Amazon /s?k= URL, Amazon /b/ category URL, Amazon /gp/browse category, Amazon bbn category filter, Amazon rh filter, Amazon search pagination, Amazon 7 pages limit, Amazon subcategory scraper, Amazon keyword scraper, Amazon SERP scraper, Amazon by URL, Amazon by category, Amazon by keyword. Also applies to price monitoring across a keyword or category, competitive listing tracking on Amazon, brand keyword ranking on Amazon, category catalog audits, best-of category discovery from a search, paginated bulk extraction of Amazon search hits, and building ASIN lists from a search."
---

# Amazon — Search & Category Listing

> Input any Amazon search results, keyword search, or category browse URL → output per-item product cards + pagination state.

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract structured product listings from any Amazon SERP or category browse page across all Amazon regional TLDs, including full pagination support to walk multiple pages of a keyword or category.

## Prerequisites

- Target page is already open in the browser: any Amazon search URL (e.g. `https://www.amazon.com/s?k={keyword}`), category browse URL (e.g. `https://www.amazon.com/s?bbn={cat}&rh=n%3A{node}`), or category deep link
- No login required; results reflect the browser's geolocation and Amazon domain

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `browser-act --session {name} eval "$(python scripts/xxx.py {params})"`. The `$(...)` is bash command substitution — it runs the python script, captures its printed JS text, and hands that JS string as a single argument to `browser-act eval`. Do not run `eval "$(python ...)"` as a bare shell command; that would ask bash to execute the JS as shell, which fails.

### DOM: extract product cards from current search/category page

Server-rendered HTML — no XHR/fetch API for listing data. Cards use the stable `[data-component-type="s-search-result"]` container.

1. `navigate {any Amazon search or category URL}` (e.g. `https://www.amazon.com/s?k={keyword}`, `https://www.amazon.com/s?k={keyword}&page={pageNumber}`, `https://www.amazon.com/s?bbn={browseNode}&rh=n%3A{nodeId}`, `https://www.amazon.co.uk/s?k={keyword}`)
2. `wait stable`
3. Extract: `browser-act --session {name} eval "$(python scripts/extract-search-results.py)"`

Output example:
```json
{
  "currentPage": 1,                                    // page number as displayed by the pagination widget
  "hasNextPage": true,                                 // true when a non-disabled next link exists
  "nextPageUrl": "https://www.amazon.com/s?k=laptop&page=2&...",  // absolute URL of next page, or null
  "totalResultsApprox": 100000,                        // parsed from "1-16 of over 100,000 results", or null
  "itemCount": 16,                                     // number of cards found on this page
  "items": [
    {
      "asin": "B09S3HNMHF",                            // 10-char Amazon Standard Identification Number
      "uuid": "d319ac5e-6161-4e4d-8ae5-1c63b8748308",  // per-render tracking id, null when absent
      "positionIndex": 3,                              // data-index attribute, indicates ordinal position in results
      "title": "Samsung 14\" Galaxy Chromebook Go ...",  // product title from h2 span
      "url": "https://www.amazon.com/.../dp/B09S3HNMHF/...",  // absolute product detail URL
      "image": "https://m.media-amazon.com/images/I/51...jpg", // thumbnail from img.s-image
      "imageAlt": "Samsung 14\" Galaxy Chromebook ...",       // truncated title from img alt
      "price": {"value": 179.99, "currencyRaw": "$", "raw": "$179.99"},  // current price, null when no offer
      "listPrice": {"value": 190.99, "currencyRaw": "$", "raw": "$190.99"},  // strike-through list price, null when absent
      "stars": 4.3,                                    // 0-5 rating, null when no reviews
      "reviewCount": 632,                              // ratings count, null when no reviews
      "ratingRaw": "4.3 out of 5 stars, rating details",
      "badges": [{"label": "Overall Pick", "supp": null}],  // all badges (Amazon's Choice, Best Seller, Overall Pick, deal labels)
      "isAmazonChoice": true,                          // derived from badge text
      "isBestSeller": false,                           // derived from badge text
      "isSponsored": false,                            // true when sponsored ad label present
      "delivery": "FREE delivery Fri, Jul 10",         // primary delivery message, null when absent
      "boughtInPast": "6K+ bought in past month"       // social proof, null when absent
    }
  ]
}
```

## Pagination

**URL Pagination**: Amazon SERP uses `?page={N}` query parameter, starting at 1. To iterate:

1. After extracting current page, use `nextPageUrl` from the output (already absolute) OR construct via URL: append/replace `&page={N+1}`
2. `navigate {nextPageUrl}` → `wait stable` → re-run extraction script
3. Termination: `hasNextPage == false` in output, OR the same ASIN list is returned as the previous page (Amazon returns page 1 when the requested page is out of range)

**Known Amazon SERP hard cap**: for keyword-only searches, Amazon limits results to 7 pages (~112 items). Category-scoped URLs (`bbn={node}&rh=n%3A{node}`) can return more. Combining a category node with a keyword often yields more pages than keyword alone.

## Success Criteria

`response.itemCount >= 1 AND response.items[0].asin matches /^[A-Z0-9]{10}$/`

## Known Limitations

- Amazon caps keyword-only search to 7 pages (~112 items). Use category-scoped URLs to go deeper.
- Some cards (video ads, banner slots) may be excluded — this is intentional, the `[data-component-type="s-search-result"]` selector only matches organic product cards.
- Prices reflect the delivery country Amazon inferred from the browsing session; use a proxy in the target region for country-specific pricing.
- `boughtInPast` and Amazon's Choice / Best Seller badges appear only on selected cards.
- `positionIndex` (data-index) is not sequential — Amazon interleaves promoted content, so index may skip.
- Search of amazon.com with browser geolocation outside the US may show region-specific interstitials; if extraction returns `error: no search result cards found`, verify no interstitial or verification challenge is blocking the page.

## Execution Efficiency

- **Batch orchestration**: Write a bash script that iterates page numbers serially within a single session; do not parallelize inside one browser. Add a 3-6 second sleep between pages to stay within normal browsing cadence. For higher throughput, distribute pages across multiple parallel browser sessions — each session maintains independent browser context and network state, so request volume spreads naturally across sessions.
- **Test before batch execution**: After writing a batch script, first test with 1-2 pages before running the full crawl. Never skip testing.
- **Reduce redundant pre-operations**: If iterating multiple keywords, keep the browser session open across keywords — reuse the `browser open` session and just `navigate` between URLs.
- **Error resumption**: Persist page-level results (one JSON per page) so a partial crash can resume from the failed page.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/amazon-scraper-amazon-search-listing.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
