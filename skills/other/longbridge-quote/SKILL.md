---
name: longbridge-quote
description: |
  Real-time quotes, static reference, and valuation indices for stocks listed in HK / US / A-share / Singapore via Longbridge Securities. Returns last price, change, volume, turnover, market cap, industry, PE/PB, turnover-rate, and other indicators. Triggers: "现在多少钱", "股价", "涨跌幅", "成交量", "市值", "市盈率", "PE", "PB", "换手率", "行业", "現在多少", "股價", "成交量", "市值", "市盈率", "stock price", "current price", "quote", "market cap", "PE ratio", "valuation", "NVDA price", "AAPL quote", "茅台市值", "腾讯股价", "700.HK", "600519.SH".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-quote

Real-time quote, static info, and valuation indices for Longbridge-supported securities (HK / US / A-share / Singapore).

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger on prompts asking about:

- Current price / change / volume — *"NVDA 现在多少钱"*, *"現在股價"*, *"What's NVDA's price?"*
- Industry / market cap / floats / EPS / BPS — *"贵州茅台市值多少"*, *"茅台屬於什麼行業"*, *"AAPL EPS"*
- Valuation indices (PE, PB, turnover rate, 5/10-day change, etc.) — *"NVDA 的 PE"*, *"700 換手率"*, *"AAPL volume ratio"*
- Trading status of a single security — *"AAPL still trading?"*, *"美股开盘了吗"*

For 2–5 symbol comparison defer to `longbridge-peer-comparison`. For historical valuation percentile, defer to `longbridge-valuation`.

## Symbol format

`<CODE>.<MARKET>`. Normalise before calling:

| Pattern | Market | Example |
|---|---|---|
| Uppercase ticker (US) | `.US` | `NVDA.US`, `AAPL.US` |
| 4-digit numeric | `.HK` | `700.HK`, `9988.HK` |
| 6-digit, starts `60` | `.SH` | `600519.SH` |
| 6-digit, starts `00`/`30` | `.SZ` | `300750.SZ` |
| Singapore ticker | `.SG` | `D05.SG` |
| Chinese / English company name | use knowledge | 腾讯 → `700.HK`, 特斯拉 → `TSLA.US`, 贵州茅台 → `600519.SH` |

If the market is ambiguous, **ask the user** rather than guessing.

## Subcommands

Run `longbridge --help` to see all available subcommands, then `longbridge <subcommand> --help` before calling. Types of data needed:

- Real-time quote data (last price, open, high, low, prev close, volume, turnover, trade status)
- Static reference data (name, industry, lot size, total/circulating shares, EPS, BPS, dividend yield, currency)
- Valuation indices (PE, PB, turnover rate, total market cap, change rates, etc.)

> **Always run `longbridge <subcommand> --help` first** — every Longbridge CLI subcommand self-documents its arguments, defaults, and examples. Do not hard-code flag names from this SKILL.md if the CLI version may have evolved.

## Workflow

1. Extract symbol(s) from the prompt; normalise each to `<CODE>.<MARKET>`.
2. Run `longbridge --help` to identify available subcommands, then `longbridge <subcommand> --help` to confirm flags.
3. Decide which subset of data is needed:
   - **Quote only** (price / change / volume) → real-time quote subcommand
   - **Static** (industry, market cap, EPS, BPS, dividend yield) → static reference subcommand
   - **Indices** (PE, PB, turnover rate, etc.) → valuation index subcommand (check `--help` for supported field names)
   - **Combined** ("full snapshot") → all three
3. Run them (parallel is fine when supported by the agent runtime). Each command returns a JSON array keyed by symbol.
4. Merge the per-symbol rows by `symbol` into a single object per security.
5. Translate to natural language; cite the source as **Longbridge Securities** / **数据来源:长桥证券** / **數據來源:長橋證券**.

## CLI examples

```bash
# Always check available flags first:
longbridge <subcommand> --help

# Then call with --format json — example structure (verify subcommand names and flags with --help):
longbridge <quote-subcommand>      NVDA.US --format json
longbridge <quote-subcommand>      NVDA.US 700.HK 600519.SH --format json   # multi-symbol
longbridge <static-subcommand>     600519.SH --format json
longbridge <calc-index-subcommand> NVDA.US --format json   # valuation indices; use --help for index field names
```

Run `longbridge <calc-index-subcommand> --help` to see all supported index field names. A reference cheat-sheet (with multilingual labels) lives in [references/calc-index-fields.md](references/calc-index-fields.md).

## Output

Each subcommand returns a JSON array, one object per requested symbol. Missing per-symbol values appear as `"-"` or `null` (not an error). When merging, key by `symbol` and emit a structure like:

```json
{
  "symbol": "NVDA.US",
  "quote":      { "last": "...", "prev_close": "...", "volume": "...", ... },
  "static":     { "industry": "...", "eps": "...", "bps": "...", ... },
  "calc_index": { "pe_ttm": "...", "pb": "...", "total_market_value": "...", ... }
}
```

## Error handling

| Situation | LLM response |
|---|---|
| Shell `command not found: longbridge` | Fall back to MCP if configured (see below); otherwise tell the user to install [longbridge-terminal](https://github.com/longportapp/longbridge-terminal). |
| stderr contains `not logged in` / `unauthorized` | Tell the user to run `longbridge auth login`. |
| stderr contains `param_error` or "invalid symbol" | Re-check the `<CODE>.<MARKET>` format with the user. |
| Other stderr | Surface verbatim — never silently retry. |

## MCP fallback

If the CLI binary is unavailable and the user has run `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp`, fall back to:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP is slower (HTTP + OAuth) but does not depend on a local binary.

## Related skills

| User asks | Route to |
|---|---|
| Candlestick / intraday chart | `longbridge-kline` |
| Orderbook depth / brokers / ticks | `longbridge-depth` |
| Capital flow / large-order distribution | `longbridge-capital-flow` |
| 2–5 symbol comparison | `longbridge-peer-comparison` |
| Historical PE / PB percentile | `longbridge-valuation` |
| Earnings / fundamentals | `longbridge-fundamental` |
| Recent news / filings | `longbridge-news` |

## File layout

```
longbridge-quote/
├── SKILL.md
└── references/
    └── calc-index-fields.md
```

Prompt-only — no `scripts/`. Discover the latest CLI flags via `longbridge <subcommand> --help`.
