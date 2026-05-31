---
name: longbridge-valuation-rank
description: |
  Industry valuation rank time series for a single stock via Longbridge — tracks how a stock's PE / PB / PS / dividend-yield rank within its sector has changed over time (rank N of total M). Answers "is my stock becoming relatively cheaper or more expensive vs peers?" Complements longbridge-valuation (single-stock percentile history) and longbridge-industry-valuation (current sector snapshot). Triggers: "行业排名变化", "估值排名", "PE排名历史", "行业估值位置", "排名走势", "估值相对同业", "行業排名變化", "估值排名", "PE排名歷史", "行業估值位置", "排名走勢", "valuation rank", "industry rank history", "PE rank trend", "relative valuation rank", "sector ranking over time", "how does AAPL rank in industry PE".
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

# longbridge-valuation-rank

Prompt-only skill. Fetches the **time series of a stock's valuation rank within its industry** — each data point shows where the stock sits among peers (e.g., rank 3 out of 28) for PE, PB, PS, and dividend yield.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"AAPL 在行业里 PE 排名怎么变化的"*, *"AAPL industry PE rank over time"*, *"AAPL 在行業裡 PE 排名怎麼變化"*
- *"茅台估值相对同业是在改善还是恶化"*, *"is Maotai getting cheaper relative to peers"*
- *"NVDA PB 行业排名走势"*, *"NVDA PB sector rank trend"*, *"NVDA PB 行業排名走勢"*
- *"700.HK 股息率行业位置历史"*, *"700.HK dividend yield rank history"*

For a current single-stock snapshot (not a trend) → `longbridge-valuation`.  
For today's full sector comparison → `longbridge-industry-valuation`.  
For multi-symbol comparison → `longbridge-peer-comparison`.

## CLI

Run `longbridge valuation-rank --help` to verify exact flags. Common calls:

```bash
# Past 1 year (default) — PE / PB / PS / dividend-yield ranks
longbridge valuation-rank AAPL.US --format json

# Custom date range
longbridge valuation-rank AAPL.US --start 20250101 --end 20251231 --format json
longbridge valuation-rank 700.HK --start 20240101 --end 20251231 --format json

# Help — always verify flags
longbridge valuation-rank --help
```

## Workflow

1. **Resolve symbol** to `<CODE>.<MARKET>` format.
2. **Run** `longbridge valuation-rank <SYMBOL> --format json` (add `--start` / `--end` if the user specifies a range; otherwise omit for the default 1-year window).
3. **Parse** the time series. Each data point includes a `timestamp` and sub-objects for `pe`, `pb`, `ps`, `dvd` — each containing `rank` and `total`.
4. **Compute trend** for each indicator:
   - Direction: is rank rising (improving relative valuation) or falling (deteriorating)?
   - Percentile at each point: `(total − rank + 1) / total × 100%` → lower rank = lower PE = cheaper.
   - Identify any notable inflection points (large rank jumps).
5. **Present** as a summary table + trend narrative; omit indicators where data is sparse.

## Output

**AAPL.US — Industry valuation rank history (past 1 year)**  
Source: Longbridge Securities

```
Date       | PE rank | PB rank | PS rank | Dvd rank | Peers (n)
2025-01-31 |  8 / 32 |  5 / 32 | 12 / 32 |  28 / 32 | 32
2025-02-28 |  9 / 32 |  5 / 32 | 11 / 32 |  27 / 32 | 32
…
```

*Trend summary*: PE rank improved from 12→8 (valuation became relatively cheaper vs peers) over the period; dividend yield rank remained near bottom (low yield vs peers).

⚠️ 排名数据仅供参考，不构成投资建议。  
⚠️ 排名數據僅供參考，不構成投資建議。  
⚠️ For reference only. Not investment advice.

## Error handling

| Situation | 简体中文回复 | 繁體中文 / English |
|---|---|---|
| `command not found: longbridge` | 回退到 MCP；如也不可用，请安装 longbridge-terminal。 | 回退到 MCP；如也不可用，請安裝 longbridge-terminal。/ Fall back to MCP; if unavailable, install longbridge-terminal. |
| `valuation-rank` returns empty | "{symbol} 暂无行业估值排名数据，可能不支持该市场或标的。" | "{symbol} 暫無行業估值排名。" / "{symbol} has no industry valuation rank data." |
| `total` = 0 or null | 跳过该指标，注明无同行数据。 | 跳過該指標，注明無同行數據。/ Skip the indicator and note no peer data. |
| Other stderr | 直接显示原始错误，不静默重试。 | 顯示原始錯誤。/ Surface verbatim — do not retry silently. |

## MCP fallback

If `longbridge` CLI is unavailable (`command not found`), use MCP tools:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP setup: `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` (`quote` scope).

## Related skills

- Single-stock historical percentile (absolute) → `longbridge-valuation`
- Current sector snapshot (today's comparison) → `longbridge-industry-valuation`
- Multi-symbol comparison matrix → `longbridge-peer-comparison`
- Full fundamentals → `longbridge-fundamental`

## File layout

```
longbridge-valuation-rank/
└── SKILL.md   # prompt-only, no scripts/
```
