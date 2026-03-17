---
name: get-crypto-price
description: Fetch current and historical crypto prices and compute ATH or ATL over common time windows.
---

# Get Crypto Price (minimal guide)

This short guide shows how to fetch current prices and at least 3 months of past price action using CoinGecko, Binance, and Coinbase public APIs. It also shows how to compute ATH (highest) and ATL (lowest) within time windows: 1 DAY, 1 WEEK, 1 MONTH.

---

## Quick notes
- Timestamps: many APIs return milliseconds since epoch (ms) or seconds (s). Convert consistently.
- Rate limits: respect exchange rate limits; cache responses when possible.
- Symbols: use canonical pair symbols (e.g., `BTCUSDT` on Binance, `bitcoin` on CoinGecko).

---

## 1) CoinGecko (recommended for simple historical ranges)

- Current price (curl):

```bash
curl "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
```

- Last 90 days (price history):

```bash
curl "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=90"
```

Response contains `prices` array: [[timestamp_ms, price], ...].

**Node.js:** Fetch 90 days and compute ATH/ATL for 1d/7d/30d windows.

```javascript
async function fetchCoinGeckoPrices(coinId = 'bitcoin', vs = 'usd', days = 90) {
  const url = `https://api.coingecko.com/api/v3/coins/${coinId}/market_chart`;
  const res = await fetch(`${url}?vs_currency=${vs}&days=${days}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = await res.json();
  return data.prices; // array of [ts_ms, price]
}

function maxMinInWindow(prices, sinceMs) {
  const window = prices.filter(([ts]) => ts >= sinceMs).map(([, p]) => p);
  if (window.length === 0) return [null, null];
  return [Math.max(...window), Math.min(...window)];
}

const prices = await fetchCoinGeckoPrices('bitcoin', 'usd', 90);
const nowMs = Date.now();

const windows = {
  '1d': nowMs - 24 * 3600 * 1000,
  '1w': nowMs - 7 * 24 * 3600 * 1000,
  '1m': nowMs - 30 * 24 * 3600 * 1000,
};

for (const [name, since] of Object.entries(windows)) {
  const [ath, atl] = maxMinInWindow(prices, since);
  console.log(name, 'ATH:', ath, 'ATL:', atl);
}
```

Notes: CoinGecko returns sampled points (usually hourly) — good for these windows.

---

## 2) Binance (exchange-level data)

- Current price (curl):

```bash
curl "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
```

- Historical klines (candles): use `klines` endpoint. Example: fetch daily candles for the last 1000 days or hourly for finer resolution.

```bash
# daily candles for BTCUSDT (limit up to 1000 rows)
curl "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=1000"
```

Each kline row: [openTime, open, high, low, close, ...] where openTime is ms.

**Node.js:** Fetch hourly klines for last 90 days and compute ATH/ATL windows.

```javascript
async function fetchBinanceKlines(symbol = 'BTCUSDT', interval = '1h', limit = 1000) {
  const url = 'https://api.binance.com/api/v3/klines';
  const params = new URLSearchParams({ symbol, interval, limit: String(limit) });
  const res = await fetch(`${url}?${params}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return await res.json(); // array of arrays
}

// To cover ~90 days hourly: 24*90 = 2160 rows -> call twice with different startTimes or use 4h interval
const klines = await fetchBinanceKlines('BTCUSDT', '1h', 1000);
// For more than 1000 rows you'd loop with startTime using ms timestamps.

// Convert to list of [ts_ms, high, low]
const data = klines.map(row => [row[0], parseFloat(row[2]), parseFloat(row[3])]);
const nowMs = Date.now();

function athAtlFromKlines(data, sinceMs) {
  const filtered = data.filter(([ts]) => ts >= sinceMs);
  if (filtered.length === 0) return [null, null];
  const highs = filtered.map(([, h]) => h);
  const lows = filtered.map(([, , l]) => l);
  return [Math.max(...highs), Math.min(...lows)];
}

const windows = {
  '1d': nowMs - 24 * 3600 * 1000,
  '1w': nowMs - 7 * 24 * 3600 * 1000,
  '1m': nowMs - 30 * 24 * 3600 * 1000,
};

for (const [name, since] of Object.entries(windows)) {
  const [ath, atl] = athAtlFromKlines(data, since);
  console.log(name, 'ATH:', ath, 'ATL:', atl);
}
```

Notes: Binance `limit` is 1000 max per request; for full 90 days hourly, page by startTime.

---

## 3) Coinbase (public example)

- Current spot price (curl):

```bash
curl "https://api.coinbase.com/v2/prices/BTC-USD/spot"
```

- Historical candles (Coinbase Exchange API):

```bash
curl "https://api.exchange.coinbase.com/products/BTC-USD/candles?granularity=3600&start=2025-11-01T00:00:00Z&end=2026-02-01T00:00:00Z"
```

Response: array of [time, low, high, open, close, volume]. Use similar filtering by timestamp to compute ATH/ATL.

---

## 4) Compute ATH / ATL for a timeframe (1 DAY, 1 WEEK, 1 MONTH)

General steps (applies to any data source that gives timestamped prices or OHLC candles):

1. Fetch historical points that cover at least the desired window (e.g., last 90 days).
2. Choose the window start timestamp (now - window_seconds).
3. Filter the points where timestamp >= window_start.
4. If you have OHLC candles, use `high` as candidate for ATH and `low` as candidate for ATL. If you only have sampled prices, use max/min of sampled values.

**Example with simple price points (Node.js):**

```javascript
// points = [[ts_ms, price], ...]
const sinceMs = Date.now() - 24 * 3600 * 1000; // 1 day
const windowPrices = points.filter(([ts]) => ts >= sinceMs).map(([, p]) => p);
if (windowPrices.length > 0) {
  const ath = Math.max(...windowPrices);
  const atl = Math.min(...windowPrices);
} else {
  const ath = null;
  const atl = null;
}
```

**If using OHLC candles:**

```javascript
// candles = [[ts_ms, open, high, low, close], ...]
const window = candles.filter(c => c[0] >= sinceMs);
const ath = Math.max(...window.map(c => c[2]));
const atl = Math.min(...window.map(c => c[3]));
```

---

## 5) Practical tips
- For 3 months of past price action, fetch 90 days of data or page the exchange candle endpoints until you cover ~90 days.
- Use hourly or daily granularity depending on required resolution. For 1-day ATH/ATL, hourly or minute granularity is better.
- Convert times into UTC and use ms for consistency.
- Respect API rate limits and use caching for repeated queries.

---

## 6) Example workflow (summary)
1. Try CoinGecko `market_chart?days=90` for quick 90-day history.
2. Compute windows for 1d/7d/30d from that array and derive ATH/ATL.
3. For exchange-precise data or higher resolution, query Binance `klines` or Coinbase `candles` and repeat the same aggregation.

---

If you want, I can add ready-to-run scripts for specific coins (BTC, ETH) and automate paginated Binance fetches to guarantee 90 days of hourly data.


Agent note: When producing human-friendly reports, agents should use the `skills/generate-report` skill to produce formatted outputs (markdown or PDF). See `skills/generate-report/SKILL.md` for examples and templates.

Example agent prompt:
> Use the generate-report skill to create a short Bitcoin price report (current price, 24h change, 7d change) in markdown and PDF. Include source URLs.
