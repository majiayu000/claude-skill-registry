---
name: binance-trading-signal
description: Binance Web3 official skill — Smart Money on-chain trading signals tracking professional investor buy/sell activity on BSC and Solana. Sourced from github.com/binance/binance-skills-hub.
metadata: { "cryptoclaw": { "emoji": "📡", "always": false } }
---

# Binance Smart Money Trading Signals

Official Binance Web3 skill for tracking on-chain Smart Money trading signals — follow professional investors' buy/sell activity.

> Source: [binance/binance-skills-hub](https://github.com/binance/binance-skills-hub/tree/main/skills/binance-web3/trading-signal)

## Supported Chains

| Chain  | chainId |
| ------ | ------- |
| BSC    | 56      |
| Solana | CT_501  |

## API — Smart Money Signals

```
POST https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money
Content-Type: application/json

{
  "chainId": "56",
  "page": 1,
  "pageSize": 20,
  "smartSignalType": ""    // optional filter, empty string = all
}
```

Max `pageSize`: 100.

## Response Fields

| Field             | Description                                      |
| ----------------- | ------------------------------------------------ |
| `signalId`        | Unique signal identifier                         |
| `tokenSymbol`     | Token ticker symbol                              |
| `contractAddress` | Token contract address                           |
| `logoUrl`         | Token logo (prepend `https://bin.bnbstatic.com`) |
| `direction`       | `buy` or `sell`                                  |
| `smartMoneyCount` | Number of smart money wallets involved           |
| `timeframe`       | Signal observation window                        |
| `triggerTime`     | Unix timestamp when signal was triggered         |
| `triggerPrice`    | Price at signal trigger                          |
| `currentPrice`    | Current token price                              |
| `highestPrice`    | Maximum price achieved after signal              |
| `maxGainPct`      | Maximum gain percentage from trigger             |
| `exitRate`        | Percentage of smart money that has exited        |
| `status`          | `active` / `timeout` / `completed`               |
| `tags`            | Token classifications (DEX Paid, Pumpfun, etc.)  |
| `launchPlatform`  | Origin platform (Pump.fun, Moonshot, etc.)       |

## Signal Status

- **active** — Signal is currently valid and ongoing
- **timeout** — Exceeded observation period without resolution
- **completed** — Target reached or stop loss triggered

## Usage Examples

```
User: Show me latest smart money buy signals on BSC
→ POST chainId:56, page:1, pageSize:20, direction filter: buy

User: What are smart money selling on Solana?
→ POST chainId:CT_501, smartSignalType: sell signals

User: Find tokens where smart money has max gain > 50%
→ GET signals, filter by maxGainPct > 50

User: Show active buy signals from Pump.fun tokens
→ GET signals, filter status:active + launchPlatform:pump.fun
```

## Notes

- Logo URLs require prefix: `https://bin.bnbstatic.com`
- Prices and percentages are returned as strings — convert for calculations
- This is for informational purposes only — not investment advice
- Past signal performance does not guarantee future results
