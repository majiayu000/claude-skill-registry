---
name: analyze-gas-optimization
description:
  "Analyze and optimize Aptos Move contracts for gas efficiency, identifying expensive operations and suggesting
  optimizations. Triggers on: 'optimize gas', 'reduce gas costs', 'gas analysis', 'make contract cheaper', 'gas
  efficiency', 'analyze gas usage', 'reduce transaction costs'."
license: MIT
metadata:
  author: aptos-labs
  version: "1.0"
  category: move
  tags: ["gas", "optimization", "performance", "costs"]
  priority: high
---

# Skill: analyze-gas-optimization

Analyze and optimize Aptos Move contracts for gas efficiency, identifying expensive operations and suggesting
optimizations.

## When to Use This Skill

**Trigger phrases:**

- "optimize gas", "reduce gas costs", "gas analysis"
- "make contract cheaper", "gas efficiency"
- "analyze gas usage", "gas optimization"
- "reduce transaction costs"

**Use cases:**

- Before mainnet deployment
- When transaction costs are high
- When optimizing for high-frequency operations
- When building DeFi protocols with many transactions

## Core Gas Optimization Principles

### 1. Storage Optimization

- Minimize stored data size
- Use efficient data structures
- Pack struct fields efficiently
- Remove unnecessary fields

### 2. Computation Optimization

- Avoid loops over large collections
- Cache repeated calculations
- Use bitwise operations when possible
- Minimize vector operations

### 3. Reference Optimization

- Prefer borrowing over moving when possible
- Use `&` and `&mut` efficiently
- Avoid unnecessary copies

## Gas Cost Analysis

### Expensive Operations

#### 1. Global Storage Operations

```move
// EXPENSIVE: Writing to global storage
move_to(account, large_struct);

// EXPENSIVE: Reading and writing
let data = borrow_global_mut<LargeData>(addr);

// EXPENSIVE: Checking existence
if (exists<Resource>(addr)) { ... }
```

#### 2. Vector Operations

```move
// EXPENSIVE: Growing vectors dynamically
vector::push_back(&mut vec, item); // O(n) worst case

// EXPENSIVE: Searching vectors
vector::contains(&vec, &item); // O(n)

// EXPENSIVE: Removing from middle
vector::remove(&mut vec, index); // O(n)
```

#### 3. String Operations

```move
// EXPENSIVE: String concatenation
string::append(&mut s1, s2);

// EXPENSIVE: UTF8 validation
string::utf8(bytes);
```

### Optimization Patterns

#### 1. Batch Operations

```move
// BAD: Multiple storage accesses
public fun update_values(account: &signer, updates: vector<Update>) {
    let i = 0;
    while (i < vector::length(&updates)) {
        let update = vector::borrow(&updates, i);
        let data = borrow_global_mut<Data>(update.address);
        data.value = update.value;
        i = i + 1;
    }
}

// GOOD: Single storage access with batch update
public fun batch_update(account: &signer, updates: vector<Update>) {
    let data = borrow_global_mut<Data>(signer::address_of(account));
    let i = 0;
    while (i < vector::length(&updates)) {
        let update = vector::borrow(&updates, i);
        // Update in memory
        update_memory_data(data, update);
        i = i + 1;
    }
}
```

#### 2. Storage Packing

```move
// BAD: Wasteful storage
struct UserData has key {
    active: bool,      // 1 byte used, 7 wasted
    level: u8,         // 1 byte used, 7 wasted
    score: u64,        // 8 bytes
    timestamp: u64,    // 8 bytes
    // Total: 32 bytes (50% wasted)
}

// GOOD: Packed storage
struct UserData has key {
    // Pack small fields together
    flags: u8,         // Bits: [active, reserved...]
    level: u8,
    reserved: u16,     // Future use
    score: u64,
    timestamp: u64,
    // Total: 20 bytes (37.5% saved)
}
```

#### 3. Lazy Evaluation

```move
// BAD: Always compute expensive value
struct Pool has key {
    total_shares: u64,
    total_assets: u64,
    // Computed on every update
    share_price: u64,
}

// GOOD: Compute only when needed
struct Pool has key {
    total_shares: u64,
    total_assets: u64,
    // Don't store computed values
}

public fun get_share_price(pool_addr: address): u64 {
    let pool = borrow_global<Pool>(pool_addr);
    if (pool.total_shares == 0) {
        INITIAL_SHARE_PRICE
    } else {
        pool.total_assets * PRECISION / pool.total_shares
    }
}
```

#### 4. Event Optimization

```move
// BAD: Large event data
struct TradeEvent has drop, store {
    pool: Object<Pool>,
    trader: address,
    token_in: Object<Token>,
    token_out: Object<Token>,
    amount_in: u64,
    amount_out: u64,
    fees: u64,
    timestamp: u64,
    metadata: vector<u8>, // Large metadata
}

// GOOD: Minimal event data
struct TradeEvent has drop, store {
    pool_id: u64,        // Use ID instead of Object
    trader: address,
    amounts: u128,       // Pack amount_in and amount_out
    fees: u64,
    // Compute other data from state
}
```

#### 5. Collection Optimization

```move
// BAD: Linear search
public fun find_item(items: &vector<Item>, id: u64): Option<Item> {
    let i = 0;
    while (i < vector::length(items)) {
        let item = vector::borrow(items, i);
        if (item.id == id) {
            return option::some(*item)
        };
        i = i + 1;
    }
    option::none()
}

// GOOD: Use Table for O(1) lookup
struct Storage has key {
    items: Table<u64, Item>,
}

public fun find_item(storage: &Storage, id: u64): Option<Item> {
    if (table::contains(&storage.items, id)) {
        option::some(*table::borrow(&storage.items, id))
    } else {
        option::none()
    }
}
```

## Gas Measurement

### 1. Transaction Simulation

```bash
# Simulate to get gas estimate
aptos move run-function \
    --function-id 0x1::module::function \
    --args ... \
    --simulate

# Output includes:
# - gas_unit_price
# - max_gas_amount
# - gas_used
```

### 2. Gas Profiling

```move
#[test]
public fun test_gas_usage() {
    // Measure gas for operation
    let gas_before = gas::remaining_gas();
    expensive_operation();
    let gas_used = gas_before - gas::remaining_gas();

    // Assert reasonable gas usage
    assert!(gas_used < MAX_ACCEPTABLE_GAS, E_TOO_EXPENSIVE);
}
```

## Optimization Checklist

### Storage Checklist

- [ ] Pack struct fields to minimize size
- [ ] Use appropriate integer sizes (u8, u16, u32, u64)
- [ ] Remove unnecessary fields
- [ ] Consider off-chain storage for large data
- [ ] Use events instead of storage for logs

### Computation Checklist

- [ ] Cache repeated calculations
- [ ] Minimize loops over collections
- [ ] Use early returns to skip unnecessary work
- [ ] Batch similar operations
- [ ] Avoid redundant checks

### Collection Checklist

- [ ] Use Table/TableWithLength for key-value lookups
- [ ] Use SmartTable for large collections
- [ ] Limit vector sizes
- [ ] Consider pagination for large results
- [ ] Use appropriate data structures

### Best Practices

- [ ] Profile before and after optimization
- [ ] Test gas usage in unit tests
- [ ] Document gas costs for public functions
- [ ] Consider gas costs in contract design
- [ ] Monitor mainnet gas usage

## Common Gas Optimizations

### 1. Replace Vectors with Tables

```move
// Before: O(n) search
struct Registry has key {
    users: vector<User>,
}

// After: O(1) lookup
struct Registry has key {
    users: Table<address, User>,
    user_list: vector<address>, // If iteration needed
}
```

### 2. Minimize Storage Reads

```move
// Before: Multiple reads
public fun transfer(from: &signer, to: address, amount: u64) {
    assert!(get_balance(signer::address_of(from)) >= amount, E_INSUFFICIENT);
    let from_balance = borrow_global_mut<Balance>(signer::address_of(from));
    let to_balance = borrow_global_mut<Balance>(to);
    // ...
}

// After: Single read with validation
public fun transfer(from: &signer, to: address, amount: u64) {
    let from_addr = signer::address_of(from);
    let from_balance = borrow_global_mut<Balance>(from_addr);
    assert!(from_balance.value >= amount, E_INSUFFICIENT);
    // ... rest of logic
}
```

### 3. Use Bitwise Flags

```move
// Before: Multiple bool fields (8 bytes each)
struct Settings has copy, drop, store {
    is_active: bool,
    is_paused: bool,
    is_initialized: bool,
    allows_deposits: bool,
}

// After: Single u8 (1 byte)
struct Settings has copy, drop, store {
    flags: u8, // Bit 0: active, 1: paused, 2: initialized, 3: deposits
}

const FLAG_ACTIVE: u8 = 1;        // 0b00000001
const FLAG_PAUSED: u8 = 2;        // 0b00000010
const FLAG_INITIALIZED: u8 = 4;   // 0b00000100
const FLAG_DEPOSITS: u8 = 8;      // 0b00001000

public fun is_active(settings: &Settings): bool {
    (settings.flags & FLAG_ACTIVE) != 0
}
```

## Gas Optimization Report Template

```markdown
# Gas Optimization Report

## Summary

- Current average gas: X units
- Optimized average gas: Y units
- Savings: Z% reduction

## Optimizations Applied

### 1. Storage Optimization

- Packed struct fields (saved X bytes)
- Replaced vectors with tables (O(n) → O(1))
- Removed redundant fields

### 2. Computation Optimization

- Cached price calculations (saved X operations)
- Batched updates (N calls → 1 call)
- Early returns in validation

### 3. Event Optimization

- Reduced event size from X to Y bytes
- Removed redundant event fields

## Measurements

| Function | Before | After  | Savings |
| -------- | ------ | ------ | ------- |
| mint     | 50,000 | 35,000 | 30%     |
| transfer | 30,000 | 25,000 | 17%     |
| swap     | 80,000 | 60,000 | 25%     |

## Recommendations

1. Consider further optimizations for high-frequency functions
2. Monitor mainnet usage patterns
3. Set up gas usage alerts
```

## Integration Notes

- Works with `security-audit` to ensure optimizations don't compromise security
- Use with `generate-tests` to verify optimizations maintain correctness
- Apply before `deploy-contracts` for mainnet deployments
- Reference `STORAGE_OPTIMIZATION.md` for detailed patterns

## NEVER Rules

- ❌ NEVER optimize away security checks (access control, input validation)
- ❌ NEVER deploy optimized code without re-testing
- ❌ NEVER read `.env` or `~/.aptos/config.yaml` during gas analysis (contain private keys)

## References

- Aptos Gas Schedule: https://github.com/aptos-labs/aptos-core/blob/main/aptos-move/aptos-gas-schedule
- Move VM Gas Metering: https://github.com/aptos-labs/aptos-core/tree/main/aptos-move/aptos-vm
- Gas Optimization Patterns: Check daily-move repository for real examples
