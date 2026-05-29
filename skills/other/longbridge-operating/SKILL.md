---
name: longbridge-operating
description: |
  Quarterly and annual operating data for listed companies via Longbridge Securities — revenue, net income, EPS, ROE, gross margin, and other KPIs broken down by reporting period. Complements longbridge-fundamental with period-by-period trend detail. Note: currently returns data for HK-listed stocks only; US and A-share symbols return empty results. Triggers: "经营数据", "运营指标", "分季度财务", "经营情况", "季度营收", "季度利润", "财务趋势", "经營數據", "運營指標", "分季度財務", "季度營收", "季度利潤", "operating data", "quarterly financials", "operating indicators", "quarterly revenue", "quarterly profit", "financial trend by period", "700.HK operating", "按期次财务", "按期次財務".
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

# longbridge-operating

Period-by-period operating and financial KPI breakdown for listed companies — quarterly or annual, sourced from Longbridge Securities.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"700.HK 分季度财务"*, *"腾讯季度营收趋势"*, *"Tencent quarterly revenue"*
- *"看一下 2388.HK 各季度利润"*, *"700.HK annual operating data"*
- *"港股季报数据"*, *"HK stock quarterly financials"*
- **Not suitable**: US-listed (TSLA.US, NVDA.US) or A-share stocks — the `operating` endpoint returns empty for those markets; redirect to `longbridge-fundamental` instead.

## Workflow

1. Resolve symbol to `<CODE>.<MARKET>`.
2. Confirm it is an HK-listed stock (`.HK`). If not, warn the user that operating data is currently HK-only and suggest `longbridge-fundamental` for non-HK symbols.
3. Determine report filter from context: all periods (default), annual (`af`), or specific quarters (`q1`, `q2`, `q3`, `q4`, comma-separated).
4. Call `longbridge operating` with `--format json`. Run `--help` first if unsure about flags.
5. Present results as a period table sorted newest-first; highlight YoY and QoQ changes where computable.

## CLI

Run `longbridge operating --help` to verify exact flags before use.

```bash
# All reporting periods (default)
longbridge operating 700.HK --format json

# Annual reports only
longbridge operating 700.HK --report af --format json

# Specific quarters
longbridge operating 700.HK --report q1,q3 --format json

# Check available flags
longbridge operating --help
```

## Output

Render as a table sorted newest period first. Include at minimum:

| Period | 简体 | 繁體 | English |
|---|---|---|---|
| `period` | 报告期 | 報告期 | Period |
| `revenue` | 营收 | 營收 | Revenue |
| `net_income` | 净利润 | 淨利潤 | Net income |
| `eps` | 每股收益 | 每股盈利 | EPS |
| `roe` | 净资产收益率 | 股本回報率 | ROE |
| `gross_margin` | 毛利率 | 毛利率 | Gross margin |

Where YoY / QoQ changes are computable from the returned data, add a `Δ%` column. Cite Longbridge Securities.

**HK-only notice** (always show when user asks for a non-HK symbol):

> 简体: `operating` 命令目前仅支持港股，{SYMBOL} 暂无数据，建议改用 `longbridge-fundamental`。
> 繁體: `operating` 命令目前僅支援港股，{SYMBOL} 暫無數據，建議改用 `longbridge-fundamental`。
> English: The `operating` command currently returns data for HK-listed stocks only. No data for {SYMBOL} — try `longbridge-fundamental` instead.

## Error handling

| Situation | 简体 | 繁體 | English |
|---|---|---|---|
| `command not found: longbridge` | 退回 MCP；如未配置，提示安装 longbridge-terminal | 退回 MCP；如未設定，提示安裝 longbridge-terminal | Fall back to MCP; if unavailable, ask user to install longbridge-terminal |
| Empty result (non-HK symbol) | 见 HK-only notice | 見 HK-only notice | See HK-only notice above |
| `not logged in` | 请运行 `longbridge auth login` | 請執行 `longbridge auth login` | Run `longbridge auth login` |
| Other stderr | 原文转达 | 原文轉達 | Relay verbatim |

## MCP fallback

If `longbridge` CLI is not installed, use:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

## Related skills

- Snapshot KPIs (revenue / EPS / margins) → `longbridge-fundamental`
- Analyst consensus estimates → `longbridge-consensus`
- Earnings calendar → `longbridge-calendar`

## File layout

```
longbridge-operating/
└── SKILL.md          # prompt-only, no scripts/
```
