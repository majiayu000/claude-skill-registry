---
name: gdex-token-discovery
description: Token details, trending tokens, OHLCV candlestick data, and top traders — requires API key auth (Bearer token)
---

# GDEX: Token Discovery

Research tokens with price data, market metrics, trending rankings, candlestick charts, and top trader leaderboards.

> **Auth required:** All token discovery endpoints (except `/v1/token_details`) return 403 "Access denied: Invalid client" without a Bearer token. Always call `loginWithApiKey()` first.

## When to Use

- Looking up token price, market cap, volume, liquidity, and socials
- Finding trending tokens on a specific chain
- Getting OHLCV candlestick data for charting or analysis
- Researching a token before buying (DEX info, security audit, holder count)
- Finding top-performing trader wallets

## Prerequisites

```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY } from '@gdexsdk/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);
```

## Token Details

```typescript
const token = await skill.getTokenDetails({
  tokenAddress: 'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm',
  chain: 622112261,  // Solana
});

console.log(token.symbol);        // "$WIF"
console.log(token.priceUsd);      // 0.176
console.log(token.marketCap);     // 176054268
console.log(token.liquidityUsd);  // 4574052
console.log(token.dexId);         // "raydium"
console.log(token.isRaydium);     // true
console.log(token.priceChanges);  // { m5: 0, h1: -0.2, h6: -2.2, h24: -1.3 }
console.log(token.volumes);       // { m5: 482, h1: 15438, h6: 74105, h24: 316704 }
console.log(token.securities?.holderCount);  // 201554
```

### TokenDetails (response)

```typescript
interface TokenDetails {
  address: string;           // token contract address
  chainId: number;           // numeric chain ID
  symbol: string;            // may include $ prefix (e.g. "$WIF")
  name: string;              // full name
  decimals: number;
  priceUsd?: number;         // current USD price
  priceNative?: number;      // price in native token (SOL/ETH)
  marketCap?: number;        // market cap in USD
  liquidityUsd?: number;     // liquidity in USD
  liquidityEth?: number;     // liquidity in native token
  totalSupply?: string;      // raw units
  pairAddress?: string;      // DEX pair address
  dexId?: string;            // primary DEX (e.g. "raydium")
  dexes?: string[];          // all DEXes
  isRaydium?: boolean;
  isMeteora?: boolean;
  isPumpfun?: boolean;
  isPumpSwap?: boolean;
  priceChanges?: {           // price changes by period
    m5?: number; h1?: number; h6?: number; h24?: number;
  };
  volumes?: {                // volume by period
    m5?: number; h1?: number; h6?: number; h24?: number;
  };
  socialInfo?: {
    telegramUrl?: string; twitterUrl?: string;
    websiteUrl?: string; logoUrl?: string;
  };
  securities?: {             // security audit
    mintAbility?: boolean; freezeAbility?: boolean;
    lpLockPercentage?: number; holderCount?: number;
    topHoldersPercentage?: number;
  };
  createdTime?: number;      // creation timestamp (Unix ms)
}
```

## Trending Tokens

```typescript
const trending = await skill.getTrendingTokens({
  chain: 622112261,   // Solana (chainId)
  period: '24h',      // '1h' | '6h' | '24h' | '7d'
  limit: 5,
});

trending.forEach(t => {
  console.log(`${t.symbol}: $${t.priceUsd} mcap=$${t.marketCap} liq=$${t.liquidityUsd}`);
});
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | `SupportedChain` | No | Chain to filter by (numeric chainId) |
| `period` | `string` | No | `'1h'`, `'6h'`, `'24h'`, `'7d'` (default: `'24h'`) |
| `limit` | `number` | No | Max results (default: 20) |
| `minLiquidity` | `number` | No | Minimum liquidity in USD |
| `minVolume` | `number` | No | Minimum 24h volume in USD |

> Trending tokens have the **same shape as TokenDetails** — same fields from the tokens collection.

## OHLCV Candlestick Data

```typescript
const ohlcv = await skill.getOHLCV({
  tokenAddress: 'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm',
  chain: 622112261,
  resolution: '60',   // 1-hour candles
  from: Math.floor(Date.now() / 1000) - 86400,  // 24h ago
  to: Math.floor(Date.now() / 1000),
});

console.log('Candles:', ohlcv.candles.length);
ohlcv.candles.forEach(c => {
  console.log(`[${new Date(c.time * 1000).toISOString()}] O=${c.open} H=${c.high} L=${c.low} C=${c.close}`);
});
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tokenAddress` | `string` | Yes | Token contract address |
| `chain` | `SupportedChain` | Yes | Chain (numeric chainId) |
| `resolution` | `string` | Yes | `'1'`, `'5'`, `'15'`, `'30'`, `'60'`, `'240'`, `'D'`, `'W'` |
| `from` | `number` | No | Start timestamp (Unix seconds) |
| `to` | `number` | No | End timestamp (Unix seconds) |
| `limit` | `number` | No | Number of candles |

> **Note:** The backend candle data may not be populated for all tokens. If `candles` is empty, the data isn't available yet — not an SDK error.

## Top Traders

```typescript
const traders = await skill.getTopTraders({
  chain: 622112261,  // Solana
  period: '7d',
  limit: 5,
});

traders.forEach((t, i) => {
  console.log(`#${i + 1}: ${t.wallet_address} PnL(7d)=$${t.realized_profit_7d} name=${t.name || '?'}`);
});
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | `SupportedChain` | No | Chain filter |
| `period` | `string` | No | `'1d'`, `'7d'`, `'30d'`, `'all'` (default: `'7d'`) |
| `limit` | `number` | No | Max results (default: 10) |
| `sortBy` | `string` | No | `'pnl'`, `'winRate'`, `'volume'`, `'tradeCount'` |

### TopTrader (response)

```typescript
interface TopTrader {
  wallet_address: string;     // wallet address
  address: string;            // same as wallet_address
  name?: string;              // display name
  twitter_username?: string;
  twitter_name?: string;
  avatar?: string;
  tags?: string[];            // e.g. ["app_smart_money", "kol"]
  realized_profit_1d?: number;
  realized_profit_7d?: number;
  realized_profit_30d?: number;
  pnl_1d?: number;           // PnL ratio (1d)
  pnl_7d?: number;
  pnl_30d?: number;
  buy?: number;               // recent buy count
  sell?: number;
  last_active?: number;       // Unix timestamp
}
```

## Example: Token Research Before Buying

```typescript
const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);

// 1. Find trending tokens on Solana
const trending = await skill.getTrendingTokens({
  chain: 622112261,
  period: '1h',
  limit: 5,
});

// 2. Get details on the top trending token
const top = trending[0];
const details = await skill.getTokenDetails({
  tokenAddress: top.address,
  chain: 622112261,
});

console.log(`${details.symbol}: $${details.priceUsd}`);
console.log(`Market Cap: $${details.marketCap}`);
console.log(`Liquidity: $${details.liquidityUsd}`);
console.log(`Holders: ${details.securities?.holderCount}`);
console.log(`DEX: ${details.dexId} (Raydium: ${details.isRaydium})`);

// 3. Check who the top traders are
const traders = await skill.getTopTraders({ chain: 622112261, period: '7d', limit: 3 });
traders.forEach(t => console.log(`  ${t.name || t.wallet_address}: $${t.realized_profit_7d} PnL`));
```

## Autonomous Agent Notes (Live-Tested)

### Chain Parameter Must Be Numeric

All token discovery endpoints (`getOHLCV`, `getTopTraders`, `getTrendingTokens`, `getTokenDetails`) require **numeric** `chainId`, not string `chain`. Use `622112261` for Solana, `8453` for Base, etc.

```typescript
// ✅ Correct
await skill.getOHLCV({ tokenAddress, chain: 622112261, resolution: '60', from, to });
await skill.getTopTraders({ chain: 622112261, period: '7d', limit: 5 });

// ❌ Wrong — string chain names may not work for all endpoints
await skill.getOHLCV({ tokenAddress, chain: 'solana', resolution: '60', from, to });
```

### OHLCV Data May Be Empty

Not all tokens have OHLCV data populated. If `candles` is an empty array, the data isn't available yet — this is not an SDK error. Try a different token or wider time range.

### Token Safety Checks Before Buying

Before buying a token autonomously, check:
1. **`dexId`**: Must be `'raydium'` on Solana (Meteora fails — see gdex-spot-trading)
2. **`liquidityUsd`**: Should be > $1000 to avoid slippage problems
3. **`securities.mintAbility`**: If `true`, the token can be infinitely minted (rug risk)
4. **`securities.freezeAbility`**: If `true`, your tokens can be frozen
5. **`securities.lpLockPercentage`**: Higher is safer (100% = fully locked LP)
6. **`marketCap`**: Sanity check — very low mcap tokens are extremely volatile

### Auth Required

All token discovery endpoints return `403 "Access denied: Invalid client"` without a Bearer token. Always call `loginWithApiKey()` first — even for read-only data.

## Related Skills

- **gdex-spot-trading** — Buy/sell tokens after researching them
- **gdex-portfolio** — Check if you already hold a token
- **gdex-authentication** — Required for all token discovery endpoints
