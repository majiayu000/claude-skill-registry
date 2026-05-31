---
name: longbridge-tech-hype
description: |
  Tech hype vs. fundamentals analysis via Longbridge — identifies valuation bubbles and fundamental disconnects in A-share / HK tech stocks. Compares PE / PS / EV-EBITDA historical percentile against actual revenue / profit growth. Analyses which AI / EV / semiconductor theme plays have fundamental support vs. pure sentiment-driven momentum. Triggers: "科技炒作", "AI泡沫", "估值泡沫", "科技估值", "概念股", "主题炒作", "基本面背离", "炒作识别", "科技泡沫", "科技炒作", "AI泡沫", "估值泡沫", "科技估值", "概念股", "主題炒作", "基本面背離", "tech hype", "AI bubble", "valuation bubble", "tech valuation", "theme stocks", "hype vs fundamentals", "concept stocks", "narrative vs reality", "AI concept", "semiconductor bubble".
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

# longbridge-tech-hype

Tech hype versus fundamentals — detect valuation bubbles and identify which theme-driven rallies have fundamental backing.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger on prompts asking for:

- Bubble or hype detection — *"这只 AI 概念股是不是泡沫"*, *"AI bubble check"*, *"估值泡沫"*
- Theme vs. fundamentals — *"主题炒作还是有基本面"*, *"hype vs fundamentals"*, *"narrative vs reality"*
- Tech sector valuation check — *"科技股估值贵不贵"*, *"半导体概念股"*, *"新能源估值"*

For pure valuation percentile defer to `longbridge-valuation`. For sector-wide ranking defer to `longbridge-constituent`.

## Workflow

1. Extract and normalise the symbol(s).
2. Fetch in parallel:
   - Valuation multiples and historical percentile (PE, PS, EV/EBITDA)
   - Industry median valuation for peer context
   - Last 2–3 years income statement (revenue growth, net income growth, gross margin trend)
   - Recent news and narrative themes
3. Compute the **Hype Score**:
   - Valuation percentile (0–100) vs. revenue growth rate
   - Gap = `valuation_percentile − revenue_growth_rank` (positive = hype-heavy)
4. Classify the stock:
   - `Fundamentally Justified` — growth supports valuation
   - `Partially Justified` — moderate gap, watch closely
   - `Hype-Driven` — large gap, sentiment outpacing fundamentals
   - `Detached Bubble` — extreme valuation with decelerating growth
5. Summarise key narrative themes from news and flag whether each has financial backing.

> If unsure of exact flag names, run `longbridge <subcommand> --help` before proceeding.

## CLI

```bash
# Valuation multiples and historical percentile
longbridge valuation <SYMBOL> --format json

# Industry median valuation
longbridge industry-valuation <SYMBOL> --format json

# Income statement — revenue, net income, margins
longbridge financial-report <SYMBOL> --kind IS --format json

# Recent news — theme keywords
longbridge news <SYMBOL> --format json
```

## Output structure

```
TECH HYPE ANALYSIS — <SYMBOL>  <Date>

VERDICT: [Fundamentally Justified | Partially Justified | Hype-Driven | Detached Bubble]
Hype Score: xx/100  (higher = more hype-heavy)

VALUATION SNAPSHOT
PE:  xx.x×  (xx-th percentile, 3Y)   Industry median: xx.x×
PS:  x.x×   (xx-th percentile, 3Y)
EV/EBITDA: xx.x×  (xx-th percentile, 3Y)

FUNDAMENTAL CHECK
Revenue Growth (YoY):  +xx%  →  +xx%  →  +xx%
Net Income Growth:     +xx%  →  +xx%  →  +xx%
Gross Margin:          xx%   →  xx%   →  xx%

NARRATIVE THEMES (from news)
Theme               Has Backing?   Evidence
AI / LLM            ✓ Partial      Revenue up xx%, but margin flat
Semiconductor cycle ✗ No data      Mostly sentiment-driven
...

CONCLUSION
<2–3 sentence synthesis of hype vs. fundamental alignment>
```

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|-----------|---------|---------|---------------|
| Symbol not found | 未找到该代码，请确认市场和格式。 | 找不到該代碼，請確認市場和格式。 | Symbol not found — verify exchange and ticker. |
| Valuation history unavailable | 历史估值分位数据不足，结果仅供参考。 | 歷史估值分位數據不足，結果僅供參考。 | Insufficient valuation history — results are approximate. |
| `command not found: longbridge` | 请安装 longbridge-terminal 或通过 MCP 连接。 | 請安裝 longbridge-terminal 或透過 MCP 連線。 | Install longbridge-terminal or connect via MCP. |
| `not logged in` | 请运行 `longbridge auth login`。 | 請執行 `longbridge auth login`。 | Run `longbridge auth login`. |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

- `longbridge-valuation` — valuation percentile and industry comparison
- `longbridge-fundamental` — deep financial KPI analysis
- `longbridge-news` — news and sentiment signals
- `longbridge-peer-comparison` — cross-symbol valuation matrix

## File layout

```
skills/longbridge-tech-hype/
└── SKILL.md
```
