---
name: manifest
creator: bonasa-tech
description: Build and integrate Manifest DEX on Solana using the Manifest SDK. Covers market reads, order placement, wrapper and global account setup, reverse and global order types, and frontend integration patterns.
---

# Manifest DEX Integration Guide

Build trading, routing, portfolio, and frontend integrations on top of Manifest's permissionless orderbook.

## Overview

Use this skill when the task involves:

- Reading Manifest market state or orderbooks
- Placing, canceling, depositing, or withdrawing via the Manifest SDK
- Choosing between local market balances and global balances
- Handling wrapper setup, seat claims, and wallet-adapter flows
- Understanding `Limit`, `PostOnly`, `ImmediateOrCancel`, `Global`, `Reverse`, and `ReverseTight` order types

Load supporting references as needed:

- `resources/manifest-actions.md`
- `resources/manifest-sdk.md`
- `docs/troubleshooting.md`
- `examples/read-market/read-market.ts`
- `examples/wallet-order/place-order.ts`
- `examples/global-liquidity/global-order.ts`
- `examples/reverse-liquidity/amm-style-batch.ts`
- `templates/manifest-setup.ts`

## Instructions

1. Determine whether the task is read-only market access or transaction-building.
2. For read-only access, prefer `Market` reads or `ManifestClient.getClientReadOnly(...)`.
3. For transaction-building, use `getClientForMarket(...)` for signer-controlled flows, or use `getSetupIxs(...)` first and then `getClientForMarketNoPrivateKey(...)` for wallet-adapter flows.
4. Decide whether liquidity should be market-local (wrapper balances plus a market seat) or global (global account plus `OrderType.Global`).
5. If the task involves recurring two-sided liquidity, evaluate `Reverse` or `ReverseTight` instead of ordinary limit orders.
6. For UI/orderbook work, prefer `bidsL2()` and `asksL2()` for display-ready levels.
7. When documenting or implementing cleanup behavior, distinguish wrapper-level cancels from core-level cancels. `cancelAllIx()` does not fully cover all reverse/global edge cases; `cancelAllOnCoreIx()` is the stronger cleanup path.
8. State assumptions explicitly:
- cluster
- market address
- trader/signer model
- whether wrapper/global setup already exists

## Examples

### Basic Usage

When user asks: "Show the best bid and ask on a Manifest market"

The agent should:
1. Use `Market.loadFromAddress(...)` or `ManifestClient.getClientReadOnly(...)`
2. Read `bestBidPrice()` and `bestAskPrice()` or `bidsL2()` / `asksL2()`
3. Return prices without introducing signing or setup logic

### Wallet Trading Flow

When user asks: "Place a Manifest order from a browser wallet"

The agent should:
1. Call `ManifestClient.getSetupIxs(...)`
2. If setup is needed, create wrapper state and/or claim the seat first
3. Then use `ManifestClient.getClientForMarketNoPrivateKey(...)`
4. Build the order instruction with `client.placeOrderIx(...)`

### Global Liquidity Flow

When user asks: "Use the same capital across multiple Manifest markets"

The agent should:
1. Explain that market-local balances are insufficient for this requirement
2. Use global-account setup with `createGlobalAddTraderIx(...)`
3. Deposit via `globalDepositIx(...)`
4. Place `OrderType.Global` orders

### Reverse Orders

When user asks: "Provide recurring liquidity that flips after fills"

The agent should:
1. Recommend `OrderType.Reverse` or `OrderType.ReverseTight`
2. Explain that reverse orders use `spreadBps` instead of `lastValidSlot`
3. Use `ReverseTight` when tighter spread precision matters
4. Mention that cleanup may require `cancelAllOnCoreIx()` rather than only wrapper-level cancellation

Copy-paste oriented examples in this skill:

- `examples/read-market/read-market.ts`
- `examples/wallet-order/place-order.ts`
- `examples/global-liquidity/global-order.ts`
- `examples/reverse-liquidity/amm-style-batch.ts`

## Guidelines

- **DO**: Use `getSetupIxs(...)` before wallet-adapter trading flows.
- **DO**: Use `getClientReadOnly(...)` for anonymous or pre-setup inspection paths.
- **DO**: Use `bidsL2()` / `asksL2()` for UI-facing orderbook displays.
- **DO**: Separate market-local account logic from global-account logic.
- **DO**: Mention wrapper state, market seats, and global accounts explicitly when relevant.
- **DON'T**: Assume a connected wallet already has wrapper state or a market seat.
- **DON'T**: Treat `OrderType.Global` as equivalent to ordinary market-local orders.
- **DON'T**: Use `cancelAllIx()` as if it always fully cleans up reverse/global edge cases.
- **DON'T**: Ask for or embed private keys in examples.

## Common Errors

### Error: Read only

**Cause**: A write method was called on a read-only client or without a payer/wrapper context.

**Solution**: Switch to `getClientForMarket(...)` or complete the `getSetupIxs(...)` flow and then use `getClientForMarketNoPrivateKey(...)`.

### Error: Setup still required

**Cause**: Wrapper creation or market seat claim has not been completed.

**Solution**: Run the instructions returned by `ManifestClient.getSetupIxs(...)` before building normal wrapper-based trading actions.

### Error: Global order funded incorrectly

**Cause**: The trader is using `OrderType.Global` without a funded global account for the supporting token.

**Solution**: Run `createGlobalAddTraderIx(...)` if needed, then `globalDepositIx(...)`, and only then place the global order.

### Error: Reverse/global orders remain after cancel-all

**Cause**: Wrapper-level cancellation does not fully cover all core-level order states.

**Solution**: Use `cancelAllOnCoreIx()` when full core cleanup is required.

## References

- Official site: `https://manifest.trade`
- SDK package: `https://www.npmjs.com/package/@bonasa-tech/manifest-sdk`
- Source repository: `https://github.com/Bonasa-Tech/manifest`
- TypeScript client docs: `https://github.com/Bonasa-Tech/manifest/tree/main/client/ts`
