---
name: aptos-move-testing
description: Expert on testing Move smart contracts on Aptos, including unit tests, integration tests, Move Prover formal verification, debugging strategies, and test coverage. Triggers on keywords move test, unit test, integration test, move prover, formal verification, debug, coverage, assert, expect
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

# Aptos Move Testing Expert

## Purpose

Provide expert guidance on testing Move smart contracts on Aptos blockchain, including unit tests, integration tests, formal verification with Move Prover, debugging strategies, and achieving comprehensive test coverage.

## When to Use

Auto-invoke when users mention:
- **Testing** - unit tests, integration tests, test coverage, test cases
- **Move Prover** - formal verification, specifications, invariants
- **Debugging** - errors, failures, stack traces, logging
- **Test Commands** - `aptos move test`, `aptos move prove`
- **Assertions** - `assert!`, test expectations, error codes
- **Mock Data** - test accounts, signers, resources

## Core Testing Concepts

### Unit Testing in Move

```move
#[test]
fun test_basic_functionality() {
    // Test code here
    assert!(condition, ERROR_CODE);
}

#[test(account = @0x1)]
fun test_with_signer(account: &signer) {
    // Test with signer parameter
}

#[test]
#[expected_failure(abort_code = ERROR_CODE)]
fun test_expected_failure() {
    // Code that should fail
}
```

### Test Attributes

- `#[test]` - Basic test function
- `#[test(param = @address)]` - Test with named parameters (signers/addresses)
- `#[test_only]` - Functions/modules only compiled in test mode
- `#[expected_failure]` - Test should abort
- `#[expected_failure(abort_code = N)]` - Test should abort with specific code

## Process

When a user asks about Move testing:

### 1. Identify Testing Need

```
Common scenarios:
- Writing unit tests for new functions
- Testing resource operations (move_to, move_from, borrow_global)
- Verifying error conditions and abort codes
- Integration testing with multiple modules
- Formal verification with Move Prover
- Debugging test failures
- Improving test coverage
```

### 2. Determine Test Type

**Unit Tests:**
- Test individual functions in isolation
- Mock dependencies
- Fast execution
- Use `#[test]` attribute

**Integration Tests:**
- Test module interactions
- Test complete workflows
- Use multiple signers
- Test state changes

**Formal Verification:**
- Use Move Prover
- Write specifications
- Verify invariants
- Prove correctness mathematically

### 3. Provide Testing Solution

Structure your response:
- **Test strategy** - what to test and why
- **Code example** - working test code
- **Setup** - any required test fixtures or helper functions
- **Assertions** - what to verify
- **Edge cases** - corner cases to consider
- **Commands** - how to run the tests

## Testing Patterns

### Pattern 1: Resource Testing

```move
#[test_only]
use std::signer;

#[test(account = @0x123)]
fun test_resource_creation(account: &signer) {
    let addr = signer::address_of(account);

    // Create resource
    create_resource(account);

    // Verify resource exists
    assert!(exists<MyResource>(addr), ERROR_RESOURCE_NOT_FOUND);

    // Verify resource state
    let resource = borrow_global<MyResource>(addr);
    assert!(resource.value == expected_value, ERROR_INVALID_STATE);
}
```

### Pattern 2: Error Condition Testing

```move
#[test]
#[expected_failure(abort_code = ERROR_INSUFFICIENT_BALANCE)]
fun test_insufficient_balance() {
    // Setup account with low balance
    // Attempt operation that should fail
    transfer(from, to, amount_too_large);
}
```

### Pattern 3: Multi-Signer Testing

```move
#[test(alice = @0x123, bob = @0x456)]
fun test_transfer(alice: &signer, bob: &signer) {
    let alice_addr = signer::address_of(alice);
    let bob_addr = signer::address_of(bob);

    // Setup initial state
    initialize(alice);
    initialize(bob);

    // Perform transfer
    transfer(alice, bob_addr, 100);

    // Verify balances
    assert!(get_balance(alice_addr) == 900, ERROR_INVALID_BALANCE);
    assert!(get_balance(bob_addr) == 100, ERROR_INVALID_BALANCE);
}
```

### Pattern 4: Test-Only Helpers

```move
#[test_only]
module test_helpers {
    use std::signer;

    public fun setup_account(account: &signer): address {
        let addr = signer::address_of(account);
        // Common setup logic
        addr
    }

    public fun create_test_token(account: &signer, amount: u64) {
        // Create tokens for testing
    }
}
```

## Move Prover Integration

### Specification Syntax

```move
spec module {
    // Module-level invariants
    invariant forall addr: address:
        exists<Balance>(addr) ==> global<Balance>(addr).value >= 0;
}

spec transfer {
    // Pre-conditions
    requires sender_balance >= amount;
    requires sender != recipient;

    // Post-conditions
    ensures global<Balance>(sender).value == old(global<Balance>(sender).value) - amount;
    ensures global<Balance>(recipient).value == old(global<Balance>(recipient).value) + amount;

    // Abort conditions
    aborts_if sender_balance < amount;
}
```

### Running Move Prover

```bash
# Verify all specs in package
aptos move prove

# Verify specific module
aptos move prove --filter MyModule

# Verbose output
aptos move prove --verbose
```

## Test Commands

### Basic Testing

```bash
# Run all tests in package
aptos move test

# Run specific test
aptos move test --filter test_name

# Run tests with coverage
aptos move test --coverage

# Run with gas profiling
aptos move test --gas

# Verbose output
aptos move test --verbose
```

### Test Output Interpretation

```
Running Move unit tests
[ PASS    ] 0x1::my_module::test_success
[ FAIL    ] 0x1::my_module::test_failure
[ TIMEOUT ] 0x1::my_module::test_slow

Error: Assertion failed
   ┌── my_module.move:42:9 ───
   │
42 │         assert!(balance == 100, ERROR_INVALID_BALANCE);
   │         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

## Debugging Strategies

### 1. Add Debug Prints (Test Only)

```move
#[test_only]
use std::debug;

#[test]
fun test_with_debug() {
    debug::print(&b"Starting test");
    debug::print(&value);
    // Test logic
}
```

### 2. Break Down Complex Tests

```move
// Instead of one large test
#[test]
fun test_complex_workflow() {
    setup();
    step1();
    step2();
    step3();
    verify();
}

// Break into multiple tests
#[test]
fun test_step1() { /* ... */ }

#[test]
fun test_step2() { /* ... */ }

#[test]
fun test_step3() { /* ... */ }
```

### 3. Use Specific Abort Codes

```move
const ERROR_INVALID_AMOUNT: u64 = 1;
const ERROR_INSUFFICIENT_BALANCE: u64 = 2;
const ERROR_UNAUTHORIZED: u64 = 3;

// In code
assert!(amount > 0, ERROR_INVALID_AMOUNT);

// In test
#[expected_failure(abort_code = ERROR_INVALID_AMOUNT)]
fun test_zero_amount() { /* ... */ }
```

## Test Coverage Best Practices

### What to Test

✅ **Critical Paths:**
- Main business logic
- State transitions
- Access control
- Resource management

✅ **Error Conditions:**
- Invalid inputs
- Insufficient permissions
- Resource not found
- Arithmetic overflow

✅ **Edge Cases:**
- Zero values
- Maximum values
- Empty collections
- Boundary conditions

✅ **Invariants:**
- Total supply conservation
- Balance constraints
- Ownership rules

### Coverage Goals

```
Aim for:
- 100% of public functions
- 100% of abort conditions
- All state transitions
- All access control checks
```

## Common Testing Patterns

### Setup/Teardown Pattern

```move
#[test_only]
fun setup_test_env(account: &signer): TestContext {
    initialize_module(account);
    create_test_resources(account);
    TestContext { /* ... */ }
}

#[test(account = @0x1)]
fun test_feature(account: &signer) {
    let ctx = setup_test_env(account);
    // Use ctx
    // No teardown needed (Move tests are isolated)
}
```

### Parameterized Testing

```move
#[test_only]
fun verify_transfer_amount(amount: u64, expected_result: bool) {
    if (expected_result) {
        transfer(sender, receiver, amount);
    } else {
        // Should fail
    }
}

#[test]
fun test_valid_amounts() {
    verify_transfer_amount(1, true);
    verify_transfer_amount(100, true);
    verify_transfer_amount(1000, true);
}

#[test]
#[expected_failure]
fun test_invalid_amounts() {
    verify_transfer_amount(0, false);
}
```

### State Verification

```move
#[test]
fun test_state_consistency(account: &signer) {
    let addr = signer::address_of(account);

    // Initial state
    let before = get_state(addr);

    // Perform operation
    perform_operation(account);

    // Verify state changes
    let after = get_state(addr);
    assert!(after.field1 == before.field1 + delta, ERROR_STATE);
}
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Move Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install Aptos CLI
        run: |
          curl -fsSL "https://aptos.dev/scripts/install_cli.py" | python3

      - name: Run Move Tests
        run: |
          aptos move test --coverage

      - name: Run Move Prover
        run: |
          aptos move prove
```

## Troubleshooting Common Issues

### Issue: Test Timeout

```move
// Problem: Test takes too long
#[test]
fun test_slow() {
    for (i in 0..1000000) { /* ... */ }
}

// Solution: Reduce iterations or split tests
#[test]
fun test_optimized() {
    for (i in 0..100) { /* ... */ }
}
```

### Issue: Resource Already Exists

```move
// Problem: Resource published twice
#[test(account = @0x1)]
fun test_duplicate() {
    move_to(account, Resource {});
    move_to(account, Resource {}); // ERROR!
}

// Solution: Check existence or use different accounts
#[test(account = @0x1)]
fun test_correct() {
    if (!exists<Resource>(addr)) {
        move_to(account, Resource {});
    }
}
```

### Issue: Signer Not Available

```move
// Problem: Need signer but don't have one
#[test]
fun test_needs_signer() {
    let signer = ???; // Can't create signer!
}

// Solution: Use test parameter
#[test(account = @0x1)]
fun test_with_signer(account: &signer) {
    // Use account
}
```

## Advanced Testing Techniques

### Property-Based Testing

```move
#[test_only]
fun property_sum_commutative(a: u64, b: u64) {
    assert!(add(a, b) == add(b, a), ERROR_PROPERTY);
}

#[test]
fun test_properties() {
    property_sum_commutative(1, 2);
    property_sum_commutative(100, 50);
    property_sum_commutative(0, 999);
}
```

### Fuzz Testing Concepts

```move
#[test]
fun test_with_various_inputs() {
    // Test boundary values
    test_function(0);
    test_function(1);
    test_function(u64::MAX);

    // Test common values
    test_function(100);
    test_function(1000);

    // Test edge cases
    test_function(u64::MAX - 1);
}
```

## Documentation References

When answering questions, reference:
- Aptos Move testing documentation
- Move Prover specifications
- Example test suites in Aptos framework
- Testing best practices guides

## Response Style

- **Example-first** - Show working test code immediately
- **Explain pattern** - Clarify what the test verifies
- **Cover edge cases** - Mention corner cases to test
- **Debugging tips** - Help troubleshoot failures
- **Best practices** - Mention testing standards

## Follow-up Suggestions

After helping with tests, suggest:
- Additional test cases to consider
- Move Prover specifications
- Code coverage analysis
- Integration testing strategies
- CI/CD integration for automated testing
