---
name: gdex-copy-trading
description: Copy trade setup — discover top wallets, create/manage copy trades, view transaction history, and browse supported DEXes. Solana only for write operations.
---

# GDEX: Copy Trading

Automatically mirror trades from top-performing Solana wallets. Includes wallet leaderboards, hot token gems, backed by a background process that copies buys/sells in real-time.

## When to Use

- Browsing the top wallet leaderboard (by PnL or net profit)
- Discovering hot new tokens from top wallets
- Creating a copy trade to follow a specific trader
- Updating, toggling, or deleting a copy trade
- Viewing copy trade transaction history with PnL
- Listing supported DEXes for exclusion

## Prerequisites

- `@gdexsdk/gdex-skill` installed
- For discovery: `loginWithApiKey()` only
- For read (list/tx_list): Full sign-in with session key
- For write (create/update): Full sign-in + computedData

## Auth Tiers

| Tier | Endpoints | Auth Needed |
|------|-----------|-------------|
| Discovery | `wallets`, `custom_wallets`, `gems`, `dexes_list`, `top_traders` | API key only |
| Read | `list`, `tx_list` | Session-key auth (`userId` + encrypted `data`) |
| Write | `create`, `update` | computedData (ABI-encode + sign + AES-encrypt) |

> **Write operations are Solana-only.** All create/update calls reject non-Solana chain IDs.

## Discovery Endpoints (No Auth)

### Top Wallets by PnL

```typescript
const wallets = await skill.getCopyTradeWallets();
// Returns 300 wallets sorted by totalPnl, cached 2 minutes
```

### Top Wallets by Net Received

```typescript
const custom = await skill.getCopyTradeCustomWallets();
// Returns 300 wallets sorted by receivedMinusSpent, cached 2 minutes
```

### CopyTradeWallet Response Shape

```typescript
interface CopyTradeWallet {
  _id: string;
  chainId: number;             // 622112261 for Solana
  address: string;             // Solana wallet address
  lastTxTimestamp: number;     // Unix timestamp
  receivedMinusSpent: number;  // Net USD profit
  spent: number;               // Total USD spent
  lastCalculateUnrealizedPnl: number;
  totalPnl: number;            // Total PnL (incl. unrealized)
  unrealizedValue: number;     // Current unrealized USD
  received: number;            // Total USD received
}
```

### Hot Token Gems

```typescript
const gems = await skill.getCopyTradeGems();
// Tokens heavily traded by 3+ hot wallets with >$10 total value
// Cached 20 seconds; may return empty array
```

### Supported DEXes

```typescript
const dexes = await skill.getCopyTradeDexes(622112261); // Solana chain ID
// { success: true, dexes: [{ chainId, dexNumber, dexName, programId }] }
```

Live DEX list (Solana):

| # | DEX | Program ID |
|---|-----|-----------|
| 1 | pumpfun | `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` |
| 2 | pumpswap | `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA` |
| 3 | raydium | `675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8` |
| 4 | raydiumCpmm | `CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C` |
| 5 | meteoraDlmm | `LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo` |

## Read Endpoints (Session-Key Auth)

Require `userId` and `data` (AES-encrypted session key from `buildGdexUserSessionData`).

### List User's Copy Trades

```typescript
import { buildGdexUserSessionData } from '@gdexsdk/gdex-skill';

const data = buildGdexUserSessionData(sessionKey, apiKey);
const list = await skill.getCopyTradeList({ userId, data });
// { isSuccess: true, count: 2, allCopyTrades: [...], dexes: [...] }
```

### CopyTradeConfig Shape

```typescript
interface CopyTradeConfig {
  copyTradeId: string;
  copyTradeName: string;
  buyMode: number;          // 1 = fixed SOL, 2 = % of trader's amount
  chainId: number;
  isActive: boolean;
  userId: string;
  userWallet: string;
  traderWallet: string;
  lossPercent: number;      // stop-loss %
  profitPercent: number;    // take-profit %
  gasPrice: string;
  copyBuyFixedAmount: string;
  copyBuyPercent: number;
  isBuyExistingToken: boolean;
  copySell: boolean;
  excludedProgramIds: string[];
  excludedDexNumbers: number[];
  txCount?: number;
  lastTxTimestamp?: number;
}
```

### Transaction History

```typescript
const txList = await skill.getCopyTradeTxList({ userId, data });
// { isSuccess: true, count: 5, txes: [...] }
```

Each `CopyTradeTx` includes:
- `isBuy`, `priceUsd`, `boughtPrice`, `pnlPercentage`
- `tokenInfo`: `{ address, symbol, name, decimals, dexId, marketCap, logoUrl }`

## Write Endpoints (ComputedData Auth, Solana Only)

### Create a Copy Trade

```typescript
await skill.createCopyTrade({
  apiKey,
  userId,
  sessionPrivateKey,
  chainId: 622112261,
  traderWallet: 'SolanaWalletAddress',
  copyTradeName: 'My Alpha Trader',
  buyMode: 1,               // 1 = fixed SOL amount
  copyBuyAmount: '0.5',     // 0.5 SOL per copied trade
  lossPercent: '50',         // 50% stop-loss
  profitPercent: '100',      // 100% take-profit
  copySell: true,
  isBuyExistingToken: true,
  excludedDexNumbers: [],    // empty = allow all DEXes
});
```

### Update a Copy Trade

```typescript
await skill.updateCopyTrade({
  apiKey,
  userId,
  sessionPrivateKey,
  chainId: 622112261,
  copyTradeId: 'a1b2c3...',
  traderWallet: 'SolanaWalletAddress',
  copyTradeName: 'Updated Name',
  buyMode: 2,                // switch to percentage mode
  copyBuyAmount: '50',       // 50% of trader's amount
  lossPercent: '30',
  profitPercent: '200',
  copySell: true,
});
```

### Delete a Copy Trade (isChangeStatus)

> **⚠️ WARNING: `isChangeStatus` permanently DELETES the trade. It does NOT toggle `isActive`.**

```typescript
await skill.updateCopyTrade({
  ...existingParams,
  isChangeStatus: true,      // WARNING: permanently deletes (same as isDelete)
});
```

### Delete a Copy Trade (isDelete)

```typescript
await skill.updateCopyTrade({
  ...existingParams,
  isDelete: true,
});
```

## Backend Validation Rules

- **Solana only**: chainId must be the Solana chain ID (622112261)
- **Valid wallet**: traderWallet must be a valid Solana address
- **TP/SL**: lossPercent > 0 and < 100, profitPercent > 0
- **buyMode 2**: percentage must be > 0 and <= 100
- **No duplicates**: Can't copy the same wallet+chain+user twice
- **Max limit**: Backend enforces max copy trades per user
- **Circular dependency**: Prevents A→B→C→A copy chains (checked to depth 50)

## How Copies Execute

Trades are NOT executed at API call time. A background process monitors tracked wallets in real-time:
1. Detects trader buy/sell transactions
2. Checks excluded DEXes and deduplication
3. Calculates buy amount (fixed or percentage)
4. Executes the copy trade
5. Places automatic TP/SL orders based on your settings

## Example: Full Copy Trading Flow

```typescript
import {
  GdexSkill,
  buildGdexUserSessionData,
  generateGdexSessionKeyPair,
  buildGdexSignInMessage,
  buildGdexSignInComputedData,
} from '@gdexsdk/gdex-skill';
import { ethers } from 'ethers';

const skill = new GdexSkill();
skill.loginWithApiKey(apiKey);

// 1. Sign in with session key
const wallet = ethers.Wallet.fromPhrase(mnemonic);
const { sessionPrivateKey, sessionKey } = generateGdexSessionKeyPair();
const nonce = String(Date.now());
const msg = buildGdexSignInMessage(wallet.address, nonce, sessionKey);
const sig = await wallet.signMessage(msg);
const payload = buildGdexSignInComputedData({ apiKey, userId: wallet.address, sessionKey, nonce, signature: sig });
await skill.signInWithComputedData({ computedData: payload.computedData, chainId: 1 });
const data = buildGdexUserSessionData(sessionKey, apiKey);
const userId = wallet.address.toLowerCase();

// 2. Browse top wallets
const wallets = await skill.getCopyTradeWallets();
const best = wallets[0];
console.log(`Top wallet: ${best.address}, PnL: $${best.totalPnl.toFixed(2)}`);

// 3. Check DEXes
const { dexes } = await skill.getCopyTradeDexes(622112261);

// 4. Create a copy trade
await skill.createCopyTrade({
  apiKey,
  userId,
  sessionPrivateKey,
  chainId: 622112261,
  traderWallet: best.address,
  copyTradeName: `Top PnL: ${best.address.slice(0, 8)}`,
  buyMode: 1,
  copyBuyAmount: '0.1',
  lossPercent: '50',
  profitPercent: '100',
  copySell: true,
});

// 5. Monitor
const list = await skill.getCopyTradeList({ userId, data });
for (const ct of list.allCopyTrades) {
  console.log(`${ct.copyTradeName}: active=${ct.isActive}, ${ct.txCount ?? 0} trades`);
}
```

## Autonomous Agent Notes (Live-Tested)

1. **All 4 discovery endpoints work with API key only (E2E verified):** `getCopyTradeWallets()`, `getCopyTradeCustomWallets()`, `getCopyTradeGems()`, `getCopyTradeDexes()`.
2. **`getCopyTradeGems()` may return empty array** — this is normal (cached 20 seconds, depends on hot wallet activity).
3. **Sign-in for Solana copy trading must use `chainId: 622112261`** (Solana), not `chainId: 1` (EVM). This is the opposite of HL perp copy trading.
4. **Both `isDelete` and `isChangeStatus` permanently DELETE the copy trade.** There is NO way to pause/toggle — you must delete and recreate.
5. **Boolean fields in ABI use `''` (empty string) for false and `'1'` for true.** The string `'0'` is truthy and WILL trigger deletion.
6. **`copySell: true`** means the copy will also mirror sell transactions, not just buys.

## Related Skills

- **gdex-authentication** — Auth setup and sign-in required for read/write
- **gdex-token-discovery** — Top trader rankings (`getTopTraders`)
- **gdex-portfolio** — Monitor portfolio including copied positions
- **gdex-spot-trading** — Understand the trades being copied
