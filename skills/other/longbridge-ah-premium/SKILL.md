---
name: longbridge-ah-premium
description: |
  A/H premium ratio for Mainland-Chinese companies dual-listed in Hong Kong and A-shares (e.g. 939.HK / 601398.SH, 1810.HK / 600519.SH-pair) via Longbridge Securities — historical premium time series (kline) or today's intraday premium curve. Only HK-side symbols of dual-listed pairs return data. Triggers: "AH 溢价", "A H 溢价率", "AH 折价", "AH 价差", "工行 AH", "建行 AH", "比价", "A 股贵还是港股贵", "AH premium", "A/H premium", "AH ratio", "AH 溢價", "A H 溢價率", "AH 折價", "AH 價差", "比價", "A 股貴還是港股貴", "dual listed premium", "Hong Kong A-share premium", "premium ratio", "939.HK", "1398.HK", "600519.SH 对应港股".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-ah-premium

A/H premium ratio for dual-listed Mainland-Chinese companies — historical kline or today's intraday curve.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger when the user asks about the **price gap** between an HK listing and its A-share twin:

- *"工行 A/H 溢价"*, *"工行 AH 比价"* → `1398.HK`
- *"建行 AH 折价"* → `939.HK`
- *"中国平安港股比 A 股贵多少"* → `2318.HK`
- *"AH premium for ICBC over the last year"* → `1398.HK --kline-type day --count 250`
- *"今天 939 的 AH 溢价走势"* → `intraday 939.HK`

For single-symbol quote, use `longbridge-quote`. For comparison of unrelated tickers, use `longbridge-peer-comparison`.

## Symbol format

Always pass the **HK side** (`<CODE>.HK`) of the dual-listed pair. The Longbridge API maps internally to the A-share counterpart. Common pairs:

| Company | HK | A-share |
|---|---|---|
| 工商银行 / ICBC | `1398.HK` | `601398.SH` |
| 建设银行 / CCB | `939.HK` | `601939.SH` |
| 中国平安 / Ping An | `2318.HK` | `601318.SH` |
| 招商银行 / CMB | `3968.HK` | `600036.SH` |
| 中国人寿 / China Life | `2628.HK` | `601628.SH` |

If the user gives an A-share symbol, translate to the HK side. If the stock is not dual-listed (e.g. `700.HK`), the API returns no data — report that, don't retry.

## Subcommands

> Run `longbridge ah-premium --help` (and `longbridge ah-premium intraday --help`) if unsure of current flags.

| CLI command | Returns |
|---|---|
| `longbridge ah-premium <SYMBOL> [--kline-type T] [--count N] --format json` | Historical premium ratio kline |
| `longbridge ah-premium intraday <SYMBOL> --format json` | Today's intraday premium time series |

`--kline-type`: `1m` / `5m` / `15m` / `30m` / `60m` / `day` (default) / `week` / `month` / `year`. `--count` defaults to 100.

## Workflow

1. Identify the dual-listed pair; pass the **HK** symbol.
2. Decide mode:
   - "近一年 / last year走势" → kline `--kline-type day --count 250`
   - "近一月 / past month" → kline `--kline-type day --count 22`
   - "今天 / 当日 / intraday" → `intraday` subcommand
3. Run the command, render the time series (table or summary: latest premium %, range, trend).
4. Cite source as **Longbridge Securities** / **数据来源:长桥证券** / **數據來源:長橋證券**.

## CLI examples

```bash
# Default daily kline (100 days)
longbridge ah-premium 939.HK                                       --format json

# Last year of daily premium
longbridge ah-premium 1398.HK --kline-type day --count 250         --format json

# Last 12 weeks
longbridge ah-premium 2318.HK --kline-type week --count 12         --format json

# Today's intraday premium curve
longbridge ah-premium intraday 939.HK                              --format json
```

## Output

Each row carries a timestamp and a premium ratio (typically expressed as `(H_price * fx) / A_price - 1`, in %). Negative = HK trades at a discount to A-share. Surface latest value + recent range.

## Error handling

| Situation | LLM response |
|---|---|
| Shell `command not found: longbridge` | Fall back to MCP if configured; otherwise tell the user to install longbridge-terminal. |
| Empty array | "No A/H premium data — `<SYMBOL>` is likely not dual-listed in A-shares." |
| stderr `param_error` | Verify the symbol is an HK ticker of a dual-listed pair. |
| Other stderr | Surface verbatim. |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

## Related skills

| User asks | Route to |
|---|---|
| Single-symbol price / change | `longbridge-quote` |
| HK or A-share candlestick history | `longbridge-kline` |
| Cross-symbol comparison (>2 tickers) | `longbridge-peer-comparison` |
| Why the premium changed (news / catalysts) | `longbridge-news` |

## File layout

```
longbridge-ah-premium/
└── SKILL.md          # prompt-only, no scripts/
```
