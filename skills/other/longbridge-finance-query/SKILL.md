---
name: longbridge-finance-query
description: |
  Cross-market financial metrics batch query — revenue, net profit, ROE, debt ratio, free cash flow, gross margin for one or more symbols across HK / US / A-share / SG markets. Supports multi-symbol horizontal comparison, similar to natural-language financial screening. Triggers: "财务数据查询", "财务指标", "营收查询", "净利润查询", "ROE查询", "负债率", "现金流查询", "毛利率查询", "财务数据批量", "財務數據查詢", "財務指標", "營收查詢", "淨利潤查詢", "ROE查詢", "負債率", "現金流查詢", "毛利率查詢", "financial data query", "revenue query", "net profit query", "ROE query", "debt ratio", "free cash flow", "gross margin query", "financial metrics", "financial comparison", "batch financials".
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

# longbridge-finance-query

Cross-market financial metrics batch query — revenue, net profit, ROE, debt ratio, free cash flow, gross margin, and other core KPIs for one or more symbols. Supports multi-symbol horizontal comparison.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger when the user asks about:

- Core financial metrics for one or more stocks — *"NVDA 最新营收"*, *"苹果净利润"*, *"帮我查这几家公司的ROE"*
- Cross-stock financial comparison — *"TSLA 和 BYD 的毛利率对比"*, *"科技股自由现金流排名"*
- Specific financial line items — *"资产负债率"*, *"经营现金流"*, *"每股收益"*
- Natural-language financial screening — *"哪些股票ROE超过20%"* (note: Longbridge returns data for specified symbols; full market screening is not supported)

For a single company's full financial deep-dive, prefer `longbridge-fundamental`. For segment-level operating breakdown, prefer `longbridge-business-query`.

## Workflow

1. Extract all symbols from the prompt; normalise each to `<CODE>.<MARKET>`.
2. Identify which financial statements are needed:
   - **Income statement** (revenue, gross profit, net profit, EPS) → `--kind IS`
   - **Balance sheet** (total assets, total liabilities, debt ratio, equity) → `--kind BS`
   - **Cash flow** (operating CF, free CF) → `--kind CF`
3. Run `longbridge financial-report` for each symbol and statement type.
4. Run `longbridge calc-index` for computed ratios (PE, PB, ROE, ROA).
5. Merge results by symbol; present as a comparison matrix when multiple symbols are requested.

## CLI

```bash
# Income statement — revenue, gross profit, net profit, EPS
longbridge financial-report <SYMBOL> --kind IS --format json

# Balance sheet — assets, liabilities, equity
longbridge financial-report <SYMBOL> --kind BS --format json

# Cash flow — operating, investing, financing, free cash flow
longbridge financial-report <SYMBOL> --kind CF --format json

# Computed indices — ROE, ROA, PE, PB
longbridge calc-index <SYMBOL> --index roe,roa,pe_ttm,pb --format json
```

> Run `longbridge financial-report --help` and `longbridge calc-index --help` to confirm current flag names and available `--kind` options.

## Output

For a single symbol, present a financial snapshot table. For multiple symbols, present a comparison matrix:

| Metric | 简体 | 繁體 | English |
|---|---|---|---|
| Revenue | 营业收入 | 營業收入 | Revenue |
| Gross profit margin | 毛利率 | 毛利率 | Gross margin |
| Net profit | 净利润 | 淨利潤 | Net profit |
| EPS | 每股收益 | 每股盈利 | EPS |
| Debt-to-asset ratio | 资产负债率 | 資產負債率 | Debt ratio |
| Free cash flow | 自由现金流 | 自由現金流 | Free cash flow |
| ROE | 净资产收益率 | 淨資產收益率 | ROE |

Always include the fiscal period and currency in the output.

## Error handling

| Situation | 简体回复 | 繁體回覆 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 请先安装 longbridge-terminal | 請先安裝 longbridge-terminal | Install longbridge-terminal first |
| `not logged in` | 请运行 `longbridge auth login` | 請執行 `longbridge auth login` | Run `longbridge auth login` |
| Symbol not covered | 提示该标的暂无财务数据 | 提示該標的暫無財務數據 | Note data not available for this symbol |
| Other stderr | 原样展示，不重试 | 原樣展示，不重試 | Surface verbatim, do not retry |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

| User asks | Route to |
|---|---|
| Full single-company fundamental deep-dive | `longbridge-fundamental` |
| Business segment breakdown | `longbridge-business-query` |
| 2–5 stock valuation comparison | `longbridge-peer-comparison` |
| Analyst consensus / EPS estimates | `longbridge-insresearch` |
| Institutional holders / insider trades | `longbridge-flows` |

## File layout

```
longbridge-finance-query/
└── SKILL.md
```

Prompt-only — no `scripts/`. Discover current CLI flags via `longbridge <subcommand> --help`.
