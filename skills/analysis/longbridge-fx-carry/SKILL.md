---
name: longbridge-fx-carry
description: |
  FX carry-trade analysis via Longbridge Securities — combines spot rates, interest-rate differentials (high-yield vs low-yield currencies), volatility, and historical price trends to assess carry opportunities. Analyses common carry pairs (AUD/JPY, NZD/USD, MXN/JPY) and outputs carry yield, drawdown risk, and Sharpe ratio. Triggers: "外汇套息", "套息交易", "carry trade", "利差交易", "高息货币", "低息货币", "汇率套利", "外汇策略", "外匯套息", "套息交易", "利差交易", "高息貨幣", "低息貨幣", "匯率套利", "FX carry trade", "carry strategy", "interest rate differential", "high yield currency", "currency carry", "AUD JPY", "NZD USD".
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

# longbridge-fx-carry

FX carry-trade analysis — evaluate interest-rate differential, historical carry returns, and key risks for currency pairs.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger on prompts asking about:

- FX carry trade opportunities — *"AUD/JPY 套息机会"*, *"carry trade 机会"*, *"FX carry strategy"*
- Interest-rate differential between currencies — *"利差交易"*, *"interest rate differential"*
- High-yield vs low-yield currency pairing — *"高息货币"*, *"high yield currency"*
- Carry trade risk (unwind scenarios) — *"套息交易风险"*, *"carry unwind"*

For plain FX spot rates defer to `longbridge-fx`. For equity market correlation defer to `longbridge-correlation`.

## Common carry pairs

| Pair | 高息货币 / High-yield | 低息货币 / Low-yield | 典型场景 |
|------|----------------------|---------------------|---------|
| AUD/JPY | AUD | JPY | Risk-on carry |
| NZD/USD | NZD | USD | Commodity carry |
| MXN/JPY | MXN | JPY | EM carry |
| TRY/USD | TRY | USD | High-risk EM |
| BRL/JPY | BRL | JPY | EM carry |

> If unsure of exact flag names, run `longbridge <subcommand> --help` before proceeding.

## Workflow

1. Identify the carry pair(s) from the user's prompt; default to AUD/JPY, NZD/USD, MXN/JPY if unspecified.
2. Fetch current spot rates for all relevant currencies.
3. Look up prevailing benchmark interest rates (use embedded knowledge or `longbridge macro` if available).
4. Calculate annualised carry yield: `(high-yield rate − low-yield rate)`.
5. Fetch historical FX price data (60 days) to estimate realised volatility.
6. Compute simplified Sharpe: `carry_yield / annualised_vol`.
7. Assess tail-risk scenarios (rapid JPY strength / EM stress / risk-off unwind).
8. Output structured summary.

## CLI

```bash
# Spot exchange rates
longbridge exchange-rate --format json

# Historical FX price series (if supported by the CLI)
longbridge kline <FX_PAIR> --period day --count 60 --format json
```

## Output

Present for each pair:

```
Pair      Carry Yield   60d Volatility   Est. Sharpe   Signal
─────────────────────────────────────────────────────────────
AUD/JPY      3.2%           8.4%            0.38       Moderate
NZD/USD      2.1%           6.2%            0.34       Moderate
MXN/JPY      8.5%          14.1%            0.60       High / Risky
```

Follow with a narrative covering: current macro environment, carry unwind risks, position sizing guidance.

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|-----------|---------|---------|---------------|
| FX pair not supported | 该货币对暂不支持，请尝试其他主要货币对。 | 該貨幣對暫不支援，請嘗試其他主要貨幣對。 | This FX pair is not supported — try a major currency pair. |
| Historical FX data unavailable | 历史汇率数据不可用，仅提供当前利差分析。 | 歷史匯率數據不可用，僅提供當前利差分析。 | Historical FX data unavailable — providing current differential only. |
| `command not found: longbridge` | 请安装 longbridge-terminal 或通过 MCP 连接。 | 請安裝 longbridge-terminal 或透過 MCP 連線。 | Install longbridge-terminal or connect via MCP. |
| `not logged in` | 请运行 `longbridge auth login`。 | 請執行 `longbridge auth login`。 | Run `longbridge auth login`. |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

- `longbridge-fx` — plain FX spot rates
- `longbridge-correlation` — cross-asset correlation
- `longbridge-volatility-strategy` — options-implied volatility surface

## File layout

```
skills/longbridge-fx-carry/
└── SKILL.md
```
