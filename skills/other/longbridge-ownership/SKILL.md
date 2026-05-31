---
name: longbridge-ownership
description: |
  Share structure and shareholder query — total shares, circulating shares, restricted shares, top-10 shareholders (circulating and total), major institutional holders, controlling shareholder / beneficial owner relationships. Shareholder count and pledge data are not available via Longbridge; check filings for those. Triggers: "股本结构", "前十大股东", "流通股东", "实控人", "股权结构", "主要持股人", "大股东", "股东查询", "股本結構", "前十大股東", "流通股東", "實控人", "股權結構", "主要持股人", "大股東", "shareholder structure", "major shareholders", "top 10 shareholders", "controlling shareholder", "share structure", "institutional holders", "beneficial owner", "ownership structure", "free float".
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

# longbridge-ownership

Share structure and shareholder query for Longbridge-covered securities — total/circulating/restricted shares, top-10 shareholders, major institutional holders, and controlling shareholder/beneficial owner relationships.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger when the user asks about:

- Share structure (total, circulating, restricted/locked-up) — *"腾讯总股本是多少"*, *"AAPL 流通股"*
- Top-10 shareholders — *"苹果前十大股东"*, *"700.HK 大股东是谁"*
- Controlling shareholder / actual controller — *"实控人是谁"*, *"谁控制这家公司"*
- Institutional holder relationships — *"持有茅台的机构"*, *"AAPL 主要机构持股"*
- Equity investment relationships — *"母公司/子公司持股"*

For insider trade history (SEC Form 4), defer to `longbridge-flows`. For full executive / board profiles, defer to `longbridge-corporate`. For 13F institutional portfolios, defer to `longbridge-flows`.

## Workflow

1. Normalise the symbol to `<CODE>.<MARKET>`.
2. Run `longbridge static` to get total shares, circulating shares, and free float from static reference data.
3. Run `longbridge shareholder` for the top-10 shareholders list (circulating and total).
4. Run `longbridge invest-relation` for parent-subsidiary equity investment relationships.
5. Merge and present a structured shareholder profile; note any data gaps (pledge data, exact shareholder count) and direct the user to company filings.

## CLI

```bash
# Share structure (total shares, circulating shares)
longbridge static <SYMBOL> --format json

# Top-10 shareholders
longbridge shareholder <SYMBOL> --format json

# Equity investment relationships (parent / subsidiary / associate)
longbridge invest-relation <SYMBOL> --format json
```

> Run `longbridge shareholder --help` and `longbridge invest-relation --help` to verify flags before calling.

## Output

Present as two sections:

**1. Share structure**

| Field | 简体 | 繁體 | English |
|---|---|---|---|
| Total shares | 总股本 | 總股本 | Total shares |
| Circulating shares | 流通股 | 流通股 | Circulating shares |
| Restricted shares | 限售股 | 限售股 | Restricted shares |

**2. Top-10 shareholders** — name, shareholding quantity, shareholding %, change since last period.

If pledge data or shareholder headcount is requested but unavailable, note: *"该数据暂不可用，建议查阅公司公告"* / *"Data unavailable; check company filings."*

## Error handling

| Situation | 简体回复 | 繁體回覆 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 请先安装 longbridge-terminal | 請先安裝 longbridge-terminal | Install longbridge-terminal first |
| `not logged in` | 请运行 `longbridge auth login` | 請執行 `longbridge auth login` | Run `longbridge auth login` |
| No shareholder data | 提示该标的暂无股东数据 | 提示該標的暫無股東數據 | No shareholder data available |
| Other stderr | 原样展示，不重试 | 原樣展示，不重試 | Surface verbatim, do not retry |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime.

## Related skills

| User asks | Route to |
|---|---|
| Executives / board / corporate profile | `longbridge-corporate` |
| 13F institutional portfolios / insider trades | `longbridge-flows` |
| Filings for pledge or headcount data | `longbridge-news` |
| Share structure + basic listing info | `longbridge-basicinfo` |

## File layout

```
longbridge-ownership/
└── SKILL.md
```

Prompt-only — no `scripts/`. Discover current CLI flags via `longbridge <subcommand> --help`.
