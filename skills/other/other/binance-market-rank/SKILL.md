---
name: binance-market-rank
description: Binance Web3 official skill — crypto market rankings including trending tokens, smart money inflow, social hype, meme ranks, and top trader PnL leaderboards. Sourced from github.com/binance/binance-skills-hub.
metadata: { "cryptoclaw": { "emoji": "📊", "always": false } }
---

# Binance Crypto Market Rank

Official Binance Web3 skill for market rankings and leaderboards across BSC, Base, Solana, and Ethereum.

> Source: [binance/binance-skills-hub](https://github.com/binance/binance-skills-hub/tree/main/skills/binance-web3/crypto-market-rank)

## Supported Chains

| Chain    | chainId |
| -------- | ------- |
| BSC      | 56      |
| Base     | 8453    |
| Solana   | CT_501  |
| Ethereum | 1       |

## API 1 — Social Hype Leaderboard

Tokens ranked by social media sentiment and engagement.

```
GET https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/social/rank/list
```

Parameters:

- `chainId`: chain identifier
- `sentiment`: `All` | `Positive` | `Negative` | `Neutral`
- `language`: e.g. `en`
- `timeRange`: time window for sentiment analysis

Response includes: token logo, symbol, address, market cap, price change, social summary, sentiment breakdown.

## API 2 — Unified Token Rank

Multi-category token rankings.

```
POST https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rank/unified
```

`rankType` values:

- `10` — Trending tokens
- `11` — Most searched
- `20` — Binance Alpha picks
- `40` — Tokenized stocks

Filters supported: price change range, market cap range, liquidity threshold, holder count, transaction count, launch time, audit status, social presence, KYC status.

Sorting: search count, volume, market cap, holder count, unique traders, price change (5m/1h/6h/24h).

Max page size: 200.

## API 3 — Smart Money Inflow Rank

Tokens receiving the most institutional/smart money buying.

```
POST https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rank/smart-money-inflow
```

Parameters:

- `chainId`
- `period`: `5m` | `1h` | `6h` | `24h`
- `page`, `pageSize`

Response: token data, inflow amount (USD), smart money trader count, risk level.

## API 4 — Meme Rank

Top meme tokens from Pulse launchpad with breakout scoring.

```
GET https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/meme/rank
```

Parameters: `chainId`, sorting options, pagination.

Includes Binance user engagement metrics and algorithmic breakout scores.

## API 5 — Address PnL Rank

Top trader leaderboard with performance metrics.

```
GET https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/address/pnl/rank
```

Parameters:

- `chainId`
- `period`: `7d` | `30d` | `90d`
- `page`, `pageSize` (max 25 per page)

Response: realized PnL, win rate, trading volume, token performance breakdown.

## Notes

- All numeric fields are returned as strings — convert before calculations
- Logo URLs require prefix: `https://bin.bnbstatic.com`
- Max page size: 200 for token queries, 25 for address queries
- Timestamps are in milliseconds

## Usage Examples

```
User: Show me trending tokens on BSC
→ POST Unified Token Rank, chainId:56, rankType:10

User: Which tokens are smart money buying on Solana right now?
→ POST Smart Money Inflow Rank, chainId:CT_501, period:1h

User: Show top traders by PnL this month on Base
→ GET Address PnL Rank, chainId:8453, period:30d
```
