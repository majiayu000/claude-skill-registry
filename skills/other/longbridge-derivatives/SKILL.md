---
name: longbridge-derivatives
description: |
  Options (US / HK) and Hong Kong warrants (callable bull/bear, call warrants, put warrants) via Longbridge Securities — option quote, option chain by underlying / expiry, option volume, warrant quote / list / issuers. Returns IV, Greeks, strikes, expiries. Triggers: "期权", "option", "call", "put", "认购", "认沽", "行权价", "到期日", "IV", "希腊字母", "delta", "gamma", "窝轮", "牛熊证", "认购证", "认沽证", "認購", "認沽", "行權價", "到期日", "窩輪", "牛熊證", "option chain", "options expiry", "warrant", "CBBC", "callable bull bear contract".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-derivatives

Options (US / HK) and HK warrants. Underlying-stock quotes belong in `longbridge-quote`.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## Subcommands

> `option` and `warrant` are **parent commands**; each has its own sub-subcommands. Run `longbridge option --help` / `longbridge warrant --help` to see the current sub-subcommand list and their flags.

| CLI command | Returns |
|---|---|
| `longbridge option quote <CONTRACT>... --format json` | Quote(s) for one or more option contracts (OCC symbols). Includes IV, delta, strike, expiry. |
| `longbridge option chain <UNDERLYING> --format json` | Available expiry dates for the underlying. |
| `longbridge option chain <UNDERLYING> --date YYYY-MM-DD --format json` | Strikes for a specific expiry — each row gives `call_symbol` and `put_symbol` OCC codes. |
| `longbridge option volume <UNDERLYING> --format json` | Real-time call / put volume snapshot (use `longbridge option volume daily ...` for historical). |
| `longbridge warrant <UNDERLYING> --format json` | Default warrants list for an underlying (HK only). |
| `longbridge warrant quote <WARRANT>... --format json` | Quote(s) for HK warrants (leverage, IV, etc.). |
| `longbridge warrant issuers --format json` | Directory of HK warrant issuers. |

## OCC option symbol

Format: `<TICKER><YYMMDD><C|P><STRIKE×1000, 8 digits>`. Example: `AAPL240119C190000` = AAPL, expires 2024-01-19, Call, strike $190.00.

## Two-step option discovery

| User input | Strategy |
|---|---|
| Full OCC symbol | `option quote <symbol>` directly |
| Underlying + expiry + strike + call/put | `option chain <UL> --date <d>` to find OCC code → `option quote` |
| Underlying + window only | `option chain <UL>` to list expiries; ask user to pick |

## Term mapping

| User says | Term |
|---|---|
| 认购证 / 牛证 / call | Call |
| 认沽证 / 熊证 / put | Put |
| 行权价 / strike | Strike |
| 到期日 / expiry | Expiry |
| 隐含波动率 / IV | Implied volatility |

## CLI

```bash
longbridge option quote     AAPL250117C190000 AAPL250117P190000  --format json
longbridge option chain     AAPL.US                              --format json
longbridge option chain     AAPL.US --date 2025-01-17            --format json
longbridge option volume    AAPL.US                              --format json
longbridge warrant          700.HK                               --format json
longbridge warrant quote    12345.HK                             --format json
longbridge warrant issuers                                       --format json
```

## Output (per subcommand)

- `option quote`: array of contract rows (each: IV, delta, strike, expiry, …).
- `option chain` (no date): array of `{expiry_date}`.
- `option chain --date`: array of `{strike, call_symbol, put_symbol, standard}`.
- `option volume`: real-time call / put volume snapshot.
- `warrant <UNDERLYING>`: array of warrant rows for that underlying.
- `warrant quote`: array of quote rows.
- `warrant issuers`: array of `{id, name_(cn), name_(en)}`.

## When to clarify

- Warrant query on a non-HK underlying → tell the user "warrants are HK-only" and route appropriately.
- Long strike list (>30) → present near-the-money strikes only.
- IV / Greeks during off-hours → may be a previous-session snapshot; mention this if the user asks for "real-time".

## MCP fallback

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

## Error handling

If `longbridge` is missing, fall back to MCP. *"no quote access"* on `option quote` indicates the account lacks the options market-data subscription — surface the message verbatim and tell the user to upgrade quote permissions on Longbridge.

## Related skills

- Underlying quote / static → `longbridge-quote`
- Underlying candlesticks → `longbridge-kline`
- Underlying orderbook depth → `longbridge-depth`

## File layout

```
longbridge-derivatives/
└── SKILL.md          # prompt-only, no scripts/
```
