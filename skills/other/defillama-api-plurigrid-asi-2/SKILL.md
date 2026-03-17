---
name: defillama-api
description: DefiLlama API integration for DeFi analytics - TVL, prices, yields, volumes, fees, bridges, and DAT data. Use for blockchain/DeFi research, protocol analysis, and market data queries.
trit: -1
color: "#4A90D9"
---

# DefiLlama API

**Trit**: -1 (MINUS - Validator/Data Source)
**Color**: #4A90D9 (Cold blue, 210°)

Comprehensive DeFi data from DefiLlama's API ecosystem.

## Base URLs

| API | Base URL | Auth |
|-----|----------|------|
| Pro API | `https://pro-api.llama.fi` | Key in path: `/API_KEY/endpoint` |
| Bridge API | `https://bridges.llama.fi` | None |

## Quick Reference

### TVL & Protocols
```bash
# All protocols with TVL
GET /api/protocols

# Single protocol detail
GET /api/protocol/{slug}

# Chain TVL
GET /api/v2/chains
GET /api/v2/historicalChainTvl/{chain}
```

### Prices
```bash
# Current prices (chain:address format)
GET /coins/prices/current/{coins}

# Historical
GET /coins/prices/historical/{timestamp}/{coins}

# Chart data
GET /coins/chart/{coins}?period=30d
```

### Yields (Pro)
```bash
GET /yields/pools           # All yield pools
GET /yields/chart/{pool}    # Pool history
GET /yields/poolsBorrow     # Borrow rates
GET /yields/perps           # Perp funding
GET /yields/lsdRates        # LSD rates
```

### Volume
```bash
GET /api/overview/dexs              # DEX volumes
GET /api/overview/dexs/{chain}      # Chain DEX
GET /api/summary/dexs/{protocol}    # Protocol detail
GET /api/overview/options           # Options
GET /api/overview/derivatives       # Derivatives (Pro)
```

### Fees & Revenue
```bash
GET /api/overview/fees              # All fees
GET /api/overview/fees/{chain}      # Chain fees
GET /api/summary/fees/{protocol}    # Protocol fees
# dataType: dailyFees | dailyRevenue | dailyHoldersRevenue
```

### Bridges
```bash
# Base: https://bridges.llama.fi
GET /bridges                        # All bridges
GET /bridge/{id}                    # Bridge detail
GET /bridgevolume/{chain}           # Volume by chain
GET /transactions/{id}              # Bridge txs
```

### DAT (Digital Asset Treasury)
```bash
GET /dat/institutions               # All institutions
GET /dat/institutions/{symbol}      # e.g., MSTR
```

## Usage Script

```clojure
;; See scripts/defillama.bb for full implementation
(require '[defillama :as dl])

;; TVL
(dl/protocols)
(dl/protocol "aave")
(dl/chain-tvl "Ethereum")

;; Prices
(dl/price "ethereum:0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
(dl/price-chart "coingecko:ethereum" {:period "30d"})

;; Yields
(dl/yield-pools)
(dl/pool-chart "747c1d2a-c668-4682-b9f9-296708a3dd90")

;; Volumes
(dl/dex-overview)
(dl/dex-protocol "uniswap")

;; Fees
(dl/fees-overview)
(dl/fees-protocol "hyperliquid")
```

## Endpoint Categories

### Free Endpoints
- `/api/protocols`, `/api/protocol/{slug}`, `/api/tvl/{slug}`
- `/api/v2/chains`, `/api/v2/historicalChainTvl`
- `/coins/prices/*`, `/coins/chart/*`
- `/api/overview/dexs`, `/api/overview/options`
- `/api/overview/fees`, `/api/summary/fees/*`

### Pro Endpoints (API Key Required)
- `/yields/*` - All yield endpoints
- `/api/overview/derivatives`
- `/api/tokenProtocols/{symbol}`
- `/api/inflows/{protocol}/{timestamp}`
- `/api/chainAssets`
- `/api/emissions`, `/api/emission/{protocol}`
- `/api/categories`, `/api/forks`, `/api/oracles`
- `/api/entities`, `/api/treasuries`
- `/api/hacks`, `/api/raises`
- `/etfs/*`, `/dat/*`
- Bridge endpoints on bridges.llama.fi

## Response Patterns

### TVL Response
```json
{"id": "2269", "name": "Aave", "tvl": 5200000000, "chains": ["Ethereum"]}
```

### Price Response
```json
{"coins": {"ethereum:0x...": {"price": 0.999, "symbol": "USDC", "confidence": 0.99}}}
```

### Yield Pool Response
```json
{"pool": "uuid", "chain": "Ethereum", "project": "aave-v3", "apy": 3.5, "tvlUsd": 1500000000}
```

## GF(3) Integration

This skill serves as MINUS (-1) validator in triads:
- Provides authoritative DeFi data
- Validates protocol metrics
- Constrains analysis with real data

Compose with:
- `aptos-agent` (+1): Execute based on data
- `exa-search` (0): Enrich with web context
