---
name: longbridge-earnings
description: >
  Post-earnings analysis skill — generates institutional-grade earnings update reports
  (8–12 page DOCX) and structured conversation summaries for companies under coverage.
  Covers beat/miss analysis, segment breakdown, margin trends, guidance assessment,
  updated estimates, and valuation. Supports US, HK, and A-share markets.
  Use this skill whenever the user wants a post-earnings analysis or quarterly-results
  writeup, even if they do not say "earnings update" verbatim. Triggers: "earnings update",
  "quarterly results", "Q1/Q2/Q3/Q4 results", "earnings report", "post-earnings analysis",
  "beat/miss", "guidance update", "财报分析", "业绩更新", "季度业绩", "季报", "年报",
  "盈利分析", "财报点评", "財報分析", "業績更新", "季度業績", "季報", "年報", "財報點評".
---

# Earnings Update Skill

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English. Both the DOCX report body and the in-chat summary follow the user's language; chart labels, axis titles, and file names always stay in English.

## When to Use

| Trigger | Example |
|---------|---------|
| Post-earnings analysis | "Analyze TSLA.US latest earnings" / "帮我分析腾讯最新财报" |
| Specific quarter update | "Tencent Q4 2024 earnings update" / "业绩更新" |
| Quarterly results | "Q1/Q2/Q3/Q4 results for [company]" |

**Do not trigger if:** user wants an initiation report.

## Data Sources

Priority: **CLI (primary) → Web Search (supplement)**

Use the Longbridge CLI for all market data. Before using any command, run `longbridge <command> --help` to check available options — the CLI is updated frequently.

**CLI + Python pattern**: prefer reading from a file over piping into `python3 -c`. Multi-line JSON with embedded quotes can hit shell-quoting edge cases (especially under zsh's `-c` argument handling), so the safer pattern is:

```bash
longbridge institution-rating 700.HK --format json > /tmp/rating.json
python3 -c "import json; d = json.load(open('/tmp/rating.json')); print(d)"
```

If you do prefer pipes, use a heredoc-fed Python script (`python3 <<'PY' ... PY`) or save to a file and run a `.py` file.

**CLI docs**: https://open.longbridge.com/zh-CN/docs/cli/
**MCP endpoint**: `https://openapi.longbridge.com/mcp`

**CLI discovery**: Run `longbridge --help` to see all available subcommands, then `longbridge <subcommand> --help` before calling. Do not assume subcommand names — the CLI is updated frequently. Broad categories needed for earnings analysis:

- Earnings calendar / upcoming earnings dates
- Financial statements (income, balance sheet, cash flow)
- Earnings snapshot / AI beat-miss summary
- Analyst consensus & EPS estimates
- Quote & valuation metrics
- Price history (candlestick)
- Analyst ratings & target prices
- Regulatory filings (10-Q, 10-K, 8-K)
- News

Web Search supplements for content not in CLI: consensus estimates vintage, earnings call transcripts, M&A precedent data.

## Execution Workflow

**Step 1 — Identify reporting period**
Use `longbridge filing --help` to find the latest quarterly or annual filing. Confirm the period with the user before proceeding.

**Step 2 — Collect data & analyze**
See [references/workflow.md](references/workflow.md)

**Step 3 — Update valuation**
See [references/valuation-methodologies.md](references/valuation-methodologies.md)

**Step 4 — Generate DOCX report**
See [references/report-structure.md](references/report-structure.md)

**Step 5 — Output conversation summary**
See [references/summary-card-spec.md](references/summary-card-spec.md)

## Output

1. **DOCX report**: `[SYMBOL]_Q[N]_[YEAR]_Earnings_Update.docx` (8-12 pages, 8-12 charts)
2. **Conversation summary**: 8-module structured output directly in chat

**IMPORTANT**: Do NOT append a Sources section or reference links to the conversation output. All citations belong in the DOCX only.

## MCP fallback

If the local `longbridge` CLI is unavailable (`command not found: longbridge`) and the user has run `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp`, the same data is reachable through MCP. Subcommand → MCP tool mapping:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP-only extras worth pulling in for Step 3 valuation:

- the equivalent MCP tool — historical PE/PB time series for percentile context
- the equivalent MCP tool — industry-relative position
- the equivalent MCP tool / `profit_analysis_detail` — only if the user wants a portfolio-level P&L view alongside the single-name update

## Related skills

This skill is the heaviest in the family (institutional-grade 8–12 page DOCX). For lighter or differently-framed asks, defer to a sibling:

| User asks for ... | Use |
|---|---|
| Historical PE/PB percentile, "is X expensive vs its own history / industry?" | [`longbridge-valuation`](../longbridge-valuation) |
| 5-dimension KPI overview (revenue / margins / ROE / dividend / consensus) without a DOCX deliverable | [`longbridge-fundamental`](../longbridge-fundamental) |
| Cross-symbol matrix, "X vs Y vs Z" | [`longbridge-peer-comparison`](../longbridge-peer-comparison) |
| Classified news + filings + community sentiment for a single name | [`longbridge-news`](../longbridge-news) |
| Daily incremental briefing across the user's watchlist | [`longbridge-catalyst-radar`](../longbridge-catalyst-radar) |
| Live quote / valuation indices | [`longbridge-quote`](../longbridge-quote) |

If the user wants the full earnings DOCX *plus* one of the above (e.g. "earnings update on TSLA and how it compares to Ford"), do this skill first, then chain to the other.

## Reference Files

| File | Contents | When to Read |
|------|----------|--------------|
| [workflow.md](references/workflow.md) | Data collection steps, beat/miss framework, segment/margin/guidance analysis | Before analysis |
| [valuation-methodologies.md](references/valuation-methodologies.md) | DCF, trading comps, precedent transactions — full methodology | During valuation |
| [report-structure.md](references/report-structure.md) | Page-by-page DOCX templates, table and chart formatting, citation rules | Before generating report |
| [summary-card-spec.md](references/summary-card-spec.md) | 8-module conversation summary format with examples | When outputting summary |
| [best-practices.md](references/best-practices.md) | Quality checklist, common mistakes, headline examples | Quality check |
