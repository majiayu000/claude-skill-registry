---
name: etsy-category-listing
description: "Etsy category page scraper: given an Etsy category URL (e.g. https://www.etsy.com/c/jewelry) and optional page number, returns paginated product listings with listingId, shopId, title, url, image, salePrice, originalPrice, currency, rating, reviewCount, shopName, isAd, freeShipping, badge from category and subcategory pages. Use when user mentions Etsy category, Etsy c/ URL, etsy.com category, browse Etsy categories, scrape Etsy category, Etsy category listing, extract Etsy category products, Etsy subcategory, Etsy jewelry, Etsy clothing, Etsy home decor, Etsy wedding, Etsy accessories, Etsy craft supplies, Etsy vintage category, Etsy category page scraper, Etsy taxonomy, get all products from an Etsy category, bulk category export from Etsy, Etsy niche scraping. Also applies to trend research within a specific Etsy category, competitor benchmarking within a category, sourcing suppliers by category, seasonal product monitoring, and paginated bulk collection driven by a category URL."
---

# Etsy — Category Listing

> Input an Etsy category URL (and optional page number) → output paginated product listings from that category page.

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Collect product listings from Etsy public category (`/c/...`) pages, one page at a time, with core fields per item.

## Prerequisites

- Target page is already open in the browser: `https://www.etsy.com/c/{category-path}` (or navigate to it during execution)
- No login required — category pages are public
- Browser session must survive anti-bot verification (DataDome). Best practice: navigate to `https://www.etsy.com/` first, then to the category URL, within an established stealth browser session

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Anti-bot Warm-up

If a fresh browser session was just created, before hitting a `/c/` URL directly:

1. `navigate https://www.etsy.com/` → `wait stable`
2. Then `navigate {category URL}` → `wait stable`

If the extraction script returns `{"error": true, "message": "blocked by anti-bot verification page"}`, switch to a stealth browser with a different fingerprint / proxy, retry the warm-up, then re-run extraction.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### DOM: extract product listings from category page

Prerequisite: current page is an Etsy category page (`https://www.etsy.com/c/{category-path}`) after `wait stable`.

Extract: `eval "$(python scripts/extract-listings.py)"`

Output example:
```json
{
  "error": false,
  "url": "https://www.etsy.com/c/jewelry?ref=catnav-10855&page=2",  // page URL
  "currentPage": 2,                        // current page number parsed from URL, defaults 1
  "count": 64,                             // number of unique listings on the page
  "nextPageUrl": "https://www.etsy.com/c/jewelry?ref=pagination&page=3",  // URL of next page, null on last page
  "listings": [
    {
      "listingId": "1791916774",           // Etsy listing id
      "shopId": "18293002",                // Etsy shop id
      "title": "Handmade Silver Ring…",    // product title
      "url": "https://www.etsy.com/listing/1791916774/…",  // canonical listing URL, tracking params stripped
      "image": "https://i.etsystatic.com/…/il_794xN.….jpg",  // primary product image
      "salePrice": "$45.00",               // current display price
      "originalPrice": null,               // original / crossed-out price, null when no discount
      "currency": "$",                     // currency symbol as shown to user
      "rating": 4.9,                       // average star rating, null when card shows none
      "reviewCount": "1.2k",               // review count as displayed
      "shopName": "SilverCraftShop",       // shop / seller display name
      "isAd": false,                       // true when card is an advertised placement
      "freeShipping": true,                // true when "Free shipping" badge shown
      "badge": "Etsy's Pick",              // ranked badge text or null
      "positionIndex": 0                   // 0-based position within the page
    }
  ]
}
```

Error handling:
- `{"error": true, "message": "blocked by anti-bot verification page"}` — DataDome interstitial; retry warm-up in a stealth browser
- `{"error": true, "message": "no listing cards found on page"}` — either category has no products or page not fully loaded; verify category URL and pagination

## Pagination

**URL Pagination**: URL pattern `{category-URL}&page={N}` (append `&page={N}` to the base category URL) where `{N}` starts at 1. Termination: navigate to `{N+1}`; if `count === 0` or previous `nextPageUrl` was null, stop. Etsy typically caps navigable pages per category at ~250.

## Success Criteria

`result.error === false && result.count >= 1 && result.listings.every(l => l.listingId && l.title && l.url)`

## Known Limitations

- DataDome anti-bot: cold cross-page navigation into `/c/` may show a CAPTCHA interstitial. Mitigate by navigating to `/` first within the same stealth session, or rotating proxy / browser fingerprint on repeated blocks
- `reviewCount` returned as displayed text (`7.9k`, `17.6k`) rather than an exact integer
- Sponsored (ad) placements marked with `isAd: true`; position is paid
- Etsy Offsite Ads anonymize the seller in the card text ("Ad from Etsy seller"); for such cards `shopName` returns `null` even though `isAd: true`. Navigate to the listing URL and run the product-detail capability to resolve the true shop if needed
- Etsy category personalization: results may vary by proxy region and account login state
- Applying category filters (price range, ship-to, colors, etc.) requires appending Etsy's URL params (e.g. `min=10&max=50`) to the base category URL before navigation; the extraction script works on whatever page state is present but does not inject filters itself

## Execution Efficiency

- **Batch orchestration**: Loop through pages serially within a single session; do not parallelize within one browser. Insert 3-8 second sleeps between page navigations. To increase throughput, open multiple stealth browser sessions and distribute categories across them
- **Test before batch execution**: Verify the script on 1-2 pages of one category first
- **Reduce redundant pre-operations**: Warm-up once per session, then loop pages within the same session
- **Error resumption**: Save each page's results to a file as soon as extraction succeeds; resume from the missing page on failure

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/etsy-scraper-etsy-category-listing.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what categories were used or how many results were returned — those are task outputs, not experience.
