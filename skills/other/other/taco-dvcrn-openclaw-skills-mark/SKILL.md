---
name: taco
description: "Interact with the Taco crypto trading platform via API. Use when the user wants to (1) get kline/candlestick market data, (2) check account balance and positions, (3) open perpetual positions, (4) close perpetual positions, (5) calculate technical indicators (EMA, MACD, RSI, ATR, BollingerBands, DonchianChannel), or (6) any trading operations on Taco. Supports exchanges: Binance, Hyper, Aster, Grvt, StandX, Lighter."
---

# Taco Trading Platform

## Setup

Config is stored at `~/.openclaw/workspace/taco/config.json`. Each exchange is bound to its own `trader_id`:

```json
{
  "user_id": "<taco user id>",
  "api_token": "<taco api key>",
  "trader_ids": {
    "StandX": "<trader id for StandX>",
    "Binance": "<trader id for Binance>",
    "Hyper": "<trader id for Hyper>",
    "Lighter": "<trader id for Lighter>",
    "Aster": "<trader id for Aster>",
    "Grvt": "<trader id for Grvt>"
  }
}
```

**Key concept:** Exchange and `trader_id` are bound 1:1. When operating on a specific exchange, the CLI automatically uses the corresponding `trader_id` from config. Only configure the exchanges you use.

**First-time setup:** If config does not exist, ask the user for their `user_id`, `api_token`, and each exchange's `trader_id`, then write the JSON file to `~/.openclaw/workspace/taco/config.json` (create parent directories as needed). Alternatively, run the interactive init command:

```bash
$PYTHON scripts/taco_client.py init
```

**Before any API call:** Check that `~/.openclaw/workspace/taco/config.json` exists. If not, guide the user through setup first.

## Python Requirement

Before running any command, detect the available Python 3 command:

```bash
command -v python3 || command -v python
```

- If `python3` is found, use `python3` (and `pip3` for package installs)
- If only `python` is found, verify it is Python 3 with `python --version`. If it reports Python 2.x, treat it as unavailable.
- If neither provides Python 3, ask the user to install Python 3 before proceeding.

Then check the `requests` package: `$PYTHON -c "import requests"`. If it fails, install with `pip3 install requests` (or `pip install requests` if only `pip` is available).

**In all examples below, `$PYTHON` represents the detected Python command.** Store the result once per session and reuse it for every subsequent call.

## Usage

Run the CLI client at `scripts/taco_client.py` (relative to this skill directory). Requires the `requests` Python package. Config defaults to `~/.openclaw/workspace/taco/config.json` (override with `--config <path>`).

### Get kline data (no auth required)

```bash
$PYTHON scripts/taco_client.py kline \
  --symbol BTCUSDT --interval 1h --exchange Binance
```

Optional: `--start-time <unix_ms>` `--end-time <unix_ms>` (max 100 klines per response)

Valid intervals: `1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `6h`, `8h`, `12h`, `1d`, `3d`, `1w`, `1M`

### Check account

```bash
$PYTHON scripts/taco_client.py account --exchange Binance
```

Returns: available_balance, total_equity, margin_used, and open positions for the specified exchange's trader.

### Open position

```bash
$PYTHON scripts/taco_client.py open \
  --exchange Binance --symbol BTCUSDT --notional 100 --long --leverage 3 \
  --sl-price 80000 --tp-price 100000
```

- `--long` for long, omit for short
- `--sl-price` and `--tp-price` are optional
- `--leverage` defaults to 1.0

### Close position

```bash
$PYTHON scripts/taco_client.py close \
  --exchange Binance --symbol BTCUSDT --notional 100 --long
```

- `--long` to close a long position, omit to close a short

### Calculate indicators (no auth required)

Fetches kline data and computes technical indicators locally. Supported types: `EMA`, `MACD`, `RSI`, `ATR`, `BollingerBands`, `DonchianChannel`.

```bash
# EMA (Exponential Moving Average)
$PYTHON scripts/taco_client.py indicator \
  --exchange Binance --symbol BTCUSDT --interval 1h --type EMA --period 20

# MACD (Moving Average Convergence Divergence)
$PYTHON scripts/taco_client.py indicator \
  --exchange Binance --symbol BTCUSDT --interval 1h --type MACD \
  --fast 12 --slow 26 --signal 9

# RSI (Relative Strength Index)
$PYTHON scripts/taco_client.py indicator \
  --exchange Binance --symbol BTCUSDT --interval 4h --type RSI --period 14

# ATR (Average True Range)
$PYTHON scripts/taco_client.py indicator \
  --exchange Binance --symbol BTCUSDT --interval 1d --type ATR --period 14

# Bollinger Bands
$PYTHON scripts/taco_client.py indicator \
  --exchange Binance --symbol BTCUSDT --interval 1h --type BollingerBands \
  --period 20 --std-dev 2.0

# Donchian Channel
$PYTHON scripts/taco_client.py indicator \
  --exchange Binance --symbol BTCUSDT --interval 1h --type DonchianChannel --period 20
```

Options:
- `--type` — required, one of: `EMA`, `MACD`, `RSI`, `ATR`, `BollingerBands`, `DonchianChannel`
- `--period` — indicator period (default varies by type: EMA=20, RSI=14, ATR=14, BollingerBands=20, DonchianChannel=20)
- `--fast`, `--slow`, `--signal` — MACD-specific (defaults: 12, 26, 9)
- `--std-dev` — BollingerBands standard deviation multiplier (default: 2.0)
- `--limit N` — show only the last N computed values (default: all)
- `--start-time`, `--end-time` — optional, same as kline

## Supported exchanges

`Binance`, `Hyper`, `Aster`, `Grvt`, `StandX`, `Lighter`

## API details

For full endpoint documentation and response schemas, see [references/api-references.md](references/api-references.md).
