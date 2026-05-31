---
name: longbridge-earnings-preview
description: >
  Pre-earnings analysis skill — extracts prior guidance, tracks events, summarises earnings
  call Q&A, and generates a structured preview report (inline summary + DOCX) before a
  company reports quarterly results. Supports US, HK, and A-share markets.
  Triggers: "财报前瞻", "财报预览", "财报季准备", "财报要关注什么", "下季度财报", "业绩前瞻",
  "上季度指引", "电话会要点", "財報前瞻", "財報預覽", "財報季準備", "財報要關注什麼",
  "下季度財報", "業績前瞻", "上季度指引", "電話會要點",
  "earnings preview", "pre-earnings", "prior guidance", "earnings call Q&A",
  "NVDA earnings preview", "what to watch this earnings", "before earnings".
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

# longbridge-earnings-preview

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## What This Skill Does

You help individual investors prepare for an upcoming earnings release by surfacing the
information they need — without requiring them to manually dig through filings, transcripts,
and news. You produce a structured preview covering 6 modules, delivered as an inline
conversation summary and an optional DOCX file.

## When to Use

| Trigger | Example |
|---------|---------|
| Before earnings release | "NVDA 下季度财报要关注什么" / "Preview TSLA.US Q3 earnings" |
| Prior guidance review | "苹果上季度给了什么指引？" / "What was AAPL's guidance last quarter?" |
| Earnings call Q&A | "上期电话会分析师在问什么？" |
| General earnings prep | "下周要发财报了，帮我梳理一下" / "Help me prepare for MSFT earnings" |

**Do not trigger if:** the company has already reported → use earnings-update skill instead.

## Output Language

Follow the user's conversation language. Both the inline summary and the DOCX must use the
same language — whichever the user is speaking.

- English conversation → fully English output (inline + DOCX)
- Chinese conversation → fully Chinese output (inline + DOCX)
- User can override at any time: "write in English" / "用中文写" / "用繁體中文寫"

**Always in English regardless of output language:** file names, ticker symbols, CLI commands,
financial metric abbreviations (EPS, EBIT, CapEx, YoY, etc.), and numeric values with currency
symbols.

**DOCX CJK font requirement:** When generating a Chinese DOCX, every `run` element must set
both the Latin font (`w:rFonts`) and the CJK font (`w:eastAsia`) explicitly — e.g. Calibri +
Microsoft YaHei. Also call `set_doc_default_cjk()` on the document's Normal style. This ensures
tables, headers, and body text all render correctly without falling back to system fonts.

## Data Sources

Priority: **CLI (primary) → Web Search (supplement)**

Before using any CLI command, run `longbridge <command> --help` to check the exact argument
format and available options — the CLI is updated frequently and flags may change.
Do not assume flag names or argument positions.

**CLI docs**: https://open.longbridge.com/zh-CN/docs/cli/
**MCP endpoint**: `https://openapi.longbridge.com/mcp`

| Data Needed | CLI Entry Point |
|-------------|----------------|
| Prior filings & guidance | `longbridge filing --help` |
| Financial statements | `longbridge financial-report --help` |
| Analyst consensus estimates | `longbridge consensus --help` |
| EPS estimates & revisions | `longbridge forecast-eps --help` |
| Operating history | `longbridge operating --help` |
| Quote & valuation | `longbridge quote --help` / `longbridge calc-index --help` |
| Price trend | `longbridge kline --help` |
| Capital flow & positioning | `longbridge capital --help` |
| Analyst ratings | `longbridge institution-rating --help` |
| News & events | `longbridge news --help` |

**JSON output handling:** When parsing CLI JSON output with Python or jq, always save to a
temp file first (`longbridge <cmd> > /tmp/data.json`), then read the file. Do not pipe
directly — the CLI may append version notification lines to stdout that break JSON parsing.

Web Search supplements: earnings call transcripts, options-implied move, whisper numbers,
recent industry events not yet in CLI.

## Functional Modules

### Module A — Prior Quarter Earnings Extraction

Extract from the most recent earnings filing and call:
- **Guidance fulfillment**: the key metric is always **management's own prior guidance vs. actual result** — not YoY comparison, not consensus vs. actual. Specifically: what did management guide for Q[N-1] at the end of Q[N-2]? How did Q[N-1] actual compare to that guidance?
- **Management outlook**: macro/sector views, strategic priorities, capital allocation
- **Performance summary**: for each guided metric, compute the beat/miss amount and direction

**Critical rule for 【一】table columns:**
```
指标 | 管理层此前指引（上上季电话会） | 上季实际值 | 与指引偏差 | 评估
```
- Column 2 = management's own guidance range/midpoint, NOT market consensus
- Column 3 = actual reported value
- Column 4 = (actual − guidance midpoint) / guidance midpoint, with sign
- Column 5 = 超预期 / 基本符合 / 不及预期

If management did not give quantitative guidance for a metric (e.g., exploration-stage companies),
use operational milestone commitment vs. actual progress instead.

Use `longbridge filing --help` to locate prior filings. For transcripts not available via CLI,
use web search: "[company] Q[X] earnings call transcript" or "[company] Q[X] guidance".

### Module B — Recent Events Tracking

Surface events since the prior earnings release that are relevant to this quarter's results.
Categorize by:
- **Macro / policy**: rate changes, trade policy, regulatory actions
- **Industry**: competitor moves, sector data, supply chain changes
- **Company**: product launches, management changes, M&A rumors, major contracts, stock moves
- **Market sentiment**: analyst rating changes, institutional activity, options implied volatility

Use `longbridge news --help` for news and `longbridge institution-rating --help` for rating changes.
Use web search for events not yet indexed in CLI.

Each event: timestamp, source, relevance to upcoming earnings.

### Module C — Prior Earnings Call Q&A Summary

Extract from the prior earnings call transcript:
- **High-frequency analyst questions**: topics multiple analysts pressed on (margins, segment growth, capex, etc.)
- **Management response**: concise conclusion for each key question — not verbatim, just the key judgment
- **Verification significance**: which of these Q&A topics will be answered or updated by this quarter's results

Source: web search for "[company] Q[X] earnings call transcript".

### Module D — Key Focus Framework for This Quarter

Synthesize Modules A–C into an actionable preview:
- **Guidance fulfillment checklist**: each prior quantitative guidance item → the specific data point to check
- **Beat / miss risk factors**: what could cause results to surprise in either direction
- **3–5 key questions to watch**: written in plain language, combining institutional focus with the user's holding thesis
- **Risk flags**: tail risks from prior management warnings + recent external events

See [references/scenarios.md](references/scenarios.md) for scenario analysis framework.

### Module E — Historical Guidance Fulfillment Tracking

Pull 4–8 quarters of history to establish management's guidance track record:
- Guidance vs. actual value table by quarter (revenue, profit, margins, key metrics)
- Bias pattern: does management consistently guide conservatively or optimistically?
- Metric reliability: which metrics have tight historical deviation (high confidence) vs. wide (apply discount)
- **Credibility assessment for current guidance**: qualitative conclusion based on the pattern
  (e.g. "Revenue guidance has beaten actual by avg 3–5% over 6 quarters — current guidance likely conservative")

Use `longbridge financial-report --help`, `longbridge operating --help`, `longbridge consensus --help`.

### Module F — Market Consensus vs. Management Guidance

Identify expectation gaps between the Street and management:
- Current consensus estimates for key metrics (revenue, EPS, margins)
- Comparison with management guidance: is consensus above / below / within the guidance range?
- Historical consensus accuracy: how well has the Street predicted results over prior quarters?
- **Expectation gap alerts**: flag significant divergences as upside or downside risk

Use `longbridge consensus --help` and `longbridge forecast-eps --help` for consensus data.

## Output

### Output 1 — Inline Conversation Summary

Use exactly the following structure. Sections with no available data must be skipped entirely
with a one-line note (e.g. "暂无电话会记录，跳过"). Do not rename, reorder, or add extra sections.

```
📊 [公司名称（股票代码）] 财报前瞻摘要
财报发布日期：{日期} | 分析日期：{今天}
════════════════════════════════════════

【一】上期业绩指引回顾
▸ [指标]：管理层指引 {区间/中值} → 实际 {值}（{超预期/不及预期 +X%}）
  ※ 必须是管理层自身指引 vs. 实际，不是共识 vs. 实际，不是 YoY 对比
▸ ...

【二】管理层展望要点
▸ ...

【三】上期电话会 | 分析师核心 Q&A
Q1：[问题]
  ↳ 管理层答复：[结论]
  ↳ 本次关注：[需验证的指标]

【四】近期重要事件
▸ [日期] [来源] 事件描述 → 关联性：...

【五】历史指引兑现规律
▸ 收入指引：过去 N 季平均偏差 {方向} {幅度}
▸ EPS 指引：兑现率 {%}，平均偏差 {值}
▸ 本次指引可信度：{评估}

【六】市场一致预期 vs 管理层指引
  指标      市场预期   管理层指引   偏差
  收入      ...        ...          ...
  EPS       ...        ...          ...
▸ 预期差提示：...

【七】本次财报核心关注点
① ...
② ...
③ ...

【八】风险提示
⚠ ...

---
⚡ 数据来源：Longbridge CLI + Web Search | 仅供参考，不构成投资建议
```

### Output 2 — DOCX Report (always generate by default)

Use the builders at `scripts/docx_builder.py` and `scripts/chart_builder.py`.
**Never write a one-off DOCX script from scratch.**

Target format: rich institutional report with **data tables + matplotlib charts** in every section.
Reference example: `00700HK_Q1_2026_Earnings_Preview.docx` (8 charts + 6 tables, 11 sections).

#### DocxBuilder API

```python
import sys
sys.path.insert(0, "<skill_dir>")          # path to earnings-preview/
from scripts.docx_builder import DocxBuilder
from scripts.chart_builder import ChartBuilder

cb = ChartBuilder()
b = DocxBuilder(
    symbol="ADBE.US", company="Adobe Inc.",
    report_date="2026年6月11日", analysis_date="2026年5月6日",
    price="$250.71", market_cap="~$1013亿",
    valuation="P/E 14.06x", rating="买入（39位分析师）",
    output_path="ADBE_Q2_FY2026_Earnings_Preview.docx",
)
b.cover()
b.toc([("【一】","上期业绩指引回顾"), ...])
b.section("【一】上期业绩指引回顾")
b.body("...")
b.table(headers, rows, col_widths)
b.image(cb.quarterly_bar(...))            # embed chart
b.section("【三】上期电话会 | 分析师核心 Q&A")
b.qa("问题", "管理层答复", "本次关注指标")
# ... repeat for all 8 sections ...
b.disclaimer()
b.save()
```

#### ChartBuilder — available chart types

| Method | Description | Typical Section |
|--------|-------------|-----------------|
| `quarterly_bar(title, quarters, values, estimate_idx, ylabel)` | 季度趋势柱状图（末栏高亮为预测值） | 营收趋势 |
| `growth_lines(title, quarters, series, ylabel)` | 多系列 YoY 增速折线图 | 营收/利润增速 |
| `grouped_bar(title, categories, series, ylabel)` | 分组柱状图（分部 vs 上期对比） | 分部营收对比 |
| `pie_pair(title1, title2, labels, values1, values2)` | 双饼图（上期 vs 本期结构） | 收入结构 |
| `scenario_hbar(title, scenarios, values, current, current_label)` | 情景分析横向条形图 | 情景分析 |
| `peer_multiples(title_l, title_r, companies, vals_l, vals_r, highlight, ...)` | 同业估值对比（P/E + P/B） | 估值对比 |
| `price_action(title, dates, prices, current, current_label, target, target_label)` | 60日股价走势线图 | 股价走势 |
| `analyst_pt_hbar(title, brokers, targets, current, current_label)` | 分析师目标价对比 | 分析师共识 |

All chart functions return a PNG file path. Pass directly to `b.image(path)`.

#### Chart generation rules

- Generate charts from actual CLI data — do not fabricate numbers.
- For exploration/pre-revenue companies, adapt charts: use operational milestones instead of
  revenue trends; use cash runway bar instead of quarterly revenue; show drill results if available.
- Always include: (1) scenario chart, (2) price action chart, (3) at least one data trend chart.
- If peer data is unavailable via CLI, use web search to get comparable multiples.

File name: `[SYMBOL]_Q[N]_[YEAR]_Earnings_Preview.docx`

The builder handles CJK font (`Microsoft YaHei` + `Calibri`) on every run automatically.
Never set fonts manually — just use `b.body()`, `b.bullet()`, `b.table()`, `b.qa()`, `b.image()`.
String content must use straight quotes only — no curly/smart quotes inside Python strings.

## Error handling

| Situation | LLM response |
|---|---|
| Shell `command not found: longbridge` | Fall back to MCP if configured; otherwise tell the user to install longbridge-terminal and provide the web-search-only preview with a clear label. |
| stderr `not logged in` / `unauthorized` | Tell the user to run `longbridge auth login`; the skill can still proceed with web search for public data. |
| Company has already reported | Tell the user to use `longbridge-earnings` instead (post-earnings update skill). |
| No CLI data + no web results | State which modules have gaps; still deliver available modules — do not produce a blank report. |
| Other stderr | Surface verbatim — never silently retry. |

## MCP fallback

If the CLI binary is unavailable and `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` is configured:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

## Related skills

| If the user wants … | Use |
|---|---|
| Post-earnings deep-dive (company has already reported) | [`longbridge-earnings`](../longbridge-earnings) |
| 5-dimension fundamentals snapshot | [`longbridge-fundamental`](../longbridge-fundamental) |
| Historical PE / PB percentile | [`longbridge-valuation`](../longbridge-valuation) |
| Classified news + filings + community sentiment | [`longbridge-news`](../longbridge-news) |
| Daily incremental briefing across watchlist | [`longbridge-catalyst-radar`](../longbridge-catalyst-radar) |
| Earnings date / calendar | [`longbridge-calendar`](../longbridge-calendar) |

## Reference Files

| File | Contents | When to Read |
|------|----------|--------------|
| [scenarios.md](references/scenarios.md) | Bull/Base/Bear scenario framework, sector-specific key metrics, options-implied move | Building Module D scenario analysis |
| [checklist.md](references/checklist.md) | Pre-report data collection checklist and output quality checks | Before finalizing output |

## File layout

```
longbridge-earnings-preview/
├── SKILL.md
├── commands/
│   └── earnings-preview.md     # /earnings-preview <SYMBOL> slash command
├── references/
│   ├── scenarios.md            # scenario analysis framework
│   └── checklist.md            # data collection + quality checklist
└── scripts/
    ├── docx_builder.py         # DocxBuilder class — DOCX generation
    └── chart_builder.py        # ChartBuilder class — matplotlib charts
```
