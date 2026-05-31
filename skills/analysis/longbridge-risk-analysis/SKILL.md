---
name: longbridge-risk-analysis
description: |
  Risk measurement and stress testing via Longbridge — computes VaR (historical simulation / parametric), CVaR (expected shortfall), max drawdown, Sharpe ratio, Calmar ratio, and runs historical scenario stress tests (2008 GFC, 2020 COVID crash, 2022 rate-hike cycle). Triggers: "风险分析", "VaR", "压力测试", "最大回撤", "夏普比率", "CVaR", "历史情景", "尾部风险", "风险测量", "風險分析", "壓力測試", "最大回撤", "夏普比率", "歷史情景", "尾部風險", "風險測量", "risk analysis", "VaR value at risk", "CVaR", "stress test", "max drawdown", "Sharpe ratio", "Calmar ratio", "tail risk", "historical scenario".
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

# longbridge-risk-analysis

Prompt-only analysis skill. Fetches price history and account positions to compute portfolio risk metrics (VaR, CVaR, max drawdown, Sharpe, Calmar) and runs historical scenario stress tests.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"帮我做风险分析"* / *"風險分析"* / *"run a risk analysis on my portfolio"*
- *"计算 VaR"* / *"計算 VaR"* / *"calculate VaR"*
- *"最大回撤是多少"* / *"最大回撤"* / *"what is the max drawdown"*
- *"夏普比率分析"* / *"夏普比率"* / *"Sharpe ratio analysis"*
- *"压力测试一下"* / *"壓力測試"* / *"run a stress test"*
- *"如果2008年金融危机再来，我的组合会损失多少"* / *"historical scenario stress test"*

## Workflow

1. Fetch current positions (if logged in) or use user-specified symbols.
2. Fetch 252-day daily price history for each symbol concurrently.
3. Compute portfolio daily return series (weighted by current/equal weights).
4. Calculate risk metrics and run scenario analyses.
5. Present a structured risk report.

## CLI

Run `longbridge <subcommand> --help` to verify exact flags before calling.

```bash
# Current positions (if logged in)
longbridge portfolio --format json
longbridge positions --format json

# 252-day daily price history per symbol (run concurrently)
longbridge kline <SYMBOL> --period day --count 252 --format json
```

## Calculations

### Core Risk Metrics

| Metric | Method |
|---|---|
| Historical VaR (95%) | 5th percentile of 252-day daily portfolio return distribution |
| Historical VaR (99%) | 1st percentile of same distribution |
| Parametric VaR (95%) | μ − 1.645σ (assuming normal distribution; annualised → daily) |
| CVaR / Expected Shortfall (95%) | Mean of returns below VaR(95%) threshold |
| Max Drawdown | max peak-to-trough decline over the 252-day window |
| Sharpe Ratio | (Annual return − 4% risk-free) ÷ Annual volatility |
| Calmar Ratio | Annual return ÷ |Max Drawdown| |
| Volatility (ann.) | Daily return std × √252 |

### Historical Scenario Stress Tests

Approximate the impact of each scenario on the portfolio by applying historically-observed drawdowns as a proxy. State clearly that these are illustrative estimates based on past market events.

| Scenario | Reference period | Typical equity drawdown |
|---|---|---|
| 2008 GFC | Sep 2008 – Mar 2009 | S&P 500 −57% |
| 2020 COVID crash | Feb 2020 – Mar 2020 | S&P 500 −34% |
| 2022 rate-hike cycle | Jan 2022 – Oct 2022 | S&P 500 −25%; Nasdaq −35% |
| 2015 A-share crash | Jun 2015 – Aug 2015 | CSI 300 −45% |

Apply sector beta adjustments where data allows; otherwise use index drawdown × portfolio beta (estimated from 60-day regression against benchmark).

## Output template

```
Portfolio Risk Analysis — Source: Longbridge Securities
Analysis window: 252 trading days  Date: <today>

[Risk Metrics]
- Daily VaR (95%, historical): <N>%   (1-day loss not exceeded 95% of the time)
- Daily VaR (99%, historical): <N>%
- CVaR / Expected Shortfall (95%): <N>%
- Max Drawdown (1yr): <N>%  (peak: <date> → trough: <date>)
- Annualised Volatility: <N>%
- Sharpe Ratio (rf=4%): <N>
- Calmar Ratio: <N>

[Scenario Stress Tests]
Scenario             Estimated Portfolio Loss   Notes
2008 GFC             −<N>%  (~$<X>)            Based on −57% S&P draw; beta adj.
2020 COVID           −<N>%  (~$<X>)            Based on −34% S&P draw
2022 Rate-hike       −<N>%  (~$<X>)            Based on −25% S&P draw
2015 A-share crash   −<N>%  (~$<X>)            Applies if holding A-shares

[Risk Summary]
- Tail risk level: {Low / Medium / High}
- Largest risk contributor: <symbol> (<N>% of portfolio risk)
- Key concern: <observation>

⚠️ 风险指标基于历史数据估算，不预测未来损失。/ 風險指標基於歷史數據估算，不預測未來損失。/ Risk metrics are historical estimates and do not predict future losses.
```

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 回退到 MCP；若也不可用，请安装 longbridge-terminal | 回退到 MCP；若也不可用，請安裝 longbridge-terminal | Fall back to MCP; if unavailable, install longbridge-terminal. |
| stderr `not logged in` | 未登录，请提供要分析的标的列表 | 未登入，請提供要分析的標的列表 | Not logged in — please provide symbol list to analyse. |
| Price history < 60 days | 数据不足，降级为近60日风险估算，结果可信度较低 | 數據不足，降級為近60日風險估算 | Insufficient history; results may be less reliable. |
| Single-asset portfolio | 无法计算分散化效益，仅显示单资产指标 | 無法計算分散化效益，僅顯示單資產指標 | Single asset — cannot compute diversification benefit. |

## MCP fallback

If `longbridge` CLI is not installed, use MCP tools:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP setup: `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` (`quote` scope; `trade_read` for account data).

## Related skills

- Portfolio health-check → `longbridge-portfolio-diagnosis`
- Asset allocation frameworks → `longbridge-asset-allocation`
- Portfolio rebalancing → `longbridge-portfolio-rebalance`

## File layout

```
longbridge-risk-analysis/
└── SKILL.md          # prompt-only, no scripts/
```
