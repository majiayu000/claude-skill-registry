---
name: solana-compression
description: Build with ZK Compression on Solana using Light Protocol. Use when creating compressed tokens, compressed PDAs, or integrating ZK compression into Solana programs. Covers compressed account model, state trees, validity proofs, and client integration with Helius/Photon RPC.
---

# ZK Compression on Solana

ZK Compression enables rent-free tokens and PDAs on Solana by storing state on the ledger instead of in accounts, using zero-knowledge proofs to validate state transitions. Built by Light Protocol and indexed by Helius Photon.

## When to Use ZK Compression

**Use ZK Compression when:**
- Creating millions of token accounts (5000x cheaper than regular accounts)
- Minting to many recipients (airdrops, loyalty programs, gaming assets)
- Building apps with many user accounts that are infrequently updated
- Reducing rent costs for PDAs with low update frequency

**Use regular accounts when:**
- Account is updated frequently (>1000 lifetime writes)
- Account stores large data accessed in on-chain transactions
- Compute budget is critical (compression adds ~100k CU overhead)

## Quick Start

### Installation

```bash
# TypeScript client
npm install @lightprotocol/stateless.js @lightprotocol/compressed-token

# Rust SDK for programs
cargo add light-sdk

# CLI for development
npm install -g @lightprotocol/zk-compression-cli
```

### Local Development

```bash
# Start local validator with compression support
light test-validator

# Initialize a new Anchor project with compression
light init my-program
```

### Mint Compressed Tokens (TypeScript)

```typescript
import { createRpc } from '@lightprotocol/stateless.js';
import { createMint, mintTo, transfer } from '@lightprotocol/compressed-token';

const rpc = createRpc(); // or createRpc('https://mainnet.helius-rpc.com?api-key=YOUR_KEY')

// Create mint with token pool for compression
const { mint } = await createMint(rpc, payer, payer.publicKey, 9);

// Mint compressed tokens (creates compressed token accounts)
await mintTo(rpc, payer, mint, recipient, payer, 1_000_000_000);

// Transfer compressed tokens
await transfer(rpc, payer, mint, 500_000_000, owner, recipient);

// Query compressed token accounts
const accounts = await rpc.getCompressedTokenAccountsByOwner(owner, { mint });
```

### Build Program with Compressed PDAs (Anchor)

```rust
use anchor_lang::prelude::*;
use light_sdk::{
    account::LightAccount,
    address::v1::derive_address,
    cpi::{v1::CpiAccounts, CpiSigner},
    derive_light_cpi_signer,
    instruction::{account_meta::CompressedAccountMeta, PackedAddressTreeInfo, ValidityProof},
    LightDiscriminator, LightHasher,
};

declare_id!("YourProgramID");

pub const LIGHT_CPI_SIGNER: CpiSigner = derive_light_cpi_signer!("YourProgramID");

#[program]
pub mod my_program {
    use super::*;
    use light_sdk::cpi::{v1::LightSystemProgramCpi, InvokeLightSystemProgram};

    pub fn create_account<'info>(
        ctx: Context<'_, '_, '_, 'info, MyAccounts<'info>>,
        proof: ValidityProof,
        address_tree_info: PackedAddressTreeInfo,
        output_state_tree_index: u8,
    ) -> Result<()> {
        let light_cpi_accounts = CpiAccounts::new(
            ctx.accounts.signer.as_ref(),
            ctx.remaining_accounts,
            crate::LIGHT_CPI_SIGNER,
        );

        let (address, address_seed) = derive_address(
            &[b"my_account", ctx.accounts.signer.key().as_ref()],
            &address_tree_info.get_tree_pubkey(&light_cpi_accounts)?,
            &crate::ID,
        );

        let new_address_params = address_tree_info.into_new_address_params_packed(address_seed);

        // Create new compressed account
        let mut account = LightAccount::<MyAccount>::new_init(
            &crate::ID,
            Some(address),
            output_state_tree_index,
        );
        account.owner = ctx.accounts.signer.key();
        account.data = 0;

        LightSystemProgramCpi::new_cpi(LIGHT_CPI_SIGNER, proof)
            .with_light_account(account)?
            .with_new_addresses(&[new_address_params])
            .invoke(light_cpi_accounts)?;

        Ok(())
    }

    pub fn update_account<'info>(
        ctx: Context<'_, '_, '_, 'info, MyAccounts<'info>>,
        proof: ValidityProof,
        current_data: u64,
        account_meta: CompressedAccountMeta,
    ) -> Result<()> {
        // Modify existing compressed account
        let mut account = LightAccount::<MyAccount>::new_mut(
            &crate::ID,
            &account_meta,
            MyAccount {
                owner: ctx.accounts.signer.key(),
                data: current_data,
            },
        )?;

        account.data = account.data.checked_add(1).unwrap();

        let light_cpi_accounts = CpiAccounts::new(
            ctx.accounts.signer.as_ref(),
            ctx.remaining_accounts,
            crate::LIGHT_CPI_SIGNER,
        );

        LightSystemProgramCpi::new_cpi(LIGHT_CPI_SIGNER, proof)
            .with_light_account(account)?
            .invoke(light_cpi_accounts)?;

        Ok(())
    }
}

#[derive(Accounts)]
pub struct MyAccounts<'info> {
    #[account(mut)]
    pub signer: Signer<'info>,
}

#[event]
#[derive(Clone, Debug, Default, LightDiscriminator, LightHasher)]
pub struct MyAccount {
    #[hash]
    pub owner: Pubkey,
    pub data: u64,
}
```

## Core Concepts

### Compressed Account Model

Compressed accounts are similar to regular Solana accounts but stored differently:

| Aspect | Regular Account | Compressed Account |
|--------|-----------------|-------------------|
| Storage | AccountsDB (disk) | Ledger (call data) |
| Rent | Required (~0.002 SOL per 100 bytes) | None |
| Identification | Pubkey | Hash (changes on write) or Address |
| State validation | Runtime checks | ZK validity proofs |

**Key differences:**
- Hash changes on every write (accounts identified by content hash)
- Optional persistent address for PDAs (similar to regular PDAs)
- State stored in Merkle trees with only roots on-chain

### State Trees

Compressed accounts are stored in concurrent Merkle trees using Poseidon hashing:
- Only the tree root is stored on-chain
- Leaves contain compressed account hashes
- Validity proofs prove account inclusion in tree

### Validity Proofs

ZK proofs (Groth16) validate state transitions:
- Prove existence of N accounts in M state trees
- Constant 128-byte proof size regardless of accounts
- ~100k CU for proof verification

### Transaction Lifecycle

1. **Build**: Client fetches compressed accounts and validity proofs via RPC
2. **Submit**: Transaction includes account data + proof in payload
3. **Validate**: Light System Program verifies proof and account integrity
4. **Update**: New state appended to tree, old state nullified
5. **Index**: Photon RPC nodes index new state from ledger

## LightAccount Operations

```rust
// Create new account (no input state, only output)
let account = LightAccount::<T>::new_init(&program_id, Some(address), tree_index);

// Modify existing account (input + output state)
let mut account = LightAccount::<T>::new_mut(&program_id, &account_meta, current_state)?;
account.field = new_value;

// Close account (input state, no output)
let account = LightAccount::<T>::new_close(&program_id, &account_meta, current_state)?;
```

## Helius SDK Integration

Query compressed state via Helius RPC:

```typescript
import { Helius } from 'helius-sdk';

const helius = new Helius('YOUR_API_KEY');

// Get compressed account by hash or address
const account = await helius.zk.getCompressedAccount({ address });

// Get all compressed accounts for owner
const accounts = await helius.zk.getCompressedAccountsByOwner(owner);

// Get compressed token accounts
const tokenAccounts = await helius.zk.getCompressedTokenAccountsByOwner(owner, { mint });

// Get validity proof for accounts
const proof = await helius.zk.getValidityProof({ hashes: [hash1, hash2] });

// Get compression signatures for account
const signatures = await helius.zk.getCompressionSignaturesForAccount(hash);
```

## RPC Methods

ZK Compression RPC API (via Helius or self-hosted Photon):

| Method | Description |
|--------|-------------|
| `getCompressedAccount` | Get account by hash or address |
| `getCompressedAccountsByOwner` | Get all accounts owned by pubkey |
| `getCompressedTokenAccountsByOwner` | Get token accounts for owner |
| `getCompressedTokenBalancesByOwner` | Get token balances summary |
| `getValidityProof` | Get ZK proof for account inclusion |
| `getMultipleCompressedAccounts` | Batch fetch accounts |
| `getCompressionSignaturesForAccount` | Get transaction history |

## Infrastructure

### Node Types

| Node | Purpose | Run By |
|------|---------|--------|
| **Photon RPC** | Index compressed state, serve queries | Helius (canonical), self-host |
| **Prover** | Generate validity proofs | Bundled with Photon or standalone |
| **Forester** | Maintain state trees, empty nullifier queues | Light Protocol, community |

### Running Photon Locally

```bash
# Install
cargo install photon-indexer

# Run against devnet
photon --rpc-url=https://api.devnet.solana.com

# With Postgres for production
photon --db-url=postgres://postgres@localhost/postgres --rpc-url=<RPC_URL>

# Load from snapshot for faster bootstrap
photon-snapshot-loader --snapshot-dir=~/snapshot --snapshot-server-url=https://photon-devnet-snapshot.helius-rpc.com
```

## Trade-offs

| Consideration | Impact |
|---------------|--------|
| **Larger transactions** | +128 bytes for proof + account data in payload |
| **Higher CU usage** | ~100k CU proof verification + ~6k CU per account |
| **Per-write cost** | Each write nullifies old state, appends new |
| **Indexer dependency** | Requires Photon RPC (or self-host) for queries |

**Break-even analysis**: Compressed account becomes more expensive than regular account after ~1000 writes.

## Reference Documentation

- **[compressed-accounts.md](references/compressed-accounts.md)** - Detailed account model, hashing, addresses
- **[compressed-tokens.md](references/compressed-tokens.md)** - Token operations, pools, batch operations
- **[compressed-pdas.md](references/compressed-pdas.md)** - Building programs with compressed PDAs
- **[client-integration.md](references/client-integration.md)** - TypeScript/Rust client setup, RPC methods

## Resources

- [ZK Compression Docs](https://www.zkcompression.com/)
- [Light Protocol GitHub](https://github.com/Lightprotocol/light-protocol)
- [Helius SDK](https://github.com/helius-labs/helius-sdk)
- [Photon Indexer](https://github.com/helius-labs/photon)
- [Program Examples](https://github.com/Lightprotocol/program-examples)
- [Helius ZK Blog](https://www.helius.dev/blog/zero-knowledge-proofs-its-applications-on-solana)
