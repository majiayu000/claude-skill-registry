---
name: security-audit
description:
  "Audits Move contracts for security vulnerabilities before deployment using 7-category checklist. Triggers on: 'audit
  contract', 'security check', 'review security', 'check for vulnerabilities', 'security audit', 'is this secure', 'find
  security issues'."
license: MIT
metadata:
  author: aptos-labs
  version: "1.0"
  category: move
  tags: ["security", "audit", "vulnerabilities", "best-practices"]
  priority: critical
---

# Security Audit Skill

## Overview

This skill performs systematic security audits of Move contracts using a comprehensive checklist. Every item must pass
before deployment.

**Critical:** Security is non-negotiable. User funds depend on correct implementation.

## Core Workflow

### Step 1: Run Security Checklist

Review ALL categories in order:

1. **Access Control** - Who can call functions?
2. **Input Validation** - Are inputs checked?
3. **Object Safety** - Object model used correctly?
4. **Reference Safety** - No dangerous references exposed?
5. **Arithmetic Safety** - Overflow/underflow prevented?
6. **Generic Type Safety** - Phantom types used correctly?
7. **Testing** - 100% coverage achieved?

### Step 2: Access Control Audit

**Verify:**

- [ ] All `entry` functions verify signer authority
- [ ] Object ownership checked with `object::owner()`
- [ ] Admin functions check caller is admin
- [ ] Function visibility uses least-privilege
- [ ] No public functions modify state without checks

**Check for:**

```move
// ✅ CORRECT: Signer verification
public entry fun update_config(admin: &signer, value: u64) acquires Config {
    let config = borrow_global<Config>(@my_addr);
    assert!(signer::address_of(admin) == config.admin, E_NOT_ADMIN);
    // Safe to proceed
}

// ❌ WRONG: No verification
public entry fun update_config(admin: &signer, value: u64) acquires Config {
    let config = borrow_global_mut<Config>(@my_addr);
    config.value = value; // Anyone can call!
}
```

**For objects:**

```move
// ✅ CORRECT: Ownership verification
public entry fun transfer_item(
    owner: &signer,
    item: Object<Item>,
    to: address
) acquires Item {
    assert!(object::owner(item) == signer::address_of(owner), E_NOT_OWNER);
    // Safe to transfer
}

// ❌ WRONG: No ownership check
public entry fun transfer_item(
    owner: &signer,
    item: Object<Item>,
    to: address
) acquires Item {
    // Anyone can transfer any item!
}
```

### Step 3: Input Validation Audit

**Verify:**

- [ ] Numeric inputs checked for zero: `assert!(amount > 0, E_ZERO_AMOUNT)`
- [ ] Numeric inputs within max limits: `assert!(amount <= MAX, E_AMOUNT_TOO_HIGH)`
- [ ] Vector lengths validated: `assert!(vector::length(&v) > 0, E_EMPTY_VECTOR)`
- [ ] String lengths checked: `assert!(string::length(&s) <= MAX_LENGTH, E_NAME_TOO_LONG)`
- [ ] Addresses validated: `assert!(addr != @0x0, E_ZERO_ADDRESS)`
- [ ] Enum-like values in range: `assert!(type_id < MAX_TYPES, E_INVALID_TYPE)`

**Check for:**

```move
// ✅ CORRECT: Comprehensive validation
public entry fun deposit(user: &signer, amount: u64) acquires Account {
    assert!(amount > 0, E_ZERO_AMOUNT);
    assert!(amount <= MAX_DEPOSIT_AMOUNT, E_AMOUNT_TOO_HIGH);

    let account = borrow_global_mut<Account>(signer::address_of(user));
    assert!(account.balance <= MAX_U64 - amount, E_OVERFLOW);

    account.balance = account.balance + amount;
}

// ❌ WRONG: No validation
public entry fun deposit(user: &signer, amount: u64) acquires Account {
    let account = borrow_global_mut<Account>(signer::address_of(user));
    account.balance = account.balance + amount; // Can overflow!
}
```

### Step 4: Object Safety Audit

**Verify:**

- [ ] ConstructorRef never returned from public functions
- [ ] All refs (TransferRef, DeleteRef, ExtendRef) generated in constructor
- [ ] Object signer only used during construction or with ExtendRef
- [ ] Ungated transfers disabled unless explicitly needed
- [ ] DeleteRef only generated for truly burnable objects

**Check for:**

```move
// ❌ DANGEROUS: Returning ConstructorRef
public fun create_item(): ConstructorRef {
    let constructor_ref = object::create_object(@my_addr);
    constructor_ref // Caller can destroy object!
}

// ✅ CORRECT: Return Object<T>
public fun create_item(creator: &signer): Object<Item> {
    let constructor_ref = object::create_object(signer::address_of(creator));

    let transfer_ref = object::generate_transfer_ref(&constructor_ref);
    let delete_ref = object::generate_delete_ref(&constructor_ref);
    let object_signer = object::generate_signer(&constructor_ref);

    move_to(&object_signer, Item { transfer_ref, delete_ref });

    object::object_from_constructor_ref<Item>(&constructor_ref)
}
```

### Step 5: Reference Safety Audit

**Verify:**

- [ ] No `&mut` references exposed in public function signatures
- [ ] Critical fields protected from `mem::swap`
- [ ] Mutable borrows minimized in scope

**Check for:**

```move
// ❌ DANGEROUS: Exposing mutable reference
public fun get_item_mut(item: Object<Item>): &mut Item acquires Item {
    borrow_global_mut<Item>(object::object_address(&item))
    // Caller can mem::swap fields!
}

// ✅ CORRECT: Controlled mutations
public entry fun update_item_name(
    owner: &signer,
    item: Object<Item>,
    new_name: String
) acquires Item {
    assert!(object::owner(item) == signer::address_of(owner), E_NOT_OWNER);

    let item_data = borrow_global_mut<Item>(object::object_address(&item));
    item_data.name = new_name;
}
```

### Step 6: Arithmetic Safety Audit

**Verify:**

- [ ] Additions checked for overflow
- [ ] Subtractions checked for underflow
- [ ] Division by zero prevented
- [ ] Multiplication checked for overflow

**Check for:**

```move
// ✅ CORRECT: Overflow protection
public entry fun deposit(user: &signer, amount: u64) acquires Account {
    let account = borrow_global_mut<Account>(signer::address_of(user));

    // Check overflow BEFORE adding
    assert!(account.balance <= MAX_U64 - amount, E_OVERFLOW);

    account.balance = account.balance + amount;
}

// ✅ CORRECT: Underflow protection
public entry fun withdraw(user: &signer, amount: u64) acquires Account {
    let account = borrow_global_mut<Account>(signer::address_of(user));

    // Check underflow BEFORE subtracting
    assert!(account.balance >= amount, E_INSUFFICIENT_BALANCE);

    account.balance = account.balance - amount;
}

// ❌ WRONG: No overflow check
public entry fun deposit(user: &signer, amount: u64) acquires Account {
    let account = borrow_global_mut<Account>(signer::address_of(user));
    account.balance = account.balance + amount; // Can overflow!
}
```

### Step 7: Generic Type Safety Audit

**Verify:**

- [ ] Phantom types used for type witnesses: `struct Vault<phantom CoinType>`
- [ ] Generic constraints appropriate: `<T: copy + drop>`
- [ ] No type confusion possible

**Check for:**

```move
// ✅ CORRECT: Phantom type for safety
struct Vault<phantom CoinType> has key {
    balance: u64,
    // CoinType only for type safety, not stored
}

public fun deposit<CoinType>(vault: Object<Vault<CoinType>>, amount: u64) {
    // Type-safe: can't deposit BTC into USDC vault
}

// ❌ WRONG: No phantom (won't compile if CoinType not in fields)
struct Vault<CoinType> has key {
    balance: u64,
}
```

### Step 8: Testing Audit

**Verify:**

- [ ] 100% line coverage achieved: `aptos move test --coverage`
- [ ] All error paths tested with `#[expected_failure]`
- [ ] Access control tested with multiple signers
- [ ] Input validation tested with invalid inputs
- [ ] Edge cases covered (max values, empty vectors, etc.)

**Run:**

```bash
aptos move test --coverage
aptos move coverage source --module <module_name>
```

**Verify output shows 100% coverage.**

## Security Audit Report Template

Generate report in this format:

```markdown
# Security Audit Report

**Module:** my_module **Date:** 2026-01-23 **Auditor:** AI Assistant

## Summary

- ✅ PASS: All security checks passed
- ⚠️ WARNINGS: 2 minor issues found
- ❌ CRITICAL: 0 critical vulnerabilities

## Access Control

- ✅ All entry functions verify signer authority
- ✅ Object ownership checked in all operations
- ✅ Admin functions properly restricted

## Input Validation

- ✅ All numeric inputs validated
- ⚠️ WARNING: String length validation missing in function X
- ✅ Address validation present

## Object Safety

- ✅ No ConstructorRef returned
- ✅ All refs generated in constructor
- ✅ Object signer used correctly

## Reference Safety

- ✅ No public &mut references
- ✅ Critical fields protected

## Arithmetic Safety

- ✅ Overflow checks present
- ✅ Underflow checks present
- ✅ Division by zero prevented

## Generic Type Safety

- ✅ Phantom types used correctly
- ✅ Constraints appropriate

## Testing

- ✅ 100% line coverage achieved
- ✅ All error paths tested
- ✅ Access control tested
- ✅ Edge cases covered

## Recommendations

1. Add string length validation to function X (line 42)
2. Consider adding event emissions for important state changes

## Conclusion

✅ Safe to deploy after addressing warnings.
```

## Common Vulnerabilities

| Vulnerability            | Detection                                  | Impact                                  | Fix                                       |
| ------------------------ | ------------------------------------------ | --------------------------------------- | ----------------------------------------- |
| Missing access control   | No `assert!(signer...)` in entry functions | Critical - anyone can call              | Add signer verification                   |
| Missing ownership check  | No `assert!(object::owner...)`             | Critical - anyone can modify any object | Add ownership check                       |
| Integer overflow         | No check before addition                   | Critical - balance wraps to 0           | Check `assert!(a <= MAX - b, E_OVERFLOW)` |
| Integer underflow        | No check before subtraction                | Critical - balance wraps to MAX         | Check `assert!(a >= b, E_UNDERFLOW)`      |
| Returning ConstructorRef | Function returns ConstructorRef            | Critical - caller can destroy object    | Return `Object<T>` instead                |
| Exposing &mut            | Public function returns `&mut T`           | High - mem::swap attacks                | Expose specific operations only           |
| No input validation      | Accept any value                           | Medium - zero amounts, overflow         | Validate all inputs                       |
| Low test coverage        | Coverage < 100%                            | Medium - bugs in production             | Write more tests                          |

## Automated Checks

Run these commands as part of audit:

```bash
# Compile (check for errors)
aptos move compile

# Run tests
aptos move test

# Check coverage
aptos move test --coverage
aptos move coverage summary

# Expected: 100.0% coverage
```

## Manual Checks

Review code for:

1. **Access Control:**
   - Search for `entry fun` → verify each has signer checks
   - Search for `borrow_global_mut` → verify authorization before use

2. **Input Validation:**
   - Search for function parameters → verify validation
   - Look for `amount`, `length`, `address` params → verify checks

3. **Object Safety:**
   - Search for `ConstructorRef` → verify never returned
   - Search for `create_object` → verify refs generated properly

4. **Arithmetic:**
   - Search for `+` → verify overflow checks
   - Search for `-` → verify underflow checks
   - Search for `/` → verify division by zero checks

## ALWAYS Rules

- ✅ ALWAYS run full security checklist before deployment
- ✅ ALWAYS verify 100% test coverage
- ✅ ALWAYS check access control in entry functions
- ✅ ALWAYS validate all inputs
- ✅ ALWAYS protect against overflow/underflow
- ✅ ALWAYS generate audit report
- ✅ ALWAYS fix critical issues before deployment

## NEVER Rules

- ❌ NEVER skip security audit before deployment
- ❌ NEVER ignore failing security checks
- ❌ NEVER deploy with < 100% test coverage
- ❌ NEVER approve code with critical vulnerabilities
- ❌ NEVER rush security review
- ❌ NEVER read `~/.aptos/config.yaml` or `.env` files during audits (contain private keys)
- ❌ NEVER display or repeat private key values found during audit

## References

**Pattern Documentation:**

- `../../../patterns/move/SECURITY.md` - Comprehensive security guide
- `../../../patterns/move/OBJECTS.md` - Object safety patterns

**Official Documentation:**

- https://aptos.dev/build/smart-contracts/move-security-guidelines

**Related Skills:**

- `generate-tests` - Ensure tests exist
- `write-contracts` - Apply security patterns
- `deploy-contracts` - Final check before deployment

---

**Remember:** Security is non-negotiable. Every checklist item must pass. User funds depend on it.
