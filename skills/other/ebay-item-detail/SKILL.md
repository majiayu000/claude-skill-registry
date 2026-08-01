---
name: ebay-item-detail
description: "Extracts full item detail from any open eBay item URL, returning JSON with url, itemNumber, title, subTitle, categories, price, priceWithCurrency, currency, wasPrice, available, availableText, sold, image, images, seller, sellerUrl, sellerFeedbackCount, sellerPositiveRating, itemLocation, brand, type, mpn, upc, ean, condition, shippingCost, shipping, whyToBuy, and itemSpecifics (full label/value map). Works across all eBay regional TLDs. Use when user mentions eBay item page, eBay listing detail, eBay product page, eBay itm, ebay.com/itm, eBay item scraper, extract eBay item details, eBay item specifics, scrape eBay item, eBay sold count, eBay availability, eBay brand MPN UPC EAN, eBay item location, eBay seller feedback, eBay wasPrice, eBay hi-res images, eBay itemNumber, eBay per-item enrichment. Also applies to enriching item URLs from a listing, monitoring price and stock, competitive product research, brand catalog audits, and pulling full field set from an individual eBay listing."
---

# eBay — Item Detail Extraction

> Input: an open eBay item URL (`/itm/{itemNumber}`) → Output: full detail JSON with 25+ fields (title, price, wasPrice, sold, available, seller, itemLocation, brand, MPN/UPC/EAN, condition, images, itemSpecifics map, whyToBuy signals, etc.).

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Given a live eBay item detail page, harvest every field visible on the listing that has clear semantic value (price surface, seller card, condition, item specifics table, sold / availability counters, item location, images) and return a compact JSON object suitable for downstream storage or comparison.

## Prerequisites

- Target page is already open in the browser: `https://www.ebay.{tld}/itm/{itemNumber}` — the extractor validates that the current URL matches `/itm/{digits}` and refuses to run otherwise.
- No login is required for public listings. Extraction runs against whatever the anonymous browser session sees.

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting.

### DOM: extract full item detail from the current item page

Precondition: `navigate {item URL}` → `wait stable` first. The page URL must be an eBay item URL (`/itm/{digits}`).

Extract: `eval "$(python scripts/extract-item-detail.py)"`

Parameters: none.

Output example:
```json
{
  "url": "https://www.ebay.com/itm/127962632528",
  "itemNumber": "127962632528",
  "title": "2017 Apple MacBook Pro 13.3\" i7 3.5GHz 16GB RAM 500GB SSD Space Gray A1706",
  "subTitle": null,                                 // .x-item-title__subTitle; often null
  "categories": ["Electronics", "Computers/Tablets & Networking", "Laptops & Netbooks", "Apple Laptops"],  // breadcrumb, deduped
  "price": 284.99,                                  // parsed numeric price
  "priceWithCurrency": "C $284.99",                 // original price string (with "or Best Offer" suffix stripped)
  "currency": "CAD",                                // ISO code inferred from prefix (US $, C $, AU $, HK $, SG $, NZ $, plain $, €, £, ¥, or explicit ISO in string)
  "wasPrice": null,                                 // strikethrough / MSRP; null when not discounted
  "wasPriceWithCurrency": null,
  "available": 1,                                   // integer; 1 when text is "LAST ONE"
  "availableText": "LAST ONE",                      // original availability string
  "sold": 982,                                      // parsed sold count
  "image": "https://i.ebayimg.com/images/g/hyIAAeSw23FqTV51/s-l1600.jpg",  // primary photo, upgraded to s-l1600
  "images": [                                       // deduplicated hi-res gallery
    "https://i.ebayimg.com/images/g/hyIAAeSw23FqTV51/s-l1600.jpg"
  ],
  "seller": "PayMore Halifax",                      // seller display name (parsed from _ssn metadata first, falls back to .x-sellercard-atf__info)
  "sellerUrl": "https://www.ebay.com/str/paymorehalifax",  // seller storefront or profile URL
  "sellerFeedbackCount": 18,                        // integer (K suffix expanded, e.g. 15.9K -> 15900)
  "sellerPositiveRating": 100,                      // percent as float
  "itemLocation": "Halifax, Nova Scotia, Canada",   // parsed from ux-labels-values Location row or Shipping "Located in:" tail
  "brand": "Apple",                                 // from Item specifics
  "type": "MacBook Pro",                            // from Item specifics "Type" or falls back to "Model"
  "mpn": "A1706",                                   // from Item specifics
  "upc": null,                                      // from Item specifics
  "ean": null,                                      // from Item specifics
  "condition": "Used",                              // short condition label (New / Used / etc.), long marketing prose trimmed
  "shippingCost": "Free",                           // "Free" if any free-shipping wording detected, otherwise the first currency-prefixed price found in the shipping row
  "shipping": "Free UPS Standard Canada. See detailsfor shippingLocated in: Halifax, Nova Scotia, Canada",  // full shipping-row text
  "whyToBuy": ["982 sold", "Free shipping", "Last one"],  // composed selling signals: sold count, free shipping flag, last-one flag, percent-off, top-rated seller flag
  "itemSpecifics": {                                // full label -> value map from the Item specifics section
    "Brand": "Apple",
    "Color": "Space Gray",
    "MPN": "A1706",
    "Model": "MacBook Pro",
    "Condition": "Used: An item that has been used previously...",
    "Location": "Halifax, Nova Scotia, Canada"
  }
}
```

Error handling:
- If the page URL does not contain `/itm/{digits}` (e.g., a redirect landed on `/sch/i.html`), the script returns `{"error": true, "message": "current URL does not look like an eBay item page ..."}`. Root cause is usually that the itemNumber points to an ended / sold-out listing and eBay redirected to a similar-item search; verify the item exists on eBay before retrying.
- If `h1.x-item-title__mainTitle` is absent, the script returns `{"error": true, "message": "item title not found ..."}`. Root causes: anti-bot interstitial, listing removed, or eBay changed the title selector. Take a `screenshot` and inspect the page state.
- Individual field-level `null` values are normal — many listings do not include UPC/EAN/MPN, wasPrice, sold count, sub-title, etc. Absence is not an error.

## Success Criteria

`error` field absent, `itemNumber` matches the `/itm/{digits}` portion of the URL, and `title` is a non-empty string. Field completeness is graded per-listing — expect at minimum: `url`, `itemNumber`, `title`, `price`, `priceWithCurrency`, `currency`, `image`, `seller`, `sellerUrl`, `condition`, `categories.length >= 1`.

## Known Limitations

- eBay regional geo-redirection: some regional TLDs (ebay.de, ebay.co.uk) will render the same item with localized subtitle wording ("Wird in neuem Fenster oder Tab geöffnet", etc.). The extractor strips these across the observed languages (English, German, French, Spanish, Italian, Dutch, Simplified Chinese, Japanese); other locales may leave residual accessibility suffixes in the raw text fields.
- Ended, sold-out, or removed listings often 302-redirect to a similar-item search page. The extractor detects this via URL mismatch and returns an error rather than scraping the wrong page.
- eBay obfuscates some class names on the sold-count line (`ONPa`, `h1WV`, etc. change over deploys). The extractor uses a text-pattern scan (`^{n} sold$`) instead of relying on those classes, which is stable across the observed language variants.
- Auction-specific fields (current bid, bid count, time-left) are not extracted by this component — they are part of the search-listing capability's per-card attribute row and are not surfaced consistently on the detail page.
- `whyToBuy` is a composed signal derived from other extracted fields (sold, wasPrice vs price, free-shipping flag, availability = last-one, top-rated seller heuristic). It is a convenience array; the underlying atomic fields are always present when meaningful.
- Extraction is DOM-based and reads only the initial server-rendered state. Fields that load lazily via later XHR (e.g., some seller reviews, live shipping estimates for the current buyer's ZIP) are not fetched — the extractor takes whatever the page shows at the moment of the eval.

## Execution Efficiency

- **Batch orchestration**: Feed item URLs (e.g., from a listing extractor) into a serial loop; `navigate → wait stable → eval`. Do not parallelize within one browser session — eBay throttles rapid item-detail hits from the same fingerprint. Insert a small pause (1–3s) between items to keep the traffic pattern natural. To increase throughput, run multiple stealth browser sessions in parallel — each has an independent fingerprint so rate limits apply per session.
- **Test before batch execution**: After wiring the loop, first process 2–3 items and inspect the output to confirm currency, seller, and Item specifics parse correctly for the current target vertical; only then run the full batch.
- **Reduce redundant pre-operations**: Reuse the same session across many item URLs; do not re-open the browser per item. Cache resolved detail JSON keyed by `itemNumber` so a re-run resumes from the next uncollected item.
- **Error resumption**: Persist per-item results (`tmp/items/{itemNumber}.json`) as they arrive; on failure, restart the loop with the "already collected" set filtered out.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/ebay-scraper-ebay-item-detail.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what item numbers were processed or how many fields were populated — those are task outputs, not experience.
