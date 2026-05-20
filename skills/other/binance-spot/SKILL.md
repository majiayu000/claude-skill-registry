---
name: binance-spot
description: Binance official spot trading skill — place orders, manage accounts, and access real-time market data via Binance Spot API. Sourced from github.com/binance/binance-skills-hub.
metadata: { "cryptoclaw": { "emoji": "🟡", "always": false } }
---

# Binance Spot Trading

Official Binance skill for CEX spot trading. Supports 60+ endpoints for market data, order management, and account operations.

> Source: [binance/binance-skills-hub](https://github.com/binance/binance-skills-hub/tree/main/skills/binance/spot)

## Configuration

Store credentials via SecureVault (recommended) or environment variables:

**Option 1 — SecureVault (TEE-protected when available):**
Use `vault_store_credential` tool with provider "binance", apiKey, and apiSecret.

**Option 2 — Environment variables:**

```
BINANCE_API_KEY=<your_api_key>
BINANCE_API_SECRET=<your_api_secret>
BINANCE_TESTNET=false  # set true for testnet
```

## How to Call Authenticated Endpoints

For all endpoints that require authentication, use the `signed_api_request` tool:

```
signed_api_request({
  provider: "binance",
  method: "POST",
  path: "/api/v3/order",
  params: '{"symbol":"BTCUSDT","side":"BUY","type":"MARKET","quantity":"0.001"}'
})
```

The vault handles HMAC-SHA256 signing, timestamp injection, and API key headers automatically.
You NEVER need to handle API keys or secrets directly.

For public endpoints (no auth required), you may use direct HTTP requests.

**Always require explicit user confirmation before executing mainnet transactions.**

## Base URLs

- Mainnet: `https://api.binance.com`
- Testnet: `https://testnet.binance.vision`

## Market Data (no auth required)

### Exchange Info

```
GET /api/v3/exchangeInfo
GET /api/v3/exchangeInfo?symbol=BTCUSDT
```

### Price Ticker

```
GET /api/v3/ticker/price?symbol=BTCUSDT
GET /api/v3/ticker/24hr?symbol=BTCUSDT
GET /api/v3/ticker/bookTicker?symbol=BTCUSDT
```

### Order Book

```
GET /api/v3/depth?symbol=BTCUSDT&limit=20
```

### Klines / Candlesticks

```
GET /api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100
```

Intervals: `1s`, `1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `6h`, `8h`, `12h`, `1d`, `3d`, `1w`, `1M`

### Recent Trades

```
GET /api/v3/trades?symbol=BTCUSDT&limit=50
GET /api/v3/aggTrades?symbol=BTCUSDT&limit=50
```

### Average Price

```
GET /api/v3/avgPrice?symbol=BTCUSDT
```

## Trading (auth required)

### Place Order

```
POST /api/v3/order
  symbol=BTCUSDT
  side=BUY|SELL
  type=LIMIT|MARKET|STOP_LOSS_LIMIT|TAKE_PROFIT_LIMIT
  quantity=0.001
  price=60000        # required for LIMIT
  timeInForce=GTC    # GTC | IOC | FOK
```

### Test Order (no execution)

```
POST /api/v3/order/test
```

### Cancel Order

```
DELETE /api/v3/order?symbol=BTCUSDT&orderId=12345
DELETE /api/v3/openOrders?symbol=BTCUSDT   # cancel all
```

### Query Order

```
GET /api/v3/order?symbol=BTCUSDT&orderId=12345
GET /api/v3/openOrders?symbol=BTCUSDT
GET /api/v3/allOrders?symbol=BTCUSDT
```

### OCO Orders

```
POST /api/v3/order/oco
POST /api/v3/orderList/oco
DELETE /api/v3/orderList?orderListId=12345
GET /api/v3/orderList?orderListId=12345
GET /api/v3/allOrderList
GET /api/v3/openOrderList
```

## Account (auth required)

### Account Info

```
GET /api/v3/account
```

Returns balances, permissions, commission rates.

### Commission Rates

```
GET /api/v3/account/commission?symbol=BTCUSDT
```

### Trade History

```
GET /api/v3/myTrades?symbol=BTCUSDT
```

### Allocations

```
GET /api/v3/myAllocations?symbol=BTCUSDT
```

## Usage Examples

```
User: What's the current BTC price?
→ GET /api/v3/ticker/price?symbol=BTCUSDT (public, no auth needed)

User: Show my USDT balance
→ signed_api_request(provider:"binance", method:"GET", path:"/api/v3/account")
→ Filter response for USDT

User: Buy 0.001 BTC at market price
→ Confirm with user first
→ signed_api_request(provider:"binance", method:"POST", path:"/api/v3/order",
     params:'{"symbol":"BTCUSDT","side":"BUY","type":"MARKET","quantity":"0.001"}')

User: Place a limit sell for 0.01 ETH at $3500
→ Confirm with user first
→ signed_api_request(provider:"binance", method:"POST", path:"/api/v3/order",
     params:'{"symbol":"ETHUSDT","side":"SELL","type":"LIMIT","quantity":"0.01","price":"3500","timeInForce":"GTC"}')
```

## Safety Rules

- Never execute mainnet orders without explicit user confirmation
- Always show order details before submission
- Display masked credentials only (never full secret key)
- Testnet recommended for testing and development
