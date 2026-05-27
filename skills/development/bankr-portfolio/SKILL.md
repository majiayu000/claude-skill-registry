---
name: Bankr Dev - Portfolio
description: This skill should be used when building portfolio dashboards, implementing balance checking, or adding multi-chain holdings views. Covers balances, holdings, and valuations across chains.
version: 1.0.0
---

# Portfolio Capability

Query portfolio data and balances via natural language prompts.

## What You Can Do

| Operation | Example Prompt |
|-----------|----------------|
| Total portfolio | `Show my portfolio` |
| Total balance | `What's my total balance?` |
| All holdings | `List all my crypto holdings` |
| Wallet value | `How much is my wallet worth?` |
| Chain balance | `Show my Base balance` |
| Chain holdings | `What tokens do I have on Polygon?` |
| Token balance | `How much ETH do I have?` |
| Token across chains | `Show my USDC on all chains` |
| Largest holding | `What's my largest holding?` |
| Token location | `Where do I have the most ETH?` |

## Prompt Patterns

```
Show my portfolio
What's my total balance?
Show my {chain} balance
How much {token} do I have?
Show my {token} on all chains
What tokens do I have on {chain}?
```

**Supported chains:** Base, Polygon, Ethereum, Unichain, Solana

## Usage

```typescript
import { execute } from "./bankr-client";

// Full portfolio
await execute("Show my portfolio");

// Chain-specific
await execute("Show my Base balance");

// Token-specific
await execute("How much ETH do I have?");

// Token across chains
await execute("Show my USDC on all chains");
```

## Related Skills

- `bankr-client-patterns` - Client setup and execute function
- `bankr-api-basics` - API fundamentals
- `bankr-token-trading` - Trade based on portfolio data
