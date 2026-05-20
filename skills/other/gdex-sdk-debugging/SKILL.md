---
name: gdex-sdk-debugging
description: Troubleshoot GDEX SDK errors — error codes, encryption debugging, chain-specific quirks, HL gotchas, and copy trade pitfalls
---

# GDEX: SDK Debugging & Troubleshooting

Comprehensive troubleshooting guide for GDEX SDK errors, covering API error codes, encryption debugging, chain-specific quirks, HyperLiquid gotchas, and copy trade pitfalls. All issues documented from live E2E testing.

## When to Use

- Getting unexpected API errors (103, 102, TIMEOUT)
- Trades failing silently or returning wrong data
- Debugging encryption / `computedData` payload issues
- Chain-specific problems (wrong chainId, wrong managed wallet)
- HyperLiquid perp issues
- Copy trade configuration problems

## API Error Codes

| Code | Error | Common Cause | Fix |
|------|-------|-------------|-----|
| `103` | Unauthorized | Wrong `walletAddress` (using managed instead of control), wrong ABI type, signing with wrong key | Use **control wallet address** as `walletAddress` / `userId`. Verify session key matches sign-in. |
| `102` | Invalid chainId | Using wrong chainId for HL operations | HL operations require `chainId: 42161` (Arbitrum). Copy trades need specific chainIds (see below). |
| `102` | Invalid params | Reused nonce, unsupported token, or malformed ABI payload | Check nonce is fresh (`Date.now()`). Verify token is supported on chain. |
| `400` | Bad Request | Missing required fields or wrong field types | Check all required params are present and correctly typed. |
| `TIMEOUT` | Request timeout | Backend processing delay (common with `hlCloseAll`) | Retry once, or use alternative approach (reduce-only order to close). |
| `JSON parse error` | Invalid response | Backend returned non-JSON (HTML error page, Cloudflare block) | Check User-Agent header is set. Verify API key is valid. |

## Critical: Control Wallet vs Managed Wallet

This is the **#1 source of errors**:

```
Control wallet:  0x53D029a671bd1CF61a2fB1F4F6e4bD830BFBb2eD  ← used for API calls (userId, walletAddress)
Managed wallet:  0x9967179de55bd67e6b90fcc4f908556d93938c0f  ← server-side, executes trades on-chain
```

**Rule:** All API calls use the **control address** — the one you signed in with. The managed address is only used when querying on-chain state directly (e.g., `user_stats` on HL needs the managed address).

> The `/v1/user` endpoint returns a **different managed wallet per chainId**:
> - `chainId=1` → EVM managed: `0x9967...`
> - `chainId=622112261` → Solana managed: `CFSi4Y...` (base58)

## Chain ID Gotchas

| Issue | Wrong | Correct | Notes |
|-------|-------|---------|-------|
| Solana chain ID | `900` | `622112261` (`ChainId.SOLANA`) | `900` returns EVM managed address with `balance: null` |
| Copy trade sign-in | `chainId: 1` | `chainId: 622112261` | Solana copy trades need Solana chainId for sign-in |
| Perp copy trade sign-in | `chainId: 622112261` | `chainId: 1` | HL perp copy trades need EVM chainId for sign-in |
| HL operations | Any other | `42161` (Arbitrum) | HL deposit, create order, close — all use Arbitrum chainId |

## HyperLiquid-Specific Issues

### `hlCloseAll` is Unreliable

The `/v1/hl/close_all_positions` endpoint frequently returns `TIMEOUT` or JSON parse errors.

**Workaround:** Place a reduce-only order for the exact position size:
```typescript
// Instead of skill.hlCloseAll() — use this:
const positions = await skill.hlGetPositions();
for (const pos of positions) {
  if (Number(pos.szi) !== 0) {
    await skill.closePerpPosition({
      coin: pos.coin,
      closePercent: 100,  // close full position
    });
  }
}
```

### Leverage Cannot Be Set via API

The `hlUpdateLeverage` / `/v1/hl/update_leverage` endpoint returns **404** — it's not implemented. The backend sets leverage automatically before each trade.

**Implication:** You control effective leverage through position sizing relative to your account balance.

### HL Signature Format

```
message = "{action}-{userId.toLowerCase()}-{dataHex}"
digest  = keccak256(utf8Bytes(message))
output  = r(64hex) + s(64hex) + v(2hex)  // 130 chars total, v=00/01, no 0x prefix
```

Common signature errors:
- Wrong `userId` (must be control wallet, lowercase)
- Wrong `action` string (e.g., `"hl_deposit"` not `"deposit"`)
- Leading `0x` on signature output (must be stripped)
- Wrong `v` value (must be `00` or `01`, not `27`/`28`)

## Encryption Debugging

All managed-custody trades use AES-256-CBC encrypted `computedData`:

```
1. ABI-encode trade parameters → hex string (no 0x prefix)
2. Sign: keccak256(action + userId + dataHex) → r+s+v (130 chars)
3. Encrypt: AES-256-CBC(dataHex + signature, derivedKey, iv)
4. POST to backend with { computedData, userId, chainId }
```

### Common Encryption Errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| `103 Unauthorized` | ABI using `uint256` when backend expects `uint64`, or vice versa | Check the exact ABI types for each endpoint — HL deposit uses `uint64`, not `uint256` |
| `Invalid signature` | Signing with wrong key or wrong message format | Ensure session key (not control wallet key) signs the message. Check action string exactly matches. |
| Empty response | `computedData` encrypted with wrong key | Verify AES key derivation: `SHA256(SHA256(SHA256(apiKey)))` |
| `Reused nonce` | Same nonce value in consecutive trades | Always use fresh `Date.now()` or incrementing nonce |

### AES Key Derivation

```typescript
const key = SHA256(SHA256(SHA256(apiKey)));  // 3× SHA256 hash chain
const iv = randomBytes(16);                  // fresh IV per request
const encrypted = AES_CBC_encrypt(payload, key, iv);
// computedData = iv.hex + encrypted.hex (concatenated)
```

## Solana-Specific Issues

### Meteora Swaps Are Broken

Tokens routed through Meteora DLMM (e.g., BONK) fail with `Program error: 1` because the backend doesn't wrap SOL into WSOL.

**Workaround:** Use Raydium-routed tokens. Check `token.dexId`:
- `"raydium"` / `"raydium_v2"` → works
- `"meteora"` → **will fail**
- `"orca"` → works

### ATA Creation Costs

First trade on a new Solana token incurs ~0.007 SOL overhead:
- ATA creation: ~0.002 SOL
- Priority fee: ~0.0005 SOL (default)
- Keep at least 0.01 SOL in the managed wallet for safety

### Solana Managed Wallet

After sign-in with `chainId: 622112261`, the Solana managed wallet is a **base58 address** (not hex):
```
CFSi4YimeCbfSNqH2WmHwJKwj1YYG1cWBtQyVPB4sCe1
```

## Copy Trade Pitfalls

### `isDelete` and `isChangeStatus` Both Delete

On **both Solana and HyperLiquid**, setting either `isDelete='1'` or `isChangeStatus='1'` **permanently deletes** the copy trade. There is no "pause" or "toggle" — it's irreversible.

> **Boolean encoding:** Use `''` (empty string) for false and `'1'` for true. The string `'0'` is **truthy** and will trigger deletion.

### ABI Offset Bugs in Responses

The backend returns ABI **byte-offsets** instead of actual values for some fields:
- `copyMode` → Returns `416` or `480` (byte offset), not the JSON value
- `oppositeCopy` → Always returns `true` regardless of actual setting

**Workaround:** Store your own copy trade configuration locally. Don't rely on response values for `copyMode` or `oppositeCopy`.

### Max 3 HL Copy Trades

The HyperLiquid perp copy trading system allows a maximum of 3 active copy trades per user. Creating a 4th will fail.

## Network Issues

### Cloudflare Blocking

The GDEX backend sits behind Cloudflare. Requests without a browser-like `User-Agent` may be blocked.

```typescript
// The SDK handles this automatically, but for manual requests:
headers: {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${apiKey}`,
}
```

### Bridge Endpoint Paths

Bridge endpoints use non-obvious paths:
- `GET /v1/bridge/estimate_bridge` (not `/bridge/estimate`)
- `POST /v1/bridge/request_bridge` (not `/bridge/execute`)
- `GET /v1/bridge/bridge_orders` (not `/bridge/orders`)

## Debugging Checklist

When a trade fails, check in order:

1. **Auth:** Is `loginWithApiKey()` called? Is the API key valid?
2. **Wallet:** Are you using the **control** wallet address (not managed)?
3. **Chain ID:** Is chain ID correct for the operation? (See table above)
4. **Nonce:** Is the nonce fresh (`Date.now()`)?
5. **ABI types:** Do the ABI types exactly match what the backend expects?
6. **Signature:** Is the session key signing (not control key)? Is the message format correct?
7. **Balance:** Does the managed wallet have enough funds + gas?

## Portfolio / Balances / Trade History Quirks (Live-Tested)

These are **critical for autonomous agents** — the high-level SDK methods have parameter mismatches:

| Endpoint | SDK Method Issue | Correct Raw Client Call |
|----------|-----------------|------------------------|
| Portfolio | `getPortfolio()` sends `walletAddress`+`chain` | `GET /v1/portfolio?userId=X&chainId=N&data=Y` |
| Balances | `getBalances()` sends `walletAddress`+`chain` | `GET /v1/balances?userId=X&chainId=N&data=Y` |
| Trade History | `getTradeHistory()` sends `userId` | `GET /v1/user_trade_history?user=X&chainId=900&data=Y` |

**Key differences:**
- Portfolio/balances: Backend expects `userId` + `chainId` + `data` (encrypted session key), NOT `walletAddress` + `chain`
- Trade history: Backend expects `user` (NOT `userId`) and `chainId: 900` for Solana (NOT `622112261`)
- All three require the encrypted session key from `buildGdexUserSessionData()`

```typescript
import { buildGdexUserSessionData } from '@gdexsdk/gdex-skill';
const data = buildGdexUserSessionData(sessionKey, apiKey);

// Correct portfolio call
const portfolio = await skill.client.get('/v1/portfolio', {
  params: { userId: controlAddress, chainId: 622112261, data }
});

// Correct trade history call
const history = await skill.client.get('/v1/user_trade_history', {
  params: { user: controlAddress, chainId: 900, data, page: 1, limit: 20 }
});
```

## Limit Order ABI Bug (Fixed in SDK)

The `limit_buy` and `update_order` ABI schemas encode `profitPercent` and `lossPercent` as `uint256`, NOT `string`. Using `string` type causes the backend to receive ABI byte-offsets (e.g. 192) instead of the actual percentage values, which always fails the 0-100 range validation.

**Symptom:** `"lossPercent must be between 0 and 100"` even with valid values like `lossPercent: '25'`
**Cause:** ABI `string` type → encoded offset (192) → fails range check
**Fix:** SDK encodes as `uint256` (correct). Only matters if encoding manually.
8. **Token support:** Is the token supported on this chain? Is the DEX working? (Meteora is broken)

## Related Skills

- **gdex-authentication** — Full auth flow and encryption details
- **gdex-spot-trading** — Spot trade parameters and chain support
- **gdex-perp-trading** — HL perp specifics
- **gdex-copy-trading** — Solana copy trade ABI format
- **gdex-perp-copy-trading** — HL perp copy trade ABI format
