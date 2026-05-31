---
name: longbridge-profit-analysis
description: |
  Account-level profit and loss analysis via Longbridge Securities — simple return, time-weighted return (TWR), per-symbol P&L breakdown, and P&L by market. Supports custom date ranges. More focused on performance attribution than longbridge-portfolio. Requires login. Triggers: "盈亏分析", "账户盈亏", "时间加权收益", "TWR", "投资回报率", "持仓盈亏", "分市场盈亏", "业绩分析", "收益率分析", "盈虧分析", "賬戶盈虧", "時間加權收益", "投資回報率", "持倉盈虧", "profit analysis", "P&L analysis", "time-weighted return", "TWR", "account performance", "holding P&L", "profit by market", "investment return analysis", "我账户赚了多少", "我的亏损", "我賺了多少", "我的虧損".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: account_read
  requires_login: true
  default_install: true
  requires_mcp: false
  tier: read
---

# longbridge-profit-analysis

Full account P&L analysis — simple return, time-weighted return (TWR), per-symbol attribution, and market-level breakdown — sourced from the user's Longbridge account.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"我账户今年赚了多少"*, *"我今年的收益率"*, *"account P&L this year"*
- *"我的时间加权收益率"*, *"TWR"*, *"time-weighted return"*
- *"TSLA 这只股票我亏了多少"*, *"holding P&L for NVDA"*
- *"美股账户盈亏"*, *"profit by market"*, *"HK market P&L"*
- *"帮我分析一下 Q1 业绩"*, *"Q1 performance analysis"*
- **Prefer over `longbridge-portfolio`** when the user wants return-rate metrics (TWR eliminates cash-flow distortion) or detailed per-symbol attribution.

## Workflow

1. Confirm login; if not logged in, tell user to run `longbridge auth login` with Trade scope.
2. Identify the operation: overall P&L / per-symbol detail / by-market / custom date range.
3. Extract date range from context if specified; default to YTD if not stated.
4. Call CLI with `--format json`; run `--help` if unsure about flags.
5. Present: overall return %, absolute gain/loss, TWR (note: eliminates cash-flow timing distortion), top contributors, and breakdown table.

## CLI

Run `longbridge profit-analysis --help` to verify exact flags before use.

```bash
# Overall account P&L with TWR (default: YTD or account lifetime)
longbridge profit-analysis --format json

# Custom date range
longbridge profit-analysis --start 2026-01-01 --end 2026-04-30 --format json

# Per-symbol P&L detail
longbridge profit-analysis detail TSLA.US --format json

# P&L broken down by market
longbridge profit-analysis by-market --market HK --format json

# Check available flags and subcommands
longbridge profit-analysis --help
```

## Output

### Overall P&L

| Field | 简体 | 繁體 | English |
|---|---|---|---|
| `simple_return` | 简单收益率 | 簡單收益率 | Simple return |
| `twr` | 时间加权收益率 | 時間加權收益率 | Time-weighted return (TWR) |
| `total_profit` | 总盈亏 | 總盈虧 | Total P&L |
| `realized` | 已实现盈亏 | 已實現盈虧 | Realized P&L |
| `unrealized` | 未实现盈亏 | 未實現盈虧 | Unrealized P&L |
| `period` | 统计期间 | 統計期間 | Period |

**TWR note**: Always explain TWR briefly — *"时间加权收益率消除了追加/取出资金对收益率的影响，是更客观的业绩衡量指标。"* / *"時間加權收益率消除了追加/取出資金對收益率的影響，是更客觀的業績衡量指標。"* / *"TWR removes the effect of cash flows (deposits/withdrawals), providing a purer performance measure."*

### Per-symbol detail

Render: symbol, market, cost basis, current value, unrealized P&L, realized P&L, total return %.

### By-market

Render: market (US / HK / CN / SG), total value, P&L, return %.

End every response with:

> ⚠️ 以上数据仅供参考，不构成投资建议。/ 以上數據僅供參考，不構成投資建議。/ For reference only. Not investment advice.

## Error handling

| Situation | 简体 | 繁體 | English |
|---|---|---|---|
| `command not found: longbridge` | 退回 MCP；如未配置，提示安装 longbridge-terminal | 退回 MCP；如未設定，提示安裝 longbridge-terminal | Fall back to MCP; if unavailable, ask user to install longbridge-terminal |
| `not logged in` / `unauthorized` | 请运行 `longbridge auth login`（需要 Trade 权限） | 請執行 `longbridge auth login`（需要 Trade 權限） | Run `longbridge auth login` with Trade scope |
| Empty result (no trade history) | 账户暂无交易记录，无法计算盈亏 | 賬戶暫無交易記錄，無法計算盈虧 | No trade history found — cannot compute P&L |
| Invalid date range | 日期格式须为 YYYY-MM-DD，开始日期须早于结束日期 | 日期格式須為 YYYY-MM-DD，開始日期須早於結束日期 | Date must be YYYY-MM-DD; start must precede end |
| Other stderr | 原文转达，不做静默重试 | 原文轉達，不作靜默重試 | Relay verbatim; never retry silently |

## MCP fallback

If `longbridge` CLI is not installed, use:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

## Related skills

- Portfolio overview (value, cash share, industry mix) → `longbridge-portfolio`
- Account holdings snapshot → `longbridge-positions`
- Order and fill history → `longbridge-orders`
- Account statements for export → `longbridge-statement`

## File layout

```
longbridge-profit-analysis/
└── SKILL.md          # prompt-only, no scripts/
```
