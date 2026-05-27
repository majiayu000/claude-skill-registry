---
name: Bankr Dev - Transfers
description: This skill should be used when building payment systems, implementing token transfers, or adding ENS/social handle resolution. Supports wallet addresses, ENS names, and social handles.
version: 1.0.0
---

# Transfers Capability

Send tokens to any recipient via natural language prompts.

## What You Can Do

| Operation | Example Prompt |
|-----------|----------------|
| Send to address | `Send 0.1 ETH to 0x1234...abcd` |
| Send to ENS | `Send $50 USDC to vitalik.eth` |
| Send to Twitter | `Send $5 ETH to @username on Twitter` |
| Send to Farcaster | `Send 10 USDC to @user on Farcaster` |
| Send to Telegram | `Send 0.01 ETH to @user on Telegram` |
| Percentage send | `Send 10% of my ETH to 0x...` |

## Prompt Patterns

```
Send {amount} {token} to {recipient} [on {chain}]
```

**Recipient formats:**
- Wallet address: `0x1234...abcd`
- ENS name: `vitalik.eth`, `name.eth`
- Social handle: `@username on Twitter/Farcaster/Telegram`

**Amount formats:**
- USD: `$50`, `$100`
- Percentage: `10%`, `50%`
- Exact: `0.5 ETH`, `100 USDC`

**Supported chains:** Base, Polygon, Ethereum, Unichain, Solana

## Usage

```typescript
import { execute } from "./bankr-client";

// To ENS
await execute("Send 0.1 ETH to vitalik.eth on Base");

// To social handle
await execute("Send $5 ETH to @user on Twitter");
```

## Related Skills

- `bankr-client-patterns` - Client setup and execute function
- `bankr-api-basics` - API fundamentals
- `bankr-portfolio` - Check balances before transfers
