---
name: longbridge-ichimoku
description: |
  Ichimoku Cloud (一目均衡表) five-line system signal engine for stocks listed in HK / US / A-share / Singapore via Longbridge Securities. Computes Tenkan-sen, Kijun-sen, Senkou Span A/B, and Chikou Span from OHLCV data; generates price-vs-cloud position, line-cross signals, and full trend-confirmation scores. Triggers: "一目均衡表", "一目云", "云图", "转折线", "基准线", "先行带", "迟行线", "云上", "云下", "一目均衡表", "一目雲", "雲圖", "轉折線", "基準線", "先行帶", "遲行線", "ichimoku", "ichimoku cloud", "tenkan sen", "kijun sen", "senkou span", "chikou span", "cloud breakout".
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

# longbridge-ichimoku

Computes the full Ichimoku Cloud five-line system from 200 days of OHLCV data and produces bullish / bearish / neutral signals with per-component interpretation.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"NVDA 一目云位置"*, *"700.HK 是否在云上方"*, *"转折线有没有上穿基准线"*
- *"TSLA ichimoku signal"*, *"is AAPL above the cloud"*, *"cloud breakout"*
- *"600519.SH 雲圖分析"*, *"先行帶是否扩张"*, *"遲行線確認"*

## Workflow

1. Resolve the symbol to `<CODE>.<MARKET>` format.
2. Fetch 200 daily candles (need ≥ 52 bars for Senkou Span B):
   ```bash
   longbridge kline <SYMBOL> --period day --count 200 --format json
   ```
3. Run the Python analysis below to compute all five lines and derive signals.
4. Report each component's value and signal, then summarise with a composite conclusion.

## CLI

```bash
longbridge kline NVDA.US   --period day --count 200 --format json
longbridge kline 700.HK    --period day --count 200 --format json
longbridge kline 600519.SH --period day --count 200 --format json
```

Run `longbridge kline --help` to verify current flag names and defaults.

## Python analysis

```python
import pandas as pd, json, sys

data = json.loads(sys.stdin.read())
df = pd.DataFrame(data)
df = df.rename(columns={"open":"o","high":"h","low":"l","close":"c","volume":"v"})
df[["o","h","l","c","v"]] = df[["o","h","l","c","v"]].apply(pd.to_numeric)
df = df.reset_index(drop=True)

def midpoint(h, l, n):
    return (h.rolling(n).max() + l.rolling(n).min()) / 2

# --- Five lines ---
tenkan  = midpoint(df["h"], df["l"], 9)           # 转折线 / 轉折線 / Tenkan-sen
kijun   = midpoint(df["h"], df["l"], 26)           # 基准线 / 基準線 / Kijun-sen
span_a  = ((tenkan + kijun) / 2).shift(26)         # 先行带A (shifted forward 26)
span_b  = midpoint(df["h"], df["l"], 52).shift(26) # 先行带B (shifted forward 26)
chikou  = df["c"].shift(-26)                        # 迟行线 (shifted back 26)

i = len(df) - 1  # latest bar index
c_now   = df["c"].iloc[i]
t_now   = tenkan.iloc[i]
k_now   = kijun.iloc[i]
sa_now  = span_a.iloc[i]
sb_now  = span_b.iloc[i]
# Chikou vs price 26 bars ago
chikou_ref = df["c"].iloc[i - 26] if i >= 26 else None

cloud_top    = max(sa_now, sb_now) if pd.notna(sa_now) and pd.notna(sb_now) else None
cloud_bottom = min(sa_now, sb_now) if pd.notna(sa_now) and pd.notna(sb_now) else None

signals = []

# 1. Price vs Cloud
if cloud_top and c_now > cloud_top:
    signals.append(("价格在云上 / 價格在雲上 / Price above cloud", +2))
elif cloud_bottom and c_now < cloud_bottom:
    signals.append(("价格在云下 / 價格在雲下 / Price below cloud", -2))
else:
    signals.append(("价格在云内 / 價格在雲內 / Price inside cloud", 0))

# 2. Tenkan / Kijun cross
if pd.notna(t_now) and pd.notna(k_now):
    t_prev = tenkan.iloc[i-1]; k_prev = kijun.iloc[i-1]
    if t_now > k_now and t_prev <= k_prev:
        signals.append(("转折线上穿基准线(买入) / 轉折線上穿基準線 / Tenkan crosses above Kijun (buy)", +2))
    elif t_now < k_now and t_prev >= k_prev:
        signals.append(("转折线下穿基准线(卖出) / 轉折線下穿基準線 / Tenkan crosses below Kijun (sell)", -2))
    elif t_now > k_now:
        signals.append(("转折线 > 基准线(多头排列) / 轉折線>基準線 / Tenkan > Kijun (bullish)", +1))
    else:
        signals.append(("转折线 < 基准线(空头排列) / 轉折線<基準線 / Tenkan < Kijun (bearish)", -1))

# 3. Cloud color (span_a vs span_b)
if pd.notna(sa_now) and pd.notna(sb_now):
    if sa_now > sb_now:
        signals.append(("云为阳色(看多) / 雲為陽色 / Green cloud (bullish)", +1))
    else:
        signals.append(("云为阴色(看空) / 雲為陰色 / Red cloud (bearish)", -1))

# 4. Chikou confirmation
if chikou_ref is not None and pd.notna(chikou_ref):
    chikou_now = df["c"].iloc[i]  # chikou = current close plotted 26 back
    if chikou_now > chikou_ref:
        signals.append(("迟行线确认多头 / 遲行線確認多頭 / Chikou confirms bullish", +1))
    else:
        signals.append(("迟行线确认空头 / 遲行線確認空頭 / Chikou confirms bearish", -1))

# 5. Price vs Tenkan / Kijun
if pd.notna(t_now) and c_now > t_now:
    signals.append(("价格 > 转折线(短期支撑) / Price > Tenkan / short-term support", +1))
if pd.notna(k_now) and c_now > k_now:
    signals.append(("价格 > 基准线(中期支撑) / Price > Kijun / medium-term support", +1))

total = sum(s for _, s in signals)
composite = "强烈看多/Strong Bullish" if total >= 5 else (
            "看多/Bullish"            if total >= 2 else (
            "看空/Bearish"            if total <= -2 else (
            "强烈看空/Strong Bearish" if total <= -5 else "中性/Neutral")))

print(f"Ichimoku composite: {total:+d}  →  {composite}")
print(f"  Tenkan-sen (转折线):  {t_now:.2f}")
print(f"  Kijun-sen  (基准线):  {k_now:.2f}")
print(f"  Senkou A   (先行带A): {sa_now:.2f}" if pd.notna(sa_now) else "  Senkou A: N/A")
print(f"  Senkou B   (先行带B): {sb_now:.2f}" if pd.notna(sb_now) else "  Senkou B: N/A")
print(f"  Cloud top: {cloud_top:.2f}  bottom: {cloud_bottom:.2f}" if cloud_top else "  Cloud: N/A")
print(f"  Current price: {c_now:.2f}")
for label, s in signals:
    print(f"    [{'+' if s>0 else ('-' if s<0 else ' ')}{abs(s)}] {label}")
```

## Output

Report the five line values and signal table, then a composite conclusion. Example structure:

| 指标 / 指標 / Component | 值 / 值 / Value | 信号 / 訊號 / Signal |
|---|---|---|
| 转折线 Tenkan-sen | 数值 | — |
| 基准线 Kijun-sen | 数值 | — |
| 先行带 A Senkou A | 数值 | — |
| 先行带 B Senkou B | 数值 | 云色 |
| 迟行线 Chikou Span | 当前收盘 | 确认多/空 |
| 价格 vs 云 | 高于/低于/在内 | +2 / -2 / 0 |
| 综合信号 | — | 看多/看空/中性 |

Cite **Longbridge Securities** / **数据来源:长桥证券** / **數據來源:長橋證券**.

## Error handling

| Situation | 简体回复 / 繁體回覆 / English reply |
|---|---|
| `command not found: longbridge` | 请安装 longbridge-terminal / 請安裝 longbridge-terminal / Install longbridge-terminal first |
| stderr `not logged in` / `unauthorized` | 请运行 `longbridge auth login` / 請執行 `longbridge auth login` / Run `longbridge auth login` |
| Fewer than 52 bars returned | 告知数据不足，需要至少 52 根 K 线 / 需至少 52 根 K 線 / Need at least 52 bars for Senkou B |
| Other stderr | 直接展示错误信息 / 直接顯示錯誤訊息 / Surface error verbatim |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

- `longbridge-kline` — raw OHLCV data and charting
- `longbridge-technical` — MACD / RSI / KDJ / Bollinger indicator signals
- `longbridge-candlestick` — K-line pattern recognition
- `longbridge-capital-flow` — intraday capital-flow signals
