---
name: longbridge-risk-return
description: |
  Risk-return optimisation for investment portfolios via Longbridge — builds risk-adjusted return-optimal portfolios based on fund size, risk preference (conservative / balanced / aggressive), and investment horizon. Asset allocation across equities / bonds / cash / commodities / alternatives. Evaluates current portfolio efficiency versus the efficient frontier. Triggers: "风险收益优化", "组合效率", "有效前沿", "风险偏好配置", "最优组合", "风险调整收益", "大类资产配置", "投资组合优化", "風險收益優化", "組合效率", "有效前沿", "風險偏好配置", "最優組合", "risk-return optimization", "portfolio efficiency", "efficient frontier", "risk preference", "optimal portfolio", "risk-adjusted return", "asset class allocation", "portfolio optimisation", "mean variance".
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

# longbridge-risk-return

Risk-return optimisation — evaluate portfolio efficiency versus the efficient frontier and recommend optimal asset allocation.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger on prompts asking for:

- Portfolio optimisation — *"帮我优化投资组合"*, *"optimal portfolio"*, *"投资组合优化"*
- Efficient frontier analysis — *"有效前沿"*, *"efficient frontier"*, *"组合效率"*
- Risk preference-based allocation — *"稳健型配置"*, *"aggressive allocation"*, *"风险偏好配置"*
- Risk-adjusted return improvement — *"提高夏普比率"*, *"risk-adjusted return"*, *"大类资产配置"*

> Requires Longbridge login with Trade scope for account data.

## Workflow

1. Fetch current portfolio and positions.
2. Ask the user for:
   - Risk preference: Conservative (低风险) / Balanced (稳健) / Aggressive (进取)
   - Investment horizon: short (1–2y) / medium (3–5y) / long (5y+)
   - Any constraints: max single-stock weight, excluded asset classes
3. Fetch 1-year daily return history for each position.
4. Compute:
   - Current portfolio: expected return, volatility, Sharpe ratio, max drawdown
   - Correlation matrix of holdings
   - Efficient frontier points (using simplified mean-variance framework)
   - Recommended target allocation for the user's risk profile
5. Compute the **Efficiency Gap**: distance from current portfolio to the nearest efficient frontier point.
6. Output target weights and rebalancing actions.
7. Convert multi-currency positions using FX rates.

> If unsure of exact flag names, run `longbridge <subcommand> --help` before proceeding.

## CLI

```bash
# Account portfolio summary
longbridge portfolio --format json

# Current positions
longbridge positions --format json

# 1-year daily OHLCV per holding (run for each symbol)
longbridge kline <SYMBOL> --period day --count 252 --format json

# FX rates for currency normalisation
longbridge exchange-rate --format json
```

## Output structure

```
RISK-RETURN OPTIMISATION  <Date>

RISK PROFILE: [Conservative | Balanced | Aggressive]
Horizon: x years

CURRENT PORTFOLIO
Expected Return:  x.x% p.a.   Volatility: x.x% p.a.
Sharpe Ratio:     x.xx         Max Drawdown: -x.x%
Efficiency Score: xx/100  (distance from efficient frontier)

EFFICIENT FRONTIER TARGETS
                   Conservative   Balanced   Aggressive
Expected Return    x.x%           x.x%       x.x%
Volatility         x.x%           x.x%       x.x%
Sharpe             x.xx           x.xx       x.xx

RECOMMENDED ALLOCATION (for your profile)
Equities:          xx%  (current: xx%)
Bonds / Fixed:     xx%  (current: xx%)
Cash:              xx%  (current: xx%)
Commodities/Alt:   xx%  (current: xx%)

CONCENTRATION RISK
Top holdings by weight:
1. <SYMBOL>  xx%  → Recommend: reduce to xx%
2. ...

REBALANCING ACTIONS
• Buy: <SYMBOL> +$x,xxx
• Sell: <SYMBOL> -$x,xxx
• No action: <SYMBOL>
```

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|-----------|---------|---------|---------------|
| Not logged in | 请运行 `longbridge auth login` 并授予 Trade 权限。 | 請執行 `longbridge auth login` 並授予 Trade 權限。 | Run `longbridge auth login` with Trade scope. |
| Insufficient history for a holding | 部分持仓历史数据不足，已使用市场代理替代。 | 部分持倉歷史數據不足，已使用市場代理替代。 | Insufficient history for some holdings — market proxy used. |
| Empty portfolio | 账户暂无持仓。 | 賬戶暫無持倉。 | No positions found in the account. |
| `command not found: longbridge` | 请安装 longbridge-terminal 或通过 MCP 连接。 | 請安裝 longbridge-terminal 或透過 MCP 連線。 | Install longbridge-terminal or connect via MCP. |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

- `longbridge-portfolio` — account P&L and current allocation
- `longbridge-positions` — holdings detail
- `longbridge-financial-planning` — retirement and savings goals
- `longbridge-strategy-optimizer` — strategy-level optimisation

## File layout

```
skills/longbridge-risk-return/
└── SKILL.md
```
