---
name: longbridge-dividend-screen
description: |
  High-dividend stock screen via Longbridge — analyse high-dividend-yield strategies for A-shares / HK / US, filter for sustainable payout (reasonable payout ratio, free-cash-flow coverage), stable dividend history, and evaluate long-term total return potential. Triggers: "高分红", "股息率", "红利股", "高股息", "分红稳定", "现金分红", "股息策略", "红利策略", "高分紅", "股息率", "紅利股", "高股息", "分紅穩定", "現金分紅", "high dividend", "dividend yield", "dividend stock", "income stock", "dividend strategy", "payout ratio", "free cash flow coverage", "dividend growth", "dividend stability".
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

# longbridge-dividend-screen

Prompt-only analysis skill. Screens an index universe for high-dividend stocks with sustainable payouts, stable dividend history, and free-cash-flow coverage. Evaluates total return potential (price appreciation + dividend income) for income-oriented investors.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"帮我筛选高分红股票"* / *"篩選高分紅股票"* / *"screen for high-dividend stocks"*
- *"A股红利股有哪些"* / *"A股紅利股"* / *"high-dividend A-shares"*
- *"港股高股息标的"* / *"港股高股息標的"* / *"HK high-dividend stocks"*
- *"股息率高且分红稳定的公司"* / *"股息率高且分紅穩定的公司"* / *"high yield with stable dividends"*
- *"红利策略选股"* / *"紅利策略選股"* / *"dividend strategy stock picking"*

## Workflow

1. **Identify universe**: confirm market (A-share / HK / US) and index pool (CSI 300 / CSI Dividend / HSI / Hang Seng High Dividend / S&P 500 / S&P Dividend Aristocrats).
2. Fetch constituent list from the chosen index.
3. For each constituent (≤20 per batch), fetch dividend data and financial KPIs concurrently.
4. Apply dividend quality filters and score each stock.
5. Present ranked shortlist with sustainability analysis.

## CLI

Run `longbridge <subcommand> --help` to verify exact flags before calling.

```bash
# Step 1: constituent list (JSON key is "stocks")
longbridge constituent <INDEX> --format json
# Examples: 000300.SH (CSI300), HSI.HK, SPX.US

# Step 2: per constituent (run concurrently, batch ≤20)
longbridge dividend <SYMBOL> --format json             # dividend history, yield, DPS
longbridge calc-index <SYMBOL> --format json           # PE, PB, ROE, dps_rate, market cap
longbridge financial-report <SYMBOL> --kind CF --format json   # cash flow statement (FCF)
```

## Dividend Quality Filters

Apply the following filters (user can adjust thresholds):

| Criterion | Default threshold | Rationale |
|---|---|---|
| Dividend yield | > 3% | Meaningful income above risk-free rate |
| Payout ratio | < 80% | Leaves room for reinvestment and dividend safety |
| Free cash flow per share | > DPS | FCF covers the dividend |
| Dividend consistency | Paid dividend in ≥ 3 of last 5 years | Stability signal |
| Dividend growth (3yr CAGR) | > 0% (i.e. not declining) | Quality signal |
| ROE | > 8% | Minimum profitability quality gate |

**Dividend sustainability score** = composite rank across (yield rank desc, FCF-coverage rank desc, consistency rank desc, payout-ratio rank asc, dividend-growth rank desc).

**Sector notes**:
- Banks and REITs typically have higher payout ratios by design — adjust payout threshold to < 90% for these sectors.
- Cyclical sectors (energy, commodities): dividend yield may be high near cycle peak; check trend vs. last 3 years.

## Output template

```
High-Dividend Screen — <INDEX> (<N> stocks screened)  Source: Longbridge Securities
Date: <today>  Filters: yield>3%, payout<80%, FCF>DPS

Rank  Symbol    Name      Yield   Payout  FCF/DPS  3yr Div CAGR  Consistency  Score
1     <SYM>     <Name>    <N>%    <N>%    <N>x     +<N>%         5/5 yrs      <N>/10
2     ...
...
(top 10 candidates)

[Dividend Sustainability Highlights]
- Most stable (dividend consistency): <symbol> — paid uninterrupted for N years, FCF cover Nx
- Highest dividend growth: <symbol> — 3yr DPS CAGR +N%
- Risk flag: <symbol> — high yield but payout ratio >80%, monitor FCF

[Total Return Estimate (illustrative, based on historical data)]
Assuming dividend reinvestment + 5% annual price appreciation:
- <symbol>: illustrative 5yr total return ~N% (div. yield N% + price N%)

⚠️ 筛选结果仅反映股息相关量化指标的符合程度，不代表对上述标的的投资建议。高股息不等于低风险，请结合个人情况独立判断。以上内容仅供参考，不构成投资建议。投资决策请结合自身风险承受能力独立判断。/ 篩選結果僅反映股息相關量化指標的符合程度，不代表對上述標的的投資建議。高股息不等於低風險，請結合個人情況獨立判斷。/ Screening results only reflect dividend-related quantitative criteria and do not represent investment recommendations for the listed securities. High dividend yield does not equal low risk. The above is for reference only and does not constitute investment advice. Please make investment decisions independently based on your own risk tolerance. Dividends are not guaranteed.
```

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 回退到 MCP；若也不可用，请安装 longbridge-terminal | 回退到 MCP；若也不可用，請安裝 longbridge-terminal | Fall back to MCP; if unavailable, install longbridge-terminal. |
| No index specified | 请告知要筛选的市场/指数，如沪深300、红利指数、恒生高息 | 請告知要篩選的市場/指數，如滬深300、紅利指數、恒生高息 | Please specify a market or index, e.g. CSI 300, HSI, or S&P 500. |
| constituent returns empty | 未能获取成分股列表，请检查指数代码 | 未能獲取成分股列表，請檢查指數代碼 | Cannot fetch constituent list; check index symbol. |
| dividend data unavailable | 跳过该标的，标注无分红历史数据 | 略過該標的，標注無分紅歷史數據 | Skip symbol; no dividend history data. |
| CF report unavailable | 使用 DPS/EPS 代替 FCF/DPS 作为覆盖率近似 | 使用 DPS/EPS 代替 FCF/DPS 作為覆蓋率近似 | Use DPS/EPS as proxy for FCF coverage. |

## MCP fallback

If `longbridge` CLI is not installed, use MCP tools:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP setup: `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` (`quote` scope).

## Related skills

- Value investing screen (PE/PB/ROE) → `longbridge-value-screen`
- Deep valuation analysis (single stock) → `longbridge-valuation`
- Dividend history for a single stock → `longbridge-fundamental`
- Peer comparison → `longbridge-peer-comparison`

## File layout

```
longbridge-dividend-screen/
└── SKILL.md          # prompt-only, no scripts/
```
