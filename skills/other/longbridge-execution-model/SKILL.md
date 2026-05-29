---
name: longbridge-execution-model
description: |
  Trade execution modelling framework (backtesting analysis only) via Longbridge — covers slippage models (linear / square-root market impact), VWAP/TWAP execution logic, market impact cost estimation (Kyle lambda), volume participation rate (POV) strategy. Helps quant traders build realistic execution assumptions in backtests. Triggers: "执行模型", "滑点模型", "VWAP执行", "TWAP执行", "市场冲击", "执行成本", "成交量参与率", "交易执行", "執行模型", "滑點模型", "VWAP執行", "TWAP執行", "市場冲擊", "執行成本", "交易執行", "execution model", "slippage model", "VWAP", "TWAP", "market impact", "execution cost", "volume participation rate", "Kyle lambda", "square root model", "POV strategy".
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

# longbridge-execution-model

Trade execution modelling framework for backtesting — slippage, VWAP/TWAP, market impact, and volume participation.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger on prompts asking for:

- Slippage or market impact modelling — *"帮我建一个滑点模型"*, *"square root market impact model"*
- VWAP / TWAP execution strategy — *"VWAP执行逻辑"*, *"TWAP slice timing"*
- Volume participation rate (POV) — *"成交量参与率策略"*, *"POV strategy"*
- Kyle lambda or price impact estimation — *"Kyle lambda 估算"*, *"execution cost analysis"*

> This skill is for **backtesting / analysis only** — no live order placement.

## Workflow

1. Identify the symbol and fetch intraday volume profile and tick data.
2. Compute average daily volume (ADV) and intraday volume curve.
3. Apply the requested execution model:
   - **Linear slippage**: `impact = k × (order_size / ADV)`
   - **Square-root impact**: `impact = σ × √(order_size / ADV)`
   - **Kyle lambda (λ)**: estimate from tick data as `ΔP / ΔQ`
   - **VWAP slice**: distribute order proportionally to historical volume curve
   - **TWAP slice**: divide order into equal time-weighted tranches
   - **POV**: cap participation at `p%` of each interval's volume
4. Output estimated cost in bps and recommended execution schedule.
5. Generate Python code skeleton if the user wants a local implementation.

> If unsure of exact flag names, run `longbridge <subcommand> --help` before proceeding.

## CLI

```bash
# 1-minute OHLCV — intraday volume distribution reference
longbridge kline <SYMBOL> --period 1m --count 200 --format json

# Tick-by-tick trades — for Kyle lambda estimation
longbridge trades <SYMBOL> --count 100 --format json
```

## Output structure

```
EXECUTION MODEL REPORT — <SYMBOL>  <Date>

VOLUME PROFILE
ADV (20d):    xx.xM shares
Intraday:     09:30–10:00  xx%  ██████
              10:00–11:00  xx%  ████
              ...

MODEL PARAMETERS
Model:        Square-Root Impact
Order Size:   xx,000 shares (xx% of ADV)
Volatility σ: x.xx% (daily)

COST ESTIMATES
Market Impact: xx bps
Spread Cost:   x bps
Total Cost:    xx bps  (~$xx,xxx on $x.xM order)

EXECUTION SCHEDULE (VWAP)
09:30–10:00   x,xxx shares
10:00–11:00   x,xxx shares
...

KYLE LAMBDA
Estimated λ:  x.xxe-6  ($/share per share traded)
```

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|-----------|---------|---------|---------------|
| Symbol not found | 未找到该代码，请确认市场和格式。 | 找不到該代碼，請確認市場和格式。 | Symbol not found — verify exchange and ticker. |
| Insufficient tick data | 逐笔数据不足，结果仅供参考。 | 逐筆數據不足，結果僅供參考。 | Insufficient tick data — estimates are approximate. |
| `command not found: longbridge` | 请安装 longbridge-terminal 或通过 MCP 连接。 | 請安裝 longbridge-terminal 或透過 MCP 連線。 | Install longbridge-terminal or connect via MCP. |
| `not logged in` | 请运行 `longbridge auth login`。 | 請執行 `longbridge auth login`。 | Run `longbridge auth login`. |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

- `longbridge-kline` — candlestick and OHLCV data
- `longbridge-depth` — orderbook depth and tick trades
- `longbridge-strategy-optimizer` — strategy backtesting and optimisation
- `longbridge-anomaly` — unusual volume and price movements

## File layout

```
skills/longbridge-execution-model/
└── SKILL.md
```
