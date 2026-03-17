---
id: APTOS-SCAN
title: Aptos Specialized Scanner
category: chain-scanner
trigger: "Audit Aptos|Aptos Move"
last_updated: 2026-02-24
description: >-
  Use when the user wants to audit Aptos Move smart contracts, scan
  Aptos-specific patterns including global storage model, resource accounts, or
  coin modules, review Aptos DeFi protocols for framework module interaction
  vulnerabilities, or analyze Aptos-specific upgrade and governance patterns.
---

# Aptos Specialized Scanner

Specialized security scanner for Aptos Move smart contracts. Extends the general [Move Scanner](../move-scanner/SKILL.md) with Aptos-specific patterns, framework modules, and the global storage model.

---

## Why a Separate Aptos Scanner?

While the Move Scanner covers language-level patterns shared between Aptos and Sui, Aptos has a fundamentally different **storage model** (global resources under addresses), **framework** (AptosFramework), and **upgrade system** that require dedicated detection rules.

| Feature | Aptos | Sui |
|---------|-------|-----|
| Storage | Global resources under addresses | Object model |
| Resource access | `move_to`, `borrow_global`, `move_from` | Passed as function parameters |
| Upgrade | Module upgrade with compatibility policy | Package upgrade with UpgradeCap |
| Tokens | `aptos_framework::coin` | `sui::coin` with TreasuryCap |
| Accounts | Account + AuthenticationKey | No account concept |
| Randomness | `aptos_framework::randomness` (commit-reveal) | `sui::random` |

---

## Detection Capabilities

| Category | Detection | Severity |
|----------|-----------|----------|
| **Resource Safety** | Resource created but never stored (`move_to` missing) | High |
| **Resource Safety** | `borrow_global_mut` without authorization check | Critical |
| **Resource Safety** | `move_from` extracting resource without ownership proof | Critical |
| **Resource Safety** | Missing `exists<T>(addr)` check before access | Medium |
| **Abilities** | Value-holding type with `copy` ability (duplication) | Critical |
| **Abilities** | Capability with `drop` (can be silently discarded) | High |
| **Upgrade** | Module upgrade authority is single EOA | High |
| **Upgrade** | `compatible` upgrade policy on critical module | Medium |
| **Coin** | `MintCapability` stored in publicly accessible location | Critical |
| **Coin** | `CoinStore` registration not checked before deposit | Medium |
| **Auth** | Missing `signer` parameter on privileged entry function | Critical |
| **Auth** | `signer::address_of()` not compared to authorized address | High |
| **Auth** | Resource account `SignerCapability` exposed publicly | Critical |
| **Storage** | `Table`/`SimpleMap` with unbounded growth | Medium |
| **Storage** | `acquires` annotation missing (compile-time, but indicates design) | Low |
| **Events** | State change without event emission | Low |

---

## Aptos Framework Security-Critical Modules

| Module | Functions to Audit | Key Risk |
|--------|--------------------|----------|
| `aptos_framework::coin` | `initialize`, `mint`, `burn`, `transfer`, `register` | Cap management |
| `aptos_framework::account` | `create_account`, `rotate_authentication_key` | Auth key rotation |
| `aptos_framework::resource_account` | `create_resource_account`, `retrieve_resource_account_cap` | Signer cap leak |
| `aptos_framework::object` | `create_object`, `transfer`, `generate_signer` | Object ownership |
| `aptos_framework::fungible_asset` | `mint`, `burn`, `transfer`, `deposit`, `withdraw` | New token standard |
| `aptos_framework::multisig_account` | `create`, `execute_transaction` | Multisig logic |
| `aptos_framework::staking_contract` | `create_staking_contract`, `distribute` | Reward calculation |
| `aptos_framework::governance` | `create_proposal`, `vote` | Voting power |

---

## Common Aptos Vulnerability Examples

### Resource Account Signer Capability Leak

```move
// CRITICAL: SignerCapability stored with 'store' ability allows extraction
struct ResourceAccountCap has key, store {
    signer_cap: account::SignerCapability,
}

// If anyone can get a reference to this struct, they can create a signer
// for the resource account and drain all its assets
public fun get_resource_signer(cap: &ResourceAccountCap): signer {
    account::create_signer_with_capability(&cap.signer_cap)
}

// SAFE: No public accessor, internal only
struct ResourceAccountCap has key {
    signer_cap: account::SignerCapability,
}

fun internal_get_signer() acquires ResourceAccountCap {
    let cap = borrow_global<ResourceAccountCap>(@resource_addr);
    let signer = account::create_signer_with_capability(&cap.signer_cap);
    // Use signer internally only
}
```

### Coin Registration Race Condition

```move
// VULNERABLE: Depositing without checking CoinStore registration
public fun distribute_rewards(recipients: &vector<address>) {
    let i = 0;
    while (i < vector::length(recipients)) {
        let addr = *vector::borrow(recipients, i);
        // ABORTS if addr doesn't have CoinStore<RewardToken> registered!
        coin::deposit(addr, reward_coins);
        i = i + 1;
    };
}

// SAFE: Check registration first
public fun distribute_rewards(recipients: &vector<address>) {
    let i = 0;
    while (i < vector::length(recipients)) {
        let addr = *vector::borrow(recipients, i);
        if (coin::is_account_registered<RewardToken>(addr)) {
            coin::deposit(addr, reward_coins);
        } else {
            // Handle: skip, queue for later, or register for them
        };
        i = i + 1;
    };
}
```

---

## Resources
- [Aptos Patterns](resources/aptos-patterns.md)

## Workflows
- [Aptos Audit](workflows/aptos-audit.md)

## See Also
- [Move Scanner](../move-scanner/SKILL.md) for general Move patterns
- [Chain Guide: Aptos](../chain-guides/aptos.md) for chain-specific context

## Error Code Reference

Aptos-specific error codes and framework abort codes. Aptos uses the Move abort system with standard error categories.

### Aptos Error Categories (std::error)

| Category | Constant | Hex Prefix | Meaning |
|----------|---------|-----------|----------|
| `INVALID_ARGUMENT` | `1` | `0x1____` | Bad input parameter |
| `OUT_OF_RANGE` | `2` | `0x2____` | Value outside acceptable range |
| `NOT_FOUND` | `6` | `0x6____` | Resource or item not found |
| `ALREADY_EXISTS` | `8` | `0x8____` | Resource or item already exists |
| `PERMISSION_DENIED` | `5` | `0x5____` | Insufficient permissions |
| `RESOURCE_EXHAUSTED` | `9` | `0x9____` | Limit reached (e.g., max supply) |
| `UNAVAILABLE` | `13` | `0xD____` | Temporarily unavailable |

### Aptos Framework Errors

| Abort Code | Module | Meaning |
|-----------|--------|----------|
| `0x10006` | `coin` | Coin store not registered for address |
| `0x10007` | `coin` | Insufficient coin balance |
| `0x80001` | `account` | Account already exists |
| `0x80002` | `account` | Account not found |
| `0x50001` | `table` | Key already exists |
| `0x50002` | `table` | Key not found |
| `0x60001` | `coin` | Coin amount is zero |
| `0x90001` | `resource_account` | Resource account already exists |
| `ENOT_OWNER` | Common | Signer is not the owner — access control check |
| `ENOT_AUTHORIZED` | Common | Lacking required authorization |

### Aptos Token / NFT Errors

| Abort Code | Module | Meaning |
|-----------|--------|----------|
| `ETOKEN_NOT_FOUND` | `token` | Token or collection does not exist |
| `ECOLLECTION_NOT_FOUND` | `token` | Collection does not exist |
| `EINSUFFICIENT_BALANCE` | `token` | Token balance too low for operation |
| `ENOT_CREATOR` | `token` | Caller is not the collection creator |
| `EFIELD_NOT_MUTABLE` | `token` | Attempting to modify immutable field |

## Troubleshooting

| Issue | Likely Cause | Solution |
|-------|-------------|----------|
| Global storage vulnerabilities missed | Scanner doesn't audit `borrow_global` / `move_to` patterns | Map all global storage operations; check `exists<T>` before `borrow_global` and `move_to` |
| Resource account risks not flagged | Scanner doesn't track `SignerCapability` lifecycle | Trace `resource_account::create_resource_account` and verify `SignerCapability` storage/access |
| Module upgrade attack surface ignored | Scanner only checks current code | Verify `UpgradePolicy` (immutable vs compatible); check who holds the `UpgradeCap` |
| View functions not audited | Scanner focuses on entry functions | View functions can leak sensitive state; audit all `#[view]` functions for information disclosure |
| Event emission gaps not detected | Scanner doesn't check event coverage | Verify all state-changing operations emit events for off-chain tracking |
| Coin type confusion not caught | Scanner trusts Move type system | Verify all coin operations use correct type parameters; check for `CoinType` aliasing |
