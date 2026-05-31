---
name: longbridge-business-query
description: |
  Main business composition and operating data — revenue breakdown by segment, gross margin by business line, and operating metrics (ROE / ROA / ROIC / working capital turnover). Shareholder / customer / supplier data is not available via Longbridge; pair with longbridge-news to extract segment detail from filings. Triggers: "主营业务", "业务构成", "分部营收", "业务拆分", "经营数据", "业务占比", "收入结构", "主营收入", "主營業務", "業務構成", "分部營收", "業務拆分", "經營數據", "業務佔比", "business breakdown", "revenue breakdown", "segment revenue", "business composition", "operating data", "revenue structure", "main business", "segment breakdown", "gross margin by segment".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
  requires_mcp: false
  tier: read
---

# longbridge-business-query

Main business composition and operating data for Longbridge-covered companies — segment revenue breakdown, gross margin by business line, and key operating metrics (ROE / ROA / ROIC / working capital turnover).

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger when the user asks about:

- Revenue / gross profit breakdown by segment — *"苹果各业务收入占比"*, *"腾讯主营业务构成"*
- Gross margin by business line — *"苹果硬件和服务毛利率对比"*
- Operating efficiency metrics — *"AAPL 的 ROE / ROA"*, *"京东 ROIC"*
- Business model composition — *"特斯拉业务结构"*, *"Tesla business breakdown"*

For full P&L / balance sheet / cash flow drill-down, prefer `longbridge-fundamental` or `longbridge-finance-query`. For company filings containing segment tables, pair with `longbridge-news`.

## Workflow

1. Normalise the symbol to `<CODE>.<MARKET>`.
2. Run `longbridge financial-report` with `--kind IS` (income statement) for revenue and gross profit.
3. Run `longbridge calc-index` for ROE / ROA and other computed operating indices.
4. For HK-listed companies, try `longbridge operating` for additional operating KPIs.
5. If segment data is not in the above responses, instruct the user to pair with `longbridge-news` to extract segment tables from the company's annual / interim reports (filings search).
6. Present a structured breakdown, noting any data gaps.

## CLI

```bash
# Income statement (revenue, COGS, gross profit by period)
longbridge financial-report <SYMBOL> --kind IS --format json

# Computed operating indices (ROE, ROA, ROIC, working capital turnover)
longbridge calc-index <SYMBOL> --index roe,roa --format json

# Operating data (HK-listed companies, may include operating KPIs)
longbridge operating <SYMBOL> --format json

# Filings for segment tables (annual / interim reports)
longbridge filing <SYMBOL> --format json
```

> Run `longbridge financial-report --help`, `longbridge calc-index --help`, and `longbridge operating --help` to verify current flags before calling.

## Output

Present as a two-part summary:

1. **Revenue composition** — total revenue, gross profit, gross margin by major segment (where available).
2. **Operating metrics table**:

| Metric | 简体 | 繁體 | English |
|---|---|---|---|
| Return on equity | 净资产收益率 | 淨資產收益率 | ROE |
| Return on assets | 总资产收益率 | 總資產收益率 | ROA |
| Return on invested capital | 投入资本回报率 | 投入資本回報率 | ROIC |
| Working capital turnover | 营运资本周转率 | 營運資本周轉率 | Working capital turnover |

If segment-level detail is absent, note: *"Longbridge 暂无分部数据，建议查阅公告 (`longbridge-news`)"* / *"Segment data unavailable via Longbridge; check filings via `longbridge-news`."*

## Error handling

| Situation | 简体回复 | 繁體回覆 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 请先安装 longbridge-terminal | 請先安裝 longbridge-terminal | Install longbridge-terminal first |
| `not logged in` | 请运行 `longbridge auth login` | 請執行 `longbridge auth login` | Run `longbridge auth login` |
| `operating` returns empty (non-HK) | 提示该命令仅支持港股 | 提示此命令僅支援港股 | Note: `operating` supports HK-listed only |
| Other stderr | 原样展示，不重试 | 原樣展示，不重試 | Surface verbatim, do not retry |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

| User asks | Route to |
|---|---|
| Full P&L / balance sheet / cash flow | `longbridge-fundamental` |
| Multi-stock financial comparison | `longbridge-finance-query` |
| News / filings for segment tables | `longbridge-news` |
| Shareholders / ownership structure | `longbridge-ownership` |
| Analyst estimates by segment | `longbridge-insresearch` |

## File layout

```
longbridge-business-query/
└── SKILL.md
```

Prompt-only — no `scripts/`. Discover current CLI flags via `longbridge <subcommand> --help`.
