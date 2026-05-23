---
name: getCriptoPrice
description: "Retrieve the latest USD price for a crypto asset (e.g., BTC, ETH) via a public API (CoinGecko). Use when the user asks for the price of a crypto asset."
---

# getCriptoPrice

This skill provides a simple, reliable way to fetch a crypto spot price in USD.

## What it does
- Input: a crypto asset symbol (e.g., `BTC`) or CoinGecko id (e.g., `bitcoin`)
- Output: JSON with the normalized price payload

## How to run (script)
Use the bundled script:

```bash
node scripts/getCriptoPrice.mjs BTC
# or
node scripts/getCriptoPrice.mjs bitcoin
```

## Output format

```json
{
  "ok": true,
  "asset": {
    "input": "BTC",
    "coingecko_id": "bitcoin",
    "symbol": "btc",
    "name": "Bitcoin"
  },
  "currency": "usd",
  "price": 12345.67,
  "ts": "2026-02-14T03:03:00.000Z",
  "source": "coingecko"
}
```

## Notes
- Uses CoinGecko's public endpoints; no API key required.
- If you later want higher rate limits/latency guarantees, swap the data source (e.g., Coinbase, Kraken, Binance) and keep the same output schema.
