---
name: goofish-item-detail
description: "Extracts full detail data from a single Goofish (闲鱼/xianyu, goofish.com) second-hand item page. Input: item URL or item ID. Output: title, price, seller info (name, labels), full description, image gallery, item tags/attributes, want-count. Use when user mentions goofish item detail, 闲鱼商品详情, xianyu item page, 二手商品详情, get goofish product info, 采集闲鱼单品数据, 抓取闲鱼商品, scrape goofish item, xianyu product detail, 获取闲鱼卖家信息, seller info goofish, item description goofish, 闲鱼详情页, 想要人数, 闲鱼图片. Also applies to: verifying a specific listing before purchase, extracting seller contact/rating information, bulk item detail enrichment from a list of item IDs."
---

# Goofish (闲鱼) — Item Detail

> item URL (or item_id + category_id) → full listing data: title, price, seller info, description, images, tags, want-count

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Load a single Goofish item detail page and extract its complete listing data including seller information, item description, image gallery, and attribute tags.

## Prerequisites

- Browser with an active Goofish session (login required — item detail pages require authenticated access)
- Target item URL format: `https://www.goofish.com/item?id={item_id}&categoryId={category_id}`

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

If login status for Goofish has been confirmed in the current session → skip this step.

Otherwise: open `https://www.goofish.com/` and observe the page:
- User avatar or account entry exists → logged in, continue
- Login/register prompt → not logged in; inform user that login is required; assist login flow

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed on the page. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; use the bash tool for execution.

### Network Capture: load item detail page

The item detail API (`mtop.taobao.idle.pc.detail/1.0/`) auto-fires when navigating to the item URL. Provide parameters via URL:

1. `navigate https://www.goofish.com/item?id={item_id}&categoryId={category_id}`
2. `wait stable`
3. Proceed to DOM extraction below

Error handling:
- If a CAPTCHA slider appears ("Please slide to verify"): the session is rate-limited. Wait 5–10 minutes, or use remote-assist to complete the slider manually, then re-navigate.
- If "网络不见了" error page appears: the item page API call failed. Retry once after 30 seconds; if it persists, the session may be temporarily blocked.
- If item shows "该宝贝已下架" or similar: item has been removed/sold — skip and move to next item.

Note: Navigating to item detail pages in rapid succession (e.g., less than 2 seconds apart) increases the probability of CAPTCHA. Add 2–5 second delays between items in batch mode.

### DOM: extract item detail data

After navigating and waiting stable, extract all available fields:

`eval "$(python scripts/extract-item-detail.py)"`

Output example:
```json
{
  "item_id": "1054899470781",
  "item_url": "https://www.goofish.com/item?id=1054899470781&categoryId=126862528",
  "title": "出一台iPhone 15 128G，电池健康度高，成色九新以上...",
  "price": "898.00",
  "original_price": "899.00",
  "seller_name": "小王数码严选",
  "seller_avatar": "https://img.alicdn.com/bao/uploaded/...",
  "seller_labels": ["成都", "刚刚擦亮", "来闲鱼5年", "卖出204件宝贝", "好评率100%"],
  "description": "出一台iPhone 15 128G，电池健康度高，成色九新以上...",
  "images": [
    "https://img.alicdn.com/bao/uploaded/i4/...",
    "https://img.alicdn.com/bao/uploaded/i2/..."
  ],
  "tags": ["品牌：Apple/苹果", "型号：iPhone 15", "存储容量：128GB", "运行内存：6GB", "成色：几乎全新"],
  "want_count": "8人想要"
}
```

Fields that may be null: `original_price`, `seller_labels`, `description`, `tags`, `want_count` (depending on listing completeness). Note: on Goofish detail pages, `title` and `description` contain the same text — there is no separate title element.

## Pagination

N/A — single item page, no pagination.

## Success Criteria

`item_id non-null` and `title non-null` and `price non-null`

## Known Limitations

- Seller user ID (numeric) is not exposed in the DOM — only seller display name is available
- Item detail pages trigger CAPTCHA if accessed too rapidly; recommended minimum interval: 3 seconds between items
- Some items may require login even for viewing; the Skill will return an error if the page fails to load
- Rapid successive navigation may trigger "网络不见了" error — wait 30 seconds before retrying

## Execution Efficiency

- **Batch orchestration**: Loop through item IDs serially with 3–5 second delays; do not parallelize within one browser. To increase throughput, distribute items across multiple browser sessions
- **Test before batch execution**: Test with 2–3 items first to confirm selectors are valid; only then run the full batch
- **Error resumption**: Save results item-by-item; on failure (CAPTCHA or error), record the failed item ID and resume after the CAPTCHA clears
- **Get item IDs from search**: Use `goofish-search-list` Skill to collect item IDs, then feed them into this Skill for detail enrichment

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/xianyu-scraper-goofish-item-detail.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file.
