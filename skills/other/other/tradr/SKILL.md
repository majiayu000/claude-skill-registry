---
name: tradr
description: Onchain trade execution engine. Feed a CA + score, get full trade lifecycle — sized entry, mode-based exits, on-chain verification, and trade logging. Requires Bankr skill.
dependencies:
  - bankr
---

# tradr

Full onchain trade execution engine. You bring the signal, tradr handles everything else.

**Input:** Contract address + score
**Output:** Buy → monitor → exit (mechanical)

No signal generation. No opinion on *what* to buy. All opinion on *how to manage it once you're in*.

## Quick Start

```bash
# 1. Install
./scripts/setup.sh

# 2. Edit config
vi config.json    # Add wallet addresses, tune scoring/modes

# 3. Start the exit manager daemon
sudo systemctl start tradr-exit-manager

# 4. Feed a trade
python3 scripts/tradr-enter.py <CA> --score <N> [--chain base] [--mode snipe]
```

## Getting Started from Zero

### Prerequisites
- **OpenClaw** running (the agent runtime)
- **Bankr skill** installed (`~/.openclaw/skills/bankr/`) with a valid API key — this is what executes on-chain trades. Sign up at [bankr.bot](https://bankr.bot) to get your API key, then add it to `~/.openclaw/skills/bankr/config.json`
- **Python 3.8+** and **jq**
- A funded wallet (Solana and/or EVM) — Bankr creates wallets for you on supported chains (Base, Solana, ETH, Polygon, Unichain). Fund them before trading.

### Step-by-Step

1. **Install tradr:**
   ```bash
   cd ~/.openclaw/skills/tradr   # or wherever you unpacked the skill
   ./scripts/setup.sh            # creates config, installs systemd service
   ```

2. **Configure your wallets:**
   Edit `config.json` and add your wallet addresses under `wallets`. These are used for on-chain balance verification (read-only — tradr never touches your private keys).

3. **Tune your strategy:**
   - `score_to_size` — how much USD to spend at each confidence level
   - `modes` — exit behavior profiles (stop loss, take profit, trailing stop)
   - `mcap_ceiling_usd` — maximum market cap for entries

4. **Start the exit manager:**
   ```bash
   sudo systemctl start tradr-exit-manager
   sudo systemctl status tradr-exit-manager  # verify it's running
   ```

5. **Connect a signal source:**
   tradr doesn't generate signals — you bring your own. See `adapters/README.md` for the interface spec and `adapters/example-adapter.py` for a working template.

   Or feed trades manually:
   ```bash
   python3 scripts/tradr-enter.py 0xABC... --score 5 --chain base --token PEPE
   ```

6. **Monitor via dashboard:**
   The `dashboard/index.html` file provides a real-time dashboard. It expects four API endpoints:
   - `GET /api/positions` — returns positions.json contents
   - `GET /api/trades` — returns trade-log.jsonl as JSON array
   - `GET /api/tradr-config` — returns config.json contents
   - `GET /api/health` — returns system health (optional)

   You can serve these from any HTTP server that reads the flat files, or embed the dashboard in your existing server.

### File Layout
```
tradr/
├── config.json              # Your live config (created from template)
├── config-template.json     # Default config for new installs
├── SKILL.md                 # This file
├── scripts/
│   ├── tradr-enter.py       # Entry engine
│   ├── exit-manager.py      # Exit daemon
│   ├── setup.sh             # Installer
│   └── notify-telegram.sh   # Example notification hook
├── adapters/
│   ├── README.md            # Signal adapter interface spec
│   └── example-adapter.py   # Working adapter template
└── dashboard/
    └── index.html           # Real-time monitoring dashboard
```

## Signal Adapters

tradr is execution-only — it doesn't have opinions about *what* to buy. You bring the signal, tradr handles the trade lifecycle.

The interface is one command:
```bash
python3 scripts/tradr-enter.py <ca> --score <N> [--chain <chain>] [--token <name>]
```

A signal adapter is any script or service that watches a source, detects signals, scores them, and calls that command. See `adapters/README.md` for the full spec and `adapters/example-adapter.py` for a working template.

**Signal source ideas:** Twitter KOL tracking, on-chain whale monitoring, Telegram alpha groups, DEX volume spikes, copy-trading apps, custom aggregators.

## Scripts

- **`scripts/tradr-enter.py`** — Entry engine. Takes CA + score, sizes position, buys via Bankr, writes position with mode attached.
- **`scripts/exit-manager.py`** — Exit daemon. Polls prices, applies mode-specific exit rules, sells via Bankr, verifies on-chain, logs everything. Runs as systemd service.
- **`scripts/setup.sh`** — Installer. Creates config from template, sets up systemd service.

## Exit Modes

Each position carries a mode that determines its exit behavior. Four built-in modes ship as defaults — you can customize them or create your own.

| Mode | Stop At | Take Profit | Trailing | Use Case |
|------|---------|-------------|----------|----------|
| **snipe** | 0.85x | 1.3x (sell 30%) | 10% from peak | Quick in/out. Low-conviction plays. |
| **swing** | 0.70x | 1.3x (sell 30%) | Tiered: 15% tight / 25% wide | Standard hold. The default. |
| **gamble** | 0.50x | none | 30% from peak | High risk, let it ride or die. |
| **diamond** | none | none | none | Pure conviction. Manual exit only. |

Swing mode has **tiered trailing**: tight trail (15%) when peak is below 2x, wide trail (25%) when peak is above 2x. Protects modest gains while letting big winners run.

### Custom Modes

Add your own modes by adding a key to `modes` in config.json. Any name works — the exit manager reads mode params dynamically. No code changes needed.

```json
"modes": {
  "snipe": { ... },
  "swing": { ... },
  "my-custom-mode": {
    "stop_at": 0.80,
    "take_profit_1": 1.2,
    "take_profit_1_size": 0.5,
    "trailing_stop": 0.12
  }
}
```

Then use it: `tradr-enter.py <CA> --score 5 --mode my-custom-mode`

### Mode Selection

Modes are selected per-trade in order of priority:
1. **Explicit `--mode` flag** on entry (always wins)
2. **Score-based auto-selection** via `score_to_mode` config map
3. **`default_mode`** fallback (default: swing)

## Entry Guards

tradr rejects entries that fail any of these checks:

- **Mcap ceiling -- token mcap exceeds `mcap_ceiling_usd` default: $10M)
- **Cooldown** — same token was closed less than `cooldown_minutes` ago (default: 30)
- **Max position size** — scored size exceeds `max_position_size_usd`
- **Already in position** — open position exists for this CA

## Partial Sell Tracking

When a take-profit triggers, tradr tracks `remaining_usd` on the position. This means:
- P&L calculations account for what was already sold at TP vs what's left at final exit
- The trade log records actual sold amounts, not the full original position
- You can see how much USD value is still in play at any time

## Notification Hook

The notification script receives three arguments: `level`, `type`, `message`.

- **level**: `info`, `trade`, `warning`, `error`
- **type**: `buy`, `sell`, `confluence`, `error`, `info`
- **message**: human-readable text

This lets your hook route notifications — e.g., buys to DM only, sells to DM + broadcast channel.

Example hook:
```bash
#!/bin/bash
LEVEL="$1"  TYPE="$2"  MSG="$3"
if [ "$TYPE" = "sell" ]; then
  # Route to both DM and broadcast
  send-dm "$MSG"
  send-broadcast "$MSG"
else
  # Everything else just DM
  send-dm "$MSG"
fi
```

## Config Reference

`config.json` (created from `config-template.json` on first setup):

```
positions_file       — path to positions.json
trade_log            — path to trade-log.jsonl
log_file             — path to tradr.log
bankr_script         — path to bankr.sh
lockfile             — exit manager lock (prevents duplicates)
poll_interval_seconds — price check interval (default: 10)
dexscreener_delay    — delay between DexScreener calls (default: 1.5s)
reconcile_every_cycles — on-chain reconciliation interval (default: every 30 cycles)

modes                — exit params per mode (add custom modes here)
  stop_at            — exit multiplier (e.g. 0.85 = sell if price drops to 0.85x entry)
  take_profit_1      — first TP multiplier (null = no TP)
  take_profit_1_size — fraction to sell at TP (e.g. 0.3 = 30%)
  trailing_stop      — trail % from peak (null = no trail)
  trailing_stop_tight — optional tight trail (swing mode)
  trailing_stop_tight_below — peak threshold for tight vs wide

default_mode         — fallback mode when not specified
score_to_mode        — map of score thresholds → mode names
score_to_size        — map of score thresholds → position size in USD

mcap_ceiling_usd     — reject entries above this mcap (0 = no limit)
cooldown_minutes     — block re-entry on same token for N minutes after close (0 = no cooldown)
max_position_size_usd — hard cap on any single position

wallets.solana       — Solana wallet address (for on-chain verification)
wallets.evm          — EVM wallet address (for on-chain verification)
rpc_urls             — custom RPC endpoints per chain

notifications.enabled — enable/disable notifications
notifications.script  — path to notification hook script (receives: level, type, message)
```

## Dashboard

tradr ships with a real-time monitoring dashboard (`dashboard/index.html`) that shows:

- **Open positions** — live P&L, entry/current/peak market cap, exit mode, time held
- **Performance stats** — total P&L, win rate, avg peak, best trade
- **Trade history** — searchable table with entry/exit details, tx links
- **Configuration** — collapsible view of exit modes, sizing tiers, limits

The dashboard is a standalone HTML file that fetches data from four JSON API endpoints. It auto-refreshes every 15 seconds. Dark theme, mobile responsive.

To use it, serve these endpoints from your HTTP server:
- `GET /api/positions` — contents of positions.json
- `GET /api/trades` — trade-log.jsonl parsed as `{ "trades": [...] }`
- `GET /api/tradr-config` — contents of config.json
- `GET /api/health` — system health (optional)

## Architecture

```
Signal Source (your adapter)
    |
    | CA + score [+ chain] [+ token]
    v
tradr-enter.py
    |
    |-- Guards: mcap ceiling, cooldown, size cap
    |-- Resolves mode (explicit > score_to_mode > default)
    |-- Sizes position (score_to_size map)
    |-- Fetches price/mcap from DexScreener
    |-- Executes buy via bankr.sh
    |-- Writes positions.json (with mode + remaining_usd fields)
    |-- Logs to trade-log.jsonl
    |-- Notifies (type=buy)
    |
    v
exit-manager.py (daemon, 10s poll)
    |
    |-- Reads positions.json
    |-- For each open position:
    |     |-- Reads position's mode → gets exit params from config
    |     |-- Fetches price from DexScreener
    |     |-- Applies: hard stop → TP → trailing
    |     |-- Executes sell via bankr.sh if triggered
    |     |-- Tracks remaining_usd after partial sells
    |     |-- Verifies on-chain balance (Solana RPC / EVM eth_call)
    |     |-- Updates positions.json + trade-log.jsonl
    |     |-- Notifies (type=sell)
    |
    |-- Every N cycles: reconcile (close stale positions where wallet is empty)
```

## Position Schema

Each position in `positions.json` (keyed by contract address):

```json
{
  "token": "EXAMPLE",
  "chain": "base",
  "buy_ts": "2026-02-11T14:00:00Z",
  "entry_mcap": 500000,
  "entry_price": 0.0001,
  "buy_amount_usd": 7.50,
  "remaining_usd": 7.50,
  "mode": "swing",
  "score": 5,
  "current_mcap": 600000,
  "current_price": 0.00012,
  "peak_mcap": 700000,
  "first_exit_done": false,
  "closed": false,
  "close_ts": null,
  "close_reason": null,
  "close_mcap": null,
  "close_multiple": null,
  "est_pnl_usd": null,
  "tx_hash": "0x..."
}
```

## Requirements

- Python 3.8+
- Bankr skill installed (`~/.openclaw/skills/bankr/`)
- jq (used by bankr.sh)
- systemd (for exit manager daemon)
- No paid APIs. No LLM cost. Pure Python.

## What tradr Is Not

- **Not a signal generator.** It doesn't tell you what to buy. You bring the alpha.
- **Not an LLM.** Zero AI cost at runtime. Pure Python, pure math.
- **Not a wallet.** It never holds or accesses private keys. Execution goes through Bankr.
- **Not opinionated about chains.** Works on Solana, Base, Ethereum, Polygon, Unichain — anywhere Bankr supports.
