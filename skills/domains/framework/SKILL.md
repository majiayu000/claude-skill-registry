---
name: aptos-framework
description: Expert on Aptos Framework (0x1 standard library) - account, coin, fungible_asset, object, timestamp, table, event, vector, string, option, error, and other core modules. Triggers on keywords aptos framework, 0x1, account module, table, smarttable, event, timestamp, randomness, aggregator, resource account
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

# Aptos Framework Expert

## Purpose

Provide comprehensive guidance on the Aptos Framework (0x1 address) - the standard library of core modules that power Aptos blockchain. These modules provide fundamental functionality for accounts, storage, events, randomness, and more.

## When to Use

Auto-invoke when users mention:
- **Framework Modules** - 0x1::*, aptos_framework::*, standard library
- **Account Management** - account creation, auth keys, rotation
- **Storage** - Table, SimpleMap, SmartTable, efficient data structures
- **Events** - event emission, event handles, indexing
- **Randomness** - VRF, secure random numbers
- **Time** - timestamp, block time access
- **Resources** - resource accounts, deterministic addresses
- **Aggregator** - parallel execution primitives

## Framework Architecture

### Core Framework Modules (0x1::)

```
aptos_framework/
├── account.move           - Account management
├── aptos_account.move     - High-level account operations
├── aptos_coin.move        - Native APT token
├── aptos_governance.move  - On-chain governance
├── coin.move              - Fungible token standard (v1)
├── fungible_asset.move    - Fungible asset standard (v2)
├── object.move            - Object model primitives
├── timestamp.move         - Block timestamp access
├── table.move             - Key-value storage
├── smart_table.move       - Auto-split table
├── event.move             - Event emission
├── randomness.move        - Secure randomness
├── aggregator.move        - Parallel execution
├── aggregator_v2.move     - Improved aggregator
├── resource_account.move  - Deterministic deployment
├── transaction_fee.move   - Fee collection
└── staking_contract.move  - Validator staking
```

### Standard Library (std::)

```
move-stdlib/
├── vector.move      - Dynamic arrays
├── option.move      - Optional values
├── string.move      - UTF8 strings
├── signer.move      - Signer operations
├── error.move       - Error codes
├── bcs.move         - Binary serialization
├── hash.move        - Cryptographic hashing
└── fixed_point64.move - Fixed-point math
```

## account.move - Account Management

### Core Functions

```move
use aptos_framework::account;

// Create new account at address
public fun create_account(new_address: address) {
    account::create_account(new_address);
}

// Get account's sequence number
public fun get_sequence_number(addr: address): u64 {
    account::get_sequence_number(addr)
}

// Get authentication key
public fun get_authentication_key(addr: address): vector<u8> {
    account::get_authentication_key(addr)
}

// Check if account exists
public fun exists_at(addr: address): bool {
    account::exists_at(addr)
}
```

### Account Rotation

```move
// Rotate authentication key
public entry fun rotate_authentication_key(
    account: &signer,
    new_auth_key: vector<u8>
) {
    account::rotate_authentication_key(account, new_auth_key);
}

// Offer rotation capability to another address
public entry fun offer_rotation_capability(
    account: &signer,
    rotation_capability_offerer: address
) {
    account::offer_rotation_capability(
        account,
        rotation_capability_offerer,
        vector::empty()
    );
}
```

### SignerCapability Pattern

```move
use aptos_framework::account::{Self, SignerCapability};

struct ModuleData has key {
    signer_cap: SignerCapability
}

public fun initialize(deployer: &signer) {
    let (resource_signer, signer_cap) = account::create_resource_account(
        deployer,
        b"SEED"
    );

    move_to(&resource_signer, ModuleData { signer_cap });
}

public fun use_resource_account() acquires ModuleData {
    let module_data = borrow_global<ModuleData>(@my_module);
    let resource_signer = account::create_signer_with_capability(&module_data.signer_cap);

    // Use resource_signer for operations
}
```

## table.move - Scalable Key-Value Storage

### Basic Table Operations

```move
use aptos_framework::table::{Self, Table};

struct Registry has key {
    data: Table<address, UserData>
}

public fun initialize(account: &signer) {
    move_to(account, Registry {
        data: table::new()
    });
}

public fun add_user(
    registry_addr: address,
    user_addr: address,
    user_data: UserData
) acquires Registry {
    let registry = borrow_global_mut<Registry>(registry_addr);
    table::add(&mut registry.data, user_addr, user_data);
}

public fun get_user(
    registry_addr: address,
    user_addr: address
): &UserData acquires Registry {
    let registry = borrow_global<Registry>(registry_addr);
    table::borrow(&registry.data, user_addr)
}

public fun update_user(
    registry_addr: address,
    user_addr: address
): &mut UserData acquires Registry {
    let registry = borrow_global_mut<Registry>(registry_addr);
    table::borrow_mut(&mut registry.data, user_addr)
}

public fun remove_user(
    registry_addr: address,
    user_addr: address
): UserData acquires Registry {
    let registry = borrow_global_mut<Registry>(registry_addr);
    table::remove(&mut registry.data, user_addr)
}

public fun has_user(
    registry_addr: address,
    user_addr: address
): bool acquires Registry {
    let registry = borrow_global<Registry>(registry_addr);
    table::contains(&registry.data, user_addr)
}
```

### Table vs SimpleMap vs SmartTable

| Feature | Vector | SimpleMap | Table | SmartTable |
|---------|--------|-----------|-------|------------|
| Max size | ~1000 | ~1000 | Unlimited | Unlimited |
| Gas cost (read) | O(n) | O(n) | O(1) | O(1) |
| Gas cost (write) | O(n) | O(n) | O(1) | O(1) |
| Storage | On-chain | On-chain | Global storage | Global + auto-split |
| Iteration | ✅ Easy | ✅ Easy | ❌ Not supported | ⚠️ Complex |
| Best for | Small lists | Small maps | Large maps | Very large maps |

### SmartTable (Auto-Splitting)

```move
use aptos_framework::smart_table::{Self, SmartTable};

struct LargeRegistry has key {
    data: SmartTable<address, UserData>
}

public fun initialize(account: &signer) {
    move_to(account, LargeRegistry {
        data: smart_table::new()
    });
}

// Same API as Table
public fun add_user(addr: address, data: UserData) acquires LargeRegistry {
    let registry = borrow_global_mut<LargeRegistry>(@my_module);
    smart_table::add(&mut registry.data, addr, data);
}

// SmartTable automatically splits when buckets get large
// Better for very large datasets (100k+ entries)
```

## event.move - Event Emission

### Event Handles (V1)

```move
use aptos_framework::event::{Self, EventHandle};

struct TransferEvent has drop, store {
    from: address,
    to: address,
    amount: u64,
}

struct Events has key {
    transfer_events: EventHandle<TransferEvent>
}

public fun initialize(account: &signer) {
    move_to(account, Events {
        transfer_events: account::new_event_handle<TransferEvent>(account)
    });
}

public fun emit_transfer(
    from: address,
    to: address,
    amount: u64
) acquires Events {
    let events = borrow_global_mut<Events>(@my_module);
    event::emit_event(&mut events.transfer_events, TransferEvent {
        from,
        to,
        amount,
    });
}
```

### Event API (V2 - Recommended)

```move
use aptos_framework::event;

#[event]
struct TransferEvent has drop, store {
    from: address,
    to: address,
    amount: u64,
}

public fun transfer(from: address, to: address, amount: u64) {
    // Direct emission (no EventHandle needed!)
    event::emit(TransferEvent { from, to, amount });
}
```

**Event V2 Advantages:**
- No EventHandle management
- Cleaner code
- Better indexing support
- Automatic event routing

## timestamp.move - Block Time

```move
use aptos_framework::timestamp;

public fun get_current_time(): u64 {
    timestamp::now_seconds()
}

public fun get_current_time_microseconds(): u64 {
    timestamp::now_microseconds()
}

// Time-based logic
public fun is_expired(deadline: u64): bool {
    timestamp::now_seconds() >= deadline
}

public fun create_with_deadline(duration: u64): u64 {
    timestamp::now_seconds() + duration
}
```

**Important:** Block timestamp is set by validators, can have small drift.

## randomness.move - Secure Randomness

### VRF-based Random Numbers

```move
use aptos_framework::randomness;

#[randomness]
public entry fun random_mint(user: &signer) {
    let random_value = randomness::u64_integer();

    let rarity = if (random_value % 100 < 1) {
        // 1% chance - legendary
        3
    } else if (random_value % 100 < 10) {
        // 9% chance - rare
        2
    } else {
        // 90% chance - common
        1
    };

    mint_nft(user, rarity);
}

// Random in range
#[randomness]
public entry fun random_reward(user: &signer) {
    let amount = randomness::u64_range(100, 1000); // 100 to 999
    transfer_reward(user, amount);
}
```

**Requirements:**
- Must use `#[randomness]` attribute
- Must be entry function
- Only works on-chain (not in view functions)

### Random Bytes

```move
#[randomness]
public entry fun random_selection() {
    let random_bytes = randomness::bytes(32); // 32 random bytes
    // Use for cryptographic purposes
}
```

## resource_account.move - Deterministic Deployment

### Creating Resource Accounts

```move
use aptos_framework::resource_account;
use aptos_framework::account;

public fun create_resource_acct(deployer: &signer) {
    let seed = b"MY_RESOURCE";

    // Create resource account
    let (resource_signer, signer_cap) = account::create_resource_account(
        deployer,
        seed
    );

    // Resource account address is deterministic:
    // hash(deployer_address, seed)
    let resource_addr = signer::address_of(&resource_signer);

    // Store signer capability to use later
    move_to(&resource_signer, ResourceData {
        signer_cap
    });
}
```

### Use Cases for Resource Accounts

1. **Module Storage** - Store module data at predictable address
2. **Liquidity Pools** - Each pool at deterministic address
3. **Protocol Treasuries** - Controlled programmatically
4. **Registry Systems** - Well-known addresses

```move
// Example: Liquidity Pool at deterministic address
public fun create_pool<X, Y>(deployer: &signer) {
    let seed = b"POOL_";
    vector::append(&mut seed, type_name<X>());
    vector::append(&mut seed, b"_");
    vector::append(&mut seed, type_name<Y>());

    let (pool_signer, signer_cap) = account::create_resource_account(
        deployer,
        seed
    );

    move_to(&pool_signer, Pool<X, Y> {
        reserve_x: 0,
        reserve_y: 0,
        signer_cap,
    });
}
```

## aggregator_v2.move - Parallel Execution

### Aggregators for Concurrent Modification

```move
use aptos_framework::aggregator_v2::{Self, Aggregator};

struct Stats has key {
    total_users: Aggregator<u64>,
    total_volume: Aggregator<u64>,
}

public fun initialize(account: &signer) {
    move_to(account, Stats {
        total_users: aggregator_v2::create_aggregator(0),
        total_volume: aggregator_v2::create_aggregator(0),
    });
}

public fun increment_users() acquires Stats {
    let stats = borrow_global_mut<Stats>(@my_module);
    aggregator_v2::add(&mut stats.total_users, 1);
}

public fun add_volume(amount: u64) acquires Stats {
    let stats = borrow_global_mut<Stats>(@my_module);
    aggregator_v2::add(&mut stats.total_volume, amount);
}

public fun get_total_users(): u64 acquires Stats {
    let stats = borrow_global<Stats>(@my_module);
    aggregator_v2::read(&stats.total_users)
}
```

**Why Use Aggregators:**
- Enable parallel transaction execution
- Multiple transactions can increment same aggregator concurrently
- No conflicts/retries like regular u64 fields
- **Critical for high-throughput protocols**

## option.move - Optional Values

```move
use std::option::{Self, Option};

struct Profile has key {
    name: String,
    bio: Option<String>,  // Optional field
}

public fun create_profile(account: &signer, name: String) {
    move_to(account, Profile {
        name,
        bio: option::none()  // No bio initially
    });
}

public fun set_bio(account: &signer, bio: String) acquires Profile {
    let addr = signer::address_of(account);
    let profile = borrow_global_mut<Profile>(addr);

    if (option::is_some(&profile.bio)) {
        // Update existing bio
        *option::borrow_mut(&mut profile.bio) = bio;
    } else {
        // Set bio for first time
        option::fill(&mut profile.bio, bio);
    }
}

public fun get_bio(addr: address): Option<String> acquires Profile {
    let profile = borrow_global<Profile>(addr);
    option::clone(&profile.bio)
}

// Using option value
public fun print_bio(addr: address) acquires Profile {
    let bio_opt = get_bio(addr);
    if (option::is_some(&bio_opt)) {
        let bio = option::extract(&mut bio_opt);
        // Use bio
    } else {
        // No bio set
    }
}
```

## string.move - UTF8 Strings

```move
use std::string::{Self, String};

public fun create_message(): String {
    string::utf8(b"Hello, Aptos!")
}

public fun concatenate(s1: String, s2: String): String {
    let mut result = s1;
    string::append(&mut result, s2);
    result
}

public fun substring(s: &String, start: u64, end: u64): String {
    string::sub_string(s, start, end)
}

public fun string_length(s: &String): u64 {
    string::length(s)
}

// String to bytes
public fun to_bytes(s: &String): vector<u8> {
    *string::bytes(s)
}
```

## vector.move - Dynamic Arrays

```move
use std::vector;

public fun vector_operations() {
    let mut v = vector::empty<u64>();

    // Add elements
    vector::push_back(&mut v, 10);
    vector::push_back(&mut v, 20);
    vector::push_back(&mut v, 30);

    // Get length
    let len = vector::length(&v);  // 3

    // Access elements
    let first = *vector::borrow(&v, 0);  // 10

    // Modify elements
    let second = vector::borrow_mut(&mut v, 1);
    *second = 25;

    // Remove element
    let last = vector::pop_back(&mut v);  // 30

    // Check if contains
    let has_ten = vector::contains(&v, &10);  // true

    // Find index
    let (found, index) = vector::index_of(&v, &25);

    // Reverse
    vector::reverse(&mut v);

    // Append another vector
    vector::append(&mut v, vector[40, 50]);

    // Remove and return element
    let removed = vector::remove(&mut v, 0);

    // Swap elements
    vector::swap(&mut v, 0, 1);
}
```

## Common Patterns

### Pattern 1: Registry with Table

```move
use aptos_framework::table::{Self, Table};

struct Registry<K: copy + drop, V: store> has key {
    data: Table<K, V>,
    count: u64,
}

public fun initialize<K: copy + drop, V: store>(account: &signer) {
    move_to(account, Registry<K, V> {
        data: table::new(),
        count: 0,
    });
}

public fun register<K: copy + drop, V: store>(
    registry_addr: address,
    key: K,
    value: V
) acquires Registry {
    let registry = borrow_global_mut<Registry<K, V>>(registry_addr);
    assert!(!table::contains(&registry.data, key), ERROR_ALREADY_EXISTS);

    table::add(&mut registry.data, key, value);
    registry.count = registry.count + 1;
}
```

### Pattern 2: Event-Driven State Changes

```move
#[event]
struct StateChanged has drop, store {
    old_state: u8,
    new_state: u8,
    timestamp: u64,
}

public fun change_state(new_state: u8) acquires State {
    let state = borrow_global_mut<State>(@my_module);
    let old = state.value;

    state.value = new_state;

    event::emit(StateChanged {
        old_state: old,
        new_state,
        timestamp: timestamp::now_seconds(),
    });
}
```

### Pattern 3: Time-Locked Operations

```move
struct TimeLock has key {
    unlock_time: u64,
    amount: u64,
}

public fun create_timelock(
    account: &signer,
    amount: u64,
    lock_duration: u64
) {
    let unlock_time = timestamp::now_seconds() + lock_duration;

    move_to(account, TimeLock {
        unlock_time,
        amount,
    });
}

public fun withdraw(account: &signer) acquires TimeLock {
    let addr = signer::address_of(account);
    let timelock = move_from<TimeLock>(addr);

    assert!(
        timestamp::now_seconds() >= timelock.unlock_time,
        ERROR_STILL_LOCKED
    );

    let TimeLock { unlock_time: _, amount } = timelock;
    // Transfer amount to user
}
```

### Pattern 4: Resource Account Pool

```move
struct Pool<phantom X, phantom Y> has key {
    reserve_x: u64,
    reserve_y: u64,
    signer_cap: SignerCapability,
}

public fun create_pool<X, Y>(creator: &signer) {
    let seed = b"POOL";
    let (pool_signer, signer_cap) = account::create_resource_account(
        creator,
        seed
    );

    coin::register<X>(&pool_signer);
    coin::register<Y>(&pool_signer);

    move_to(&pool_signer, Pool<X, Y> {
        reserve_x: 0,
        reserve_y: 0,
        signer_cap,
    });
}

public fun swap<X, Y>(amount_in: u64): u64 acquires Pool {
    let pool_addr = account::create_resource_address(&@my_module, b"POOL");
    let pool = borrow_global_mut<Pool<X, Y>>(pool_addr);

    // Swap logic using signer_cap for transfers
    let pool_signer = account::create_signer_with_capability(&pool.signer_cap);
    // ...
}
```

## Framework Module Reference

### Quick Reference Table

| Module | Key Functions | Use Case |
|--------|--------------|----------|
| account | create_account, rotate_authentication_key | Account management |
| coin | transfer, balance, register | Fungible tokens |
| fungible_asset | mint, burn, transfer | Advanced tokens |
| object | create_object, transfer | Object model |
| table | add, borrow, remove | Large key-value stores |
| smart_table | add, borrow, remove | Very large stores |
| event | emit, emit_event | Event emission |
| timestamp | now_seconds | Time access |
| randomness | u64_integer, bytes | Secure randomness |
| aggregator_v2 | create, add, read | Parallel execution |
| resource_account | create_resource_account | Deterministic addresses |

## Best Practices

### ✅ Do

- **Use SmartTable for large datasets** - Better than Table for 100k+ entries
- **Use Event V2 API** - Simpler than EventHandle
- **Use Aggregator for counters** - Enables parallel execution
- **Use resource accounts for protocols** - Deterministic addresses
- **Check timestamp carefully** - Validator-set, can have drift
- **Use randomness for fair selection** - VRF-based security

### ❌ Avoid

- **Don't iterate over Tables** - Not supported, use vector/map if needed
- **Don't trust timestamp for exact timing** - Block-level granularity
- **Don't use randomness in view functions** - Not supported
- **Don't forget to handle Option::none** - Check before unwrapping
- **Don't create too many event handles** - Use Event V2 instead

## Response Style

- **Module-focused** - Reference specific framework modules
- **Pattern-driven** - Show common framework usage patterns
- **Performance-aware** - Mention gas implications
- **Practical** - Real-world examples with framework modules
- **Reference docs** - Link to specific module documentation

## Follow-up Suggestions

After helping with framework modules, suggest:
- Gas optimization for storage structures
- Event indexing strategies
- Parallel execution with aggregators
- Resource account architectures
- Time-based protocol designs
- Random number generation patterns
