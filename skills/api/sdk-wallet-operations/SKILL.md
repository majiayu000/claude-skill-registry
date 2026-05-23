---
name: Bankr x402 SDK - Wallet Operations
description: This skill should be used when the user asks to "set up the SDK", "initialize BankrClient", "configure wallet", "set up payment wallet", "connect wallet to Bankr", "get wallet address", "set up environment variables", "configure private key", "two wallet setup", "separate payment and trading wallets", or needs help with SDK client initialization, two-wallet configuration, wallet address derivation, environment setup, or BankrClient options.
version: 1.1.0
---

# SDK Wallet Operations

Initialize and configure the BankrClient with proper wallet setup.

## Two-Wallet System

| Wallet | Purpose | Required |
|--------|---------|----------|
| Payment (`privateKey`) | Signs x402 micropayments ($0.01/request) | Yes |
| Context (`walletAddress`) | Receives swapped tokens, NFTs | No (defaults to payment wallet) |

## Basic Setup

```typescript
import { BankrClient } from "@bankr/sdk";

const client = new BankrClient({
  privateKey: process.env.BANKR_PRIVATE_KEY as `0x${string}`,
});

const result = await client.promptAndWait({
  prompt: "What are my balances?",
});
```

## Separate Wallets (Recommended)

For enhanced security, use different wallets for payments and receiving:

```typescript
const client = new BankrClient({
  // Hot wallet with minimal USDC for payments
  privateKey: process.env.PAYMENT_WALLET_PK as `0x${string}`,
  // Cold/trading wallet receives tokens
  walletAddress: process.env.RECEIVING_WALLET,
});
```

## Configuration Options

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `privateKey` | `0x${string}` | Yes | Payment wallet private key |
| `walletAddress` | `string` | No | Override receiving wallet |
| `baseUrl` | `string` | No | API endpoint (default: production) |
| `timeout` | `number` | No | Request timeout ms (default: 600000) |

## SDK Methods

| Method | Description |
|--------|-------------|
| `promptAndWait()` | Submit prompt and wait for result |
| `prompt()` | Submit prompt, return immediately |
| `pollJob()` | Poll until job completes |
| `getJobStatus()` | Check job status once |
| `cancelJob()` | Cancel pending/processing job |
| `getWalletAddress()` | Get context wallet address |

## Per-Request Override

```typescript
// Override wallet for a single request
const result = await client.promptAndWait({
  prompt: "Swap 0.1 ETH to USDC",
  walletAddress: "0xDifferentWallet...",
});
```

## Environment Setup

```bash
# Required
BANKR_PRIVATE_KEY=0x...your_payment_wallet_key...

# Optional
BANKR_WALLET_ADDRESS=0x...your_receiving_wallet...
```

## Security Best Practices

1. **Never commit private keys** - Use environment variables
2. **Minimize payment wallet balance** - Keep only $1-2 USDC
3. **Use separate wallets** - Payment (hot) vs receiving (cold)
4. **Rotate keys periodically** - If payment wallet compromised

## Related Skills

- **sdk-capabilities**: Full list of supported operations
- **sdk-job-management**: Async job handling and polling
