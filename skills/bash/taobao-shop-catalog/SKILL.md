---
name: taobao-shop-catalog
description: "Browse a Taobao or Tmall shop's product catalog by shopId, returning paginated product listings with itemId and title. Use when user asks to scrape a Taobao shop, get all products from a store, list items in a Taobao/Tmall shop, fetch shop catalog by userId or shopId, 采集淘宝店铺商品, 抓取淘宝店铺所有商品, 获取天猫店铺商品列表, 淘宝店铺目录, 按店铺ID采集商品. Also applies to shop inventory monitoring, competitor store analysis, and bulk itemId collection from a specific seller."
---

# Taobao — Shop Catalog

> shopId → paginated shop product listing (itemId, title, image URL)

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Navigate to a Taobao or Tmall shop's catalog page and extract product listings.

## Prerequisites

- Target page is already open in the browser: `https://shop{shopId}.taobao.com/category.htm`
- User is logged in to Taobao (user avatar or nickname visible in the page header)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

If login status for Taobao has been confirmed in the current session → skip this step.

Otherwise: open `https://www.taobao.com` and observe the page header:
- User nickname visible → logged in, continue execution
- Login button visible → not logged in, inform the user that Taobao login is needed first, assist the user in completing the login flow

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### DOM: shop catalog product list (data extraction)

Navigate to the shop's catalog page, then extract:

1. `navigate "https://shop{shopId}.taobao.com/category.htm?search=y&pageNo={page}"`
   - Note: Tmall shops redirect to `https://{shopName}.tmall.com/category.htm?search=y&pageNo={page}`
   - The `search=y` parameter activates the paginated search mode
2. `wait stable`
3. `eval "$(python scripts/extract-catalog.py '{shopId}' --page {page})"`

Parameters:
- `shopId`: numerical shop ID (e.g., `67095450`); found in shop URL as `shop{shopId}.taobao.com`
- `--page`: page number, 1-based, default `1`

Output example:
```json
[
  {
    "itemId": "1041516493508",
    "title": "绿联T8梯形排插插座转换器插线板大间距宿舍桌面充电多孔位插排",
    "imageUrl": "https://img.alicdn.com/imgextra/...",
    "itemUrl": "https://detail.tmall.com/item.htm?id=1041516493508"
  }
]
```

Notes:
- `price` is not included — Taobao shop catalog pages use font-based price obfuscation that cannot be decoded via DOM extraction. Use the `taobao-product-detail` skill to fetch prices for specific items.
- `imageUrl` may be a lazy-loaded URL from `data-ks-lazyload-custom` attribute when the image has not scrolled into view

Error handling: if result count = 0, check that the page loaded correctly (`screenshot`), confirm the shopId is valid, and retry. Some shops may be Tmall-only and require following the redirect URL.

## Pagination

**URL Pagination**: URL pattern `https://shop{shopId}.taobao.com/category.htm?search=y&pageNo={N}` (or `https://{shopName}.tmall.com/category.htm?search=y&pageNo={N}` after redirect), increment `pageNo` from 1. Each page returns up to 60 items. Termination: when `result count = 0` or next page link `href` with `pageNo={N+1}` is absent from the DOM.

Next page link selector: `a[href*="pageNo"]` (contains the next page number).

## Success Criteria

`result count >= 1` and `itemId` non-null rate = 100%

## Known Limitations

- Prices are font-obfuscated on the shop catalog page and cannot be extracted; fetch individual item prices via `taobao-product-detail`
- Some shop categories are not shown in the default `category.htm` view; category-specific browsing requires clicking category links in the shop nav
- Shop redirect from `shop{id}.taobao.com` to `{name}.tmall.com` changes the URL structure; the script handles both

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through pages serially; add 2–3 second intervals between navigations.
- **Test before batch execution**: After writing a batch script, you must first test with 1–2 pages to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly.
- **Reduce redundant pre-operations**: Stay in the same session for all pages of one shop without re-login checks.
- **Error resumption**: Save results page by page during batch processing; on failure, resume from the last successful page rather than starting over.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/taobao-shop-catalog.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
