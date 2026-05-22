---
name: anchor-expert-2026
description: Expert Anchor smart contract development for Solana (January 2026). Use when (1) Writing or auditing Solana programs, (2) Implementing security patterns, (3) Defining account structures and constraints, (4) Building CPI interactions, (5) Testing with Mollusk/LiteSVM, (6) Deploying programs, or any Anchor/Solana program development questions.
---

# Anchor Expert Guide - January 2026

## What is Anchor?

Anchor is a framework for Solana smart contract development that provides:
- **Security by default** - Automatic checks for common vulnerabilities
- **Simplified account management** - Declarative account validation
- **IDL generation** - Automatic TypeScript client generation
- **Testing framework** - Integrated testing with TypeScript
- **CLI tooling** - Build, deploy, test, upgrade programs

**Current Version**: 0.32.1
**Solana Version**: 1.18+ (compatible with 2.x)

## When to Use This Skill

- Writing Rust smart contracts for Solana
- Implementing secure account validation
- Building cross-program invocations (CPI)
- Testing programs with Mollusk or LiteSVM
- Deploying and upgrading programs
- Generating TypeScript clients

## Quick Reference

See `.claude/rules/programs.md` for comprehensive patterns and security checklist.

## Core Patterns

### Program Structure
```rust
use anchor_lang::prelude::*;

declare_id!("YourProgramId11111111111111111111111111111");

#[program]
pub mod my_program {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        // Implementation
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(init, payer = user, space = 8 + MyAccount::INIT_SPACE)]
    pub my_account: Account<'info, MyAccount>,

    #[account(mut)]
    pub user: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[account]
#[derive(InitSpace)]
pub struct MyAccount {
    pub data: u64,
}
```

### Critical Security Rules

1. **ALWAYS verify account ownership**: Use `Account<'info, T>` not `AccountInfo`
2. **ALWAYS use checked arithmetic**: `.checked_add()`, `.checked_mul()`, etc.
3. **ALWAYS validate signers**: Use `Signer<'info>` for authorities
4. **ALWAYS store PDA bumps**: Store bump seeds in account data
5. **NEVER use init_if_needed without validation**: Reinitialization attacks

### Account Constraints

```rust
// Initialize new account
#[account(init, payer = user, space = 8 + SIZE)]

// PDA with seeds
#[account(seeds = [b"my-seed", user.key().as_ref()], bump)]

// Verify field matches
#[account(has_one = authority)]

// Custom constraint
#[account(constraint = amount > 0 @ ErrorCode::InvalidAmount)]

// Close account
#[account(close = authority)]
```

## Testing

### Mollusk (Fast Unit Tests)
```rust
use mollusk::Mollusk;

#[test]
fn test_initialize() {
    let program_id = Pubkey::new_unique();
    let mut mollusk = Mollusk::new(&program_id, "target/deploy/my_program");

    // Test execution...
}
```

### Anchor Tests (Integration)
```bash
anchor test                # Run all tests
anchor test --skip-local-validator  # Skip starting validator
```

## Deployment

```bash
# Build
anchor build

# Deploy to devnet
anchor deploy

# Upgrade existing program
anchor upgrade target/deploy/program.so --program-id <ID>

# Verify
solana program show <PROGRAM_ID>
```

## Additional Resources

- Full patterns: `.claude/rules/programs.md`
- Anchor Docs: https://anchor-lang.com/docs
- Security Audit: https://github.com/coral-xyz/sealevel-attacks
