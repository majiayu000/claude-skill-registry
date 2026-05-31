---
name: longbridge-valuation
description: |
  Valuation analysis for a single stock via Longbridge — current PE / PB / PS / EV-EBITDA snapshot, historical percentile (1–3 years), industry median + relative premium, industry rank. Triggers: "估值贵不贵", "是不是被低估", "PE 历史百分位", "PB 分位", "行业溢价", "行业折价", "X 现在适合买不", "估值水平", "估值貴不貴", "是否被低估", "PE 歷史分位", "行業溢價", "行業折價", "is X expensive", "is X undervalued", "PE percentile", "industry valuation premium", "valuation snapshot".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
  requires_mcp: false
  tier: analysis
---

# longbridge-valuation

Prompt-only analysis skill. Orchestrates Longbridge CLI commands to answer *"is X expensive?"* across three dimensions: current snapshot, historical percentile, industry context.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"NVDA 估值贵不贵"*, *"is NVDA expensive?"*, *"NVDA 估值貴不貴"*
- *"茅台是不是被低估了"*, *"is Maotai undervalued?"*
- *"700 估值在历史什么位置"*, *"700 historical PE percentile"*
- *"宁德时代相对行业贵多少"*, *"how much does CATL trade above industry median"*
- *"GOOG 现在适合买入吗"*

For multi-symbol comparison route to `longbridge-peer-comparison`. For business-fundamentals questions route to `longbridge-fundamental`.

## CLI

Run `longbridge --help` to see all available subcommands, then `longbridge <subcommand> --help` before calling. Types of data needed (run concurrently):

- Current valuation snapshot + peer comparison
- Historical valuation series (PE, PB — run `--help` for available indicators and range flags)
- Daily industry percentile rank for PE / PB / PS (run `--help` for date range flags)
- Industry median + distribution
- Industry percentile distribution
- Optional intraday valuation correction (for live mid-day prices — run `--help` for the relevant subcommand)

```bash
longbridge <subcommand> TSLA.US --format json   # run --help for available flags and subcommand names
```

## Workflow

1. **Resolve symbol** to `<CODE>.<MARKET>` (rules in `longbridge-quote`). Multiple symbols → route to `longbridge-peer-comparison`.
2. **Concurrently call** CLI commands above. If `longbridge` is not installed, fall back to MCP (see MCP fallback section).
3.

   Optional intraday correction (only when needed): run `longbridge --help` to find the subcommand for live intraday valuation — note that the standard valuation subcommand is often EOD only.

4. **Compute** in the LLM:

   | Quantity | Method |
   |---|---|
   | Historical PE percentile | prefer the daily valuation-rank series from CLI; fallback: rank current PE against historical valuation series |
   | Historical PB percentile | same |
   | Industry premium | `(current PE − industry median PE) / industry median PE` |
   | Industry rank | bucket from industry valuation distribution data |

   If history is sparse (< 1y) or the industry has fewer than 5 peers, **degrade gracefully** — show snapshot + relative-to-industry only, drop the percentile claim.

5. **Output the three sections** (template below). Cite **Longbridge Securities**.

## Output template

```
{Symbol} ({code}) valuation snapshot — Source: Longbridge Securities

[Current snapshot]
- PE (TTM): X
- PB:        X
- PS:        X
- EV/EBITDA: X (if available)
- Dividend yield: X%

[Historical (past 3y)]
- PE in N-th percentile (low / mid / high)
- PB in N-th percentile

[Industry (N peers)]
- Industry median PE: X → currently {premium/discount} of N%
- Industry rank: {position} / N (high / mid / low bucket)

[Combined]
From historical + industry views, valuation is {low / neutral / high} — historical N-th pct, {N% above/below} industry median.

⚠️ 以上数据仅供参考，不构成投资建议。/ 以上數據僅供參考，不構成投資建議。/ For reference only. Not investment advice.
```

(Translate into the user's language; keep numeric values as-is.)

## Cyclical industries — special handling

Energy / chemicals / steel / shipping / banks / property are cyclical: PE inverts (high PE near troughs because earnings are depressed; low PE near peaks may signal a top). When the symbol is in such an industry, **add the caveat**: *"Cyclical industry — PE percentile must be interpreted alongside industry cycle position; do not read 'high PE = expensive' mechanically."*

## Output constraints

- **Must** include three dimensions (snapshot + historical + industry); state "data unavailable" if a dimension fails.
- **Must** cite "Longbridge Securities" / "数据来源:长桥证券" / "數據來源:長橋證券".
- **Must** end with the not-investment-advice disclaimer.
- **May** characterise combinations like "high-historical + high-industry" and give a view; qualify with data.

## Error handling

| Situation | Reply |
|---|---|
| `command not found: longbridge` | Fall back to MCP; if MCP also unavailable, tell user to install longbridge-terminal. |
| stderr `not logged in` | Tell user to run `longbridge auth login`. |
| Valuation data returns empty | "{symbol} has no valuation data (likely an obscure or newly listed name)." |
| history < 1 year | Degrade to snapshot + industry-only |
| Industry < 5 peers | Caveat: "industry sample sparse; industry percentile is indicative only" |

## MCP fallback

If `longbridge` CLI is not installed (`command not found`), use MCP tools instead:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP setup: `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` (`quote` scope).

## Related skills

- 2–5 symbol valuation comparison → `longbridge-peer-comparison`
- Business fundamentals (revenue, ROE, margins) → `longbridge-fundamental`
- News / market reaction → `longbridge-news`
- Real-time price alert → `longbridge-alert`

## File layout

```
longbridge-valuation/
└── SKILL.md          # prompt-only, no scripts/
```
