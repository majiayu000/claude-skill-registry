---
name: dune
description: Execute and query Dune Analytics dashboards for on-chain data and custom SQL analytics.
metadata:
  {
    "cryptoclaw":
      { "emoji": "🔮", "requires": { "env": ["DUNE_API_KEY"] }, "primaryEnv": "DUNE_API_KEY" },
  }
---

# Dune Analytics API

Execute SQL queries on blockchain data, fetch dashboard results, and access curated datasets via the Dune API.

## Base URL

```
https://api.dune.com/api/v1
```

Requires API key: set `DUNE_API_KEY`. Free tier available at https://dune.com/settings/api

Pass via header: `X-Dune-API-Key: {key}`

## Core Workflow

### 1. Execute a Query

```
POST /query/{query_id}/execute
```

Body (optional filters):

```json
{
  "query_parameters": {
    "wallet_address": "0x...",
    "token_address": "0x..."
  }
}
```

Returns `execution_id` for polling.

### 2. Check Execution Status

```
GET /execution/{execution_id}/status
```

States: `QUERY_STATE_PENDING`, `QUERY_STATE_EXECUTING`, `QUERY_STATE_COMPLETED`, `QUERY_STATE_FAILED`

Poll every 2-3 seconds until completed.

### 3. Get Results

```
GET /execution/{execution_id}/results
```

Returns rows as JSON with column metadata. Use `?limit=100&offset=0` for pagination.

### Shortcut: Get Latest Results

```
GET /query/{query_id}/results
```

Returns cached results from the last execution without re-running. Fast and free of execution credits.

## Useful Public Query IDs

| Query ID  | Description                       |
| --------- | --------------------------------- |
| `3237721` | Top DEX traders by volume (7d)    |
| `3105506` | Whale token transfers (24h)       |
| `2030664` | Stablecoin flows by chain         |
| `1847958` | NFT marketplace volume comparison |
| `3532352` | Bridge volume across chains       |
| `2474310` | Gas spent by protocol (Ethereum)  |

Note: Public query IDs may change or become unavailable. Verify before relying on them.

## Writing Custom Queries

### Create a Query

```
POST /query
```

Body:

```json
{
  "name": "My Query",
  "query_sql": "SELECT * FROM ethereum.transactions WHERE \"from\" = {{wallet_address}} ORDER BY block_time DESC LIMIT 100",
  "is_private": false
}
```

### Key Tables

| Table                         | Chain    | Description            |
| ----------------------------- | -------- | ---------------------- |
| `ethereum.transactions`       | ETH      | All transactions       |
| `bnb.transactions`            | BSC      | BSC transactions       |
| `polygon.transactions`        | Polygon  | Polygon transactions   |
| `arbitrum.transactions`       | Arbitrum | Arbitrum transactions  |
| `erc20_ethereum.evt_Transfer` | ETH      | ERC-20 transfer events |
| `erc20_bnb.evt_Transfer`      | BSC      | BEP-20 transfer events |
| `dex.trades`                  | Multi    | Aggregated DEX trades  |
| `nft.trades`                  | Multi    | Aggregated NFT trades  |
| `prices.usd`                  | Multi    | Token prices (hourly)  |
| `tokens.erc20`                | Multi    | Token metadata         |

### DuneSQL Syntax Notes

- DuneSQL is based on Trino (Presto fork)
- Use double quotes for column names with special chars: `"from"`, `"to"`
- Byte arrays (addresses): `0x` prefix works, use `LOWER()` for case-insensitive matching
- Timestamps: `block_time` is TIMESTAMP type, use `NOW() - INTERVAL '7' DAY` for ranges
- Aggregations: standard SQL — `SUM()`, `COUNT()`, `AVG()`, `GROUP BY`
- Use `LIMIT` always — avoid unbounded queries

### Example Custom Queries

Wallet transaction count (last 30 days):

```sql
SELECT COUNT(*) as tx_count, SUM(value / 1e18) as total_eth
FROM ethereum.transactions
WHERE "from" = {{wallet_address}}
  AND block_time > NOW() - INTERVAL '30' DAY
```

Top tokens by transfer volume (24h):

```sql
SELECT t.symbol, COUNT(*) as transfers, SUM(evt.value / POW(10, t.decimals)) as volume
FROM erc20_ethereum.evt_Transfer evt
JOIN tokens.erc20 t ON t.contract_address = evt.contract_address AND t.blockchain = 'ethereum'
WHERE evt.evt_block_time > NOW() - INTERVAL '1' DAY
GROUP BY t.symbol
ORDER BY transfers DESC
LIMIT 20
```

## API Limits (Free Tier)

- 10 query executions per day (re-execute)
- 250 datapoints per result
- Cached results (`/query/{id}/results`) do not count against execution limits
- Prefer cached results when freshness is not critical

## Usage Notes

- **Prefer cached results** (`GET /query/{id}/results`) over re-executing queries to conserve credits
- For wallet-specific analysis, pass the address as a `query_parameter` rather than hardcoding
- Always use `LIMIT` in custom SQL to avoid timeouts and large payloads
- Combine with `debank` for real-time portfolio data and `defillama` for protocol-level TVL
- When building custom queries, test with small limits first
- Present results in tables or summaries — raw Dune output can be verbose

## Example Interactions

User: "Show top DEX traders this week"
→ Fetch cached results from query 3237721, present top 10 by volume

User: "How many transactions has my wallet done?"
→ Execute custom query with wallet_address parameter, report count and total value

User: "What are the biggest token transfers today?"
→ Fetch cached whale transfer query, present top movers

User: "Write a query to find all USDT transfers over $100k on BSC"
→ Create custom SQL on `erc20_bnb.evt_Transfer`, filter by USDT address and amount threshold
