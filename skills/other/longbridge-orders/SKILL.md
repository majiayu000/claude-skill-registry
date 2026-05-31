---
name: longbridge-orders
description: |
  Read-only account orders, executions, and cash flow — today's or historical orders (filterable by symbol / date), single-order detail with status history, today/historical fills, and cash flow (deposits, withdrawals, dividends, settlements). Requires longbridge login. Read-only — no order placement here. Triggers: "今天我下了哪些单", "我的订单", "历史成交", "上个月成交", "出入金", "分红记录", "资金流水", "結算記錄", "我的訂單", "歷史成交", "上個月", "出入金記錄", "分紅", "資金流水", "today's orders", "order history", "executions", "fills", "cash flow", "deposits and withdrawals", "dividend record", "settlement".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: account_read
  requires_login: true
  default_install: true
---

# longbridge-orders

Read-only orders / executions / cash flow. The `order` parent command also has buy / sell / cancel / replace sub-subcommands — **this skill does not place trades**; those belong to a future trading skill that is designed but intentionally not shipped in this release.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.
>
> **Privacy**: orders, fills, and cash-flow data are private account state. Only return details in direct conversation.

## Subcommands

> `order` is a parent command with several sub-subcommands. Run `longbridge order --help` to see the full list and current flags.

| CLI command | Returns |
|---|---|
| `longbridge order --format json` | Today's orders (default mode). |
| `longbridge order --history --start --end [--symbol] --format json` | Historical orders, filtered. |
| `longbridge order detail <ORDER_ID> --format json` | Full single-order detail (status history, fees). |
| `longbridge order executions --format json` | Today's fills (default). |
| `longbridge order executions --history --start --end [--symbol] --format json` | Historical fills. |
| `longbridge cash-flow [--start --end] --format json` | Deposits / withdrawals / dividends / settlements. |

## Time-window inference

LLM converts natural-language windows to `--start` / `--end` (ISO `YYYY-MM-DD`):

| User says | Window |
|---|---|
| 今天 / today | no `--start --end` |
| 上个月 / last month | first → last day of previous month |
| 近 30 天 / past 30 days | `today-30` → `today` |
| 4 月 5 日 / April 5 | `--start = --end = 2026-04-05` |

Use today's date from the system context.

## When to use

- *"今天我下了哪些单"* → `order` (default, no `--history`)
- *"上个月所有成交"* → `order executions --history --start --end`
- *"TSLA 历史订单"* → `order --history --symbol TSLA.US --start ... --end ...`
- *"订单 20240101-123456789 详情"* → `order detail <ORDER_ID>`
- *"近 30 天出入金"*, *"上次分红"* → `cash-flow --start --end`

## CLI

```bash
longbridge order                                                                       --format json
longbridge order --history --start 2025-01-01 --end 2025-04-01 --symbol TSLA.US        --format json
longbridge order detail 20240101-123456789                                             --format json
longbridge order executions                                                            --format json
longbridge order executions --history --start 2025-01-01 --end 2025-04-01              --format json
longbridge cash-flow --start 2025-04-01 --end 2025-04-30                               --format json
```

## Output

- `order` / `order executions`: array of order / fill rows.
- `order detail`: full single-order object (status history, fees). Empty result → "order not found".
- `cash-flow`: array of cash-flow events.

Status translation (LLM should map):

| Raw | 简体 | 繁體 | English |
|---|---|---|---|
| `Filled` | 已成交 | 已成交 | Filled |
| `PartialFilled` | 部分成交 | 部分成交 | Partially filled |
| `Canceled` | 已撤单 | 已撤單 | Cancelled |
| `New` | 待成交 | 待成交 | Working |
| `Rejected` | 被拒 | 被拒 | Rejected |

## OAuth scope

Same as `longbridge-positions`: needs trade scope. Lacking it → both CLI and MCP return `unauthorized`. Tell the user to `longbridge auth logout && longbridge auth login` and tick "Trade".

## Error handling

If `longbridge` is missing, fall back to MCP. Long history ranges may take a while — surface progress to the user. Other stderr messages relay verbatim.

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP-only extensions are available; discover them from the MCP server's tool list at runtime.

## Related skills

- Holdings + assets → `longbridge-positions`
- Account-level P&L analysis → `longbridge-portfolio`

## File layout

```
longbridge-orders/
└── SKILL.md          # prompt-only, no scripts/
```
