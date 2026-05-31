---
name: longbridge-constituent
description: |
  Constituent stocks of an index or ETF via Longbridge Securities — list members of HSI / SPX / DJI / IXIC / CSI300 / a sector ETF, sortable by change, price, turnover, capital inflow, turnover-rate, or market cap. Returns a ranked roster. Triggers: "标普500有哪些", "标普成分股", "恒生成分股", "纳斯达克成分", "道琼斯成分", "沪深300成分", "ETF 持仓", "ETF 成分股", "指数成分", "成分股涨幅榜", "標普500成分", "恒生成分股", "納斯達克成分", "道瓊成分", "滬深300成分", "ETF 持倉", "ETF 成分股", "指數成分", "成分股漲幅榜", "S&P 500 constituents", "Hang Seng constituents", "IXIC components", "Dow components", "CSI 300 members", "ETF holdings", "ETF constituents", "index members", "what's in SPX", "what's in HSI", "HSI.HK", "SPX.US", "IXIC.US", "DJI.US", "000300.SH".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-constituent

List the constituent stocks of an index or ETF, ranked by a chosen indicator.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger when the user wants the **members** of an index or ETF (not the index quote itself):

- *"标普 500 有哪些股票"*, *"S&P 500 constituents"* → `SPX.US`
- *"恒生指数成分股"*, *"Hang Seng constituents"* → `HSI.HK`
- *"纳斯达克 100 涨幅榜"*, *"IXIC components by gain"* → `IXIC.US`
- *"沪深 300 成分股"*, *"CSI 300 members"* → `000300.SH`
- *"QQQ 持仓"*, *"SPY holdings"* → ETF symbol like `QQQ.US`, `SPY.US`

For the index *quote* (level, change, volume), use `longbridge-quote` instead. For 2–5 explicit-symbol comparison, use `longbridge-peer-comparison`.

## Symbol format

`<CODE>.<MARKET>`. Common indices:

| Index | Symbol |
|---|---|
| 恒生指数 / Hang Seng | `HSI.HK` |
| 国企指数 / HSCEI | `HSCEI.HK` |
| 标普 500 / S&P 500 | `SPX.US` |
| 道琼斯 / Dow Jones | `DJI.US` |
| 纳斯达克综合 / Nasdaq | `IXIC.US` |
| 纳指 100 / Nasdaq 100 | `NDX.US` |
| 沪深 300 / CSI 300 | `000300.SH` |
| 上证指数 / SSE Composite | `000001.SH` |

ETFs use their own ticker (e.g. `SPY.US`, `QQQ.US`, `2800.HK`).

## CLI

Run `longbridge --help` to see all available subcommands, then `longbridge <subcommand> --help` before calling.

```bash
longbridge <subcommand> HSI.HK --format json   # run --help for available flags and subcommand names
```

Types of data needed:
- Constituent list for an index or ETF symbol
- Sort/filter options: by change, price, turnover, capital inflow, turnover rate, or market cap (run `--help` for available sort flags)
- Limit on number of members to return (run `--help` for the flag name)

## Workflow

1. Resolve the user's index/ETF name to `<CODE>.<MARKET>` (use the table above; if ambiguous between markets, ask).
2. Pick sort order from intent (run `--help` to confirm flag names):
   - "涨幅榜 / gainers" → sort by change, descending
   - "跌幅榜 / losers" → sort by change, ascending
   - "成交活跃 / most traded" → sort by turnover
   - "主力净流入 / net inflow" → sort by inflow
   - "权重股 / largest weight" → sort by market cap
3. Pick result count: default 50 unless user specifies (e.g. "前 10" → limit 10).
4. Run the CLI command with `--format json`, render the rows in a table.

## Output

JSON array, one row per constituent — fields typically include `symbol`, `name`, `last`, `change_rate`, `volume`, `turnover`, `market_cap`, plus the indicator used for sorting. Render as a 5–8 column table; preserve `symbol` verbatim.

## Error handling

| Situation | LLM response |
|---|---|
| Shell `command not found: longbridge` | Fall back to MCP if configured; otherwise tell the user to install longbridge-terminal. |
| stderr `param_error` / "invalid symbol" | Confirm the index symbol — e.g. `SPX.US` not `S&P500`. |
| Empty array | "No constituents returned — confirm the symbol is an index or ETF, not a single stock." |
| Other stderr | Surface verbatim. |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

If unsure of the exact MCP tool name, run the CLI; the binary is the canonical path.

## Related skills

| User asks | Route to |
|---|---|
| Index level / change / volume | `longbridge-quote` |
| 2–5 explicit-symbol comparison | `longbridge-peer-comparison` |
| Single-stock fundamentals after picking from the list | `longbridge-fundamental` |
| Single-stock valuation snapshot | `longbridge-valuation` |

## File layout

```
longbridge-constituent/
└── SKILL.md          # prompt-only, no scripts/
```
