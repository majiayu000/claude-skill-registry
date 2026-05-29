---
name: longbridge-technical
description: |
  Core technical-indicator signal engine for stocks listed in HK / US / A-share / Singapore via Longbridge Securities. Computes and interprets MACD, KDJ, RSI, Bollinger Bands, EMA, ADX, and OBV from OHLCV data; combines multi-dimensional votes (trend / mean-reversion / volume-price) to produce a composite buy / sell / neutral signal. Triggers: "技术指标", "MACD", "KDJ", "RSI", "布林带", "布林线", "EMA", "ADX", "OBV", "金叉", "死叉", "超买", "超卖", "技术分析", "趋势指标", "量价", "技術指標", "布林帶", "技術分析", "超買", "超賣", "technical indicator", "MACD signal", "KDJ overbought", "RSI oversold", "Bollinger Bands", "moving average", "golden cross", "death cross", "technical analysis".
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

# longbridge-technical

Computes seven classic technical indicators from 200 days of OHLCV data and produces a composite buy / sell / neutral signal via a multi-dimensional voting mechanism.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"NVDA MACD 金叉了吗"*, *"TSLA RSI 超买了吗"*, *"700.HK 技术指标怎么看"*
- *"600519.SH 布林带收口"*, *"AAPL 技術分析信號"*, *"ADX 趋势强吗"*
- *"technical analysis for NVDA"*, *"is TSLA overbought on RSI"*, *"MACD signal"*

## Workflow

1. Resolve the symbol to `<CODE>.<MARKET>` format.
2. Fetch 200 daily candles:
   ```bash
   longbridge kline <SYMBOL> --period day --format json   # run --help for available flags
   ```
3. Run the Python analysis below to compute all indicators and their individual votes.
4. Report each indicator's current value and signal, then summarise with the composite vote tally.

## CLI

```bash
longbridge kline NVDA.US   --period day --format json   # run --help for available flags
longbridge kline 700.HK    --period day --format json
longbridge kline 600519.SH --period day --format json
```

Run `longbridge kline --help` to verify current flag names and defaults.

## Python analysis

```python
import pandas as pd, json, sys

data = json.loads(sys.stdin.read())
df = pd.DataFrame(data)
df = df.rename(columns={"open":"o","high":"h","low":"l","close":"c","volume":"v"})
df[["o","h","l","c","v"]] = df[["o","h","l","c","v"]].apply(pd.to_numeric)

votes = {}

# EMA helper
def ema(s, n): return s.ewm(span=n, adjust=False).mean()

# --- MACD (12, 26, 9) ---
ema12 = ema(df["c"], 12); ema26 = ema(df["c"], 26)
macd = ema12 - ema26; signal = ema(macd, 9); hist = macd - signal
votes["MACD"] = +1 if hist.iloc[-1] > 0 and hist.iloc[-1] > hist.iloc[-2] else (
                -1 if hist.iloc[-1] < 0 and hist.iloc[-1] < hist.iloc[-2] else 0)

# --- RSI (14) ---
delta = df["c"].diff(); gain = delta.clip(lower=0); loss = (-delta).clip(lower=0)
avg_g = gain.ewm(alpha=1/14, adjust=False).mean()
avg_l = loss.ewm(alpha=1/14, adjust=False).mean()
rsi = 100 - 100 / (1 + avg_g / avg_l.replace(0, 1e-9))
rsi_last = rsi.iloc[-1]
votes["RSI"] = -1 if rsi_last > 70 else (+1 if rsi_last < 30 else 0)

# --- KDJ (9, 3, 3) ---
low9  = df["l"].rolling(9).min(); high9 = df["h"].rolling(9).max()
rsv   = (df["c"] - low9) / (high9 - low9 + 1e-9) * 100
K = rsv.ewm(alpha=1/3, adjust=False).mean()
D = K.ewm(alpha=1/3, adjust=False).mean()
J = 3*K - 2*D
votes["KDJ"] = +1 if J.iloc[-1] < 20 else (-1 if J.iloc[-1] > 80 else 0)

# --- Bollinger Bands (20, 2) ---
mid = df["c"].rolling(20).mean(); std = df["c"].rolling(20).std()
upper_bb = mid + 2*std; lower_bb = mid - 2*std
c_last = df["c"].iloc[-1]
votes["Bollinger"] = +1 if c_last < lower_bb.iloc[-1] else (
                     -1 if c_last > upper_bb.iloc[-1] else 0)

# --- EMA cross (50 / 200) ---
e50 = ema(df["c"], 50); e200 = ema(df["c"], 200)
votes["EMA_cross"] = +1 if e50.iloc[-1] > e200.iloc[-1] else -1

# --- ADX (14) ---
tr = pd.concat([df["h"]-df["l"], (df["h"]-df["c"].shift()).abs(),
                (df["l"]-df["c"].shift()).abs()], axis=1).max(axis=1)
dm_plus  = (df["h"]-df["h"].shift()).clip(lower=0)
dm_minus = (df["l"].shift()-df["l"]).clip(lower=0)
atr14 = tr.ewm(alpha=1/14, adjust=False).mean()
di_plus  = 100 * dm_plus.ewm(alpha=1/14, adjust=False).mean() / atr14
di_minus = 100 * dm_minus.ewm(alpha=1/14, adjust=False).mean() / atr14
dx = (di_plus - di_minus).abs() / (di_plus + di_minus + 1e-9) * 100
adx = dx.ewm(alpha=1/14, adjust=False).mean()
# ADX > 25 confirms trend; direction from DI cross
votes["ADX"] = +1 if adx.iloc[-1] > 25 and di_plus.iloc[-1] > di_minus.iloc[-1] else (
               -1 if adx.iloc[-1] > 25 and di_minus.iloc[-1] > di_plus.iloc[-1] else 0)

# --- OBV ---
obv = (df["v"] * df["c"].diff().apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))).cumsum()
votes["OBV"] = +1 if obv.iloc[-1] > obv.iloc[-5] else (-1 if obv.iloc[-1] < obv.iloc[-5] else 0)

# --- Composite ---
total = sum(votes.values())
composite = "买入/Buy" if total >= 3 else ("卖出/Sell" if total <= -3 else "持观望/Neutral")

print(f"Composite vote: {total:+d}  →  {composite}")
print(f"  MACD hist={hist.iloc[-1]:.4f}  vote={votes['MACD']:+d}")
print(f"  RSI(14)={rsi_last:.1f}  vote={votes['RSI']:+d}")
print(f"  KDJ J={J.iloc[-1]:.1f}  vote={votes['KDJ']:+d}")
print(f"  Bollinger  vote={votes['Bollinger']:+d}  (price vs bands)")
print(f"  EMA50/200  vote={votes['EMA_cross']:+d}  (50={'above' if e50.iloc[-1]>e200.iloc[-1] else 'below'} 200)")
print(f"  ADX={adx.iloc[-1]:.1f}  DI+={di_plus.iloc[-1]:.1f} DI-={di_minus.iloc[-1]:.1f}  vote={votes['ADX']:+d}")
print(f"  OBV trend  vote={votes['OBV']:+d}")
```

## Output

Present a table of indicator values, individual votes (+1 / 0 / -1), and a composite summary row. End with a one-sentence interpretation in the user's language.

| 指标 / 指標 / Indicator | 当前值 / 當前值 / Value | 信号 / 訊號 / Signal |
|---|---|---|
| MACD | hist 值 | 多/空/中性 |
| RSI(14) | 数值 | 超卖/中性/超买 |
| KDJ J | 数值 | 超卖/中性/超买 |
| Bollinger | 价格位置 | 超卖/中性/超买 |
| EMA 50/200 | 多空排列 | 多头/空头 |
| ADX | 趋势强度 | 趋势/震荡 |
| OBV | 5日趋势 | 流入/流出 |

## Error handling

| Situation | 简体回复 / 繁體回覆 / English reply |
|---|---|
| `command not found: longbridge` | 请安装 longbridge-terminal / 請安裝 longbridge-terminal / Install longbridge-terminal first |
| stderr `not logged in` / `unauthorized` | 请运行 `longbridge auth login` / 請執行 `longbridge auth login` / Run `longbridge auth login` |
| Other stderr | 直接展示错误信息 / 直接顯示錯誤訊息 / Surface error verbatim |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

- `longbridge-kline` — raw OHLCV data and charting
- `longbridge-candlestick` — K-line pattern recognition
- `longbridge-ichimoku` — Ichimoku Cloud system
- `longbridge-capital-flow` — intraday capital-flow signals
