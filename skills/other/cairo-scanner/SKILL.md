---
id: SCANNER-CAIRO
title: Cairo Smart Contract Security Scanner
category: chain-scanner
chains: [starknet]
languages: [cairo]
version: cairo-2.x
last_updated: 2026-02-24
description: >-
  Use when the user wants to audit Cairo smart contracts for security
  vulnerabilities, scan Starknet contracts for felt overflow, storage collision,
  or account abstraction issues, review Cairo 2.x contracts for component
  architecture flaws, or analyze STARK-based protocols for cryptographic and
  computational errors.
---

# Cairo Scanner Skill

## Purpose

Analyze Cairo smart contracts deployed on Starknet for security vulnerabilities. Cairo's unique computational model — based on field elements (felts), STARK proofs, and native account abstraction — creates attack surfaces that don't exist on EVM chains.

## Cairo Security Model

| Property | Cairo/Starknet | EVM/Solidity |
|----------|---------------|-------------|
| Integer type | Felt252 (field element, $0$ to $P-1$ where $P = 2^{251} + 17 \cdot 2^{192} + 1$) | uint256, int256 |
| Arithmetic | Modular (wraps around $P$) | Checked (reverts in Solidity 0.8+) |
| Division | Modular inverse (not integer division) | Integer truncation |
| Account model | All accounts are smart contracts (native AA) | EOAs + smart contracts |
| Upgrades | `replace_class_syscall` (instant) | Proxy patterns (delegatecall) |
| Storage | Pedersen hash-based addresses | Sequential slots (keccak256) |
| L1 interaction | L1-L2 messaging via Starknet Core on Ethereum | Bridges required |
| Proving | STARK proofs for L1 verification | No proofs needed |

## Detection Capabilities

### Critical — Direct Fund Loss

| Vulnerability | Description | Detection Signal |
|---------------|-------------|-----------------|
| **Felt overflow wrapping** | Arithmetic on felt252 wraps around $P$, enabling underflow/overflow | Felt252 used for balances or amounts without range checks |
| **Unprotected `replace_class_syscall`** | Anyone can upgrade the contract logic | `replace_class_syscall` without `assert_only_owner` or equivalent |
| **L1-L2 message replay** | Same L1→L2 message consumed multiple times | Missing nonce or message hash tracking in `l1_handler` |
| **Account validation bypass** | Custom `__validate__` skips critical checks | `__validate__` returns success without signature verification |
| **Storage collision** | Two different state variables map to same storage slot | Custom `storage_address_from_base` with colliding inputs |

### High — Significant Impact

| Vulnerability | Description | Detection Signal |
|---------------|-------------|-----------------|
| **Reentrancy via `call_contract_syscall`** | External contract call re-enters before state update | `call_contract_syscall` before storage writes |
| **Missing caller validation** | External function callable by anyone | `get_caller_address()` not checked in sensitive functions |
| **Felt252 comparison pitfalls** | Comparing felts that represent "negative" numbers (near $P$) | `<` or `>` on felts where semantic negativity matters |
| **Component storage isolation failure** | Components sharing storage addresses | Overlapping `#[storage]` declarations across components |
| **Incorrect modular division** | Using `/` operator expecting integer division | `a / b` on felt252 produces modular inverse, not truncation |

### Medium — Conditional Impact

| Vulnerability | Description | Detection Signal |
|---------------|-------------|-----------------|
| **Unbounded storage growth** | Maps or arrays without size limits | `Map<K, V>` without pruning mechanism |
| **Missing events** | State changes without event emission | `write` to storage without `emit` |
| **Library dispatch trust** | Using `library_call_syscall` with unchecked class hash | External class hash in library call |
| **Paymaster manipulation** | Transaction fee payment logic exploitable | Custom `__validate__` with fee token handling |
| **Felt-to-u256 conversion errors** | Incorrect type casting between felt and uint types | `felt252.into()` or `TryInto::<u256>` without bounds |

## Cairo-Specific Pitfalls

### Felt Arithmetic Is Modular

```cairo
// DANGEROUS: Felt subtraction wraps around P
let balance: felt252 = 100;
let amount: felt252 = 200;
let result = balance - amount;
// result is NOT -100, it is P - 100 (a very large number)
// Any comparison result > 0 will be TRUE

// SAFE: Use u256 for amounts
let balance: u256 = 100;
let amount: u256 = 200;
assert(balance >= amount, 'Insufficient balance'); // Correctly reverts
```

### Division Is Not Integer Division

```cairo
// UNEXPECTED: Felt division is modular inverse
let a: felt252 = 7;
let b: felt252 = 2;
let result = a / b;
// result is NOT 3 (integer truncation)
// result is the felt252 x such that x * 2 ≡ 7 (mod P)
// This is (P + 7) / 2 = a very large number

// SAFE: Use u256 for integer division
let a: u256 = 7;
let b: u256 = 2;
let result = a / b; // result is 3 (integer truncation, as expected)
```

## Resources

| Resource | Description |
|----------|-------------|
| [Cairo Patterns](resources/cairo-patterns.md) | Vulnerability patterns specific to Cairo language and Starknet |
| [Starknet Security](resources/starknet-security.md) | Starknet architecture security: sequencer, proofs, upgrades |
| [Messaging Security](resources/messaging-security.md) | L1-L2 messaging: message replay, nonce handling, proof finalization |

## Workflows

| Workflow | Description |
|----------|-------------|
| [Cairo Audit](workflows/cairo-audit.md) | Step-by-step audit workflow for Cairo contracts on Starknet |

## Notable Starknet Security Incidents

| Incident | Root Cause | Impact |
|----------|-----------|--------|
| Various DeFi exploits on Starknet testnet | Felt overflow in token balances | Fund inflation |
| L1→L2 message replay in early bridges | Missing consumed message tracking | Double-spending |
| Account contract vulnerabilities | Insufficient `__validate__` logic | Transaction forging |

## Integration with Other Skills

| Skill | Connection |
|-------|-----------|
| `starknet-scanner/` | Shares Cairo language patterns; this skill focuses on language, starknet-scanner focuses on chain |
| `chain-guides/starknet.md` | Chain-level context for Starknet architecture |
| `patterns/` | Cross-reference with general vulnerability categories (reentrancy, access control) |
| `exploit-forensics/` | Limited Starknet exploits but growing as ecosystem matures |

## Error Code Reference

Common Cairo/Starknet errors encountered during audits. Cairo errors manifest as felt252 values in transaction reverts.

### Cairo Language Errors

| Error Pattern | Error Source | Meaning |
|--------------|-------------|----------|
| `felt252 overflow` | Arithmetic operation | Result exceeds field prime P (≈ 2^251 + 17·2^192 + 1) — wraps silently |
| `index out of bounds` | Array access | Array index exceeds length — causes execution failure |
| `Option::unwrap on None` | Option handling | Attempted to unwrap an empty Option — missing existence check |
| `assertion failed` | `assert()` macro | Contract invariant violation — check assert conditions |
| `'Entry not found'` | StorageMap access | Key does not exist in LegacyMap/Map — missing default handling |
| `u256_sub Overflow` | Subtraction underflow | Unsigned subtraction result would be negative |
| `u256_add Overflow` | Addition overflow | Addition exceeds u256 max value |
| `Division by zero` | Division operation | Denominator is zero — missing zero-check |

### Starknet Contract Errors

| Error Pattern | Error Source | Meaning |
|--------------|-------------|----------|
| `'Caller is not the owner'` | OZ Ownable | Missing ownership — check access control |
| `'Caller is the zero address'` | OZ Ownable | Zero address caller — validate caller identity |
| `'ERC20: insufficient balance'` | OZ ERC20 | Token balance too low |
| `'ERC20: insufficient allowance'` | OZ ERC20 | Approval not set or insufficient |
| `'ERC20: approve to zero address'` | OZ ERC20 | Invalid spender address |
| `'ERC721: invalid token ID'` | OZ ERC721 | Token does not exist |
| `'Contract already initialized'` | Initializable pattern | Re-initialization attempt — check initializer guard |
| `'ENTRYPOINT_NOT_FOUND'` | Starknet OS | Called selector doesn't exist on contract |
| `'UNINITIALIZED_CONTRACT'` | Starknet OS | Class not declared or deployed |
| `'TRANSACTION_FAILED'` | Starknet sequencer | Generic failure — check inner error for details |

### Felt Arithmetic Audit Concerns

| Issue | Risk | Detection |
|-------|------|----------|
| Felt overflow wrapping | Arithmetic wraps mod P instead of reverting | Flag all felt252 math ops — prefer u256/u128 for financial math |
| Felt comparison edge cases | `<` and `>` comparisons are mod P, not natural ordering | Check comparisons on felt252 values — may produce unexpected results |
| Integer to felt truncation | Converting large u256 to felt252 silently truncates | Flag all `into()` / `try_into()` conversions between types |
| Storage key collision | LegacyMap keys hash via Pedersen — potential collision with crafted inputs | Verify map key uniqueness assumptions |

## Troubleshooting

| Issue | Likely Cause | Solution |
|-------|-------------|----------|
| Scanner misses felt overflow issues | Analyzing code as if integers revert on overflow | Cairo felt252 wraps mod P — flag all felt arithmetic in financial logic |
| False positives on storage access | Scanner flags all LegacyMap reads as risky | Verify if default value (0) is safe for the use case |
| Account abstraction patterns not detected | Scanner uses EVM mental model | Load `starknet-scanner/` for account abstraction-specific checks |
| Component architecture flaws missed | Scanner doesn't understand Cairo components | Manually review component trait implementations and storage conflicts |
| Missed reentrancy via L1 handler | Scanner only checks external functions | Include `#[l1_handler]` functions in reentrancy analysis |
| Cairo version mismatch warnings | Pattern written for Cairo 1.x, contract uses 2.x | Verify syntax patterns match target Cairo version; update detection rules |
