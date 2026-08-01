---
name: etsy-product-detail
description: "Etsy product detail scraper: given an Etsy listing URL, returns full product detail including listingId, title, priceCurrent, priceOriginal, currency, images (all), description, shopName, shopUrl, rating, reviewCount, favorites, inCartCount, variations (with per-option price ranges), highlights, listedDate, relatedTags. Use when user mentions Etsy product, Etsy listing detail, Etsy item info, Etsy product page, scrape Etsy listing, extract Etsy product data, Etsy price and variations, Etsy product images, Etsy product description, Etsy shop from listing, Etsy favorites count, Etsy sale count, Etsy variations extraction, Etsy listing metadata, single Etsy product scrape, bulk enrich Etsy listing URLs, Etsy product details export. Also applies to competitor product monitoring, price and variation tracking on a specific listing, favorites/wishlist popularity tracking, description mining for SEO analysis, and any per-listing enrichment task."
---

# Etsy — Product Detail

> Input an Etsy listing URL → output full product detail including price, variations, images, shop, rating, favorites, and description.

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract complete detail data from a single Etsy listing page.

## Prerequisites

- Target page is already open in the browser: `https://www.etsy.com/listing/{listing-id}/{slug}` (or navigate to it during execution)
- No login required — listing pages are public
- Browser session must survive anti-bot verification (DataDome). Best practice: navigate to `https://www.etsy.com/` first, then to the listing URL

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Anti-bot Warm-up

If a fresh browser session was just created:

1. `navigate https://www.etsy.com/` → `wait stable`
2. Then `navigate {listing URL}` → `wait stable`

On `blocked by anti-bot verification page` errors, switch to a stealth browser with a different fingerprint / proxy and retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### DOM: extract product detail from listing page

Prerequisite: current page is an Etsy listing page (`https://www.etsy.com/listing/{listing-id}/...`) after `wait stable`.

Extract (description included): `eval "$(python scripts/extract-detail.py)"`

Extract (skip description text to reduce output size): `eval "$(python scripts/extract-detail.py --include-description false)"`

Parameters:
- `--include-description`: `true` (default) to include full description text; `false` to omit and return `description: null`

Output example:
```json
{
  "error": false,
  "url": "https://www.etsy.com/listing/870439619/personalized-handmade-leather-mens",  // canonical URL
  "listingId": "870439619",                // Etsy listing id
  "title": "Handmade Personalized Men's Full Grain Leather Wallet…",  // full product title
  "priceCurrent": "Price:$23.26+",         // current display price (raw text as shown; may include '+' for variation min)
  "priceOriginal": null,                   // original / crossed-out price, null when no discount
  "currency": "$",                         // currency symbol, null if not detected
  "imageCount": 50,                        // total unique image URLs discovered on the page (includes user-uploaded review photos)
  "images": [                              // ordered list of image URLs (main product images first, then review photos)
    "https://i.etsystatic.com/22700950/r/il/…/il_fullxfull.….jpg"
  ],
  "description": "** Handwriting Engraved Leather Wallet for Men … **",  // full description text; null when --include-description=false
  "shopName": "CaglarCreations",           // shop / seller display name
  "shopUrl": "https://www.etsy.com/shop/CaglarCreations",  // shop URL, tracking params stripped
  "rating": 4.9,                           // average star rating (numeric)
  "reviewCount": "7.8k",                   // review count as displayed by Etsy (may include k/M suffix)
  "favorites": 27013,                      // favorites count (integer), null when not present
  "inCartCount": null,                     // count of active shoppers with item in cart, null when not present
  "variations": [                          // ordered variation groups (e.g. color, size, engraving)
    {
      "label": "Engraving Options",        // variation group label
      "options": [
        {
          "value": "4124115439",           // Etsy option id
          "text": "NO PERSONALIZATION",    // option display name
          "priceRange": "$23.26 - $38.76"  // per-option price range if shown, null otherwise
        }
      ]
    }
  ],
  "highlights": [],                        // seller-declared highlight bullets (materials, dimensions, etc.); empty when not shown
  "listedDate": "Jul 8, 2026",             // date extracted from 'Listed on ...' text; null when not present
  "relatedTags": [                         // links to related Etsy search / market pages surfaced on the listing
    {"text": "Personalized Wedding Scroll for Sale", "url": "https://www.etsy.com/market/personalized_wedding_scroll"}
  ]
}
```

Error handling:
- `{"error": true, "message": "blocked by anti-bot verification page"}` — DataDome interstitial; retry warm-up
- `{"error": true, "message": "not a listing page"}` — URL does not match `/listing/{id}/...`; check input URL
- Individual fields being `null` (e.g. `inCartCount`, `listedDate`) is normal — those elements are not always rendered

## Success Criteria

`result.error === false && result.listingId && result.title && result.imageCount >= 1 && (result.priceCurrent !== null)`

## Known Limitations

- DataDome anti-bot: fresh sessions may hit a CAPTCHA interstitial; warm up via `/` first
- `reviewCount` returned as displayed text (e.g. `7.8k`) rather than an exact integer, matching what Etsy shows on the page
- Variations that require dynamic selection to reveal a final price (e.g. color + size combined) return their per-option price range as displayed — combined price for a specific selection is not fetched
- `inCartCount` is only shown for listings that exceed Etsy's threshold ("N people have this in their cart"); most listings return `null`
- `highlights` appear on some categories only; when absent the field returns `[]`
- `relatedTags` may include tangentially-related Etsy market links that were surfaced in the page's link soup; treat as informational, not curated related-search
- `description` may include Unicode formatting characters and inline URLs; consumer code should sanitize if needed
- Multi-image listings return both product photos and user-uploaded review photos in the same list; the first ~20 URLs matching pattern `/il/…/il_fullxfull.` are the seller's own images

## Execution Efficiency

- **Batch orchestration**: Loop through listing URLs serially within a single session; insert 3-8 second sleeps between page navigations. Distribute URL batches across multiple stealth browser sessions for higher throughput
- **Test before batch execution**: Verify on 1-2 listings first before running the full batch
- **Reduce redundant pre-operations**: Warm-up once per session, then process listings sequentially in the same session
- **Skip description when unused**: pass `--include-description false` to shrink per-record output when descriptions are not needed downstream
- **Error resumption**: Save each listing's result to `results/{listingId}.json` immediately; on failure resume from the missing listing

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/etsy-scraper-etsy-product-detail.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what listings were used or how many results were returned — those are task outputs, not experience.
