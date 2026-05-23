---
name: market-data
description: Fetch cryptocurrency prices, market caps, charts, and trending tokens.
metadata: { "cryptoclaw": { "emoji": "📊", "always": true } }
---

# Market Data Skill

Fetch cryptocurrency prices, market caps, charts, and trending tokens.

## Overview

Provide real-time and historical market data for cryptocurrencies using public APIs (CoinGecko free tier).

## Capabilities

- **Price lookup**: Current price of any token in USD/BTC/ETH
- **Market overview**: Top tokens by market cap, 24h volume, gainers/losers
- **Trending tokens**: Currently trending on CoinGecko
- **Price history**: Historical price data for charting
- **Token search**: Find tokens by name or symbol

## Data Sources

- CoinGecko API (free, no key required for basic queries)
- On-chain price from DEX pools via `read_contract` when needed

## Example Interactions

User: "What's the price of ETH?"
Action: Query CoinGecko for ethereum price, report USD value and 24h change

User: "Show me trending tokens"
Action: Query CoinGecko trending endpoint, list top 10 with prices

User: "How has BNB performed this week?"
Action: Query 7-day price history, summarize with high/low/change

## Notes

- Rate limits: CoinGecko free tier allows ~30 calls/minute
- For on-chain token prices, use DEX router contracts
- Always show the data source and timestamp
- For detailed CoinGecko API usage (endpoints, parameters, ID lookup), see the `coingecko` skill
