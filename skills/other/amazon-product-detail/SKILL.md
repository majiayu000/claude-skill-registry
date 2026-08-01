---
name: amazon-product-detail
description: "Amazon product detail page scraper: extract full product data from any open Amazon product detail URL (any /dp/{asin} or /gp/product/{asin} page across all Amazon regional TLDs) — returns asin, url, title, brand, price, listPrice, stars, reviewsCount, starsBreakdown (5/4/3/2/1 star percentages), answeredQuestions, inStock, inStockText, delivery, fastestDelivery, returnPolicy, breadCrumbs, features (bullet points), description, bookDescription, thumbnailImage, highResolutionImages, galleryThumbnails, productOverview (Brand/Model/etc.), attributes (tech spec table), attributesMapped (flat key-value), bestsellerRanks (rank + category + url), variantAttributes (currently selected color/size/style), variantAsins, seller (name + id + url), isAmazonChoice, amazonChoiceText, monthlyPurchaseVolume, hasAPlusContent, hasBrandStory, aiReviewsSummary, reviewsLink, productPageReviews (sample), videosCount, locationText, loadedCountryCode. Works on amazon.com, amazon.co.uk, amazon.de, amazon.co.jp, amazon.fr, amazon.it, amazon.es, amazon.ca, amazon.com.au, amazon.in, amazon.com.mx, amazon.com.br, amazon.nl, amazon.se, amazon.sg, amazon.ae, amazon.sa, amazon.pl, amazon.tr, amazon.eg. Use when user mentions Amazon product page, Amazon /dp/, Amazon dp URL, Amazon ASIN scraper, Amazon product detail, Amazon PDP, Amazon product data, Amazon product info, Amazon product fields, Amazon product attributes, Amazon full field extraction, Amazon per-ASIN enrichment, Amazon rating breakdown, Amazon stars breakdown, Amazon bestseller rank, Amazon BSR, Amazon variants, Amazon variant ASINs, Amazon color size options, Amazon feature bullets, Amazon A+ content, Amazon brand story, Amazon AI review summary, Amazon bought in past month, Amazon monthly sales volume, Amazon Amazon's Choice badge, Amazon seller info, scrape Amazon product, enrich Amazon ASIN, Amazon ASIN details, Amazon product review data. Also applies to bulk ASIN enrichment from a list of URLs, competitive product research, brand catalog audits, price and stock monitoring per ASIN, and building a normalized product dataset from a list of Amazon URLs."
---

# Amazon — Product Detail

> Input any Amazon product URL → output full product record (100+ fields).

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract the complete product record from any Amazon detail page URL across all Amazon regional TLDs, including price, ratings breakdown, attributes, variants, bestseller ranks, seller info, delivery, and sample reviews.

## Prerequisites

- Target page is already open in the browser: any Amazon product URL (e.g. `https://www.amazon.com/dp/{ASIN}`, `https://www.amazon.com/gp/product/{ASIN}`, `https://www.amazon.co.uk/dp/{ASIN}`, or the canonical SEO-slug URL `https://www.amazon.com/{slug}/dp/{ASIN}`)
- No login required

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `browser-act --session {name} eval "$(python scripts/xxx.py {params})"`. The `$(...)` is bash command substitution — it runs the python script, captures its printed JS text, and hands that JS string as a single argument to `browser-act eval`. Do not run `eval "$(python ...)"` as a bare shell command; that would ask bash to execute the JS as shell, which fails.

### DOM: extract full product detail from current product page

Amazon detail pages are server-rendered HTML — no XHR/fetch API for detail data. All fields come from stable DOM selectors:

1. `navigate {any Amazon product URL, e.g. https://www.amazon.com/dp/{ASIN}}`
2. `wait stable`
3. Extract: `browser-act --session {name} eval "$(python scripts/extract-product-detail.py)"`

On error paths, the script returns:
- `{"error": true, "message": "product_not_found: 404 page"}` when the URL resolves to Amazon's not-found page
- `{"error": true, "message": "productTitle not found - page may not be a product detail page"}` when the URL resolves to a non-detail page (e.g. search results, homepage)

Output example:
```json
{
  "asin": "B09S3HNMHF",                                // parsed from /dp/{ASIN} or /gp/product/{ASIN} path segment
  "url": "https://www.amazon.com/dp/B09S3HNMHF",       // canonical origin + pathname
  "title": "Samsung 14\" Galaxy Chromebook Go ...",    // #productTitle
  "brand": "Samsung",                                  // #bylineInfo, falls back to attributesMapped.Brand/Manufacturer
  "price": {"value": 179.99, "currencyRaw": "$", "raw": "$179.99"},   // current buybox price, null when no offer
  "listPrice": {"value": 190.99, "currencyRaw": "$", "raw": "$190.99"}, // strike-through list price, null when absent
  "stars": 4.3,                                        // 0-5 average rating, null when no reviews
  "reviewsCount": 632,                                 // total review count, null when no reviews
  "starsBreakdown": {"5 star": 70, "4 star": 13, "3 star": 5, "2 star": 3, "1 star": 9},  // percentage per star bucket
  "answeredQuestions": null,                           // number, null when absent or non-numeric
  "inStock": true,                                     // derived from availability text, null when unclear
  "inStockText": "In Stock",                           // raw #availability text
  "delivery": "FREE delivery Wednesday, July 15",      // primary delivery message, null when absent
  "fastestDelivery": null,                             // secondary/fastest delivery, null when absent
  "returnPolicy": "30-day return period",              // null when absent
  "breadCrumbs": "Electronics > Computers > Laptops > Traditional Laptops",  // joined with ' > ', "" when absent
  "features": ["Slim design", "12-hour battery", "..."],  // #feature-bullets bullet points
  "description": "A+ in performance and value...",     // #productDescription, null when absent
  "bookDescription": null,                             // #bookDescription_feature_div for books, null otherwise
  "thumbnailImage": "https://m.media-amazon.com/images/I/51...jpg",
  "highResolutionImages": ["https://m.media-amazon.com/images/I/51...SY450_.jpg", "..."],  // from #imgTagWrapperId data-a-dynamic-image JSON
  "galleryThumbnails": ["https://m.media-amazon.com/images/I/41...jpg", "..."],
  "productOverview": [{"key": "Brand", "value": "Samsung"}, {"key": "Model Name", "value": "XE340XDA-KA2US"}],  // #productOverview_feature_div table
  "attributes": [{"key": "Color", "value": "Silver"}, {"key": "Item Weight", "value": "3.2 pounds"}],  // technical spec tables
  "attributesMapped": {"Brand": "Samsung", "Item Weight": "3.2 pounds"},  // flat merged key-value
  "bestsellerRanks": [
    {"rank": 44, "category": "Computers & Accessories", "url": "https://www.amazon.com/gp/bestsellers/pc/..."},
    {"rank": 5, "category": "Traditional Laptop Computers", "url": "https://www.amazon.com/gp/bestsellers/pc/13896615011/..."}
  ],
  "variantAttributes": [{"key": "Color", "value": "Silver"}],  // currently selected variant dimensions
  "variantAsins": ["B09S3HNMHF", "B0G4WBD45V", "B0GG2CPM1K"],  // all variant ASINs from swatches, empty [] when no variants
  "seller": {"name": "Amazon.com", "id": "ATVPDKIKX0DER", "url": "https://www.amazon.com/sp?seller=..."},  // null when no seller link
  "isAmazonChoice": false,                             // .ac-badge-rectangle presence
  "amazonChoiceText": null,                            // Amazon's Choice label text, null when badge absent
  "monthlyPurchaseVolume": "6K+ bought in past month", // #social-proofing-faceout-title-tk_bought, null when absent
  "hasAPlusContent": true,                             // #aplus presence
  "hasBrandStory": false,                              // #brand-snapshot_feature_div presence
  "aiReviewsSummary": null,                            // AI-generated review summary text, null when absent
  "reviewsLink": "https://www.amazon.com/product-reviews/B09S3HNMHF",
  "productPageReviews": [
    {"username": "Jane D.", "ratingScore": 5, "reviewTitle": "Great product!", "reviewDescription": "Really happy with this purchase.", "date": "Reviewed in the United States on January 15, 2025"}
  ],
  "videosCount": null,                                 // count of gallery video slots, null when none
  "locationText": "Update location",                   // #glow-ingress-line2 delivery-location display
  "loadedCountryCode": "com"                           // amazon.{tld} suffix used to detect region (com, co.uk, de, co.jp, etc.)
}
```

## Success Criteria

`response.error is not present AND response.asin matches /^[A-Z0-9]{10}$/ AND response.title is a non-empty string`

## Known Limitations

- `answeredQuestions` is `null` on many pages because Amazon's Q&A widget layout varies; when present, the field surfaces the numeric count.
- `aiReviewsSummary` is populated only on products with sufficient reviews and Amazon's AI summary feature enabled.
- `variantAsins` covers ASINs visible in swatch elements (`data-defaultasin`, `data-asin`, `data-dp-url`); large twister structures whose variants are lazy-loaded via XHR only surface the visible subset on first render.
- `productPageReviews` returns the sample reviews Amazon renders on the detail page (typically 6-10 items) — for full review pagination use a separate review-scraping capability.
- Prices, delivery, and stock reflect the browsing session's inferred country/zip; use a proxy in the target region to fetch localized values.
- CAPTCHA / anti-bot interstitials will cause the script to return `productTitle not found` — surface this to the caller so it can retry with a fresh session or proxy.
- Bestseller ranks are only populated when the product page renders the "Best Sellers Rank" row in detail bullets or product-details tables.
- Amazon A/B experiments occasionally reorder DOM containers; on failure to extract a specific field, inspect page structure and open an issue rather than assuming Amazon-wide breakage.

## Execution Efficiency

- **Batch orchestration**: Write a bash script iterating ASINs serially inside one browser session; do not parallelize inside one browser. Insert a 3-6 second delay between ASINs to reduce anti-scraping pressure. For higher throughput, open multiple stealth sessions (different fingerprints/proxies) and shard the ASIN list.
- **Test before batch execution**: After writing the batch script, first test with 2-3 ASINs before running the full enrichment. Never skip testing.
- **Reduce redundant pre-operations**: Reuse the same browser session across ASINs — only `navigate` + `wait stable` + `eval` per item, no need to re-open.
- **Error resumption**: Persist per-ASIN JSON as it completes so a partial crash resumes from the failed ASIN.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/amazon-scraper-amazon-product-detail.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
