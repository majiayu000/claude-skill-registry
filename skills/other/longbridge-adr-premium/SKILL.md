---
name: longbridge-adr-premium
description: |
  ADR / H-share / A-share cross-market pricing analysis via Longbridge Securities — tracks the premium or discount between US-listed ADRs, HK-listed H-shares, and A-shares; calculates theoretical arbitrage spread; analyses constraints (FX controls, transaction costs, liquidity). Triggers: "ADR溢价", "ADR折价", "AH溢价", "ADR套利", "美股ADR", "三地比价", "跨市场套利", "双重上市", "ADR溢價", "ADR折價", "AH溢價", "ADR套利", "三地比價", "跨市場套利", "ADR premium", "ADR discount", "AH premium", "ADR arbitrage", "cross-listing premium", "dual-listed", "three-market comparison", "BABA ADR", "HK ADR".
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

# longbridge-adr-premium

Cross-market premium / discount analysis for companies dual- or triple-listed as ADR (US), H-share (HK), and/or A-share (CN).

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger on prompts asking about:

- ADR vs H-share premium / discount — *"BABA ADR 溢价"*, *"百度 ADR 和港股哪个便宜"*
- Three-market comparison — *"BABA.US / 9988.HK / 阿里A股 比价"*
- Theoretical arbitrage spread and constraints — *"ADR 套利空间"*, *"ADR arbitrage"*
- Dual-listing pricing discrepancy — *"dual-listed premium"*, *"跨市场套利"*

For pure A/H premium time series defer to `longbridge-ah-premium`.

## Workflow

1. Identify all available listing venues for the company (ADR ticker, HK code, A-share code).
2. Fetch real-time quotes for each venue.
3. Fetch USD/HKD and USD/CNY exchange rates.
4. Convert all prices to a common currency (USD) using the ADR ratio where applicable.
5. Calculate premium / discount between each pair: `(Price_A − Price_B) / Price_B × 100%`.
6. Assess arbitrage constraints: FX repatriation rules, stamp duty, liquidity depth, settlement lag.
7. Output a comparison table and narrative.

> If unsure of exact flag names, run `longbridge <subcommand> --help` before proceeding.

## CLI

```bash
# Quotes for each listing venue
longbridge quote <ADR_SYMBOL> --format json
longbridge quote <HK_SYMBOL> --format json
longbridge quote <A_SYMBOL> --format json   # omit if no A-share listing

# Exchange rates for currency conversion
longbridge exchange-rate --format json
```

Common examples:

| Company | ADR | H-share | A-share |
|---------|-----|---------|---------|
| Alibaba | BABA.US | 9988.HK | — |
| Baidu | BIDU.US | 9888.HK | — |
| JD.com | JD.US | 9618.HK | — |
| NIO | NIO.US | 9866.HK | — |

## Output

Present a summary table then a narrative:

```
Symbol        Price (local)   Price (USD)   vs ADR
──────────────────────────────────────────────────
BABA.US        $82.50          $82.50        baseline
9988.HK        HK$638.00       $81.79        −0.9%
```

Then explain:
- Which venue is cheapest / most expensive and why.
- Arbitrage constraints (FX controls, transaction costs, liquidity).
- Whether the spread is actionable or structural.

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|-----------|---------|---------|---------------|
| Symbol not found | 未找到该代码，请确认上市交易所和代码格式。 | 找不到該代碼，請確認上市交易所和代碼格式。 | Symbol not found — please verify the exchange and ticker format. |
| No ADR listing | 该公司没有美股 ADR，只能比较 H 股和 A 股。 | 該公司沒有美股 ADR，只能比較 H 股和 A 股。 | No US ADR found — comparing H-share vs A-share only. |
| Exchange rate unavailable | 汇率数据暂时不可用，无法换算成同一货币。 | 匯率數據暫時不可用，無法換算成同一貨幣。 | Exchange rate unavailable — cannot convert to a common currency. |
| `command not found: longbridge` | 请先安装 longbridge-terminal，或通过 MCP 连接。 | 請先安裝 longbridge-terminal，或透過 MCP 連線。 | Install longbridge-terminal or connect via MCP. |
| `not logged in` | 请运行 `longbridge auth login` 完成登录。 | 請執行 `longbridge auth login` 完成登入。 | Run `longbridge auth login` to authenticate. |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

- `longbridge-ah-premium` — A/H premium time series and intraday curve
- `longbridge-peer-comparison` — side-by-side valuation across 2–5 symbols
- `longbridge-fx` — FX spot rates

## File layout

```
skills/longbridge-adr-premium/
└── SKILL.md
```
