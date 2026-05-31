---
name: longbridge-sector-rotation
description: |
  Sector-rotation snapshot across A-share, HK, and US markets — point-in-time multi-factor scoring of momentum, capital flow, and valuation to rank sectors by current cycle strength. For ongoing 6–12 month cycle positioning and allocation recommendations use longbridge-sector-monitor. Triggers: "行业轮动", "板块轮动", "行业动量排名", "强势板块", "弱势板块", "行业资金流", "板块涨幅榜", "行業輪動", "板塊輪動", "行業動量排名", "強勢板塊", "弱勢板塊", "行業資金流", "板塊漲幅榜", "sector rotation", "sector momentum ranking", "leading sector", "lagging sector", "sector capital flow", "sector strength ranking".
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

# longbridge-sector-rotation

Multi-factor sector-rotation scanner. Combines price momentum, capital flow, and valuation to rank industries by cycle leadership across A-share, HK, and US markets.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"当前哪些行业最强"*, *"which sectors are leading?"*, *"目前哪些行業最強"*
- *"A 股行业轮动到哪了"*, *"sector rotation signal for A-shares"*
- *"科技 vs 消费 vs 金融谁在跑赢"*, *"板块动量排名"*
- *"强势板块有哪些"*, *"弱势板块"*, *"leading / lagging sectors"*

For single-stock capital flow route to `longbridge-capital-flow`. For single-stock valuation route to `longbridge-valuation`.

## Workflow

1. **Clarify scope** — ask the user for market (A-share / HK / US) and time window (20-day / 60-day) if not given. Default: A-share, 20-day momentum.
2. **Select representative sector indices or ETFs** for the market:
   - A-share: 申万一级行业指数 (SW L1); common symbols like `801010.SH` (agriculture), `801020.SH` (mining), `801030.SH` (chemicals), `801040.SH` (steel), `801050.SH` (non-ferrous), `801080.SH` (electronics), `801130.SH` (media), `801140.SH` (retail), `801150.SH` (F&B), `801160.SH` (home appliances), `801170.SH` (auto), `801180.SH` (property), `801200.SH` (retail), `801710.SH` (building materials), `801720.SH` (construction), `801730.SH` (utilities), `801740.SH` (defense), `801750.SH` (IT), `801760.SH` (telecom), `801770.SH` (biotech), `801780.SH` (financials), `801790.SH` (brokers).
   - HK: use sector ETFs or HSI sub-indices.
   - US: use SPDR sector ETFs (`XLK.US`, `XLF.US`, `XLE.US`, `XLV.US`, `XLY.US`, `XLI.US`, `XLP.US`, `XLB.US`, `XLRE.US`, `XLU.US`, `XLC.US`).
3. **Fetch kline data** for each sector symbol to compute momentum. Run `longbridge kline --help` to verify exact flags, then call:
   ```bash
   longbridge kline <SYMBOL> --format json   # run --help for available period/count flags
   ```
4. **Compute momentum score** for each sector (LLM in-context):
   - 20-day return: `(close[-1] / close[-20]) - 1`
   - 60-day return: `(close[-1] / close[-60]) - 1`
5. **Fetch capital flow** for top candidates (up to 5 by momentum). Run `longbridge capital --help` to verify flags, then call:
   ```bash
   longbridge capital <SYMBOL> --format json   # run --help for time-series vs snapshot flags
   ```
6. **Fetch industry valuation** for context:
   ```bash
   longbridge industry-valuation <SYMBOL> --format json
   ```
   Run `longbridge industry-valuation --help` if unsure of flags.
7. **Score and rank**: combine momentum (60%), capital flow direction (25%), valuation discount vs history (15%). Sort descending.
8. **Output the rotation table** (see Output section). Cite Longbridge Securities.

## CLI

Run `--help` before calling any subcommand if unsure of flags.

```bash
# Step 1: kline for momentum (repeat per sector symbol); run --help for period/count flags
longbridge kline 801750.SH --format json

# Step 2: capital flow for shortlisted sectors; run --help for time-series vs snapshot flags
longbridge capital 801750.SH --format json

# Step 3: industry valuation for context
longbridge industry-valuation 801750.SH --format json

# Sector ETFs for US market
longbridge kline XLK.US --format json
longbridge capital XLK.US --format json
```

## Output

Render as a ranked table, then a short narrative:

```
Sector Rotation Snapshot — Source: Longbridge Securities
Market: A-share  |  Time: YYYY-MM-DD  |  Momentum window: 20d / 60d

Rank | Sector       | 20d Ret | 60d Ret | Capital Flow | Valuation | Signal
-----|-------------|---------|---------|-------------|-----------|-------
  1  | IT / 信息技术 | +8.2%  | +15.4%  | Net inflow  | Neutral   | ▲ Leader
  2  | Healthcare / 医疗卫生 | +5.1% | +11.2% | Net inflow | Low | ▲ Leader
 ...
 10  | Property / 房地产 | -3.4% | -8.0% | Net outflow | High | ▼ Laggard

Narrative: IT and Healthcare are in the leading quadrant with positive momentum and 
capital inflows. Property and Utilities are lagging. Rotation signal suggests early-cycle 
tilt toward growth sectors.

⚠️ 数据仅供参考，不构成投资建议。/ 數據僅供參考，不構成投資建議。/ For reference only. Not investment advice.
```

## Error handling

| Situation | 简体 | 繁體 | English |
|---|---|---|---|
| `command not found: longbridge` | 回退到 MCP；否则告知用户安装 longbridge-terminal | 回退到 MCP；否則告知用戶安裝 longbridge-terminal | Fall back to MCP; otherwise tell user to install longbridge-terminal. |
| stderr `not logged in` | 请运行 `longbridge auth login` | 請執行 `longbridge auth login` | Run `longbridge auth login`. |
| kline returns < 60 bars | 动量计算退化为可用历史 | 動量計算退化為可用歷史 | Degrade momentum to available history length. |
| Other stderr | 原文显示错误 | 原文顯示錯誤 | Surface verbatim. |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

## Related skills

- Single-stock capital flow → `longbridge-capital-flow`
- Single-stock valuation → `longbridge-valuation`
- Index constituents → `longbridge-constituent`
- Multi-symbol comparison → `longbridge-peer-comparison`
- Market anomalies → `longbridge-anomaly`

## File layout

```
longbridge-sector-rotation/
└── SKILL.md          # prompt-only, no scripts/
```
