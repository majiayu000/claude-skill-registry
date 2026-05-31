---
name: longbridge-market-scanner
description: |
  Comprehensive market scanner — combines real-time quotes, capital flow (large/medium/small order distribution), and candlestick data for multi-symbol technical analysis (MACD / RSI / Bollinger Bands computed from OHLCV). Supports batch multi-symbol scanning. Triggers: "行情扫描", "综合行情", "多标的扫描", "行情数据", "实时行情综合", "技术+资金综合", "行情指标", "行情監控", "行情掃描", "綜合行情", "多標的掃描", "技術+資金綜合", "market scanner", "comprehensive quote", "multi-stock scan", "real-time data", "market data query", "technical plus capital flow", "market overview", "batch quote", "technical indicators", "MACD RSI scan".
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

# longbridge-market-scanner

Comprehensive market scanner combining real-time quotes, capital flow (large/medium/small order breakdown), and OHLCV candlestick data to compute technical indicators (MACD / RSI / Bollinger Bands) for one or more symbols in a single pass.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger when the user asks about:

- Multi-symbol comprehensive scan — *"帮我扫描这10只股票的技术面和资金面"*
- Combined technical + capital flow view — *"TSLA 技术指标加资金流向"*
- Real-time multi-metric snapshot — *"综合行情数据"*, *"batch quote with capital flow"*
- MACD / RSI / Bollinger Band status for a stock — *"NVDA RSI 现在多少"*

For a single quote only, prefer `longbridge-quote`. For capital flow only, prefer `longbridge-capital-flow`. For candlestick charting, prefer `longbridge-kline`.

## Workflow

1. Extract all symbols from the prompt; normalise each to `<CODE>.<MARKET>`.
2. Run `longbridge quote` for real-time price/volume snapshot.
3. Run `longbridge capital` for intraday capital flow (large/medium/small net flow).
4. Run `longbridge kline` (daily, last 60 candles) to compute technical indicators:
   - **MACD**: 12/26 EMA diff and signal line (9-day EMA of diff).
   - **RSI**: 14-day RSI.
   - **Bollinger Bands**: 20-day SMA ± 2 standard deviations.
5. Compute the technical indicators from the OHLCV data in-context.
6. Synthesise a per-symbol scan card: price status, capital flow summary, and technical signals.

## CLI

```bash
# Real-time quote
longbridge quote <SYMBOL> --format json

# Intraday capital flow (large / medium / small order net flow)
longbridge capital <SYMBOL> --format json

# Daily candlestick data for technical indicator computation
longbridge kline <SYMBOL> --period day --count 60 --format json
```

> Run `longbridge kline --help` and `longbridge capital --help` to verify current flags.

## Output

For each symbol, emit a scan card:

| Field | 简体 | 繁體 | English |
|---|---|---|---|
| Last price / change | 最新价 / 涨跌幅 | 最新價 / 漲跌幅 | Last / Change % |
| Net capital flow (large orders) | 大单净流入 | 大單淨流入 | Large-order net inflow |
| MACD signal | MACD 信号 | MACD 信號 | MACD signal |
| RSI (14) | RSI(14) | RSI(14) | RSI (14) |
| Bollinger Band position | 布林带位置 | 布林帶位置 | BB position |

Note: Technical indicators are computed in-context from `kline` OHLCV data and are approximations — not sourced from a TA library. For precision, pair with a dedicated TA tool.

## Error handling

| Situation | 简体回复 | 繁體回覆 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 请先安装 longbridge-terminal | 請先安裝 longbridge-terminal | Install longbridge-terminal first |
| `not logged in` | 请运行 `longbridge auth login` | 請執行 `longbridge auth login` | Run `longbridge auth login` |
| `capital` returns empty (pre-market) | 提示盘中资金数据仅交易时间可用 | 提示盤中資金數據僅交易時間可用 | Capital flow available during trading hours only |
| Other stderr | 原样展示，不重试 | 原樣展示，不重試 | Surface verbatim, do not retry |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

| User asks | Route to |
|---|---|
| Single real-time quote | `longbridge-quote` |
| Capital flow only | `longbridge-capital-flow` |
| Candlestick chart / price history | `longbridge-kline` |
| Market anomalies / unusual moves | `longbridge-anomaly` |
| Orderbook depth | `longbridge-depth` |

## File layout

```
longbridge-market-scanner/
└── SKILL.md
```

Prompt-only — no `scripts/`. Technical indicators are computed in-context from kline OHLCV data. Discover current CLI flags via `longbridge <subcommand> --help`.
