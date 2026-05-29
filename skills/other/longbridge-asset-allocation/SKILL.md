---
name: longbridge-asset-allocation
description: |
  Asset allocation and portfolio optimisation via Longbridge — efficient frontier (MPT), Black-Litterman model overview, risk parity / risk budgeting, all-weather strategy, and practical allocation recommendations based on the user's Longbridge account data. Triggers: "资产配置", "组合优化", "有效前沿", "Black-Litterman", "风险预算", "风险平价", "全天候策略", "大类资产", "資產配置", "組合優化", "有效前沿", "風險預算", "風險平價", "全天候策略", "大類資產", "asset allocation", "portfolio optimization", "efficient frontier", "Black-Litterman", "risk parity", "all-weather strategy", "mean-variance optimization", "strategic allocation".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: account_read
  requires_login: false
  default_install: true
  requires_mcp: false
  tier: analysis
---

# longbridge-asset-allocation

Prompt-only analysis skill. Explains major asset-allocation frameworks (MPT efficient frontier, Black-Litterman, risk parity, all-weather) and, when the user is logged in, applies them to their actual Longbridge portfolio data.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"帮我做资产配置分析"* / *"資產配置分析"* / *"help me with asset allocation"*
- *"什么是有效前沿"* / *"有效前沿"* / *"explain the efficient frontier"*
- *"Black-Litterman 模型怎么用"* / *"Black-Litterman model"*
- *"风险平价策略"* / *"風險平價策略"* / *"risk parity strategy"*
- *"全天候策略怎么配置"* / *"全天候策略"* / *"all-weather portfolio allocation"*
- *"帮我优化组合配置"* / *"optimize my portfolio allocation"*

## Workflow

1. **Framework selection**: identify which allocation approach the user wants (MPT / Black-Litterman / risk parity / all-weather / practical advice).
2. **Account data** (if logged in): fetch current positions and 252-day price history for each holding.
3. **Explain the framework** with the user's actual holdings as context.
4. **Generate suggested target weights** based on the chosen framework.
5. Present the allocation with rationale.

## CLI

Run `longbridge <subcommand> --help` to verify exact flags before calling.

```bash
# Current holdings (if user is logged in)
longbridge portfolio --format json
longbridge positions --format json

# 252-day daily price history for each holding (run concurrently; ~1 year for covariance)
longbridge kline <SYMBOL> --period day --count 252 --format json

# Optional: valuation context
longbridge calc-index <SYMBOL> --format json
```

## Framework Reference

### MPT (Modern Portfolio Theory)
- Compute expected return (historical mean daily return × 252) and covariance matrix from 252-day returns.
- Find minimum-variance portfolio and tangency portfolio (max Sharpe).
- Caution: MPT is sensitive to input estimation error; treat outputs as directional, not prescriptive.

### Black-Litterman
- Start from market-cap equilibrium weights (CAPM implied returns).
- Blend user's views (e.g. "I expect TSLA to outperform by 5%") via Bayesian update.
- Output: posterior expected returns + revised weights.
- Explain conceptually; provide numeric illustration when user supplies explicit views.

### Risk Parity
- Allocate so each asset contributes equally to total portfolio volatility.
- Approximate weight ∝ 1 / volatility (simplified). For full risk parity use covariance.
- Result: typically overweights low-volatility assets (bonds, gold) vs equities.

### All-Weather (Bridgewater style)
- 4 economic quadrants: growth up/down × inflation up/down.
- Suggested weight guidance: 30% equities, 40% long bonds, 15% intermediate bonds, 7.5% gold, 7.5% commodities.
- Map user's holdings to quadrant exposure; identify gaps.

## Output template

```
Asset Allocation Analysis — Source: Longbridge Securities
Framework: <MPT / Black-Litterman / Risk Parity / All-Weather / Practical>
Date: <today>

[Current Portfolio]
Asset       Weight   Expected Return   Volatility (ann.)
<symbol>    <N>%     <N>%              <N>%
...

[Suggested Allocation — <Framework>]
Asset       Target Weight   Rationale
<symbol>    <N>%            <reason>
...

[Key Metrics]
- Portfolio expected return (ann.): N%
- Portfolio volatility (ann.): N%
- Sharpe ratio (rf=4%): N

[Caveats]
- Historical returns do not guarantee future results.
- Covariance estimates are noisy over short windows.
- <framework-specific caveats>

⚠️ 仅供参考，不构成投资建议。/ 僅供參考，不構成投資建議。/ For reference only. Not investment advice.
```

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 回退到 MCP；若也不可用，请安装 longbridge-terminal | 回退到 MCP；若也不可用，請安裝 longbridge-terminal | Fall back to MCP; if unavailable, install longbridge-terminal. |
| stderr `not logged in` | 未登录时将使用用户指定的标的做示例分析 | 未登入時將使用用戶指定的標的做示例分析 | Not logged in — will analyse user-specified symbols instead. |
| Price history < 60 days | 数据不足，降级为简单波动率估算 | 數據不足，降級為簡單波動率估算 | Insufficient history; degrade to simple volatility estimate. |
| No positions and no symbols given | 请提供要分析的标的或登录账户 | 請提供要分析的標的或登入賬戶 | Please provide symbols to analyse or log in to your account. |

## MCP fallback

If `longbridge` CLI is not installed, use MCP tools:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP setup: `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` (`quote` scope; `trade_read` for account data).

## Related skills

- Rebalance to a new target → `longbridge-portfolio-rebalance`
- Portfolio health-check → `longbridge-portfolio-diagnosis`
- Risk metrics (VaR, drawdown) → `longbridge-risk-analysis`

## File layout

```
longbridge-asset-allocation/
└── SKILL.md          # prompt-only, no scripts/
```
