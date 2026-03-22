---
name: binance-address-info
description: Binance Web3 official skill — query any wallet address for token holdings, balances, and portfolio data across BSC, Base, and Solana. Sourced from github.com/binance/binance-skills-hub.
metadata: { "cryptoclaw": { "emoji": "👛", "always": false } }
---

# Binance Address Info

Official Binance Web3 skill for querying on-chain wallet token holdings and portfolio positions.

> Source: [binance/binance-skills-hub](https://github.com/binance/binance-skills-hub/tree/main/skills/binance-web3/query-address-info)

## Supported Chains

| Chain  | chainId |
| ------ | ------- |
| BSC    | 56      |
| Base   | 8453    |
| Solana | CT_501  |

## API — Active Token Positions

```
GET https://web3.binance.com/bapi/defi/v3/public/wallet-direct/buw/wallet/address/pnl/active-position-list
  ?address=<wallet_address>
  &chainId=<chainId>
  &offset=0             # pagination offset
```

## Response Fields

Per token holding:

| Field             | Description                                      |
| ----------------- | ------------------------------------------------ |
| `contractAddress` | Token contract address                           |
| `tokenName`       | Full token name                                  |
| `tokenSymbol`     | Token ticker                                     |
| `iconUrl`         | Token icon (prepend `https://bin.bnbstatic.com`) |
| `decimals`        | Token decimal places                             |
| `priceUsd`        | Current price in USD (string)                    |
| `priceChange24h`  | 24-hour price change percentage (string)         |
| `quantity`        | Amount held by the wallet (string)               |
| `chainId`         | Chain identifier                                 |
| `walletAddress`   | Queried wallet address                           |

## Notes

- All numeric fields (`priceUsd`, `priceChange24h`, `quantity`) are returned as strings — convert for calculations
- Icon URLs require prefix: `https://bin.bnbstatic.com`
- Use `offset` for pagination when a wallet holds many tokens
- No authentication required — public endpoint

## Usage Examples

```
User: What tokens does this wallet hold? 0xabc...
→ GET address:0xabc..., chainId:56

User: Show me my Solana portfolio
→ GET address:<solana_address>, chainId:CT_501

User: What's the total USD value of this wallet on Base?
→ GET all positions on Base, sum (quantity × priceUsd)

User: Is this wallet holding any risky tokens?
→ GET positions, then run binance-token-audit on each contract
```

## Combined Use Cases

Pair with other Binance skills for deeper analysis:

- `binance-token-audit` — audit each held token for safety
- `binance-token-info` — get detailed metadata for any holding
- `binance-trading-signal` — check if smart money is buying/selling held tokens
