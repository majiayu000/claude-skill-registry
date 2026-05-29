---
name: Bankr Dev - Leverage Trading
description: This skill should be used when building perpetual trading bots, implementing leverage functionality, or adding position management. Covers Avantis integration, long/short positions, and risk controls.
version: 1.0.0
---

# Leverage Trading Capability

Trade perpetuals with leverage via natural language prompts.

## What You Can Do

| Operation | Example Prompt |
|-----------|----------------|
| Open long | `Open a 5x long on ETH with $100` |
| Open short | `Open a 3x short on BTC with $50` |
| Long with stop loss | `Open a 5x long on ETH with $100, stop loss at -10%` |
| Long with take profit | `Open a 5x long on ETH with $100, take profit at +20%` |
| Full risk management | `Open a 5x long on ETH with $100, stop loss at -10%, take profit at +20%` |
| View positions | `Show my Avantis positions` |
| Close position | `Close my ETH long position` |
| Close all | `Close all my Avantis positions` |
| Check PnL | `Check my PnL on Avantis` |

## Prompt Patterns

```
Open a {leverage}x {long|short} on {asset} with {collateral}
Open a {leverage}x long on {asset} with {collateral}, stop loss at {price|percent}
Close my {asset} {long|short} position
Show my Avantis positions
```

**Supported assets:**
- Crypto: BTC, ETH, SOL, ARB, AVAX, BNB, DOGE, LINK, OP, MATIC
- Forex: EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD
- Commodities: Gold, Silver, Oil, Natural Gas

**Chain:** Base

## Usage

```typescript
import { execute } from "./bankr-client";

// Open leveraged position
await execute("Open a 5x long on ETH with $100, stop loss at -10%");

// Check positions
await execute("Show my Avantis positions");

// Close position
await execute("Close my ETH long position");
```

## Related Skills

- `bankr-client-patterns` - Client setup and execute function
- `bankr-api-basics` - API fundamentals
- `bankr-market-research` - Price data for trading decisions
