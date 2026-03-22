---
name: gdex-portfolio
description: Cross-chain portfolio overview, chain-specific token balances, and paginated trade history
---

# GDEX: Portfolio & Balances

Query cross-chain portfolio summaries, chain-specific balances, and trade history.

## When to Use

- Getting a user's total portfolio value across all chains
- Checking token balances on a specific chain
- Retrieving trade history with pagination and filters

## Prerequisites

- `@gdexsdk/gdex-skill` installed
- Authenticated via `loginWithApiKey()` — see **gdex-authentication**

## Cross-Chain Portfolio

> **WARNING (Live-Tested):** The high-level `getPortfolio()` and `getBalances()` methods send `walletAddress` + `chain` to the backend, but the backend expects `userId` + `chainId` + `data` (encrypted session key). **These methods return empty or incorrect results.** Use the raw client workaround below.

### Correct Way — Raw Client (Live-Tested, Works)

```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY, buildGdexUserSessionData } from '@gdexsdk/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);

// Build encrypted session data
const data = buildGdexUserSessionData(sessionKey, GDEX_API_KEY_PRIMARY);

// Portfolio — use raw client with correct params
const portfolio = await skill.client.get('/v1/portfolio', {
  params: {
    userId: controlAddress,   // control wallet, NOT managed
    chainId: 622112261,       // numeric Solana chain ID
    data,                     // encrypted session key
  }
});
```

### Incorrect Way — High-Level Methods (SDK Bug)

```typescript
// ❌ These send wrong params to backend — DO NOT USE for managed custody
const portfolio = await skill.getPortfolio({ walletAddress: '0x...', chain: 'solana' });
const balances = await skill.getBalances({ walletAddress: '0x...', chain: 8453 });
```

### Portfolio Response

```typescript
interface Portfolio {
  totalValueUsd: number;
  balances: Balance[];
  perpPositions?: PerpPosition[];
  realizedPnl?: number;
  unrealizedPnl?: number;
  totalPnl?: number;
}

interface Balance {
  tokenAddress: string;
  symbol: string;
  name: string;
  decimals: number;
  rawBalance: string;
  balance: string;        // human-readable
  usdValue: number;
  priceUsd: number;
  change24h?: number;
  chain: string | number;
}
```

## Chain-Specific Balances

> **WARNING (Live-Tested):** Same issue as portfolio — use raw client:

```typescript
const balances = await skill.client.get('/v1/balances', {
  params: {
    userId: controlAddress,
    chainId: 622112261,       // numeric chain ID
    data,                     // encrypted session key
  }
});
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `walletAddress` | `string` | Yes | Wallet address to query |
| `chain` | `string \| ChainId` | Yes | Chain to query balances on |
| `tokenAddress` | `string` | No | Filter to a specific token |

## Trade History

> **WARNING (Live-Tested):** The backend expects param `user` (NOT `userId`), and managed Solana chainId for trade history is `900` (NOT `622112261`). Use the raw client:

```typescript
const history = await skill.client.get('/v1/user_trade_history', {
  params: {
    user: controlAddress,     // NOTE: "user", not "userId"
    chainId: 900,             // NOTE: 900 for Solana trade history, not 622112261
    data,                     // encrypted session key
    page: 1,
    limit: 20,
  }
});
```

> The high-level `getTradeHistory()` sends wrong param names. Use raw client above.

### Trade Record

```typescript
interface TradeRecord {
  id: string;
  type: string;        // 'buy' | 'sell'
  inputToken: string;
  outputToken: string;
  amountIn: string;
  amountOut: string;
  usdValue?: number;
  chain: string | number;
  dex?: string;
  txHash: string;
  timestamp: number;
  status: string;
}
```

## Example: Portfolio Dashboard (Autonomous Agent — Live-Tested)

```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY, buildGdexUserSessionData } from '@gdexsdk/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);

// Build encrypted session data (required for all portfolio/balance/history queries)
const data = buildGdexUserSessionData(sessionKey, GDEX_API_KEY_PRIMARY);
const userId = controlAddress; // control wallet, NOT managed

// 1. Get portfolio (raw client — high-level method has wrong params)
const portfolio = await skill.client.get('/v1/portfolio', {
  params: { userId, chainId: 622112261, data }
});

// 2. Get balances
const balances = await skill.client.get('/v1/balances', {
  params: { userId, chainId: 622112261, data }
});

// 3. Get trade history (use "user" param, chainId 900 for Solana)
const history = await skill.client.get('/v1/user_trade_history', {
  params: { user: userId, chainId: 900, data, page: 1, limit: 20 }
});
```

## Autonomous Agent Notes

1. **Always use raw client** for portfolio, balances, and trade history. The high-level SDK methods send incorrect parameter names.
2. **Portfolio/balances chainId**: Use `622112261` for Solana, standard EVM chain IDs for others.
3. **Trade history chainId**: Use `900` for Solana (not `622112261`). This is a backend quirk.
4. **Trade history param**: Use `user` (not `userId`) — backend expects different param name for this endpoint.
5. **Data param**: Always pass the encrypted session key from `buildGdexUserSessionData()`.
6. **userId**: Always use the **control** wallet address, never the managed address.

## Related Skills

- **gdex-authentication** — Auth setup required for portfolio queries
- **gdex-spot-trading** — Execute trades based on portfolio analysis
- **gdex-perp-trading** — View perp positions in portfolio
- **gdex-token-discovery** — Research tokens found in portfolio
