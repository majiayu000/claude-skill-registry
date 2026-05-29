---
name: longbridge-seasonality
description: |
  Seasonality and calendar-effect strategy via Longbridge Securities — uses historical OHLCV data to compute month-of-year returns (January Effect), day-of-week returns (Monday / Friday effect), pre/post-holiday drift, and earnings-season effect; identifies statistically significant patterns and generates trading signals. Triggers: "季节性", "日历效应", "月份效应", "周一效应", "年初效应", "节假日效应", "财报季效应", "时间模式", "季節性", "日曆效應", "月份效應", "周一效應", "年初效應", "節假日效應", "財報季效應", "seasonality", "calendar effect", "January effect", "day of week effect", "holiday effect", "earnings season effect", "seasonal pattern", "time series anomaly", "月度效应", "月度效應", "monthly seasonality".
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

# longbridge-seasonality

Identifies calendar-driven return anomalies for a stock by analysing multi-year historical OHLCV data. Computes average returns grouped by month, day-of-week, and proximity to known events (holidays, earnings seasons) to surface statistically significant seasonal patterns.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- User asks "does AAPL tend to rise in January?", "周一买还是周五买", "节假日前后涨跌规律", "NVDA 财报季行情", "月份效应", "seasonality analysis".

## Workflow

1. Fetch 5 years of daily candles (≈ 1260 trading days):
   `longbridge kline <SYMBOL> --period day --count 1260 --format json`
2. Compute daily log-returns from `close` column.
3. Group by:
   - **Month effect**: average return per calendar month (Jan–Dec); flag months with |avg| > 1 std of all monthly averages.
   - **Day-of-week effect**: parse `time` field for weekday; average return Mon–Fri; flag extremes.
   - **Holiday drift**: identify the 3 trading days before/after major holidays (Christmas, Chinese New Year, Golden Week for HK/CN); compute average drift window.
   - **Earnings season**: roughly Q1 (Jan–Feb), Q2 (Apr–May), Q3 (Jul–Aug), Q4 (Oct–Nov) for US stocks; compute average return in those windows vs non-earnings months.
4. Summarise each effect as: (a) average return, (b) win rate (% positive days), (c) signal direction (Bullish/Bearish/Neutral).
5. Output a summary table + top-3 actionable patterns.

Run `longbridge kline --help` to confirm flag names before calling.

## CLI

```bash
longbridge kline --help

# 5-year daily history
longbridge kline <SYMBOL> --period day --count 1260 --format json
```

JSON rows: `{time, open, high, low, close, volume}`. Parse `time` for year/month/weekday grouping.

## Output

| Effect | 简体 | 繁體 | English |
|---|---|---|---|
| Month effect | 月份效应 | 月份效應 | Month-of-year effect |
| Day-of-week | 星期效应 | 星期效應 | Day-of-week effect |
| Holiday drift | 节假日效应 | 節假日效應 | Holiday drift |
| Earnings season | 财报季效应 | 財報季效應 | Earnings season effect |
| Signal | 信号 | 訊號 | Signal |

Output: one table per effect (Month / DOW / Holiday / Earnings), then a "Top Patterns" section with concrete entry/exit rules. Cite **Longbridge Securities** / **数据来源：长桥证券** / **數據來源：長橋證券**.

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 回退到 MCP 或提示安装 longbridge-terminal | 回退到 MCP 或提示安裝 longbridge-terminal | Fall back to MCP or install longbridge-terminal |
| `not logged in` / `unauthorized` | 请运行 `longbridge auth login` | 請執行 `longbridge auth login` | Run `longbridge auth login` |
| Fewer than 250 candles returned | 数据不足以计算季节性，建议选择历史更长的标的 | 數據不足，建議選擇歷史更長的標的 | Insufficient data; choose a more liquid / longer-history symbol |
| Other stderr | 直接显示原始错误 | 直接顯示原始錯誤 | Surface verbatim |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

- `longbridge-kline` — raw candle data
- `longbridge-calendar` — forward earnings dates and holidays
- `longbridge-volatility-strategy` — vol regime complement to seasonality

## File layout

```
longbridge-seasonality/
└── SKILL.md
```
