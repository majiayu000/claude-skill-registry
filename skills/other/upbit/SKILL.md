---
name: upbit
description: Real-time cryptocurrency price lookup from Upbit (Korean KRW exchange). Use when user asks for Korean crypto prices, Upbit prices, domestic cryptocurrency rates, or market ticker in Korean won (KRW). Supports all coins listed on Upbit exchange.
---

# Upbit Price Lookup

## Overview

Query real-time cryptocurrency prices from Upbit, South Korea's largest cryptocurrency exchange. Provides KRW-based pricing with 24h statistics, trading volume, and 52-week highs/lows.

## Quick Start

Fetch ticker data using Upbit's public API:

```bash
curl -s "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
```

Replace `KRW-BTC` with the desired market code (e.g., `KRW-ETH`, `KRW-SUI`, `KRW-DOGE`).

## Market Code Format

Upbit uses `KRW-{SYMBOL}` format:
- Bitcoin: `KRW-BTC`
- Ethereum: `KRW-ETH`
- Sui: `KRW-SUI`
- Dogecoin: `KRW-DOGE`

**Important:** Always use uppercase for the symbol.

## Response Format

The API returns JSON with these key fields:

```json
{
  "market": "KRW-BTC",
  "trade_price": 145000000.0,
  "opening_price": 144000000.0,
  "high_price": 146000000.0,
  "low_price": 143000000.0,
  "prev_closing_price": 144000000.0,
  "change": "RISE",
  "change_price": 1000000.0,
  "change_rate": 0.00694444,
  "signed_change_price": 1000000.0,
  "signed_change_rate": 0.00694444,
  "acc_trade_volume_24h": 123.456,
  "acc_trade_price_24h": 17890000000.0,
  "highest_52_week_price": 150000000.0,
  "highest_52_week_date": "2025-12-01",
  "lowest_52_week_price": 100000000.0,
  "lowest_52_week_date": "2025-02-01",
  "trade_date_kst": "20260209",
  "trade_time_kst": "074511"
}
```

### Key Fields

- `trade_price`: Current price (KRW)
- `change`: Price direction (`RISE`, `FALL`, `EVEN`)
- `change_price`: Absolute change from previous close (KRW)
- `change_rate`: Percentage change (0.00694444 = 0.69%)
- `signed_change_price`: Signed price change (negative for falls)
- `signed_change_rate`: Signed percentage change
- `acc_trade_volume_24h`: 24-hour trading volume (coins)
- `acc_trade_price_24h`: 24-hour trading value (KRW)
- `highest_52_week_price` / `lowest_52_week_price`: 52-week price range
- `trade_date_kst` / `trade_time_kst`: Last trade timestamp (Korea time)

## Formatting Output

Present prices in a readable format with:

1. **Current price** with change indicator (▲/▼)
2. **Percentage change** from previous close
3. **Day range** (high/low)
4. **24h volume** in both coins and KRW
5. **52-week range** for context

Example output:

```
**BTC/KRW (2026-02-09 07:45:11 기준)**

- **현재가:** 145,000,000원
- **전일대비:** +1,000,000원 (+0.69%) ▲
- **시가:** 144,000,000원
- **고가:** 146,000,000원
- **저가:** 143,000,000원
- **24시간 거래량:** 123.46 BTC
- **24시간 거래대금:** 약 178억원

**52주 기록**
- 최고: 150,000,000원 (2025-12-01)
- 최저: 100,000,000원 (2025-02-01)
```

## Multiple Markets

Query multiple markets at once:

```bash
curl -s "https://api.upbit.com/v1/ticker?markets=KRW-BTC,KRW-ETH,KRW-SUI"
```

Returns an array of ticker objects.

## Error Handling

If the market code is invalid or not listed on Upbit, the API returns an empty array `[]`. In this case, inform the user that the coin is not available on Upbit or verify the market code.
