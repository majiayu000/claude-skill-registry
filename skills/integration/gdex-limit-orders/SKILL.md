---
name: gdex-limit-orders
description: Limit buy, limit sell, update/delete, and list limit orders via managed-custody encrypted payloads
---

# GDEX: Limit Orders

Create limit buy/sell orders that trigger when a token reaches your target price. Uses the same managed-custody encryption flow as spot trades (ABI-encoded → signed → AES-encrypted `computedData`).

## Critical: Endpoint Structure

Limit orders use **separate endpoints for buy vs sell** (NOT a single create endpoint):

| Action | Endpoint | SDK Method |
|--------|----------|------------|
| List orders | `GET /v1/orders` | `getLimitOrders()` |
| Buy when price drops | `POST /v1/limit_buy` | `limitBuy()` |
| Sell when price rises/drops | `POST /v1/limit_sell` | `limitSell()` |
| Update or delete order | `POST /v1/update_order` | `updateOrder()` |

> There is NO `/v1/orders/create` or `/v1/orders/cancel` endpoint.

## When to Use

- Buy a token when its price drops to a target → `limitBuy()`
- Sell a token when its price rises (take-profit) or drops (stop-loss) → `limitSell()`
- Cancel an existing order → `updateOrder({ isDelete: true })`
- Update an order's price/amount → `updateOrder()`
- List all active orders → `getLimitOrders()`

## Prerequisites

- `@gdexsdk/gdex-skill` installed
- Authenticated via `loginWithApiKey()` — see **gdex-authentication**
- Minimum order: `config.chains[chainId].minLimitOrder` (typically 0.01 native token)

## Limit Buy — Buy Token When Price Drops

```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY } from '@gdexsdk/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);

const result = await skill.limitBuy({
  apiKey: GDEX_API_KEY_PRIMARY,
  userId: '0x53D029a671bd1CF61a2fB1F4F6e4bD830BFBb2eD',  // control wallet
  sessionPrivateKey: '<session-private-key-hex>',
  chainId: 622112261,           // Solana
  tokenAddress: 'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm', // WIF
  amount: '10000000',           // 0.01 SOL in lamports
  triggerPrice: '0.50',         // trigger when WIF price ≤ $0.50
  profitPercent: '50',          // take profit at 50% gain (optional)
  lossPercent: '25',            // stop loss at 25% loss (optional)
});
```

### LimitBuyParams

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `apiKey` | `string` | Yes | API key for AES encryption |
| `userId` | `string` | Yes | Control wallet address (NOT managed) |
| `sessionPrivateKey` | `string` | Yes | Session key from sign-in |
| `chainId` | `number` | Yes | Numeric chain ID (e.g. 622112261 for Solana) |
| `tokenAddress` | `string` | Yes | Token to buy |
| `amount` | `string` | Yes | Native token to spend (raw units: wei/lamports) |
| `triggerPrice` | `string` | Yes | USD price to trigger the buy |
| `profitPercent` | `string` | No | Take-profit % above trigger ("0" to skip) |
| `lossPercent` | `string` | No | Stop-loss % below trigger ("0" to skip) |

**ABI schema:** `['string','string','string','uint256','uint256','string']` = `[tokenAddress, amount, triggerPrice, profitPercent, lossPercent, nonce]`
**Signature:** `limit_buy-{userId}-{data}`

> **CRITICAL (Live-Tested):** `profitPercent` and `lossPercent` MUST be ABI-encoded as `uint256`, NOT `string`. The backend decodes them as uint256 and validates `0-100` range. Using `string` type produces ABI byte-offsets (e.g. 192) that fail the range check with `"lossPercent must be between 0 and 100"`. The SDK handles this correctly — only matters if encoding manually.

## Limit Sell — Sell Token at Target Price

```typescript
// Sell WIF when price reaches $999.99 (take-profit)
const result = await skill.limitSell({
  apiKey: GDEX_API_KEY_PRIMARY,
  userId: '0x53D029a671bd1CF61a2fB1F4F6e4bD830BFBb2eD',
  sessionPrivateKey: '<session-private-key-hex>',
  chainId: 622112261,
  tokenAddress: 'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm', // WIF
  amount: '100000',             // token amount in raw units
  triggerPrice: '999.99',       // trigger when WIF price reaches $999.99
});
```

### LimitSellParams

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `apiKey` | `string` | Yes | API key for AES encryption |
| `userId` | `string` | Yes | Control wallet address |
| `sessionPrivateKey` | `string` | Yes | Session key from sign-in |
| `chainId` | `number` | Yes | Numeric chain ID |
| `tokenAddress` | `string` | Yes | Token to sell |
| `amount` | `string` | Yes | Token amount to sell (raw units) |
| `triggerPrice` | `string` | Yes | USD price to trigger the sell |

**ABI schema:** `['string','string','string','string']` = `[tokenAddress, amount, triggerPrice, nonce]`
**Signature:** `limit_sell-{userId}-{data}`

> The backend auto-classifies as take-profit (trigger > current price) or stop-loss (trigger < current price).

## Update or Delete an Order

```typescript
// Delete an order
await skill.updateOrder({
  apiKey: GDEX_API_KEY_PRIMARY,
  userId: '0x53D029a671bd1CF61a2fB1F4F6e4bD830BFBb2eD',
  sessionPrivateKey: '<session-private-key-hex>',
  chainId: 622112261,
  orderId: '64-char-hex-order-id',
  isDelete: true,
});

// Update an order's trigger price
await skill.updateOrder({
  apiKey: GDEX_API_KEY_PRIMARY,
  userId: '0x53D029a671bd1CF61a2fB1F4F6e4bD830BFBb2eD',
  sessionPrivateKey: '<session-private-key-hex>',
  chainId: 622112261,
  orderId: '64-char-hex-order-id',
  triggerPrice: '1.50',
  amount: '10000000',
});
```

### UpdateOrderParams

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `apiKey` | `string` | Yes | API key for AES encryption |
| `userId` | `string` | Yes | Control wallet address |
| `sessionPrivateKey` | `string` | Yes | Session key from sign-in |
| `chainId` | `number` | Yes | Numeric chain ID |
| `orderId` | `string` | Yes | Order ID from getLimitOrders() |
| `amount` | `string` | No | New amount (raw units) |
| `triggerPrice` | `string` | No | New trigger price (USD) |
| `profitPercent` | `string` | No | New take-profit % (buy orders) |
| `lossPercent` | `string` | No | New stop-loss % (buy orders) |
| `isDelete` | `boolean` | No | Set true to cancel/delete the order |

**ABI schema:** `['string','string','string','uint256','uint256','string','string']` = `[orderId, amount, triggerPrice, profitPercent, lossPercent, nonce, isDelete]`
**Signature:** `update_order-{userId}-{data}`

> **CRITICAL:** Same as `limit_buy` — `profitPercent` and `lossPercent` are `uint256`, not `string`.

## List Orders

```typescript
const { count, orders } = await skill.getLimitOrders({
  userId: '0x53D029a671bd1CF61a2fB1F4F6e4bD830BFBb2eD',
  data: encryptedSessionKey,  // from buildGdexUserSessionData()
  chainId: 622112261,
});
```

### GetLimitOrdersParams

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `userId` | `string` | Yes | Control wallet address |
| `data` | `string` | Yes | Encrypted session key (from `buildGdexUserSessionData`) |
| `chainId` | `number` | Yes | Numeric chain ID |

### LimitOrder Object (response)

```typescript
interface LimitOrder {
  orderId: string;           // unique 64-char hex ID
  fromToken: string;         // token being sold
  toToken: string;           // token being bought
  isBuyLimit: boolean;       // true = buy limit, false = sell limit
  price: number;             // trigger price in USD
  takeProfitPrice: number;   // TP price (0 = disabled)
  stopLossPrice: number;     // SL price (0 = disabled)
  fromTokenAmount: string;   // amount in raw units
  toTokenAmount: string;     // computed output amount
  walletAddress: string;     // managed wallet address
  userId: string;            // control wallet address
  chainId: number;           // numeric chain ID
  pairAddress: string;       // DEX pair address
  isActive: boolean;         // still pending?
  isCancelled?: boolean;     // was cancelled?
  expiredAt: number;         // expiry Unix timestamp
  profitPercent?: string;    // TP % (buy orders)
  lossPercent?: string;      // SL % (buy orders)
}
```

## Order Fill Logic

Orders are filled by background processes that monitor prices via NATS:
- **Buy limit:** triggers when `tokenPrice <= order.price`
- **Sell take-profit:** triggers when `tokenPrice >= takeProfitPrice`
- **Sell stop-loss:** triggers when `tokenPrice <= stopLossPrice`

## Error Codes

| Code | Meaning |
|------|---------|
| 101 | Missing required parameters |
| 102 | Invalid nonce or params |
| 103 | Unauthorized (wrong userId or session key) |
| 1011 | Invalid/expired order |
| 1012 | Order expired |
| 1031 | Unsupported token |
| 400 | Insufficient balance (need ≥ minLimitOrder in native token) |

## Legacy Aliases

For backward compatibility, older method names still work:
- `createLimitOrder()` → calls `limitBuy()`
- `cancelLimitOrder()` → calls `updateOrder({ isDelete: true })`

## Autonomous Agent Notes (Live-Tested)

### Verified Working Flow (Solana/WIF Example)

This exact sequence was tested end-to-end and succeeded:

```typescript
// 1. List existing orders
const orders = await skill.getLimitOrders({ userId, data, chainId: 622112261 });

// 2. Create a limit buy order
const result = await skill.limitBuy({
  apiKey: GDEX_API_KEY_PRIMARY,
  userId: controlAddress,          // MUST be control address, lowercase
  sessionPrivateKey,
  chainId: 622112261,              // Solana
  tokenAddress: 'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm', // WIF
  amount: '1000000',               // ~0.001 SOL in lamports (raw units)
  triggerPrice: '0.0001',          // trigger when price drops to $0.0001
  profitPercent: '50',             // 50% take-profit
  lossPercent: '30',               // 30% stop-loss
});
// → { isSuccess: true, message: "Order created successfully", order: {...} }

// 3. Verify order appears in list
const updated = await skill.getLimitOrders({ userId, data, chainId: 622112261 });

// 4. Cancel the order
await skill.updateOrder({
  apiKey, userId, sessionPrivateKey,
  chainId: 622112261,
  orderId: result.order.orderId,
  isDelete: true,
});
```

### Key Requirements for Limit Buy

- `amount` must be in **raw units** (lamports for Solana, wei for EVM) — NOT float
- `profitPercent` and `lossPercent` are **mandatory** for `limit_buy` (both must be > 0)
- `profitPercent` and `lossPercent` must be valid 0-100 range (ABI-encoded as `uint256`)
- `userId` must be the **control** wallet address, **lowercase**
- `triggerPrice` is in USD (string)

### Minimum Order Size

The backend enforces `config.chains[chainId].minLimitOrder` per chain. For Solana, this is approximately 0.001 SOL (1000000 lamports). Going below returns "Insufficient balance".

### Order Cancellation

To cancel, use `updateOrder({ isDelete: true })`. There is no separate cancel endpoint. The `cancelLimitOrder()` alias calls this internally.

### Error Messages and What They Mean

| Error | Cause | Fix |
|-------|-------|-----|
| `lossPercent must be between 0 and 100` | ABI encoding used `string` type instead of `uint256` | SDK handles this correctly; only matters for manual encoding |
| `Insufficient balance` | Amount too small or managed wallet underfunded | Increase amount or fund the managed Solana wallet |
| `Order not found` (on update/delete) | Wrong `orderId` or order already filled/expired | Refresh order list with `getLimitOrders()` first |
| `Invalid nonce` | Reused or stale nonce | Generate fresh: `String(Date.now())` |

## Related Skills

- **gdex-authentication** — Auth setup required before creating orders
- **gdex-spot-trading** — Market orders (immediate execution) instead of limits
- **gdex-portfolio** — Track order fills in trade history
