---
name: longbridge-northbound-flow
description: |
  Shanghai-Shenzhen-Hong Kong Stock Connect capital flow analysis — tracks northbound (foreign capital buying A-shares) and southbound (mainland capital buying HK stocks) net flows, sector allocation, and AH-premium arbitrage signals. Triggers: "北向资金", "南向资金", "沪深港通", "陆港通", "外资流入", "北向净买入", "沪股通", "深股通", "北向加仓", "北向减仓", "北向資金", "南向資金", "滬深港通", "陸港通", "外資流入", "北向淨買入", "北向加倉", "northbound flow", "southbound flow", "Stock Connect", "Shanghai-Hong Kong connect", "foreign capital inflow", "smart money northbound".
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

# longbridge-northbound-flow

Stock Connect cross-border capital flow analysis. Identifies northbound (foreign → A-share) and southbound (mainland → HK) net flows, sector biases, and AH-premium arbitrage signals.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"今天北向资金净买入多少"*, *"northbound net inflow today"*, *"今天北向資金淨買入多少"*
- *"外资在加仓哪些板块"*, *"which sectors are foreigners buying"*
- *"南向资金今日动向"*, *"southbound flow today"*
- *"陆港通套利机会"*, *"AH premium arbitrage signal"*
- *"北向连续净流入天数"*, *"consecutive northbound inflow days"*

For single-stock capital flow (not cross-border context) route to `longbridge-capital-flow`. For AH premium detail route to `longbridge-ah-premium`.

## Data availability note

Longbridge CLI may not expose a dedicated northbound-fund endpoint. Always run `longbridge capital --help` and `longbridge broker-holding --help` first to discover available flags. If a dedicated northbound command is absent:

1. Use `longbridge capital <SYMBOL> --flow --format json` for proxy signals (large-order / institutional net flow as a northbound proxy).
2. Use `longbridge ah-premium` commands for AH arbitrage context.
3. Inform the user that official daily northbound totals are published by Hong Kong Exchanges (hkex.com.hk) and the Shanghai/Shenzhen Stock Exchanges.

## Workflow

1. **Check available commands**:
   ```bash
   longbridge capital --help
   longbridge broker-holding --help
   ```
2. **If a `northbound` or `stock-connect` subcommand exists**, call it directly:
   ```bash
   longbridge northbound --format json
   longbridge northbound --sector --format json
   ```
3. **Otherwise, build a proxy analysis**:
   a. For key dual-listed A+H stocks (e.g. `601398.SH`/`939.HK`, `600519.SH`, `300750.SZ`), fetch capital flow:
      ```bash
      longbridge capital <SYMBOL> --flow --format json
      ```
   b. Fetch AH premium for cross-market arbitrage signals:
      ```bash
      longbridge calc-index <SYMBOL> --format json
      longbridge ah-premium <SYMBOL> --format json
      ```
      Run `longbridge ah-premium --help` to verify exact flags.
   c. Fetch today's quote for southbound-relevant HK stocks:
      ```bash
      longbridge quote <SYMBOL> --format json
      ```
4. **Aggregate and interpret**:
   - Net inflow direction and magnitude per sector.
   - Consecutive net-buy / net-sell days.
   - Correlation with AH premium compression (northbound buying narrows premium).
5. **Output the flow summary** (see Output section). Cite Longbridge Securities and note if official HKEX data is needed for exact totals.

## CLI

```bash
# Discover available flags first
longbridge capital --help
longbridge broker-holding --help

# Capital flow proxy for key A-share stocks
longbridge capital 601398.SH --flow --format json
longbridge capital 600519.SH --flow --format json

# AH premium (arbitrage reference)
longbridge ah-premium 939.HK --format json

# Southbound proxy: HK blue chips
longbridge capital 700.HK --flow --format json
longbridge quote 700.HK --format json
```

## Output

```
Stock Connect Flow Summary — Source: Longbridge Securities
Date: YYYY-MM-DD

[Northbound (foreign → A-share)]
- Proxy net flow (via large-order analysis): ¥ X bn
- Top sectors with net inflow: IT, Consumer Staples, Healthcare
- Key stocks being accumulated: 600519.SH (Maotai), 300750.SZ (CATL)
- Consecutive net-buy days: N (streak signal)

[Southbound (mainland → HK)]
- Proxy net flow: HK$ X bn
- Key HK stocks with strong mainland interest: 700.HK, 9988.HK

[AH Premium signal]
- 939.HK (ICBC) AH premium: +X% → narrowing → northbound buying signal
- Average AH premium trend: compressing / expanding

[Note] Official daily northbound quotas and exact totals: hkex.com.hk → Market Data → Stock Connect

⚠️ 数据仅供参考，不构成投资建议。/ 數據僅供參考，不構成投資建議。/ For reference only. Not investment advice.
```

## Error handling

| Situation | 简体 | 繁體 | English |
|---|---|---|---|
| `command not found: longbridge` | 回退到 MCP；否则告知安装 longbridge-terminal | 回退到 MCP；否則告知安裝 longbridge-terminal | Fall back to MCP; otherwise tell user to install longbridge-terminal. |
| stderr `not logged in` | 请运行 `longbridge auth login` | 請執行 `longbridge auth login` | Run `longbridge auth login`. |
| No dedicated northbound command | 使用资金流代理分析，并提示用户参考港交所官网获取官方数据 | 使用資金流代理分析，並提示用戶參考港交所官網獲取官方數據 | Use capital-flow proxy; direct user to hkex.com.hk for official totals. |
| Other stderr | 原文显示错误 | 原文顯示錯誤 | Surface verbatim. |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

## Related skills

- AH premium detail → `longbridge-ah-premium`
- Single-stock capital flow → `longbridge-capital-flow`
- Sector rotation → `longbridge-sector-rotation`
- HK broker holdings (CCASS) → `longbridge-flows`
- Real-time quote → `longbridge-quote`

## File layout

```
longbridge-northbound-flow/
└── SKILL.md          # prompt-only, no scripts/
```
