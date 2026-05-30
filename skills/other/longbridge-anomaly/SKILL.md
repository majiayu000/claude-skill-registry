---
name: longbridge-anomaly
description: |
  Market anomaly scanner and price-by-volume distribution via Longbridge Securities — `anomaly` lists unusual price/volume movements across a market (HK / US / CN / SG) or for a specific symbol; `trade-stats` returns a single stock's intraday price-volume profile (where volume sat in the day's range). Read-only. Triggers: "异动", "今天哪些股票异动", "市场异动榜", "成交分布", "价格分布", "筹码分布", "今日筹码", "成交密集区", "盘中异动", "拉升", "跳水", "閃崩", "異動", "今天哪些股票異動", "市場異動榜", "成交分佈", "價格分佈", "籌碼分佈", "今日籌碼", "成交密集區", "盤中異動", "拉昇", "跳水", "anomaly", "unusual movements", "intraday alerts", "volume spike", "price spike", "price by volume", "trade distribution", "volume profile", "VWAP zone", "where the volume sat", "TSLA anomaly", "700.HK anomaly".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-anomaly

Two complementary intraday lenses: market-wide unusual movements (`anomaly`) and a single stock's price-by-volume distribution (`trade-stats`).

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"今天港股有什么异动"*, *"US anomaly today"*, *"市场异动榜"* → `anomaly --market <MKT>`
- *"TSLA 今天有没有异动"*, *"700.HK 异动"* → `anomaly --market <MKT> --symbol <SYMBOL>`
- *"AAPL 今日筹码分布"*, *"成交密集区"*, *"price by volume"*, *"volume profile"* → `trade-stats <SYMBOL>`
- *"X 拉升的位置在哪"*, *"成交都堆在哪个价位"* → `trade-stats`

For tick-by-tick trade ribbon → `longbridge-depth` (`trades`). For intraday capital flow (large/medium/small orders) → `longbridge-capital-flow`. For market-level mood → `longbridge-market-temp`.

## Subcommands

> Run `longbridge anomaly --help` and `longbridge trade-stats --help` if unsure of current flags. The CLI's built-in help is the canonical source.

| CLI command | Returns |
|---|---|
| `longbridge anomaly --market <HK\|US\|CN\|SG> --format json` | List of unusual movements in that market (default `HK`, `--count` up to 100, default 50). |
| `longbridge anomaly --market <MKT> --symbol <SYMBOL> --format json` | Anomalies filtered to a specific symbol. |
| `longbridge trade-stats <SYMBOL> --format json` | Intraday price-by-volume distribution for the symbol — bucketed price levels with the volume traded at each. |

## Workflow

1. Decide the lens:
   - **Market scan** → `anomaly --market`. Default to `HK` if the user does not specify.
   - **Single-symbol scan** → `anomaly --market <MKT> --symbol`.
   - **Volume profile** → `trade-stats <SYMBOL>`.
2. Resolve symbol → `<CODE>.<MARKET>` and infer market for `--market`.
3. Call the CLI; render a structured summary (see Output).
4. Cite **Longbridge Securities** and the data timestamp.

## CLI

```bash
# Market-wide anomaly board
longbridge anomaly --market HK                                --format json
longbridge anomaly --market US --count 100                    --format json

# Single-symbol anomaly
longbridge anomaly --market US --symbol TSLA.US               --format json

# Price-by-volume distribution
longbridge trade-stats 700.HK                                 --format json
longbridge trade-stats AAPL.US                                --format json
```

If `--help` shows newer flags, follow the help output rather than hard-coding here.

## Output

Render in the user's language.

**`anomaly`** — table grouped by anomaly type (e.g. *spike up / spike down / volume surge / 60-day high / 60-day low*): time / symbol / name / type / price / change %. For a market scan, sort within each group by time (most recent first) or by magnitude.

**`trade-stats`** — price-bucket distribution. Suggested layout:

```
{Symbol} ({code}) intraday price-by-volume — Source: Longbridge Securities

Total volume: V    | Total turnover: T    | VWAP: P

Top 5 volume buckets (where the volume sat):
- price [a–b]: vol X (Y% of day) ▇▇▇▇▇
- ...

Day high / low: H / L
Most-traded zone: [a–b]   (this is the heaviest range, not "support / resistance")
```

Do **not** call any range "support" or "resistance" — that is interpretive. Stick to *"heaviest-traded zone"*. State the timestamp.

When a result is empty (no anomalies, or no volume data yet), state so explicitly.

## Error handling

| Situation | Reply |
|---|---|
| Shell `command not found: longbridge` | Fall back to MCP if configured; otherwise tell the user to install longbridge-terminal. |
| stderr `not logged in` / `unauthorized` | Hint `longbridge auth login`. |
| Empty `anomaly` list | *"No anomalies detected for this market/symbol right now."* |
| `trade-stats` empty (pre-market / new listing) | *"No intraday volume data yet — try after the session opens."* |
| Symbol mapping fails | Ask for `<CODE>.<MARKET>`. |
| Other stderr | Relay verbatim — never silently retry. |

## MCP fallback

When the CLI binary is missing, fall back via the equivalent MCP tool. Tool names typically mirror CLI subcommand names (snake_case).

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

If a name above does not resolve, fall back via the equivalent MCP tool when CLI is missing.

## Related skills

| Skill | Why |
|---|---|
| `longbridge-quote` | Live price + change behind the anomaly. |
| `longbridge-capital-flow` | Whose money drove the move (large / medium / small orders). |
| `longbridge-depth` | Tick-by-tick trades and orderbook microstructure. |
| `longbridge-news` | News / filings that could explain the spike. |
| `longbridge-catalyst-radar` | Watchlist-scoped briefings that aggregate anomalies. |

## File layout

```
longbridge-anomaly/
└── SKILL.md          # prompt-only, no scripts/
```
