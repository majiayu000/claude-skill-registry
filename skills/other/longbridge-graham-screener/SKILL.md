---
name: longbridge-graham-screener
description: |
  Graham cigar-butt batch screener — runs Benjamin Graham's NCAV / net-net / defensive-investor hard filters across an index or market universe and returns a ranked candidate list with NCAV ratio, PE, PB, dividend yield, debt coverage, 5y earnings stability, Graham buy price, and a dynamic value-trap warning. Longbridge CLI first; MCP fallback if CLI unavailable; WebSearch fills genuine gaps (PMI, sector outlook). Every figure footnoted to its source. Auto-switches model for banks / insurance / REITs and flags <2y IPOs and suspended names. Triggers: "格雷厄姆筛选", "格雷厄姆选股", "捡烟蒂榜单", "烟蒂股榜", "NCAV筛选", "NCAV排行榜", "净流动资产筛选", "防御型投资者选股", "撿煙蒂榜單", "煙蒂股榜", "NCAV篩選", "淨流動資產篩選", "防禦型投資者選股", "Graham screen", "Graham screener", "NCAV screen", "net-net screen", "net-net list", "cigar-butt screen", "defensive investor screen", "liquidation value screen", "Benjamin Graham screen".
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

# longbridge-graham-screener

Prompt-only batch screener. Given a market or index universe, applies Graham's six hard filters (NCAV, PE, PB, dividend yield, debt coverage, earnings stability), scores each name on a 100-point static + dynamic composite, and returns a ranked list of stocks meeting Graham's quantitative criteria, with Graham buy lines, holding-period expectation, and value-trap warnings.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"港股里现在有没有 NCAV<1 的股票"* / *"港股裡現在有沒有 NCAV<1 的股票"* / *"any HK stocks with NCAV < 1"*
- *"给我 A 股 PE 最低的 20 只股票，格雷厄姆标准"* / *"給我 A 股 PE 最低的 20 隻股票，格雷厄姆標準"* / *"top 20 lowest-PE A-shares by Graham standard"*
- *"帮我筛一下符合格雷厄姆防御型投资者条件的美股"* / *"幫我篩一下符合格雷厄姆防禦型投資者條件的美股"* / *"screen US stocks meeting Graham defensive-investor rules"*
- *"沪深300里的烟蒂股"* / *"滬深300裡的煙蒂股"* / *"cigar-butt names in CSI 300"*
- *"每周更新港股 NCAV 排行榜"* / *"每週更新港股 NCAV 排行榜"* / *"weekly HK NCAV leaderboard"*

For single-stock deep diagnostic use `longbridge-graham-stock-analysis`. For broader low-PE / low-PB / high-ROE value (not NCAV-centric) use `longbridge-value-screen`. For high-dividend-only screens use `longbridge-dividend-screen`.

## Cognitive frame (do not skip)

Graham screening is **patient arbitrage**, not a dip-buy signal. Hold periods: 6–18 months (explicit catalyst), 1–3 years (sector re-rating), 3–5 years (organic accrual), or never (value trap — exit). Every ranking output **must** carry the waiting-cost (dividend yield) and the holding-period framing; never display a score number on its own.

Two failure modes the user must be able to distinguish — and the screener must signal:
- **"Cheap but time hasn't come"** → NCAV stable QoQ, keep on the list.
- **"Value trap"** → NCAV shrinking ≥3 quarters, persistent insider selling, negative OCF, PMI persistently <50, AR growth outpacing revenue. Override to ⚠️ regardless of static score.

## Workflow

1. **Confirm market + universe**. Ask the user for: (a) market — HK / US / A-share, (b) screening pool — single index (HSI, S&P 500, CSI 300, NDX, etc.) or a watchlist. Default batch ceiling: 300 names per run.
2. **Fetch constituent list** for the chosen index (or watchlist) — see [§CLI](#cli).
3. **Sector pre-classification**: **exclude** banks / insurance / REITs / pure financials / negative-equity / pure-holding shells from the universe before scoring — NCAV does not apply to balance sheets dominated by financial assets, so these are removed, not run through a substitute model. Count the exclusion in the Market Summary "Excluded — NCAV inapplicable" line. Separately, flag IPOs < 2 years (pro-rata earnings-stability sub-score, noted in row) and suspended names (last-trade snapshot, prepend ⏸).
4. **Batch-fetch fundamentals in parallel** (≤20 symbols per wave): balance sheet (annual + last 4Q), income statement (5y annual + 4Q quarterly), cash flow (4Q quarterly), `calc-index` + `quote` snapshot, `dividend`, `ownership`.
5. **Apply hard filters** with user-overridable thresholds — see [§Filters](#filters).
6. **Score each candidate** — static (0–100) + dynamic adjustments + value-trap override. See `references/criteria.md`.
7. **Reconciliation gate per row**: if balance-sheet sum / current-assets sum / shares×price mismatches the reported total by >3%, drop the row from the leaderboard with a "data anomaly" note (do not silently average).
8. **Rank by adjusted score** (descending); default top 10–20 returned. Emit the table + market summary + waiting-cost note + suggested next step.
9. **Append a Data Source Appendix** (mandatory) listing every Longbridge endpoint hit, every WebSearch hit (publisher + URL + access date), fetch timestamps, and any field substitutions.
10. **End every output** with: «筛选结果仅反映量化指标的符合程度，不代表对上述标的的投资建议。投资决策请结合个人情况独立判断。/ Screening results only reflect quantitative criteria compliance and do not constitute investment advice. 本筛选器仅静态硬指标 + 通用动态因子，未考虑公司层面主观估值陷阱。命中标的请用 `longbridge-graham-stock-analysis` 做单股深度诊断。»

## CLI

Run `longbridge <subcommand> --help` to verify exact flags before each call — the CLI is the source of truth, do not hard-code flag spellings from memory.

```bash
# Universe
longbridge constituent <INDEX>   --format json     # e.g. 000300.SH, HSI.HK, SPX.US

# Per-symbol snapshot (run in parallel, batches of ≤20)
longbridge calc-index   <SYMBOL> --format json     # PE / PB / market cap / ROE / dividend yield
longbridge quote        <SYMBOL> --format json     # current price + suspended flag
longbridge dividend     <SYMBOL> --format json     # TTM dividend (waiting-cost)

# Per-symbol fundamentals (run in parallel)
longbridge financial-report    <SYMBOL> --kind BS --report af --format json   # 5y annual BS → NCAV
longbridge financial-statement <SYMBOL> --kind BS --report qf --format json   # last 4Q BS → NCAV trajectory
longbridge financial-report    <SYMBOL> --kind IS --report af --format json   # 5y annual IS → earnings stability
longbridge financial-report    <SYMBOL> --kind CF --report qf --format json   # 4Q CF → OCF rule

# Insider / institutional flow (value-trap rule 2)
longbridge ownership    <SYMBOL> --format json
longbridge insresearch  <SYMBOL> --format json
```

### WebSearch fallback (use only when Longbridge has the gap)

| Missing input | WebSearch query pattern |
|---|---|
| Industry PMI / inventory cycle | `"<industry> PMI <year>"`, `"中国制造业 PMI <month>"`, `"<industry> inventory cycle <year>"` |
| Capacity utilisation | `"<industry> capacity utilization <year>"` |
| Sector outlook (qualitative) | `"<sector> outlook <year> site:reuters.com OR site:bloomberg.com OR site:wsj.com"` |
| Recent insider transactions (if `ownership` is stale) | `"<ticker> insider selling <year>"`, `"<公司> 大股东减持 <month>"` |

Each WebSearch-sourced figure must be tagged with publisher + URL + access date in the **Data Source Appendix**; never silently mix it into a Longbridge column.

## Filters

User-overridable. Defaults from Graham's *Intelligent Investor* with light modernisation; threshold detail and the composite scoring weights live in `references/criteria.md`.

| Filter | Graham threshold | Notes |
|---|---|---|
| NCAV ratio (market cap ÷ haircut NCAV) | < 1.0 ideal, < 1.5 acceptable | Core. Haircut: cash 100% / AR 75% / inventory 50% / other CA 25% / liabilities 100% |
| PE (TTM) | < 10 (defensive) | Rolling TTM |
| PB | < 1.5 | — |
| Dividend yield (TTM) | > 3% | Waiting-cost compensation |
| Current assets ÷ total liabilities | > 2.0 | Debt safety |
| Consecutive no-loss years | ≥ 5 | Earnings stability |
| Dynamic warning state | none triggered | Optional pre-filter; defaults to "show but flag" |

Default rank key = adjusted cigar-butt score (static composite + dynamic adjustments + value-trap override). The user can override the rank key to: static-only, NCAV ratio asc, PE asc, dividend yield desc.

## Special handling

| Cohort | Treatment |
|---|---|
| Banks / insurance / REITs / pure financials / negative-equity / pure-holding shells | **Excluded** — NCAV is not a valid valuation lens for these business models. No substitute model is run; the symbols are dropped from the universe before scoring and counted in the Market Summary "Excluded — NCAV inapplicable" line. If the user wants these analysed, point them to `longbridge-valuation-methodology` or `longbridge-valuation`. |
| IPOs listed < 2 years | Earnings-stability sub-score pro-rated on available years. Mark row "数据局限". |
| Suspended stocks | Show last-trade snapshot, prepend "⏸ 停牌" / "⏸ Suspended" to the name, exclude from default top-N (still listable on request). |
| Reconciliation fail >3% | Drop from leaderboard; surface in a "数据异常待复核" footer list with the failing check named. |

## Output

Default leaderboard (top 10–20 rows). Full template, market-summary block, waiting-cost line, subscription hook, and the mandatory **Data Source Appendix** structure live in `references/output.md`.

Minimum columns:

```
排名  代码  名称  静态评分  调整后评分  NCAV比率  PE  PB  股息率  Graham买入价  动态预警  数据局限
```

After the table, every output must include:
1. **Market summary** — universe size, hard-filter pass count, dynamic-clean count.
2. **Waiting-cost line** — average dividend yield of the top-N; the «持有等待期间每年可获约 X% 股息回报作为补偿» line.
3. **Next-step recommendation** — point users to `longbridge-graham-stock-analysis` for any name they want to research further (筛选器未考虑主观估值陷阱因素).
4. **Data Source Appendix** — mandatory; every field, every Longbridge endpoint, every WebSearch hit (publisher + URL + date).
5. **Disclaimer** — full trilingual disclaimer from `references/output.md`, including: 「筛选结果仅反映量化指标的符合程度，不代表对上述标的的投资建议。投资决策请结合个人情况独立判断。/ Screening results only reflect quantitative criteria compliance and do not constitute investment advice.」

> ⚠️ 以上内容仅供参考，不构成投资建议。投资决策请结合自身风险承受能力独立判断。/ 以上內容僅供參考，不構成投資建議。投資決策請結合自身風險承受能力獨立判斷。/ For reference only. Not investment advice. Please make investment decisions independently based on your own risk tolerance.

## Error handling

| Situation | 简体回复 | 繁體回覆 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 回退到 MCP；若不可用，请安装 longbridge-terminal。 | 回退到 MCP；若不可用，請安裝 longbridge-terminal。 | Fall back to MCP; if unavailable install longbridge-terminal. |
| stderr `not logged in` / `unauthorized` | 请运行 `longbridge auth login`。 | 請執行 `longbridge auth login`。 | Run `longbridge auth login`. |
| `constituent` returns empty | 未能获取成分股，请确认指数代码（如 000300.SH / HSI.HK / SPX.US）。 | 未能獲取成分股，請確認指數代碼（如 000300.SH / HSI.HK / SPX.US）。 | Cannot fetch constituents; verify index symbol (e.g. 000300.SH / HSI.HK / SPX.US). |
| BS / IS / CF partial fetch for a symbol | 该标的数据不完整，跳过并在「数据异常」脚注列出。 | 該標的數據不完整，跳過並於「數據異常」腳註列出。 | Symbol has incomplete fundamentals; skipped and listed in the data-anomaly footer. |
| Industry-cycle data missing (Longbridge + WebSearch both empty) | 仅展示静态评分，动态层标注「数据不足」。 | 僅展示靜態評分，動態層標註「數據不足」。 | Static score only; dynamic layer marked "unavailable". |
| Per-row reconciliation gap >3% | 从榜单剔除并在「数据异常」附录列出失败项及差异。 | 自榜單剔除並於「數據異常」附錄列出失敗項及差異。 | Drop from leaderboard; list failing check + gap in data-anomaly appendix. |

## MCP fallback

If `longbridge` CLI is not installed, use MCP tools:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP setup: `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` (`quote` scope).

## Related skills

- Single-stock Graham diagnostic → `longbridge-graham-stock-analysis`
- Broader value (PE / PB / ROE) screen → `longbridge-value-screen`
- High-dividend screen → `longbridge-dividend-screen`
- DCF intrinsic value → `longbridge-dcf`
- Method selection guide → `longbridge-valuation-methodology`
- Three-statement reading → `longbridge-financial-report`

## File layout

```
longbridge-graham-screener/
├── SKILL.md
└── references/
    ├── criteria.md   # filter thresholds, six-dimension static scoring, dynamic adjustments, value-trap override, NCAV-inapplicable exclusions
    └── output.md     # full leaderboard template, market-summary block, data-source appendix, disclaimer
```
