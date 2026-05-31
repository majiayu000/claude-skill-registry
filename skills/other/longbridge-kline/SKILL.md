---
name: longbridge-kline
description: |
  Candlestick / OHLCV data and intraday minute series for stocks listed in HK / US / A-share / Singapore via Longbridge Securities. Supports 1m / 5m / 15m / 30m / 1h / day / week / month / year periods, history by date range, and today's intraday curve. Triggers: "K线", "K 线", "走势", "历史价格", "日K", "月K", "周K", "分时图", "近一周走势", "K線", "走勢", "歷史價格", "日K", "月K", "週K", "分時圖", "candlestick", "candles", "OHLCV", "intraday chart", "price history", "weekly chart", "monthly chart", "1-year chart", "前复权", "前復權", "forward adjusted".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-kline

Historical candlesticks and today's intraday curve for Longbridge-supported securities (HK / US / A-share / Singapore). Does **not** support options, warrants, or indices — defer to `longbridge-derivatives` (derivatives) or `longbridge-quote` (indices).

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## Subcommands

> Run `longbridge kline --help` to confirm current period values, defaults, and aliases.

| CLI command | Use when |
|---|---|
| `longbridge kline <SYMBOL> --period <P> --count <N> --format json` | Latest N candles. Periods: `1m / 5m / 15m / 30m / 1h / day / week / month / year`. |
| `longbridge kline history <SYMBOL> --start YYYY-MM-DD --end YYYY-MM-DD --period <P> --format json` | OHLCV across an explicit date range (sub-subcommand). |
| `longbridge intraday <SYMBOL> --format json` | Today's per-minute curve (price + volume + avg_price). |

Period aliases: `minute=1m`, `hour=1h`, `d/1d=day`, `w=week`, `m/1mo=month`, `y=year`. `--adjust none` (default) or `--adjust forward` for 前复权 / 前復權.

## When to use

- *"NVDA 最近一周走势"*, *"近一年走勢"*, *"AAPL 1-month chart"* → `kline --period day`
- *"TSLA 5 分钟 K"*, *"近 100 根 5 分钟"* → `kline --period 5m --count 100`
- *"今天 700.HK 分时图"*, *"AAPL today's intraday"* → `intraday`
- *"AAPL 2024 年 1-12 月日 K"* (explicit dates) → `kline history --start --end`
- *"前复权日 K"* → add `--adjust forward`

## Workflow

1. Resolve the symbol to `<CODE>.<MARKET>` (see `longbridge-quote` for the rules).
2. Pick the form:
   - Explicit start/end dates → `kline history`.
   - "Today" / "intraday" → `intraday`.
   - Otherwise → `kline` with sensible defaults (`--period day --count 100`).
3. Map natural-language windows to (`period`, `count`). Examples: "最近一周" → `day,7`, "最近一年" → `day,252`, "月 K" → `month,100`.
4. Call the Longbridge CLI directly (preferred) or fall back to MCP.
5. Translate datasets into prose (range high / low, net move, volume note); use ▲ / ▼ for direction. Cite **Longbridge Securities** / **数据来源:长桥证券** / **數據來源:長橋證券**.

## CLI

```bash
longbridge kline         NVDA.US --period day --count 100             --format json
longbridge kline         700.HK  --period 5m  --count 100 --adjust forward --format json
longbridge kline history NVDA.US --start 2025-01-01 --end 2025-12-31  --format json
longbridge intraday      700.HK                                       --format json
```

## Output

`longbridge kline ... --format json` returns a list of OHLCV rows:

```json
[
  {"time": "...", "open": "...", "high": "...", "low": "...", "close": "...", "volume": "...", "turnover": "..."}
]
```

`intraday` rows are `{time, price, volume, turnover, avg_price}`.

## Error handling

If `longbridge` is not installed, the shell returns a `command not found` error → fall back to MCP (see below) or tell the user to install longbridge-terminal. If `longbridge` prints `Error: ...` to stderr, surface the message to the user — common causes:

- `Error: not logged in` / `unauthorized` → user runs `longbridge auth login`.
- `Error: invalid symbol` / `param_error` → re-check the `<CODE>.<MARKET>` format.

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

## Related skills

- Quote / static / valuation indices → `longbridge-quote`
- Orderbook / brokers / ticks → `longbridge-depth`
- Capital flow → `longbridge-capital-flow`

## File layout

```
longbridge-kline/
└── SKILL.md          # prompt-only, no scripts/
```
