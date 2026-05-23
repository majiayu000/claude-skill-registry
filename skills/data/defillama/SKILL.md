---
name: defillama
description: Query DeFiLlama for TVL, protocol analytics, yield pools, and stablecoin data.
metadata: { "cryptoclaw": { "emoji": "🦙", "always": true } }
---

# DeFiLlama API

Query DeFi protocol TVL, yield farming opportunities, chain analytics, and stablecoin data via the free DeFiLlama API.

## Base URLs

- **TVL & Protocols**: `https://api.llama.fi`
- **Yields**: `https://yields.llama.fi`
- **Stablecoins**: `https://stablecoins.llama.fi`
- **Coins (prices)**: `https://coins.llama.fi`

No API key required. No strict rate limits, but be respectful.

## Endpoints

### Protocol List

```
GET https://api.llama.fi/v2/protocols
```

Returns all tracked protocols with current TVL, chain breakdown, category, and URL. **Large payload** — always filter or limit output to top N results.

### Protocol TVL History

```
GET https://api.llama.fi/v2/tvl/{protocol}
```

- `protocol`: slug from protocols list (see table below)
- Returns daily TVL data points

### Protocol Detail

```
GET https://api.llama.fi/protocol/{protocol}
```

Returns full protocol info: TVL per chain, token breakdown, governance token, audits.

### Chain TVL

```
GET https://api.llama.fi/v2/chains
```

Returns TVL for every tracked chain. Useful for chain comparison.

### Yield Pools

```
GET https://yields.llama.fi/pools
```

Returns all tracked yield pools. **Very large payload** — always filter by chain or project in your output.

Useful fields per pool: `chain`, `project`, `symbol`, `tvlUsd`, `apy`, `apyBase`, `apyReward`, `stablecoin`.

### Stablecoins

```
GET https://stablecoins.llama.fi/stablecoins?includePrices=true
```

Returns all stablecoins with circulating supply, peg data, and chain breakdown.

### Token Prices

```
GET https://coins.llama.fi/prices/current/{coins}
```

- `coins`: comma-separated in format `{chain}:{address}` (e.g., `bsc:0x0E09...`)
- Chain keys: `bsc`, `ethereum`, `polygon`, `arbitrum`, `optimism`, `base`

## Common Protocol Slugs

| Protocol       | Slug             |
| -------------- | ---------------- |
| PancakeSwap    | pancakeswap      |
| Uniswap        | uniswap          |
| Aave V3        | aave-v3          |
| Lido           | lido             |
| Curve          | curve-finance    |
| MakerDAO       | makerdao         |
| Compound       | compound-finance |
| GMX            | gmx              |
| Convex         | convex-finance   |
| Rocket Pool    | rocket-pool      |
| Venus          | venus            |
| Alpaca Finance | alpaca-finance   |
| Biswap         | biswap           |
| Radiant        | radiant-v2       |

## Usage Notes

- **Large payloads**: The `/v2/protocols` and `/pools` endpoints return massive JSON arrays. Always extract and present only the top N items relevant to the user's query.
- Combine with CoinGecko for token price context and with `read_contract` for on-chain verification of TVL claims.
- When presenting yield data, always note that APY is historical and not guaranteed.
- Sort pools by TVL to surface safer opportunities first.

## Example Queries

User: "What's the TVL of PancakeSwap?"
→ Fetch `https://api.llama.fi/v2/tvl/pancakeswap`, report latest TVL

User: "Top yield pools on BSC"
→ Fetch `/pools`, filter `chain === "BSC"`, sort by `tvlUsd` desc, show top 10 with APY

User: "Compare TVL across chains"
→ Fetch `/v2/chains`, sort by `tvl` desc, present top 10
