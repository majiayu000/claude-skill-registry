---
name: solana-development
description: Build Solana programs with Anchor framework or native Rust. Use when developing Solana smart contracts, implementing token operations, testing programs, deploying to networks, or working with Solana development. Covers both high-level Anchor framework (recommended) and low-level native Rust for advanced use cases.
---

# Solana Development

Build Solana programs using Anchor framework or native Rust. Both approaches share the same core concepts (accounts, PDAs, CPIs, tokens) but differ in syntax and abstraction level.

## Quick Start

### Recommended: Anchor Framework

Anchor provides macros and tooling that reduce boilerplate and increase developer productivity:

```rust
use anchor_lang::prelude::*;

declare_id!("YourProgramID");

#[program]
pub mod my_program {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>, data: u64) -> Result<()> {
        ctx.accounts.account.data = data;
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(init, payer = user, space = 8 + 8)]
    pub account: Account<'info, MyAccount>,
    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[account]
pub struct MyAccount {
    pub data: u64,
}
```

**When to use Anchor:**
- Building DeFi, NFT, or standard programs
- Need TypeScript client generation with IDL
- Want faster development with less boilerplate
- Following common Solana patterns
- New to Solana development

**Installation:**
```bash
cargo install --git https://github.com/coral-xyz/anchor avm --locked --force
avm install latest
avm use latest
anchor --version
```

**Create project:**
```bash
anchor init my_project
cd my_project
anchor build
anchor test
```

**→ See [references/anchor.md](references/anchor.md) for complete Anchor guide**

### Advanced: Native Rust

Native Rust provides maximum control, optimization potential, and deeper understanding of Solana's runtime:

```rust
use solana_program::{
    account_info::AccountInfo,
    entrypoint,
    entrypoint::ProgramResult,
    pubkey::Pubkey,
    msg,
};

entrypoint!(process_instruction);

pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    msg!("Processing instruction");
    // Manual account parsing and validation
    // Manual instruction routing
    Ok(())
}
```

**When to use Native Rust:**
- Need maximum compute efficiency (CU optimization critical)
- Require advanced features (versioned transactions, durable nonces, ALTs)
- Learning Solana fundamentals from first principles
- Building highly optimized or specialized programs
- Framework overhead is unacceptable

**Setup:**
```bash
cargo new my_program --lib
cd my_program
# Configure Cargo.toml (see native-rust.md)
cargo build-sbf
```

**→ See [references/native-rust.md](references/native-rust.md) for complete native Rust guide**

## Core Concepts

Essential knowledge for all Solana developers, regardless of framework:

### Foundational Concepts

- **[accounts.md](references/accounts.md)** - Account model, ownership, rent, validation patterns
- **[pda.md](references/pda.md)** - Program Derived Addresses: derivation, canonical bumps, signing patterns
- **[cpi.md](references/cpi.md)** - Cross-Program Invocations: calling other programs safely

### Program Integration

- **[tokens-overview.md](references/tokens-overview.md)** - Token account structures and ATAs
- **[tokens-operations.md](references/tokens-operations.md)** - Create, mint, transfer, burn, close operations
- **[tokens-validation.md](references/tokens-validation.md)** - Account validation patterns
- **[tokens-2022.md](references/tokens-2022.md)** - Token Extensions Program features
- **[tokens-patterns.md](references/tokens-patterns.md)** - Common patterns and security
- **[testing-overview.md](references/testing-overview.md)** - Test pyramid and strategy
- **[testing-frameworks.md](references/testing-frameworks.md)** - Mollusk, Anchor test, Native Rust
- **[testing-practices.md](references/testing-practices.md)** - Best practices and patterns
- **[surfpool.md](references/surfpool.md)** - Local development with Surfpool: mainnet forking, cheatcodes, IaC
- **[deployment.md](references/deployment.md)** - Deploy, upgrade, verify, and manage programs
- **[production-deployment.md](references/production-deployment.md)** - Verified builds for production (Anchor 0.32.1 workflow)

### Implementation Details

- **[serialization.md](references/serialization.md)** - Account data layout, Borsh, zero-copy patterns
- **[error-handling.md](references/error-handling.md)** - Custom error types, propagation, client-side handling
- **[security.md](references/security.md)** - Security best practices and defensive programming patterns

### Advanced Features

- **[compute-optimization.md](references/compute-optimization.md)** - CU optimization techniques and benchmarking
- **[versioned-transactions.md](references/versioned-transactions.md)** - Address Lookup Tables for 256+ accounts
- **[durable-nonces.md](references/durable-nonces.md)** - Offline signing with durable transaction nonces
- **[transaction-lifecycle.md](references/transaction-lifecycle.md)** - Submission, retry patterns, confirmations

### Low-Level Details

- **[sysvars.md](references/sysvars.md)** - System variables (Clock, Rent, EpochSchedule, SlotHashes)
- **[builtin-programs.md](references/builtin-programs.md)** - System Program and Compute Budget Program

### Resources

- **[resources.md](references/resources.md)** - Official docs, tools, learning paths, community

## Common Tasks Quick Reference

**Create a new program:**
- Anchor: `anchor init my_project` → [anchor.md#getting-started](references/anchor.md)
- Native: `cargo new my_program --lib` → [native-rust.md#setup](references/native-rust.md)

**Initialize a PDA account:**
- Anchor: Use `#[account(init, seeds = [...], bump)]` → [pda.md#anchor](references/pda.md)
- Native: Manual `invoke_signed` with System Program → [pda.md#native](references/pda.md)

**Transfer SPL tokens:**
- Anchor: Use `anchor_spl::token::transfer` → [tokens-operations.md#transferring-tokens](references/tokens-operations.md)
- Native: CPI to Token Program → [tokens-operations.md#transferring-tokens](references/tokens-operations.md)

**Test your program:**
- Both: Mollusk for fast unit tests → [testing-frameworks.md#mollusk-testing](references/testing-frameworks.md)
- Anchor: `anchor test` for integration tests → [testing-frameworks.md#anchor-specific-testing](references/testing-frameworks.md)

**Local development with mainnet forking:**
- Both: `surfpool start` for mainnet-forked local network → [surfpool.md](references/surfpool.md)

**Test with mainnet state (Jupiter, Raydium CPIs):**
- Both: Use Surfpool JIT forking → [surfpool.md#mainnet-forking](references/surfpool.md)

**Profile compute units in detail:**
- Both: `surfnet_profileTransaction` cheatcode → [surfpool.md#transaction-profiling](references/surfpool.md)

**Deploy to devnet:**
- Anchor: `anchor deploy` → [deployment.md#anchor](references/deployment.md)
- Native: `solana program deploy` → [deployment.md#native](references/deployment.md)

**Deploy to production (verified builds):**
- Both: `solana-verify build` + `solana program deploy` → [production-deployment.md](references/production-deployment.md)

**Optimize compute units:**
- Both: Profile with Mollusk bencher → [compute-optimization.md](references/compute-optimization.md)

**Handle 40+ accounts:**
- Both: Use Address Lookup Tables → [versioned-transactions.md](references/versioned-transactions.md)

**Offline transaction signing:**
- Both: Use durable nonces → [durable-nonces.md](references/durable-nonces.md)

## Decision Guide

| Your Need | Recommended Approach | Reason |
|-----------|---------------------|---------|
| Standard DeFi/NFT program | Anchor | Faster development, proven patterns |
| TypeScript client needed | Anchor | Auto-generates IDL and client types |
| Learning Solana fundamentals | Native Rust first | Understand the platform deeply |
| Compute optimization critical | Native Rust | Direct control, minimal overhead |
| Advanced tx features (ALTs, nonces) | Either (slight edge to Native) | Framework-agnostic features |
| Fast prototyping | Anchor | Less boilerplate, faster iteration |
| Maximum control over every detail | Native Rust | No abstraction layer |
| Team familiar with frameworks | Anchor | Lower learning curve |
| Program size matters | Native Rust | Smaller compiled programs |

**Note:** You can also start with Anchor for rapid development, then optimize critical paths with native Rust patterns if needed.

## Framework Comparison

| Aspect | Anchor | Native Rust |
|--------|--------|-------------|
| **Setup complexity** | Simple (`anchor init`) | Manual (Cargo.toml, entrypoint) |
| **Boilerplate** | Minimal (macros handle it) | Significant (manual everything) |
| **Account validation** | Declarative (`#[account(...)]`) | Manual (explicit checks) |
| **Serialization** | Automatic (Borsh via macros) | Manual (Borsh or custom) |
| **Type safety** | High (compile-time checks) | High (but more verbose) |
| **IDL generation** | Automatic | Manual or tools |
| **Client library** | TypeScript + Rust auto-gen | Manual client code |
| **Testing** | `anchor test`, Mollusk | Mollusk, cargo test |
| **Deployment** | `anchor deploy` | `solana program deploy` |
| **Compute overhead** | Small (~1-3% typical) | None (direct) |
| **Program size** | Slightly larger | Smaller |
| **Learning curve** | Gentler (abstractions help) | Steeper (need SVM knowledge) |
| **Debugging** | Good (clear macro errors) | More complex (lower level) |
| **Community** | Large (most use Anchor) | Growing (optimization focus) |

## Typical Development Workflow

### Anchor Workflow

1. **Init**: `anchor init my_project`
2. **Define accounts**: Use `#[derive(Accounts)]` with constraints
3. **Implement instructions**: Write functions in `#[program]` module
4. **Define state**: Use `#[account]` macro for account structures
5. **Test**: Write tests in `tests/`, run `anchor test`
6. **Deploy**: `anchor deploy` to configured network
7. **Client**: Import generated IDL and types in TypeScript/Rust

### Native Rust Workflow

1. **Setup**: `cargo new my_program --lib`, configure Cargo.toml
2. **Define entrypoint**: Implement `process_instruction` function
3. **Define state**: Manual Borsh serialization structs
4. **Implement instructions**: Manual routing and account parsing
5. **Validate accounts**: Explicit ownership, signer, writable checks
6. **Test**: Write Mollusk tests, run `cargo test`
7. **Build**: `cargo build-sbf`
8. **Deploy**: `solana program deploy target/deploy/program.so`
9. **Client**: Build client manually or use web3.js/rs

## Best Practices

### General (Both Approaches)

✅ **Always validate accounts**: Check ownership, signers, mutability
✅ **Use checked arithmetic**: `.checked_add()`, `.checked_sub()`, etc.
✅ **Test extensively**: Unit tests, integration tests, edge cases
✅ **Handle errors gracefully**: Return descriptive errors
✅ **Document your code**: Explain account requirements and constraints
✅ **Version your programs**: Plan for upgrades and migrations
✅ **Use PDAs for program-owned accounts**: Don't pass private keys
✅ **Minimize compute units**: Profile and optimize hot paths
✅ **Add security.txt**: Make it easy for researchers to contact you

### Anchor-Specific

✅ **Use `InitSpace` derive**: Auto-calculate account space
✅ **Prefer `has_one` constraints**: Clearer than custom constraints
✅ **Use `Program<'info, T>`**: Validate program accounts in CPIs
✅ **Emit events**: Use `emit!` for important state changes
✅ **Group related constraints**: Keep account validation readable

### Native Rust-Specific

✅ **Use `next_account_info`**: Safe account iteration
✅ **Cache PDA bumps**: Store bump in account, use `create_program_address`
✅ **Zero-copy when possible**: 50%+ CU savings for large structs
✅ **Minimize logging**: Especially avoid pubkey formatting (expensive)
✅ **Build verifiable**: Use `solana-verify build` for production

## Security Considerations

**Both frameworks require security vigilance:**

⚠️ **Common vulnerabilities:**
- Missing signer checks
- Integer overflow/underflow
- Account confusion attacks
- PDA substitution
- Arbitrary CPI targets
- Missing account ownership checks
- Insufficient rent exemption
- Account closing without zeroing

**→ For defensive programming patterns and secure coding practices, see [security.md](references/security.md)**

That guide provides:
- Core security rules and principles
- Account validation patterns
- Arithmetic safety guidelines
- Pre-deployment security checklist

**→ For comprehensive security audits, use the `solana-security` skill**

That skill provides:
- Systematic vulnerability analysis
- Attack scenarios and exploit POCs
- Framework-specific security reviews
- Professional audit workflows

## When to Switch or Combine

**Start with Anchor, optimize later:**
- Build MVP with Anchor for speed
- Profile to find CU bottlenecks
- Optimize critical paths with native patterns
- Keep Anchor for non-critical code

**Start with Native, add Anchor features:**
- Build core program logic in native Rust
- Use Anchor's client generation separately
- Leverage anchor-spl for common patterns
- Maintain control where it matters

**Use both in a workspace:**
```toml
[workspace]
members = [
    "programs/core",      # Native Rust
    "programs/wrapper",   # Anchor facade
]
```

## Getting Help

- **Anchor**: [Discord](https://discord.gg/srmqvxf), [Docs](https://www.anchor-lang.com/docs)
- **Solana**: [Stack Exchange](https://solana.stackexchange.com/), [Discord](https://discord.gg/solana)
- **General**: See [resources.md](references/resources.md) for comprehensive links

## Next Steps

**New to Solana?**
1. Read [accounts.md](references/accounts.md) - Understand the account model
2. Read [anchor.md](references/anchor.md) - Start with Anchor framework
3. Read [security.md](references/security.md) - Learn secure coding from the start
4. Build a simple program following [testing-overview.md](references/testing-overview.md)
5. Deploy to devnet using [deployment.md](references/deployment.md)

**Coming from another blockchain?**
1. Read [accounts.md](references/accounts.md) - Solana's model is different
2. Read [pda.md](references/pda.md) - Unique to Solana
3. Choose Anchor for familiar framework experience
4. Explore [resources.md](references/resources.md) for migration guides

**Want to optimize?**
1. Start with working Anchor program
2. Profile with [compute-optimization.md](references/compute-optimization.md)
3. Learn native patterns from [native-rust.md](references/native-rust.md)
4. Refactor bottlenecks selectively

**Building production apps?**
1. Master [security considerations](references/pda.md#security)
2. Use [testing-practices.md](references/testing-practices.md) for comprehensive best practices
3. Follow [production-deployment.md](references/production-deployment.md) for verified builds
4. Get security audit with `solana-security` skill
