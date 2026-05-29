---
name: longbridge-ipo
description: |
  IPO full-lifecycle management via Longbridge Securities — HK/US IPO calendar, subscription/pending/listed rosters, individual IPO details and timelines, account IPO orders, and P&L analysis. Calendar and stock lists require no login; account order and P&L queries require Trade permission. Triggers: "新股", "IPO", "打新", "新股申购", "新股日历", "IPO日历", "待上市", "认购", "新股盈亏", "上市首日", "打新收益", "新股申購", "新股日曆", "IPO日曆", "認購", "新股盈虧", "new IPO", "IPO calendar", "subscribe IPO", "new listing", "IPO orders", "IPO profit loss", "new stock listing", "upcoming IPO", "grey market".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: account_read
  requires_login: false
  default_install: true
  requires_mcp: false
  tier: read
---

# longbridge-ipo

IPO full-lifecycle hub: browse upcoming and recent IPOs in HK and US markets, view individual IPO details, and query your own IPO orders and profit/loss.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"近期港股新股"*, *"港股認購中"*, *"HK IPO subscriptions"* → `longbridge ipo subscriptions`
- *"待上市新股"*, *"等待上市"*, *"pending listings HK"* → `longbridge ipo wait-listing`
- *"最近上市的港股"*, *"近期上市"*, *"recently listed HK"* → `longbridge ipo listed`
- *"美股认购"*, *"US IPO subscriptions"* → `longbridge ipo us-subscriptions`
- *"美股新上市"*, *"US recent IPOs"* → `longbridge ipo us-listed`
- *"IPO 日历"*, *"新股日程"*, *"IPO calendar"* → `longbridge ipo calendar`
- *"XXXX.HK 打新详情"*, *"IPO detail"* → `longbridge ipo detail <SYMBOL>`
- *"我的打新订单"*, *"我的新股申購記錄"*, *"my IPO orders"* → `longbridge ipo orders` (requires login + Trade)
- *"我打新赚了多少"*, *"IPO 盈亏"*, *"IPO profit/loss"* → `longbridge ipo profit-loss` (requires login + Trade)

For general earnings/dividend calendars, defer to `longbridge-calendar`. For account orders on secondary-market stocks, defer to `longbridge-orders`.

## Workflow

**Public data (no login required):**
1. Identify the market (HK / US) and the type of list requested.
2. Call the appropriate subcommand with `--format json`.
3. Render a table sorted by listing date or subscription close date.

**Account data (login + Trade permission required):**
1. Confirm the user is asking about their own orders or P&L.
2. Check login state — if not logged in, prompt `longbridge auth login` with Trade scope.
3. Call `longbridge ipo orders` or `longbridge ipo profit-loss`.
4. Summarise: total subscribed amount, filled lots, return%, P&L in home currency.

## CLI

> Run `longbridge ipo --help` before constructing calls — it is the canonical source for flags and subcommands.

```bash
# Public — no login required
longbridge ipo calendar --format json           # Full IPO calendar (all markets)
longbridge ipo subscriptions --format json      # HK IPOs currently open for subscription
longbridge ipo wait-listing --format json       # HK IPOs pending listing
longbridge ipo listed --format json             # HK recently listed IPOs
longbridge ipo us-subscriptions --format json   # US IPOs currently open for subscription
longbridge ipo us-listed --format json          # US recently listed IPOs
longbridge ipo detail <SYMBOL> --format json    # Individual IPO details + timeline

# Account — requires login with Trade permission
longbridge ipo orders --format json             # My IPO subscription orders
longbridge ipo profit-loss --format json        # My IPO P&L analysis

# Always check flags first
longbridge ipo --help
```

## Output

**IPO list / calendar** — table: symbol / company name / market / price range / subscription open–close / listing date / lot size / status.

**IPO detail** — structured timeline: announcement → subscription window → allotment → listing date → first-day open/close (if listed). Include: price range, lot size, fundraising size, industry, underwriters.

**My orders** — table: symbol / company / applied lots / filled lots / applied amount / status / listing date.

**P&L analysis** — table: symbol / company / filled lots / cost / listing price / current price / return% / P&L amount. Include a summary row for total P&L.

Cite **Longbridge Securities** as the data source and note the data timestamp.

## Error handling

| 情形 | 简体回复 | 繁體回覆 / English reply |
|---|---|---|
| `command not found: longbridge` | 请安装 longbridge-terminal | 請安裝 longbridge-terminal / Install longbridge-terminal |
| `not logged in` / 账户功能未登录 | 账户功能需要 Trade 权限，请运行 `longbridge auth login` | 請執行 `longbridge auth login` / Run with Trade permission |
| `detail` 找不到新股 | 找不到该新股，请确认股票代码格式 | 找不到該新股 / IPO detail not found — verify symbol |
| 结果为空 | 当前无符合条件的新股 | 目前無符合條件的新股 / No IPOs match the filter |
| 其他 stderr | 原样返回错误，不静默重试 | 原樣返回 / Surface verbatim, never retry |

## MCP fallback

When the CLI binary is missing, fall back via the equivalent MCP tool:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

If a tool name does not resolve, ask the user to install the CLI.

## Related skills

| Skill | Why |
|-------|-----|
| `longbridge-calendar` | General earnings / dividend / IPO / macro calendar (lighter IPO view). |
| `longbridge-orders` | Secondary-market order history and fills. |
| `longbridge-fundamental` | Post-listing fundamentals once the company has reported. |
| `longbridge-quote` | Real-time quote for a newly listed stock on its first day. |

## File layout

```
longbridge-ipo/
└── SKILL.md          # prompt-only, no scripts/
```
