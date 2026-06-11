---
name: goofish-search-list
description: "Scrapes second-hand item search results from Goofish (闲鱼/xianyu, goofish.com) — China's largest second-hand marketplace. Input: keyword, optional sort/filter params. Output: list of items with id, title, price, image, location, want-count per page (30 items/page). Use when user mentions goofish, 闲鱼, xianyu, 二手交易, second-hand marketplace China, 二手商品搜索, search used goods, scrape goofish listings, xianyu search results, collect second-hand prices, monitor used item prices, 闲鱼关键词搜索, 闲鱼数据采集, 批量抓取闲鱼, goofish scraper, goofish data, xianyu data extraction, 二手商品价格监控, used iPhone prices, 二手手机价格. Also applies to: price research on Chinese second-hand market, competitor product monitoring via used goods listings, inventory analysis."
---

# Goofish (闲鱼) — Search Results List

> keyword + optional filters → list of 30 second-hand item cards per page (id, title, price, image, location, want-count)

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract second-hand item listing cards from Goofish keyword search results, supporting sort options, price range filters, and publish-date filters, with page-by-page pagination.

## Prerequisites

- Browser with an active Goofish session (logged-in account recommended for full results)
- Target page is already open or will be opened: `https://www.goofish.com/search?q={keyword}`

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

If login status for Goofish has been confirmed in the current session → skip this step.

Otherwise: open `https://www.goofish.com/` and observe the page:
- User avatar or account entry exists → logged in, continue
- Login/register prompt → not logged in; inform user that login may be required for full results; assist login if needed

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

### Network Capture: trigger search and load results

Search requests use a dynamic `sign` token computed client-side — they cannot be reconstructed directly. Navigate to the search URL to trigger the API automatically.

1. `navigate https://www.goofish.com/search?q={keyword}`
2. `wait stable`
3. Proceed to DOM extraction below

Error handling: If the page shows a CAPTCHA slider ("Please slide to verify") instead of search results, the session has been rate-limited. Wait 5–10 minutes before retrying, or switch to a fresh browser session.

### DOM: search result item cards (data extraction)

After navigating and waiting stable, extract all 30 item cards on the current page:

`eval "$(python scripts/extract-search-items.py)"`

Output example:
```json
{
  "items": [
    {
      "item_id": "1054668718340",        // unique item ID
      "category_id": "126862528",        // category ID
      "item_url": "https://www.goofish.com/item?id=1054668718340&categoryId=126862528",
      "title": "美版iPhone 14 国行256G 纯原 原版原漆",  // full title text
      "image_url": "https://img.alicdn.com/bao/uploaded/...",  // thumbnail URL
      "price": "1810",                   // numeric string, CNY, no ¥ sign
      "service_tag": "Apple/苹果256GB无任何维修",  // condition/attribute tag or recency label, null if absent
      "price_desc": "2人想要",           // want-count or price-drop info, null if absent
      "location": "广东"                 // seller's location province/city
    }
  ],
  "count": 30
}
```

### DOM: apply sort and filter options (operation)

Apply sort order, publish-date filter, or price range before extracting. Call before running `extract-search-items.py`. After calling, `wait stable` before extracting.

`eval "$(python scripts/apply-search-filters.py --sort {sort} --publish-days {days} --price-min {min} --price-max {max})"`

Parameters:
- `--sort`: Sort option — `""` default (综合), `"reduce"` price-drop (新降价), `"create"` newest (新发布), `"price-asc"` price low-to-high, `"price-desc"` price high-to-low. Default: `""`
- `--publish-days`: Filter by publish date — `""` all, `"1"` within 1 day, `"3"` within 3 days, `"7"` within 7 days, `"14"` within 14 days. Default: `""`
- `--price-min`: Minimum price (CNY integer string, e.g., `"500"`). Requires `--price-max`. Default: `""`
- `--price-max`: Maximum price (CNY integer string, e.g., `"3000"`). Requires `--price-min`. Default: `""`

Output example:
```json
{
  "ok": true,
  "applied": {
    "sort": "reduce:desc",
    "searchFilter": "publishDays:7;priceRange:500,3000;"
  }
}
```

### DOM: navigate to a specific page (operation)

`eval "$(python scripts/goto-page.py {page_number})"`

Parameters:
- `page_number`: Target page number (integer, 1-based)

Output example:
```json
{ "ok": true, "clicked_page": 2 }
```

After clicking, `wait stable` then re-run `extract-search-items.py` to get the new page's items.

## Enum Parameters

[AI] sort options: `""` (综合/default), `"reduce"` (新降价), `"create"` (新发布/最新), `"price-asc"` (价格从低到高), `"price-desc"` (价格从高到低)

[AI] publish-days filter: `""` (all), `"1"`, `"3"`, `"7"`, `"14"`

## Pagination

**DOM Pagination**: Click the target page number button using `goto-page.py {page}`, then `wait stable`, then re-run `extract-search-items.py`. Page numbers appear in the pagination bar at the bottom of the search results.

Termination: When `goto-page.py` returns `error: Page N not found` — no more pages available, or the target page exceeds the pagination range displayed (typically up to 25 pages / 750 items).

## Success Criteria

`result count >= 1` and `item_id non-null rate = 100%` and `price non-null rate >= 80%`

## Known Limitations

- 30 items per page (fixed by the site)
- Maximum ~750 items accessible via pagination (25 pages × 30)
- Seller username and user ID are not available in search cards — only seller location
- Session rate limiting: accessing item detail pages rapidly after heavy search usage may trigger a CAPTCHA slider; mitigate by adding 1–2 second delays between page navigations
- The `sign` token in search API requests is computed client-side; direct API replay without browser context is not supported — always trigger via page navigation

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through keywords serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping). Add 1–2 second delays between page navigations. To increase throughput, open multiple stealth browser sessions and distribute keywords across them
- **Test before batch execution**: After writing a batch script, first test with 1–2 keywords/pages to verify the script runs correctly; only then run the full batch
- **Reduce redundant pre-operations**: Navigate once per keyword, apply all filters at once before extracting, rather than navigating multiple times
- **Error resumption**: Save results keyword-by-keyword and page-by-page during batch processing; on failure, resume from the last saved position

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/xianyu-scraper-goofish-search-list.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
