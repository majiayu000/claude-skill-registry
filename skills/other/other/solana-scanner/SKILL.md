---
id: SCANNER-SOLANA
title: Solana Program Security Scanner
category: chain-scanner
chains: [solana]
languages: [rust]
frameworks: [anchor, native]
last_updated: 2026-02-24
description: >-
  Use when auditing Solana programs for security vulnerabilities, reviewing
  Anchor or Pinocchio/native Rust smart contracts, checking CPI safety, PDA
  validation, account ownership, signer verification, or Token-2022 security.
---

# Solana Scanner Skill

## Purpose

Analyze Solana programs (Rust/Anchor) for security vulnerabilities specific to the Solana runtime model. Solana's account-based execution model, where programs are stateless and all state is passed via accounts, creates a fundamentally different attack surface from EVM chains.

## Core Principle

> An attacker controls **every account, argument, ordering, and CPI call-graph** passed to your program. Your on-chain code must prove each input is legitimate before touching state or funds.

## Solana Security Model

| Property | Solana | EVM |
|----------|--------|-----|
| Execution model | Programs receive accounts as input | Contracts own their storage |
| State ownership | Account owner (program ID) controls data | Contract controls its own storage |
| Caller identity | Signer flag on accounts | `msg.sender` |
| Cross-program calls | CPI — accounts passed through | Internal calls share storage |
| Math safety | Overflow wraps in release mode | Solidity 0.8+ reverts on overflow |
| Account validation | Manual (native) or declarative (Anchor) | Automatic via `msg.sender` |
| Upgrades | Program authority can upgrade any time | Proxy patterns required |
| Rent | Accounts must maintain minimum SOL balance | No rent (storage is permanent) |

## Detection Capabilities

### Critical — Direct Fund Loss

| Vulnerability | Description | Detection Signal |
|---------------|-------------|-----------------|
| **Missing signer check** | Privileged instruction lacks signer validation | `AccountInfo` without `is_signer` check |
| **Missing owner check** | Program accepts accounts owned by other programs | No `owner == program_id` validation |
| **Arbitrary CPI** | Cross-program invocation to user-controlled program ID | `invoke()` with unchecked `program_id` |
| **PDA seed manipulation** | PDA derived with controllable seeds | Seeds include user-controlled data without validation |
| **Account data overwrite** | Writing data to wrong account | Missing discriminator / account type check |

### High — Significant Impact

| Vulnerability | Description | Detection Signal |
|---------------|-------------|-----------------|
| **Integer overflow (release)** | Wrapping arithmetic in release builds | Math ops without `checked_*` or Anchor `require!` |
| **Account closing revival** | Closed account can be revived in same tx | Close without zeroing data + relying on zero lamports |
| **Duplicate account injection** | Same account passed for two different parameters | No uniqueness check between accounts |
| **Type confusion** | Account deserialized as wrong type | Missing discriminator validation |
| **CPI privilege escalation** | CPI inherits signer privileges incorrectly | `invoke_signed()` with wrong seeds |

### Medium — Conditional Impact

| Vulnerability | Description | Detection Signal |
|---------------|-------------|-----------------|
| **PDA bump seed guessing** | Not storing/reusing canonical bump | `find_program_address` in instruction logic |
| **Missing rent exemption** | Account may be garbage collected | No rent-exempt check after creation |
| **Unchecked account size** | Account realloc without bounds | `realloc()` without size validation |
| **Clock dependency** | Using `Clock::get()` for security-sensitive logic | Validator can influence timestamp slightly |
| **Token account validation** | SPL Token account not validated for mint/owner | Missing `token::mint` or `token::authority` check |

## Key Audit Patterns

### Vulnerability Categories with Prevention Code

Each category shows the **risk**, an **attack** example, and **prevention** for both Anchor and Pinocchio/native Rust.

#### 1. Missing Owner Checks

**Risk**: Attacker substitutes a fake account owned by their own program with crafted data.

```rust
// Anchor Prevention — Account<'info, T> auto-checks owner
#[account]
pub struct Vault { pub authority: Pubkey, pub balance: u64 }

#[derive(Accounts)]
pub struct Withdraw<'info> {
    #[account(mut, has_one = authority)]
    pub vault: Account<'info, Vault>,  // owner = this program ✓
    pub authority: Signer<'info>,
}
```

```rust
// Pinocchio Prevention — explicit owner check
assert!(vault.is_owned_by(&crate::ID), ProgramError::IllegalOwner);
```

#### 2. Missing Signer Checks

**Risk**: Anyone can call privileged instructions (withdraw, admin config).

```rust
// Anchor: Signer<'info> enforces is_signer automatically
pub authority: Signer<'info>,

// Pinocchio: manual check
assert!(authority.is_signer(), ProgramError::MissingRequiredSignature);
```

#### 3. Arbitrary CPI

**Risk**: Attacker passes a malicious program ID, redirecting CPI to their program.

```rust
// Anchor Prevention — Program<'info, T> validates executable + ID
pub token_program: Program<'info, Token>,

// Pinocchio Prevention — compare key against known constant
assert_eq!(token_program.key(), &spl_token::ID);
```

#### 4. Reinitialization

**Risk**: Attacker re-calls `initialize` to overwrite authority/settings.

```rust
// Anchor: init constraint creates + sets discriminator in one atomic step
#[account(init, payer = user, space = 8 + Vault::INIT_SPACE)]
pub vault: Account<'info, Vault>,
// ⚠️ Avoid init_if_needed — lets attacker front-run with bad data

// Pinocchio: check discriminator before writing
let data = vault.try_borrow_data()?;
assert_eq!(data[0..8], [0u8; 8], "already initialized");
```

#### 5. PDA Sharing

**Risk**: Multiple users share one PDA → state confusion, fund theft.

```rust
// ❌ Bad: seeds only use pool-level data
#[account(seeds = [b"pool", pool.mint.as_ref()], bump)]

// ✅ Good: include user-specific identifier
#[account(seeds = [b"position", pool.key().as_ref(), user.key().as_ref()], bump)]
```

#### 6. Type Cosplay

**Risk**: Attacker passes account of type A where type B is expected (same size).

```rust
// Anchor auto-adds 8-byte discriminator to all #[account] types,
// and Account<'info, T> validates it on deserialization.

// Pinocchio: first 8 bytes must be a unique discriminator per type
let disc = &data[0..8];
assert_eq!(disc, VAULT_DISCRIMINATOR, "wrong account type");
```

#### 7. Duplicate Mutable Accounts

**Risk**: Same account passed as both `source` and `destination` → double-counting.

```rust
// Both frameworks — explicit key comparison
require!(source.key() != destination.key(), ErrorCode::DuplicateAccounts);
```

#### 8. Account Revival (Closing)

**Risk**: Closed account (0 lamports) data remains in tx — later instruction reads stale state.

```rust
// Anchor: close transfers lamports + zero discriminator
#[account(mut, close = destination)]
pub vault: Account<'info, Vault>,

// Pinocchio: manually zero + transfer + realloc
data[0] = 0xFF; // poison discriminator
**vault.try_borrow_mut_lamports()? = 0;
**destination.try_borrow_mut_lamports()? += lamports;
vault.realloc(0, false)?;
```

#### 9. Data Matching

**Risk**: Token account's `mint` or `authority` doesn't match expected values.

```rust
// Anchor: has_one validates field matches account key
#[account(mut, has_one = authority, has_one = mint)]
pub token_acct: Account<'info, TokenAccount>,

// Pinocchio: manual comparison
assert_eq!(token_acct.authority, expected_authority.key());
```

### Account Validation Matrix

Every instruction must validate EVERY account it accesses. Use this matrix:

| Check | Native Solana | Anchor |
|-------|--------------|--------|
| Is signer? | `account.is_signer` | `Signer<'info>` |
| Is writable? | `account.is_writable` | `#[account(mut)]` |
| Correct owner? | `account.owner == &program_id` | `Account<'info, T>` (automatic) |
| Correct PDA? | `Pubkey::find_program_address()` | `#[account(seeds = [...], bump)]` |
| Correct data type? | Check discriminator manually | `Account<'info, T>` (automatic) |
| Belongs to user? | Manual field comparison | `#[account(has_one = owner)]` |
| Not closed? | Check lamports > 0 and data | `Account<'info, T>` (checks discriminator) |
| Unique? | Compare pubkeys between params | Manual (Anchor doesn't auto-check) |

### Solana-Specific Attack Vectors

1. **Account Confusion Attack**: Passing a token account where a mint account is expected (or vice versa)
2. **Reinitialization Attack**: Calling `initialize` on already-initialized account
3. **Closing Account Revival**: Closing an account (zero lamports) but data remains readable in same tx
4. **CPI Re-signer Attack**: Exploiting that CPI can sign with PDA seeds the caller controls
5. **Remaining Accounts Abuse**: Exploiting unchecked accounts in `ctx.remaining_accounts`
6. **Flashback Attack**: Solana transactions can include multiple instructions — attacker can create and exploit account state in same tx

## Program-Side Security Checklist

### Account Validation (7 checks)

- [ ] Every account has an **owner check** (native) or uses `Account<'info, T>` (Anchor)
- [ ] Every privileged account has a **signer check**
- [ ] PDAs are derived with **sufficient unique seeds** (no PDA sharing)
- [ ] All accounts have **discriminator** validation (type cosplay prevention)
- [ ] Semantically distinct accounts are **compared for uniqueness**
- [ ] `has_one` / manual field comparison for **data matching** (mint, authority)
- [ ] Accounts in `remaining_accounts` are validated before use

### CPI Safety (3 checks)

- [ ] CPI target is a **known program** (`Program<'info, T>` or key comparison)
- [ ] `invoke_signed` seeds are **deterministic** and cannot be replayed
- [ ] CPI return data is **validated**, not blindly trusted

### Arithmetic (3 checks)

- [ ] All math uses `checked_*` operations or `overflow-checks = true` in Cargo.toml
- [ ] Token amounts validated against **actual balances** before transfer
- [ ] Fee/reward calculations handle **rounding** and **zero-value** edge cases

### State Lifecycle (4 checks)

- [ ] `init` is used instead of `init_if_needed` (prevents front-running)
- [ ] Closed accounts are **zeroed + poisoned** (discriminator = 0xFF)
- [ ] Upgrade authority is **verified** or program is **immutable** in production
- [ ] Account realloc operations check **size bounds**

## Client-Side Security Checklist

- [ ] Correct **cluster** (mainnet vs devnet) — program IDs differ
- [ ] Transactions are **simulated** before sending to catch errors early
- [ ] `getLatestBlockhash` uses **confirmed** or **finalized** commitment
- [ ] Transaction confirmation waits for **sufficient commitment** level
- [ ] **Token-2022** extensions (transfer hooks, transfer fees) are handled
- [ ] Lookup tables / versioned transactions are used for **large** account sets
- [ ] Priority fees are set appropriately for **congested** network conditions

## Build & IDL Integrity Checklist

Supply-chain and deployment verification — catches mismatches between audited source and deployed program.

- [ ] On-chain program **matches audited source** — verify with `solana program dump` + local rebuild
- [ ] **IDL matches on-chain behavior** — generated IDL (Anchor/Codama) reflects actual instruction layouts
- [ ] No **hand-written Borsh layouts** for programs the team owns — use IDL/codegen pipeline (hand-written layouts risk serialization mismatches → type confusion)
- [ ] No **hand-written IDLs** — generate from source via `anchor build` or Shank macros
- [ ] Codegen outputs **checked into git** for deterministic builds, or generated in CI with pinned versions
- [ ] Anchor version **pinned** in `Anchor.toml` — different Anchor versions produce different discriminators
- [ ] Solana CLI + Anchor versions **aligned** across dev, CI, and audit environments
- [ ] Program upgrade authority is **multisig or governance** (not a single EOA) for mainnet deployments
- [ ] If upgradeable, **upgrade timelock** exists to allow users to exit before code changes

## Security Review Questions

When reviewing a Solana program, systematically ask:

1. Can an attacker pass a **fake account** (wrong owner / wrong type)?
2. Can a **non-authorized** user trigger this instruction?
3. Can CPI be **substituted** to a malicious program?
4. Can `initialize` be **called again** on an existing account?
5. Are PDAs **shared** across users or contexts unintentionally?
6. Can the **same account** be passed for two different params?
7. Can a **closed account** be read or revived in a later instruction?
8. Do on-chain fields **match** expected accounts (authority, mint, owner)?

## Solana Audit Procedure

Step-by-step execution flow when auditing a Solana program. Adapted from Solana Foundation's recommended operating procedure.

### Step 1: Classify the Program

| Question | Why It Matters |
|----------|----------------|
| Anchor or native/Pinocchio? | Determines which constraint system to audit (declarative vs manual) |
| What token programs are used? | SPL Token vs Token-2022 — different extension attack surfaces |
| Is the program upgradeable? | If yes, audit the upgrade authority and governance process |
| Does it use CPI? | Cross-program calls are the #1 privilege escalation vector |
| Are there multiple instructions per tx? | Multi-instruction flows enable flashback attacks |

### Step 2: Map Every Account

For each instruction, build the **Account Validation Matrix** (see above). Every cell must be explicitly checked in code. An empty cell is a potential vulnerability.

### Step 3: Trace CPI Chains

For each `invoke()` / `invoke_signed()`:
1. Is the target program ID validated? (`Program<'info, T>` or key comparison)
2. Are signer seeds deterministic and non-replayable?
3. Does the CPI return data get validated, or is it blindly trusted?
4. Can an attacker substitute a malicious program ID?

### Step 4: Verify Arithmetic Safety

1. Check `Cargo.toml` for `overflow-checks = true` (release profile)
2. If not present, **every** arithmetic operation must use `checked_*`
3. Verify token amount calculations handle rounding and zero-value edge cases
4. Check for division before multiplication (precision loss)

### Step 5: Evaluate Formal Verification (if present)

If the program includes Kani proofs or other formal verification:
1. **Inventory proofs** — count, classify (STRONG/WEAK/VACUOUS), categorize by domain
2. **Map proofs to security claims** — does the proof actually back the claim?
3. **Identify what is NOT proven** — CPI execution, oracle reads, and runtime behavior are never Kani-verifiable
4. **Check for coupling proofs** — does the `verify` module match the production handler?
5. **Flag vacuous proofs** — any proof with contradictory `assume()` chains is a finding
6. **Report strength** — "N proofs (X% STRONG) covering [categories]"

See [Formal Verification for Auditors](resources/formal-verification-for-auditors.md) for proof classification and evaluation methodology.

### Step 6: Test with PoCs

Use the testing tools to write targeted PoCs for any findings:
- **LiteSVM** — Fast in-process execution for exploit PoCs (seconds, not minutes)
- **Mollusk** — Direct program execution for CU impact analysis
- **Surfpool** — Integration testing against real mainnet state (Jupiter, Orca, etc.)

See [Solana Testing for Auditors](resources/solana-testing-for-auditors.md) for setup guides.

### Step 7: Deliverables

For each finding, provide:
- **Vulnerability category** (from the 9 categories above)
- **Affected instruction(s)** with account layout
- **Exploit scenario** — step-by-step attack using concrete accounts
- **PoC code** (if applicable) using LiteSVM or Mollusk
- **Fix recommendation** with Anchor and/or native Rust code
- **Risk notes** for anything touching signing, fees, CPIs, or token transfers

## Workflows

| Workflow | Description |
|----------|-------------|
| [Anchor Audit](workflows/anchor-audit.md) | Audit workflow for Anchor framework programs — constraint validation, CPI safety, PDA verification |
| [Native Audit](workflows/native-audit.md) | Audit workflow for native Solana programs — manual account deserialization, raw instruction processing |

## Resources

| Resource | Description |
|----------|-------------|
| [Account Validation](resources/account-validation.md) | Complete guide to account validation checks: signer, owner, PDA, type, uniqueness |
| [Anchor Security](resources/anchor-security.md) | Anchor-specific security patterns: constraints, CPI, init_if_needed, close |
| [Solana Patterns](resources/solana-patterns.md) | Common vulnerability patterns with code examples and fixes |
| [Curated Links](resources/curated-links.md) | 50+ curated links to official docs, audit reports, security courses, tools, and firms |
| [Security Fundamentals](resources/security-fundamentals.md) | Core Solana security principles, threat model, and best practices |
| [Native Security](resources/native-security.md) | Native Solana (non-Anchor) security patterns and pitfalls |
| [Security Checklists](resources/security-checklists.md) | Audit and client-side checklists for Solana programs |
| [Caveats](resources/caveats.md) | Solana-specific caveats, gotchas, and edge cases for auditors |
| [Formal Verification](resources/formal-verification-for-auditors.md) | Kani proof evaluation: classification, property categories, verify module extract-and-prove pattern |
| [Adversarial Test Design](resources/adversarial-test-design.md) | Attack-first test taxonomy, conservation invariant methodology, 10-category checklist |

## Notable Solana Security Incidents

| Incident | Date | Root Cause | Loss |
|----------|------|-----------|------|
| Wormhole bridge | Feb 2022 | Missing signer verification on `complete_wrapped` | $326M |
| Cashio stablecoin | Mar 2022 | Missing `crate_collateral_tokens.mint` validation | $52M |
| Mango Markets | Oct 2022 | Oracle price manipulation + account borrowing | $116M |
| Crema Finance | Jul 2022 | Fake tick account injection in CPI | $8.8M |
| Slope wallet | Aug 2022 | Private key logging in centralized server | $4.1M |
| Solend | Various | Multiple oracle and liquidation issues | Various |

## Ecosystem Context

| Metric | Value |
|--------|-------|
| Smart contract language | Rust |
| Primary framework | Anchor (>90% of new projects) |
| Block time | ~400ms |
| Transaction model | Multiple instructions per transaction |
| Account size limit | 10MB |
| Compute budget | 200,000 compute units per instruction (adjustable to 1.4M) |
| Token standard | SPL Token / Token-2022 |
| NFT standard | Metaplex Token Metadata |

## Integration with Other Skills

| Skill | Connection |
|-------|-----------|
| `patterns/` | Cross-reference Solana-specific patterns with Solodit database (limited but growing) |
| `exploit-forensics/` | Wormhole, Cashio, Mango exploits provide forensic case studies |
| `chain-guides/solana.md` | Chain-level context for Solana validator behavior, consensus, fees |
| `attack-trees/` | Solana-specific attack trees (account confusion, CPI escalation) |

## Error Code Reference

Common Solana program error codes encountered during audits. These appear in transaction logs and simulation failures.

### Anchor Framework Errors

| Error Code | Error Name | Meaning |
|------------|-----------|----------|
| `0x64` (100) | `InstructionMissing` | Expected instruction not found in transaction |
| `0x65` (101) | `InstructionFallbackNotFound` | No fallback handler for instruction |
| `0xBB8` (3000) | `ConstraintMut` | Account not marked as mutable (`#[account(mut)]` missing) |
| `0xBB9` (3001) | `ConstraintHasOne` | `has_one` constraint failed — account field doesn't match |
| `0xBBA` (3002) | `ConstraintSigner` | Account is not a signer |
| `0xBBB` (3003) | `ConstraintRaw` | Custom `constraint = <expr>` evaluated to false |
| `0xBBC` (3004) | `ConstraintOwner` | Account owner does not match expected program |
| `0xBBF` (3007) | `ConstraintSeeds` | PDA seeds do not derive the expected address |
| `0xBC4` (3012) | `ConstraintSpace` | Account data space insufficient |
| `0x7D0` (2000) | `DeclaredProgramIdMismatch` | `declare_id!` does not match actual program ID |
| `0x7D1` (2001) | `TryingToInitPayerAsProgramAccount` | Payer account reused as program-owned account |
| `0xBCE` (3022) | `AccountNotInitialized` | Account data is empty / uninitialized |
| `0xBC0` (3008) | `ConstraintExecutable` | Account is not an executable program |
| `0x1770` (6000)+ | Custom errors | Application-specific errors start at 6000 |

### SPL Token Program Errors

| Error Code | Error Name | Meaning |
|------------|-----------|----------|
| `0x0` | `NotRentExempt` | Account balance below rent-exempt minimum |
| `0x1` | `InsufficientFunds` | Token balance too low for transfer |
| `0x3` | `InvalidMint` | Token account mint does not match expected mint |
| `0x4` | `MintMismatch` | Mint of token account does not match instruction mint |
| `0x5` | `OwnerMismatch` | Token account owner does not match expected owner |
| `0xA` | `AlreadyInUse` | Account is already initialized |
| `0xC` | `InvalidNumberOfProvidedSigners` | Wrong number of multisig signers |
| `0xD` | `InvalidNumberOfRequiredSigners` | Invalid multisig threshold |
| `0x11` | `AccountFrozen` | Token account is frozen — transfers blocked |

### System Program / Runtime Errors

| Error Code | Error Name | Meaning |
|------------|-----------|----------|
| `0x0` | `InsufficientFundsForRent` | Account will drop below rent-exempt after operation |
| `0x1` | `AccountAlreadyInitialized` | Cannot reinitialize existing account |
| `0x3` | `AccountNotFound` | Referenced account does not exist |
| `ProgramFailedToComplete` | (Runtime) | Program exceeded compute budget or panicked |
| `PrivilegeEscalation` | (Runtime) | CPI attempted to escalate privileges |
| `AccountDataTooSmall` | (Runtime) | Account data buffer too small for deserialization |

## Troubleshooting

| Issue | Likely Cause | Solution |
|-------|-------------|----------|
| Scanner misses missing-signer vulnerabilities | Native program uses `AccountInfo` without Anchor constraints | Check all `AccountInfo` params for explicit `is_signer` / `is_writable` validation |
| False positive on PDA seeds | Scanner flags all user-controlled seeds | Verify if seeds are bounded by program logic; canonical bump stored correctly |
| Account confusion not detected | Different account types share same structure size | Check discriminator bytes; Anchor auto-adds 8-byte discriminators |
| CPI privilege escalation missed | `invoke_signed` seeds not analyzed | Manually trace PDA seed derivation through CPI chain |
| Scanner doesn't flag overflow in release mode | Release builds wrap instead of panic | Flag all non-`checked_*` math ops; verify `overflow-checks = true` in Cargo.toml |
| Duplicate account injection not caught | Scanner doesn't check account uniqueness | Verify all instruction accounts are compared for uniqueness where semantically distinct |
