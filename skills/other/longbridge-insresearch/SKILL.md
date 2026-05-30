---
name: longbridge-insresearch
description: |
  Institutional research and analyst ratings — buy/hold/sell distribution, consensus price target, EPS/revenue forecasts, and rating change history. ESG and credit ratings are not available via Longbridge. Triggers: "研报评级", "机构评级", "买入评级", "目标价", "机构观点", "分析师推荐", "券商评级", "机构研究", "研報評級", "機構評級", "買入評級", "目標價", "機構觀點", "分析師推薦", "券商評級", "analyst rating", "institution rating", "buy rating", "price target", "broker recommendation", "analyst opinion", "research rating", "sell-side rating", "consensus target", "EPS forecast", "analyst consensus".
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

# longbridge-insresearch

Institutional research and analyst ratings for Longbridge-covered securities — buy/hold/sell distribution, consensus price target, forward EPS/revenue estimates, and rating change history.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger when the user asks about:

- Analyst rating distribution — *"NVDA 有多少个买入评级"*, *"AAPL 分析师怎么看"*
- Consensus price target — *"特斯拉目标价共识"*, *"TSLA analyst price target"*
- Forward EPS / revenue estimates — *"苹果下个季度EPS预测"*, *"NVDA revenue forecast"*
- Rating change history — *"近期哪些机构升级了这只股票"*, *"recent rating upgrades"*

For full fundamentals, prefer `longbridge-fundamental`. For insider trades, prefer `longbridge-flows`.

## Workflow

1. Normalise the symbol to `<CODE>.<MARKET>`.
2. Run `longbridge institution-rating` for buy/hold/sell distribution and recent rating events.
3. Run `longbridge consensus` for consensus price target and aggregated analyst view.
4. Run `longbridge forecast-eps` for forward EPS and revenue estimates by period.
5. Synthesise into a structured analyst overview: rating distribution pie, consensus target vs. current price upside, and EPS/revenue estimates table.

## CLI

```bash
# Buy / hold / sell distribution and recent rating events
longbridge institution-rating <SYMBOL> --format json

# Consensus price target and aggregated analyst view
longbridge consensus <SYMBOL> --format json

# Forward EPS and revenue estimates
longbridge forecast-eps <SYMBOL> --format json
```

> Run `longbridge institution-rating --help`, `longbridge consensus --help`, and `longbridge forecast-eps --help` to verify current flags.

## Output

Present a three-part summary:

1. **Rating distribution** — count and % of Buy / Hold / Sell ratings, total analyst coverage.
2. **Price target** — consensus target, high/low range, upside vs. current price.
3. **Estimates table** — forward EPS and revenue for next 1–2 fiscal years.

| Field | 简体 | 繁體 | English |
|---|---|---|---|
| Buy ratings | 买入评级数 | 買入評級數 | Buy ratings |
| Hold ratings | 持有评级数 | 持有評級數 | Hold ratings |
| Sell ratings | 卖出评级数 | 賣出評級數 | Sell ratings |
| Consensus target | 目标价共识 | 目標價共識 | Consensus target |
| Upside to target | 目标价上行空间 | 目標價上行空間 | Upside to target |
| Forward EPS | 预测每股收益 | 預測每股盈利 | Forward EPS |

Note: ESG ratings and credit ratings (Moody's / S&P) are not available via Longbridge.

## Error handling

| Situation | 简体回复 | 繁體回覆 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 请先安装 longbridge-terminal | 請先安裝 longbridge-terminal | Install longbridge-terminal first |
| `not logged in` | 请运行 `longbridge auth login` | 請執行 `longbridge auth login` | Run `longbridge auth login` |
| No analyst coverage | 提示该标的暂无机构评级数据 | 提示該標的暫無機構評級數據 | No analyst coverage available |
| Other stderr | 原样展示，不重试 | 原樣展示，不重試 | Surface verbatim, do not retry |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

| User asks | Route to |
|---|---|
| Full fundamentals (P&L, balance sheet, cash flow) | `longbridge-fundamental` |
| Insider trades / institutional holdings | `longbridge-flows` |
| Historical valuation percentile | `longbridge-valuation` |
| Post-earnings analyst reaction | `longbridge-earnings` |
| Pre-earnings preview | `longbridge-earnings-preview` |

## File layout

```
longbridge-insresearch/
└── SKILL.md
```

Prompt-only — no `scripts/`. Discover current CLI flags via `longbridge <subcommand> --help`.
