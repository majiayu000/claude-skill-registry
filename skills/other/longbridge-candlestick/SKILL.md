---
name: longbridge-candlestick
description: |
  K-line candlestick pattern recognition for stocks listed in HK / US / A-share / Singapore via Longbridge Securities. Identifies 15 classic patterns (hammer, hanging man, engulfing, doji, morning/evening star, three white soldiers/black crows, shooting star, etc.) from OHLCV data and generates a composite bullish/bearish/neutral signal. Triggers: "K线形态", "蜡烛图形态", "锤子线", "吞没形态", "十字星", "早晨之星", "暮色之星", "三白兵", "三黑鸦", "吊颈线", "射击之星", "K線形態", "蠟燭圖形態", "錘子線", "吞沒形態", "早晨之星", "暮色之星", "candlestick pattern", "hammer", "engulfing", "doji", "morning star", "evening star", "three white soldiers", "shooting star", "K-line pattern".
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

# longbridge-candlestick

Identifies 15 classic K-line candlestick patterns from recent OHLCV data and produces a composite bullish / bearish / neutral signal with per-pattern explanations.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"NVDA 最近有什么 K 线形态"*, *"700.HK 是否出现锤子线"*
- *"TSLA candlestick patterns"*, *"看看吞没形态"*, *"有没有早晨之星"*
- *"600519.SH K線形態分析"*, *"是否出現三白兵"*

## Workflow

1. Resolve the symbol to `<CODE>.<MARKET>` format.
2. Fetch 200 daily candles:
   ```bash
   longbridge kline <SYMBOL> --period day --count 200 --format json
   ```
3. Run the Python analysis below to identify patterns and compute a composite score.
4. Report detected patterns (most recent first), each with date, name, and interpretation. Summarise with a composite signal.

## CLI

```bash
longbridge kline NVDA.US --period day --count 200 --format json
longbridge kline 700.HK  --period day --count 200 --format json
longbridge kline 600519.SH --period day --count 200 --format json
```

Run `longbridge kline --help` to verify current flag names and defaults.

## Python analysis

```python
import pandas as pd, json, sys

data = json.loads(sys.stdin.read())  # list of OHLCV dicts
df = pd.DataFrame(data)
df = df.rename(columns={"open": "o", "high": "h", "low": "l", "close": "c", "volume": "v"})
df[["o","h","l","c","v"]] = df[["o","h","l","c","v"]].apply(pd.to_numeric)

body  = (df["c"] - df["o"]).abs()
rng   = df["h"] - df["l"]
upper = df.apply(lambda r: r["h"] - max(r["c"], r["o"]), axis=1)
lower = df.apply(lambda r: min(r["c"], r["o"]) - r["l"], axis=1)
bull  = df["c"] > df["o"]

signals, score = [], 0

# --- single-bar patterns (check last 5 bars) ---
for i in range(max(0, len(df)-5), len(df)):
    r = df.iloc[i]; b = body.iloc[i]; u = upper.iloc[i]; lo = lower.iloc[i]; rg = rng.iloc[i]
    # Doji
    if b < 0.05 * rg:
        signals.append((df["time"].iloc[i], "十字星/Doji", 0))
    # Hammer (bullish reversal after downtrend)
    elif lo > 2*b and u < 0.1*b and not bull.iloc[i]:
        signals.append((df["time"].iloc[i], "锤子线/Hammer", +1))
    elif lo > 2*b and u < 0.1*b and bull.iloc[i]:
        signals.append((df["time"].iloc[i], "锤子线/Hammer(bullish)", +1))
    # Hanging Man (bearish)
    elif lo > 2*b and u < 0.1*b and i > 0 and df["c"].iloc[i-1] < df["c"].iloc[i]:
        signals.append((df["time"].iloc[i], "吊颈线/Hanging Man", -1))
    # Shooting Star (bearish)
    elif u > 2*b and lo < 0.1*b and bull.iloc[i-1] if i > 0 else False:
        signals.append((df["time"].iloc[i], "射击之星/Shooting Star", -1))
    # Inverted Hammer (bullish)
    elif u > 2*b and lo < 0.1*b:
        signals.append((df["time"].iloc[i], "倒锤线/Inverted Hammer", +1))
    # Marubozu bullish
    elif b > 0.9*rg and bull.iloc[i]:
        signals.append((df["time"].iloc[i], "光头光脚阳线/Bullish Marubozu", +1))
    # Marubozu bearish
    elif b > 0.9*rg and not bull.iloc[i]:
        signals.append((df["time"].iloc[i], "光头光脚阴线/Bearish Marubozu", -1))

# --- two-bar patterns ---
for i in range(max(1, len(df)-5), len(df)):
    p, c_ = df.iloc[i-1], df.iloc[i]
    pb, cb = body.iloc[i-1], body.iloc[i]
    # Bullish engulfing
    if not bull.iloc[i-1] and bull.iloc[i] and c_["o"] < p["c"] and c_["c"] > p["o"]:
        signals.append((df["time"].iloc[i], "看涨吞没/Bullish Engulfing", +2)); score += 2
    # Bearish engulfing
    elif bull.iloc[i-1] and not bull.iloc[i] and c_["o"] > p["c"] and c_["c"] < p["o"]:
        signals.append((df["time"].iloc[i], "看跌吞没/Bearish Engulfing", -2)); score -= 2
    # Piercing line
    elif not bull.iloc[i-1] and bull.iloc[i] and c_["o"] < p["l"] and c_["c"] > (p["o"]+p["c"])/2:
        signals.append((df["time"].iloc[i], "刺透线/Piercing Line", +1)); score += 1
    # Dark cloud cover
    elif bull.iloc[i-1] and not bull.iloc[i] and c_["o"] > p["h"] and c_["c"] < (p["o"]+p["c"])/2:
        signals.append((df["time"].iloc[i], "乌云盖顶/Dark Cloud Cover", -1)); score -= 1

# --- three-bar patterns ---
for i in range(max(2, len(df)-5), len(df)):
    a, b_, c_ = df.iloc[i-2], df.iloc[i-1], df.iloc[i]
    sb = body.iloc[i-1]
    # Morning star
    if not bull.iloc[i-2] and sb < 0.3*(body.iloc[i-2]) and bull.iloc[i] and c_["c"] > (a["o"]+a["c"])/2:
        signals.append((df["time"].iloc[i], "早晨之星/Morning Star", +2)); score += 2
    # Evening star
    elif bull.iloc[i-2] and sb < 0.3*(body.iloc[i-2]) and not bull.iloc[i] and c_["c"] < (a["o"]+a["c"])/2:
        signals.append((df["time"].iloc[i], "暮色之星/Evening Star", -2)); score -= 2
    # Three white soldiers
    elif bull.iloc[i-2] and bull.iloc[i-1] and bull.iloc[i] and c_["c"]>b_["c"]>a["c"]:
        signals.append((df["time"].iloc[i], "三白兵/Three White Soldiers", +2)); score += 2
    # Three black crows
    elif not bull.iloc[i-2] and not bull.iloc[i-1] and not bull.iloc[i] and c_["c"]<b_["c"]<a["c"]:
        signals.append((df["time"].iloc[i], "三黑鸦/Three Black Crows", -2)); score -= 2

# add single-bar scores
for _, _, s in signals:
    score += s

composite = "看多/Bullish" if score >= 2 else ("看空/Bearish" if score <= -2 else "中性/Neutral")
print(f"Composite score: {score}  →  {composite}")
for ts, name, s in signals:
    print(f"  {ts}  {name}  ({'+'if s>=0 else ''}{s})")
```

## Output

Report format (3 languages):

| 字段 / 欄位 / Field | 简体 / 繁體 / English |
|---|---|
| 检测到的形态 | 检测到的形态 / 檢測到的形態 / Detected patterns |
| 综合信号 | 看多 / 看空 / 中性 | 看多 / 看空 / 中性 | Bullish / Bearish / Neutral |
| 解释 | 解释 / 解釋 / Explanation |

Present at most 5 most-recent patterns. Conclude with the composite signal and a one-sentence interpretation.

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
- `longbridge-technical` — indicator-based signals (MACD, RSI, KDJ, etc.)
- `longbridge-ichimoku` — Ichimoku Cloud system
- `longbridge-quote` — real-time price and reference data
