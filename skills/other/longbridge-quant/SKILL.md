---
name: longbridge-quant
description: |
  Server-side quantitative indicator runner via Longbridge Securities — execute Pine Script v6 syntax subset against historical K-line data on Longbridge servers without a local Python environment. Supports built-in indicators (MACD, RSI, Bollinger Bands, EMA, SMA, etc.) and custom calculation logic; results returned as JSON. Triggers: "量化指标", "Pine Script", "指标计算", "MACD计算", "RSI计算", "服务端指标", "指标脚本", "量化脚本", "技术指标运行", "量化指標", "指標計算", "MACD計算", "RSI計算", "服務端指標", "指標腳本", "quant indicator", "Pine Script", "indicator calculation", "run indicator", "server-side quant", "MACD script", "RSI calculation", "technical indicator runner", "quant run".
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

# longbridge-quant

Server-side quantitative indicator runner: execute Pine Script v6 syntax subset on historical K-line data via Longbridge Securities servers.

> ⚠️ **Beta feature**: `longbridge quant run` may return `internal server error` if the feature is not yet enabled for your account. Contact Longbridge support to enable quantitative script access if needed.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"帮我算 TSLA 的 MACD"*, *"計算 RSI(14)"*, *"run MACD on NVDA"* → `longbridge quant run` with a built-in `ta.*` function
- *"用 Pine Script 算布林带"*, *"自定义指标脚本"*, *"custom Pine Script indicator"* → pass a script string or pipe a `.pine` file
- *"我想看近一年 EMA20"*, *"EMA 20 for the past year"* → set `--start` / `--end` accordingly

For raw OHLCV data without indicator logic, defer to `longbridge-kline`. For visual chart output, defer to `longbridge-kline`.

## Workflow

1. Identify the symbol, date range, and indicator expression from the prompt.
2. Run `longbridge quant run --help` to check supported functions and flags before constructing the call.
3. Build the `--script` string using Pine Script v6 `ta.*` built-ins (e.g. `ta.macd`, `ta.rsi`, `ta.ema`, `ta.bb`).
4. For multi-indicator requests, wrap them in a list: `"[ta.macd(...), ta.rsi(...)]"`.
5. Return JSON output; summarise the last N rows in a date-sorted table.

## CLI

> Run `longbridge quant run --help` before constructing calls — it is the canonical source for supported functions, operators, and flags.

```bash
# Inspect supported functions and flags first
longbridge quant run --help

# Single built-in indicator — 20-day EMA
longbridge quant run AAPL.US --start 2025-01-01 --end 2025-12-31 \
  --script "ta.ema(close, 20)" --format json

# RSI(14) for a date range
longbridge quant run TSLA.US --start 2026-01-01 --end 2026-04-30 \
  --script "ta.rsi(close, 14)" --format json

# Multi-indicator: MACD + RSI combined
longbridge quant run NVDA.US --start 2025-01-01 --end 2026-01-01 \
  --script "[ta.macd(close,12,26,9), ta.rsi(close,14)]" --format json

# Bollinger Bands
longbridge quant run 700.HK --start 2025-06-01 --end 2025-12-31 \
  --script "ta.bb(close, 20, 2)" --format json

# Pipe a custom Pine Script file
cat myindicator.pine | longbridge quant run AAPL.US \
  --start 2025-01-01 --end 2025-12-31 --format json
```

**Note**: `longbridge quant run` uses a Pine Script v6 syntax subset. Not all Pine Script v6 functions are available — check `--help` for the full supported function and operator list.

## Output

Present results as a date-sorted table with indicator columns. Example layout:

| Date | EMA(20) | RSI(14) |
|------|---------|---------|
| 2025-12-31 | 248.32 | 61.4 |
| 2025-12-30 | 247.89 | 59.8 |

- Always show the date range queried and the symbol.
- For multi-output indicators (e.g. MACD returns MACD line / signal / histogram), show all components as separate columns.
- Cite **Longbridge Securities** as the data source.

## Error handling

| Situation | 简体回复 / 繁体回复 / English reply |
|-----------|--------------------------------------|
| `command not found: longbridge` | 请安装 longbridge-terminal / 請安裝 longbridge-terminal / Install longbridge-terminal first; fall back to MCP if configured. |
| `unsupported function` / `parse error` | 指定函数不在支持列表，请运行 `--help` 查看可用函数 / 指定函數不在支援清單，請執行 `--help` 查看可用函數 / Function not supported — run `longbridge quant run --help` for the full list. |
| `not logged in` / `unauthorized` | 运行 `longbridge auth login` / 執行 `longbridge auth login` / Run `longbridge auth login`. |
| Empty result | 指定日期范围内无数据 / 指定日期範圍內無數據 / No data for the requested date range. |
| Other stderr | Surface verbatim — never silently retry. |

## MCP fallback

When the CLI binary is missing, fall back via the equivalent MCP tool:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

If the tool name does not resolve, ask the user to install the CLI.

## Related skills

| Skill | Why |
|-------|-----|
| `longbridge-kline` | Raw OHLCV candlestick data without indicator computation. |
| `longbridge-anomaly` | Pre-computed unusual price/volume alerts on the server. |
| `longbridge-capital-flow` | Intraday money-flow signals complementing technical indicators. |

## File layout

```
longbridge-quant/
└── SKILL.md          # prompt-only, no scripts/
```
