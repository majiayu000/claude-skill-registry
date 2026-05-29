---
name: gdex-spot-trading
description: Buy and sell tokens on Solana, Sui, and EVM chains with automatic DEX routing, slippage control, and percentage-based sells
---

# GDEX: Spot Trading

Buy and sell tokens across Solana, Sui, and 12+ EVM chains. The SDK routes through the best available DEX automatically, or you can specify one.

## When to Use

- Buying a token with native currency (SOL, ETH, etc.)
- Selling a token (absolute amount or percentage of holdings)
- Executing managed-custody spot trades with encrypted payloads

## Prerequisites

- `@gdexsdk/gdex-skill` installed
- Authenticated via `loginWithApiKey()` or managed-custody sign-in
- See **gdex-authentication** for auth setup

## Buy a Token

```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY } from '@gdexsdk/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);

const trade = await skill.buyToken({
  chain: 'solana',                                        // chain name or ChainId number
  tokenAddress: 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v', // USDC on Solana
  amount: '0.1',                                          // 0.1 SOL (native token input)
  slippage: 1,                                            // 1% max slippage (optional, default: 1)
  dex: 'raydium',                                         // optional: prefer a specific DEX
});
// Returns: { jobId, status, inputAmount, outputAmount, txHash?, error? }
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | `string \| ChainId` | Yes | `'solana'`, `'sui'`, or ChainId number (1=Ethereum, 8453=Base, 42161=Arbitrum, 56=BSC, **622112261=Solana**) |

> **Critical:** The Solana numeric chainId is `622112261` (`ChainId.SOLANA`), NOT `900`. Using `900` returns the EVM managed address with `balance: null`. The `/v1/user` endpoint returns a different managed wallet per chainId (e.g. `CFSi4Y...` for Solana, `0x9967...` for EVM). |
| `tokenAddress` | `string` | Yes | Contract address of the token to buy |
| `amount` | `string` | Yes | Amount of native token to spend (e.g., `'0.1'` for 0.1 SOL) |
| `slippage` | `number` | No | Max slippage % (default: 1) |
| `dex` | `string` | No | Force specific DEX: `'raydium'`, `'orca'`, `'uniswap-v3'`, `'cetus'`, etc. |
| `walletAddress` | `string` | No | Override wallet address |
| `priorityFee` | `number` | No | Solana priority fee in lamports |

## Sell a Token

```typescript
// Sell absolute amount
const trade = await skill.sellToken({
  chain: 8453,                                            // Base
  tokenAddress: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913', // USDC on Base
  amount: '100',                                          // sell 100 tokens
  slippage: 0.5,
});

// Sell percentage of holdings
const trade = await skill.sellToken({
  chain: 'solana',
  tokenAddress: 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263', // BONK
  amount: '50%',                                          // sell 50% of holdings
});
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | `string \| ChainId` | Yes | Chain identifier |
| `tokenAddress` | `string` | Yes | Token contract address |
| `amount` | `string` | Yes | Absolute amount (`'100'`) or percentage (`'50%'`) |
| `slippage` | `number` | No | Max slippage % (default: 1) |
| `walletAddress` | `string` | No | Override wallet address |

## Managed-Custody Trade Submission

For full managed-custody trading with encrypted payloads:

```typescript
import {
  GdexSkill,
  GDEX_API_KEY_PRIMARY,
  buildGdexManagedTradeComputedData,
} from '@gdexsdk/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);

// Build encrypted trade payload (requires session key from sign-in)
const trade = buildGdexManagedTradeComputedData({
  apiKey: GDEX_API_KEY_PRIMARY,
  action: 'purchase',  // or 'sell'
  userId: '0xYourAddress',
  tokenAddress: 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263',
  amount: '100000',     // in smallest unit
  nonce: String(Math.floor(Date.now() / 1000) + Math.floor(Math.random() * 1000)),
  sessionPrivateKey,    // from generateGdexSessionKeyPair()
});

const result = await skill.submitManagedPurchase({
  computedData: trade.computedData,
  chainId: 622112261,   // 622112261=Solana (ChainId.SOLANA), NOT 900
  slippage: 15,          // 10-15% recommended for Solana
});
```

### Solana-Specific Notes (Live-Tested)

- **Raydium-routed tokens work; Meteora tokens fail.** The backend has a bug where Meteora DLMM swaps don't wrap SOL into WSOL before swapping. Check `token.dexId` — if `"meteora"`, the swap will fail with `Program error: 1`. Tokens with `dexId: "raydium"` work correctly.
- **Minimum ~0.01 SOL balance needed.** Each new token ATA costs ~0.002 SOL rent + priority fee (0.0005 default) + base tx fee. The first trade on a token needs significantly more SOL than just the swap amount.
- **Amount is in lamports** (1 SOL = 1,000,000,000 lamports). Pass as a string, e.g. `'5000000'` for 0.005 SOL.
- **Use `chainId: 622112261`**, not `900`. Using `900` will submit the trade to the wrong chain context.
```
```

## Trade Status Polling

```typescript
if (result.requestId) {
  const status = await skill.getManagedTradeStatus(result.requestId);
  console.log('Status:', status.status, 'Hash:', status.hash);
}
```

**Status values:**
- `'queued'` — submitted to queue
- `'pending'` — being processed
- `'completed'` — executed on-chain
- `'failed'` — failed (check `error` field)

## Supported Chains × DEXes

| Chain | Available DEXes |
|-------|-----------------|
| Solana | Raydium, Raydium v2, Orca |
| Sui | Cetus, Bluefin |
| Ethereum | Uniswap v2, Uniswap v3, Odos |
| Base | Uniswap v3, Odos, Arcadia |
| Arbitrum | Uniswap v3, Odos |
| BSC | PancakeSwap, Odos |
| Optimism | Uniswap v3, Odos |
| Fraxtal | Uniswap v3 |

## Error Handling

```typescript
import { GdexValidationError, GdexApiError, GdexRateLimitError } from '@gdexsdk/gdex-skill';

try {
  await skill.buyToken({ chain: 'solana', tokenAddress: '...', amount: '0.1' });
} catch (err) {
  if (err instanceof GdexRateLimitError) {
    await delay(err.retryAfter * 1000);  // wait and retry
  } else if (err instanceof GdexValidationError) {
    console.error('Invalid param:', err.message);
  } else if (err instanceof GdexApiError) {
    console.error('API error:', err.status, err.message);
  }
}
```

## Notes

- All amounts are strings to preserve precision (e.g., `'0.1'`, `'1000'`)
- Chain can be string (`'solana'`) or ChainId number (`622112261`)
- The SDK retries on transient errors (429, 503) with exponential backoff
- If no `dex` specified, the backend selects the best route automatically

## Autonomous Agent Notes (Live-Tested)

### Managed-Custody Trades Require Raw Units

For `buildGdexManagedTradeComputedData()` + `submitManagedPurchase()` / `submitManagedSell()`, the `amount` must be in **raw units** (lamports for Solana, wei for EVM), NOT human-readable:

```typescript
// ❌ WRONG: amount: '0.01' (this is a float, not raw units)
// ✅ CORRECT: amount: '10000000' (0.01 SOL = 10,000,000 lamports)
// ✅ CORRECT: amount: '10000000000000000' (0.01 ETH = 10^16 wei)
```

### Raydium vs Meteora on Solana

- **Raydium-routed tokens work correctly** (WIF, most liquid tokens)
- **Meteora DLMM tokens fail** with `Program error: 1` (backend bug — doesn't wrap SOL into WSOL)
- **Check before buying:** `token.dexId === 'raydium'` ✅ / `token.dexId === 'meteora'` ❌
- If you get `Program error: 1`, the token is Meteora-routed — don't retry, pick a different token

### Minimum SOL Balance

Keep at least **0.01 SOL** in the managed Solana wallet. First trade on a new token costs ~0.007 SOL overhead (ATA creation + priority fee + base tx fee) on top of the trade amount.

### Trade Status Polling

After a managed trade returns a `requestId`, poll until `status === 'completed'`:
```typescript
if (result.requestId) {
  let status;
  do {
    await new Promise(r => setTimeout(r, 3000)); // wait 3s between polls
    status = await skill.getManagedTradeStatus(result.requestId);
  } while (status.status === 'queued' || status.status === 'pending');
  console.log('Final:', status.status, status.hash);
}
```

### Sell by Percentage

To sell a portion of holdings, use `amount: '50%'` (string with % sign). The backend calculates the exact token amount.

## Related Skills

- **gdex-authentication** — Auth setup required before trading
- **gdex-portfolio** — Check balances and trade history after trading
- **gdex-token-discovery** — Research tokens before buying (no auth needed)
- **gdex-limit-orders** — Set limit orders instead of market buys/sells
