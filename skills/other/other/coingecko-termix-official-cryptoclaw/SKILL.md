---
name: coingecko
description: Query CoinGecko API for prices, market data, trending tokens, and historical charts.
metadata: { "cryptoclaw": { "emoji": "🦎", "always": true } }
---

# CoinGecko API

Query cryptocurrency prices, market caps, charts, and trending tokens via the CoinGecko free API.

## Base URL

```
https://api.coingecko.com/api/v3
```

No API key required. Rate limit: ~30 calls/minute.

## Endpoints

### Price Lookup

```
GET /simple/price?ids={ids}&vs_currencies={currencies}&include_24hr_change=true&include_market_cap=true
```

- `ids`: comma-separated CoinGecko IDs (see ID table below)
- `vs_currencies`: `usd`, `btc`, `eth`, `bnb`

Example: `/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true`

### Token Price by Contract Address

```
GET /simple/token_price/{platform}?contract_addresses={addresses}&vs_currencies=usd&include_24hr_change=true
```

Platform IDs:

- `binance-smart-chain` — BSC
- `ethereum` — Ethereum
- `polygon-pos` — Polygon
- `arbitrum-one` — Arbitrum
- `optimistic-ethereum` — Optimism
- `base` — Base

Example: `/simple/token_price/binance-smart-chain?contract_addresses=0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82&vs_currencies=usd`

### Market Rankings

```
GET /coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1&sparkline=false
```

Returns top coins with price, market cap, volume, and 24h change.

### Trending

```
GET /search/trending
```

Returns trending coins, NFTs, and categories. No parameters needed.

### Historical Chart

```
GET /coins/{id}/market_chart?vs_currency=usd&days={days}
```

- `days`: `1`, `7`, `14`, `30`, `90`, `365`, `max`
- Returns arrays of `[timestamp, value]` for prices, market_caps, total_volumes

### Coin Detail

```
GET /coins/{id}?localization=false&tickers=false&community_data=false&developer_data=false
```

Returns full metadata: description, links, contract addresses, market data.

## CoinGecko ID Reference

| Token | CoinGecko ID      |
| ----- | ----------------- |
| BTC   | bitcoin           |
| ETH   | ethereum          |
| BNB   | binancecoin       |
| SOL   | solana            |
| USDT  | tether            |
| USDC  | usd-coin          |
| XRP   | ripple            |
| ADA   | cardano           |
| DOGE  | dogecoin          |
| AVAX  | avalanche-2       |
| DOT   | polkadot          |
| MATIC | matic-network     |
| LINK  | chainlink         |
| UNI   | uniswap           |
| CAKE  | pancakeswap-token |
| ARB   | arbitrum          |
| OP    | optimism          |
| AAVE  | aave              |
| LDO   | lido-dao          |
| SHIB  | shiba-inu         |

For unknown tokens, search: `GET /search?query={name}`

## Usage Notes

- Always use `curl -s` to fetch, then parse the JSON response
- For on-chain token prices not listed on CoinGecko, fall back to DEX quotes via `swap_get_quote`
- The `market-data` skill provides high-level workflow guidance; this skill is the concrete API reference
- Report data source and freshness: "CoinGecko, fetched just now"
