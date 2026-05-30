---
name: longbridge-options-pnl
description: |
  Options P&L analysis via Longbridge — payoff diagrams, breakeven points, max profit/loss, and Greeks sensitivity (Delta/Gamma/Theta/Vega) for single-leg and multi-leg strategies. Triggers: "期权盈亏", "盈亏图", "盈亏平衡", "最大亏损", "最大盈利", "Greeks敏感性", "Delta", "Gamma", "Theta", "Vega", "多腿组合", "期权到期", "期權盈虧", "盈虧圖", "盈虧平衡", "最大虧損", "最大盈利", "Greeks敏感性", "多腿組合", "options payoff", "P&L diagram", "breakeven", "max profit", "max loss", "Greeks sensitivity", "delta gamma theta vega", "multi-leg options".
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

# longbridge-options-pnl

Prompt-only analysis skill. Fetches live option quotes, then computes and explains payoff diagrams, breakevens, max profit/loss, and Greeks sensitivities for single-leg and multi-leg option positions.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"AAPL 200 call 的盈亏平衡点在哪"* / *"AAPL 200 call 盈虧平衡在哪"* / *"What is the breakeven on AAPL 200 call?"*
- *"我卖出一个 TSLA put，最大亏损多少"* / *"I sold a TSLA put, what is my max loss?"*
- *"帮我算跨式组合的到期盈亏"* / *"Show me the straddle payoff at expiry"*
- *"这个期权的 Theta 每天损耗多少"* / *"How much Theta decay per day?"*

For vol surface and IV analysis route to `longbridge-options-volatility`. For strategy selection route to `longbridge-options-strategy`.

## CLI

Run `longbridge <subcommand> --help` to verify exact flags.

```bash
# Fetch option quote (IV, Greeks, premium) for a known OCC symbol
longbridge option quote <OCC_SYMBOL> --format json

# Discover OCC symbol from underlying + expiry
longbridge option chain <SYMBOL> --format json
longbridge option chain <SYMBOL> --date <YYYY-MM-DD> --format json

# Underlying spot price for payoff x-axis range
longbridge quote <SYMBOL> --format json
```

## Workflow

1. **Identify legs** — extract each leg: side (buy/sell), type (call/put), strike, expiry, quantity, premium paid/received.
2. **Fetch live data** — call `longbridge option quote` for each OCC symbol; if not known, use `option chain` to find it. Fetch underlying spot with `longbridge quote`.
3. **Compute at-expiry payoff** for each leg:
   - Long call: `max(S − K, 0) − premium`
   - Short call: `premium − max(S − K, 0)`
   - Long put: `max(K − S, 0) − premium`
   - Short put: `premium − max(K − S, 0)`
   - Net payoff = sum across all legs.
4. **Find breakeven(s)** — stock price(s) where net payoff = 0.
5. **Find max profit and max loss** — scan payoff at key price points (strikes + beyond).
6. **Summarise Greeks** from `option quote` output; compute net Greeks for multi-leg.
7. **Output** payoff table + summary (template below).

## Output template

```
{Strategy name} P&L snapshot — Source: Longbridge Securities

[Position]
Leg 1: {Buy/Sell} {N} {SYMBOL} {YYMMDD} {C/P} K={strike}  Premium={prem}
...

[Payoff at expiry]
S      Net P&L
{S-30%} {$X}
{S-15%} {$X}
{ATM}   {$X}  ← current spot
{S+15%} {$X}
{S+30%} {$X}

[Key metrics]
- Breakeven: ${X} [and ${Y} for two-sided strategies]
- Max profit: ${X} {at S ≥/≤ $Y / unlimited}
- Max loss:   ${X} {at S ≤/≥ $Y / unlimited}

[Net Greeks (current)]
- Delta: {X}  (position moves ~${X} per $1 in underlying)
- Gamma: {X}
- Theta: {X} / day  (time decay per calendar day)
- Vega:  {X} / 1% IV change

⚠️ 以上分析仅供参考，不构成投资建议。/ 以上分析僅供參考，不構成投資建議。/ For reference only. Not investment advice.
```

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 切换到 MCP；若不可用，请安装 longbridge-terminal | 切換至 MCP；若不可用，請安裝 longbridge-terminal | Fall back to MCP; if unavailable, install longbridge-terminal |
| stderr `not logged in` | 请执行 `longbridge auth login` | 請執行 `longbridge auth login` | Run `longbridge auth login` |
| OCC symbol not found in chain | 请提供到期日和行权价以便查找合约 | 請提供到期日和行權價以便查找合約 | Please provide expiry and strike to locate the contract |
| Greeks missing from quote | 从 Black-Scholes 近似计算，精度有限 | 從 Black-Scholes 近似計算，精度有限 | Approximated via Black-Scholes; limited accuracy |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

## Related skills

- IV / vol analysis → `longbridge-options-volatility`
- Strategy selection → `longbridge-options-strategy`
- Advanced vol strategies → `longbridge-options-advanced`
- Raw option chain / quotes → `longbridge-derivatives`

## File layout

```
longbridge-options-pnl/
└── SKILL.md          # prompt-only, no scripts/
```
