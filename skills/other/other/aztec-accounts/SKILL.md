---
name: aztec-accounts
description: Manage Aztec accounts including Schnorr account creation, deployment, and recovery from credentials. Use when creating accounts, deploying wallets, or recovering existing accounts.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Aztec Accounts Skill

Create, deploy, and manage Aztec accounts with proper key management.

## Subskills

* [Schnorr Accounts](./schnorr-accounts.md) - Creating and deploying Schnorr accounts
* [Account Recovery](./account-recovery.md) - Recovering accounts from saved credentials

## Quick Start: Create and Deploy Account

```typescript
import { Fr } from "@aztec/aztec.js/fields";
import { GrumpkinScalar } from "@aztec/foundation/curves/grumpkin";
import { AztecAddress } from "@aztec/stdlib/aztec-address";
import { AccountManager } from "@aztec/aztec.js/wallet";
import { SponsoredFeePaymentMethod } from "@aztec/aztec.js/fee";

// Generate new account keys
const secretKey = Fr.random();
const signingKey = GrumpkinScalar.random();
const salt = Fr.random();

// Create account manager
const account = await wallet.createSchnorrAccount(secretKey, salt, signingKey);
console.log(`Account address: ${account.address}`);

// Deploy account (required before use)
await (await account.getDeployMethod()).send({
    from: AztecAddress.ZERO,
    fee: { paymentMethod: sponsoredPaymentMethod },
    wait: { timeout: 120000 }
});
```

## Account Types

Aztec supports several account types:

| Type | Description | Use Case |
|------|-------------|----------|
| Schnorr | ECDSA-compatible | Most common, recommended |
| ECDSA | Ethereum-style | Ethereum compatibility |

## Key Components

- **Secret Key (Fr)** - Private key for encryption
- **Signing Key (GrumpkinScalar)** - Private key for transaction signing
- **Salt (Fr)** - Randomness for address derivation
- **Address** - Derived deterministically from above

## Important: Save Credentials

After creating an account, **always save the credentials**:

```typescript
console.log(`SECRET=${secretKey.toString()}`);
console.log(`SIGNING_KEY=${signingKey.toString()}`);
console.log(`SALT=${salt.toString()}`);
```

Store these in your `.env` file for later recovery.

## Key Imports

```typescript
// Key types
import { Fr } from "@aztec/aztec.js/fields";
import { GrumpkinScalar } from "@aztec/foundation/curves/grumpkin";

// Account management
import { AccountManager } from "@aztec/aztec.js/wallet";
import { AztecAddress } from "@aztec/stdlib/aztec-address";

// Wallet
import { EmbeddedWallet } from "@aztec/wallets/embedded";

// Fee payment
import { SponsoredFeePaymentMethod } from "@aztec/aztec.js/fee";
```
