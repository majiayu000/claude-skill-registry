---
name: taobao-product-reviews
description: "Fetch customer reviews for a Taobao or Tmall product by itemId, returning reviewer name, date, purchased variant, review text, and photo URLs. Use when user asks to get product reviews from Taobao, scrape Taobao customer feedback, extract buyer reviews by item ID, collect Tmall ratings and comments, 采集淘宝商品评价, 抓取淘宝买家评论, 获取淘宝商品评论, 天猫商品评价抓取, 按商品ID获取评价. Also applies to sentiment analysis of product reviews, building review datasets, and monitoring product rating changes."
---

# Taobao — Product Reviews

> itemId → paginated customer reviews (reviewer, date, purchased SKU, text, photos)

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Navigate to a Taobao/Tmall product page, load the reviews section, and extract customer review content.

## Prerequisites

- Target page is already open in the browser: `https://item.taobao.com/item.htm?id={itemId}`
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

### DOM: product reviews (data extraction)

The reviews section is lazy-loaded below the main product area. Follow these steps to load and extract reviews:

1. `navigate "https://item.taobao.com/item.htm?id={itemId}"`
2. `wait stable`
3. Close any popup: look for buttons with text "开心收下", "不了", "关闭" and click to dismiss
4. Scroll to trigger lazy loading of the tabs/reviews section:
   `scroll down --amount 8000`
5. `wait --selector "[class*='tabTitleItem--']" --state attached --timeout 10000`
   - If timeout: `scroll down --amount 8000` again and retry wait once more
   - If still no tabs after 2 attempts: take `screenshot` to confirm page state; the product page may be rendering in a condensed mode — check Known Limitations below
6. `eval "$(python scripts/extract-reviews.py '{itemId}')"`

Output example:
```json
[
  {
    "username": "一笑奈何",
    "date": "2026-06-03",
    "purchasedSku": "轻巧白|英转中转换器【适用国内电器】适用马来西亚/新加坡等国家",
    "content": "商品非常好，造工很用心！，还会再回购！",
    "photos": [
      "https://gw.alicdn.com/bao/uploaded/i1/O1CN015Cyg4b2FPR2YNq3PD_!!4611686018427383816-0-rate.jpg"
    ],
    "rating": null
  }
]
```

Notes:
- `purchasedSku`: the specific variant the reviewer purchased (extracted from "已购：{sku}" prefix in review header)
- `content`: review text body; may be empty if reviewer submitted only photos
- `photos`: review photo URLs; empty array if no photos
- `rating`: star rating; not always visible in current page layout (null is common)
- Reviews shown are the default sort (most recent or most helpful as determined by Taobao)

Error handling: if result count = 0 after scroll attempts, the reviews section may not have loaded in the current browser rendering environment. Try navigating to the product page fresh (`navigate` again) and repeating the scroll sequence. If still failing, this is a known rendering limitation — see Known Limitations below.

### DOM: paginate to next review page

After extracting current page reviews:

1. `eval "$(python scripts/next-review-page.py)"`
   - Returns `{"hasNext": true, "buttonText": "下一页"}` if next page exists, or `{"hasNext": false}` if on last page
2. If `hasNext` is true: `state` to find the "下一页" button index → `click <index>`
3. `wait stable`
4. Re-run `eval "$(python scripts/extract-reviews.py '{itemId}')"`

## Enum Parameters

[collection failed] Sort/filter options for reviews (e.g., newest, most helpful): these controls exist in the reviews section UI but require the tabs section to be loaded; their URL parameters are not exposed and must be set via UI clicks on the sort tabs within the reviews section.

## Pagination

**DOM Pagination**: Click the "下一页" button in the reviews section footer. Each page shows ~10 reviews. Termination: "下一页" button is absent or `hasNext` returns false.

## Success Criteria

`result count >= 1` and `username` non-null rate = 100%

## Known Limitations

- **Tab section lazy-loading**: The reviews section (along with all tabs: specs, images, recommendations) is lazy-loaded and requires scrolling past the main product area to appear. In some browser sessions or rendering environments, the tabs section does not load even after multiple scroll attempts. This is an intermittent behavior of the Taobao product page rendering engine and does not indicate a site change. Workaround: close and reopen the browser session, then navigate fresh.
- Requires Taobao login; unauthenticated sessions redirect to login page
- Review content is only visible on the product page; there is no standalone reviews URL for Taobao/Tmall products
- Only shows positive buyer reviews by default; negative reviews may require clicking a filter tab within the reviews section (if visible)

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through itemIds serially within a single session; add 3–5 second intervals to allow the lazy-loaded reviews section to render.
- **Test before batch execution**: After writing a batch script, you must first test with 1–2 items to verify the reviews section loads correctly; only then run the full batch. Never skip testing and execute in batch directly.
- **Reduce redundant pre-operations**: When collecting multiple pages of reviews for one product, stay on the same page and paginate via button click rather than re-navigating.
- **Error resumption**: Save results page by page; on failure, resume from the last successful page.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/taobao-product-reviews.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
