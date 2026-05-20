---
name: mpp-tempo-method
description: Configure Tempo blockchain as an MPP payment method — USDC stablecoin payments with sub-second finality, 100,000+ TPS, and no gas volatility. Use when setting up crypto-native payment rails for machine payments.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# MPP Tempo Payment Method

## Before writing code

**Fetch live docs**:
1. Fetch `https://docs.stripe.com/payments/machine/mpp` for Stripe's Tempo integration guide
2. Web-search `tempo blockchain usdc machine payments mpp` for current Tempo chain details
3. Web-search `site:github.com stripe-samples machine-payments tempo` for Tempo payment sample code
4. Fetch `https://mpp.dev/overview` for the Tempo payment method specification

## Conceptual Architecture

### What Tempo Is

Tempo is a purpose-built blockchain for stablecoin payments and high-frequency transactions, incubated by Stripe and Paradigm. It is the primary crypto payment rail for MPP.

### Key Properties

| Property | Value |
|----------|-------|
| Chain ID | 4217 (mainnet) |
| Throughput | 100,000+ TPS |
| Finality | Sub-second |
| Gas model | No native gas token (predictable fees, no gas volatility) |
| Currency | USDC |
| USDC Contract | `0x20c000000000000000000000b9537d11c60e8b50` |
| Minimum charge | 0.01 USDC |

### Server-Side Configuration

```typescript
import { Mppx, tempo } from 'mppx/server';

const mppx = Mppx.create({
  secretKey: process.env.MPP_SECRET_KEY,
  methods: [
    tempo.charge({
      chainId: 4217,                        // Tempo mainnet
      currency: '0x20C000000000000000000000b9537d11c60E8b50',  // USDC
      recipient: process.env.TEMPO_RECIPIENT_ADDRESS,
    }),
  ],
});
```

### Payment Flow (Tempo)

1. Server returns 402 with Tempo-specific challenge (includes deposit address)
2. Client sends USDC on Tempo chain to the deposit address
3. Transaction confirms in sub-second
4. Client constructs credential with on-chain proof (tx hash)
5. Server verifies the on-chain transaction
6. Server returns resource with receipt

### Stripe Integration for Tempo

When using Stripe as the merchant backend, Tempo payments land directly in your Stripe balance:

```javascript
// Stripe PaymentIntent for crypto (requires preview API version)
const paymentIntent = await stripe.paymentIntents.create({
  amount: 1,
  currency: 'usd',
  payment_method_types: ['crypto'],
  payment_method_options: {
    crypto: {
      mode: 'deposit',
      deposit_options: {
        network: ['tempo']
      }
    }
  }
}, {
  apiVersion: '2026-03-04.preview'  // Required preview version
});
```

The response includes `next_action.crypto_display_details.deposit_addresses.tempo.address`.

### Stripe Settlement Properties

- Payments land in your Stripe balance in fiat
- Standard Stripe metrics, reporting, and multi-currency payouts apply
- Individual charges can be as low as 0.01 USDC
- Stripe uses a unique deposit address per payment for privacy
- Refunds return stablecoins to the originating wallet

### Geographic Availability

Available to developers with a **US legal entity** in all states **except** New York and Texas.

### Tempo vs Other Chains

| Property | Tempo | Base (x402) | Solana (x402) |
|----------|-------|-------------|---------------|
| Protocol | MPP | x402 | x402 |
| Finality | Sub-second | ~2 seconds | ~400ms |
| Gas model | No gas token | ETH gas | SOL gas |
| Stripe integration | Native | Via facilitator | Via facilitator |
| Sessions | Yes | No | No |

### Best Practices

- Use environment variables for recipient address and private keys
- Monitor wallet balances for receiving addresses
- Implement refund logic using the Stripe Refunds API
- Set up Stripe webhook listeners for `payment_intent.succeeded` events
- Consider multi-chain support (Tempo + Stripe SPT) for maximum client compatibility

Fetch the latest Stripe machine payments docs and Tempo blockchain documentation for current contract addresses, API versions, and chain configuration before implementing.
