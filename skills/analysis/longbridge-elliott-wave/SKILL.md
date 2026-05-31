---
name: longbridge-elliott-wave
description: Elliott Wave technical timing analysis for individual stocks. Identifies current wave cycle position (impulse 5-wave / corrective ABC), validates with Fibonacci ratios, confirms with momentum indicators (MACD, RSI, volume divergence), and evaluates market environment per market (HK / US / A-share / SGX). Outputs structured natural language report with Fibonacci price zones and actionable reference. Triggers on "波浪分析", "艾略特波浪", "Elliott Wave", "波浪周期", "wave analysis", "技术择时", "technical timing", stock ticker + wave/timing keywords, "现在是第几浪", "处于哪个波浪", "波浪判断", "波浪理论", "浪形分析", "波浪择时".
---

# Elliott Wave Analysis

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

Technical timing skill that positions a stock within its Elliott Wave cycle, confirms with momentum, and contextualizes with market environment. Three modules run sequentially; each result feeds the next.

## When to Use

| Trigger | Example |
|---------|---------|
| Wave position inquiry | "TSLA.US 现在是第几浪" / "700.HK波浪分析" |
| Technical timing | "NVDA.US 技术择时" / "苹果波浪择时" |
| Pre-trade check | "我想买，波浪角度看合适吗" |
| General wave theory | "帮我做个艾略特波浪分析" |

**Do not trigger if:** the user requests fundamental analysis, earnings preview, or valuation — use the relevant skill instead.

## Data Sources

All price data comes from the Longbridge CLI. **Before the first invocation of any
`longbridge` subcommand in a session, run `longbridge <subcommand> --help` to confirm
available flags, required arguments, and symbol format.** Do this for every distinct
subcommand you use (e.g. `kline`, `quote`, `capital`, `news`).

### What to fetch

| Data | Purpose | Minimum |
|------|---------|---------|
| Daily K-line | Primary wave analysis | ≥ 250 bars, JSON |
| Weekly K-line | Higher-degree wave context | ~100 bars, JSON |
| Current quote | Latest price, range | JSON |
| Capital flow | Southbound / Northbound flow (if available) | JSON |

### Symbol validation

Not all ticker-like strings are valid on Longbridge — **index codes (e.g. SPX, HSI) are
not tradable securities and will return `invalid symbol`.** When you need broad-market
data, use a tracking ETF instead (e.g. SPY.US for S&P 500, 2800.HK for HSI). If
uncertain whether a symbol is supported, test with a small kline query first and handle
the error gracefully.

### Practical notes

- Always redirect CLI output to a temp file (e.g. `/tmp/kline_day.json`) — the CLI may
  append version notices to stdout that break JSON parsing.
- Use `--format json` on every call so output is machine-readable.
- Market environment data not available in CLI → use Web Search (see Module C).

## Workflow

### Step 1 — Pre-flight checks

Before analysis, verify:
1. Run `longbridge kline --help` and `longbridge news --help` if you haven't already in this session.
2. Fetch ≥ 300 daily candles for the target symbol in JSON format; save to a temp file.
3. Count returned bars. **If < 250 bars → refuse analysis**, reply:
   - CN: "历史数据不足250根日K，波浪计数不可靠，建议选择数据更充足的标的。"
   - EN: "Fewer than 250 daily candles available — wave count unreliable."
4. Fetch the 5 most recent news items for the symbol. **If recent suspension/resumption or confirmed fraud/delisting → refuse.**
5. For A-share: if ticker has "ST" prefix → refuse.

### Step 2 — Module A: Wave Cycle Identification

Run `scripts/signal_engine.py` to compute swing points, wave count, and Fibonacci zones:

```bash
python3 scripts/signal_engine.py --kline /tmp/kline_day.json --symbol SYMBOL
```

The script outputs JSON with:
- `stage`: wave stage label (see Stage Labels below)
- `count_a` / `count_b`: two candidate count scenarios
- `agreed`: true if both counts give the same stage conclusion
- `fib_zones`: dict of Fibonacci price levels
- `swings`: list of recent swing points

**If `agreed` is false → output "结构待确认 / Structure Unconfirmed", do not force a stage label.**

**Stage Labels** (translate to user's language):

| Internal | Simplified CN | Traditional CN | English |
|----------|--------------|----------------|---------|
| `impulse_early` | 上升初段 | 上升初段 | Early Impulse |
| `impulse_wave3` | 主升段（③浪） | 主升段（③浪） | Wave 3 Advance |
| `impulse_late` | 上升末段（⑤浪） | 上升末段（⑤浪） | Late Impulse (Wave 5) |
| `top_zone` | 顶部区域 | 頂部區域 | Top Zone |
| `corrective_abc` | 调整段（ABC） | 調整段（ABC） | ABC Correction |
| `bottom_zone` | 底部区域 | 底部區域 | Bottom Zone |
| `unconfirmed` | 结构待确认 | 結構待確認 | Structure Unconfirmed |

### Step 3 — Module B: Momentum Confirmation

Compute from the same daily K-line data (all calculable from OHLCV, no extra API calls):

| Indicator | Parameters | Signal to Report |
|-----------|-----------|-----------------|
| MACD | 12/26/9 EMA | Line vs signal, histogram direction, **divergence vs price** |
| RSI | 14-period | Level (>70 overbought / <30 oversold), **divergence vs price** |
| Volume | Raw volume | Wave 3 highest volume? Wave 5 / C-wave volume vs prior wave |
| MA trend | 20 / 50 SMA | Price above/below each MA; MA slope direction |

**Critical divergence signals (must flag explicitly):**
- Wave 5 top + MACD/RSI bearish divergence → **high alert, potential reversal**
- C-wave bottom + MACD/RSI bullish divergence → **potential bottom**
- Wave 3 + volume expansion → **confirms wave 3 validity**

Each indicator: state its current condition and whether it **supports / is neutral toward / contradicts** the Module A wave label. Do **not** sum into a single score.

### Step 4 — Module C: Market Environment

Assess macro/market context relevant to the stock's market. Each signal is independent — do not aggregate into a score.

For CLI data in this module, run `longbridge <subcommand> --help` first if you haven't
already. **Index codes are not valid symbols on Longbridge** — use tracking ETFs instead
(see "Suggested proxy" column). If a proxy symbol returns an error, fall back to Web Search.

**HK (HKEX)**

| Signal | How to get | Suggested proxy | Web Search fallback |
|--------|-----------|-----------------|---------------------|
| HSI trend (60-day) | `longbridge kline` — 60 daily bars | 2800.HK (Tracker Fund) | "恒生指数 今日" |
| Southbound flow | `longbridge capital` for the target symbol | — | "南向资金 今日净买入" |
| Short-sell ratio | Not in CLI | — | "[stock name] HK short selling ratio" |
| Recent policy / regulatory | — | — | Web Search |

**US (NYSE/NASDAQ)**

| Signal | How to get | Suggested proxy | Web Search fallback |
|--------|-----------|-----------------|---------------------|
| S&P 500 trend (60-day) | `longbridge kline` — 60 daily bars | SPY.US | "S&P 500 price today" |
| VIX level | Not in CLI | — | "VIX current level" |
| Put/call ratio | Not in CLI | — | "CBOE equity put call ratio" |
| Sector ETF trend | `longbridge kline` — 30 daily bars | Relevant sector ETF (e.g. XLK.US, XLE.US) | Web Search |

**A-share (SSE/SZSE)**

| Signal | How to get | Suggested proxy | Web Search fallback |
|--------|-----------|-----------------|---------------------|
| Shanghai Composite trend | `longbridge kline` — 60 daily bars | 000001.SH | "上证指数 今日" |
| Northbound flow | `longbridge capital` for the target symbol | — | "北向资金 今日" |
| Margin balance trend | Not in CLI | — | "融资余额" |
| Recent CSRC/policy signals | — | — | Web Search |

**SGX**

| Signal | How to get | Web Search fallback |
|--------|-----------|---------------------|
| STI trend | CLI coverage may be limited — try a proxy first, expect errors | "Straits Times Index today" |
| Stock-specific news | `longbridge news` for the target symbol | "[company] SGX news" |

If a data item is unavailable from both CLI and Web Search, note "数据不可用 / Data unavailable" for that item only. Do not skip the whole module.

### Step 5 — Generate Output

Assemble the three-module result into the output template below.

## Output Template

The output uses **four sections** written in natural language — no bullet dumps. Match the user's language (Simplified CN / Traditional CN / English) throughout.

```
【{Company Name}（{SYMBOL}）】波浪技术分析
分析日期：{today}　｜　当前价：{price}　｜　今日区间：{low} – {high}

【一】波浪结构

当前阶段
{stage_label_natural} · {one-line characterisation}

{2–3 paragraph prose narrative:}
- Para 1: Describe the swing sequence in plain language from the key bottom/origin,
  naming each wave and the price/date of each pivot. Explain why the current move
  matches the identified stage. Avoid jargon — translate wave numbers to meaning.
- Para 2: Confirm with a second counting perspective (different threshold / degree).
  State whether both agree ("两套视角结论一致") or conflict ("结构待确认，建议观望").
- Para 3 (if unconfirmed): Explain what would resolve the ambiguity.

波浪结构示意（ASCII，仅在结构清晰时输出）
价格
  │
{high} ┤                    {stage} ?
  │                      ╱
...                     ╱
{origin}┤  起点╱
  └──────────────────────▶ 时间

斐波那契参考区间

上行延伸目标（基准：{base_swing_low} → {base_swing_high}，波幅 {span}）

| 延伸比例 | 参考价位 | 说明 |
|---------|---------|------|
| 1.618 倍 | {price} | {interpretation} |
| 2.618 倍 | {price} | {interpretation — note if already breached} |
| 3.618 倍 | {price} | {next resistance if prior targets breached} |

回调支撑参考

| 支撑区 | 参考价位 | 说明 |
|-------|---------|------|
| 近期关注 | {price} | 整数关口 / 前期突破区 |
| 中度支撑 | {price} | 内部 38.2% 回撤 |
| 关键支撑 | {price} | 跌破则 {wave} 计数失效 |
| 深度支撑 | {price} | 跌破则整体结构需重新评估 |

失效条件：若日线收盘跌破 {invalidation_price}，{what it means}。

【二】动量与市场环境

动量指标

| 指标 | 当前状态 | 对波浪判断的意义 |
|------|---------|----------------|
| MACD（12/26/9） | 线值 {x} {>/< } 信号线 {y}，柱状图 {z} {扩张/收缩} | {supports/neutral/contradicts + reason} |
| RSI-14 | {value}，{超买/超卖/中性区}，{有/无}背离 | {meaning in context of wave stage} |
| 均线（MA20/MA50） | MA20 {x} / MA50 {y}，价格{领先/滞后}，MA20{向上/走平/向下} | {trend context} |
| 成交量 | 当日 {x}，{高于/低于} 20日均量 {y}（{+/-}%），近3日{放量/缩量} | {confirms or warns} |

{1–2 sentence synthesis: which indicators align, which diverge, and what that means for the wave count.}
{If bearish/bullish divergence detected: ⚠ 检测到 {顶/底}背离——{plain-language explanation of risk}.}

市场背景
{2–4 bullet points from news + Web Search covering catalysts, sector context, macro.
 Each bullet: [emoji] event description → market interpretation.
 End with a note if SPX/VIX data was not fetched: "VIX 及大盘最新状态建议通过 Web Search 确认。"}

【三】综合参考

趋势方向：{one sentence on primary trend and whether counter-trend trades are appropriate now.}

值得关注的区间
{Prose paragraph: describe 1–2 price zones worth watching for entry or caution,
 combining Fibonacci levels + momentum trigger conditions in plain language.}

需要盯住的信号
{3 bullets, each: condition → what it implies for the wave count}

失效观察线：日线收盘跌破 {price}，当前判断需重新评估。

【四】做这个分析前，有几点需要告诉你

{3–4 short paragraphs of plain-language caveats tailored to THIS stock's specific situation:}
- Subjectivity of wave counting and what gives/reduces confidence here
- Fundamental / news drivers and "buy the rumour sell the fact" risk if applicable
- Any unusual price characteristics (e.g. Fibonacci targets already breached, extreme RSI)
- Reminder that daily close matters more than intraday wicks for invalidation levels

---
⚠ 本分析基于历史技术数据，不代表未来表现，不构成投资建议。
```

### Output rules

- **No bullet-list dumps** in sections 【一】–【三】. Use tables for data, prose for narrative.
- **ASCII wave diagram**: include when `agreed: true`; omit when `unconfirmed`.
- **Section 【四】is mandatory** — always write stock-specific caveats, never generic boilerplate.
- If `agreed: false`: replace 【一】prose with "两套计数方案结论不一致，建议观望" and skip the diagram and Fibonacci tables.
- **Disclaimer** is system-injected at the end; never omit or modify it.

## Error Handling

| Situation | Response |
|-----------|----------|
| `command not found: longbridge` | Fall back to MCP `mcp__longbridge__*`; if also unavailable, ask user to install longbridge CLI |
| `not logged in` / `unauthorized` | Ask user to run `longbridge auth login` |
| < 250 daily candles | Refuse analysis with explanation |
| Recent suspension / ST stock | Refuse analysis with explanation |
| Both wave count scenarios conflict, no momentum tiebreak | Output "结构待确认，建议观望" — do not force a label |
| Web Search unavailable for Module C item | Mark that item as "数据不可用" — continue other items |
| Other CLI stderr | Surface verbatim — do not silently retry |

## Script

> ⚠️ **额外依赖 / Extra dependency required**
>
> `scripts/signal_engine.py` 依赖 `pandas` 和 `numpy`，使用前请确认已安装：
>
> ```bash
> pip install pandas numpy
> ```
>
> 通常已预装；若报 `ModuleNotFoundError`，运行上述命令后重试。
> Requires `pandas` and `numpy` — usually pre-installed. Run `pip install pandas numpy` if you see `ModuleNotFoundError`.

See `scripts/signal_engine.py` for the wave engine (ZigZag + 5-wave impulse + ABC correction + Fibonacci validation).

Usage:
```bash
python3 scripts/signal_engine.py --kline /tmp/kline_day.json --symbol AAPL.US
```

## MCP fallback

When `longbridge` CLI is not installed, fall back to MCP tools:

| CLI command | MCP tool |
|---|---|
| `longbridge kline <SYMBOL> --period day --format json` | `mcp__longbridge__candlesticks` |
| `longbridge kline <SYMBOL> --period week --format json` | `mcp__longbridge__candlesticks` (period=Week) |
| `longbridge news <SYMBOL> --format json` | `mcp__longbridge__news` |

MCP setup: `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` (Quote scope).

## Reference Files

| File | Contents |
|------|----------|
| [references/fibonacci.md](references/fibonacci.md) | Fibonacci ratio tables for all wave relationships |
| [references/wave-structure.md](references/wave-structure.md) | Wave structure diagrams, iron rules, corrective variants |
| [references/market-environment.md](references/market-environment.md) | Per-market data sources and signal interpretation guide |

## Related Skills

- `longbridge-kline` — raw K-line data queries
- `longbridge-capital-flow` — capital flow data
- `idea-generation` — fundamental screening to complement technical timing
- `earnings-analysis` — fundamental event context
