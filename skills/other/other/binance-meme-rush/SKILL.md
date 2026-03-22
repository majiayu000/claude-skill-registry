---
name: binance-meme-rush
description: Binance Web3 official skill — real-time meme token launchpad tracking and AI-powered trending topic discovery on Solana and BSC. Sourced from github.com/binance/binance-skills-hub.
metadata: { "cryptoclaw": { "emoji": "🚀", "always": false } }
---

# Binance Meme Rush

Official Binance Web3 skill for real-time meme token discovery across launchpad lifecycles and AI-powered trending narrative tracking.

> Source: [binance/binance-skills-hub](https://github.com/binance/binance-skills-hub/tree/main/skills/binance-web3/meme-rush)

## Supported Platforms

**Solana**: Pump.fun, Moonit, Raydium, Orca, and 10+ protocols
**BSC**: Four.meme, Flap

## API 1 — Meme Rush Rank

Tracks meme tokens through three launchpad lifecycle stages.

```
POST https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/rank/list
Content-Type: application/json

{
  "chainId": "CT_501",
  "rankType": 10,
  "page": 1,
  "pageSize": 20,
  // optional filters below
  "minBondingCurveProgress": 0,
  "maxBondingCurveProgress": 100,
  "minHolders": 0,
  "minLiquidity": 0,
  "minVolume24h": 0,
  "narratives": []
}
```

`rankType` values:

- `10` — **New**: Freshly created tokens on bonding curves
- `20` — **Finalizing**: Tokens nearing migration threshold
- `30` — **Migrated**: Recently migrated to DEX

Available filters:

- Bonding curve progress range
- Holder count minimum
- Liquidity and volume thresholds
- Dev behavior flags
- Holder distribution (top10%, dev%, sniper%, KOL%, pro%)
- Social links (has website / Twitter / Telegram)
- Narratives / token tags

Response includes: token metadata, migration status and timing, bonding curve progress, holder distribution breakdown, AI-generated narratives (EN/ZH), social proof, tax rates, trading fees.

## API 2 — Topic Rush Rank

AI-powered discovery of trending market narratives.

```
GET https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/social-rush/rank/list
  ?rankType=20
  &chainId=CT_501
  &page=1
  &pageSize=20
```

`rankType` values:

- `10` — **Latest**: Newest emerging topics
- `20` — **Rising**: Topics with $1k–$20k all-time net inflows
- `30` — **Viral**: Topics exceeding $20k all-time net inflows

Response: trending topics with associated tokens ranked by net inflow.

## Key Features

- Real-time launchpad token discovery
- Dev wallet behavior analysis
- Wash trading detection
- Holder distribution metrics (top 10%, dev %, sniper %, KOL %, pro %)
- AI-generated token narratives in English and Chinese
- Social proof tracking (website, Twitter, Telegram links)
- Migration status and timing data
- Tax rate and trading fee information

## Usage Examples

```
User: Show me new meme tokens launching on Pump.fun right now
→ POST Meme Rush, chainId:CT_501, rankType:10

User: Find meme tokens about to graduate (migrate) on BSC
→ POST Meme Rush, chainId:56, rankType:20

User: What crypto narratives are trending on Solana?
→ GET Topic Rush, chainId:CT_501, rankType:30

User: Find low-risk meme tokens with real holders
→ POST Meme Rush with filters: minHolders:500, hasTwitter:true, maxDevPct:5
```

## Notes

- All numeric values returned as strings — convert before calculations
- Logo URLs require prefix: `https://bin.bnbstatic.com`
- This is for informational purposes only — not investment advice
- Meme tokens carry extremely high risk — always DYOR
