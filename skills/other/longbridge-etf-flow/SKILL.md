---
name: longbridge-etf-flow
description: |
  US ETF capital-flow analysis via Longbridge Securities — tracks institutional money migration via ETF creation/redemption changes, sector breadth signals, and thematic momentum. Analyses major SPDR sector ETFs (XLK / XLF / XLE / XLV etc.) for net inflow / outflow to gauge industry rotation and risk-appetite shifts. Triggers: "ETF资金流", "ETF流向", "美国ETF", "板块ETF", "XLK", "XLF", "XLE", "机构资金迁移", "行业轮动信号", "ETF資金流", "ETF流向", "美國ETF", "板塊ETF", "機構資金遷移", "ETF flow", "US ETF flow", "sector ETF", "SPDR", "institutional flow", "sector rotation signal", "ETF inflow outflow", "fund flow".
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

# longbridge-etf-flow

US ETF capital-flow analysis — sector rotation signals from ETF inflows and outflows.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger on prompts asking about:

- ETF-level capital flows — *"XLK 资金流向"*, *"SPDR ETF flow"*, *"哪个板块 ETF 资金在流入"*
- Sector rotation signals via ETFs — *"行业轮动信号"*, *"sector rotation signal"*
- Risk appetite from ETF volume — *"避险情绪"*, *"risk-on / risk-off via ETF"*
- Thematic momentum — *"科技 ETF 动量"*, *"tech ETF momentum"*

For individual stock capital flow defer to `longbridge-capital-flow`. For index constituents defer to `longbridge-constituent`.

## Common sector ETF reference

| Sector | ETF | 板块（简体） | 板塊（繁體） |
|--------|-----|------------|------------|
| Technology | XLK.US | 科技 | 科技 |
| Financials | XLF.US | 金融 | 金融 |
| Energy | XLE.US | 能源 | 能源 |
| Health Care | XLV.US | 医疗 | 醫療 |
| Consumer Disc. | XLY.US | 非必需消费 | 非必需消費 |
| Consumer Staples | XLP.US | 必需消费 | 必需消費 |
| Industrials | XLI.US | 工业 | 工業 |
| Materials | XLB.US | 材料 | 材料 |
| Real Estate | XLRE.US | 房地产 | 房地產 |
| Utilities | XLU.US | 公用事业 | 公用事業 |
| Communication | XLC.US | 通信 | 通信 |

> If unsure of exact flag names, run `longbridge <subcommand> --help` before proceeding.

## Workflow

1. Identify which ETF(s) the user is interested in; default to all 11 SPDR sectors if none specified.
2. Fetch real-time quote and volume for each ETF.
3. Fetch recent daily OHLCV to compute 5-day / 20-day volume trend.
4. Fetch intraday capital flow if available.
5. Rank ETFs by net inflow signal; identify top-3 inflow and top-3 outflow sectors.
6. Synthesise sector rotation narrative and risk-appetite assessment.

## CLI

```bash
# Real-time quote + volume
longbridge quote <ETF_SYMBOL> --format json

# Recent price + volume history (20 trading days)
longbridge kline <ETF_SYMBOL> --period day --count 20 --format json

# Intraday capital flow
longbridge capital <ETF_SYMBOL> --format json
```

## Output

1. Ranked table: ETF | Sector | Today's change | Volume vs 20-day avg | Flow signal
2. Top inflow / outflow sectors highlighted.
3. Narrative: what the rotation pattern implies for risk appetite and market leadership.

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|-----------|---------|---------|---------------|
| ETF symbol not found | 未找到该 ETF，请确认代码（如 XLK.US）。 | 找不到該 ETF，請確認代碼（如 XLK.US）。 | ETF not found — verify the ticker (e.g. XLK.US). |
| Capital flow data unavailable | 资金流数据暂不可用，仅展示价格和成交量。 | 資金流數據暫不可用，僅展示價格和成交量。 | Capital flow data unavailable — showing price and volume only. |
| `command not found: longbridge` | 请安装 longbridge-terminal 或通过 MCP 连接。 | 請安裝 longbridge-terminal 或透過 MCP 連線。 | Install longbridge-terminal or connect via MCP. |
| `not logged in` | 请运行 `longbridge auth login`。 | 請執行 `longbridge auth login`。 | Run `longbridge auth login`. |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

- `longbridge-capital-flow` — intraday capital flow for a single stock
- `longbridge-constituent` — index / ETF constituent stocks
- `longbridge-sector-rotation` — macro-driven sector rotation framework

## File layout

```
skills/longbridge-etf-flow/
└── SKILL.md
```
