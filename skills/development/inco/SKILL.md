---
name: inco-svm
description: Build confidential dApps on Solana using Inco Lightning encryption — encrypted balances, private transfers, and attested decryption
---

# Inco SVM — Confidential Computing on Solana

Inco Lightning is a confidentiality layer for Solana that enables developers to build applications where sensitive data remains encrypted even during computation. It uses Trusted Execution Environments (TEEs) to deliver verifiable confidential compute — no new chain, no new wallet required.

> **Note:** Inco SVM is currently in **beta** on Solana devnet. Features are subject to change.

## Overview

- **Encrypted Types** — `Euint128` and `Ebool` handles representing encrypted values stored off-chain
- **Homomorphic Operations** — Arithmetic, comparison, bitwise, and control flow on encrypted data via CPI
- **Access Control** — Allowance PDA system for granting per-handle decryption permissions
- **Attested Decryption** — Ed25519 signature-verified decryption through TEE covalidators
- **Confidential SPL Token** — Privacy-preserving token standard with encrypted balances and transfers
- **Client SDK** — `@inco/solana-sdk` for encryption, decryption, and utility helpers

## Architecture

```
Client                    Solana Program              Inco Covalidator (TEE)
  │                            │                              │
  ├─ encryptValue() ──────────►│                              │
  │                            ├─ CPI: new_euint128 ─────────►│
  │                            │◄─── handle (u128) ──────────┤
  │                            ├─ CPI: e_add / e_sub / ... ──►│
  │                            │◄─── result handle ──────────┤
  │                            ├─ CPI: allow() ──────────────►│
  │                            │                              │
  ├─ decrypt([handle]) ───────────────────────────────────────►│
  │◄─── plaintext + Ed25519 attestation ──────────────────────┤
```

**Inco Lightning Program ID:** `5sjEbPiqgZrYwR31ahR6Uk9wf5awoX61YGg7jExQSwaj`

## Quick Start

### Installation

**Rust Crate (on-chain):**

Add to your `Cargo.toml`:
```toml
[dependencies]
inco-lightning = { version = "0.1", features = ["cpi"] }
```

Add to `Anchor.toml`:
```toml
[programs.devnet]
inco_lightning = "5sjEbPiqgZrYwR31ahR6Uk9wf5awoX61YGg7jExQSwaj"
```

**JavaScript SDK (client-side):**
```bash
npm install @inco/solana-sdk
```

### Basic Program Setup

```rust
use anchor_lang::prelude::*;
use inco_lightning::cpi::accounts::Operation;
use inco_lightning::cpi::{e_add, e_sub, e_ge, e_select, new_euint128, as_euint128};
use inco_lightning::types::{Euint128, Ebool};
use inco_lightning::ID as INCO_LIGHTNING_ID;

declare_id!("YOUR_PROGRAM_ID");

#[program]
pub mod my_confidential_program {
    use super::*;

    pub fn deposit(ctx: Context<Deposit>, ciphertext: Vec<u8>) -> Result<()> {
        let cpi_ctx = CpiContext::new(
            ctx.accounts.inco_lightning_program.to_account_info(),
            Operation {
                signer: ctx.accounts.authority.to_account_info(),
            },
        );

        // Create encrypted handle from client ciphertext
        let amount: Euint128 = new_euint128(cpi_ctx.clone(), ciphertext, 0)?;

        // Add to existing balance
        let new_balance = e_add(cpi_ctx, ctx.accounts.vault.balance, amount, 0)?;
        ctx.accounts.vault.balance = new_balance;

        Ok(())
    }
}

#[derive(Accounts)]
pub struct Deposit<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,
    #[account(mut)]
    pub vault: Account<'info, Vault>,
    /// CHECK: Inco Lightning program
    #[account(address = INCO_LIGHTNING_ID)]
    pub inco_lightning_program: AccountInfo<'info>,
}

#[account]
pub struct Vault {
    pub balance: Euint128,
}
```

### Basic Client Usage

```typescript
import { encryptValue } from "@inco/solana-sdk/encryption";
import { decrypt } from "@inco/solana-sdk/attested-decrypt";

// Encrypt a value before sending to program
const encrypted = await encryptValue(1000n);

await program.methods
  .deposit(Buffer.from(encrypted, "hex"))
  .accounts({ authority: wallet.publicKey, vault: vaultPda, incoLightningProgram: INCO_LIGHTNING_ID })
  .rpc();

// Decrypt a handle (requires wallet signature)
const result = await decrypt([handleString], {
  address: wallet.publicKey,
  signMessage: wallet.signMessage,
});
console.log("Decrypted:", result.plaintexts[0]);
```

## Encrypted Types & Handles

Handles are 128-bit references to encrypted values stored off-chain in the covalidator network.

| Type | Description | Rust Definition |
|------|-------------|-----------------|
| `Euint128` | Encrypted unsigned 128-bit integer | `pub struct Euint128(pub u128)` |
| `Ebool` | Encrypted boolean | `pub struct Ebool(pub u128)` |

Store handles directly in account structs:
```rust
#[account]
pub struct ConfidentialAccount {
    pub balance: Euint128,
    pub is_active: Ebool,
}
```

### Input Functions

| Function | Description |
|----------|-------------|
| `new_euint128(ctx, ciphertext, input_type)` | Create from client-encrypted ciphertext |
| `new_ebool(ctx, ciphertext, input_type)` | Create encrypted bool from ciphertext |
| `as_euint128(ctx, value)` | Trivial encryption of plaintext u128 (for constants like zero) |
| `as_ebool(ctx, value)` | Trivial encryption of plaintext bool |

## Operations on Encrypted Data

All operations require a CPI context and return new handles.

```rust
let cpi_ctx = CpiContext::new(
    ctx.accounts.inco_lightning_program.to_account_info(),
    Operation { signer: ctx.accounts.authority.to_account_info() },
);
let result = e_add(cpi_ctx, a, b, 0)?;
```

The last parameter (`scalar_byte`) is `0` for encrypted-encrypted operations, `1` when the left operand is plaintext.

### Arithmetic → `Euint128`
`e_add`, `e_sub`, `e_mul`, `e_rem`

### Comparison → `Ebool`
`e_ge`, `e_gt`, `e_le`, `e_lt`, `e_eq`

### Bitwise → `Euint128`
`e_and`, `e_or`, `e_not`, `e_shl`, `e_shr`

### Control Flow (Multiplexer)
```rust
// Cannot use if/else on encrypted values — use e_select instead
let result = e_select(cpi_ctx, condition, if_true, if_false, 0)?;
```

### Random Number Generation
```rust
let random_value = e_rand(cpi_ctx, 0)?;
```

See [resources/rust-sdk-reference.md](resources/rust-sdk-reference.md) for the complete API.

## Access Control

Decryption permissions are managed through **Allowance PDAs** derived from `[handle.to_le_bytes(), allowed_address]`.

```rust
use inco_lightning::cpi::accounts::Allow;
use inco_lightning::cpi::allow;

let cpi_ctx = CpiContext::new(
    ctx.accounts.inco_lightning_program.to_account_info(),
    Allow {
        allowance_account: ctx.accounts.allowance_account.to_account_info(),
        signer: ctx.accounts.authority.to_account_info(),
        allowed_address: ctx.accounts.user.to_account_info(),
        system_program: ctx.accounts.system_program.to_account_info(),
    },
);
allow(cpi_ctx, handle.0, true, user_pubkey)?;
```

**Important:** Operations produce new handles, and allowance PDAs depend on the handle value. You must **simulate the transaction first** to get the result handle, derive the PDA, then submit with `remaining_accounts`.

See [resources/access-control.md](resources/access-control.md) for the full simulation-then-submit pattern.

## Attested Decryption

Two modes:

| Mode | Purpose | Returns |
|------|---------|---------|
| **Attested Reveal** | Display values in UI | `result.plaintexts` |
| **Attested Decrypt** | Verify values on-chain | `result.ed25519Instructions` + program IX |

```typescript
import { decrypt } from "@inco/solana-sdk/attested-decrypt";

const result = await decrypt([handle], {
  address: wallet.publicKey,
  signMessage: wallet.signMessage,
});

// Reveal: use plaintext directly
console.log(result.plaintexts[0]);

// Decrypt: verify on-chain
const tx = new Transaction();
result.ed25519Instructions.forEach(ix => tx.add(ix));
tx.add(yourProgramVerifyInstruction);
await sendTransaction(tx);
```

On-chain verification:
```rust
use inco_lightning::cpi::is_validsignature;
use inco_lightning::cpi::accounts::VerifySignature;

let cpi_ctx = CpiContext::new(
    ctx.accounts.inco_lightning_program.to_account_info(),
    VerifySignature {
        instructions: ctx.accounts.instructions.to_account_info(),
        signer: ctx.accounts.authority.to_account_info(),
    },
);
is_validsignature(cpi_ctx, 1, Some(handles), Some(plaintext_values))?;
```

## Confidential SPL Token

A full privacy-preserving token implementation. See [resources/confidential-spl-token.md](resources/confidential-spl-token.md).

Key functions: `initialize_mint`, `create_account`, `mint_to`, `transfer`, `approve`

```typescript
// Encrypt and transfer
const encrypted = await encryptValue(500_000_000n);
await program.methods
  .transfer(Buffer.from(encrypted, "hex"), 0)
  .accounts({ source: srcAta, destination: destAta, authority: wallet.publicKey })
  .rpc();
```

## Best Practices

1. **Always call `allow()` after operations** that produce handles you want to decrypt later
2. **Use `remaining_accounts`** to pass allowance PDAs and grant access in the same transaction
3. **Grant minimal permissions** — only allow specific addresses to decrypt what they need
4. **Use the multiplexer pattern** (`e_select`) instead of if/else on encrypted conditions
5. **Trivial encryption only for constants** (like zero) — use client-side encryption for sensitive values
6. **Verify the intended handle** in attestations to prevent handle-swap attacks
7. **Simulate transactions first** to get result handles before deriving allowance PDAs

## Resources

- [Inco SVM Docs](https://docs.inco.org/svm/home)
- [Rust SDK Reference](https://docs.inco.org/svm/rust-sdk/overview)
- [JS SDK Reference](https://docs.inco.org/svm/js-sdk/overview)
- [Concepts Guide](https://docs.inco.org/svm/guide/intro)
- [Confidential SPL Token](https://docs.inco.org/svm/tutorials/confidential-spl-token/overview)
- [Private Raffle Tutorial](https://docs.inco.org/svm/tutorials/private-raffle/overview)
- [Next.js Template Repo](https://github.com/Inco-fhevm/nextjs-template-svm.git)
- [Lightning Rod Solana Repo](https://github.com/Inco-fhevm/lightning-rod-solana.git)

## Skill Structure

```
inco/
├── SKILL.md                              # This file — main reference
├── docs/
│   └── troubleshooting.md                # Common issues and solutions
├── examples/
│   ├── basic-operations/
│   │   └── encrypted-operations.ts       # Arithmetic, comparison, select
│   ├── confidential-spl-token/
│   │   ├── mint-and-transfer.ts          # Mint & transfer confidential tokens
│   │   └── reveal-balance.ts             # Decrypt and reveal token balance
│   └── private-raffle/
│       └── raffle-client.ts              # Full raffle lifecycle client
├── resources/
│   ├── rust-sdk-reference.md             # Complete Rust CPI API
│   ├── js-sdk-reference.md               # JS SDK encryption & decryption
│   ├── access-control.md                 # Allowance PDAs & simulation pattern
│   └── confidential-spl-token.md         # SPL token program reference
└── templates/
    └── inco-svm-setup.ts                 # Starter template with helpers
```
