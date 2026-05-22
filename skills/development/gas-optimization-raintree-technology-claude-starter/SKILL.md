---
name: aptos-gas-optimization
description: Expert on Aptos gas optimization, performance tuning, storage costs, execution efficiency, inline functions, aggregator usage, parallel execution, table vs vector tradeoffs, and gas profiling tools. Triggers on keywords gas optimization, performance, gas cost, storage fee, inline, aggregator, parallel execution, gas profiling, optimization
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

# Aptos Gas & Performance Optimization Expert

## Purpose

Provide expert guidance on optimizing gas costs and performance for Aptos smart contracts. Cover storage optimization, execution efficiency, parallel execution enablers, profiling tools, and cost-effective design patterns.

## When to Use

Auto-invoke when users mention:
- **Gas Costs** - gas fees, transaction costs, gas optimization
- **Performance** - slow transactions, execution time, throughput
- **Storage** - storage fees, data structures, table vs vector
- **Optimization** - code optimization, inline functions, efficiency
- **Parallel Execution** - aggregators, concurrent transactions
- **Profiling** - gas profiling, benchmarking, analysis

## Gas Model Overview

### Aptos Gas Components

```
Total Gas Cost = Execution Gas + Storage Gas + IO Gas
```

**1. Execution Gas:**
- Function calls, loops, computations
- Instruction-level costs
- Type operations, memory access

**2. Storage Gas:**
- Per-byte storage cost
- Write amplification
- State rent (upcoming)

**3. IO Gas:**
- Reading from storage
- Writing to storage
- Event emission

### Gas Units to APT Conversion

```
Gas Fee (APT) = Gas Units × Gas Unit Price
Gas Unit Price = market-determined (typically 100-1000 octas per gas unit)
1 APT = 100,000,000 octas
```

**Example:**
```
Transaction uses 1,000 gas units
Gas price = 100 octas/unit
Cost = 1,000 × 100 = 100,000 octas = 0.001 APT
```

## Storage Optimization

### Data Structure Costs

| Structure | Read Cost | Write Cost | Storage Cost | Best For |
|-----------|-----------|------------|--------------|----------|
| u64 | ~10 gas | ~15 gas | 8 bytes | Simple counters |
| vector<u64>(100) | ~100 gas | ~150 gas | 800 bytes | Small lists |
| SimpleMap(100) | ~100 gas | ~150 gas | ~1KB | Small maps |
| Table(100) | ~15 gas | ~20 gas | ~2KB | Medium maps |
| SmartTable(100) | ~15 gas | ~20 gas | ~2KB | Large maps |
| Aggregator | ~10 gas | ~12 gas | 32 bytes | **Parallel counters** |

### Choosing the Right Data Structure

```move
// ❌ Bad: Vector for large datasets
struct Registry has key {
    users: vector<User>  // O(n) search, expensive for 1000+ items
}

// ✅ Better: Table for large datasets
struct Registry has key {
    users: Table<address, User>  // O(1) lookup, scalable
}

// ✅ Best: SmartTable for very large datasets
struct Registry has key {
    users: SmartTable<address, User>  // Auto-splitting, 100k+ items
}
```

### Storage Pattern: Minimize State

```move
// ❌ Bad: Storing redundant data
struct User has store {
    address: address,        // Redundant (key already has this)
    total_deposits: u64,     // Can be calculated
    deposit_history: vector<u64>,
    last_update: u64,        // Often unnecessary
}

// ✅ Good: Minimal state
struct User has store {
    deposit_history: vector<u64>,  // Essential data only
}

// Calculate total on-demand (no storage cost)
public fun get_total_deposits(user: &User): u64 {
    let mut total = 0;
    let i = 0;
    while (i < vector::length(&user.deposit_history)) {
        total = total + *vector::borrow(&user.deposit_history, i);
        i = i + 1;
    };
    total
}
```

### Struct Packing

```move
// ❌ Bad: Inefficient packing (64 bytes)
struct Data has store {
    flag1: bool,        // 1 byte + 7 padding
    value1: u64,        // 8 bytes
    flag2: bool,        // 1 byte + 7 padding
    value2: u64,        // 8 bytes
    flag3: bool,        // 1 byte + 7 padding
    value3: u64,        // 8 bytes
}

// ✅ Good: Optimized packing (32 bytes)
struct Data has store {
    // Group small fields together
    flag1: bool,        // 1 byte
    flag2: bool,        // 1 byte
    flag3: bool,        // 1 byte
    // Padding: 5 bytes
    // Then larger fields
    value1: u64,        // 8 bytes
    value2: u64,        // 8 bytes
    value3: u64,        // 8 bytes
}

// ✅ Best: Pack flags into single byte
struct Data has store {
    flags: u8,          // All 3 flags in 1 byte (bitwise)
    value1: u64,
    value2: u64,
    value3: u64,
}

public fun get_flag1(data: &Data): bool {
    (data.flags & 0b001) != 0
}

public fun set_flag1(data: &mut Data, value: bool) {
    if (value) {
        data.flags = data.flags | 0b001;
    } else {
        data.flags = data.flags & 0b110;
    }
}
```

## Execution Optimization

### Inline Functions

```move
// Small, frequently called functions should be inline
inline fun add(a: u64, b: u64): u64 {
    a + b
}

inline fun min(a: u64, b: u64): u64 {
    if (a < b) a else b
}

inline fun max(a: u64, b: u64): u64 {
    if (a > b) a else b
}

public fun calculate(): u64 {
    // Inlined: no function call overhead
    let sum = add(10, 20);
    let minimum = min(sum, 50);
    minimum
}
```

**When to inline:**
- Functions < 5 lines
- Called frequently
- Simple computations
- Math helpers
- Validation checks

**When NOT to inline:**
- Large functions (increases code size)
- Rarely called functions
- Recursive functions (not supported)

### Loop Optimization

```move
// ❌ Bad: Inefficient loop
public fun sum_vector(v: &vector<u64>): u64 {
    let mut sum = 0;
    let mut i = 0;
    while (i < vector::length(v)) {  // Calls length() every iteration!
        sum = sum + *vector::borrow(v, i);
        i = i + 1;
    };
    sum
}

// ✅ Good: Cache length
public fun sum_vector(v: &vector<u64>): u64 {
    let mut sum = 0;
    let len = vector::length(v);  // Call once
    let mut i = 0;
    while (i < len) {
        sum = sum + *vector::borrow(v, i);
        i = i + 1;
    };
    sum
}

// ✅ Best: Use built-in functions when available
public fun sum_vector(v: &vector<u64>): u64 {
    vector::fold(v, 0, |acc, x| acc + *x)
}
```

### Early Returns

```move
// ❌ Bad: Unnecessary work
public fun validate_and_process(amount: u64, user: address) {
    let valid = amount > 0 && amount < MAX_AMOUNT && is_whitelisted(user);

    if (valid) {
        // Expensive operations
        complex_calculation();
        update_state();
        emit_events();
    }
}

// ✅ Good: Early return
public fun validate_and_process(amount: u64, user: address) {
    // Check cheapest conditions first
    if (amount == 0) return;
    if (amount >= MAX_AMOUNT) return;
    if (!is_whitelisted(user)) return;

    // Only do expensive work if all checks pass
    complex_calculation();
    update_state();
    emit_events();
}
```

### Minimize Global Storage Access

```move
// ❌ Bad: Multiple borrows
public fun update_balance(addr: address, amount: u64) acquires Balance {
    let balance = borrow_global_mut<Balance>(addr);
    balance.value = balance.value + amount;

    let balance2 = borrow_global_mut<Balance>(addr);  // Second borrow!
    balance2.last_update = timestamp::now_seconds();
}

// ✅ Good: Single borrow
public fun update_balance(addr: address, amount: u64) acquires Balance {
    let balance = borrow_global_mut<Balance>(addr);
    balance.value = balance.value + amount;
    balance.last_update = timestamp::now_seconds();
}
```

### Batch Operations

```move
// ❌ Bad: Individual operations
public entry fun transfer_to_many(
    sender: &signer,
    recipients: vector<address>,
    amounts: vector<u64>
) {
    let i = 0;
    while (i < vector::length(&recipients)) {
        transfer(sender, *vector::borrow(&recipients, i), *vector::borrow(&amounts, i));
        i = i + 1;
    }
}

// ✅ Good: Batched operation (single transaction)
public entry fun batch_transfer(
    sender: &signer,
    recipients: vector<address>,
    amounts: vector<u64>
) acquires Balance {
    let sender_addr = signer::address_of(sender);
    let sender_balance = borrow_global_mut<Balance>(sender_addr);

    let mut i = 0;
    let len = vector::length(&recipients);

    // Calculate total first
    let mut total = 0;
    while (i < len) {
        total = total + *vector::borrow(&amounts, i);
        i = i + 1;
    };

    assert!(sender_balance.value >= total, ERROR_INSUFFICIENT_BALANCE);

    // Single deduction from sender
    sender_balance.value = sender_balance.value - total;

    // Batch credit recipients
    i = 0;
    while (i < len) {
        let recipient = *vector::borrow(&recipients, i);
        let amount = *vector::borrow(&amounts, i);

        let recipient_balance = borrow_global_mut<Balance>(recipient);
        recipient_balance.value = recipient_balance.value + amount;

        i = i + 1;
    }
}
```

## Parallel Execution with Aggregators

### Understanding Aggregators

**Problem:** Traditional counter creates conflicts
```move
// ❌ Bad: Conflicts on concurrent access
struct Stats has key {
    total_users: u64  // Multiple txns modifying = conflict!
}

public fun register_user() acquires Stats {
    let stats = borrow_global_mut<Stats>(@protocol);
    stats.total_users = stats.total_users + 1;
    // If 2 txns do this simultaneously, one must retry
}
```

**Solution:** Aggregators enable parallel updates
```move
// ✅ Good: No conflicts!
use aptos_framework::aggregator_v2::{Self, Aggregator};

struct Stats has key {
    total_users: Aggregator<u64>  // Concurrent-safe!
}

public fun register_user() acquires Stats {
    let stats = borrow_global_mut<Stats>(@protocol);
    aggregator_v2::add(&mut stats.total_users, 1);
    // Multiple txns can do this in parallel!
}
```

### When to Use Aggregators

**✅ Use aggregators for:**
- Global counters (total users, total volume)
- Protocol-level statistics
- Supply tracking
- Frequently updated metrics

**❌ Don't use aggregators for:**
- Per-user balances (no conflicts)
- Rarely updated values
- Values that need exact reads mid-transaction

### Aggregator Patterns

```move
use aptos_framework::aggregator_v2::{Self, Aggregator};

struct Protocol has key {
    // High-throughput stats
    total_swaps: Aggregator<u64>,
    total_volume: Aggregator<u128>,
    active_pools: Aggregator<u64>,

    // Low-throughput data (use regular fields)
    admin: address,
    fee_rate: u64,
}

public fun initialize(deployer: &signer) {
    move_to(deployer, Protocol {
        total_swaps: aggregator_v2::create_aggregator(0),
        total_volume: aggregator_v2::create_aggregator(0),
        active_pools: aggregator_v2::create_aggregator(0),
        admin: signer::address_of(deployer),
        fee_rate: 30,  // 0.3%
    });
}

public fun record_swap(volume: u128) acquires Protocol {
    let protocol = borrow_global_mut<Protocol>(@my_protocol);

    // Parallel-safe increments
    aggregator_v2::add(&mut protocol.total_swaps, 1);
    aggregator_v2::add(&mut protocol.total_volume, volume);
}

// Reading aggregator value
public fun get_total_volume(): u128 acquires Protocol {
    let protocol = borrow_global<Protocol>(@my_protocol);
    aggregator_v2::read(&protocol.total_volume)
}
```

## Event Optimization

### Event V1 vs V2 Costs

```move
// ❌ Expensive: Event V1 (requires EventHandle)
use aptos_framework::event::{Self, EventHandle};

struct Events has key {
    transfer_events: EventHandle<TransferEvent>  // Storage overhead
}

public fun emit_v1() acquires Events {
    let events = borrow_global_mut<Events>(@module);
    event::emit_event(&mut events.transfer_events, TransferEvent {});
    // Higher gas: borrow_global_mut + emit_event
}

// ✅ Cheap: Event V2 (direct emission)
#[event]
struct TransferEvent has drop, store {
    from: address,
    to: address,
    amount: u64,
}

public fun emit_v2() {
    event::emit(TransferEvent { from: @0x1, to: @0x2, amount: 100 });
    // Lower gas: direct emission
}
```

### Event Size Optimization

```move
// ❌ Bad: Large event payload
#[event]
struct DetailedEvent has drop, store {
    user_address: address,
    user_name: String,           // Expensive!
    full_history: vector<u64>,   // Very expensive!
    timestamp: u64,
    metadata: vector<u8>,        // Expensive!
}

// ✅ Good: Minimal event payload
#[event]
struct OptimizedEvent has drop, store {
    user: address,        // Just the address
    amount: u64,          // Essential data only
    event_type: u8,       // Use codes instead of strings
}

// Off-chain can look up details using user address
```

## Gas Profiling Tools

### Using CLI Gas Profiler

```bash
# Run tests with gas profiling
aptos move test --gas

# Output shows gas usage per function
Running Move unit tests
[ PASS    ] 0x1::my_module::test_transfer
Gas used: 1,234 gas units

# Detailed gas profile
aptos move test --gas --verbose
```

### Simulation and Benchmarking

```bash
# Simulate transaction locally
aptos move run \
  --function-id 0x1::my_module::my_function \
  --args address:0x123 u64:1000 \
  --profile gas

# Output:
# Gas used: 2,500 units
# Storage: +120 bytes
# Estimated cost: 0.0025 APT
```

### In-Code Gas Assertions

```move
#[test]
fun test_gas_usage() {
    let gas_before = aptos_framework::transaction_context::get_gas_used();

    // Operation to test
    expensive_function();

    let gas_after = aptos_framework::transaction_context::get_gas_used();
    let gas_used = gas_after - gas_before;

    assert!(gas_used < 1000, 0);  // Assert max gas
}
```

## Advanced Optimization Patterns

### Pattern 1: Lazy Initialization

```move
// ❌ Bad: Eager initialization (storage cost upfront)
public fun register_user(account: &signer) {
    move_to(account, UserData {
        balance: 0,
        rewards: 0,
        history: vector::empty(),
        config: default_config(),  // Created but might never be used
    });
}

// ✅ Good: Lazy initialization
public fun register_user(account: &signer) {
    move_to(account, UserData {
        balance: 0,
        rewards: 0,
        history: vector::empty(),
        config: option::none(),  // Only create when needed
    });
}

public fun get_or_create_config(user: &mut UserData): &mut Config {
    if (option::is_none(&user.config)) {
        option::fill(&mut user.config, default_config());
    };
    option::borrow_mut(&mut user.config)
}
```

### Pattern 2: Bitmap Flags

```move
// ❌ Bad: Multiple boolean fields (8 bytes)
struct Permissions has store {
    can_mint: bool,      // 1 byte + padding
    can_burn: bool,      // 1 byte + padding
    can_freeze: bool,    // 1 byte + padding
    can_transfer: bool,  // 1 byte + padding
    can_update: bool,    // 1 byte + padding
}

// ✅ Good: Bitmap (1 byte)
struct Permissions has store {
    flags: u8  // All 5 flags in 1 byte
}

const FLAG_MINT: u8 = 0b00001;
const FLAG_BURN: u8 = 0b00010;
const FLAG_FREEZE: u8 = 0b00100;
const FLAG_TRANSFER: u8 = 0b01000;
const FLAG_UPDATE: u8 = 0b10000;

public fun has_permission(perms: &Permissions, flag: u8): bool {
    (perms.flags & flag) != 0
}

public fun set_permission(perms: &mut Permissions, flag: u8, value: bool) {
    if (value) {
        perms.flags = perms.flags | flag;
    } else {
        perms.flags = perms.flags & !flag;
    }
}
```

### Pattern 3: Merkle Proof Verification (Off-Chain Heavy)

```move
// Instead of storing whitelist on-chain
// ❌ Bad: Store entire whitelist (expensive!)
struct Whitelist has key {
    addresses: vector<address>  // 10,000 addresses = huge storage!
}

// ✅ Good: Store only Merkle root (32 bytes)
struct Whitelist has key {
    merkle_root: vector<u8>  // 32 bytes
}

public fun verify_whitelisted(
    user: address,
    proof: vector<vector<u8>>
): bool acquires Whitelist {
    let whitelist = borrow_global<Whitelist>(@module);
    verify_merkle_proof(user, proof, &whitelist.merkle_root)
}

// User provides proof off-chain, we verify on-chain
```

## Cost Comparison Table

| Operation | Gas Cost (approx) | Notes |
|-----------|------------------|-------|
| u64 addition | 1 | Primitive op |
| u64 multiplication | 2 | Primitive op |
| Vector push_back | 5-10 | Depends on size |
| Table lookup | 10-15 | O(1) access |
| SmartTable lookup | 10-15 | O(1) access |
| borrow_global | 20-50 | Depends on resource size |
| move_to | 50-200 | Depends on resource size |
| Event emission (V2) | 50-100 | Per event |
| Event emission (V1) | 100-200 | Higher overhead |
| String operation | 10-50 | Depends on length |
| Cryptographic hash | 100-500 | SHA256, etc |

## Best Practices Summary

### ✅ Do

- **Use aggregators for global counters** - Enable parallel execution
- **Use inline for small functions** - Reduce call overhead
- **Cache vector lengths in loops** - Avoid repeated calls
- **Use Event V2** - Cheaper than V1
- **Batch operations** - Single transaction vs multiple
- **Minimize storage** - Store only essential data
- **Use Table/SmartTable for large datasets** - Not vectors
- **Pack booleans into bitmaps** - Save storage space
- **Profile with --gas flag** - Measure before optimizing

### ❌ Avoid

- **Don't iterate over Tables** - Not supported
- **Don't store redundant data** - Calculate on-demand
- **Don't use large event payloads** - Keep events minimal
- **Don't access global storage repeatedly** - Borrow once
- **Don't use vector for large datasets** - Use Table/SmartTable
- **Don't inline large functions** - Increases code size
- **Don't optimize prematurely** - Profile first

## Gas Optimization Checklist

Before deploying to mainnet:

- [ ] Run `aptos move test --gas` and review gas usage
- [ ] Use aggregators for all global counters
- [ ] Inline small helper functions
- [ ] Use Event V2 for all events
- [ ] Use Table/SmartTable for large datasets
- [ ] Minimize struct sizes (pack fields efficiently)
- [ ] Cache loop lengths and frequently accessed values
- [ ] Batch operations where possible
- [ ] Use bitmap flags instead of multiple booleans
- [ ] Store Merkle roots instead of full lists
- [ ] Early returns for validation logic
- [ ] Minimize global storage access

## Response Style

- **Measure-first** - Always profile before optimizing
- **Pattern-driven** - Show before/after optimization patterns
- **Cost-aware** - Mention gas implications explicitly
- **Practical** - Real-world optimization examples
- **Tool-focused** - Reference profiling commands

## Follow-up Suggestions

After helping with gas optimization, suggest:
- Profile specific functions with --gas flag
- Implement aggregators for high-throughput paths
- Review storage structure efficiency
- Consider parallel execution opportunities
- Benchmark against similar protocols
- Set up gas regression tests
