---
name: aztec-testing
description: Assists with testing Aztec smart contracts using the TestEnvironment. Use when writing unit tests, integration tests, or debugging test failures for Aztec contracts.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Aztec Testing Skill

You are an expert in testing Aztec smart contracts. Help users write comprehensive tests using Aztec's TestEnvironment and debugging test failures.

## Testing Framework Overview

Aztec provides a Noir-native testing framework using `TestEnvironment` that allows you to:

- Deploy contracts in a simulated environment
- Call private and public functions
- Verify state changes
- Test access control
- Simulate multiple users

## Test Setup

### Basic Test Structure

```rust
use aztec::{
    protocol::address::AztecAddress,
    test::helpers::test_environment::TestEnvironment,
};

#[test]
unconstrained fn test_example() {
    // Setup
    let mut env = TestEnvironment::new();
    let owner = env.create_light_account();

    // Deploy
    let initializer = MyContract::interface().constructor(args);
    let contract_address = env.deploy("MyContract").with_public_initializer(owner, initializer);

    // Act - call private function
    env.call_private(owner, MyContract::at(contract_address).some_function(args));

    // Assert - view public state
    let result = env.view_public(MyContract::at(contract_address).view_function());
    assert(result == expected);
}
```

### Account Types

```rust
// Light account - fast, limited features (use for most tests)
let owner = env.create_light_account();

// Contract account - full features including authwit support (slower)
let owner = env.create_contract_account();
```

### Deployment Options

```rust
// Deploy with public initializer
let address = env.deploy("MyContract").with_public_initializer(owner, initializer);

// Deploy with private initializer
let address = env.deploy("MyContract").with_private_initializer(owner, initializer);

// Deploy without initializer
let address = env.deploy("MyContract").without_initializer();
```

## Common Testing Patterns

### Testing Private Functions

```rust
#[test]
unconstrained fn test_private_transfer() {
    let mut env = TestEnvironment::new();
    let alice = env.create_light_account();
    let bob = env.create_light_account();

    // Deploy and setup
    let contract_address = deploy_token(&mut env, alice);

    // Mint to alice first
    env.call_private(alice, Token::at(contract_address).mint_private(alice, 100));

    // Transfer from alice to bob
    env.call_private(alice, Token::at(contract_address).transfer(bob, 50));

    // Verify balances using simulate_utility for unconstrained reads
    let alice_balance = env.simulate_utility(Token::at(contract_address).balance_of_private(alice));
    let bob_balance = env.simulate_utility(Token::at(contract_address).balance_of_private(bob));

    assert(alice_balance == 50);
    assert(bob_balance == 50);
}
```

### Testing Public Functions

```rust
#[test]
unconstrained fn test_public_mint() {
    let mut env = TestEnvironment::new();
    let admin = env.create_light_account();
    let user = env.create_light_account();

    let contract_address = deploy_token(&mut env, admin);

    // Admin mints tokens
    env.call_public(admin, Token::at(contract_address).mint_public(user, 1000));

    // Verify balance
    let balance = env.view_public(Token::at(contract_address).balance_of_public(user));
    assert(balance == 1000);
}
```

### Testing Access Control

```rust
#[test(should_fail)]
unconstrained fn test_unauthorized_mint() {
    let mut env = TestEnvironment::new();
    let admin = env.create_light_account();
    let attacker = env.create_light_account();

    let contract_address = deploy_token(&mut env, admin);

    // Non-admin tries to mint - should fail
    env.call_public(attacker, Token::at(contract_address).mint_public(attacker, 1000));
}
```

### Testing Private <> Public Communication

```rust
#[test]
unconstrained fn test_public_to_private() {
    let mut env = TestEnvironment::new();
    let user = env.create_light_account();

    let contract_address = deploy_token(&mut env, user);

    // Give user some public tokens
    env.call_public(user, Token::at(contract_address).mint_public(user, 100));

    // Move tokens from public to private
    env.call_private(user, Token::at(contract_address).public_to_private(50));

    // Verify balances in both domains
    let public_balance = env.view_public(Token::at(contract_address).balance_of_public(user));
    let private_balance = env.simulate_utility(Token::at(contract_address).balance_of_private(user));

    assert(public_balance == 50);
    assert(private_balance == 50);
}
```

## Testing Best Practices

### 1. Test Isolation

- Each test should be independent
- Don't rely on state from other tests
- Use fresh TestEnvironment for each test

### 2. Test Coverage

- Happy path scenarios
- Edge cases (zero amounts, max values)
- Access control violations
- Invalid inputs

### 3. Descriptive Test Names

```rust
#[test]
fn test_transfer_succeeds_with_sufficient_balance() { }

#[test(should_fail)]
fn test_transfer_fails_with_insufficient_balance() { }
```

### 4. Helper Functions

Create reusable helpers for common setup:

```rust
unconstrained fn deploy_token(env: &mut TestEnvironment, admin: AztecAddress) -> AztecAddress {
    let initializer = Token::interface().constructor(admin);
    env.deploy("Token").with_public_initializer(admin, initializer)
}
```

## Debugging Test Failures

### Common Issues

1. **"Not authorized" errors**

   - Check if you've called `env.impersonate(correct_user)`
   - Verify the user has the required role

2. **State not updating**

   - Ensure you're using the right context (`.private()` vs `.public()`)
   - Check that enqueued calls are being processed

3. **Note not found**

   - Make sure notes were created before consumption
   - Verify the note owner is correct

4. **Assertion failures**
   - Add print statements to debug values
   - Check for off-by-one errors
   - Verify expected vs actual values

## Running Tests

```bash
# Run all tests
aztec test

# Run specific test
aztec test --test-name test_transfer

# Run with verbose output
aztec test --show-output
```
