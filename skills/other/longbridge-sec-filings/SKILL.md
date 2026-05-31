---
name: longbridge-sec-filings
description: |
  SEC EDGAR filing analysis via Longbridge — 10-K annual report, 10-Q quarterly, 8-K material events, proxy statement, insider Form 4. Extracts risk factors, MD&A, non-recurring items, and investment signals. Triggers: "SEC文件", "SEC申报", "10-K", "10-Q", "8-K", "委托投票书", "Form 4", "MD&A", "风险因素", "内部人申报", "SEC文件", "SEC申報", "委託投票書", "風險因素", "內部人申報", "SEC filing", "10-K annual report", "10-Q quarterly", "8-K material event", "proxy statement", "Form 4 insider", "MD&A", "risk factors", "SEC EDGAR".
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

# longbridge-sec-filings

Prompt-only analysis skill. Retrieves SEC filings via Longbridge and extracts investment-relevant signals: financial KPIs (10-K/10-Q), material events (8-K), governance/compensation (Proxy), and insider behaviour (Form 4).

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"帮我看下 AAPL 最新的 10-K"* / *"What are AAPL's key risks from the latest 10-K?"*
- *"TSLA 昨天发了个 8-K，说了什么？"* / *"What did TSLA's 8-K say?"*
- *"高管最近有没有申报卖股票 (Form 4)？"* / *"Any insider Form 4 sales recently?"*
- *"10-Q 的 MD&A 里有什么异常？"* / *"Any unusual items in the MD&A?"*
- *"Proxy 里高管薪酬怎么样？"* / *"What does the proxy say about exec compensation?"*

For institutional 13F holdings route to `longbridge-flows`. For quarterly earnings analysis route to `longbridge-earnings`.

## CLI

Run `longbridge <subcommand> --help` to verify exact flags.

```bash
# List recent filings for a symbol
longbridge filing <SYMBOL> --format json

# Filter by filing type (if supported — verify with --help)
longbridge filing <SYMBOL> --type 10-K --format json
longbridge filing <SYMBOL> --type 10-Q --format json
longbridge filing <SYMBOL> --type 8-K  --format json

# Financial data (structured KPIs from filings)
longbridge financial-report <SYMBOL> --format json

# News — supplement for 8-K summaries and insider trade coverage
longbridge news <SYMBOL> --format json
```

## Filing type guide

| Filing | Frequency | Key content | Investment signal |
|---|---|---|---|
| 10-K | Annual | Full financials, Risk Factors, MD&A, auditor opinion | Baseline quality, hidden risks |
| 10-Q | Quarterly | Interim financials, MD&A updates, legal proceedings | Trend vs prior quarters |
| 8-K | Ad hoc | Material events: earnings, M&A, exec changes, defaults | Immediate catalyst |
| Proxy (DEF 14A) | Annual | Exec compensation, board composition, shareholder proposals | Governance quality |
| Form 4 | Within 2 days | Insider buy/sell transactions (officers/directors) | Insider sentiment signal |
| SC 13G/13D | On crossing 5% | Large investor disclosures | Block-holder moves |

## Workflow

1. **Identify filing type** from the user's question; default to most recent filing if unspecified.
2. **Fetch filings list** with `longbridge filing <SYMBOL>`, select the relevant entry.
3. **Fetch financial KPIs** with `longbridge financial-report` for structured numbers.
4. **Supplement with news** (`longbridge news`) for 8-K summaries or insider trade narratives if filing detail is sparse.
5. **Extract key items** per filing type (see extraction guide below).
6. **Output** structured analysis (template below). Cite Longbridge Securities.

## Extraction guide by filing type

### 10-K / 10-Q
- Revenue, net income, EPS vs prior period
- Gross/operating margin trend
- Free cash flow
- Key risk factors (new risks added or escalated language)
- MD&A: management commentary on performance drivers
- Non-recurring items (impairments, restructuring, gains on asset sales)
- Debt and liquidity (cash, revolver capacity)

### 8-K
- Event type (Item number: 1.01=material agreement, 2.02=earnings, 5.02=exec change, etc.)
- Material fact in 2–3 sentences
- Bull/bear interpretation

### Proxy (DEF 14A)
- CEO total comp vs prior year and vs peers
- Performance metrics in comp plan (revenue, TSR, EPS targets)
- Board independence and audit committee composition
- Shareholder proposals (activist items)

### Form 4
- Filer: name and title
- Transaction: buy vs sell, shares, price, date
- Post-transaction ownership
- Pattern: first purchase, cluster selling near highs, 10b5-1 plan flag

## Output template

```
{Symbol} {Filing type} analysis — Source: Longbridge Securities

[Filing metadata]
- Form: {type}  |  Filed: {date}  |  Period: {period}

[Key findings]
1. {Finding — max 2 sentences}
2. {Finding}
3. {Finding}

[Financial snapshot] (10-K / 10-Q)
- Revenue: ${X}  YoY: {+/-X%}
- Net income: ${X}  |  EPS: ${X}
- Free cash flow: ${X}
- Non-recurring: {describe or "none identified"}

[Risk factors / MD&A highlights] (10-K / 10-Q)
- New or escalated risks: {list}
- Management tone: {cautious / neutral / optimistic}

[Investment signal]
{Bullish / Bearish / Neutral} — {1-sentence rationale}

⚠️ 以上分析仅供参考，不构成投资建议。/ 以上分析僅供參考，不構成投資建議。/ For reference only. Not investment advice.
```

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 切换到 MCP；若不可用，请安装 longbridge-terminal | 切換至 MCP；若不可用，請安裝 longbridge-terminal | Fall back to MCP; if unavailable, install longbridge-terminal |
| stderr `not logged in` | 请执行 `longbridge auth login` | 請執行 `longbridge auth login` | Run `longbridge auth login` |
| `filing` returns empty | 暂无 SEC 申报数据；尝试 `longbridge news` 补充 | 暫無 SEC 申報數據；嘗試 `longbridge news` 補充 | No filing data available; try `longbridge news` as supplement |
| Non-US symbol requested | SEC 申报仅适用于美股；港股/A股请改用相应披露渠道 | SEC 申報僅適用於美股；港股/A股請改用相應披露渠道 | SEC filings are US-listed only; for HK/A-share use relevant disclosure channels |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

## Related skills

- Quarterly earnings analysis → `longbridge-earnings`
- Insider / institutional flows (13F) → `longbridge-flows`
- Fundamental KPIs → `longbridge-fundamental`
- Company news and sentiment → `longbridge-news`

## File layout

```
longbridge-sec-filings/
└── SKILL.md          # prompt-only, no scripts/
```
