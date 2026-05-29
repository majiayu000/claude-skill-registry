---
name: Bankr Dev - Automation
description: This skill should be used when building automated trading systems, implementing limit orders, or adding DCA/TWAP functionality. Covers limit orders, stop losses, DCA schedules, and TWAP execution.
version: 1.0.0
---

# Automation Capability

Create and manage automated orders via natural language prompts.

## What You Can Do

| Operation | Example Prompt |
|-----------|----------------|
| Limit buy | `Set a limit order to buy ETH at $3,000` |
| Limit buy with amount | `Set a limit order to buy $500 of ETH at $3,000` |
| Limit sell | `Limit sell my ETH when it hits $4,000` |
| Stop loss (price) | `Set stop loss for my ETH at $2,800` |
| Stop loss (percent) | `Stop loss: sell ETH if it drops 10%` |
| DCA | `DCA $100 into ETH every week` |
| DCA with duration | `DCA $50 into BTC every day for 1 month` |
| TWAP buy | `TWAP buy $5000 of ETH over 24 hours` |
| TWAP sell | `TWAP sell 1 ETH over 4 hours` |
| Scheduled command | `Every Monday, buy $100 of ETH` |
| View automations | `Show my automations` |
| View limit orders | `What limit orders do I have?` |
| Cancel automation | `Cancel automation abc123` |
| Cancel all | `Cancel all my automations` |

## Prompt Patterns

```
Set a limit order to buy {token} at {price}
Set stop loss for my {token} at {price|percent}
DCA {amount} into {token} {frequency} [for {duration}]
TWAP buy {amount} of {token} over {duration}
Show my automations
Cancel automation {id}
```

**Frequencies:** every hour, every day, every week, every month

**Supported chains:** Base, Polygon, Ethereum (EVM), Solana (Jupiter triggers)

## Usage

```typescript
import { execute } from "./bankr-client";

// Create limit order
await execute("Set a limit order to buy $500 of ETH at $3,000");

// Create DCA
await execute("DCA $100 into ETH every week for 3 months");

// Create TWAP
await execute("TWAP buy $5000 of ETH over 24 hours");

// View automations
await execute("Show my automations");
```

## Related Skills

- `bankr-client-patterns` - Client setup and execute function
- `bankr-api-basics` - API fundamentals
- `bankr-token-trading` - Immediate trades
