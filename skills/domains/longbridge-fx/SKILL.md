---
name: longbridge-fx
description: |
  Foreign-exchange rates for all currencies supported by Longbridge Securities — HKD / USD / CNY / SGD / EUR / GBP / JPY / etc. Use to convert multi-currency holdings, normalise account values, or quote a cross-rate. Light-touch utility skill, no login required. Triggers: "汇率", "美元兑港币", "人民币兑美元", "港币换美金", "今天汇率", "USD HKD", "CNY USD", "外汇", "匯率", "美元兌港幣", "人民幣兌美元", "港幣換美金", "今天匯率", "外匯", "exchange rate", "fx rate", "currency conversion", "USD to HKD", "HKD to USD", "CNY to USD", "JPY to USD", "convert HKD to USD", "1 USD in HKD".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-fx

Foreign-exchange rates for all currencies Longbridge supports.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"今天美元兑港币多少"*, *"USD to HKD today"* → run, look up `USD/HKD` row.
- *"100 港币能换多少美金"* → run, compute `100 / (USD/HKD)` (or `100 * (HKD/USD)`, depending on the row's quote convention).
- *"我组合里 HKD / USD / CNY 都有，统一换算成 USD"* → run once, normalise each currency leg.
- *"人民币兑美元 / CNH vs CNY"* → check whether the row is `CNY/USD` or `CNH/USD`; surface the symbol verbatim.

For cross-rates not directly listed, derive from two USD-quoted rows (e.g. `EUR/JPY = (EUR/USD) / (JPY/USD)`).

## Subcommand

> Single CLI command, no arguments beyond format. Run `longbridge exchange-rate --help` if unsure of current flags.

```bash
longbridge exchange-rate --format json
```

There are no per-currency filters — the command returns the full table; pick the row(s) you need from the JSON.

## Workflow

1. Run `longbridge exchange-rate --format json`.
2. Find the row matching the user's pair (mind the quote convention: `BASE/QUOTE` is "1 BASE = N QUOTE").
3. If user wants a specific amount, do the arithmetic inline; show both rate and computed amount.
4. If the user's pair isn't directly quoted, derive via USD: `A/B = (A/USD) / (B/USD)`.
5. Cite source as **Longbridge Securities** / **数据来源:长桥证券** / **數據來源:長橋證券**, plus the as-of timestamp from the response if provided.

## CLI examples

```bash
# Full rate table
longbridge exchange-rate --format json
```

That's it — there's no symbol argument. Filter on the JSON client-side.

## Output

JSON array, one row per supported pair. Typical fields:

| Field | Meaning |
|---|---|
| `symbol` / `pair` | e.g. `USD/HKD`, `CNY/USD` |
| `rate` | numeric exchange rate |
| `timestamp` | as-of time |

Render the relevant row(s) only; don't dump the full table unless the user asked for it.

## Error handling

| Situation | LLM response |
|---|---|
| Shell `command not found: longbridge` | Fall back to MCP if configured; otherwise tell the user to install longbridge-terminal. |
| Empty array | Unusual — relay verbatim and tell the user to retry shortly. |
| Pair not in response | "Longbridge doesn't quote `<X/Y>` directly — derive from `X/USD` and `Y/USD`." |
| Other stderr | Surface verbatim. |

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

## Related skills

| User asks | Route to |
|---|---|
| Multi-currency holdings normalised to one base | `longbridge-positions` then convert with this skill |
| Account-level performance with currency exposure | `longbridge-portfolio` |
| Statement export with FX legs | `longbridge-statement` |
| Stock quote in native currency | `longbridge-quote` |

## File layout

```
longbridge-fx/
└── SKILL.md          # prompt-only, no scripts/
```
