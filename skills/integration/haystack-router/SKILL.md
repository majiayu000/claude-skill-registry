---
name: haystack-router
description: >-
  Route and execute optimal token swaps on Algorand using Haystack Router,
  a DEX aggregator and smart order routing protocol. Use when building swap
  interfaces, getting best-price quotes across multiple Algorand DEXes and
  LST protocols, executing atomic swaps, integrating token exchange into
  React apps with use-wallet, automating swaps from Node.js, or migrating
  from @txnlab/deflex.
---

# Haystack Router

Haystack Router is a DEX aggregator and smart order routing protocol on Algorand. It finds optimal swap routes across multiple DEXes (Tinyman V2, Pact, Folks) and LST protocols (tALGO, xALGO), then executes them atomically through on-chain smart contracts.

Formerly known as Deflex (originally developed by Defly and Alammex), acquired by TxnLab and rebranded as Haystack Router.

## Package

`@txnlab/haystack-router` — TypeScript SDK for DEX-aggregated swaps. Requires `algosdk` (v3+) as a peer dependency.

```bash
npm install @txnlab/haystack-router algosdk
```

**API key required.** A free tier key is available for immediate use — see [configuration.md](references/configuration.md) for details.

## Core Flow

```typescript
import { RouterClient } from '@txnlab/haystack-router'

// 1. Initialize
const router = new RouterClient({
  apiKey: '1b72df7e-1131-4449-8ce1-29b79dd3f51e', // Free tier (60 requests/min)
})

// 2. Get a quote
const quote = await router.newQuote({
  fromASAID: 0, // ALGO
  toASAID: 31566704, // USDC
  amount: 1_000_000, // 1 ALGO (base units)
  address: activeAddress,
})

// 3. Execute the swap
const swap = await router.newSwap({
  quote,
  address: activeAddress,
  signer: transactionSigner,
  slippage: 1, // 1%
})
const result = await swap.execute()
```

The SDK is the **only** supported integration path. Do not call the API directly.

## Key Concepts

- **Amounts** are always in base units (microAlgos for ALGO, smallest unit for ASAs)
- **ASA IDs**: 0 = ALGO, 31566704 = USDC, etc.
- **Quote types**: `fixed-input` (default) — specify input amount; `fixed-output` — specify desired output
- **Slippage**: Percentage tolerance on output (e.g., 1 = 1%). Applied to the final output, not individual hops
- **Routing**: Supports multi-hop and parallel (combo) swaps for optimal pricing
- **Middleware**: Plugin system for custom pre/post-swap transactions (e.g., auto opt-out)

## Reference Files

Read the appropriate file based on the task:

| Task                                  | Reference                                                 |
| ------------------------------------- | --------------------------------------------------------- |
| Install SDK, initialize RouterClient  | [getting-started.md](references/getting-started.md)       |
| Get swap quotes, display pricing      | [quotes.md](references/quotes.md)                         |
| Execute swaps, sign transactions      | [swaps.md](references/swaps.md)                           |
| Build React swap UI with use-wallet   | [react-integration.md](references/react-integration.md)   |
| Automate swaps from Node.js scripts   | [node-automation.md](references/node-automation.md)       |
| RouterClient config, slippage, assets | [configuration.md](references/configuration.md)           |
| Fee structure, referral program       | [fees-and-referrals.md](references/fees-and-referrals.md) |
| Migrate from @txnlab/deflex           | [migration.md](references/migration.md)                   |
| Full API surface and types            | [api-reference.md](references/api-reference.md)           |
