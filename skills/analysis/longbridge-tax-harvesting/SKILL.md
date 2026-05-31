---
name: longbridge-tax-harvesting
description: |
  Tax-loss harvesting via Longbridge — identify unrealised-loss positions in the account, evaluate tax benefit of realising losses, suggest substitute securities to maintain market exposure (avoiding wash-sale rules), and track the 30-day wash-sale window. Suited for year-end US tax planning. Triggers: "税损收割", "亏损锁定", "wash sale", "税务规划", "节税", "税务优化", "年末税务", "未实现亏损", "稅損收割", "虧損鎖定", "稅務規劃", "節稅", "年末稅務", "未實現虧損", "tax loss harvesting", "wash sale", "tax planning", "realized loss", "unrealized loss", "tax optimization", "year-end tax", "substitute securities".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: account_read
  requires_login: true
  default_install: true
  requires_mcp: false
  tier: analysis
---

# longbridge-tax-harvesting

Prompt-only analysis skill. Scans account positions for unrealised losses, calculates the potential tax saving from harvesting each loss, flags wash-sale risk, and suggests economically-similar substitute securities. Applies to US-listed securities only (US tax rules). Read-only — does not place orders.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"帮我做税损收割分析"* / *"稅損收割分析"* / *"tax-loss harvesting analysis"*
- *"哪些持仓可以锁定亏损来节税"* / *"哪些持倉可以節稅"* / *"which positions can I harvest for tax losses"*
- *"wash sale 规则是什么"* / *"wash sale 規則"* / *"explain wash sale rule"*
- *"年末税务规划"* / *"年末稅務規劃"* / *"year-end tax planning"*

## Important Notes

- **US tax rules only**: wash-sale rule (IRS Section 1091) applies to US investors trading US-listed securities. Not applicable to HK, A-share, or other markets without equivalent rules.
- **Requires Trade permission**: cost basis data requires `longbridge auth login` with Trade scope.
- **Not tax advice**: always consult a qualified tax professional before executing.

## Workflow

1. Fetch all positions including cost basis (average cost).
2. Fetch current prices for all positions.
3. Compute unrealised gain/loss per position.
4. Filter to positions with unrealised losses.
5. For each loss position, compute potential tax saving (loss × estimated marginal tax rate).
6. Flag wash-sale risk (any purchase of the same or substantially-identical security within 30 days before or after the sale).
7. Suggest substitute securities that maintain similar market exposure.
8. Rank opportunities by tax saving magnitude.

## CLI

Run `longbridge <subcommand> --help` to verify exact flags before calling.

```bash
# Positions with cost basis
longbridge positions --format json

# Current prices (run concurrently for each symbol)
longbridge quote <SYMBOL> --format json
```

## Calculations

| Quantity | Method |
|---|---|
| Unrealised loss | (Current price − Average cost) × Quantity |
| Tax saving estimate | |Unrealised loss| × assumed marginal tax rate (default 37% short-term / 20% long-term) |
| Holding period | Today − position open date (if available); classify short-term (<1yr) or long-term (≥1yr) |
| Wash-sale window | 30 days before + 30 days after the sale date |

## Substitute Securities

When suggesting substitutes to avoid wash-sale, recommend securities that are economically similar but not "substantially identical":

| Original | Example substitute (same sector, different issuer) |
|---|---|
| AAPL (tech) | MSFT, GOOGL, or a tech ETF like QQQ |
| SPY (S&P 500 ETF) | IVV or VOO (different fund family) |
| XOM (energy) | CVX, SLB, or XLE ETF |
| Individual stock | Sector ETF covering the same industry |

Always note that substitute suitability depends on investor-specific factors; these are illustrative only.

## Output template

```
Tax-Loss Harvesting Analysis — Source: Longbridge Securities
Date: <today>  Account: US Securities

[Positions with Unrealised Losses]
Symbol   Cost Basis  Current Price  Unreal. Loss  Hold Period  Tax Saving Est.
TSLA.US  $280.00     $210.00        −$7,000       8 months     ~$2,590 (37% rate)
XOM.US   $120.00     $108.00        −$1,200       14 months    ~$240 (20% rate)

[Tax Harvesting Opportunity Analysis (ranked by potential tax saving)]
1. TSLA.US  若实现亏损 $7,000（示例）→ 预计可节省税款约 $2,590（仅为说明税务亏损收割原理，不构成具体操作建议）
   Substitute reference (for wash-sale avoidance illustration): RIVN.US / LCID.US / DRIV ETF (do not repurchase TSLA within 30 days of any sale)
   ⚠️ Wash-sale risk if TSLA was purchased in last 30 days

2. XOM.US   若实现亏损 $1,200（示例）→ 预计可节省税款约 $240（仅供参考）
   Substitute reference: CVX.US or XLE ETF

[Wash-Sale Warnings]
- Check recent purchase dates; do not repurchase within 30 days of sale.
- Purchasing a call option on the sold stock may also trigger wash-sale.

⚠️ 本分析仅供参考，不构成税务建议或投资建议。以上内容仅为说明税务亏损收割原理，不代表对任何具体操作的建议。请咨询持牌税务顾问。投资决策请结合自身风险承受能力独立判断。/ 本分析僅供參考，不構成稅務建議或投資建議。以上內容僅為說明稅務虧損收割原理，不代表對任何具體操作的建議。請諮詢持牌稅務顧問。/ For reference only. Not tax or investment advice. The above examples are for illustrative purposes only and do not constitute specific trading recommendations. Consult a qualified tax professional. Please make investment decisions independently based on your own risk tolerance.
```

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 回退到 MCP；若也不可用，请安装 longbridge-terminal | 回退到 MCP；若也不可用，請安裝 longbridge-terminal | Fall back to MCP; if unavailable, install longbridge-terminal. |
| stderr `not logged in` | 请运行 `longbridge auth login`（需要 Trade 权限） | 請運行 `longbridge auth login`（需要 Trade 權限） | Run `longbridge auth login` with Trade permission. |
| No US positions | 账户中无美股持仓，税损收割仅适用于美股 | 賬戶中無美股持倉，稅損收割僅適用於美股 | No US positions found; tax-loss harvesting applies to US stocks only. |
| All positions profitable | 当前所有持仓均为浮盈，无税损收割机会 | 當前所有持倉均為浮盈，無稅損收割機會 | All positions are profitable; no harvesting opportunities. |
| Cost basis unavailable | 无法获取持仓成本，请检查账户权限 | 無法獲取持倉成本，請檢查賬戶權限 | Cannot retrieve cost basis; check account permissions. |

## MCP fallback

If `longbridge` CLI is not installed, use MCP tools:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP setup: `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` (`quote` + `trade_read` scopes).

## Related skills

- Portfolio health-check → `longbridge-portfolio-diagnosis`
- Account order history → `longbridge-orders`
- Dividend history → `longbridge-fundamental`

## File layout

```
longbridge-tax-harvesting/
└── SKILL.md          # prompt-only, US accounts only, read-only
```
