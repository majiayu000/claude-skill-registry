---
name: hyperliquid
description: Trade perpetual futures & spot on Hyperliquid DEX — market data, orders, positions, and vaults.
metadata: { "cryptoclaw": { "emoji": "💎", "always": true } }
---

# Hyperliquid DEX

Trade perpetual futures and spot tokens on Hyperliquid — a high-performance DEX built on its own L1 chain. USDC is the primary collateral for perpetuals; the native token is HYPE.

## Base URLs

**Mainnet:**

```
POST https://api.hyperliquid.xyz/info      # read-only queries
POST https://api.hyperliquid.xyz/exchange   # signed trading actions
WSS  wss://api.hyperliquid.xyz/ws           # real-time subscriptions
```

**Testnet:**

```
POST https://api.hyperliquid-testnet.xyz/info
POST https://api.hyperliquid-testnet.xyz/exchange
WSS  wss://api.hyperliquid-testnet.xyz/ws
```

All requests use `POST` with JSON body `Content-Type: application/json`.

## Info Endpoints (POST /info)

### Perpetual Metadata

```json
{ "type": "meta" }
```

Returns `universe` array (coin name, szDecimals, maxLeverage) and margin tables.

### Metadata + Market Context

```json
{ "type": "metaAndAssetCtxs" }
```

Returns metadata plus per-asset context: mark price, funding rate, open interest, 24h volume.

### All Mid Prices

```json
{ "type": "allMids" }
```

Returns `{ "BTC": "62345.5", "ETH": "3012.1", ... }` — mid prices for every listed asset.

### Order Book (L2)

```json
{ "type": "l2Book", "coin": "BTC", "nSigFigs": 5 }
```

- `nSigFigs`: 2–5, controls price level grouping
- Returns `levels`: `[[{px, sz, n}]]` for bids and asks (up to 20 levels per side)

### Candles (OHLCV)

```json
{
  "type": "candleSnapshot",
  "req": { "coin": "ETH", "interval": "1h", "startTime": 1700000000000, "endTime": 1700100000000 }
}
```

Intervals: `1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `8h`, `12h`, `1d`, `1M`

Returns: `[{ t, T, s, i, o, c, h, l, v, n }]` (open/close/high/low/volume).

### Funding History

```json
{ "type": "fundingHistory", "coin": "BTC", "startTime": 1700000000000 }
```

Returns array of `{ coin, fundingRate, premium, time }`. Max 500 per query; paginate with last `time`.

### User Account State (Perpetuals)

```json
{ "type": "clearinghouseState", "user": "0x..." }
```

Returns: `marginSummary` (accountValue, totalMarginUsed, withdrawable), `assetPositions` array (coin, size, entryPx, unrealizedPnl, leverage, liquidationPx).

### User Open Orders

```json
{ "type": "openOrders", "user": "0x..." }
```

Returns array of `{ coin, side, limitPx, sz, oid, timestamp }`.

### User Fills

```json
{ "type": "userFills", "user": "0x..." }
```

Returns array of `{ coin, px, sz, side, time, fee, oid, crossed }`.

### Order Status

```json
{ "type": "orderStatus", "user": "0x...", "oid": 12345 }
```

Returns order details and current status (open, filled, cancelled).

### Spot Metadata

```json
{ "type": "spotMeta" }
```

Returns `tokens` array and `universe` (trading pairs with index, name, tokens).

### Spot Metadata + Market Context

```json
{ "type": "spotMetaAndAssetCtxs" }
```

Returns spot metadata plus per-pair context: mark price, mid price, 24h volume.

### Spot Balances

```json
{ "type": "spotClearinghouseState", "user": "0x..." }
```

Returns user's spot token balances.

### Vault Details

```json
{ "type": "vaultDetails", "vaultAddress": "0x..." }
```

Returns vault info: leader, followers, portfolio, APR, PnL history.

## Exchange Endpoints (POST /exchange)

All exchange requests require EIP-712 signatures (see Authentication below).

### Place Order

```json
{
  "action": {
    "type": "order",
    "orders": [{
      "a": 0,
      "b": true,
      "p": "62000",
      "s": "0.01",
      "r": false,
      "t": { "limit": { "tif": "Gtc" } }
    }],
    "grouping": "na"
  },
  "nonce": 1700000000000,
  "signature": { ... }
}
```

Fields:

- `a`: asset index (from `meta` universe)
- `b`: `true` = buy/long, `false` = sell/short
- `p`: price (string)
- `s`: size in base asset (string)
- `r`: reduce-only
- `t`: order type — `{ "limit": { "tif": "Gtc" } }`, `{ "limit": { "tif": "Ioc" } }`, or `{ "limit": { "tif": "Alo" } }`

Time-in-force: `Gtc` (Good-til-Cancel), `Ioc` (Immediate-or-Cancel), `Alo` (Add-Liquidity-Only / post-only).

### Cancel Order

```json
{
  "action": {
    "type": "cancel",
    "cancels": [{ "a": 0, "o": 12345 }]
  },
  "nonce": 1700000000000,
  "signature": { ... }
}
```

- `a`: asset index, `o`: order ID

### Modify Order

```json
{
  "action": {
    "type": "batchModify",
    "modifies": [{
      "oid": 12345,
      "order": { "a": 0, "b": true, "p": "63000", "s": "0.01", "r": false, "t": { "limit": { "tif": "Gtc" } } }
    }]
  },
  "nonce": 1700000000000,
  "signature": { ... }
}
```

### TWAP Order

```json
{
  "action": {
    "type": "twapOrder",
    "twap": { "a": 0, "b": true, "s": "1.0", "r": false, "m": 10, "t": true }
  },
  "nonce": 1700000000000,
  "signature": { ... }
}
```

- `m`: duration in minutes, `t`: randomize

### Update Leverage

```json
{
  "action": {
    "type": "updateLeverage",
    "asset": 0,
    "isCross": true,
    "leverage": 10
  },
  "nonce": 1700000000000,
  "signature": { ... }
}
```

### Update Isolated Margin

```json
{
  "action": {
    "type": "updateIsolatedMargin",
    "asset": 0,
    "isBuy": true,
    "ntli": 100
  },
  "nonce": 1700000000000,
  "signature": { ... }
}
```

- `ntli`: signed integer, positive to add margin, negative to remove

### Transfer (Spot <-> Perp)

```json
{
  "action": {
    "type": "usdClassTransfer",
    "amount": "100",
    "toPerp": true
  },
  "nonce": 1700000000000,
  "signature": { ... }
}
```

### Vault Deposit/Withdraw

```json
{
  "action": {
    "type": "vaultTransfer",
    "vaultAddress": "0x...",
    "isDeposit": true,
    "usd": 1000000
  },
  "nonce": 1700000000000,
  "signature": { ... }
}
```

- `usd`: amount in raw units (6 decimals, e.g. `1000000` = 1 USDC)

## WebSocket Subscriptions

Connect to `wss://api.hyperliquid.xyz/ws` and send:

```json
{ "method": "subscribe", "subscription": { "type": "<channel>", ... } }
```

### Channels

| Channel       | Params             | Description                                     |
| ------------- | ------------------ | ----------------------------------------------- |
| `allMids`     | —                  | All mid prices (streaming)                      |
| `trades`      | `coin`             | Real-time trades for a coin                     |
| `l2Book`      | `coin`             | Order book updates                              |
| `candle`      | `coin`, `interval` | Live candle updates                             |
| `userEvents`  | `user`             | Fills, order updates, margin changes for a user |
| `liquidation` | —                  | Real-time liquidation feed                      |

Limits per connection: max 1000 subscriptions, max 2000 messages/min sent.

## Authentication

Exchange endpoints require **EIP-712 typed data signatures**.

- Sign with the wallet private key (or an approved API wallet)
- `nonce`: current timestamp in milliseconds — must be unique and increasing
- `signatureChainId`: `"0x66eee"` for mainnet (chain ID 421614 hex), varies per environment
- Two signing schemes: `sign_l1_action` (for trading) and `sign_user_signed_action` (for agent setup)

**Strongly recommended:** Use the official Python SDK (`hyperliquid-python-sdk`) or a community TypeScript SDK for signing. Manual EIP-712 construction is error-prone.

## Rate Limits

- **Aggregate weight:** 1200 per minute per IP
- Exchange actions: weight = `1 + floor(batch_size / 40)`
- Info requests: weight 2–60 depending on endpoint
- When rate limited: 1 request per 10 seconds until window resets
- **Open order limit:** 1000 base + 1 per 5M USDC cumulative volume (max 5000)

## Asset Reference (Perpetuals)

Common tickers (asset index from `meta` universe):

| Ticker | Description                        |
| ------ | ---------------------------------- |
| BTC    | Bitcoin perpetual                  |
| ETH    | Ethereum perpetual                 |
| SOL    | Solana perpetual                   |
| BNB    | BNB perpetual                      |
| ARB    | Arbitrum perpetual                 |
| DOGE   | Dogecoin perpetual                 |
| AVAX   | Avalanche perpetual                |
| MATIC  | Polygon perpetual                  |
| OP     | Optimism perpetual                 |
| APT    | Aptos perpetual                    |
| SUI    | Sui perpetual                      |
| HYPE   | Hyperliquid native token perpetual |

For the full list and exact asset indices, query `{ "type": "meta" }`.

Spot assets use index `10000 + spotIndex` (from `spotMeta` universe).

## Security Rules

- ALWAYS show order details (side, size, price, leverage, estimated margin) before placing
- ALWAYS confirm with the user before submitting any order or modifying leverage
- NEVER place orders without explicit user approval
- Warn if leverage exceeds 10x or position notional exceeds $10,000
- Warn if the order book is thin (low liquidity at target price)
- For large positions, suggest using TWAP orders to reduce market impact
- Check `clearinghouseState` before orders to verify sufficient margin
- Default to `Gtc` limit orders — avoid `Ioc` market orders unless user explicitly requests
- Always display liquidation price after a position is opened

## Example Interactions

User: "What's the current BTC price on Hyperliquid?"
-> `POST /info` with `{ "type": "allMids" }`, return BTC mid price

User: "Show me ETH order book"
-> `POST /info` with `{ "type": "l2Book", "coin": "ETH", "nSigFigs": 5 }`
-> Display top 5 bid/ask levels with size

User: "Show my open positions"
-> `POST /info` with `{ "type": "clearinghouseState", "user": "<active_wallet>" }`
-> Display positions table: coin, side, size, entry, unrealizedPnl, leverage, liqPx

User: "Long 0.1 BTC at $62,000 with 5x leverage"
-> First set leverage: `updateLeverage` asset=BTC, leverage=5, isCross=true
-> Then place order: buy 0.1 BTC @ $62,000 GTC
-> Show order summary, ask for confirmation, then execute

User: "Cancel all my open orders"
-> Query `openOrders` for user -> batch `cancel` all returned oids

User: "What's the funding rate for ETH?"
-> `POST /info` with `{ "type": "metaAndAssetCtxs" }`, extract ETH funding from asset context

User: "Show me the 4h ETH chart"
-> `POST /info` with `{ "type": "candleSnapshot", "req": { "coin": "ETH", "interval": "4h", ... } }`
-> Summarize recent candles: open, close, high, low, volume trend

User: "Transfer 500 USDC from spot to perp wallet"
-> `POST /exchange` with `usdClassTransfer`, amount="500", toPerp=true

## Usage Notes

- All prices and sizes are strings in API requests/responses
- Pagination: max 500 results per query; use last `time` as `startTime` for next page
- Spot asset index = `10000 + index` from `spotMeta` universe
- Testnet is recommended for development and testing
- Report data source: "Hyperliquid API, fetched just now"
