---
name: taobao-product-detail
description: "Fetch full product detail from a Taobao or Tmall product page by itemId, returning title, price, shop info, images, SKU variants, and product attributes. Use when user asks to get product details from Taobao, scrape a Taobao item page, extract product info by item ID, fetch Tmall product data, 抓取淘宝商品详情, 获取淘宝商品信息, 淘宝商品页面采集, 天猫商品详情, 按商品ID获取信息. Also applies to building product databases, price tracking by itemId, and product comparison research."
---

# Taobao — Product Detail

> itemId → full product detail (title, price, shop, images, SKU variants, attributes)

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Navigate to a Taobao or Tmall product page and extract full product information from the DOM.

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

### DOM: product detail page (data extraction)

Navigate to the product page and extract all fields:

1. `navigate "https://item.taobao.com/item.htm?id={itemId}"`
2. `wait stable`
3. Close any popup if present: look for buttons with text "开心收下", "不了", "关闭" and click to dismiss
4. `eval "$(python scripts/extract-product.py '{itemId}')"`

Output example:
```json
{
  "itemId": "744983869996",
  "itemUrl": "https://detail.tmall.com/item.htm?id=744983869996",
  "isTmall": true,
  "title": "绿联转换插头英标马来西亚新加坡澳洲韩国新西兰Switch插头转换器",
  "price": 17.9,
  "priceFormatted": "￥17.9",
  "originalPrice": null,
  "shopName": "绿联数码旗舰店",
  "shopUrl": "https://shop67095450.taobao.com/category.htm",
  "shopId": "67095450",
  "images": [
    "https://img.alicdn.com/imgextra/i3/713464357/O1CN01fQN7GG1i3YdCfBjzF_!!0-item_pic.jpg"
  ],
  "skuVariants": [
    "磨砂黑|英转中转换器【适用国内电器】适用马来西亚/新加坡等国家",
    "轻巧白|英转中转换器【适用国内电器】适用马来西亚/新加坡等国家"
  ],
  "attributes": {
    "产地": "中国大陆",
    "品牌": "绿联",
    "转换器类型": "英标",
    "型号": "S510"
  },
  "reviewCount": "7000+"
}
```

Notes:
- `isTmall`: true when product is on Tmall (URL contains `tmall.com`)
- `price`: the currently displayed price (may be flash sale, subsidized, or post-coupon price); multiply SKU variants affect the displayed price
- `originalPrice`: the crossed-out original price when a sale is active; null when no sale
- `shopName`: cleaned shop name (shop header link text)
- `images`: deduplicated, `.webp` suffix removed for cleaner URLs; first image is the main listing image
- `skuVariants`: all visible SKU option labels (color, size, etc.)
- `attributes`: key-value pairs from the product specifications section; may include `颜色分类` with all variant names as a combined string
- `reviewCount`: approximate text from page (e.g., "7000+"), not a precise integer

Error handling: if `title` is null, the product page may not have loaded correctly — check if still on the product page (`state` to inspect URL) and retry navigation.

## Pagination

N/A — single product page, no pagination.

## Success Criteria

`title` non-null AND `itemId` matches input

## Known Limitations

- `price` is the currently displayed price for the default/first SKU; to get prices for other SKU variants, click each `skuVariants` option and re-run the price extraction
- Shop name in raw DOM concatenates rating text; the script extracts only the link text but may still include ratings in some layouts
- Images include both product listing images and some thumbnail duplicates; the script deduplicates by URL
- `originalPrice` extraction depends on the `subPrice--` class structure which varies by product type (flash sale vs regular discount)

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through itemIds serially within a single session; add 2–3 second intervals between navigations.
- **Test before batch execution**: After writing a batch script, you must first test with 1–2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly.
- **Reduce redundant pre-operations**: When scraping multiple products, stay in the same session without re-login checks between items.
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/taobao-product-detail.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
