---
name: longbridge-peer-comparison
description: |
  Cross-symbol comparison (2–5 stocks) via Longbridge — valuation (PE / PB / PS / dividend yield), current price + change, latest financial KPIs (revenue / net income / ROE), market cap. Renders as a single matrix; flags cross-currency or cross-industry caveats. Triggers: "X 和 Y 哪个值得买", "X vs Y", "几只股票对比", "同行业谁最强", "X 跟 Y 谁更便宜", "几只哪个增速快", "科技七姐妹谁最强", "X 跟 Y 對比", "X 跟 Y 哪個便宜", "X vs Y", "compare X and Y", "peer comparison", "which is more expensive", "which has higher growth".
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

# longbridge-peer-comparison

Prompt-only skill that takes 2–5 symbols, runs the same per-symbol orchestration concurrently, and renders one normalised matrix.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"茅台 五粮液 哪个便宜"*, *"AAPL vs GOOG vs MSFT"*
- *"NVDA AMD 哪个增速快"*, *"科技七姐妹谁最强"*
- *"茅台跟 700 谁估值低"* (cross-currency + cross-industry — render with explicit disclaimer)

## Symbol-count rules

| Count | Behaviour |
|---|---|
| 0 | Ask: *"Which symbols would you like to compare?"* |
| **1** | Reroute → `longbridge-valuation` (#14) or `longbridge-fundamental` (#15) |
| 2–5 | Run normally |
| ≥ 6 | Ask user to narrow to 3–5 ("matrix becomes unreadable beyond 5") |

## Cross-cohort caveats

- **Cross-currency** (e.g. `NVDA.US` + `600519.SH`) → render the matrix; add an explicit disclaimer at the top of the table: *"cross-currency comparison shows relative levels only; no FX conversion is applied"*.
- **Cross-industry** (e.g. tech + spirits) → render the matrix; add: *"cross-industry comparison has limited meaning — valuation thresholds are not comparable"*.
- **Cross-market** (different accounting standards: IFRS / US GAAP / CN GAAP) → add: *"data uses different accounting standards; treat as a rough benchmark."*

## CLI

Run `longbridge --help` to see all available subcommands, then `longbridge <subcommand> --help` before calling. Types of data needed per symbol (run concurrently for all symbols):

- Real-time quote (last price, change)
- Valuation indices (PE, PB, PS, dividend yield, market cap)
- Financial KPIs from the most recent report (revenue, net income, ROE) — headline figures only, not full statements
- Historical valuation data

```bash
# Always check flags first, then call — example structure:
longbridge <subcommand> NVDA.US --format json
```

## Workflow

1. Resolve every symbol to `<CODE>.<MARKET>`. Apply the count rules above.
2. **Concurrently per symbol**, call CLI commands (see CLI section). If `longbridge` is not installed, fall back to MCP.
3. **Do not** pull the full IS/BS/CF — `financial-report` headline fields are enough for the KPIs.

4. Normalise (label currency on every figure; **do not** auto-convert FX). Render as a Markdown table — rows are dimensions, columns are symbols.
5. Add the **observations** paragraph at the bottom (data-only, no winners).

## Output template

```
{symbol₁ vs symbol₂ vs ...} comparison — Source: Longbridge Securities
[If cross-currency / cross-industry / cross-market: disclaimer here]

| Dimension | Symbol₁ | Symbol₂ | Symbol₃ |
|---|---|---|---|
| Last (CCY) | ... | ... | ... |
| Today's change | ... | ... | ... |
| Market cap | ... | ... | ... |
| **Valuation** | | | |
| PE (TTM) | ... | ... | ... |
| PB | ... | ... | ... |
| PS | ... | ... | ... |
| Dividend yield | ... | ... | ... |
| **Financials (latest period)** | | | |
| Revenue YoY | ... | ... | ... |
| Net income YoY | ... | ... | ... |
| ROE | ... | ... | ... |

[Observations]
- Valuation: who is highest / lowest on PE / PB / PS
- Growth: who leads on revenue / net income YoY
- Dividend: highest yield
- Scale: market-cap ratios

⚠️ 以上数据仅供参考，不构成投资建议。/ 以上數據僅供參考，不構成投資建議。/ For reference only. Not investment advice.
```

(Translate into the user's language; keep numerics + ticker symbols verbatim.)

## Output constraints

- **Must** be a Markdown table, dimensions × symbols.
- **Must** label currency on every numeric figure (CNY / USD / HKD / SGD); no auto-FX conversion.
- **Must** end with not-investment-advice disclaimer.
- Cross-currency / cross-industry / cross-market → **must** include the disclaimer at the top of the table.

## Performance note

2–5 symbols × 4 tools = 8–20 MCP calls. Latency may be visible. If the user gives 5 symbols, optionally tell them *"comparing 5 symbols, fetching in parallel..."* before delivering.

## Error handling

| Situation | Reply |
|---|---|
| `command not found: longbridge` | Fall back to MCP; if MCP also unavailable, tell user to install longbridge-terminal. |
| Some symbols' data missing | Render N/A in those rows; explain which symbol(s) failed |
| 1 symbol only | Reroute to `longbridge-valuation` / `longbridge-fundamental` |
| ≥ 6 symbols | Trim to top 5; tell user the rest are dropped |
| stderr `not logged in` | Tell user to run `longbridge auth login`. |

## MCP fallback

If `longbridge` CLI is not installed (`command not found`), use MCP tools instead (per symbol):

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP setup: `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` (`quote` scope).

## Related skills

- Single-symbol valuation drill-down → `longbridge-valuation`
- Single-symbol fundamentals drill-down → `longbridge-fundamental`
- Recent news on a specific name → `longbridge-news`

## File layout

```
longbridge-peer-comparison/
└── SKILL.md          # prompt-only, no scripts/
```
