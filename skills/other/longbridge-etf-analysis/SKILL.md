---
name: longbridge-etf-analysis
description: |
  ETF analysis framework via Longbridge — product screening (AUM/expense ratio/index), tracking error, liquidity (bid-ask spread/volume), premium/discount (NAV vs market price), and A-share ETF allocation insights. Triggers: "ETF分析", "ETF选择", "ETF跟踪误差", "ETF溢价", "ETF流动性", "ETF费率", "ETF规模", "宽基ETF", "行业ETF", "指数基金", "ETF分析", "ETF選擇", "ETF追蹤誤差", "ETF溢價", "ETF流動性", "ETF費率", "ETF規模", "指數基金", "ETF analysis", "ETF selection", "tracking error", "ETF premium discount", "ETF liquidity", "expense ratio", "broad market ETF", "sector ETF", "index fund".
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

# longbridge-etf-analysis

Prompt-only analysis skill. Analyses ETFs across five dimensions: product profile, tracking error, liquidity, premium/discount, and allocation fit — supporting both US-listed ETFs and A-share ETFs.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"QQQ 和 QQQM 哪个更适合长期持有？"* / *"QQQ vs QQQM for long-term holding?"*
- *"这只 ETF 的跟踪误差大不大？"* / *"Is the tracking error on this ETF high?"*
- *"510300 现在溢价还是折价？"* / *"Is 510300 trading at a premium or discount?"*
- *"帮我分析沪深300 ETF 的流动性"* / *"Analyse the liquidity of CSI 300 ETFs"*
- *"行业 ETF 怎么选？"* / *"How to pick a sector ETF?"*

For index constituent stocks route to `longbridge-constituent`. For individual stock valuation route to `longbridge-valuation`.

## CLI

Run `longbridge <subcommand> --help` to verify exact flags.

```bash
# ETF quote — price, volume, market cap, turnover
longbridge quote <ETF_SYMBOL> --format json

# Constituent holdings — underlying stocks and weights
longbridge constituent <ETF_SYMBOL> --format json

# Historical price — compute tracking error vs index
longbridge kline <ETF_SYMBOL> --period day --count 60 --format json

# Index / benchmark price for comparison
longbridge kline <BENCHMARK_SYMBOL> --period day --count 60 --format json

# Valuation indices (PE/PB of ETF if available)
longbridge calc-index <ETF_SYMBOL> --format json
```

## Five-dimension analysis

### 1. Product profile
Extract from `quote` + `constituent` output:
- Underlying index tracked
- AUM / total market cap (proxy)
- Expense ratio (if available in quote metadata; otherwise note "check fund prospectus")
- Inception date / listing exchange

### 2. Tracking error
- Fetch ETF daily kline and benchmark daily kline (60 bars).
- Daily return difference: `d_i = r_ETF_i − r_index_i`
- Tracking error (annualised): `TE = std(d) × √252`
- Interpretation: TE < 0.3% excellent; 0.3–1% acceptable; > 1% investigate.

### 3. Liquidity
From `quote`:
- Average daily volume and turnover
- Bid-ask spread (if tick data available; otherwise use turnover-rate as proxy)
- Liquidity flag: turnover-rate > 0.5% = liquid; < 0.1% = illiquid (A-share ETFs)

### 4. Premium / discount (NAV vs market price)
- For A-share ETFs: `premium = (market price − NAV) / NAV × 100%`
- NAV may not be in real-time quote; note this and use EOD NAV if available.
- Persistent premium > 2% or discount < −2% signals arbitrage opportunity or liquidity issue.
- For US ETFs: premium/discount is typically < 0.1% due to continuous creation/redemption.

### 5. Allocation fit
- Index type: broad market (SPY/QQQ/510300) vs sector (XLK/515790) vs factor (value/growth/momentum)
- Currency and market exposure
- Overlap analysis: if user holds multiple ETFs, flag significant holdings overlap from `constituent`

## Workflow

1. Resolve ETF symbol to `<CODE>.<MARKET>` (e.g. `SPY.US`, `510300.SH`).
2. Concurrently fetch: `quote`, `constituent`, ETF kline, benchmark kline.
3. Compute TE, assess liquidity, estimate premium/discount.
4. Summarise all five dimensions.
5. Output structured report (template below). Cite Longbridge Securities.

## Output template

```
{ETF Symbol} analysis — Source: Longbridge Securities

[1. Product profile]
- Index tracked: {name}  |  Exchange: {ex}
- AUM proxy (mkt cap): {$X}  |  Expense ratio: {X% / see prospectus}

[2. Tracking error (60-day)]
- Annualised TE: X%  → {excellent / acceptable / elevated}

[3. Liquidity]
- Avg daily volume: {X}  |  Turnover rate: X%  → {liquid / moderate / illiquid}
- Bid-ask spread estimate: {X% / data unavailable}

[4. Premium / Discount]
- Latest: {+X% premium / −X% discount / ~flat}
- Note: {A-share ETF — NAV published after close / US ETF — near-zero typical}

[5. Allocation fit]
- Type: {broad market / sector / factor}
- Key holdings (top 5): {list from constituent}
- Currency exposure: {USD / CNY / HKD}

[Summary]
{2–3 sentence overall assessment}

⚠️ 以上分析仅供参考，不构成投资建议。/ 以上分析僅供參考，不構成投資建議。/ For reference only. Not investment advice.
```

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 切换到 MCP；若不可用，请安装 longbridge-terminal | 切換至 MCP；若不可用，請安裝 longbridge-terminal | Fall back to MCP; if unavailable, install longbridge-terminal |
| stderr `not logged in` | 请执行 `longbridge auth login` | 請執行 `longbridge auth login` | Run `longbridge auth login` |
| `constituent` returns empty | 持仓数据暂不可用，跳过重叠分析 | 持倉數據暫不可用，跳過重疊分析 | Constituent data unavailable; skipping overlap analysis |
| Benchmark kline unavailable | 无法计算跟踪误差，仅显示 ETF 本身收益 | 無法計算追蹤誤差，僅顯示 ETF 本身收益 | Cannot compute TE; showing ETF return only |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

## Related skills

- Constituent stock list → `longbridge-constituent`
- Individual stock valuation → `longbridge-valuation`
- Capital flow into ETF holdings → `longbridge-capital-flow`
- Market / index temperature → `longbridge-market-temp`

## File layout

```
longbridge-etf-analysis/
└── SKILL.md          # prompt-only, no scripts/
```
