---
name: acp-product-feed
description: Build product feed generation and submission for ACP. Use when implementing product catalog export, feed formatting (CSV/JSON/XML/TSV), feed validation, and push-based catalog sync to the agent platform.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# ACP Product Feed

## Before writing code

**Fetch live docs**: Fetch `https://developers.openai.com/commerce/product-feeds/spec` for the exact feed field specifications, supported formats, required vs optional fields, and submission endpoint.

Also web-search `site:developers.openai.com commerce feed` for any updates to feed requirements.

## Conceptual Architecture

### What Product Feeds Do

ACP uses a **push model** for product discovery. Merchants generate structured product data files and push them to the agent platform's ingestion endpoint. The agent (ChatGPT) indexes this data to surface products in conversational shopping.

### Feed Formats

Four supported formats:
- **CSV** — Comma-separated, with header row
- **JSON** — Array of product objects
- **XML** — Structured product elements
- **TSV** — Tab-separated, with header row

### Feed Fields (~40+ fields across 15 categories)

Key field categories include:
1. **Identification** — Product ID, title, brand, SKU, GTIN/UPC/EAN
2. **Pricing** — Price, sale price, currency, price effective dates
3. **Media** — Image URLs, additional images, product page URL
4. **Fulfillment** — Availability, shipping info, condition, fulfillment type
5. **Attributes** — Category, description, color, size, material, gender, age group, custom attributes
6. **Eligibility** — `is_eligible_search` (controls ChatGPT search visibility), `is_eligible_checkout` (controls ChatGPT checkout visibility) — both are critical required fields
7. **Seller Info** — `seller_name`, `seller_url`, `target_countries`, `store_country` — required fields identifying the merchant and market

### Refresh Frequency

Feeds can be refreshed up to **every 15 minutes**. Merchants should refresh more frequently for volatile data (pricing, stock) and less frequently for static data (descriptions, images).

### Key Concepts

- **Product variants** — Size/color/material variants are separate feed entries linked by a group ID
- **Availability signals** — `in_stock`, `out_of_stock`, `pre_order`, `backorder`, `unknown`
- **Price formatting** — Check feed spec for exact format (may differ from checkout's integer minor units)
- **Image requirements** — Minimum resolution, accepted formats, primary vs additional images
- **Category taxonomy** — Standard category paths for product classification

### Use Cases

- E-commerce catalog export
- Shopify/WooCommerce product sync
- Multi-channel product distribution
- Inventory-aware feed generation (suppress out-of-stock)
- Scheduled feed refresh pipelines

### Best Practices

- Validate feed against the spec schema before submission
- Include GTIN/UPC when available for better product matching
- Use high-quality primary images (min resolution per spec)
- Set appropriate refresh intervals based on data volatility
- Handle feed generation errors gracefully — partial feeds are better than no feeds
- Log submission responses for debugging

Fetch the feed spec for exact field names, types, constraints, validation rules, and the submission endpoint URL before implementing.
