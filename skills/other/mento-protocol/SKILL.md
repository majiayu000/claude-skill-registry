---
name: mento-protocol
description: 'Mento Protocol smart contracts for stablecoin swaps on Celo. Use when working with token swaps, exchange routing, quotes, Broker contract, BiPoolManager, or stablecoin operations. Triggers on: "mento", "swap", "exchange", "broker", "BiPoolManager", "stablecoin", "quote", "slippage", "route", "USDm", "EURm", "token swap".'
---

## Architecture

Mento Protocol is an on-chain AMM for stablecoins on Celo. Key contracts:

| Contract | Address | Role |
|---|---|---|
| **Broker** | `0x777A8255cA72412f0d706dc03C9D1987306B4CaD` | Entry point for all swaps |
| **BiPoolManager** | `0x22d9db95E6Ae61c104A7B6F6C78D7993B94ec901` | Manages exchange pools |

The Broker delegates to BiPoolManager, which uses SortedOracles for vAMM pricing.

## Supported Tokens (15 Mento Stablecoins)

All Mento tokens use 18 decimals. See `packages/shared/src/types/tokens.ts` for full list:

- USDm, EURm, BRLm, KESm, PHPm, COPm, XOFm, NGNm, JPYm, CHFm, ZARm, GBPm, AUDm, CADm, GHSm

Plus: USDC (6 decimals), USDT (6 decimals) as base tokens.

## Swap Flow

### 1. Find Route (`packages/contracts/src/exchanges.ts`)

```ts
import { findRoute } from '@autoclaw/contracts';

const route = await findRoute(tokenIn, tokenOut, celoClient);
// Returns ExchangeRoute[] — either 1 hop (direct) or 2 hops (via hub)
```

Routing strategy:
1. Try direct pair first
2. If no direct pool, try 2-hop via USDm hub
3. If not via USDm, try 2-hop via CELO hub

### 2. Get Quote (`packages/contracts/src/quote.ts`)

```ts
import { getQuote } from '@autoclaw/contracts';

const quote = await getQuote({
  tokenIn,
  tokenOut,
  amountIn: parseUnits('100', 18),
  tokenInDecimals: 18,
  tokenOutDecimals: 18,
  celoClient,
});
// Returns: { amountOut, rate, route, exchangeId, exchangeProvider }
```

For multi-hop routes, the quote walks each hop calling `Broker.getAmountOut()`.

### 3. Build Swap Transaction (`packages/contracts/src/swap.ts`)

```ts
import { buildSwapInTxs, applySlippage } from '@autoclaw/contracts';

const amountOutMin = applySlippage(quote.amountOut, 0.5); // 0.5% slippage

const txs = buildSwapInTxs({
  route: quote.route,
  amountIn,
  amountOutMin,
});
// Returns SwapTxData[] — one tx per hop
```

### 4. Token Approval

Before swapping, the user must approve the Broker to spend their tokens:

```ts
import { BROKER_ADDRESS } from '@autoclaw/contracts';

// Check allowance, approve if needed
// Use ERC20 approve(BROKER_ADDRESS, amount)
```

See `packages/contracts/src/allowance.ts` for approval helpers.

## Key Interfaces

```ts
interface ExchangeRoute {
  exchangeId: `0x${string}`;
  tokenIn: Address;
  tokenOut: Address;
}

interface QuoteResult {
  amountOut: bigint;
  exchangeProvider: Address;
  exchangeId: `0x${string}`;
  rate: number;
  route: ExchangeRoute[];
}

interface SwapTxData {
  to: Address;
  data: `0x${string}`;
}
```

## Route Cache

`getRoutes()` caches exchange pools for 5 minutes. Call `clearRouteCache()` to force refresh.

## Important Notes

- Mento stablecoins use 18 decimals; USDC/USDT use 6 decimals — always check with `getTokenDecimals()`
- Multi-hop swaps require separate transactions per hop (executed sequentially)
- The Broker's `swapIn` function takes: exchangeProvider, exchangeId, tokenIn, tokenOut, amountIn, amountOutMin
- Slippage is applied only to the final hop; intermediate hops use 0n for minOut
- Token addresses are in `packages/shared/src/types/tokens.ts` (MENTO_TOKEN_ADDRESSES, ALL_TOKEN_ADDRESSES)
- Contract addresses are in `packages/contracts/src/addresses.ts`
