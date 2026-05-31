---
name: longbridge-flows
description: |
  Smart-money and ownership-flow signals for a single stock via Longbridge Securities — SEC 13F institutional portfolios + position changes (US), funds and ETFs that hold the stock, SEC Form 4 insider trades (US-only), US short-interest history, and HK broker holdings (HK-only). Read-only. Markets vary by subcommand. Triggers: "13F", "机构持仓", "基金持仓", "ETF 持有", "持有这只股票的基金", "内部人交易", "高管买卖", "Form 4", "做空数据", "空头", "卖空", "经纪商持仓", "中央结算", "13F", "機構持倉", "基金持倉", "ETF 持有", "持有這隻股票的基金", "內部人交易", "高管買賣", "做空數據", "空頭", "賣空", "經紀商持倉", "中央結算", "13F holdings", "institutional holders", "fund holders", "ETF holders", "insider trades", "insider buying", "insider selling", "Form 4", "short interest", "days to cover", "short ratio", "broker holding", "CCASS", "AAPL insider sales", "TSLA short interest", "700.HK broker holding".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-flows

Single-symbol ownership and money-flow lens: who's buying/selling at the institutional, fund, insider, broker, and short-seller layers.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"13F 谁持仓最多", "Berkshire 13F", "巴菲特最新持仓", "active fund AUM ranking"* → `investors`
- *"哪些基金持有 NVDA", "AAPL 被多少 ETF 持有"* → `fund-holder`
- *"TSLA 高管最近买入", "AAPL Form 4", "内部人减持"* → `insider-trades` (US only)
- *"AMD 空头数据", "TSLA 做空比例", "days to cover"* → `short-positions` (US only)
- *"700.HK 中央结算", "腾讯经纪商持仓", "broker holding 700"* → `broker-holding` (HK only)
- *"X 资金面全景"* → call multiple subcommands by market (US: `fund-holder` + `insider-trades` + `short-positions`; HK: `fund-holder` + `broker-holding`).

For intraday large/medium/small-order capital flow → `longbridge-capital-flow`. For institutional shareholders by % held → `longbridge-corporate` (`shareholder`).

## Subcommands

> Run `longbridge <subcommand> --help` if unsure of current flags. The CLI's built-in help is the canonical source.

| Capability | Returns | Markets |
|---|---|---|
| Fund-manager AUM rankings (no symbol) | Live active fund-manager rankings by AUM. | global |
| 13F holdings for a manager (by CIK) | Latest 13F holdings snapshot; run `--help` for count/filter flags. | US (SEC EDGAR) |
| 13F quarter-over-quarter changes | Position changes (NEW / ADDED / REDUCED / EXITED). | US |
| Funds and ETFs holding a symbol | Fund name, ticker, currency, weight, report date; run `--help` for count flags. | global |
| SEC Form 4 insider trades | BUY / SELL / GRANT / DISP / TAX / EXERCISE / GIFT; run `--help` for count flags. | **US only** |
| Short interest history | Short interest, short ratio, days to cover; run `--help` for range flags. | **US only** |
| Broker holdings over a period | Top buy / sell brokers; run `--help` for period options. | **HK only** |
| Broker holdings detail | Full broker-holding detail list. | HK only |
| Daily holding history for a broker | Single broker's daily history; run `--help` for broker-filter flags. | HK only |

Single symbol per call (except `investors` rankings).

## Workflow

1. Resolve to `<CODE>.<MARKET>`. Reject US-only subcommands for non-US, HK-only for non-HK — explain politely.
2. Pick subcommands by prompt cue. Don't run all of them by default.
3. Call concurrently when the question is *"全景资金面"* style.
4. Summarise direction (net buying / net selling), top names, freshness (report date).
5. Cite **Longbridge Securities** (and SEC EDGAR for `insider-trades` / `investors`).

## CLI

```bash
# Discover available subcommands and their flags first
longbridge --help
longbridge <subcommand> --help   # run for each subcommand before use

longbridge <investors-subcommand> --format json                   # AUM rankings (no CIK)
longbridge <investors-subcommand> 1067983 --format json           # Berkshire 13F
longbridge <investors-changes-subcommand> 1067983 --format json   # QoQ changes
longbridge <fund-holder-subcommand> AAPL.US --format json
longbridge <insider-trades-subcommand> TSLA.US --format json      # US only
longbridge <short-positions-subcommand> AAPL.US --format json     # US only
longbridge <broker-holding-subcommand> 700.HK --format json       # HK only
longbridge <broker-holding-detail-subcommand> 700.HK --format json
longbridge <broker-holding-daily-subcommand> 700.HK --format json
```

## Output

Render in the user's language. Suggested layouts:

**13F (`investors`)** — when no CIK: AUM-ranked manager table. With CIK: top-N positions (ticker / value / shares / weight / change vs last filing). For `changes`: NEW / ADDED / REDUCED / EXITED grouped lists.

**`fund-holder`** — table sorted by weight: fund name / ticker / currency / weight % / report date. Highlight high-weight funds (> 1%).

**`insider-trades`** — chronological list (most recent first): date / insider / role / type (BUY/SELL/GRANT/...) / shares / price / value. Net buy vs sell summary at top.

**`short-positions`** — time-series table: date / short interest / short ratio / days-to-cover. Note trend (rising / falling).

**`broker-holding`** — for the `--period` view: top buy brokers and top sell brokers side by side. For `detail`: full list. For `daily`: a single broker's history.

When a result is empty, state so. Do not invent.

## Error handling

| Situation | Reply |
|---|---|
| Shell `command not found: longbridge` | Fall back to MCP if configured; otherwise tell the user to install longbridge-terminal. |
| Non-US symbol passed to `insider-trades` / `short-positions` | Reply *"This subcommand only supports US-listed equities."* |
| Non-HK symbol passed to `broker-holding` | Reply *"Broker holding is HK-only."* |
| Empty result | State explicitly. Do not invent. |
| Other stderr | Relay verbatim — never silently retry. |

## MCP fallback

When the CLI binary is missing, fall back via the equivalent MCP tool. Tool names typically mirror CLI subcommand names (snake_case).

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

If a name above does not resolve, fall back via the equivalent MCP tool when CLI is missing.

## Related skills

| Skill | Why |
|---|---|
| `longbridge-corporate` | Major shareholder % structure (a different lens than 13F flow). |
| `longbridge-capital-flow` | Today's intraday large/medium/small-order distribution. |
| `longbridge-news` | Filings (8-K / 13D / 13G) often pair with flow events. |
| `longbridge-fundamental` | Earnings + dividend backdrop for insider context. |
| `longbridge-quote` | Live price for sizing the flow. |

## File layout

```
longbridge-flows/
└── SKILL.md          # prompt-only, no scripts/
```
