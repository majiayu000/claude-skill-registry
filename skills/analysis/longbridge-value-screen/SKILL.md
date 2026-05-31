---
name: longbridge-value-screen
description: |
  Value investing screen via Longbridge — scan A-share / HK / US stocks for fundamentally strong but undervalued companies based on PE, PB, dividend yield, ROE, and margin of safety. Suitable for value investing strategy. Triggers: "低估值", "价值投资", "低PE", "低PB", "便宜股票", "安全边际", "高股息低估值", "被低估", "低估值", "價值投資", "低PE", "低PB", "便宜股票", "安全邊際", "高股息低估值", "value investing", "undervalued stocks", "low PE", "low PB", "margin of safety", "value screen", "cheap stocks", "bargain stocks".
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

# longbridge-value-screen

Prompt-only analysis skill. Screens an index constituent universe for stocks meeting value criteria (low PE/PB, high ROE, reasonable dividend yield), ranks candidates by composite value score, and presents a shortlist with rationale.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"帮我筛选低估值好股"* / *"篩選低估值好股"* / *"screen for undervalued stocks"*
- *"价值投资选股"* / *"價值投資選股"* / *"value investing stock screen"*
- *"A股中有哪些低PE低PB的好公司"* / *"A股低PE低PB好公司"* / *"low PE low PB A-shares"*
- *"港股被低估的股票"* / *"港股被低估的股票"* / *"undervalued HK stocks"*
- *"安全边际高的公司"* / *"安全邊際高的公司"* / *"stocks with high margin of safety"*

## Workflow

1. **Identify universe**: ask user for market (A-share / HK / US) and an index as screening pool (e.g. CSI 300, HSI, S&P 500).
2. Fetch constituent list from the chosen index.
3. For each constituent (up to 50 per batch), fetch valuation and financial KPIs concurrently.
4. Apply value filters and score each stock.
5. Present top candidates with supporting data.

## CLI

Run `longbridge <subcommand> --help` to verify exact flags before calling.

```bash
# Step 1: get constituent list (JSON key is "stocks", not "list")
longbridge constituent <INDEX> --format json
# Examples: 000300.SH (CSI300), HSI.HK, SPX.US, IXIC.US

# Step 2: for each constituent symbol (run concurrently, batch of ≤20 at a time)
longbridge calc-index <SYMBOL> --format json       # PE, PB, ROE, dividend yield, market cap
longbridge valuation <SYMBOL> --format json        # current snapshot + historical percentile
longbridge dividend <SYMBOL> --format json         # dividend history and yield
```

## Value Screening Criteria

Apply the following filters (user can adjust thresholds):

| Criterion | Default threshold | Rationale |
|---|---|---|
| PE (TTM) | < 20 (A/HK); < 25 (US) | Below market average |
| PB | < 2.0 | Below book value or modest premium |
| ROE | > 10% | Profitability quality gate |
| Dividend yield | > 2% (optional) | Shareholder return signal |
| PE historical percentile | < 50th pct (if available) | Below own history |
| Gross margin | > 20% (if available) | Business quality filter |

**Composite value score** = equal-weight rank across (PE rank asc, PB rank asc, ROE rank desc, dividend yield rank desc). Higher score = better value candidate.

**Cyclical-industry caveat**: for energy, steel, banks, shipping — low PE near a cycle peak may not signal undervaluation. Flag these and suggest using PB or dividend yield as primary metric.

## Output template

```
Value Screen — <INDEX> (<N> stocks screened)  Source: Longbridge Securities
Date: <today>  Filters: PE<20, PB<2, ROE>10%

Rank  Symbol      Name         PE    PB    ROE    Div.Yield  Score   Note
1     <SYM>       <Name>       <N>   <N>   <N>%   <N>%       <N>/10
2     ...
...
(top 10 candidates)

[Interpretation]
- Top pick: <symbol> — <brief rationale>
- Key risk: <e.g. sector concentration, cyclical exposure>

⚠️ 筛选结果仅供参考，不构成投资建议。/ 篩選結果僅供參考，不構成投資建議。/ Screening results are for reference only. Not investment advice.
```

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 回退到 MCP；若也不可用，请安装 longbridge-terminal | 回退到 MCP；若也不可用，請安裝 longbridge-terminal | Fall back to MCP; if unavailable, install longbridge-terminal. |
| No index specified | 请告知要筛选的指数，如沪深300、恒生指数、标普500 | 請告知要篩選的指數，如滬深300、恒生指數、標普500 | Please specify an index, e.g. CSI 300, HSI, or S&P 500. |
| constituent returns empty | 未能获取成分股列表，请检查指数代码 | 未能獲取成分股列表，請檢查指數代碼 | Cannot fetch constituent list; check index symbol. |
| calc-index missing fields | 跳过该标的，标注数据缺失 | 略過該標的，標注數據缺失 | Skip symbol; note data gap. |

## MCP fallback

If `longbridge` CLI is not installed, use MCP tools:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP setup: `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` (`quote` scope).

## Related skills

- Deep valuation analysis (single stock) → `longbridge-valuation`
- High-dividend screen → `longbridge-dividend-screen`
- Peer comparison → `longbridge-peer-comparison`
- Fundamentals deep-dive → `longbridge-fundamental`

## File layout

```
longbridge-value-screen/
└── SKILL.md          # prompt-only, no scripts/
```
