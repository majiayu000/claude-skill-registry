---
name: longbridge-investment-ideas
description: |
  Investment idea generation — systematically surfaces new investment opportunities by combining quantitative screening (low valuation / high momentum / improving fundamentals), thematic research (sector trends / policy catalysts), and pattern recognition (historical analogues), producing a long/short candidate list. Triggers: "投资想法", "选股灵感", "投资机会", "找股票", "发掘机会", "多头机会", "空头机会", "主题投资", "投資想法", "選股靈感", "投資機會", "找股票", "多頭機會", "空頭機會", "主題投資", "investment ideas", "stock ideas", "investment opportunities", "idea generation", "long ideas", "short ideas", "thematic investing", "stock discovery", "find me stocks", "what should I buy".
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

# longbridge-investment-ideas

Surfaces actionable investment ideas through a multi-lens screening process: value, momentum, fundamental improvement, and thematic catalysts — outputting a prioritised candidate list with brief rationale for each idea.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger when the user wants to discover new investment opportunities rather than research a specific stock:

- *"帮我找一些当前有投资价值的股票"* / *"幫我發掘一些港股投資機會"* / *"Generate some investment ideas in AI infrastructure"*
- *"选股灵感"*, *"多头机会"*, *"what should I be looking at this quarter"*

## Workflow

1. Clarify parameters with the user if not provided:
   - **Market**: US / HK / A-share / SG (or multiple)
   - **Theme / sector** (optional): e.g. AI, EV, healthcare, energy
   - **Style**: value / growth / momentum / contrarian / short ideas
2. Fetch the relevant universe (index constituents or sector ETF).
3. For top candidates, fetch valuation indices and recent 60-day price momentum.
4. Apply the selected screening lens (see below) to rank candidates.
5. For top 5–8 ideas, fetch news to validate the narrative.
6. Output a ranked candidate list with rationale.

## Screening lenses

| Lens | Signal | CLI data |
|---|---|---|
| Value | Low PE / PB vs industry median | `longbridge industry-valuation` |
| Momentum | Top 60-day price return in universe | `longbridge kline --period day --count 60` |
| Fundamental improvement | Revenue acceleration / margin expansion (QoQ) | `longbridge financial-report --kind IS` |
| Thematic | Recent policy / product catalyst in news | `longbridge news` |

## CLI

> If you're unsure of exact flag names or defaults, run `longbridge <subcommand> --help` first.

```bash
# Fetch universe (index constituents)
longbridge constituent <INDEX_SYMBOL> --format json

# Valuation indices for screening (PE, PB, momentum)
longbridge calc-index <SYMBOL> --format json

# 60-day daily price for momentum calculation
longbridge kline <SYMBOL> --period day --count 60 --format json

# News for narrative validation
longbridge news <SYMBOL> --format json
```

## Output

**Screening parameters**: market, theme, style lens, date

**Idea candidate table**:

| Rank | Symbol | Company | Market Cap | Lens | Key Signal | Rationale |
|---|---|---|---|---|---|---|
| 1 | NVDA.US | NVIDIA | $2.5T | Momentum + Thematic | +40% in 60d; AI capex cycle | ... |

For each top idea, add a one-paragraph 分析摘要 / Analysis summary covering:
- 近期催化剂或关注事项 / Recent catalysts or watchpoints（供参考）
- 关键指标与事件 / Key metrics and events
- Key risk (one-liner bear case)

> 以上内容仅供参考，不构成投资建议。投资决策请结合自身风险承受能力独立判断。/ The above is for reference only and does not constitute investment advice.

## Error handling

| Situation | Simplified Chinese | Traditional Chinese / English |
|---|---|---|
| `command not found: longbridge` | 回退到 MCP；否则提示安装 longbridge-terminal | 回退到 MCP；否則提示安裝 / Fall back to MCP; prompt to install |
| `not logged in` / `unauthorized` | 请运行 `longbridge auth login` | 請運行 `longbridge auth login` / Run `longbridge auth login` |
| No market or theme specified | 请告知目标市场和投资风格 | 請告知目標市場和投資風格 / Please specify target market and style |
| Other stderr | 原样展示错误，不重试 | 原樣展示，不重試 / Surface verbatim, no silent retry |

## Related skills

| User asks | Route to |
|---|---|
| Small-cap growth screening | `longbridge-smallcap-growth` |
| Peer comparison | `longbridge-peer-comparison` |
| Industry valuation | `longbridge-valuation` |
| Full research on a specific idea | `longbridge-stock-research` |
| Market anomaly / unusual movers | `longbridge-anomaly` |

## File layout

```
longbridge-investment-ideas/
└── SKILL.md
```

Prompt-only — no `scripts/`. Discover the latest CLI flags via `longbridge <subcommand> --help`.
