---
name: four-meme
description: Discover and analyze tokens on the four.meme BSC launchpad.
metadata: { "cryptoclaw": { "emoji": "🐸", "always": true } }
---

# four.meme Launchpad

Discover and analyze memecoin launches on the four.meme BSC launchpad.

## Overview

four.meme is a memecoin launchpad on BSC where tokens are created with bonding curve mechanics. This skill covers **read-only discovery and analysis** — it does NOT auto-execute trades.

**Experimental**: Contract addresses and page structure may change. Verify before relying on cached data.

## Data Sources

### Web Fetch

Fetch trending and new token listings from the four.meme website:

```
https://four.meme
```

Parse the page for:

- Token name, symbol, contract address
- Creator address
- Current bonding curve progress
- Market cap / liquidity

### On-chain Queries

Use `read_contract` to query bonding curve contracts:

- **Token balance**: Check how many tokens remain in the curve
- **Current price**: Read the current price point on the curve
- **Graduation threshold**: When the token migrates to PancakeSwap
- **LP status**: Whether liquidity has been added to a DEX

## Workflow

1. User asks about four.meme tokens → web fetch the page
2. Extract token list with contract addresses
3. For a specific token: `read_contract` on the bonding curve for price/supply data
4. Present findings with contract address, progress, and holder count
5. If user wants to buy: direct them to use the `token-swap` skill with the contract address

## Risk Warning

Memecoins launched on four.meme carry **extreme risk**:

- Most tokens go to zero
- Bonding curves can be manipulated by creators
- Rug pulls are common — creator can dump tokens after graduation
- Low liquidity means high slippage
- Smart contract risk — contracts may not be verified

**Always remind users of these risks when discussing four.meme tokens.**

## Usage Notes

- This skill is discovery-only; actual trades go through `token-swap`
- Contract addresses for the launchpad factory may change — verify on the site
- The bonding curve contract differs from the final PancakeSwap pair
- Check if the token has graduated (migrated to DEX) before attempting swaps
- Track creator wallets for patterns across multiple launches

## Example Interactions

User: "What's trending on four.meme?"
→ Web fetch four.meme, parse trending tokens, list top 5 with progress %

User: "Analyze this four.meme token: 0x..."
→ Read bonding curve contract, report price, supply, graduation progress

User: "Has this token graduated yet?"
→ Check if liquidity exists on PancakeSwap for the token address
