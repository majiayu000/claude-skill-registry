---
name: geckoterminal-api
version: "1.1.0"
description: GeckoTerminal API - DeFi and DEX aggregator providing real-time cryptocurrency prices, trading volumes, OHLCV charts, and liquidity data across 250+ blockchain networks and 1,800+ decentralized exchanges
---

# GeckoTerminal API Skill

**GeckoTerminal** is a DeFi and DEX aggregator that provides real-time cryptocurrency prices, trading volumes, transactions, and liquidity data across decentralized exchanges. The API enables developers to access on-chain market data for any token using its contract address.

**Key Value Proposition**: Access live, on-chain market data for 6M+ tokens across 250+ blockchain networks and 1,800+ DEXes - all indexed by contract address rather than ticker symbols, enabling queries for tokens not listed on centralized exchanges.

## When to Use This Skill

- Querying real-time prices for tokens on decentralized exchanges
- Building DeFi dashboards with live pool and token data
- Fetching OHLCV candlestick data for charting applications
- Discovering trending or newly created liquidity pools
- Tracking trading activity and transactions for specific pools
- Finding all pools trading a specific token across DEXes
- Building trading bots that need on-chain price feeds
- Analyzing liquidity and volume across multiple chains

## When NOT to Use This Skill

- For centralized exchange (CEX) data (use CoinGecko or exchange APIs)
- For tokens only on CEXes with no DEX liquidity
- For market cap data (use CoinGecko API for verified supply data)
- For high-frequency trading requiring <1 second updates (rate limits apply)
- For historical data beyond 6 months (OHLCV limitation)
- For off-chain order book data (GeckoTerminal is AMM/DEX focused)

---

## Core Concepts

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    GeckoTerminal API v2                         │
│                 api.geckoterminal.com/api/v2                    │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   Networks    │    │    Tokens     │    │    Pools      │
│   & DEXes     │    │               │    │               │
├───────────────┤    ├───────────────┤    ├───────────────┤
│ /networks     │    │ /tokens/...   │    │ /pools/...    │
│ /dexes        │    │ /simple/...   │    │ /trending_... │
│ 250+ chains   │    │ 6M+ tokens    │    │ /new_pools    │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Market Data     │
                    ├───────────────────┤
                    │ • OHLCV Charts    │
                    │ • Trade History   │
                    │ • Pool Analytics  │
                    │ • Price Changes   │
                    └───────────────────┘
```

### Key Differences from CoinGecko

| Feature | GeckoTerminal | CoinGecko |
|---------|---------------|-----------|
| **Data Source** | On-chain DEX only | CEX + DEX |
| **Token ID** | Contract address | Coin ID (slug) |
| **Coverage** | All traded tokens | Listed tokens only |
| **OHLCV Source** | On-chain trades | Exchange feeds |
| **Market Cap** | FDV only (on-chain) | Verified supply data |

---

## API Basics

### Base URL

```
https://api.geckoterminal.com/api/v2
```

### Rate Limits

| Tier | Rate Limit | Notes |
|------|------------|-------|
| **Free** | 30 calls/minute | No API key required |
| **Paid (CoinGecko)** | 500 calls/minute | Via CoinGecko subscription |

### Headers

```bash
# Required header for all requests
-H 'accept: application/json'
```

### Response Format

All responses follow JSON:API specification:

```json
{
  "data": {
    "id": "eth_0x...",
    "type": "token",
    "attributes": {
      "name": "Token Name",
      "symbol": "TKN",
      "price_usd": "1.23"
    }
  }
}
```

---

## Endpoints Reference

### Networks

**List all supported networks:**

```bash
GET /networks
```

```bash
curl -X GET 'https://api.geckoterminal.com/api/v2/networks?page=1' \
  -H 'accept: application/json'
```

**Response:**
```json
{
  "data": [
    {
      "id": "eth",
      "type": "network",
      "attributes": {
        "name": "Ethereum",
        "coingecko_asset_platform_id": "ethereum"
      }
    },
    {
      "id": "solana",
      "type": "network",
      "attributes": {
        "name": "Solana",
        "coingecko_asset_platform_id": "solana"
      }
    }
  ]
}
```

**Common Network IDs:**
| Network | ID |
|---------|-----|
| Ethereum | `eth` |
| Solana | `solana` |
| Base | `base` |
| Arbitrum | `arbitrum` |
| Polygon | `polygon_pos` |
| BSC | `bsc` |
| Avalanche | `avax` |
| Optimism | `optimism` |

### DEXes

**List DEXes on a network:**

```bash
GET /networks/{network}/dexes
```

```bash
curl -X GET 'https://api.geckoterminal.com/api/v2/networks/eth/dexes' \
  -H 'accept: application/json'
```

**Query Parameters:**
| Parameter | Description | Default |
|-----------|-------------|---------|
| `page` | Page number for pagination | 1 |

---

### Token Prices (Simple Endpoint)

**Get token prices by address:**

```bash
GET /simple/networks/{network}/token_price/{addresses}
```

```bash
# Single token
curl -X GET 'https://api.geckoterminal.com/api/v2/simple/networks/eth/token_price/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2' \
  -H 'accept: application/json'

# Multiple tokens (comma-separated, max 30)
curl -X GET 'https://api.geckoterminal.com/api/v2/simple/networks/eth/token_price/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2,0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48' \
  -H 'accept: application/json'
```

**Response:**
```json
{
  "data": {
    "id": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    "type": "simple_token_price",
    "attributes": {
      "token_prices": {
        "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "3245.67"
      }
    }
  }
}
```

---

### Token Information

**Get detailed token info:**

```bash
GET /networks/{network}/tokens/{address}
```

```bash
curl -X GET 'https://api.geckoterminal.com/api/v2/networks/eth/tokens/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2' \
  -H 'accept: application/json'
```

**Get multiple tokens:**

```bash
GET /networks/{network}/tokens/multi/{addresses}
```

```bash
# Up to 30 addresses
curl -X GET 'https://api.geckoterminal.com/api/v2/networks/eth/tokens/multi/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2,0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48' \
  -H 'accept: application/json'
```

**Get token metadata:**

```bash
GET /networks/{network}/tokens/{address}/info
```

Returns token information including name, symbol, image URL, social links, and description.

**Get recently updated tokens:**

```bash
GET /tokens/info_recently_updated
```

```bash
# Get 100 most recently updated tokens with network info
curl -X GET 'https://api.geckoterminal.com/api/v2/tokens/info_recently_updated?include=network' \
  -H 'accept: application/json'
```

**Query Parameters:**
| Parameter | Description | Values |
|-----------|-------------|--------|
| `include` | Include related resources | `network` |
| `network` | Filter by specific network | e.g., `eth`, `solana` |

Response includes `image_url` and decimal places for each token.

---

### Pools

**Get pools for a token:**

```bash
GET /networks/{network}/tokens/{token_address}/pools
```

```bash
curl -X GET 'https://api.geckoterminal.com/api/v2/networks/eth/tokens/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2/pools' \
  -H 'accept: application/json'
```

**Get specific pool:**

```bash
GET /networks/{network}/pools/{pool_address}
```

```bash
curl -X GET 'https://api.geckoterminal.com/api/v2/networks/eth/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640' \
  -H 'accept: application/json'
```

**Get multiple pools:**

```bash
GET /networks/{network}/pools/multi/{addresses}
```

**Pool Response Attributes:**
```json
{
  "attributes": {
    "name": "WETH / USDC 0.05%",
    "address": "0x88e6...",
    "base_token_price_usd": "3245.67",
    "quote_token_price_usd": "1.00",
    "base_token_price_quote_token": "3245.67",
    "quote_token_price_base_token": "0.000308",
    "base_token_price_native_currency": "1.0",
    "quote_token_price_native_currency": "0.000308",
    "reserve_in_usd": "450000000",
    "fdv_usd": "12000000000",
    "market_cap_usd": "8000000000",
    "pool_created_at": "2023-05-01T12:00:00Z",
    "volume_usd": {
      "h24": "125000000",
      "h6": "32000000",
      "h1": "5400000",
      "m5": "450000"
    },
    "price_change_percentage": {
      "h24": "2.5",
      "h6": "0.8",
      "h1": "0.2",
      "m5": "0.05"
    },
    "transactions": {
      "h24": { "buys": 1250, "sells": 980, "buyers": 890, "sellers": 720 },
      "h6": { "buys": 320, "sells": 280, "buyers": 210, "sellers": 180 },
      "h1": { "buys": 52, "sells": 41, "buyers": 38, "sellers": 29 },
      "m5": { "buys": 5, "sells": 3, "buyers": 4, "sellers": 2 }
    }
  }
}
```

**Include Parameters:**

When querying pools, use `include` to get related token/DEX data:

```bash
# Include base token, quote token, and DEX info
curl -X GET 'https://api.geckoterminal.com/api/v2/networks/eth/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640?include=base_token,quote_token,dex' \
  -H 'accept: application/json'
```

| Include Value | Returns |
|---------------|---------|
| `base_token` | Base token metadata (name, symbol, coingecko_coin_id) |
| `quote_token` | Quote token metadata |
| `dex` | DEX information |

**Get pool token info:**

```bash
GET /networks/{network}/pools/{pool_address}/info
```

Returns detailed token information for tokens in a specific pool.

---

### Trending & New Pools

**Trending pools (network-specific):**

```bash
GET /networks/{network}/trending_pools
```

```bash
curl -X GET 'https://api.geckoterminal.com/api/v2/networks/solana/trending_pools' \
  -H 'accept: application/json'
```

**Trending pools (all networks):**

```bash
GET /networks/trending_pools
```

**New pools (network-specific):**

```bash
GET /networks/{network}/new_pools
```

**New pools (all networks):**

```bash
GET /networks/new_pools
```

---

### Top Pools

**Top pools on a network:**

```bash
GET /networks/{network}/pools
```

**Query Parameters:**
| Parameter | Description | Values |
|-----------|-------------|--------|
| `page` | Page number | Integer |
| `sort` | Sort order | `h24_volume_usd_desc`, `h24_tx_count_desc` |
| `include` | Include related data | `base_token`, `quote_token`, `dex` |

```bash
# Top pools by 24h volume
curl -X GET 'https://api.geckoterminal.com/api/v2/networks/eth/pools?sort=h24_volume_usd_desc&page=1' \
  -H 'accept: application/json'

# Top pools by transaction count
curl -X GET 'https://api.geckoterminal.com/api/v2/networks/solana/pools?order=h24_tx_count_desc&page=1' \
  -H 'accept: application/json'
```

**Top pools on a specific DEX:**

```bash
GET /networks/{network}/dexes/{dex}/pools
```

```bash
# Top pools on Uniswap V3
curl -X GET 'https://api.geckoterminal.com/api/v2/networks/eth/dexes/uniswap_v3/pools?include=base_token,quote_token' \
  -H 'accept: application/json'
```

---

### OHLCV Data

**Get candlestick data:**

```bash
GET /networks/{network}/pools/{pool_address}/ohlcv/{timeframe}
```

**Timeframe Options:**
| Timeframe | Aggregate Values | Description |
|-----------|------------------|-------------|
| `minute` | 1, 5, 15 | 1m, 5m, 15m candles |
| `hour` | 1, 4, 12 | 1h, 4h, 12h candles |
| `day` | 1 | Daily candles |

**Query Parameters:**
| Parameter | Description | Default |
|-----------|-------------|---------|
| `aggregate` | Candle period | Required |
| `before_timestamp` | Unix epoch seconds | Now |
| `limit` | Number of candles | 100 (max 1000) |
| `currency` | Price currency | `usd` or `token` |
| `token` | Which token price | `base` or `quote` (can also pass token address) |

**Note:** The `token` parameter can now accept a token address directly (as long as it exists in the pool being queried), allowing you to specify exactly which token's price data you want returned.

```bash
# 15-minute candles
curl -X GET 'https://api.geckoterminal.com/api/v2/networks/eth/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640/ohlcv/minute?aggregate=15&limit=100' \
  -H 'accept: application/json'

# Daily candles for last 30 days
curl -X GET 'https://api.geckoterminal.com/api/v2/networks/eth/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640/ohlcv/day?aggregate=1&limit=30' \
  -H 'accept: application/json'
```

**Response:**
```json
{
  "data": {
    "attributes": {
      "ohlcv_list": [
        [1679414400, 3240.5, 3255.2, 3238.1, 3250.0, 12500000],
        [1679500800, 3250.0, 3262.8, 3245.3, 3258.6, 15200000]
      ]
    }
  },
  "meta": {
    "base": { "address": "0x...", "symbol": "WETH" },
    "quote": { "address": "0x...", "symbol": "USDC" }
  }
}
```

**OHLCV Array Format:** `[timestamp, open, high, low, close, volume]`

---

### Trade History

**Get recent trades:**

```bash
GET /networks/{network}/pools/{pool_address}/trades
```

```bash
curl -X GET 'https://api.geckoterminal.com/api/v2/networks/solana/pools/69grLw4PcSypZnn3xpsozCJFT8vs8WA5817VUVnzNGTh/trades' \
  -H 'accept: application/json'
```

Returns the latest 300 trades in the past 24 hours for the pool.

**Query Parameters:**
| Parameter | Description | Values |
|-----------|-------------|--------|
| `trade_volume_in_usd_greater_than` | Filter by minimum trade size | Number (e.g., `1000`) |

```bash
# Get trades with minimum $1000 volume
curl -X GET 'https://api.geckoterminal.com/api/v2/networks/eth/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640/trades?trade_volume_in_usd_greater_than=1000' \
  -H 'accept: application/json'
```

---

### Search

**Search for pools:**

```bash
GET /search/pools?query={query}
```

```bash
# Search by token symbol, name, or address
curl -X GET 'https://api.geckoterminal.com/api/v2/search/pools?query=PEPE' \
  -H 'accept: application/json'

# Search within a specific network
curl -X GET 'https://api.geckoterminal.com/api/v2/search/pools?query=PEPE&network=eth' \
  -H 'accept: application/json'
```

**Query Parameters:**
| Parameter | Description | Values |
|-----------|-------------|--------|
| `query` | Search term (symbol, name, or address) | String |
| `network` | Filter by network | e.g., `eth`, `solana` |
| `include` | Include related data | `base_token`, `quote_token`, `dex` |

Returns top 5 matching pools by default.

---

## Complete Endpoint Reference

| Category | Endpoint | Method | Description |
|----------|----------|--------|-------------|
| **Networks** | `/networks` | GET | List all supported networks |
| **Networks** | `/networks/{network}/dexes` | GET | List DEXes on a network |
| **Simple** | `/simple/networks/{network}/token_price/{addresses}` | GET | Get token prices (up to 30) |
| **Tokens** | `/networks/{network}/tokens/{address}` | GET | Get specific token info |
| **Tokens** | `/networks/{network}/tokens/multi/{addresses}` | GET | Get multiple tokens (up to 30) |
| **Tokens** | `/networks/{network}/tokens/{address}/info` | GET | Get token metadata |
| **Tokens** | `/tokens/info_recently_updated` | GET | Get 100 recently updated tokens |
| **Pools** | `/networks/{network}/pools` | GET | Top pools on network |
| **Pools** | `/networks/{network}/pools/{pool_address}` | GET | Get specific pool |
| **Pools** | `/networks/{network}/pools/multi/{addresses}` | GET | Get multiple pools (up to 30) |
| **Pools** | `/networks/{network}/pools/{pool_address}/info` | GET | Get pool token info |
| **Pools** | `/networks/{network}/tokens/{address}/pools` | GET | Get pools for a token |
| **Pools** | `/networks/{network}/dexes/{dex}/pools` | GET | Top pools on a DEX |
| **Trending** | `/networks/{network}/trending_pools` | GET | Trending pools on network |
| **Trending** | `/networks/trending_pools` | GET | Trending pools (all networks) |
| **New** | `/networks/{network}/new_pools` | GET | New pools on network |
| **New** | `/networks/new_pools` | GET | New pools (all networks) |
| **OHLCV** | `/networks/{network}/pools/{pool}/ohlcv/{timeframe}` | GET | Candlestick data |
| **Trades** | `/networks/{network}/pools/{pool}/trades` | GET | Recent trades (up to 300) |
| **Search** | `/search/pools` | GET | Search pools by query |

---

## Python Client

### Installation

```bash
pip install geckoterminal-api
```

### Synchronous Usage

```python
from geckoterminal_api import GeckoTerminalAPI

# Initialize client
gt = GeckoTerminalAPI()

# Get all networks
networks = gt.networks()

# Get token price on Ethereum
price = gt.simple_token_price(
    network="eth",
    addresses="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
)

# Get pools for a token
pools = gt.network_token_pools(
    network="eth",
    token_address="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
)

# Get trending pools on Solana
trending = gt.network_trending_pools(network="solana")

# Get new pools
new_pools = gt.network_new_pools(network="base")

# Get OHLCV data
ohlcv = gt.network_pool_ohlcv(
    network="eth",
    pool_address="0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",
    timeframe="hour",
    aggregate=1,
    limit=100
)

# Get trade history
trades = gt.network_pool_trades(
    network="solana",
    pool="69grLw4PcSypZnn3xpsozCJFT8vs8WA5817VUVnzNGTh"
)
```

### Asynchronous Usage

```python
import asyncio
from geckoterminal_api import AsyncGeckoTerminalAPI

async def main():
    agt = AsyncGeckoTerminalAPI()

    # Get networks
    networks = await agt.networks()

    # Get trending pools
    trending = await agt.network_trending_pools(network="eth")

    return networks, trending

networks, trending = asyncio.run(main())
```

### With Proxy

```python
# Synchronous
gt = GeckoTerminalAPI(proxies={
    'http': 'http://10.10.10.10:8000',
    'https': 'http://10.10.10.10:8000'
})

# Asynchronous
agt = AsyncGeckoTerminalAPI(proxy="http://proxy.com:8000")
```

---

## Node.js Client

### Installation

```bash
npm install geckoterminal-api
```

### Usage

```javascript
import { GeckoTerminalAPI } from 'geckoterminal-api';

const gt = new GeckoTerminalAPI();

// Get networks
const networks = await gt.getNetworks();

// Get DEXes on Ethereum
const dexes = await gt.getDexes('eth');

// Get token pools
const pools = await gt.getPoolsByToken('eth', '0xc02aa...');

// Get trending pools
const trending = await gt.getTrendingPoolsByNetwork('solana');

// Get OHLCV data
const ohlcv = await gt.getPoolOhlcv('eth', '0x88e6a...', {
  timeframe: 'hour',
  aggregate: 1,
  limit: 100
});

// Get recent trades
const trades = await gt.getTrades('solana', '69grLw4...');

// Search pools
const results = await gt.searchPools('PEPE');

// Get prices (up to 30 tokens)
const prices = await gt.getPrices('eth', [
  '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
  '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
]);
```

---

## Common Use Cases

### Get Token Price by Address

```python
from geckoterminal_api import GeckoTerminalAPI

gt = GeckoTerminalAPI()

# WETH on Ethereum
weth_price = gt.simple_token_price(
    network="eth",
    addresses="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
)
print(f"WETH: ${weth_price['data']['attributes']['token_prices']['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2']}")
```

### Find Best Liquidity Pool

```python
# Get all pools for a token, sorted by volume
pools = gt.network_token_pools(
    network="eth",
    token_address="0x6982508145454ce325ddbe47a25d4ec3d2311933"  # PEPE
)

# First pool has highest liquidity/volume
top_pool = pools['data'][0]
print(f"Best pool: {top_pool['attributes']['name']}")
print(f"24h Volume: ${top_pool['attributes']['volume_usd']['h24']}")
print(f"Liquidity: ${top_pool['attributes']['reserve_in_usd']}")
```

### Build Price Chart

```python
import pandas as pd

# Get 4-hour candles for last 7 days
ohlcv = gt.network_pool_ohlcv(
    network="eth",
    pool_address="0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",
    timeframe="hour",
    aggregate=4,
    limit=42  # 7 days * 6 candles/day
)

# Convert to DataFrame
candles = ohlcv['data']['attributes']['ohlcv_list']
df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
```

### Monitor New Token Launches

```python
# Get newly created pools across all networks
new_pools = gt.new_pools()

for pool in new_pools['data'][:10]:
    attrs = pool['attributes']
    print(f"Pool: {attrs['name']}")
    print(f"Network: {pool['relationships']['network']['data']['id']}")
    print(f"Created: {attrs['pool_created_at']}")
    print(f"Volume: ${attrs['volume_usd']['h24']}")
    print("---")
```

---

## Important Notes

### Timestamp Format

Always use **Unix epoch seconds**, not milliseconds:

```python
# Correct
before_timestamp = 1679414400

# Wrong - will cause errors
before_timestamp = 1679414400000
```

### Market Cap vs FDV

- `market_cap_usd` returns `null` for unlisted tokens or those without verified supply
- `fdv` (Fully Diluted Valuation) is always available, calculated from on-chain supply

### Pool Ranking

Top 20 pools are ranked by combining:
- `reserve_in_usd` (liquidity)
- `volume_usd` (24h trading volume)

### Price Reference

`price_usd` reflects the token's USD value in its first listed top pool.

---

## Troubleshooting

### Rate Limit Errors

```
Error: 429 Too Many Requests
```

**Solution:** Implement request throttling (max 30/min for free tier):

```python
import time

def rate_limited_request(func, *args, **kwargs):
    result = func(*args, **kwargs)
    time.sleep(2)  # 2 seconds = 30 requests/minute max
    return result
```

### Token Not Found

- Verify the contract address is correct
- Ensure the token has liquidity on a DEX
- Check the network ID matches where the token is deployed

### Empty OHLCV Data

- Pool may be too new (no trading history)
- Timestamp may be outside available data range (max 6 months)
- Pool may have very low volume

---

## Resources

### Official Documentation
- [API Guide](https://apiguide.geckoterminal.com/)
- [Swagger Docs](https://api.geckoterminal.com/docs/index.html)
- [DEX API Overview](https://www.geckoterminal.com/dex-api)

### Client Libraries
- [Python: geckoterminal-api](https://pypi.org/project/geckoterminal-api/)
- [Node.js: geckoterminal-api](https://github.com/alaarab/geckoterminal-api)

### Related Services
- [CoinGecko API](https://www.coingecko.com/api) - CEX data and /onchain endpoints
- [GeckoTerminal Website](https://www.geckoterminal.com/) - Web interface

---

## Version History

- **1.1.0** (2026-01-12): Enhanced with complete API reference
  - Added complete endpoint reference table (21 endpoints)
  - Enhanced pool response with all available fields (FDV, market cap, pool_created_at, native currency prices)
  - Added transaction statistics with buyer/seller counts for all time intervals
  - Added `/tokens/info_recently_updated` endpoint with network filtering
  - Added `/networks/{network}/dexes/{dex}/pools` endpoint for DEX-specific pools
  - Added `/networks/{network}/pools/{pool_address}/info` for pool token info
  - Added trade size filtering parameter for trades endpoint
  - Added network parameter for search endpoint
  - Enhanced `include` parameter documentation for all endpoints
  - Added note about token address support in OHLCV token parameter
  - Updated with API changelog updates through October 2024

- **1.0.0** (2026-01-12): Initial skill release
  - Complete GeckoTerminal API v2 documentation
  - All endpoints (networks, tokens, pools, OHLCV, trades)
  - Python client examples (sync + async)
  - Node.js client examples
  - Rate limiting guidance
  - Common use cases and troubleshooting
