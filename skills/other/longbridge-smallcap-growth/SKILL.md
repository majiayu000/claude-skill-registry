---
name: longbridge-smallcap-growth
description: |
  Small-cap growth stock discovery — identifies overlooked small/mid-cap high-growth companies (A-share 专精特新, HK growth stocks, US small-cap growth) by screening for market cap < 5–10B, revenue growth > 30%, ROE > 15%, and low institutional ownership. Triggers: "小盘成长", "小市值", "成长股", "中小盘", "专精特新", "隐形冠军", "小盘股", "成长潜力", "小盤成長", "小市值", "成長股", "中小盤", "專精特新", "隱形冠軍", "small cap growth", "small cap stocks", "growth stocks", "mid-small cap", "hidden champions", "high growth companies", "small cap discovery", "emerging growth", "小市值成长股", "中小市值".
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

# longbridge-smallcap-growth

Screens for overlooked small/mid-cap high-growth stocks across US, HK, and A-share markets using quantitative filters (market cap, revenue growth, ROE) and qualitative overlays (sector focus, 专精特新 category for A-shares).

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger when the user wants to find small or mid-cap growth names:

- *"帮我找一些专精特新的小盘成长股"* / *"幫我發掘港股中小市值成長股"* / *"Find me high-growth small caps in the US"*
- *"隐形冠军"*, *"小盘成长"*, *"small cap discovery"*, *"emerging growth stocks"*

## Default screening criteria

| Criterion | Default threshold | User-adjustable |
|---|---|---|
| Market cap (US/HK) | < USD 10B | Yes |
| Market cap (A-share) | < CNY 50B | Yes |
| Revenue YoY growth | > 30% | Yes |
| ROE | > 15% | Yes |
| Institutional ownership | Low (qualitative flag) | Note only |

Ask the user if they want to adjust any threshold before running.

## Workflow

1. Clarify market (US / HK / A-share / all) and any sector preference.
2. Fetch index constituents for the relevant small/mid-cap indices (e.g. `IWM.US` for Russell 2000, `399006.SZ` for ChiNext, `399005.SZ` for SME Board).
3. For each constituent, fetch market cap via `calc-index` and filter by size.
4. For size-passing candidates, fetch the latest income statement to check revenue growth.
5. Further filter by ROE from the balance sheet / financial-report data.
6. Return the top 10 candidates ranked by revenue growth rate, with a brief profile for each.

## CLI

> If you're unsure of exact flag names or defaults, run `longbridge <subcommand> --help` first.

```bash
# Small/mid-cap index constituents
longbridge constituent <INDEX_SYMBOL> --format json
# Examples: IWM.US (Russell 2000), 399006.SZ (ChiNext), HSI.HK (Hang Seng)

# Market cap and valuation indices per symbol
longbridge calc-index <SYMBOL> --format json

# Latest income statement (revenue growth)
longbridge financial-report <SYMBOL> --kind IS --format json

# News / recent catalysts for top candidates
longbridge news <SYMBOL> --format json
```

## Output

**Screening parameters**: market, sector, market cap threshold, revenue growth threshold, ROE threshold

**Top candidates table**:

| Rank | Symbol | Company | Market Cap | Rev Growth YoY | ROE | Sector | Thesis |
|---|---|---|---|---|---|---|---|

For each top 5 candidate, include a brief (3–4 sentence) investment thesis:
- Business model and competitive advantage
- Growth driver and runway
- Key risk
- Catalyst to watch

**A-share note**: For 专精特新 (specialized, sophisticated, distinctive, innovative) classification, note if the company holds a national-level 专精特新小巨人 designation when mentioned in filings/news.

**Disclaimer**: Small-cap stocks carry higher liquidity and volatility risk. Not a buy recommendation.

## Error handling

| Situation | Simplified Chinese | Traditional Chinese / English |
|---|---|---|
| `command not found: longbridge` | 回退到 MCP；否则提示安装 longbridge-terminal | 回退到 MCP；否則提示安裝 / Fall back to MCP; prompt to install |
| `not logged in` / `unauthorized` | 请运行 `longbridge auth login` | 請運行 `longbridge auth login` / Run `longbridge auth login` |
| No market specified | 请告知目标市场（美股/港股/A股） | 請告知目標市場 / Please specify market (US/HK/A-share) |
| Other stderr | 原样展示错误，不重试 | 原樣展示，不重試 / Surface verbatim, no silent retry |

## Related skills

| User asks | Route to |
|---|---|
| Broader investment ideas | `longbridge-investment-ideas` |
| Full research on a candidate | `longbridge-stock-research` |
| Peer comparison | `longbridge-peer-comparison` |
| Insider buying signals | `longbridge-flows` |

## File layout

```
longbridge-smallcap-growth/
└── SKILL.md
```

Prompt-only — no `scripts/`. Discover the latest CLI flags via `longbridge <subcommand> --help`.
