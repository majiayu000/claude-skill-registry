---
name: longbridge-news
description: |
  Aggregated news, regulatory filings, and Longbridge-community discussion for a single stock — classified into catalyst / regulatory / strategic / financial / opinion / other, with a fact-only key-takeaway summary and a sentiment skew. Falls back to WebSearch only when data is sparse or stale, and labels the source. Triggers: "X 最近新闻", "X 公告", "市场对 X 财报怎么看", "X 社区讨论", "X 公司动态", "市场情绪", "最近怎么了", "X 最近新聞", "X 公告", "市場對 X 財報怎麼看", "X 社區討論", "recent news", "company filings", "market reaction", "what is everyone saying about X", "community sentiment", "8-K", "港交所披露", "earnings reaction".
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

# longbridge-news

Prompt-only skill that aggregates news, filings, and community topics for a single stock — classifies them, distils a fact-only takeaway, and reports sentiment at coarse granularity. May call WebSearch as a clearly-labelled fallback.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"NVDA 最近新闻"*, *"recent news on NVDA"*, *"NVDA 最近新聞"*
- *"茅台公告"*, *"700 港交所披露"*, *"NVDA 8-K"*
- *"市场对 X 财报怎么看"*, *"X 财报后股价为什么跌"* — this is news + community
- *"X 社区在聊什么"*, *"long port community on NVDA"*
- *"X 全面综述"* (default omnibus)

## Depth selection

| Prompt cue | Tools |
|---|---|
| 新闻 / news / "最近怎么了" | `news` only |
| 搜索新闻 / search news / keyword news | `news search <keyword>` |
| 公告 / 披露 / filing / 8-K / 中报 | `filings` only |
| 市场怎么看 / market reaction / sentiment | `news` + `topic` |
| 社区 / community / discussion | `topic` (+ `topic detail`, `topic replies` for hot topics) |
| 搜索社区 / search community topics | `topic search <keyword>` |
| 全面 / 综述 / overview (default) | `news` + `filings` + `topic` (concurrent) |

## CLI

Run `longbridge <subcommand> --help` to verify exact flags. Default omnibus example (run concurrently):

```bash
longbridge news NVDA.US --format json
longbridge filing NVDA.US --format json
longbridge topic NVDA.US --format json
```

Keyword search (no symbol required):

```bash
longbridge news search "AI chips" --format json        # search news by keyword
longbridge topic search "NVDA earnings" --format json  # search community topics by keyword
```

## Workflow

1. Resolve symbol; if mapping fails, ask back (this is common with small-caps).
2. Pick depth (table above) and call CLI commands concurrently (see CLI section). If `longbridge` is not installed, fall back to MCP.
3.

4. **Classify the news array** into 6 buckets (mandatory — never dump raw titles):

   | Bucket | Cues |
   |---|---|
   | **catalyst** (业绩 / 基本面) | earnings, revenue, guidance, EPS, 财报, 营收, 利润 |
   | **regulatory** (监管 / 合规) | SEC, 证监会, fine, lawsuit, 调查, 处罚, 罚款 |
   | **strategic** (战略 / 业务) | acquisition, partnership, launch, 收购, 拆分, 新产品 |
   | **financial** (资本动作) | buyback, split, dividend, 增发, 回购, 股权激励 |
   | **opinion** (评级 / 目标价) | upgrade, downgrade, analyst, 评级, 目标价 |
   | **other** | unclassified |

5. Render the structured summary (template below). Skip empty buckets but **always include the key-takeaway summary** (≤ 100 chars, fact-only).

## Output template

```
{Symbol} ({code}) news digest — Source: Longbridge Securities

[Past N days · M news + K filings]

🟢 Earnings / fundamentals (N)
- [date] headline — one fact (number / ratio)

🟡 Strategic / business (N)
- [date] ...

🔴 Regulatory / compliance (N)
- [date] ...

📈 Analyst opinions (N)
- [date] {rating} by {bank}; target {currency} Y (was Z)

📃 Filings
- [date] 8-K / interim / earnings preview / ...

💬 Community discussion (when topic was queried)
- N hot topics: {title} — {comment count}
- Sentiment skew: positive / neutral / negative — coarse %

[Key facts] (≤ 100 chars, neutral)
- ...

⚠️ 以上数据仅供参考，不构成投资建议。/ 以上數據僅供參考，不構成投資建議。/ For reference only. Not investment advice.
```

(Translate into the user's language.)

## WebSearch fallback (optional)

Use **only** when:

- MCP `news` returns empty, **or**
- the latest item is > 7 days old, **or**
- the user asks about a breaking event the MCP dataset has not yet captured.

When you do, prepend: *"Below is from a web search — not Longbridge data."* / *"以下为网络搜索结果,非长桥数据。"* / *"以下為網絡搜尋結果,非長橋數據。"*

## Output constraints

- **Must** classify into the 6 buckets — never dump raw titles.
- **Must** include the key-takeaway summary (≤ 100 chars, fact-only).
- **Must** end with the not-investment-advice disclaimer.
- 给有证据的方向性判断，例如 *"市场普遍将此解读为正面 / 负面"*；避免只贴 "利好 / 利空" 标签而不附事实。
- **Do not** quote individual community comments verbatim (cherry-pick risk); report sentiment as a coarse skew.
- **Do not** invent news. If MCP is sparse, say so and offer WebSearch.

## Compliance: hype vocabulary

If `topic` / `topic_replies` content contains a high density of hype words — *"涨停板"*, *"主升浪"*, *"必涨"*, *"满仓"*, *"all in"*, *"庄家"*, *"次新妖股"* — do not echo them. Downgrade to *"discussion contains a notable share of speculative posts"* and move on.

## Error handling

| Situation | Reply |
|---|---|
| `command not found: longbridge` | Fall back to MCP; if MCP also unavailable, tell user to install longbridge-terminal. |
| `news` returns empty | "{symbol} has no recent news in Longbridge data — switching to WebSearch (note: web data, not Longbridge)." |
| `news` > 7 days stale | Same — note the staleness explicitly. |
| Symbol mapping fails | Ask the user for the code or English ticker. |
| stderr `not logged in` | Tell user to run `longbridge auth login`. |

## MCP fallback

If `longbridge` CLI is not installed (`command not found`), use MCP tools instead:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP setup: `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` (`quote` scope).

## Related skills

- Earnings detail → `longbridge-fundamental`
- Whether valuation has priced in the news → `longbridge-valuation`
- Cross-stock impact → `longbridge-peer-comparison`

## File layout

```
longbridge-news/
└── SKILL.md          # prompt-only, no scripts/
```
