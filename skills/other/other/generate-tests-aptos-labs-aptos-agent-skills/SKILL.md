---
name: generate-tests
description:
  "Creates comprehensive test suites for Move contracts with 100% coverage requirement. Triggers on: 'generate tests',
  'create tests', 'write test suite', 'test this contract', 'how to test', 'add test coverage', 'write unit tests'."
license: MIT
metadata:
  author: aptos-labs
  version: "1.0"
  category: move
  tags: ["testing", "unit-tests", "coverage", "quality"]
  priority: critical
---

# Generate Tests Skill

## Overview

This skill generates comprehensive test suites for Move contracts with **100% line coverage** requirement. Tests verify:

- ✅ Happy paths (functionality works)
- ✅ Access control (unauthorized users blocked)
- ✅ Input validation (invalid inputs rejected)
- ✅ Edge cases (boundaries, limits, empty states)

**Critical Rule:** NEVER deploy without 100% test coverage.

## Core Workflow

### Step 1: Create Test Module

```move
#[test_only]
module my_addr::my_module_tests {
    use my_addr::my_module::{Self, MyObject};
    use aptos_framework::object::{Self, Object};
    use std::string;
    use std::signer;

    // Test constants
    const ADMIN_ADDR: address = @0x100;
    const USER_ADDR: address = @0x200;
    const ATTACKER_ADDR: address = @0x300;

    // ========== Setup Helpers ==========
    // (Reusable setup functions)

    // ========== Happy Path Tests ==========
    // (Basic functionality)

    // ========== Access Control Tests ==========
    // (Unauthorized access blocked)

    // ========== Input Validation Tests ==========
    // (Invalid inputs rejected)

    // ========== Edge Case Tests ==========
    // (Boundaries and limits)
}
```

### Step 2: Write Happy Path Tests

**Test basic functionality works correctly:**

```move
#[test(creator = @0x1)]
public fun test_create_object_succeeds(creator: &signer) {
    // Execute
    let obj = my_module::create_my_object(
        creator,
        string::utf8(b"Test Object")
    );

    // Verify
    assert!(object::owner(obj) == signer::address_of(creator), 0);
}

#[test(owner = @0x1)]
public fun test_update_object_succeeds(owner: &signer) {
    // Setup
    let obj = my_module::create_my_object(owner, string::utf8(b"Old Name"));

    // Execute
    let new_name = string::utf8(b"New Name");
    my_module::update_object(owner, obj, new_name);

    // Verify (if you have view functions)
    // assert!(my_module::get_object_name(obj) == new_name, 0);
}

#[test(owner = @0x1, recipient = @0x2)]
public fun test_transfer_object_succeeds(
    owner: &signer,
    recipient: &signer
) {
    let recipient_addr = signer::address_of(recipient);

    // Setup
    let obj = my_module::create_my_object(owner, string::utf8(b"Object"));
    assert!(object::owner(obj) == signer::address_of(owner), 0);

    // Execute
    my_module::transfer_object(owner, obj, recipient_addr);

    // Verify
    assert!(object::owner(obj) == recipient_addr, 1);
}
```

### Step 3: Write Access Control Tests

**Test unauthorized access is blocked:**

```move
#[test(owner = @0x1, attacker = @0x2)]
#[expected_failure(abort_code = my_module::E_NOT_OWNER)]
public fun test_non_owner_cannot_update(
    owner: &signer,
    attacker: &signer
) {
    let obj = my_module::create_my_object(owner, string::utf8(b"Object"));

    // Attacker tries to update (should abort)
    my_module::update_object(attacker, obj, string::utf8(b"Hacked"));
}

#[test(owner = @0x1, attacker = @0x2)]
#[expected_failure(abort_code = my_module::E_NOT_OWNER)]
public fun test_non_owner_cannot_transfer(
    owner: &signer,
    attacker: &signer
) {
    let obj = my_module::create_my_object(owner, string::utf8(b"Object"));

    // Attacker tries to transfer (should abort)
    my_module::transfer_object(attacker, obj, @0x3);
}

#[test(admin = @0x1, user = @0x2)]
#[expected_failure(abort_code = my_module::E_NOT_ADMIN)]
public fun test_non_admin_cannot_configure(
    admin: &signer,
    user: &signer
) {
    my_module::init_module(admin);

    // Regular user tries admin function (should abort)
    my_module::update_config(user, 100);
}
```

### Step 4: Write Input Validation Tests

**Test invalid inputs are rejected:**

```move
#[test(user = @0x1)]
#[expected_failure(abort_code = my_module::E_ZERO_AMOUNT)]
public fun test_zero_amount_rejected(user: &signer) {
    my_module::deposit(user, 0); // Should abort
}

#[test(user = @0x1)]
#[expected_failure(abort_code = my_module::E_AMOUNT_TOO_HIGH)]
public fun test_excessive_amount_rejected(user: &signer) {
    my_module::deposit(user, my_module::MAX_DEPOSIT_AMOUNT + 1); // Should abort
}

#[test(owner = @0x1)]
#[expected_failure(abort_code = my_module::E_EMPTY_NAME)]
public fun test_empty_string_rejected(owner: &signer) {
    let obj = my_module::create_my_object(owner, string::utf8(b"Initial"));
    my_module::update_object(owner, obj, string::utf8(b"")); // Empty - should abort
}

#[test(owner = @0x1)]
#[expected_failure(abort_code = my_module::E_NAME_TOO_LONG)]
public fun test_string_too_long_rejected(owner: &signer) {
    let obj = my_module::create_my_object(owner, string::utf8(b"Initial"));

    // String exceeding MAX_NAME_LENGTH
    let long_name = string::utf8(b"This is an extremely long name that exceeds the maximum allowed length");

    my_module::update_object(owner, obj, long_name); // Should abort
}

#[test(owner = @0x1)]
#[expected_failure(abort_code = my_module::E_ZERO_ADDRESS)]
public fun test_zero_address_rejected(owner: &signer) {
    let obj = my_module::create_my_object(owner, string::utf8(b"Object"));
    my_module::transfer_object(owner, obj, @0x0); // Should abort
}
```

### Step 5: Write Edge Case Tests

**Test boundary conditions:**

```move
#[test(user = @0x1)]
public fun test_max_amount_allowed(user: &signer) {
    my_module::init_account(user);

    // Exactly MAX_DEPOSIT_AMOUNT should work
    my_module::deposit(user, my_module::MAX_DEPOSIT_AMOUNT);

    // Verify
    assert!(my_module::get_balance(signer::address_of(user)) == my_module::MAX_DEPOSIT_AMOUNT, 0);
}

#[test(user = @0x1)]
public fun test_max_name_length_allowed(user: &signer) {
    // Create string exactly MAX_NAME_LENGTH long
    let max_name = string::utf8(b"12345678901234567890123456789012"); // 32 chars if MAX = 32

    // Should succeed
    let obj = my_module::create_my_object(user, max_name);
}

#[test(user = @0x1)]
public fun test_empty_collection_operations(user: &signer) {
    let collection = my_module::create_collection(user, string::utf8(b"Collection"));

    // Should handle empty collection gracefully
    assert!(my_module::get_collection_size(collection) == 0, 0);
}
```

### Step 6: Verify Coverage

**Run tests with coverage:**

```bash
# Run all tests
aptos move test

# Run with coverage
aptos move test --coverage

# Generate detailed coverage report
aptos move coverage source --module <module_name>

# Verify 100% coverage
aptos move coverage summary
```

**Coverage report example:**

```
module: my_module
coverage: 100.0% (150/150 lines covered)
```

**If coverage < 100%:**

1. Check uncovered lines in report
2. Write tests for missing paths
3. Repeat until 100%

## Test Template Structure

```move
#[test_only]
module my_addr::module_tests {
    use my_addr::module::{Self, Type};

    // ========== Setup Helpers ==========

    fun setup_default(): Object<Type> {
        // Common setup code
    }

    // ========== Happy Path Tests ==========

    #[test(user = @0x1)]
    public fun test_basic_operation_succeeds(user: &signer) {
        // Test happy path
    }

    // ========== Access Control Tests ==========

    #[test(owner = @0x1, attacker = @0x2)]
    #[expected_failure(abort_code = E_NOT_OWNER)]
    public fun test_unauthorized_access_fails(
        owner: &signer,
        attacker: &signer
    ) {
        // Test access control
    }

    // ========== Input Validation Tests ==========

    #[test(user = @0x1)]
    #[expected_failure(abort_code = E_INVALID_INPUT)]
    public fun test_invalid_input_rejected(user: &signer) {
        // Test input validation
    }

    // ========== Edge Case Tests ==========

    #[test(user = @0x1)]
    public fun test_boundary_condition(user: &signer) {
        // Test edge cases
    }
}
```

## Testing Checklist

For each contract, verify you have tests for:

**Happy Paths:**

- [ ] Object creation works
- [ ] State updates work
- [ ] Transfers work
- [ ] All main features work

**Access Control:**

- [ ] Non-owners cannot modify objects
- [ ] Non-admins cannot call admin functions
- [ ] Unauthorized users blocked

**Input Validation:**

- [ ] Zero amounts rejected
- [ ] Excessive amounts rejected
- [ ] Empty strings rejected
- [ ] Strings too long rejected
- [ ] Zero addresses rejected

**Edge Cases:**

- [ ] Maximum values work
- [ ] Minimum values work
- [ ] Empty states handled

**Coverage:**

- [ ] 100% line coverage achieved
- [ ] All error codes tested
- [ ] All functions tested

## ALWAYS Rules

- ✅ ALWAYS achieve 100% test coverage
- ✅ ALWAYS test error paths with `#[expected_failure(abort_code = E_CODE)]`
- ✅ ALWAYS test access control with multiple signers
- ✅ ALWAYS test input validation with invalid inputs
- ✅ ALWAYS test edge cases (boundaries, limits, empty states)
- ✅ ALWAYS use clear test names: `test_feature_scenario`
- ✅ ALWAYS verify all state changes in tests
- ✅ ALWAYS run `aptos move test --coverage` before deployment

## NEVER Rules

- ❌ NEVER deploy without 100% coverage
- ❌ NEVER skip testing error paths
- ❌ NEVER skip access control tests
- ❌ NEVER use unclear test names
- ❌ NEVER batch tests without verifying each case
- ❌ NEVER hardcode real private keys or account addresses in test code — use test addresses like `@0x1`, `@0x100`,
  `@0xCAFE`
- ❌ NEVER read `.env` or `~/.aptos/config.yaml` to get test addresses

## Common Pitfalls

### Struct Field Access Across Modules

**Problem:** Test modules cannot access struct fields from other modules directly.

```move
// ❌ WRONG - Will NOT compile
let listing = marketplace::get_listing(nft_addr);
assert!(listing.price == 1000, 0);  // ERROR: field access not allowed
```

**Solution:** Use public view accessor functions from the main module.

```move
// ✅ CORRECT - Use accessor function
let (seller, price, timestamp) = marketplace::get_listing_details(nft_addr);
assert!(price == 1000, 0);
```

If the module doesn't have accessors, add them:

```move
// In main module
#[view]
public fun get_listing_details(nft_addr: address): (address, u64, u64) acquires Listings {
    let listing = table::borrow(&listings.items, nft_addr);
    (listing.seller, listing.price, listing.listed_at)
}
```

### Escrow Pattern Error Expectations

**Problem:** After listing an NFT to escrow, the seller no longer owns it.

```move
// ❌ WRONG expectation
#[expected_failure(abort_code = marketplace::E_ALREADY_LISTED)]
public fun test_cannot_list_twice(seller: &signer) {
    list_nft(seller, nft, 1000);  // NFT transfers to marketplace
    list_nft(seller, nft, 2000);  // Fails with E_NOT_OWNER, not E_ALREADY_LISTED!
}
```

**Solution:** Understand validation order - ownership is checked before listing status.

```move
// ✅ CORRECT expectation
#[expected_failure(abort_code = marketplace::E_NOT_OWNER)]
public fun test_cannot_list_twice(seller: &signer) {
    list_nft(seller, nft, 1000);  // NFT transfers to marketplace
    list_nft(seller, nft, 2000);  // Seller doesn't own it -> E_NOT_OWNER
}
```

### Acquires Annotation Errors

**Problem:** Adding acquires for resources borrowed by framework functions causes errors.

```move
// ❌ WRONG - framework handles its own acquires
public entry fun stake(...) acquires VaultConfig, Stakes, StakeTokenRefs {
    primary_fungible_store::transfer(...);  // Don't list what framework borrows
}
```

**Solution:** Only list resources YOUR code borrows.

```move
// ✅ CORRECT
public entry fun stake(...) acquires VaultConfig, Stakes {
    let config = borrow_global<VaultConfig>(...);  // You borrow this
    primary_fungible_store::transfer(...);          // Framework handles its own
}
```

## References

**Pattern Documentation:**

- `../../../patterns/move/TESTING.md` - Comprehensive testing guide (see Pattern 8 for cross-module issues)
- `../../../patterns/move/SECURITY.md` - Security testing requirements

**Official Documentation:**

- https://aptos.dev/build/smart-contracts/book/unit-testing

**Related Skills:**

- `write-contracts` - Generate code to test
- `security-audit` - Verify security after testing

---

**Remember:** 100% coverage is mandatory. Test happy paths, error paths, access control, and edge cases.
