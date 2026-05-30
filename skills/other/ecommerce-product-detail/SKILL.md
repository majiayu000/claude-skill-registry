---
name: ecommerce-product-detail
description: "Extract complete product information from any e-commerce product page. Returns name, price, currency, brand, images, description, SKU/ASIN/EAN/UPC/GTIN/MPN identifiers, stock availability, rating, review count, variants, and seller. Works on Shopify, Amazon, WooCommerce, eBay, Walmart, Etsy, AliExpress, Alibaba, Target, Best Buy, Rakuten, Magento, BigCommerce, PrestaShop, and any public e-commerce site. Accepts product URL, keyword, or product identifier (SKU/ASIN/EAN/UPC). Use when: scrape product page, get product details, extract price and availability, product info extraction, check product data, product detail scraping, get product from URL, keyword product search, ASIN lookup, EAN search, UPC lookup, price check, product research, compare products, monitor product price, get product images, product brand and description, ecommerce data extraction, product catalog scraping, product page scraper, get item price, fetch product info."
---

# E-commerce — Product Detail

> Product URL / keyword / SKU → complete product data (name, price, brand, images, identifiers, availability, rating, variants)

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract complete product information from any publicly accessible e-commerce product page using a universal multi-layer extraction strategy (JSON-LD → platform-specific DOM → OG meta → microdata).

## Prerequisites

- Target browser is open and connected
- No login required for public product pages

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. Use the bash tool for execution.

### DOM: Extract product data from current product page

Navigate to the product URL first, then extract:

```bash
eval "$(python scripts/extract-product.py)"
```

Output example:
```json
{
  "url": "https://www.amazon.com/dp/B09WNK39JN",
  "name": "Amazon Echo Pop",
  "price": 39.99,
  "price_currency": "USD",
  "brand": "Amazon",
  "image": "https://m.media-amazon.com/images/I/61bTwy0ooPL.jpg",
  "images": ["https://...jpg", "https://...jpg"],
  "description": "Compact smart speaker with Alexa...",
  "category": ["Electronics", "Smart Speakers"],
  "sku": "B09WNK39JN",
  "gtin": null,
  "mpn": null,
  "availability": "InStock",
  "rating": 4.7,
  "review_count": 103789,
  "variants": [{"name": "Charcoal", "sku": "B09WNK39JN", "price": 39.99}],
  "seller": "Amazon",
  "identifiers": {"ASIN": "B09WNK39JN", "Best Sellers Rank": "#1 in Smart Speakers"},
  "_platform": "amazon",
  "_source": "json-ld"
}
```

### Composite: Keyword or SKU → product detail

When input is a keyword, ASIN/SKU, or EAN/UPC rather than a direct product URL:

**Step 1 — Navigate to search URL based on input type:**

| Input type | Target site | URL pattern |
|-----------|-------------|-------------|
| ASIN (10-char alphanumeric) | Amazon | `https://www.amazon.com/dp/{ASIN}` |
| Keyword | Amazon | `https://www.amazon.com/s?k={keyword_urlencoded}` |
| Keyword | eBay | `https://www.ebay.com/sch/i.html?_nkw={keyword_urlencoded}` |
| Keyword | Walmart | `https://www.walmart.com/search?q={keyword_urlencoded}` |
| Keyword + `--site` specified | Any site | `https://{site}/search?q={keyword_urlencoded}` |
| Keyword (no site) | Cross-site | `https://www.google.com/search?tbm=shop&q={keyword_urlencoded}` |
| EAN / UPC / GTIN | Cross-site | `https://www.google.com/search?tbm=shop&q={identifier}` |

**Step 2 — If landed on a search/listing page (multiple results):**
1. `wait stable`
2. `eval "$(python scripts/extract-listing.py --max-results 3)"` — get top 3 results
3. Pick the most relevant product URL from `items[0].url`
4. `navigate {product_url}` → `wait stable`

**Step 3 — Extract product data:**
```bash
eval "$(python scripts/extract-product.py)"
```

Note: `scripts/extract-listing.py` is located in `../ecommerce-listing/scripts/extract-listing.py` if used as a standalone Skill install; otherwise reference the listing Skill.

## Success Criteria

`result.name != null AND (result.price != null OR result.availability != null)`

## Known Limitations

- Amazon bot detection: direct navigation to a product URL may redirect to a CAPTCHA or bot-check page on fresh sessions. Navigate from `https://www.amazon.com` first to establish session cookies, then navigate to the product page
- eBay product pages may require navigating from `https://www.ebay.com` first; use `solve-captcha` if a challenge appears
- Some sites render product data entirely via client-side JavaScript; always use `wait stable` before extracting
- Price may be null for out-of-stock items or when login is required to view pricing
- Variant data completeness depends on whether the site includes full variant markup in JSON-LD

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through product URLs serially within a single session; add 1–2 second intervals between requests to avoid triggering anti-scraping restrictions
- **Test before batch execution**: Test with 1–2 URLs before running the full batch
- **Error resumption**: Save results item by item; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/ecommerce-scraper-ecommerce-product-detail.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`
