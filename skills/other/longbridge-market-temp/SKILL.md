---
name: longbridge-market-temp
description: |
  Market-level state from Longbridge Securities — market temperature index (0–100, higher = more bullish), trading session times (open/close), and the trading day calendar (with half-days). Triggers: "今天开盘吗", "今天美股开市吗", "几点开盘", "下个交易日", "市场情绪", "牛熊度数", "温度计", "市场温度", "今天開盤嗎", "幾點開盤", "下個交易日", "市場情緒", "溫度計", "is the market open", "trading hours", "next trading day", "market temperature", "market sentiment".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-market-temp

Market-level state: open / close, calendar, sentiment temperature. Symbol-level questions belong in `longbridge-quote`.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## Subcommands

> The `MARKET` argument is **positional** (not a `--market` flag). Run `longbridge <subcommand> --help` to confirm.

| CLI command | Returns |
|---|---|
| `longbridge market-temp <MARKET> --format json` | Today's market temperature (0–100). Add `--history --start --end` for a time series. Default market = `HK`. |
| `longbridge trading session --format json` | Trading sessions for all markets (open / close times). |
| `longbridge trading days <MARKET> [--start --end] --format json` | Trading day calendar with half-days. Default market = `HK`. |

## Market mapping

LLM maps colloquial names to the positional `<MARKET>`:

| User says | `<MARKET>` |
|---|---|
| 美股 / US / Nasdaq / S&P / Dow | `US` |
| 港股 / HK / Hang Seng / 恒生 / 恆生 | `HK` |
| A 股 / 沪 / 深 / 上证 / 深证 / SH / SZ | `CN` (aliases: `SH`, `SZ`) |
| 新加坡 / SG / Straits / 海峡 / 海峽 | `SG` |

`trading session` does not take a market argument; it returns all markets in one call.

## When to use

- *"今天美股开盘了吗"*, *"is HK open?"* — call `trading session`, then reason against current local time and the user's target market.
- *"几点开盘"* → `trading session`
- *"下个交易日"*, *"this week's trading days"* → `trading days <MARKET>`
- *"圣诞节港股开市吗"* → `trading days HK --start <date> --end <date>`
- *"市场情绪"*, *"温度多少"* → `market-temp <MARKET>`
- *"今年港股市场情绪走势"* → `market-temp HK --history --start ... --end ...`

## Workflow

1. Pick the subcommand (table above).
2. Resolve the positional `<MARKET>` if needed.
3. For "is the market open?" — call `trading session`, then reason against the current local time (US = UTC-5/-4 DST, HK / CN / SG = UTC+8) and the user's target market.
4. Call the Longbridge CLI directly (preferred) or fall back to MCP.
5. Translate the `market-temp` value into wording: 0–30 *偏空*, 30–50 *中性偏空*, 50–70 *中性偏多*, 70–100 *偏多* (translate into the user's language).

## CLI

```bash
longbridge market-temp     HK                                          --format json
longbridge trading session                                              --format json
longbridge trading days    US --start 2026-04-28 --end 2026-05-31       --format json
longbridge market-temp     HK --history --start 2026-01-01 --end 2026-04-28 --format json
```

## Output

- `market-temp` (snapshot): single object with the temperature value. With `--history`, an array of historical points.
- `trading session`: array spanning all markets.
- `trading days`: `{trading_days, half_trading_days}` arrays for the selected market.

## Error handling

If `longbridge` is missing, fall back to MCP. Other stderr messages get relayed verbatim to the user.

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP-only extensions are available; discover them from the MCP server's tool list at runtime.

## Related skills

- Single-stock quote / status → `longbridge-quote`
- Earnings calendar / IPO / macro events → use the equivalent MCP tool directly

## File layout

```
longbridge-market-temp/
└── SKILL.md          # prompt-only, no scripts/
```
