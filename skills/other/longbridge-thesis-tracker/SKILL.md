---
name: longbridge-thesis-tracker
description: |
  Investment thesis tracker — maintains and updates the investment thesis for portfolio holdings and watchlist names by continuously tracking key data points (revenue growth, gross margin, user metrics), catalyst progress (new products, expansion, policy), and risk milestones, then renders a verdict on whether the thesis still holds. Triggers: "投资逻辑", "Thesis追踪", "投资假设", "逻辑验证", "跟踪持仓", "买入逻辑", "持仓理由", "投資邏輯", "Thesis追蹤", "投資假設", "邏輯驗證", "追蹤持倉", "investment thesis", "thesis tracking", "investment hypothesis", "thesis validation", "thesis check", "investment rationale", "position monitoring", "thesis intact", "is my thesis still valid".
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

# longbridge-thesis-tracker

Checks whether an investment thesis for a given stock is intact by pulling the latest financial data, analyst revisions, news, and regulatory filings, then rendering a structured verdict.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger when the user wants to validate or update a buy thesis for a position:

- *"帮我检查一下 NVDA 的买入逻辑还成立吗"* / *"幫我追蹤一下 700.HK 的投資邏輯"* / *"Check if my thesis on TSLA still holds"*
- *"持仓理由验证"*, *"逻辑是否还成立"*, *"thesis intact?"*

The user may provide a pre-written thesis; if not, ask for key thesis pillars (2–5 bullet points the user cares about).

## Workflow

1. Ask the user to state their thesis pillars if not already provided (e.g. *"AI capex supercycle"*, *"margin expansion to 30%"*, *"China re-opening"*).
2. Map each pillar to one or more measurable data points.
3. Run CLI commands to fetch the latest evidence.
4. For each pillar, render: **Still intact / Weakened / Broken** with supporting data.
5. Overall verdict: thesis confidence score (High / Medium / Low) + recommended action.

## CLI

> If you're unsure of exact flag names or defaults, run `longbridge <subcommand> --help` first.

```bash
# Recent news and regulatory filings (catalyst/risk updates)
longbridge news <SYMBOL> --format json

# Latest income statement (revenue growth, margin trends)
longbridge financial-report <SYMBOL> --kind IS --format json

# Analyst consensus (EPS revisions, target price changes, rating)
longbridge consensus <SYMBOL> --format json

# SEC / HKEx regulatory filings (material disclosures)
longbridge filing <SYMBOL> --format json
```

## Output

Structure the tracker output as follows:

**Header**: Symbol, company name, today's date, thesis check date

**Thesis pillars status table**:

| Pillar | Data Point | Last Value | vs Expectation | Status |
|---|---|---|---|---|
| e.g. Revenue acceleration | YoY revenue growth | +24% | >20% target | Intact |
| e.g. Margin expansion | Gross margin % | 61% | >65% target | Weakened |

**Catalyst tracking**:
- List of expected catalysts, whether they have materialised, and market reaction

**Risk monitoring**:
- Key risks flagged at thesis initiation and current status

**Overall verdict**:

> **Thesis confidence: Medium** — 2 of 4 pillars intact. Core AI-driven revenue growth on track; margin expansion lagging. No thesis-breaking events in filings. Suggest hold and monitor next earnings.

## Error handling

| Situation | Simplified Chinese | Traditional Chinese / English |
|---|---|---|
| `command not found: longbridge` | 回退到 MCP；否则提示安装 longbridge-terminal | 回退到 MCP；否則提示安裝 / Fall back to MCP; prompt to install |
| `not logged in` / `unauthorized` | 请运行 `longbridge auth login` | 請運行 `longbridge auth login` / Run `longbridge auth login` |
| No thesis pillars provided | 请告知您的核心买入逻辑（2–5条） | 請提供核心買入邏輯 / Please state 2–5 thesis pillars |
| `filing` subcommand unavailable | 跳过监管文件检索，标注缺失 | 跳過文件檢索，標注缺失 / Skip filing fetch, flag as missing |
| Other stderr | 原样展示错误，不重试 | 原樣展示，不重試 / Surface verbatim, no silent retry |

## Related skills

| User asks | Route to |
|---|---|
| Full research snapshot | `longbridge-stock-research` |
| Post-earnings update | `longbridge-earnings` |
| News only | `longbridge-news` |
| Analyst consensus only | `longbridge-fundamental` |
| Portfolio P&L | `longbridge-portfolio` |

## File layout

```
longbridge-thesis-tracker/
└── SKILL.md
```

Prompt-only — no `scripts/`. Discover the latest CLI flags via `longbridge <subcommand> --help`.
