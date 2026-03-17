---
name: getFuturesPrice
description: "Retrieve the latest price for a futures instrument (e.g., NQ, ES) using a public quote endpoint (Yahoo Finance). Use when the user asks for a futures price like NQ (Nasdaq-100 futures)."
---

# getFuturesPrice

Fetch the latest available quote for common futures symbols.

## Quick usage

```bash
node scripts/getFuturesPrice.mjs NQ
node scripts/getFuturesPrice.mjs ES
```

## Output format

```json
{
  "ok": true,
  "input": "NQ",
  "resolved": {
    "symbol": "NQ=F",
    "name": "E-mini NASDAQ 100 Futures"
  },
  "currency": "USD",
  "price": 12345.25,
  "bid": 12345.0,
  "ask": 12345.5,
  "change": -12.75,
  "changePercent": -0.10,
  "marketState": "REGULAR",
  "ts": "2026-02-14T03:07:00.000Z",
  "source": "yahoo"
}
```

## Notes / Caveats
- This uses Yahoo Finance's public quote endpoint. It may be delayed and is not guaranteed for trading execution.
- For production trading and strict accuracy, migrate to an exchange-grade feed (CQG/Rithmic/Tradovate/IBKR) via API/WebSocket.
