---
name: longbridge-morning-brief
description: |
  Daily morning briefing — writes a concise pre-market morning brief summarising overnight major moves (US/HK close, A-share pre-market signals), key events on the watchlist, today's catalysts (earnings / economic data / policy), and a trading ideas overview. Triggers: "晨会", "晨报", "早报", "早盘", "盘前简报", "今日重点", "开盘前", "晨会纪要", "晨會", "晨報", "早報", "盤前簡報", "今日重點", "開盤前", "晨會紀要", "morning brief", "morning call", "pre-market brief", "daily briefing", "market morning", "opening summary", "today's focus", "AM brief", "morning meeting".
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

# longbridge-morning-brief

Produces a structured daily morning briefing (晨会纪要) covering overnight market moves, watchlist highlights, today's key catalysts, and a concise trading agenda.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger when the user wants a morning-meeting style market summary:

- *"帮我写今天的晨报"* / *"幫我準備今天的晨會紀要"* / *"Give me a morning brief"*
- *"早盘有什么重点"*, *"今日开盘前要关注什么"*, *"pre-market summary"*

Also trigger if the user provides a watchlist of symbols and asks for a pre-market digest.

## Workflow

1. Identify the user's watchlist symbols (ask if not provided; accept up to 10).
2. Determine today's date and relevant markets (US, HK, CN, SG).
3. Fetch quotes, today's calendar events, and intraday capital flow.
4. Check for recent news on each watchlist symbol.
5. Synthesise into a morning brief (see Output section).

## CLI

> If you're unsure of exact flag names or defaults, run `longbridge <subcommand> --help` first.

```bash
# Current quotes for watchlist symbols (can pass multiple)
longbridge quote <SYMBOL1> <SYMBOL2> ... --format json

# Today's earnings / economic / dividend calendar (requires subcommand)
longbridge finance-calendar report --format json      # earnings reports
longbridge finance-calendar macrodata --format json   # macro releases
longbridge finance-calendar dividend --format json    # dividend events

# Recent news per symbol
longbridge news <SYMBOL> --format json

# Intraday capital flow (same-day only)
longbridge capital <SYMBOL> --format json
```

Run `longbridge finance-calendar --help` to see all available subcommands (report / dividend / split / ipo / macrodata / closed).

## Output

Structure the morning brief in five concise sections (keep total length under 600 words):

**1. Overnight recap** (2–3 bullets)
- US market close: index levels, winners/losers, VIX
- HK market close: HSI level, major moves
- Other notable macro (currencies, commodities, yields)

**2. Watchlist highlights** (table)

| Symbol | Last Price | Change % | Key Event |
|---|---|---|---|

**3. Today's catalysts** (bulleted)
- Earnings releases today (company, before/after market)
- Economic data (CPI, FOMC, NFP, etc.) with consensus
- Policy / regulatory events

**4. Capital flow signals** (if data available)
- Sectors or names with notable inflow/outflow

**5. Trading agenda** (2–4 bullets)
- Specific names or themes to watch
- Suggested entry/exit levels or key levels to monitor (use analyst targets from consensus if available)

Close with: *Data sourced from Longbridge Securities / 数据来源：长桥证券 / 數據來源：長橋證券*

## Error handling

| Situation | Simplified Chinese | Traditional Chinese / English |
|---|---|---|
| `command not found: longbridge` | 回退到 MCP；否则提示安装 longbridge-terminal | 回退到 MCP；否則提示安裝 / Fall back to MCP; prompt to install |
| `not logged in` / `unauthorized` | 请运行 `longbridge auth login` | 請運行 `longbridge auth login` / Run `longbridge auth login` |
| No symbols provided | 请告知您的自选股或关注标的 | 請告知您的自選股 / Please provide your watchlist symbols |
| Other stderr | 原样展示错误，不重试 | 原樣展示，不重試 / Surface verbatim, no silent retry |

## Related skills

| User asks | Route to |
|---|---|
| Watchlist contents | `longbridge-watchlist` |
| Capital flow detail | `longbridge-capital-flow` |
| Earnings calendar | `longbridge-calendar` |
| Catalyst radar (automated) | `longbridge-catalyst-radar` |
| News for a single stock | `longbridge-news` |

## File layout

```
longbridge-morning-brief/
└── SKILL.md
```

Prompt-only — no `scripts/`. Discover the latest CLI flags via `longbridge <subcommand> --help`.
