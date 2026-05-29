---
name: longbridge-ark-analysis
description: |
  ARK-style single-stock disruptive-innovation diagnostic. Suitability gate on 4 dimensions (platform fit / innovation revenue / R&D intensity / management vision); if it passes, builds TAM (low/base/high), Wright's-Law cost curve with sourced learning rate, three-scenario 5-year target (Bull/Base/Bear, 15% discount), risks, conditional action frame. Data: Longbridge CLI first, MCP fallback, WebSearch only for TAM / learning rates / industry runway. Runs cross-statement reconciliation BEFORE analysis. Closes with a data-source appendix whose final row is the reconciliation summary. Independent implementation — not affiliated with ARK Invest. Triggers: "木头姐", "ARK", "ARKK", "颠覆式创新", "莱特定律", "TAM", "5年目标价", "情景分析", "AI 与大数据", "自动化与机器人", "能源存储", "基因革命", "区块链与金融科技", "木頭姐", "顛覆式創新", "萊特定律", "5年目標價", "Cathie Wood", "ARK Invest", "disruptive innovation", "Wright's Law", "learning rate", "bull base bear", "scenario analysis".
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

# longbridge-ark-analysis

Prompt-only ARK-inspired diagnostic for a single ticker. Runs a suitability gate (must be a disruptive-innovation name), then builds TAM, a Wright's-Law cost-curve note, and a three-scenario 5-year target price. Closes with a mandatory data-source appendix whose final row is a one-line reconciliation summary.

> **Response language**: detect the user's input language (Simplified Chinese / Traditional Chinese / English) and render the **entire report — every section heading, label, scenario write-up, narrative, education block, appendix row, reconciliation summary, and disclaimer — in that one language**. Do not mix languages within a single output. The output template in `references/output.md` is shown in English for reference; translate it as a whole into the user's language using the label-translation lookup in that file. The error / source tables inside *this* SKILL.md remain 3-column because they document what the skill says under each language — that 3-column form is for the skill's reference docs, not for the user-facing report.

> **Independence statement (mandatory)**: this skill is an independent implementation inspired by ARK Invest's publicly described methodology. It is **not affiliated with, endorsed by, or representative of ARK Invest or Cathie Wood's actual views or positions**. The independence statement must appear in the disclaimer of every output.

## When to use

- *"用木头姐的方法分析 TSLA"* / *"用木頭姐的方法分析 TSLA"* / *"analyze TSLA with the ARK framework"*
- *"ARK 怎么看 NVDA"* / *"ARK 怎麼看 NVDA"* / *"how does ARK see NVDA"*
- *"PLTR 的颠覆式创新逻辑成立吗"* / *"PLTR 的顛覆式創新邏輯成立嗎"* / *"is PLTR a real disruptive-innovation story"*
- *"帮我算一下 TSLA 5 年的 bull base bear 目标价"* / *"算一下 TSLA 5 年的 bull base bear 目標價"* / *"build a 5-year bull/base/bear target on TSLA"*
- *"AMZN 属于 ARK 的哪个平台"* / *"AMZN 屬於 ARK 的哪個平台"* / *"which ARK platform is AMZN in"*
- *"建行用 ARK 怎么看"* / *"建行用 ARK 怎麼看"* / *"would the ARK framework work on CCB"* (→ reject + recommend alternative)

For Buffett-style moat analysis → `longbridge-buffett-moat-analyzer`. For Graham cigar-butt → `longbridge-graham-stock-analysis`. For pure DCF → `longbridge-dcf`. For peer benchmarking → `longbridge-peer-comparison`.

## Cognitive frame (do not skip)

ARK's reference is **5-year ownership of disruptive-innovation companies**, with three-scenario thinking around a TAM × market-share × margin × multiple terminal value, discounted back. Three things every output must surface:

1. **Suitability is a gate, not a soft preference.** If the company is not in one of ARK's five innovation platforms (**Artificial Intelligence · Robotics & Autonomous Mobility · Energy Storage & EV Adoption · Multiomic Sequencing & AI Drug Discovery · Public Blockchains & Digital Assets** — see `references/scoring.md` §Suitability for the value-chain decomposition into upstream / core / downstream / adjacent tiers, and the convergence themes), **reject** and recommend an alternative method — do not produce a "for reference" ARK report on a bank, oil major, or consumer staple. A company qualifies if its revenue depends materially on **any tier** of a platform (upstream / core / downstream / adjacent) — not only on being the platform's headline name.
2. **5-year predictions are wide ranges, not point estimates.** TAM and market share are deeply uncertain. The output always shows three scenarios (Bull / Base / Bear) with explicit assumptions; never collapse them to a single confident number, and never present the weighted target price as a forecast — call it a model-derived expectation.
3. **Many disruptors have short history — analyse them anyway, on forward inputs.** A large share of ARK-style names (RIVN, RXRX, IONQ, BEAM, NTLA, COIN post-pivot, PLTR's commercial-AI era) have 1–3 fiscal years of public history and live almost entirely in the **forward** thesis. The skill enters **Young-company mode** (see `references/scoring.md` §Young-company mode) and explicitly anchors on forward consensus, cash runway, dilution path, capacity roadmap, regulatory milestones, and customer pipeline — not on a backward 5-year operating-leverage curve. **Short history alone is not a rejection.** Reject reason C is reserved for genuinely pre-revenue names.

Three failure modes the user must be able to distinguish:
- **"Right platform, wrong company"** → platform fit strong but innovation revenue < 20% or no quantified management vision → ❌ reject; recommend a method that fits the actual revenue mix.
- **"Right company, framework limit (pre-revenue)"** → fits the platform but truly no commercial revenue base → ❌ reject (reason C); recommend an early-stage framework.
- **"Right company, short history but commercial"** → fits the platform, has commercial revenue, but < 3 yrs of public scale history → ✅ **enter Young-company mode**, do **not** reject.

## Workflow

1. **Resolve symbol** to `<CODE>.<MARKET>` (e.g. `TSLA.US`, `00700.HK`, `300750.SZ`).
2. **Sector triage** (decides mode + reject branch):
   - Traditional industry (bank / insurance / oil / real estate / staples / utilities not in energy-transition) → halt with reject reason **A — Traditional industry** (see `references/scoring.md` §Reject reasons).
   - Being-disrupted incumbent (e.g. ICE auto, fossil-fuel major, legacy media against streaming) → halt with reason **B — Being disrupted**.
   - Mature tech with disruption already priced in (e.g. mature consumer electronics supply chain) → halt with reason **D — Disruption premium already realised**.
   - **Truly pre-revenue** (no commercial product/service revenue, or revenue is < ~$10M annualised with no commercial path in 18 months) → halt with reason **C — Data basis insufficient**.
   - **Has commercial revenue but short public history** (listed < 3 fiscal years OR < 3 yrs of scale revenue OR recent business-model pivot OR post-SPAC < 12 months) → **enter Young-company mode** (see `references/scoring.md` §Young-company mode). Do **not** reject. The mode loosens history requirements and adds **mandatory forward-looking inputs** (forward consensus, cash runway, dilution path, capacity roadmap, regulatory milestones, customer pipeline).
   - **Standard mode** (commercial revenue + ≥ 3 yrs scale history + no recent pivot) → proceed without mode flag.
3. **Fetch raw data via Longbridge CLI first** (parallel where possible). See [§CLI](#cli). If `longbridge` is missing, fall back to MCP (see [§MCP fallback](#mcp-fallback)). Use WebSearch **only** for items genuinely outside Longbridge — TAM figures, Wright's-Law learning rates, qualitative management innovation signals, industry-runway evidence.
4. **Reconciliation gate** (勾稽校验) — runs **before** suitability scoring or any analysis. See [§Reconciliation](#reconciliation-勾稽校验). Two-state outcome:
   - **Pass (every check within tolerance)** → proceed. A one-line summary of the result still appears at the end of the data-source appendix.
   - **Fail (any check exceeds tolerance)** → halt all downstream analysis, emit a halt message naming the failing check and gap, still print the data-source appendix and the reconciliation summary describing the failure.
5. **Suitability scoring** — score 4 dimensions on 强/中/弱; apply the pass/reject matrix in `references/scoring.md` §Suitability. If Young-company mode is active, dimensions are evaluated on the available history (pro-rated, tagged in the appendix) and the **management-vision bar is raised** — quantified milestones + dated regulatory or commercial gates are now required for 强. If reject, emit the reject layout (see `references/output.md` §Reject case) with an alternative-method recommendation matched from `references/scoring.md` §Alternative-method matching. **Do not** produce a "for reference" ARK analysis on a rejected name.
6. **TAM** — three tiers (low / base / high), each tagged with a source priority (权威机构 > 公司自披露 > 学术/智库 > ARK 公开报告 > 估算). Estimation-only TAM must be explicitly labelled `估算`. See `references/scoring.md` §TAM rules.
7. **Wright's-Law note** — pick the technology learning rate from the table in `references/scoring.md` §Wright's Law and refresh it via WebSearch against the cited authority (BloombergNEF / IRENA / NHGRI / Epoch AI / ARK). Never use the embedded historical figure as the current value without verification.
8. **Three-scenario 5-year target** — Bull / Base / Bear with explicit (TAM, market share, net margin, terminal multiple) for each; weights 25 / 50 / 25 by default; discount rate 15% over 5 years; report each scenario price plus weighted expectation and upside/downside vs current price. See `references/scoring.md` §Scenario. **In Young-company mode**: year-5 share count uses the dilution path (not current shares); Bull CAGR must clear a 1.5× sell-side high-end sanity check or be flagged explicitly; Bear must include a runway-exhaustion sub-scenario if cash runway < 24 months.
9. **Forward-looking inputs panel (Young-company mode only)** — fetch the mode's required inputs (forward consensus, cash runway, 5-year dilution path, capex / capacity roadmap, regulatory / commercial milestone calendar, customer pipeline, technology-readiness signal). If any cannot be sourced, cap management-vision at 中 and say so in the report. See `references/output.md` §Forward inputs panel.
10. **Risks, action-frame, key observation node** — three concrete risks (in Young-company mode, at least one must come from the young-company sub-catalogue: cash runway / dilution / execution / tech-readiness gap), condition-based action sentences (no buy/sell command), one explicit next observation event/date.
11. **Output** the report from `references/output.md` — summary line → suitability → (forward-inputs panel if Young-company mode) → TAM → cost curve → 3 scenarios → risks → action frame → **Data Source Appendix (mandatory)** ending with the reconciliation summary line. Close with the ARK disclaimer variant matching the user's input language (single-language only — see `references/output.md` §Disclaimer variants).

## CLI

Run `longbridge <subcommand> --help` to verify exact flags before each call — do not hard-code flag names without verification. Primary calls (run in parallel):

```bash
# Balance sheet — equity, debt, working capital (for reconciliation only; ARK analysis is forward-looking)
longbridge financial-report <SYMBOL> --kind BS --report af --format json   # last 3–5 annual
longbridge financial-report <SYMBOL> --kind BS --report qf --format json   # last 4 quarterly

# Income statement — revenue, segment mix, gross/operating margin, R&D
longbridge financial-report <SYMBOL> --kind IS --report af --format json
longbridge financial-report <SYMBOL> --kind IS --report qf --format json

# Cash flow — CFO, capex, FCF; for reconciliation and capital-intensity context
longbridge financial-report <SYMBOL> --kind CF --report af --format json
longbridge financial-report <SYMBOL> --kind CF --report qf --format json

# Snapshot: current price, PE, PB, shares outstanding, market cap
longbridge quote <SYMBOL> --format json
longbridge calc-index <SYMBOL> --format json

# Long-window history (used for sanity-checking current vs historical valuation, not as the primary anchor)
longbridge kline <SYMBOL> --period day --count 2500 --format json

# Company profile + classification (for platform-fit decision)
longbridge basicinfo <SYMBOL> --format json
longbridge company-profile <SYMBOL> --format json

# Recent news + filings — for verifying management innovation vision claims
longbridge news <SYMBOL> --format json
longbridge sec-filings <SYMBOL> --format json     # US; for HK use the appropriate filings endpoint per --help

# Forward consensus + share-count history — REQUIRED in Young-company mode
longbridge analyst-estimates <SYMBOL> --format json   # forward EPS / revenue consensus
longbridge consensus <SYMBOL> --format json           # alternate consensus / sell-side dispersion
longbridge corporate <SYMBOL> --format json           # share-count history for the dilution path
longbridge calendar <SYMBOL> --format json            # upcoming events for key-observation node
```

### WebSearch fallback — only for items not available from Longbridge

ARK methodology depends heavily on third-party market-size and learning-rate data. WebSearch is **required** for TAM and Wright's-Law inputs; it must not be skipped to "save a step".

| Missing data | WebSearch query pattern | Acceptable source authorities |
|---|---|---|
| Sector TAM (general tech) | `"<market name> market size 2030 Gartner"` `"<market name> TAM IDC"` | Gartner, IDC, Forrester, McKinsey Global Institute |
| Clean-energy TAM | `"<segment> market size BloombergNEF"` `"<segment> 2030 IRENA"` | BloombergNEF, IRENA |
| Battery learning rate | `"battery learning rate" BloombergNEF` | BloombergNEF EV Outlook (latest annual) |
| Solar PV learning rate | `"solar PV learning rate" IRENA` | IRENA Renewable Power Generation Costs |
| DNA sequencing cost trend | `"DNA sequencing cost" NHGRI` | NHGRI cost database (latest update) |
| AI compute / inference cost | `"AI compute cost" learning rate "Epoch AI"` | Epoch AI, MLCommons, Stanford AI Index |
| Autonomous-driving runway | `site:ark-invest.com "autonomous" "Big Ideas"` | ARK Big Ideas (yearly, free) |
| Management innovation vision | `"<CEO>" innovation roadmap shareholder letter` | Annual report, earnings call, IR deck |
| Regulatory / policy overhangs | `"<sector> regulation <region> 2025"` | Government agency, FT, Reuters, WSJ |

Every WebSearch-sourced figure must be tagged `[Source: WebSearch — <publisher>, <report name>, <year>, <url>]` in the appendix; never silently mix it with Longbridge data, never invent a publisher to dress up an internal estimate.

## Reconciliation (勾稽校验)

Before any suitability scoring, TAM construction, or target-price calculation, verify the fetched figures are internally consistent. Reconciliation is **user-visible in this skill** — a one-line summary always appears as the final row of the Data Source Appendix. If a check fails, all downstream analysis halts.

| Check | Formula | Tolerance |
|---|---|---|
| IS↔BS link | Net income(t) ≈ Δ Retained earnings(BS, t) − dividends paid(CF, t) | ±3% |
| IS↔CF link | Net income + D&A + impairments + ΔWC ≈ Operating CF | ±5% |
| CF↔BS link | ΔCash from CF statement = Cash(t) − Cash(t−1) on BS | ±1% |
| Revenue segment sum | Σ segment revenue ≈ total revenue | ±2% |
| Innovation-revenue share | Innovation-related revenue / total revenue used in suitability matches the segment-mix breakdown | exact (must match what you display) |
| R&D ratio | R&D expense / total revenue used in suitability matches the IS statement | exact |
| BS — current assets sum | Cash + AR + Inventory + Other CA ≈ Total current assets | ±2% |
| BS — liabilities sum | ST debt + LT debt + Other liabilities ≈ Total liabilities | ±2% |
| Market cap | `calc-index` shares × current price ≈ market cap from `quote` | ±2% |
| Period alignment | All statements from the same fiscal period (or the lag is named) | exact |
| TAM source-tagging | Each TAM number has a source row in the appendix (机构 + 报告 + 年份, or `估算`) | exact |
| Learning-rate source-tagging | Wright's-Law learning rate has a source row (BloombergNEF / IRENA / NHGRI / Epoch AI / ARK) | exact |

Output rules for reconciliation:
- **All pass within tolerance** → final appendix row uses the clean-pass variant from `references/output.md` §Reconciliation summary, rendered in the user's input language only.
- **Some residuals within tolerance but material to displayed figures** → final appendix row lists each material residual on its own sub-line (which figure it affects).
- **Any check fails > tolerance** → halt all analysis; emit the halt message defined in `references/output.md` §Reject case-reconciliation and still print the appendix with the reconciliation summary describing the failure.
- **Young-company mode**: the 12 checks still apply, but rows that span more periods than the company has are pro-rated and tagged `history-limited (N quarters)` in the appendix; the reconciliation **summary line** still uses the standard ✅ / ⚠️ / ❌ variants — there is no separate young-company variant.

## Output

ARK-style diagnostic with 7 fixed sections (full template in `references/output.md`):

1. **Header + one-line conclusion** — platform attribution, weighted 5-year target, upside/downside vs current price, the one-line "core bet" sentence.
2. **Suitability check** — 4 dimensions (platform fit / innovation revenue / R&D intensity / management vision) each tagged 强 / 中 / 弱, with one-line evidence.
3. **TAM** — three tiers with source tags and a plain-language analogy.
4. **Wright's-Law cost curve** — technology domain, learning rate with cited authority, current cost position, plain-language interpretation.
5. **5-year target — three scenarios** — Bull / Base / Bear table with explicit (market share, net margin, terminal multiple), weighted expectation, current price, upside/downside.
6. **Main risks** — 3 concrete, named risks (not generic boilerplate).
7. **Action frame + key observation node** — condition-based sentences only ("if you believe X, then current price implies Y"); never a buy/sell directive. Plus one explicit next observation event/date.

Followed by the **Data Source Appendix (mandatory)** — every figure in sections [1]–[7] traceable to a row with source, fetch time, period, and (for WebSearch rows) URL; **final row is the reconciliation summary line** (pass / within-tolerance residual list / or failure description).

> ⚠️ 以上内容仅供参考，不构成投资建议。投资决策请结合自身风险承受能力独立判断。/ 以上內容僅供參考，不構成投資建議。投資決策請結合自身風險承受能力獨立判斷。/ For reference only. Not investment advice. Please make investment decisions independently based on your own risk tolerance.

## Error handling

| Situation | 简体回复 | 繁體回覆 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 回退到 MCP；若不可用，请安装 longbridge-terminal。 | 回退到 MCP；若不可用，請安裝 longbridge-terminal。 | Fall back to MCP; if unavailable install longbridge-terminal. |
| stderr `not logged in` / `unauthorized` | 请运行 `longbridge auth login`。 | 請執行 `longbridge auth login`。 | Run `longbridge auth login`. |
| Sector = traditional / being-disrupted / pre-revenue / mature | 直接拒绝并按 `references/output.md` 给出原因 A/B/C/D 与替代方法推荐。 | 直接拒絕並按 `references/output.md` 給出原因 A/B/C/D 與替代方法推薦。 | Reject and emit reason A/B/C/D plus alternative-method recommendation per `references/output.md`. |
| Reconciliation fails > tolerance | 明确披露失败项与差距，不输出任何评分或目标价；附录仍输出且勾稽汇总行注明失败。 | 明確披露失敗項與差距，不輸出任何評分或目標價；附錄仍輸出且勾稽匯總行註明失敗。 | Disclose failing check and gap; do not emit any scoring or target price; appendix still printed and reconciliation summary marks the failure. |
| TAM authority WebSearch returns nothing | 标注「TAM 暂无可引用的权威数据，以下为基于行业逻辑的估算区间」，附录该行写 `估算` 而非伪造机构。 | 標註「TAM 暫無可引用的權威數據，以下為基於行業邏輯的估算區間」，附錄該行寫 `估算` 而非偽造機構。 | Tag "TAM has no citable authoritative figure; the band shown is a logic-based estimate"; appendix row uses `估算` (estimated), never a fabricated publisher. |
| Learning-rate authority WebSearch returns nothing | 标注「学习率暂无公开权威数据」；不得直接使用本 Skill 中嵌入的历史数字。 | 標註「學習率暫無公開權威數據」；不得直接使用本 Skill 中嵌入的歷史數字。 | Tag "no publicly available authoritative learning rate"; do not silently use the embedded historical figure as current. |
| Suitability < pass threshold | 拒绝并匹配替代方法，不得给出「仅供参考」的 ARK 分析。 | 拒絕並匹配替代方法，不得給出「僅供參考」的 ARK 分析。 | Reject and match an alternative method; do not produce a "for reference" ARK analysis. |
| User horizon < 3 years stated | 提示 ARK 框架是 5 年视角，与短期需求不匹配。 | 提示 ARK 框架是 5 年視角，與短期需求不匹配。 | Warn that the ARK framework is a 5-year lens and does not fit a < 3-year horizon. |
| Young-company mode active, forward inputs missing | 报告中明示缺失项，把管理层愿景维度封顶到「中」，不得用乐观占位符填充。 | 報告中明示缺失項，把管理層願景維度封頂到「中」，不得用樂觀佔位符填充。 | Disclose the missing input(s) in the report and cap management-vision at 中; do not silently fill with optimistic placeholders. |
| Other stderr | 原样透传错误，不静默重试。 | 原樣透傳錯誤，不靜默重試。 | Surface stderr verbatim; never silently retry. |

## MCP fallback

If `longbridge` CLI is not installed, use MCP tools (`claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp`, `quote` scope):

| MCP tool | CLI equivalent |
|---|---|
| `mcp__longbridge__financial_report` | `longbridge financial-report` |
| `mcp__longbridge__calc_indexes` | `longbridge calc-index` |
| `mcp__longbridge__quote` | `longbridge quote` |
| `mcp__longbridge__kline` | `longbridge kline` |
| `mcp__longbridge__basicinfo` | `longbridge basicinfo` |
| `mcp__longbridge__news` | `longbridge news` |
| `mcp__longbridge__sec_filings` | `longbridge sec-filings` |
| `mcp__longbridge__analyst_estimates` | `longbridge analyst-estimates` (Young-company mode) |
| `mcp__longbridge__consensus` | `longbridge consensus` (Young-company mode) |
| `mcp__longbridge__corporate` | `longbridge corporate` (dilution path) |
| `mcp__longbridge__calendar` | `longbridge calendar` (key observation node) |

## Related skills

- Buffett moat single-stock view → `longbridge-buffett-moat-analyzer`
- Graham cigar-butt single-stock view → `longbridge-graham-stock-analysis`
- DCF intrinsic value → `longbridge-dcf`
- Three-statement reading → `longbridge-financial-report`
- Peer benchmarking → `longbridge-peer-comparison`
- Industry runway / sector view → `longbridge-industry-overview`
- Method selection guide → `longbridge-valuation-methodology`
- Small-cap growth → `longbridge-smallcap-growth`

## File layout

```
longbridge-ark-analysis/
├── SKILL.md
└── references/
    ├── scoring.md      # suitability rubric + reject reasons + alt-method matching + TAM rules + Wright's-Law table + scenario formula
    └── output.md       # full report template + label-translation lookup + reconciliation summary variants + ARK disclaimer
```
