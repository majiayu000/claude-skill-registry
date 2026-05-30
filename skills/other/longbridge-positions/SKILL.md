---
name: longbridge-positions
description: |
  Account holdings — stock positions, fund positions, multi-currency assets / cash, margin ratio (initial / maintenance / forced liquidation), and estimated max buy/sell quantity for a symbol. Requires longbridge login. Triggers: "我的持仓", "我有什么股票", "账户余额", "我有多少美金", "基金持仓", "我能买多少股", "保证金率", "杠杆要求", "账户全貌", "我的持倉", "賬戶餘額", "我有多少美金", "基金持倉", "保證金率", "賬戶全貌", "my holdings", "stock positions", "account balance", "how much can I buy", "margin ratio", "max buy qty", "portfolio snapshot".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: account_read
  requires_login: true
  default_install: true
---

# longbridge-positions

Read-only account snapshot — what the user holds, how much cash, what they can buy/sell, and per-symbol margin ratios.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.
>
> **Privacy**: the data here is the user's private account state. Only return detailed numbers in direct conversation; if you suspect screen-sharing or third-party observation, confirm before showing exact figures.

## Subcommands

> Run `longbridge <subcommand> --help` to confirm current flags / defaults if anything below seems off.

| CLI command | Returns |
|---|---|
| `longbridge portfolio --format json` | Combined view: total assets, P/L, intraday P/L, holdings, and cash breakdown. Single call — useful for "account snapshot" questions. |
| `longbridge positions --format json` | Stock holdings array. |
| `longbridge fund-positions --format json` | Fund holdings array. |
| `longbridge assets [--currency USD\|HKD\|CNY\|SGD] --format json` | Net assets, cash, buy power, margins; per-currency breakdown in `cash_infos`. |
| `longbridge margin-ratio <SYMBOL> --format json` | Initial / maintenance / forced-liquidation factors for a symbol. |
| `longbridge max-qty <SYMBOL> --side buy\|sell [--price <p>] [--order-type LO\|MO\|ELO\|ALO] --format json` | Estimated max purchasable / sellable quantity (cash vs margin). |

## When to use

- *"我的持仓"*, *"我有什么股票"*, *"我的持倉"* → `positions`
- *"账户余额"*, *"我有多少美金 / 港币"*, *"current USD balance"* → `assets --currency USD`
- *"我的基金持仓"* → `fund-positions`
- *"NVDA 我能买多少股"*, *"how many TSLA can I buy"* → `max-qty <SYMBOL> --side buy --price <current>` (limit) or `--order-type MO` (market)
- *"茅台保证金率"* → `margin-ratio 600519.SH`
- *"看一下我的账户全貌"*, *"account snapshot"* → `portfolio` (one call gives total assets + P/L + holdings + cash)
- *"我的浮盈"* → `portfolio` already includes intraday P/L; otherwise `positions` + chain to `longbridge-quote` for live last price

## max-qty workflow

1. **Limit order (default LO)**: first call `longbridge quote <SYMBOL> --format json` for the current last price → pass it as `--price`.
2. **Market order**: skip price; pass `--order-type MO`.
3. The response includes `cash_max_qty` (cash only) and `margin_max_qty` (with financing). Always disclose both numbers and remind the user that financing carries interest cost + forced-liquidation risk.

## CLI

```bash
longbridge portfolio                                                  --format json
longbridge positions                                                  --format json
longbridge fund-positions                                             --format json
longbridge assets --currency USD                                      --format json
longbridge margin-ratio TSLA.US                                       --format json
longbridge max-qty TSLA.US --side buy --price 250                     --format json
```

## Output

- `portfolio`: combined object with total assets, P/L, intraday P/L, holdings list, cash breakdown.
- `positions` / `fund-positions`: array of holding rows.
- `assets`: per-currency `cash_infos` array plus net-assets / buy-power / margin fields.
- `margin-ratio`: `{im_factor, mm_factor, fm_factor}`.
- `max-qty`: `{cash_max_qty, margin_max_qty}`.

## OAuth scope

Requires the trade scope on the OAuth token. If the token lacks it, both CLI and MCP fail with `unauthorized` / `not in authorized scope`. Tell the user to re-authorise: `longbridge auth logout && longbridge auth login` (and tick "Trade" in the browser).

## Error handling

If `longbridge` is missing, fall back to MCP. If stderr contains `unauthorized` / `not in authorized scope`, the OAuth token lacks trade scope — guide the user through re-auth (see "OAuth scope" above). Other stderr messages relay verbatim.

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP-only extensions are available; discover them from the MCP server's tool list at runtime.

## Related skills

- Orders / executions / cash flow → `longbridge-orders`
- Watchlist (read) → `longbridge-watchlist`
- Account-level P&L analysis → `longbridge-portfolio`

## File layout

```
longbridge-positions/
└── SKILL.md          # prompt-only, no scripts/
```
