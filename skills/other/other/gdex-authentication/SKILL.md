---
name: gdex-authentication
description: Managed-custody authentication — shared API key login, session keypair generation, encrypted computedData payloads, AES-256-CBC encryption, and secp256k1 trade signing
---

# GDEX: Authentication

All GDEX trading uses **managed-custody wallets** with encrypted `computedData` payloads. This skill covers both the simple shared-API-key auth and the full managed-custody flow.

## When to Use

- Setting up authentication for any trading operation
- Implementing managed-custody sign-in for a control wallet
- Understanding the encryption and signing pipeline
- Troubleshooting auth errors (401, 403, code 103)

## Prerequisites

```bash
npm install @gdexsdk/gdex-skill
```

## 1. Shared API Key Login (Simple)

For agents that need quick access — no wallet signing required:

```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY } from '@gdexsdk/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);
// skill.isAuthenticated() → true
```

**Shared API Keys:**
- Primary: `9b4e1c73-6a2f-4d88-b5c9-3e7a2f1d6c54`
- Secondary: `2c8f0a91-5d34-4e7b-9a62-f1c3d8e4b705`

> Read-only endpoints (`getTokenDetails`, `getTrendingTokens`, `getOHLCV`, `getTopTraders`) do not require any authentication.

## 2. Managed-Custody Flow (Full Trading)

For trading operations, the full managed-custody flow is:

```
Generate Session Keypair → Build Sign-In Message → Control Wallet Signs →
Encrypt as computedData → POST /v1/sign_in → Resolve User → Trade
```

### Step-by-Step

```typescript
import {
  GdexSkill,
  GDEX_API_KEY_PRIMARY,
  generateGdexSessionKeyPair,
  buildGdexSignInMessage,
  buildGdexSignInComputedData,
  buildGdexManagedTradeComputedData,
  buildGdexUserSessionData,
} from '@gdexsdk/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);
const apiKey = GDEX_API_KEY_PRIMARY;

// Step 1: Generate a secp256k1 session keypair
const { sessionPrivateKey, sessionKey } = generateGdexSessionKeyPair();
// sessionKey = compressed public key (0x + 66 hex chars)

// Step 2: Build the sign-in message
const userId = '0xYourControlWalletAddress'; // EVM address or Solana pubkey
const nonce = String(Math.floor(Date.now() / 1000) + Math.floor(Math.random() * 1000));
const message = buildGdexSignInMessage(userId, nonce, sessionKey);
// → "By signing, you agree to GDEX Trading Terms of Use..."

// Step 3: Sign with control wallet
//   EVM:    wallet.signMessage(message) → EIP-191 personal_sign
//   Solana: nacl.sign.detached(Buffer.from(message)) → base58 encoded
const signature = '...'; // your wallet's signature

// Step 4: Build encrypted computedData and POST to /v1/sign_in
const signInPayload = buildGdexSignInComputedData({
  apiKey, userId, sessionKey, nonce, signature,
});
const signInResult = await skill.signInWithComputedData({
  computedData: signInPayload.computedData,
  chainId: 900, // 900=Solana, 101=Sui, or numeric EVM chain ID
});

// Step 5: Resolve user profile / check managed wallet
const userData = buildGdexUserSessionData(sessionKey, apiKey);
const user = await skill.getManagedUser({ userId, data: userData, chainId: 622112261 }); // Solana
// → { address: "CFSi4YimeCbfSNqH2WmHwJKwj1YYG1cWBtQyVPB4sCe1", chainId: "622112261", ... }
```

> **Critical: Solana chainId is `622112261` (`ChainId.SOLANA`), NOT `900`.** Using `900` returns the EVM managed address with `balance: null`. The `/v1/user` endpoint returns a **different managed wallet address** per `chainId`:
> - `chainId=1` → EVM managed: `0x9967179de55bd67e6b90fcc4f908556d93938c0f`
> - `chainId=622112261` → Solana managed: `CFSi4YimeCbfSNqH2WmHwJKwj1YYG1cWBtQyVPB4sCe1` (base58)

### Nonce Generation

Nonces are **client-generated** (not fetched from the server):

```typescript
const nonce = String(Math.floor(Date.now() / 1000) + Math.floor(Math.random() * 1000));
```

## 3. Encryption Details (AES-256-CBC)

All payloads use **deterministic** AES-256-CBC — no random IV:

| Property | Derivation |
|----------|------------|
| **Key** | First 32 bytes of `SHA256(apiKey)` hex |
| **IV** | First 16 bytes of `SHA256(SHA256(apiKey))` hex |

```typescript
import { encryptGdexComputedData, decryptGdexComputedData, deriveGdexAesMaterial } from '@gdexsdk/gdex-skill';

// Encrypt a JSON payload
const cipherHex = encryptGdexComputedData(JSON.stringify({ userId, data, signature, apiKey }), apiKey);

// Decrypt
const plaintext = decryptGdexComputedData(cipherHex, apiKey);

// Get raw key/IV material
const { key, iv } = deriveGdexAesMaterial(apiKey);
```

**Important:**
- Trade/sign-in payloads: `JSON.stringify(...)` → UTF-8 → encrypt → hex
- Session key for `/v1/user`: raw hex-decoded bytes → encrypt (NOT UTF-8 string; use `encryptGdexHexData`)
- The API key is included **inside** the encrypted JSON payload, not just used for encryption
- Do NOT use random IVs or `iv:ciphertext` format

## 4. Trade Signing (secp256k1)

**Spot trade signatures** use raw keccak256 + secp256k1 (no EIP-191 prefix):

```typescript
import { signGdexTradeMessageWithSessionKey } from '@gdexsdk/gdex-skill';

const signature = signGdexTradeMessageWithSessionKey(
  'purchase',       // action: 'purchase' or 'sell'
  userId,           // lowercase address
  dataHex,          // ABI-encoded trade data (without 0x prefix)
  sessionPrivateKey,
);
// Returns: r(64 hex) + s(64 hex) + v(2 hex) = 130 chars, no 0x prefix
// v = raw recoveryParam (00 or 01), NOT EIP-155 (1b/1c)
```

**Sign-in** is the ONLY operation that uses EIP-191 `personal_sign` with the control wallet.

### ABI Encoding Schemas

| Operation | ABI Types | Fields |
|-----------|-----------|--------|
| **Sign-in** | `['bytes', 'string', 'string']` | `[sessionKey, nonce, refCode]` |
| **Trade** | `['string', 'uint256', 'string']` | `[tokenAddress, amount, nonce]` |

## 5. Building Trade Payloads

```typescript
import { buildGdexManagedTradeComputedData } from '@gdexsdk/gdex-skill';

const trade = buildGdexManagedTradeComputedData({
  apiKey,
  action: 'purchase',  // or 'sell'
  userId: '0xYourAddress',
  tokenAddress: 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263',
  amount: '100000',     // in smallest unit
  nonce: String(Math.floor(Date.now() / 1000) + Math.floor(Math.random() * 1000)),
  sessionPrivateKey,
});

const result = await skill.submitManagedPurchase({
  computedData: trade.computedData,
  chainId: 900,
  slippage: 1,
});

// Poll trade status
if (result.requestId) {
  const status = await skill.getManagedTradeStatus(result.requestId);
  console.log('Status:', status.status, 'Hash:', status.hash);
}
```

## 6. Wallet-Based Auth (Advanced)

For user-owned wallets or browser extensions:

```typescript
// EVM wallet
await skill.authenticate({
  type: 'evm',
  address: '0xYourAddress',
  privateKey: '0xPrivateKey',
});

// Solana wallet
await skill.authenticate({
  type: 'solana',
  address: 'YourSolanaAddress',
  privateKey: 'base58EncodedPrivateKey',
});

// Custom signer (MetaMask / Phantom)
await skill.authenticate({
  type: 'evm',
  address: accounts[0],
  signer: async (message) =>
    window.ethereum.request({ method: 'personal_sign', params: [message, accounts[0]] }),
});
```

## 7. SDK Configuration

```typescript
const skill = new GdexSkill({
  apiUrl:     'https://trade-api.gemach.io/v1', // Default backend
  timeout:    30000,                             // Request timeout ms
  maxRetries: 3,                                 // Retry on 429/503
  debug:      false,                             // Log requests
});
```

HTTP headers MUST include a browser User-Agent (e.g., Chrome/91) — non-browser UAs get 403 from Cloudflare. Use `Authorization: Bearer <apiKey>` header, NOT `X-API-Key`.

## Helper Functions Reference

| Function | Purpose |
|----------|---------|
| `generateGdexSessionKeyPair()` | Generate secp256k1 session keypair |
| `buildGdexSignInMessage(userId, nonce, sessionKey)` | Build sign-in message for wallet signing |
| `buildGdexSignInComputedData({...})` | Build encrypted sign-in payload |
| `buildGdexUserSessionData(sessionKey, apiKey)` | Encrypt session key for `/v1/user` |
| `buildGdexManagedTradeComputedData({...})` | Build encrypted trade payload |
| `signGdexTradeMessageWithSessionKey(action, userId, data, privKey)` | Sign trade with session key |
| `encryptGdexComputedData(plaintext, apiKey)` | AES-256-CBC encrypt UTF-8 |
| `encryptGdexHexData(hexData, apiKey)` | AES-256-CBC encrypt raw hex bytes |
| `decryptGdexComputedData(cipherHex, apiKey)` | AES-256-CBC decrypt |
| `deriveGdexAesMaterial(apiKey)` | Get raw AES key/IV |

## Common Issues

### 401 Unauthorized
- API key not set or expired — call `skill.loginWithApiKey(apiKey)` first
- Session expired — re-authenticate

### 403 Forbidden
- Non-browser User-Agent header — the SDK handles this automatically
- Using `X-API-Key` instead of `Authorization: Bearer`

### 400 Unauthorized (code 103) on HL operations
- **Most common cause:** Passing the **managed address** as `walletAddress` instead of the **control wallet address**.
- During sign-in, the session key is registered for the control wallet address (the one that signed the sign-in message).
- All HL write operations (`hlCreateOrder`, `perpDeposit`, `hlCloseAll`, etc.) sign the payload as `{action}-{walletAddress}-{data}` — if `walletAddress` doesn't match the sign-in `userId`, the signature verification fails.
- **Fix:** Always set `walletAddress` to the control wallet address used during sign-in, NOT the managed address returned by `/v1/user` or `/v1/sign_in`.

```typescript
// ❌ WRONG — managed address causes code 103
const creds = { apiKey, walletAddress: user.address, sessionPrivateKey };

// ✅ CORRECT — use the control wallet that signed in
const creds = { apiKey, walletAddress: controlWallet.address, sessionPrivateKey };
```

### 400 Unauthorized (code 103) on HL operations
- Wrong ABI encoding for the specific HL action — see **gdex-perp-trading** skill
- Using `uint256` instead of `uint64` for chainId in `hl_deposit`
- Wrong signature format (must be raw `v=00/01`, not EIP-155 `v=1b/1c`)

## Autonomous Agent Notes (Live-Tested)

### Complete Auth Flow — Verified Working

```typescript
import { ethers } from 'ethers';
import {
  GdexSkill, GDEX_API_KEY_PRIMARY,
  generateGdexSessionKeyPair, buildGdexSignInMessage,
  buildGdexSignInComputedData, buildGdexUserSessionData,
} from '@gdexsdk/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);

// 1. Generate session keypair
const { sessionPrivateKey, sessionKey } = generateGdexSessionKeyPair();

// 2. Sign in with control wallet
const wallet = ethers.Wallet.fromPhrase('your mnemonic phrase...');
const userId = wallet.address;
const nonce = String(Math.floor(Date.now() / 1000) + Math.floor(Math.random() * 1000));
const message = buildGdexSignInMessage(userId, nonce, sessionKey);
const signature = await wallet.signMessage(message);

const signInPayload = buildGdexSignInComputedData({
  apiKey: GDEX_API_KEY_PRIMARY, userId, sessionKey, nonce, signature,
});
await skill.signInWithComputedData({
  computedData: signInPayload.computedData,
  chainId: 1,  // EVM for HL/perps, 622112261 for Solana spot
});

// 3. Resolve managed wallet
const data = buildGdexUserSessionData(sessionKey, GDEX_API_KEY_PRIMARY);
const user = await skill.getManagedUser({ userId, data, chainId: 622112261 });
// user.address = managed Solana wallet (base58)
```

### ChainId for Sign-In Matters

| Operation | Sign-In ChainId | Why |
|-----------|----------------|-----|
| Solana spot/limit/copy | `622112261` | Solana chain context |
| HL perps, deposit, withdraw | `1` (EVM) | HL uses EVM wallets |
| HL perp copy trading | `1` (EVM) | HL copy uses EVM |
| Bridge | `1` (EVM) | Bridge uses EVM context |

### Credentials to Keep Track Of

An autonomous agent must persist these across operations:
- `sessionPrivateKey` — signs all trade payloads (one per sign-in session)
- `sessionKey` — used to build encrypted `data` for read endpoints
- `controlAddress` (=`userId`) — the wallet that signed in (used in all API calls)
- `managedEvmAddress` — from `/v1/user?chainId=1` (needed for `user_stats` only)
- `managedSolanaAddress` — from `/v1/user?chainId=622112261` (for on-chain queries only)

## Related Skills

- **gdex-onboarding** — Platform overview and getting started
- **gdex-spot-trading** — Buy/sell tokens (requires auth)
- **gdex-perp-trading** — HyperLiquid perps (requires auth + HL-specific crypto)
- **gdex-wallet-setup** — Generate control wallets for new users
