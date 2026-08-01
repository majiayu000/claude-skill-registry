---
name: ebay-sold-listings-search
description: "eBay sold-listings scraper across 8 marketplaces (ebay.com/.co.uk/.de/.fr/.it/.es/.ca/.com.au). Takes keyword plus filters (category, price range, item condition, item location, sort order, completed toggle) and returns paginated real-sale records with itemId, url, title, condition, conditionId, endedAt, soldPrice, soldCurrency, listingType (best_offer_accepted / buy_it_now / auction), isBestOfferAccepted, buyingFormat, bidCount, shipping, totalPrice, thumbnails, seller info, sellerType. Use when user mentions ebay sold, ebay sold listings, ebay sold prices, ebay completed listings, ebay comps, ebay resale prices, ebay auction sold results, ebay best offer accepted, scrape ebay sold, ebay market research, ebay pricing intelligence, ebay flipping research, real sold prices ebay, get sold prices from ebay. Also applies to price benchmarking, sold-price analytics, resale valuation, cross-marketplace price arbitrage, appraisal for collectibles, brand demand tracking on ebay."
---

# eBay — Sold Listings Search

> Keyword + filters → paginated list of items that actually sold on eBay, with final price, sold date, condition, listing format, shipping, seller, and images.

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Given one or more search keywords, fetch real sold (completed) listings from a chosen eBay marketplace with a user-defined filter set (category, price range, item condition, item location, sort order, completed-listings toggle), paginate up to the desired result count per keyword, and return one structured record per confirmed sale.

## Prerequisites

- Target eBay marketplace search page reachable in the browser: e.g. `https://www.ebay.com/sch/i.html?_nkw={keyword}&LH_Sold=1`. No login required.
- Ability to run `python`, `browser-act`, and `bash` (for `eval "$(python ...)"`).

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the search results page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the sold data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; use the bash tool for execution.

Below are all atomic capabilities discovered and verified during exploration. Combine freely as needed.

### URL Builder: assemble a sold-listings search URL for any of the 8 marketplaces

`URL=$(python scripts/build-url.py '{keyword}' --ebaySite {ebaySite} --sortOrder {sortOrder} --categoryId {categoryId} --subcategoryId {subcategoryId} --itemLocation {itemLocation} --itemCondition {itemCondition} --minPrice {minPrice} --maxPrice {maxPrice} --includeCompletedListings {true|false} --ipg {60|120|240} --page {pageNumber})`

The script prints one URL to stdout — capture into a bash variable and pass to `navigate`.

Parameters:
- `{keyword}` (positional, required): search term. 1–6 terms should each be run through a separate call.
- `--ebaySite`: `ebay.com` (default) · `ebay.co.uk` · `ebay.de` · `ebay.fr` · `ebay.it` · `ebay.es` · `ebay.ca` · `ebay.com.au`
- `--sortOrder`: `endedRecently` (default, `_sop=13`) · `timeNewlyListed` (`_sop=10`) · `pricePlusPostageLowest` (`_sop=15`) · `pricePlusPostageHighest` (`_sop=16`) · `distanceNearest` (`_sop=7`)
- `--categoryId`: main category filter (`_sacat`); default `0` (All Categories). Common IDs: see "Enum Parameters" section.
- `--subcategoryId`: subcategory ID; when set, overrides `--categoryId`.
- `--itemLocation`: `default` (`LH_PrefLoc=98`) · `domestic` (`LH_PrefLoc=1`, US Only on ebay.com) · `worldwide` (`LH_PrefLoc=2`)
- `--itemCondition`: `any` (no filter) · `new` (`LH_ItemCondition=1000`) · `used` (`LH_ItemCondition=3000`) · or pass any numeric eBay condition id (e.g. `1500` for Open Box, `2010` for Excellent Refurbished, `7000` for Parts). See enum section.
- `--minPrice` / `--maxPrice`: numeric filters `_udlo` / `_udhi`.
- `--includeCompletedListings`: `true` (default, adds `LH_Complete=1` — Best-Offer-Accepted detection works) or `false` (BOA appears as plain `buy_it_now`).
- `--ipg`: items per page — `60` (default), `120`, or `240`. Larger `ipg` fetches more per page but pages get heavier.
- `--page`: page number for pagination (`_pgn`), default `1`.

Output: a single fully-qualified URL string on stdout.

### DOM: extract sold-listing cards from the current eBay search results page

Prerequisite: browser is currently on an eBay sold-listings search URL and the results have rendered.

1. `navigate "$URL"` (using URL from build-url.py)
2. `wait --selector "li.s-card" --state visible --timeout 30000` (eBay may show a splash challenge before the results page; the splash resolves itself and `li.s-card` appears)
3. `eval "$(python scripts/extract-page.py --keyword '{keyword}')"`

Parameters of `extract-page.py`:
- `--keyword`: pass-through tag written to each item's `keyword` field so multi-keyword batches can be regrouped later. Optional; empty by default.

The extractor filters out eBay's promotional "Shop on eBay" placeholder cards automatically, only keeping cards with a real `data-listingid`.

Output example (top-level shape):
```json
{
  "error": false,
  "pageUrl": "https://www.ebay.com/sch/i.html?_nkw=iphone+15&LH_Sold=1&LH_Complete=1&_ipg=60&_pgn=1&_sop=13",
  "heading": "17,000+ results for iphone 15",   // total count string as shown on the page; may say "10,000+" for very large sets
  "categoryId": null,                            // _sacat from URL, null if All Categories
  "category": "Cell Phones & Smartphones",       // label from the eBay category dropdown
  "itemCount": 60,                               // number of real items (excludes promo cards)
  "hasNextPage": true,                           // whether a "Next" pagination link exists
  "nextUrl": "https://www.ebay.com/sch/...&_pgn=2", // href of the Next link, if present
  "items": [ /* array of item records */ ]
}
```

Per-item record example:
```json
{
  "itemId": "198484429340",                                   // eBay item ID
  "url": "https://www.ebay.com/itm/198484429340",             // canonical item URL (query stripped)
  "title": "Apple iPhone 15 Pro 128GB Blue A2848 Triple ...", // localized card title
  "condition": "Pre-Owned",                                    // localized condition label as displayed (Pre-Owned, Gebraucht, Neuf, Nuovo, Usado, Open Box, etc.); null when not shown
  "conditionId": 3000,                                         // best-effort numeric eBay condition ID; null when the label isn't in the lookup table
  "categoryId": null,                                          // effective _sacat used for the search; null when All Categories
  "category": "Cell Phones & Smartphones",                     // category label from the search page dropdown
  "endedAt": "2026-07-08T00:00:00.000Z",                       // sale completion date (parsed from "Sold X" caption, midnight UTC)
  "soldPrice": "437.40",                                       // final displayed price (string, 2-decimal). For BOA, this is the asking price — actual accepted offer is not disclosed by eBay
  "soldCurrency": "USD",                                       // ISO currency code — USD / GBP / EUR / AUD / CAD
  "listingType": "best_offer_accepted",                        // best_offer_accepted | buy_it_now | auction | null
  "isBestOfferAccepted": true,                                 // true only when includeCompletedListings=true and BOA signals detected
  "buyingFormat": "buyItNow",                                  // auction | buyItNow | auctionWithBIN | null
  "bidCount": null,                                            // integer for auctions, null for fixed-price
  "shippingPrice": "5.70",                                     // shipping cost (string, 2-decimal); "0.00" for free; null when not disclosed
  "shippingCurrency": "USD",                                   // shipping currency; may be null when free or hidden
  "shippingType": "paid",                                      // free | paid | pickup | unknown
  "totalPrice": "443.10",                                      // soldPrice + shippingPrice when currencies match, else equal to soldPrice
  "thumbnailUrl": "https://i.ebayimg.com/images/g/yf0AAeSwyeRqTgsw/s-l500.webp",  // 500px product image; null if only a promo/logo image is on the card
  "fullResThumbnailUrl": "https://i.ebayimg.com/images/g/yf0AAeSwyeRqTgsw/s-l1600.webp", // 1600px derived best-effort; may 404 for items eBay only hosts low-res
  "sellerUsername": "arn-987085",                              // seller handle
  "sellerPositivePercent": 100,                                // positive-feedback percentage as number; 0 is a valid data value (new sellers), null when not shown
  "sellerFeedbackScore": 47,                                   // feedback count as integer; K/M suffix expanded (1.4K → 1400)
  "sellerType": null,                                          // "private" | "business" on EU sites (ebay.de/.fr/.it/.es); null elsewhere or when label unrecognised
  "keyword": "iphone 15",                                       // pass-through from --keyword
  "scrapedAt": "2026-07-08T10:46:07.053Z"                       // ISO timestamp of extraction
}
```

Error handling: when the extractor returns `{"error": true, ...}`, check `window.location.href` and `document.title` via `state` — the page may be an eBay splash challenge (`ebay.com/splashui/challenge`), an anti-scrape "SORRY / Something went wrong" error page, or a redirect to a different page (very large ambiguous queries occasionally auto-redirect to a similar-item page). Wait longer or re-navigate; if repeatedly blocked, switch to a stealth browser with a different IP.

### DOM: enumerate eBay top-level categories from the search page

Prerequisite: currently on any eBay search results page (any keyword).

`eval "$(python scripts/enum-categories.py)"`

Output example:
```json
{
  "error": false,
  "count": 34,
  "items": [
    { "id": "20081", "label": "Antiques", "depth": 0 },
    { "id": "550", "label": "Art", "depth": 0 },
    { "id": "58058", "label": "Computers/Tablets & Networking", "depth": 0 },
    { "id": "281", "label": "Jewelry & Watches", "depth": 0 }
  ]
}
```

`depth: 0` = top-level main category. Subcategories with `depth >= 1` may also appear when the current search is scoped to a category. For deep subcategory IDs beyond top-level, users should first search within the desired top category, then re-run the enum.

### Composite: batch-collect sold listings across multiple keywords with pagination

For each keyword in the caller's list, loop pagination until either the caller-defined `count` (max items) is reached OR `hasNextPage=false`. Between pages, back off briefly (2–4 seconds) to avoid triggering rate limits. Deduplicate by `itemId` if a keyword sees the same item on adjacent pages.

Cross-page (contains navigate + non-JS steps):

1. For each `{keyword}` in the keyword list:
   a. Initialize `page=1`, `collected=[]`, `seenIds=set()`
   b. Loop while `len(collected) < count`:
      - `URL=$(python scripts/build-url.py '{keyword}' --ebaySite {ebaySite} --sortOrder {sortOrder} --categoryId {categoryId} --subcategoryId {subcategoryId} --itemLocation {itemLocation} --itemCondition {itemCondition} --minPrice {minPrice} --maxPrice {maxPrice} --includeCompletedListings {includeCompletedListings} --page $page)`
      - `navigate "$URL"` → `wait --selector "li.s-card" --state visible --timeout 30000`
      - `RESULT=$(browser-act --session {name} eval "$(python scripts/extract-page.py --keyword '{keyword}')")`
      - Parse RESULT JSON. If `error=true`, retry once after a longer wait; if still failing, mark keyword incomplete and break.
      - For each item, if `itemId` not in `seenIds`: add to `collected` and `seenIds`.
      - If `hasNextPage=false` or `len(collected) >= count`: break.
      - `sleep 2-4s`, increment `page`.
   c. Persist collected items keyed by keyword (write JSONL to disk to survive interruptions).
2. Merge all keyword outputs into a single dataset.

Optional post-filter: if the caller supplied `daysToScrape`, discard items whose `endedAt` is older than `now - daysToScrape` days after collection (eBay's URL does not accept a direct sold-date range; sorting by `endedRecently` and stopping when items fall out of the window is the standard approach).

## Enum Parameters

[DOM] `categoryId` / `subcategoryId` — retrieve top-level `_sacat` values via `eval "$(python scripts/enum-categories.py)"` (see "DOM: enumerate eBay top-level categories" above). Subcategories require first navigating to a category-scoped search. eBay publishes exhaustive category trees on its own site (footer link "See all categories") for deep hierarchies.

[Static] `sortOrder` — fixed mapping, no runtime enumeration needed: `endedRecently=13`, `timeNewlyListed=10`, `pricePlusPostageLowest=15`, `pricePlusPostageHighest=16`, `distanceNearest=7`. Applied by `build-url.py`.

[Static] `itemLocation` — fixed mapping: `default=98`, `domestic=1`, `worldwide=2`. Applied by `build-url.py`.

[Static] `itemCondition` — common eBay condition IDs (pass any numeric ID directly via `--itemCondition`):
- `1000` New / Brand New
- `1500` New Other / Open Box
- `1750` New with defects
- `2000` Certified Refurbished · `2010` Excellent - Refurbished · `2020` Very Good - Refurbished · `2030` Good - Refurbished
- `2500` Seller Refurbished
- `2750` Like New
- `3000` Used / Pre-Owned
- `7000` For parts or not working

[Static] `ebaySite` — fixed list of 8 marketplaces: `ebay.com`, `ebay.co.uk`, `ebay.de`, `ebay.fr`, `ebay.it`, `ebay.es`, `ebay.ca`, `ebay.com.au`. Applied by `build-url.py`.

## Pagination

**URL Pagination**: URL pattern `...&_pgn={N}` (1-based). Next page link selector: `a[type=next], a[rel=next]` — the extractor exposes it as `nextUrl` and `hasNextPage` in the response. Termination: `hasNextPage=false`, or `items.length === 0`, or `endedAt` of the last item is older than the caller's `daysToScrape` window when sorted by `endedRecently`, or the caller's `count` reached.

## Success Criteria

`error === false && itemCount >= 1 && items.every(i => i.itemId && i.url && i.title && (i.soldPrice !== null))`

For pagination flows: `unique itemIds across all collected pages >= min(count, hasNextPage-terminated total)` and `every item has soldPrice non-null`.

## Known Limitations

- eBay does not disclose the actual accepted amount for Best-Offer-Accepted sales. `soldPrice` for BOA items is the asking price at listing time, and `isBestOfferAccepted=true` signals the discrepancy. This is a data-source limitation, not a scraper limitation.
- BOA detection requires `includeCompletedListings=true` (the default). With `LH_Complete=0`, eBay strips the `strikethrough` price styling and "Best offer accepted" caption, so BOA sales appear as ordinary `buy_it_now`. All results are still genuinely sold either way (`LH_Sold=1` is always applied).
- eBay's URL does not accept a direct sold-date range filter. Time-window scoping (e.g., "last 30 days") is achieved by sorting by `endedRecently` and stopping pagination when items fall out of the desired window.
- `sellerType` (`private` / `business`) is only labeled on EU marketplaces (`ebay.de`, `ebay.fr`, `ebay.it`, `ebay.es`); non-EU sites return `null`.
- `fullResThumbnailUrl` is derived by rewriting `s-l500` → `s-l1600` in the thumbnail URL. For items where eBay only hosts a low-res image, the URL may 404.
- IP-based rate limiting and splash challenges: aggressive pagination from a single IP can trigger `ebay.com/splashui/challenge` interstitials (typically resolve themselves within seconds) or a "SORRY / Something went wrong" error page (requires switching IPs or waiting). Space out requests 2–4 seconds between pages.
- Some marketplaces (`ebay.co.uk`, `ebay.de`) may refuse requests from IPs geolocated in unrelated regions with an outright error page. Use a stealth browser bound to a matching-region proxy (e.g., UK IP for ebay.co.uk) for reliable access to non-US sites.
- Localized condition labels are covered for English, German, French, Italian, Spanish. Novel or newly introduced eBay condition labels not present in the lookup table return `conditionId: null` while `condition` still shows the localized text.

## Execution Efficiency

- **Batch orchestration**: For multi-keyword collection, loop keywords serially within a single browser session; only page-by-page pagination is safe from a single IP. Do not parallelize pages of the same keyword within one browser — the anti-scrape system tracks sessions.
- **Higher throughput**: For truly large batches, distribute keywords across multiple stealth browsers with independent fingerprints/proxies, one keyword per session. Each session has its own rate-limit budget.
- **Test before batch execution**: After wiring up the batch script, first run 1–2 keywords × 2 pages to verify parsing quality (spot-check `listingType`, `soldPrice`, `endedAt`), only then run the full batch.
- **Reduce redundant pre-operations**: Reuse the same browser session across keywords when possible; navigation between search URLs is cheap.
- **Error resumption**: Persist per-keyword results as JSONL to disk after each page; on failure, resume from the last completed page rather than restarting the keyword.
- **Larger `_ipg`**: Setting `--ipg 240` (max) reduces the number of paginated requests four-fold, at the cost of heavier pages. Use for exhaustive collections; keep `60` for spot checks.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/ebay-sold-listings-search.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
