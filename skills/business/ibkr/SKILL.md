---
name: ibkr
description: Trade and research options on Interactive Brokers via a local CLI (chains, quotes, Greeks, single-leg and vertical orders). Use when the user asks about option chains, option quotes, or wants to place/cancel option orders on IBKR. Requires IB Gateway running locally. Paper account is the default; live needs --live.
---

# IBKR Options Trading

All commands run as `ibkr <command>`. If `ibkr` is not on PATH, install it
(requires Python 3.11+ and [uv](https://github.com/astral-sh/uv)):

    git clone https://github.com/baileywickham/ibkr
    cd ibkr && uv tool install --editable .

Output is JSON. Exit codes: 0 ok, 2 gateway unreachable,
3 validation error, 4 token rejected, 5 account error, 6 delayed-data blocked.

**Mode**: paper account by default (Gateway port 4002). Add `--live` (port 4001) ONLY
when the user explicitly says to trade the live account.

## Commands

```
ibkr status                          # connection + account summary
ibkr positions | orders | trades
ibkr chain AAPL                      # expirations
ibkr chain AAPL --expiry 2026-07-17 --strikes 8   # strikes around spot, quotes + Greeks
ibkr quote AAPL                      # stock quote
ibkr quote AAPL --expiry 2026-07-17 --strike 200 --right C   # option quote
ibkr place --symbol AAPL --expiry 2026-07-17 --strike 200 --right C \
           --side BUY --qty 1 --limit 3.50        # PREVIEW (never trades)
ibkr place ... --execute TOKEN                    # place previewed order
ibkr place-vertical --symbol AAPL --expiry 2026-07-17 --right C --side BUY \
           --long-strike 200 --short-strike 205 --qty 1 --limit 1.80
ibkr stock --symbol AAPL --side BUY --qty 10 --limit 250     # shares (preview/execute)
ibkr cancel ORDER_ID
ibkr close 355C              # PREVIEW closing one position (match by symbol)
ibkr close --all            # PREVIEW closing every position
ibkr close 355C --execute TOKEN          # place the closing order(s)
ibkr close --all --limit 0.02            # override the closing limit price
```

Limit orders only; market orders are intentionally not implemented.
For verticals, `--limit` is the net debit (BUY) or net credit (SELL), always positive.

`close` builds an offsetting order priced marketably at the current bid/ask
(SELL to close a long, BUY to close a short). A long/short option pair on one
underlying is recognized as a spread and closed as a SINGLE net-priced combo —
so `--limit` is the net price for the whole spread, not a per-leg price (a
per-leg limit would make the buy-to-close leg marketable and leg you into a
naked option). Other multi-leg matches refuse `--limit`; narrow the query to one
leg or use `place-vertical --side SELL` for a net-priced combo close. There is no
native close-position call in the IBKR API — this replicates the TWS "Close" button.
Same preview→confirm→execute flow as place. If a position has no bid/ask quote
(e.g. a deep-OTM contract whose closing bid is negative), pass `--limit`. The
preview prints each position, its closing action, quantity, and limit, plus a
token; nothing is placed until you re-run with `--execute TOKEN`.

## Confirmation protocol (NON-NEGOTIABLE for live mode)

1. Run the `place`/`place-vertical` command WITHOUT `--execute`. This is a preview:
   it prints the resolved contract, current quotes, max loss/gain, and a `token`.
2. Show the user the preview (contract, side, qty, limit, max loss, premium).
3. LIVE MODE: wait for the user to explicitly approve THIS order in chat. Never
   infer approval from an earlier message, never batch approvals. Paper mode:
   self-confirmation is acceptable for testing.
4. Re-run the identical command with `--execute TOKEN`. The CLI rejects the token
   if any parameter changed, the preview is older than 5 minutes, or it was
   already used — in that case re-preview, re-confirm.

## Real-money safety (read before live trading)

- **Account pinning**: every order pins an account. With a single-account login
  it's automatic; if the login has multiple accounts, set `account = "U..."` in
  `~/.ibkr-options/config.toml` or orders fail with an account error (exit 5).
- **Delayed-data guard**: by default the tool uses delayed (~15 min) data
  (`market_data_type = 3`). A **live** order priced off delayed data is refused
  (exit 6) unless you pass `--allow-delayed` or set `allow_delayed_live = true`
  in config. Only suggest that opt-in when the user understands their limit
  prices are based on stale quotes; previews still print a DELAYED warning.
  For realtime, subscribe and set `market_data_type = 1`. Paper is never blocked.
- **Rejection surfacing**: a rejected order returns `"rejected": true` with the
  reason in `messages` (e.g. `[202] Limit price too far outside of NBBO`). Always
  check for this — a `Cancelled`/`Inactive` status means the order did NOT work.
- **Limit orders only**, and prices must respect IBKR tick rules ($0.05 ≥ $3.00,
  else $0.01) or IBKR rejects them.

## Reads vs writes (all-account vs this-CLI)

One consistent rule: **reads are account-wide, writes act only on orders this CLI
placed.**
- `positions` and `orders` show everything the account holds, regardless of where
  it was placed. Each open order carries `client_id` (0 = placed via web Portal /
  TWS / mobile) and `perm_id` (stable id to cross-reference with the Portal).
- `cancel` only works on orders this CLI placed (nonzero `order_id`). An order with
  `client_id: 0` is read-only here — cancel it where it was placed. So before a
  `close`, check `orders`: if a resting exit already exists there, closing again
  would double up.
- `trades` is the exception the TWS API forces: fills are session-scoped, not
  account-wide. For full account trade history use the Portal or Flex Queries.

## Operational notes

- If you get `gateway_unreachable`: ask the user to launch IB Gateway (on macOS
  something like `open -a "IB Gateway 10.45"` — the app name carries its version)
  and log in (paper or live to match the mode).
  Do not attempt to enter credentials yourself — login is the user's job.
- First-time Gateway setup: in Configure → Settings → API → Settings, "Enable
  ActiveX and Socket Clients" must be on and "Read-Only API" must be OFF for
  order placement. Socket port: 4002 paper / 4001 live.
- `"data": "delayed"` in output means no realtime subscription for that
  instrument — quotes are 15-20 min old. Say so when showing the user numbers.
- Never provide personalized investment advice; research, data, and executing
  the user's decisions only.
