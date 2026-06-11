---
name: taobao-keyword-search
description: "Search Taobao and Tmall product listings by keyword, returning paginated product cards with title, price, shop, image, sales, and tags. Use when user asks to search Taobao, find products on Taobao/Tmall, scrape Taobao search results, get product listings from Taobao, collect Taobao items by keyword, 搜索淘宝, 淘宝关键词搜索, 采集淘宝商品, 抓取淘宝搜索结果, 淘宝天猫商品列表. Also applies to bulk keyword searches, price monitoring across keywords, and competitive product research on Taobao."
---

# Taobao — Keyword Search

> keyword + optional filters → paginated product listing (itemId, title, price, shop, image, sales)

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Search Taobao/Tmall for products by keyword and extract product cards from search results pages.

## Prerequisites

- Target page is already open in the browser: `https://s.taobao.com/search`
- User is logged in to Taobao (user avatar or nickname visible in the page header)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

If login status for Taobao has been confirmed in the current session → skip this step.

Otherwise: open `https://www.taobao.com` and observe the page header:
- User nickname visible (e.g., "心林vs妞妞") → logged in, continue execution
- "亲，请登录" or login button visible → not logged in, inform the user that Taobao login is needed first, assist the user in completing the login flow

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### DOM: product search results (data extraction)

Navigate to search results URL, then extract:

1. `navigate "https://s.taobao.com/search?q={keyword}&page={page}&ie=utf8"`
2. `wait stable`
3. `eval "$(python scripts/search-products.py '{keyword}' --page {page} --sort '{sort}' --tab '{tab}' --start-price {startPrice} --end-price {endPrice})"`

URL Parameters:
- `q`: URL-encoded keyword
- `page`: page number, 1-based, default `1`
- `sort`: sort order — empty string (default/recommended), `sale-desc` (by sales), `price-asc` (price low→high), `price-desc` (price high→low)
- `tab`: `mall` for Tmall-only results; omit for all results
- `startPrice` / `endPrice`: price range filter in yuan (e.g., `startPrice=100&endPrice=500`)

Output example:
```json
[
  {
    "itemId": "694593508978",
    "itemUrl": "https://item.taobao.com/item.htm?id=694593508978",
    "title": "蓝牙耳机2025新款官方",
    "subTitle": "AI耳机热卖榜第1名",
    "priceYuan": 79.9,
    "priceDesc": "券后价",
    "imageUrl": "https://img.alicdn.com/imgextra/...",
    "salesCount": "40万+人付款",
    "shopName": "金运旗舰店",
    "location": "广东",
    "rating": null,
    "tags": ["政府补贴15%", "官方立减26元"]
  }
]
```

Notes:
- `priceYuan` is the displayed price (may be post-coupon price, not pre-coupon)
- `priceDesc` indicates price type: `券后价` (after coupon), `补贴价` (subsidized price), etc.
- `rating` is rarely shown on search cards; null is expected
- Sponsored/ad items have `itemUrl` pointing to `click.simba.taobao.com` — they will have `itemId` extracted from query params

## Enum Parameters

[collection failed] `sort` values: confirmed values are empty string (default), `sale-desc`, `price-asc`, `price-desc`; no API for enumeration, values are hardcoded constants.

## Pagination

**URL Pagination**: URL pattern `https://s.taobao.com/search?q={keyword}&page={N}&ie=utf8`, increment `page` from 1. Each page returns ~47 items. Termination: when `result count < 10` or returned items duplicate previous page.

## Success Criteria

`result count >= 1` and `itemId` non-null rate = 100%

## Known Limitations

- Requires Taobao login; unauthenticated sessions redirect to login page
- Prices shown are displayed prices (may be post-coupon), not pre-discount prices
- Sponsored/ad items appear at unpredictable positions in results
- Price filter (`startPrice`/`endPrice`) filters on pre-coupon prices, so post-coupon prices displayed may fall outside the requested range near boundaries
- Taobao may return different result counts across pages; page count is approximate

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through keywords serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Add 2–3 second intervals between page navigations. To increase throughput, open multiple stealth browser sessions and distribute keywords across them.
- **Test before batch execution**: After writing a batch script, you must first test with 1–2 keywords to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly.
- **Reduce redundant pre-operations**: When scraping multiple pages for one keyword, navigate page 2, 3 etc. within the same session without re-login checks.
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/taobao-keyword-search.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
