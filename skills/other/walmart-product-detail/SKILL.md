---
name: walmart-product-detail
description: "Walmart product detail page extractor: given a walmart.com product URL (walmart.com/ip/...), extract full product data including itemId, title, brand, model, UPC, price, wasPrice, currency, availability, category path, seller info, all images, shortDescription, longDescription, product highlights, full specifications as key-value map, color/size variants with item IDs, fulfillment options (shipping/pickup/delivery with dates), return policy, and review summary with rating breakdown. Use when user mentions walmart product detail, walmart item page, walmart product page, scrape walmart product, extract walmart item, walmart product data, walmart item details, walmart product info, walmart product scraper, walmart item scraper, walmart product URL, walmart ip URL, walmart.com/ip, walmart specifications, walmart product specs, walmart product images, walmart variants, walmart color options, walmart size options, walmart seller info, walmart return policy, walmart fulfillment options, walmart shipping info, walmart availability, walmart product enrichment. Also applies to enriching a list of walmart product URLs with full details, monitoring walmart product price and availability changes, building a walmart product catalog, competitive product research on walmart, and batch collection of full product data from walmart item IDs."
---

# Walmart — Product Detail

> product URL → full structured product data from walmart.com product detail page

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract complete product data from a Walmart product detail page, including pricing, images, specifications, variants, fulfillment options, and review summary.

## Prerequisites

- Target product page is open in the browser: `https://www.walmart.com/ip/{product-slug}/{item-id}`

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### DOM: extract full product data from current product page

Navigate to the product URL first, then extract:

1. `navigate "https://www.walmart.com/ip/{product-slug}/{item-id}"`
2. `wait stable`
3. `eval "$(python scripts/extract-product-detail.py)"`

The `item-id` is the numeric Walmart item ID (usItemId). The `product-slug` portion of the URL does not affect which product is loaded — only the `item-id` matters.

Output example:
```json
{
  "itemId": "18656507313",
  "url": "https://www.walmart.com/ip/HP-14-N150-4-128-Blue/18656507313",
  "title": "HP 14 inch HD Windows Laptop Intel Processor N150 4GB 128GB UFS Waterfall Blue",
  "brand": "HP",
  "brandUrl": "https://www.walmart.com/search?q=HP&facet=brand:HP",
  "model": "14-ep2112wm",
  "upc": "199764359186",
  "manufacturerProductId": "CQ5J6UA#ABA",
  "classType": "VARIANT",
  "price": 229,
  "priceString": "$229.00",
  "currencyUnit": "USD",
  "wasPrice": null,
  "availability": "IN_STOCK",
  "category": [
    {"name": "Electronics", "url": "https://www.walmart.com/cp/electronics/3944"},
    {"name": "Laptops", "url": "https://www.walmart.com/cp/laptops/3951"}
  ],
  "sellerId": "F55CDC31AB754BB68FE0B39041159D63",
  "sellerName": "Walmart.com",
  "sellerDisplayName": "Walmart.com",
  "sellerType": "INTERNAL",
  "sellerAverageRating": null,
  "sellerReviewCount": null,
  "averageRating": 4.4,
  "numberOfReviews": 63,
  "thumbnail": "https://i5.walmartimages.com/seo/HP-14.jpeg",
  "images": ["https://i5.walmartimages.com/seo/image1.jpeg", "https://i5.walmartimages.com/asr/image2.jpeg"],
  "shortDescription": "The HP 14 inch Laptop PC has it all...",
  "longDescription": "<ul><li><strong>Intel N150 processor:</strong> ...</li></ul>",
  "productHighlights": [
    {"name": "RAM memory", "value": "4 GB"},
    {"name": "Processor", "value": "N150"}
  ],
  "specifications": {
    "RAM memory": "DDR5",
    "OS": "Windows 11",
    "Screen size": "14 in",
    "Weight": "3.11 lb"
  },
  "variants": [
    {
      "name": "Actual Color",
      "type": "DROPDOWN",
      "options": [
        {"id": "actual_color-tranquilpink", "name": "Tranquil pink", "availability": "AVAILABLE", "itemIds": ["6G9VW0QQAI2X"]},
        {"id": "actual_color-waterfallblue", "name": "Waterfall blue", "availability": "AVAILABLE", "itemIds": ["4QPDNGIGKZZ8"]}
      ]
    }
  ],
  "fulfillmentOptions": [
    {"type": "SHIPPING", "status": "IN_STOCK", "freeShipping": true, "deliveryDate": "2026-07-09T21:59:00.000Z", "fulfillmentBadge": "Tomorrow"},
    {"type": "PICKUP", "status": "IN_STOCK", "freeShipping": true, "deliveryDate": null, "fulfillmentBadge": "Today"},
    {"type": "DELIVERY", "status": "IN_STOCK", "freeShipping": false, "deliveryDate": null, "fulfillmentBadge": "Today"}
  ],
  "returnPolicy": {
    "returnable": true,
    "freeReturns": true,
    "returnWindowDays": 30,
    "returnPolicyText": "Free 30-day returns"
  },
  "reviewSummary": {
    "averageRating": 4.2,
    "totalReviews": 279,
    "ratingBreakdown": {"5": 191, "4": 29, "3": 15, "2": 10, "1": 34},
    "reviewsLookupId": "19X7KSSCUQU5"
  }
}
```

Error response (when extraction fails or wrong page):
```json
{"error": true, "message": "No product in __NEXT_DATA__. Ensure the page is a Walmart product detail page (walmart.com/ip/...)."}
```

## Success Criteria

`itemId` is non-null AND `title` is non-null AND `price` is non-null OR `availability` is non-null

## Known Limitations

- `wasPrice` is null unless the item currently has an active markdown/rollback promotion
- `sellerAverageRating` and `sellerReviewCount` are null for Walmart first-party listings (INTERNAL sellerType)
- `longDescription` may be null for items without IDML data (less common)
- `specifications` may be empty for items without IDML specifications
- Variant `itemIds` are internal product IDs (format: alphanumeric, e.g., "6G9VW0QQAI2X"), not the usItemId; to get the usItemId for a specific variant, navigate to that variant's URL
- Delivery dates in `fulfillmentOptions` reflect the browser session's location context (set by the browser's stored zip code)

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through product URLs serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Add 1–2 second intervals between navigations. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/walmart-scraper-walmart-product-detail.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what product URLs were scraped or what prices were found — those are task outputs, not experience.
