---
name: check-prod
description: Query the production Vercel database via the public API to investigate data issues
disable-model-invocation: true
argument-hint: [query description]
allowed-tools: Bash, Read
---

# Check Production Data

Query the **production** Sai Explorer API to investigate data in the Vercel Postgres database.

**Base URL**: `https://sai-explorer.vercel.app`

Use `curl -s` to fetch JSON, then pipe to `python3 -c` for parsing/filtering.

## User Request

$ARGUMENTS

## Available Endpoints

| Endpoint | Params | Description |
|----------|--------|-------------|
| `/api/trades` | `network`, `limit`, `offset` | All trades (default limit 1000) |
| `/api/user-trades` | `network`, `address` | Trades for a specific user |
| `/api/user-stats` | `network`, `address` | Aggregate stats for a user (volume, PnL, trade count) |
| `/api/user-deposits` | `network`, `address` | Deposits for a specific user |
| `/api/user-withdraws` | `network`, `address` | Withdraws for a specific user |
| `/api/stats` | `network` | Global platform stats |
| `/api/volume` | `network` | Volume leaderboard |
| `/api/deposits` | `network` | All deposits |
| `/api/withdraws` | `network` | All withdraws |
| `/api/insights` | `network` | PnL insights and analytics |
| `/api/chart-data` | `network`, `type` | Chart time series data |
| `/api/markets` | `network` | Market info |
| `/api/collateral` | `network` | Collateral breakdown |
| `/api/tvl-breakdown` | `network` | TVL by vault |

Default `network=mainnet` for all endpoints.

## Key Data Mappings

- **Micro-units**: `collateralAmount`, `realizedPnlCollateral`, `openCollateralAmount` are in micro-units (divide by 1,000,000)
- **USD conversion**: `microAmount / 1e6 * collateralPrice`
- **Collateral types**: USDC (price ~$1.0) or stNIBI (price ~$0.005)
- **Trade fields**: Nested under `trade.perpBorrowing.collateralToken.symbol` and `trade.perpBorrowing.baseToken.symbol`
- **Address formats**: Users have both Bech32 (`nibi1...`) and EVM (`0x...`) addresses

## Instructions

1. Determine which endpoint(s) to query based on the user's request
2. Fetch data with `curl -s` and parse with `python3 -c`
3. Present findings in a clear, formatted table or summary
4. If investigating data quality, check for NULL values, unexpected ranges, or inconsistencies
5. For large datasets, use `limit` and `offset` to page through results
