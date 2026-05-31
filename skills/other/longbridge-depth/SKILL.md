---
name: longbridge-depth
description: |
  Orderbook depth (5/10-level bid/ask), broker queue (HK only), and tick-by-tick trades for stocks via Longbridge Securities. Use for orderbook microstructure questions. Triggers: "盘口", "买卖盘", "5 档", "10 档", "深度", "经纪商队列", "逐笔", "tick", "成交明细", "盤口", "買賣盤", "5 檔", "10 檔", "經紀商隊列", "逐筆", "成交明細", "depth", "orderbook", "level 2", "broker queue", "tick data", "trades", "time and sales".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-depth

Orderbook depth, broker queue (HK-only), and tick-by-tick trades.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## Subcommands

| Subcommand | Returns |
|---|---|
| `depth` | 5 / 10-level orderbook: per-level price / volume / order_num |
| `brokers` | Per-level broker_id queue (**HK only**). Tell the user the queue is HK-only when they ask about a non-HK symbol. |
| `trades` | Latest N trades: time / price / volume / direction / type. Pass `--count 1..1000`. |

`broker_id` integers can be translated to names via `longbridge-security-list` → `participants`.

## When to use

- *"看下 700.HK 的盘口"*, *"TSLA 5 档买卖盘"* → `depth`
- *"茅台经纪商队列"* — non-HK symbol → tell user *"broker queue is HK-only"* and switch to `depth`
- *"NVDA 最近 50 笔成交"*, *"腾讯 tick 数据"* → `trades --count 50`
- *"700 全部盘口"*, *"microstructure overview"* → call `depth`, `brokers` (if HK), and `trades` and merge the results

## Workflow

1. Resolve the symbol to `<CODE>.<MARKET>`.
2. Pick the subcommand by user intent (table above). For an "overview" intent, run `depth` + `brokers` (HK-only) + `trades` and merge.
3. **Off-hours warning**: outside trading hours, `depth` is the closing snapshot and `trades` are the last N of the previous session — call this out explicitly when responding.
4. Call the Longbridge CLI directly (preferred) or fall back to MCP.
5. Render `depth` as a bid / ask table; describe `trades` as a direction summary (buy-dominant / sell-dominant) plus the latest few rows. Cite Longbridge Securities.

## CLI

```bash
longbridge depth   700.HK                  --format json
longbridge brokers 700.HK                  --format json   # HK-only
longbridge trades  700.HK --count 50       --format json
```

Always pass `--format json` so the output is machine-parseable.

## Output

- `depth` / `brokers`: `{asks: [...], bids: [...]}` (`brokers[i]` includes a `broker_id` array)
- `trades`: array of trade rows (`time / price / volume / direction / type`)

## Error handling

If `longbridge` is missing, fall back to MCP. If stderr surfaces *"broker queue not supported"* / *"non-HK"* on a `brokers` call, explain that broker queues are HK-only and switch to `depth`. Other stderr messages (auth / invalid symbol) get relayed verbatim.

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP-only extensions are available; discover them from the MCP server's tool list at runtime.

## Related skills

- Quote / static / indices → `longbridge-quote`
- Capital flow / large-order distribution → `longbridge-capital-flow`
- broker_id → name lookup → `longbridge-security-list`

## File layout

```
longbridge-depth/
└── SKILL.md          # prompt-only, no scripts/
```
