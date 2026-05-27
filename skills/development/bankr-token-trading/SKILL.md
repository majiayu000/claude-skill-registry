---
name: Bankr Dev - Token Trading
description: This skill should be used when building trading bots, implementing swap functionality, or adding cross-chain bridge support. Covers same-chain swaps, cross-chain bridges, ETH/WETH conversions, and amount formats.
version: 1.0.0
---

# Token Trading Capability

Execute token swaps and trades via natural language prompts.

## What You Can Do

| Operation | Example Prompt |
|-----------|----------------|
| Buy tokens | `Buy $50 of ETH` |
| Sell tokens | `Sell 10% of my USDC` |
| Swap tokens | `Swap 0.1 ETH for USDC` |
| Cross-chain bridge | `Bridge 100 USDC from Ethereum to Base` |
| Cross-chain swap | `Swap ETH on Ethereum for USDC on Polygon` |
| Wrap ETH | `Convert 1 ETH to WETH` |
| Unwrap WETH | `Convert 1 WETH to ETH` |

## Prompt Patterns

```
Buy {amount} of {token} [on {chain}]
Sell {amount} of {token} [on {chain}]
Swap {amount} {fromToken} for {toToken} [on {chain}]
Bridge {amount} {token} from {sourceChain} to {destChain}
```

**Amount formats:**
- USD: `$50`, `$100`
- Percentage: `10%`, `50%`
- Exact: `0.5 ETH`, `100 USDC`

**Supported chains:** Base, Polygon, Ethereum, Unichain, Solana

## Usage

```typescript
import { execute } from "./bankr-client";

// Simple trade
await execute("Buy $50 of ETH on Base");

// Cross-chain
await execute("Bridge 100 USDC from Ethereum to Base");
```

## Related Skills

- `bankr-client-patterns` - Client setup and execute function
- `bankr-api-basics` - API fundamentals
- `bankr-market-research` - Price data for trading decisions
