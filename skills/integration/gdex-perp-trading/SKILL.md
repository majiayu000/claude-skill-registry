---
name: gdex-perp-trading
description: HyperLiquid perpetual futures — open/close positions, set leverage, place market and limit orders with TP/SL, and manage open orders
---

# GDEX: Perpetual Futures Trading (HyperLiquid)

Trade perpetual futures on HyperLiquid through GDEX managed-custody. Supports long/short positions, configurable leverage, take-profit/stop-loss, and market/limit orders.

## When to Use

- Opening or closing perp positions
- Setting leverage for an asset
- Placing HL orders (market/limit) with TP/SL
- Querying positions, mark prices, or account state
- Canceling orders

## Prerequisites

- `@gdexsdk/gdex-skill` installed
- Authenticated via `loginWithApiKey()` — see **gdex-authentication**
- USDC deposited to HyperLiquid — see **gdex-perp-funding**

## Open a Position

```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY } from '@gdexsdk/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);

const pos = await skill.openPerpPosition({
  coin: 'BTC',                // asset symbol
  side: 'long',               // 'long' or 'short'
  sizeUsd: '1000',            // collateral in USD
  leverage: 10,               // 1–50× (default: 5)
  takeProfitPrice: '110000',  // optional TP
  stopLossPrice: '95000',     // optional SL
  marginMode: 'cross',        // 'cross' or 'isolated' (default: 'cross')
});
```

## Close a Position

```typescript
// Close 100% (default)
await skill.closePerpPosition({ coin: 'BTC' });

// Partial close
await skill.closePerpPosition({ coin: 'ETH', closePercent: 50 });
```

## Set / Update Leverage

> **WARNING:** The `hlUpdateLeverage` / `/v1/hl/update_leverage` endpoint **is not implemented** on the backend (returns 404). Leverage is set automatically when the backend executes orders — it calls `setMaxLeverage()` internally before each trade. You can control effective leverage through position sizing relative to your account balance.

```typescript
// Simple (may not work — backend endpoint not implemented)
await skill.setPerpLeverage({ coin: 'BTC', leverage: 20 });

// Via HL managed-custody (ENDPOINT NOT IMPLEMENTED — returns 404)
// await skill.hlUpdateLeverage({
//   coin: 'BTC',
//   leverage: 40,
//   isCross: true,
//   apiKey,
//   walletAddress,  // control address, not managed
//   sessionPrivateKey,
// });

// ✅ Leverage is set automatically by the backend before each order.
// Control effective leverage via position sizing:
//   10 USDC balance, 0.001 BTC @ $67k = ~$67 notional → ~6.7x effective leverage
```

## Query Positions & Account State

```typescript
// Get open positions
const positions = await skill.getPerpPositions({
  walletAddress: '0xYourAddress',
  coin: 'BTC',   // optional filter
});
// Each: { coin, side, size, entryPrice, markPrice, leverage, unrealizedPnl, liquidationPrice }

// Full account state
const state = await skill.getHlAccountState({ walletAddress: '0xYourAddress' });
// { accountValue, totalNtlPos, totalRawUsd, totalMarginUsed, withdrawable, positions[] }

// Mark price for an asset
const price = await skill.getHlMarkPrice({ coin: 'BTC' });
```

## Place Orders (HL Managed-Custody)

### Market Order with TP/SL

```typescript
await skill.hlCreateOrder({
  coin: 'ETH',
  isLong: true,
  price: '0',       // '0' for market orders
  size: '0.5',      // position size
  reduceOnly: false,
  isMarket: true,
  tpPrice: '4000',  // take-profit (optional)
  slPrice: '3200',  // stop-loss (optional)
  apiKey,
  walletAddress,
  sessionPrivateKey,
});
```

### Simple Order (no TP/SL)

```typescript
await skill.hlPlaceOrder({
  coin: 'SOL',
  isLong: false,     // short
  price: '180',      // limit price
  size: '10',
  reduceOnly: false,
  apiKey,
  walletAddress,
  sessionPrivateKey,
});
```

## Cancel Orders

```typescript
// Cancel specific order
await skill.hlCancelOrder({
  coin: 'BTC',
  orderId: '12345',
  apiKey,
  walletAddress,
  sessionPrivateKey,
});

// Cancel all orders
await skill.hlCancelAllOrders({
  apiKey,
  walletAddress,
  sessionPrivateKey,
});
```

## Close All Positions

> **WARNING:** The `hlCloseAll` / `/v1/hl/close_all_positions` endpoint is unreliable — it frequently returns `TIMEOUT` or JSON parse errors from the backend. **Use a reduce-only order instead** (see below).

```typescript
// ❌ Unreliable — may timeout
await skill.hlCloseAll({
  apiKey,
  walletAddress,   // MUST be control address, not managed address
  sessionPrivateKey,
});

// ✅ Reliable — close via reduce-only sell order
// To close a LONG position, place a SHORT reduce-only order for the exact size:
const btcPrice = await skill.getHlMarkPrice('BTC');
await skill.hlCreateOrder({
  coin: 'BTC',
  isLong: false,                               // opposite of your position
  price: Math.round(btcPrice * 0.97).toString(), // 3% below mid for market sell
  size: '0.001',                                 // exact position size
  reduceOnly: true,                              // close only, don't open new position
  isMarket: true,
  tpPrice: '0',
  slPrice: '0',
  apiKey,
  walletAddress,   // MUST be control address
  sessionPrivateKey,
});
```

## HL ABI Schemas (Critical)

HL operations use a **different crypto pipeline** than spot trades. Getting any detail wrong produces `400 Unauthorized (code 103)`.

| Action | ABI Types | Fields |
|--------|-----------|--------|
| `hl_deposit` | `['uint64', 'address', 'uint256', 'string']` | `[chainId, tokenAddress, amount, nonce]` |
| `hl_withdraw` | `['string', 'string']` | `[amount, nonce]` |
| `hl_create_order` | `['string', 'bool', 'string', 'string', 'bool', 'string', 'string', 'string', 'bool']` | `[coin, isLong, price, size, reduceOnly, nonce, tpPrice, slPrice, isMarket]` |
| `hl_place_order` | `['string', 'bool', 'string', 'string', 'bool', 'string']` | `[coin, isLong, price, size, reduceOnly, nonce]` |
| `hl_close_all` | `['string']` | `[nonce]` |
| `hl_cancel_order` | `['string', 'string', 'string']` | `[nonce, coin, orderId]` |
| `hl_cancel_all_orders` | `['string']` | `[nonce]` |
| `hl_update_leverage` | `['string', 'uint32', 'bool', 'string']` | `[coin, leverage, isCross, nonce]` |

**CRITICAL:** `hl_deposit` chainId is `uint64`, NOT `uint256`. This is the #1 cause of Unauthorized errors. The backend re-encodes with `uint64` for signature verification — if you encode with `uint256`, the hex differs and you get code 103.

## HL Managed-Custody Credentials

All HL write operations require `HlManagedCredentials`:

```typescript
interface HlManagedCredentials {
  apiKey: string;            // GDEX API key for AES encryption
  walletAddress: string;     // CONTROL wallet address (from sign-in), NOT managed address
  sessionPrivateKey: string; // Session key from sign-in flow
}
```

## Default HL Assets

BTC, ETH, SOL, DOGE, AVAX, APE, APT, ARB, ATOM, BCH, BLUR, BNB, COMP, CRV, DOT, EOS, FIL, FTM, HBAR, ICP, IMX, INJ, JUP, KPEPE, LDO, LINK, LTC, MATIC, MKR, NEAR, OP, ORDI, PEPE, PYTH, RNDR, RUNE, SEI, SHIB, SNX, STX, SUI, TIA, TON, TRX, UNI, WIF, WLD, XRP

## Critical: walletAddress Must Be Control Address

**The #1 cause of `400 Unauthorized (code 103)` on HL operations is passing the wrong `walletAddress`.**

- During sign-in, the session key is registered against your **control wallet address** (e.g., `0x53D0...2eD`).
- The backend returns a **managed address** (e.g., `0x9967...0f`) that holds the actual funds.
- All HL write operations sign the message as `{action}-{walletAddress}-{data}`, and the backend verifies the signature against the session key registered for that address.
- If you pass the managed address, the signature verification fails → code 103.

```typescript
// ❌ WRONG — causes 400 Unauthorized (code 103)
const creds = { apiKey, walletAddress: managedAddress, sessionPrivateKey };

// ✅ CORRECT — use the control wallet address from sign-in
const creds = { apiKey, walletAddress: controlAddress, sessionPrivateKey };
```

## Related Skills

- **gdex-authentication** — Auth setup required for all HL operations
- **gdex-perp-funding** — Deposit/withdraw USDC to HyperLiquid
- **gdex-portfolio** — View positions and P&L

## Autonomous Agent Notes (Live-Tested)

### Endpoints That Don't Work

| Endpoint | Status | What to Do |
|----------|--------|------------|
| `hlCloseAll` / `/v1/hl/close_all_positions` | Returns TIMEOUT or 400 | Place a reduce-only `hlCreateOrder` for the exact position size |
| `hlUpdateLeverage` / `/v1/hl/update_leverage` | Returns 404 | The backend sets leverage automatically per order. Control effective leverage via position sizing. |
| `getGbotUsdcBalance` | Returns 404 | Use `getHlAccountState()` or clearinghouse state to check balance |

### Close Position Reliably (Live-Tested)

```typescript
// Get current positions
const state = await skill.getHlAccountState({ walletAddress: controlAddress });
const positions = state?.assetPositions || [];

for (const p of positions) {
  const pos = p.position;
  if (Number(pos.szi) !== 0) {
    const markPrice = Number(pos.entryPx); // or fetch via getHlMarkPrice
    await skill.hlCreateOrder({
      coin: pos.coin,
      isLong: Number(pos.szi) < 0,    // opposite direction
      price: '0',                       // market
      size: Math.abs(Number(pos.szi)).toString(),
      reduceOnly: true,
      isMarket: true,
      tpPrice: '0',
      slPrice: '0',
      apiKey,
      walletAddress: controlAddress,   // MUST be control address
      sessionPrivateKey,
    });
  }
}
```

### HL Deposit Minimum

- **Minimum deposit: 10 USDC** (10000000 in smallest unit)
- Managed wallet must hold `amount × 1.01` (1% fee buffer)
- Delivery takes ~10 minutes after Arbitrum tx confirms

### Position Sizing Notes

Since leverage cannot be set via API:
- **Effective leverage** = position notional value / account equity
- To get 5x leverage on $100 account: open a $500 position
- The backend may auto-set leverage to 50x cross — your risk is determined by position size relative to margin

### Critical Checks Before Opening a Position

1. Verify USDC is deposited on HL (use `getHlAccountState()`)
2. Use **control** wallet address (not managed) for all write operations
3. Generate a fresh nonce for every order
4. For market orders: set `price: '0'` and `isMarket: true`
5. `tpPrice` and `slPrice` can be `'0'` to skip TP/SL
