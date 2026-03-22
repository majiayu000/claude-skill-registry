---
name: gdex-wallet-setup
description: Generate EVM control wallets offline, create session keypairs, get wallet info — first step for users without wallets
---

# GDEX: Wallet Setup

Generate EVM control wallets for new users and session keypairs for managed-custody trading. Wallet generation is fully offline — no network or auth required.

## When to Use

- A user says they don't have a wallet
- Setting up a new user for the first time
- Generating session keypairs for managed-custody trading
- Querying wallet info on a specific chain

## Prerequisites

```bash
npm install @gdexsdk/gdex-skill
```

No authentication needed for wallet generation.

## Generate an EVM Control Wallet

```typescript
import { generateEvmWallet } from '@gdexsdk/gdex-skill';

const wallet = generateEvmWallet();
console.log('Address:', wallet.address);        // public — safe to display
console.log('Private Key:', wallet.privateKey);  // SECRET — store securely
console.log('Mnemonic:', wallet.mnemonic);       // SECRET — 12-word backup phrase

// wallet.type         → 'evm'
// wallet.derivationPath → "m/44'/60'/0'/0/0"
```

**Important:**
- Works fully offline — no network or API calls
- The private key and mnemonic must be stored securely
- Never log, display in UI, or transmit the private key
- The EVM control wallet is all you need — after managed-custody sign-in, the backend provisions Solana + other chain wallets automatically

## Generate a Session Keypair

Session keypairs (secp256k1) are used to sign trades after the initial control-wallet sign-in:

```typescript
import { generateGdexSessionKeyPair } from '@gdexsdk/gdex-skill';

const { sessionPrivateKey, sessionKey } = generateGdexSessionKeyPair();
// sessionPrivateKey: hex string (store securely, reuse across requests)
// sessionKey: compressed public key (0x + 66 hex chars)
```

## Get Wallet Info

Query native balance and token count on a specific chain (requires auth):

```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY } from '@gdexsdk/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);

const info = await skill.getWalletInfo({
  walletAddress: '0xYourAddress',
  chain: 1,   // Ethereum
});
```

### Wallet Info Response

```typescript
interface WalletInfo {
  address: string;
  chain: string | number;
  nativeBalance: string;
  nativeSymbol: string;    // 'ETH', 'SOL', 'SUI', etc.
  totalValueUsd?: number;
  tokenCount?: number;
}
```

## Full New User Onboarding Flow

```typescript
import {
  generateEvmWallet,
  generateGdexSessionKeyPair,
  buildGdexSignInMessage,
  buildGdexSignInComputedData,
  GdexSkill,
  GDEX_API_KEY_PRIMARY,
} from '@gdexsdk/gdex-skill';

// Step 1: Generate a control wallet (offline)
const wallet = generateEvmWallet();
console.log('Your new wallet address:', wallet.address);
// ⚠️ Tell user to save privateKey and mnemonic securely!

// Step 2: Generate session keypair
const { sessionPrivateKey, sessionKey } = generateGdexSessionKeyPair();

// Step 3: Initialize SDK
const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);

// Step 4: Build sign-in message and sign with the new wallet
const userId = wallet.address;
const nonce = String(Math.floor(Date.now() / 1000) + Math.floor(Math.random() * 1000));
const message = buildGdexSignInMessage(userId, nonce, sessionKey);

// For a generated wallet, sign directly with ethers:
import { ethers } from 'ethers';
const signer = new ethers.Wallet(wallet.privateKey);
const signature = await signer.signMessage(message);

// Step 5: Sign in via managed custody
const signInPayload = buildGdexSignInComputedData({
  apiKey: GDEX_API_KEY_PRIMARY,
  userId,
  sessionKey,
  nonce,
  signature,
});
await skill.signInWithComputedData({
  computedData: signInPayload.computedData,
  chainId: 1,  // EVM
});

// ✅ User is now authenticated and can trade
// The backend has provisioned Solana + other chain wallets automatically
```

## Autonomous Agent Notes (Live-Tested)

1. **`generateEvmWallet()` works fully offline (E2E verified).** No network calls needed. Returns `{ address, privateKey, mnemonic, type, derivationPath }`.
2. **After sign-in, the backend auto-provisions managed wallets** on all chains. You only need one EVM control wallet.
3. **Store the mnemonic and private key securely.** Loss = permanent loss of access.
4. **The session keypair is separate from the wallet.** Generate it with `generateGdexSessionKeyPair()` — it's used for signing trades, not wallet derivation.
5. **Multiple sign-ins are fine.** You can generate new session keys and re-sign-in at any time.

## Related Skills

- **gdex-authentication** — Full managed-custody auth details
- **gdex-onboarding** — Platform overview for new users
- **gdex-spot-trading** — Start trading after wallet setup
