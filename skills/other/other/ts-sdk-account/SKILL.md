---
name: ts-sdk-account
description:
  "How to create and use Account (signer) in @aptos-labs/ts-sdk. Covers Account.generate(), fromPrivateKey(),
  fromDerivationPath(), Ed25519 vs SingleKey vs MultiKey vs Keyless, serialization (fromHex/toHex). Triggers on:
  'Account.generate', 'Account.fromPrivateKey', 'Ed25519PrivateKey', 'SDK account', 'mnemonic', 'SingleKeyAccount',
  'KeylessAccount'."
license: MIT
metadata:
  author: aptos-labs
  version: "1.0"
  category: sdk
  tags: ["typescript", "sdk", "account", "signer", "private-key", "ed25519", "keyless"]
  priority: high
---

# TypeScript SDK: Account (Signer)

## Purpose

Guide creation and use of **Account** (signer) in `@aptos-labs/ts-sdk`. An Account holds address + key material and can
sign transactions and messages. **Creating an Account does NOT create the account on-chain**; use faucet or transfer to
fund it.

## ALWAYS

1. **Use `Account.generate()` or `Account.fromPrivateKey()` only in server/script** – never in frontend; use wallet
   adapter for end users.
2. **Load private keys from env (e.g. `process.env.PRIVATE_KEY`) on server** – never hardcode.
3. **Use `account.accountAddress` when building transactions** – pass as sender/secondary signers.
4. **Use `aptos.signAndSubmitTransaction({ signer: account, transaction })`** with the same Account instance that holds
   the key.

## NEVER

1. **Do not use `Account.generate()` or raw private keys in browser/frontend** – use wallet adapter.
2. **Do not hardcode private keys** in source or commit to git.
3. **Do not confuse `Account` (API namespace) with `Account` (signer class)** – API is `aptos.account.*`; signer is the
   class from `Account` module (e.g. `Account.fromPrivateKey`).

---

## Account types (signing schemes)

| Type              | Class                     | Use case                           |
| ----------------- | ------------------------- | ---------------------------------- |
| Ed25519 (legacy)  | `Ed25519Account`          | Single Ed25519 key, legacy auth    |
| SingleKey         | `SingleKeyAccount`        | Ed25519 or Secp256k1, unified auth |
| MultiKey          | `MultiKeyAccount`         | Multi-sig                          |
| Keyless           | `KeylessAccount`          | Keyless (e.g. OIDC)                |
| Federated Keyless | `FederatedKeylessAccount` | Federated keyless                  |

---

## Generate new account (server/script only)

```typescript
import { Account, SigningSchemeInput } from "@aptos-labs/ts-sdk";

// Default: Ed25519 legacy
const ed25519Account = Account.generate();

// SingleKey (unified) with Ed25519
const singleKeyAccount = Account.generate({ scheme: SigningSchemeInput.Ed25519, legacy: false });

// SingleKey with Secp256k1
const secpAccount = Account.generate({ scheme: SigningSchemeInput.Secp256k1 });

// Access address and public key
const address = ed25519Account.accountAddress;
const pubKey = ed25519Account.publicKey;
```

---

## From private key

```typescript
import { Account, Ed25519PrivateKey, Secp256k1PrivateKey } from "@aptos-labs/ts-sdk";

// Ed25519 legacy (default)
const privateKeyHex = process.env.PRIVATE_KEY!; // e.g. "0x..." or AIP-80 prefixed
const privateKey = new Ed25519PrivateKey(privateKeyHex);
const account = Account.fromPrivateKey({ privateKey });

// Ed25519 SingleKey (unified)
const accountSingle = Account.fromPrivateKey({
  privateKey: new Ed25519PrivateKey(privateKeyHex),
  legacy: false
});

// Secp256k1 (always SingleKey)
const secpKey = new Secp256k1PrivateKey(process.env.SECP_KEY!);
const accountSecp = Account.fromPrivateKey({ privateKey: secpKey });

// Optional: fixed address (e.g. after key rotation)
const accountWithAddr = Account.fromPrivateKey({
  privateKey,
  address: "0x..."
});
```

---

## From mnemonic (derivation path)

```typescript
import { Account } from "@aptos-labs/ts-sdk";

const mnemonic = "word1 word2 ... word12";
const path = "m/44'/637'/0'/0'/0'"; // Aptos BIP-44 path

// Ed25519 legacy
const acc = Account.fromDerivationPath({ mnemonic, path });

// Ed25519 SingleKey
const accSingle = Account.fromDerivationPath({ mnemonic, path, legacy: false });

// Secp256k1
const accSecp = Account.fromDerivationPath({
  scheme: SigningSchemeInput.Secp256k1,
  mnemonic,
  path
});
```

---

## Auth key (for rotation / lookup)

```typescript
const authKey = Account.authKey({ publicKey: account.publicKey });
// Use authKey.derivedAddress() for address derivation; useful for multi-account lookup
```

---

## Serialization (toHex / fromHex)

Use when persisting or sending account (e.g. server-only, never expose private key to frontend):

```typescript
import { Account, AccountUtils } from "@aptos-labs/ts-sdk";

const account = Account.generate();

// Serialize to hex (includes private key – treat as secret)
const hex = AccountUtils.toHexString(account);

// Deserialize back
const restored = AccountUtils.fromHex(hex);

// Typed deserialize
const edAccount = AccountUtils.ed25519AccountFromHex(hex);
const singleAccount = AccountUtils.singleKeyAccountFromHex(hex);
const multiAccount = AccountUtils.multiKeyAccountFromHex(hex);
const keylessAccount = AccountUtils.keylessAccountFromHex(hex);
```

---

## Signing

```typescript
// Sign message (returns Signature)
const sig = account.sign(messageHex);

// Sign transaction (returns Signature; for submit use aptos.transaction.sign + submit)
const txSig = account.signTransaction(rawTransaction);

// With authenticator (used by SDK internally for submit)
const auth = account.signWithAuthenticator(messageHex);
```

---

## Verify signature

```typescript
const ok = account.verifySignature({ message: messageHex, signature: sig });

// Async (if key type needs on-chain state)
const okAsync = await account.verifySignatureAsync({
  aptosConfig: aptos.config,
  message: messageHex,
  signature: sig
});
```

---

## Derive account from private key (on-chain lookup)

When the same key may have multiple on-chain accounts (e.g. after rotation), use internal derivation + lookup:

```typescript
// Returns list of accounts owned by this key on chain
const accounts = await aptos.deriveOwnedAccountsFromSigner({
  signer: account
});
// Prefer wallet or explicit address for production; this is for scripts/tooling
```

---

## Common mistakes

| Mistake                                            | Correct approach                                                                              |
| -------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Using `Account.generate()` in frontend             | Use wallet adapter; generate only in server/script                                            |
| Hardcoding private key                             | Load from `process.env` (server) and never commit                                             |
| Using `aptos.account` as signer                    | `aptos.account` is API namespace; signer is `Account.fromPrivateKey()` / `Account.generate()` |
| Expecting account to exist on-chain after generate | Fund with faucet or transfer first                                                            |

---

## References

- SDK: `src/account/Account.ts`, `src/account/Ed25519Account.ts`, `src/account/AccountUtils.ts`, `src/api/account.ts`
- Pattern: [TYPESCRIPT_SDK.md](../../../../patterns/fullstack/TYPESCRIPT_SDK.md)
- Related: [ts-sdk-client](../ts-sdk-client/SKILL.md), [ts-sdk-transactions](../ts-sdk-transactions/SKILL.md),
  [use-ts-sdk](../use-ts-sdk/SKILL.md)
