---
name: longbridge-sector-monitor
description: |
  Sector rotation continuous monitoring via Longbridge — 6–12 month trend tracking across economic cycles (recovery / overheating / stagflation / recession), identifies leading sectors per cycle phase (recovery→consumer discretionary/financials, overheating→energy/materials, stagflation→healthcare/staples, recession→utilities/bonds), and outputs sector allocation recommendations. Differs from longbridge-sector-rotation which gives a point-in-time snapshot. Triggers: "行业监控", "板块监控", "行业跟踪", "经济周期", "顺周期", "逆周期", "行业配置", "周期行业", "防御行业", "行业仓位", "行業監控", "板塊監控", "行業追蹤", "經濟週期", "順週期", "逆週期", "行業配置", "週期行業", "防禦行業", "sector monitor", "sector tracking", "economic cycle", "defensive sector", "cyclical sector", "sector allocation", "late cycle", "early cycle", "sector positioning".
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

# longbridge-sector-monitor

Prompt-only analysis skill. Tracks sector rotation over 6–12 months by locating the current economic cycle phase and mapping it to historically favoured sectors. Provides ongoing allocation recommendations rather than a point-in-time snapshot.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"当前经济周期在哪个阶段"*, *"where are we in the economic cycle"*, *"當前經濟週期在哪個階段"*
- *"行业配置建议"*, *"sector allocation recommendation"*, *"行業配置建議"*
- *"现在应该超配哪些行业"*, *"which sectors to overweight now"*
- *"防御性板块 vs 顺周期板块"*, *"defensive vs cyclical sectors"*
- *"行业轮动跟踪"*, *"sector rotation tracking over 6 months"*

For a quick point-in-time sector strength ranking use `longbridge-sector-rotation`. For single-stock capital flow use `longbridge-capital-flow`.

## Economic cycle framework

| Phase | 阶段 | Key macro signals | Favoured sectors |
|---|---|---|---|
| Recovery / 复苏 | GDP turning up, unemployment falling, rates low | Consumer discretionary, Financials, Real estate |
| Overheating / 过热 | GDP above trend, inflation rising, rates rising | Energy, Materials, Industrials |
| Stagflation / 滞涨 | Growth slowing, inflation still high | Healthcare, Consumer staples, Utilities |
| Recession / 衰退 | GDP contracting, unemployment rising | Utilities, Consumer staples, Government bonds proxy |

## CLI

Run `longbridge <subcommand> --help` to verify exact flags before use:

```bash
# Index constituents to identify sector universe
longbridge constituent <INDEX> --format json

# 120-day kline for sector ETFs / indices (trend tracking)
longbridge kline <SECTOR_ETF> --period day --count 120 --format json

# Capital flow for individual sector symbols
longbridge capital <SYMBOL> --flow --format json

# If unsure about flags:
longbridge constituent --help
longbridge kline --help
longbridge capital --help
```

## Workflow

1. **Clarify scope** — market (A-share / HK / US) and horizon (6-month / 12-month). Default: A-share, 6-month.
2. **Select sector proxies**:
   - A-share: 申万一级行业指数 (e.g. `801750.SH` IT, `801780.SH` Financials, `801730.SH` Utilities)
   - US: SPDR ETFs (`XLK.US`, `XLF.US`, `XLE.US`, `XLV.US`, `XLY.US`, `XLP.US`, `XLU.US`, `XLB.US`)
   - HK: HSI sector sub-indices or representative ETFs
3. **Fetch 120-day kline** for each sector proxy:
   ```bash
   longbridge kline <SECTOR> --period day --count 120 --format json
   ```
4. **Compute trend metrics** in-LLM:
   - 20d, 60d, 120d returns for each sector
   - Trend direction: 20d MA vs 60d MA (above = uptrend)
5. **Fetch capital flow** for top and bottom 3 sectors by 60d return:
   ```bash
   longbridge capital <SECTOR> --flow --format json
   ```
6. **Locate economic cycle phase** using trend patterns and macro context provided by the user (or inferred from sector behaviour):
   - Broad market trend + sector leadership pattern → infer phase
7. **Map to allocation recommendation**: overweight sectors favoured in current phase; underweight laggards.
8. **Output monitoring report**; cite **Longbridge Securities**; end with disclaimer.

## Output

```
Sector Monitor Report — Source: Longbridge Securities
Market: {market}  |  Horizon: {6M / 12M}  |  Date: {date}

[Economic cycle positioning]
Current phase estimate: {Recovery / Overheating / Stagflation / Recession}
Basis: {trend patterns, sector leadership, user-provided macro context}

[Sector trend table (120-day window)]
Sector            | 20d Ret | 60d Ret | 120d Ret | Trend    | Capital Flow
──────────────────|---------|---------|----------|----------|--------------
{Sector A}        | +X%     | +Y%     | +Z%      | Uptrend  | Net inflow
{Sector B}        | ...
...

[Allocation recommendation]
Overweight:  {Sector 1}, {Sector 2}  — favoured in {phase} phase
Neutral:     {Sector 3}, {Sector 4}
Underweight: {Sector 5}, {Sector 6}  — typically lag in {phase} phase

[Cycle transition watch]
Next likely phase: {phase}  |  Trigger signals to watch: {signals}

⚠️ 以上分析仅供参考，不构成投资建议。/ 以上分析僅供參考，不構成投資建議。/ For reference only. Not investment advice.
```

## Error handling

| Situation | 简体中文回复 | 繁體中文 / English |
|---|---|---|
| `command not found: longbridge` | 回退到 MCP；如 MCP 也不可用，请安装 longbridge-terminal。 | 回退到 MCP；如也不可用，請安裝 longbridge-terminal。/ Fall back to MCP; if also unavailable, install longbridge-terminal. |
| stderr `not logged in` | 请运行 `longbridge auth login` 登录。 | 請執行 `longbridge auth login`。/ Run `longbridge auth login`. |
| kline returns < 60 bars | 趋势分析退化为可用历史，注明数据长度不足。 | 趨勢分析退化為可用歷史，注明數據長度不足。/ Degrade to available history length; note limitation. |
| Other stderr | 直接显示原始错误，不静默重试。 | 顯示原始錯誤。/ Surface verbatim — do not retry silently. |

## MCP fallback

If `longbridge` CLI is not installed, use MCP tools:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP setup: `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` (`quote` scope).

## Related skills

- Point-in-time sector strength snapshot → `longbridge-sector-rotation`
- Single-stock capital flow → `longbridge-capital-flow`
- Index constituents → `longbridge-constituent`
- Market temperature & trading session → `longbridge-market-temp`

## File layout

```
longbridge-sector-monitor/
└── SKILL.md   # prompt-only, no scripts/
```
