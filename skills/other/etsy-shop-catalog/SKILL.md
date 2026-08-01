---
name: etsy-shop-catalog
description: "Etsy shop catalog scraper: given an Etsy shop URL (e.g. https://www.etsy.com/shop/{shop-name}) and optional page number, returns paginated product listings from that shop's own storefront with listingId, shopId, title, url, image, salePrice, originalPrice, currency, rating, reviewCount, shopName, isAd, freeShipping, badge. Use when user mentions Etsy shop, Etsy seller, Etsy store, etsy.com/shop, scrape Etsy shop, extract all products from Etsy shop, Etsy shop catalog, Etsy seller catalog, list all Etsy shop items, Etsy storefront scraper, Etsy vendor products, Etsy competitor shop, Etsy shop monitoring, get inventory of an Etsy shop, dump Etsy shop products, Etsy seller product export, seller product benchmarking, Etsy shop bulk export. Also applies to competitor shop tracking, supplier catalog collection, price monitoring for a specific shop, new-item detection on a shop, and any paginated bulk collection driven by a single Etsy shop URL."
---

# Etsy — Shop Catalog

> Input an Etsy shop URL (and optional page number) → output paginated product listings from that shop's storefront.

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Collect a shop's own storefront listings, one page at a time, with core fields per item.

## Prerequisites

- Target page is already open in the browser: `https://www.etsy.com/shop/{shop-name}` (or navigate to it during execution)
- No login required — shop pages are public
- Browser session must survive anti-bot verification (DataDome). Best practice: navigate to `https://www.etsy.com/` first, then to the shop URL

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Anti-bot Warm-up

If a fresh browser session was just created:

1. `navigate https://www.etsy.com/` → `wait stable`
2. Then `navigate https://www.etsy.com/shop/{shop-name}` → `wait stable`

On `blocked by anti-bot verification page` errors, switch to a stealth browser with a different fingerprint / proxy and retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### DOM: extract product listings from shop storefront page

Prerequisite: current page is an Etsy shop page (`https://www.etsy.com/shop/{shop-name}`) after `wait stable`. Works on both the default first tab and paginated tabs.

Extract: `eval "$(python scripts/extract-listings.py)"`

Output example:
```json
{
  "error": false,
  "url": "https://www.etsy.com/shop/Xcraftsman?ref=items-pagination&page=2&sort_order=custom",  // page URL
  "currentPage": 2,                        // current page number parsed from URL, defaults 1
  "count": 44,                             // number of unique listings on the page
  "nextPageUrl": "https://www.etsy.com/shop/Xcraftsman?ref=items-pagination&page=3&sort_order=custom",  // URL of next page, null on last page
  "listings": [
    {
      "listingId": "4332558944",           // Etsy listing id
      "shopId": "13350861",                // Etsy shop id (same across the whole shop)
      "title": "Handmade Leather Bifold Wallet",  // product title
      "url": "https://www.etsy.com/listing/4332558944/…",  // canonical listing URL, tracking params stripped
      "image": "https://i.etsystatic.com/…/il_794xN.….jpg",  // primary product image
      "salePrice": "$120.00",              // current display price
      "originalPrice": null,               // original / crossed-out price, null when no discount
      "currency": "$",                     // currency symbol as shown to user
      "rating": 4.8,                       // average star rating on the shop card, null when card shows none
      "reviewCount": "455",                // review count as displayed
      "shopName": "Xcraftsman",            // shop / seller display name (same for all cards)
      "isAd": false,                       // typically false on shop pages
      "freeShipping": true,                // true when "Free shipping" badge shown
      "badge": null,                       // ranked badge text or null
      "positionIndex": 0                   // 0-based position within the page
    }
  ]
}
```

Error handling:
- `{"error": true, "message": "blocked by anti-bot verification page"}` — DataDome interstitial; retry warm-up
- `{"error": true, "message": "no listing cards found on page"}` — shop may be empty, on vacation, or URL is wrong; check the shop URL and shop status shown on the page

## Pagination

**URL Pagination**: URL pattern `https://www.etsy.com/shop/{shop-name}?ref=items-pagination&page={N}&sort_order=custom` where `{N}` starts at 1. Follow the returned `nextPageUrl` verbatim to preserve `sort_order` and other shop-tab params. Termination: `count === 0` or previous `nextPageUrl` was null.

## Success Criteria

`result.error === false && result.count >= 1 && result.listings.every(l => l.listingId && l.title && l.url && l.shopName)`

## Known Limitations

- DataDome anti-bot: fresh sessions may hit a CAPTCHA interstitial; warm up via `/` first
- Shop-specific tabs (e.g. featured, sections) may reorder items; passing `?sort_order=custom` matches the shop owner's default ordering
- Shops that use the "sections" navigation may split their catalog across multiple section-scoped pages; iterate each section URL for full catalog coverage
- Shop pages sometimes show fewer cards on the initial paint until user scrolls (`~44` on page 1 vs `~64` on paginated pages); this is normal — extract what is rendered, then paginate
- Shops on vacation display an announcement banner; the extraction still works but `count` may be 0

## Execution Efficiency

- **Batch orchestration**: Loop through pages serially within a single session; insert 3-8 second sleeps between page navigations. Distribute shops across multiple stealth browser sessions for higher throughput
- **Test before batch execution**: Verify the script on 1-2 pages of one shop first
- **Reduce redundant pre-operations**: Warm-up once per session, then process shops sequentially in the same session
- **Error resumption**: Save each page's results to `results/{shop-name}-p{N}.json` immediately; on failure resume from the missing page

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/etsy-scraper-etsy-shop-catalog.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what shops were used or how many results were returned — those are task outputs, not experience.
