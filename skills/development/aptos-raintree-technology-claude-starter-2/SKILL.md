---
name: aptos
description: Aptos blockchain and Move language expert. Covers Move programming (abilities, generics, resources), Aptos framework modules, smart contract development, token standards (Coin, Fungible Asset, Digital Asset), object model, gas optimization, and dApp integration. Triggers on Aptos, Move language, Move smart contract, Aptos blockchain, abilities, generics, resources, fungible asset, digital asset.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
license: MIT
metadata:
  author: raintree
  version: "1.0"
---

# Aptos Blockchain & Move Language Expert

Aptos is a Layer 1 blockchain with the Move programming language, designed for safe and scalable smart contracts.

## When to Use

- Writing Move smart contracts
- Understanding Move type system (abilities, generics, resources)
- Using Aptos framework modules (coin, fungible_asset, object)
- Token standards (Coin, Fungible Asset, Digital Asset/NFT)
- Gas optimization and testing
- dApp integration with TypeScript SDK

## Move Language Fundamentals

### Abilities - Move's Core Feature

Every type has abilities that control what you can do with it:

| Ability | Meaning | Example |
|---------|---------|---------|
| `copy` | Can be duplicated | Primitives, configs |
| `drop` | Can be discarded | Temporary data |
| `store` | Can be stored in structs | Most data types |
| `key` | Can be top-level resource | Account resources |

```move
// Resource that can be stored globally
struct Balance has key, store {
    coins: u64
}

// Value type that behaves like a primitive
struct Point has copy, drop, store {
    x: u64,
    y: u64
}

// No abilities = must be explicitly handled (hot potato)
struct Receipt {
    amount: u64
}
```

### Generics and Phantom Types

```move
// Type parameter with ability constraint
struct Box<T: store> has key {
    value: T
}

// Phantom type - zero runtime cost, type safety only
struct Coin<phantom CoinType> has store {
    value: u64
}

// Different types can't be mixed
let btc: Coin<BTC> = Coin { value: 100 };
let eth: Coin<ETH> = Coin { value: 50 };
// btc + eth → compile error!
```

### Global Storage Operations

```move
// Store resource at signer's address
public fun initialize(account: &signer) {
    move_to(account, MyResource { value: 0 });
}

// Read resource (requires acquires annotation)
public fun get_value(addr: address): u64 acquires MyResource {
    borrow_global<MyResource>(addr).value
}

// Modify resource
public fun set_value(addr: address, val: u64) acquires MyResource {
    borrow_global_mut<MyResource>(addr).value = val;
}

// Check existence
public fun exists_at(addr: address): bool {
    exists<MyResource>(addr)
}

// Remove and return resource
public fun destroy(addr: address): MyResource acquires MyResource {
    move_from<MyResource>(addr)
}
```

### Signer - Authentication

```move
use std::signer;

// Only the account owner can call this
public entry fun transfer(
    sender: &signer,
    recipient: address,
    amount: u64
) acquires Balance {
    let sender_addr = signer::address_of(sender);
    // sender proves ownership of sender_addr
}
```

### Visibility Modifiers

```move
module example {
    // Private (default) - only within module
    fun internal() { }

    // Public - callable from anywhere
    public fun library_fn() { }

    // Friend - only from declared friend modules
    public(friend) fun restricted() { }

    // Entry - transaction entry point
    public entry fun user_action(account: &signer) { }
}
```

## Aptos Framework (0x1)

### Core Modules

| Module | Purpose |
|--------|---------|
| `account` | Account creation, auth key rotation |
| `coin` | Original fungible token standard |
| `fungible_asset` | New flexible token standard |
| `object` | Object model for composable assets |
| `aptos_coin` | Native APT token |
| `timestamp` | Block timestamp |
| `event` | Event emission |

### Coin Standard (0x1::coin)

```move
use aptos_framework::coin;

// Register to receive a coin type
public entry fun register<CoinType>(account: &signer) {
    coin::register<CoinType>(account);
}

// Transfer coins
public entry fun transfer<CoinType>(
    from: &signer,
    to: address,
    amount: u64
) {
    coin::transfer<CoinType>(from, to, amount);
}

// Check balance
public fun balance<CoinType>(addr: address): u64 {
    coin::balance<CoinType>(addr)
}
```

### Fungible Asset Standard (0x1::fungible_asset)

Modern, flexible token standard:

```move
use aptos_framework::fungible_asset::{Self, FungibleAsset, Metadata};
use aptos_framework::primary_fungible_store;

// Create fungible asset metadata
public fun create_fa(creator: &signer): Object<Metadata> {
    let constructor_ref = object::create_named_object(creator, b"MY_FA");
    
    primary_fungible_store::create_primary_store_enabled_fungible_asset(
        &constructor_ref,
        option::none(), // max supply
        utf8(b"My Token"),
        utf8(b"MTK"),
        8, // decimals
        utf8(b"https://example.com/icon.png"),
        utf8(b"https://example.com"),
    );
    
    object::object_from_constructor_ref(&constructor_ref)
}

// Transfer FA
public entry fun transfer_fa(
    sender: &signer,
    metadata: Object<Metadata>,
    recipient: address,
    amount: u64
) {
    primary_fungible_store::transfer(sender, metadata, recipient, amount);
}
```

### Object Model (0x1::object)

Composable, transferable objects:

```move
use aptos_framework::object::{Self, Object, ConstructorRef};

struct MyObject has key {
    value: u64
}

// Create object
public fun create(creator: &signer): Object<MyObject> {
    let constructor_ref = object::create_object(signer::address_of(creator));
    let object_signer = object::generate_signer(&constructor_ref);
    
    move_to(&object_signer, MyObject { value: 42 });
    
    object::object_from_constructor_ref(&constructor_ref)
}

// Transfer object
public entry fun transfer_object(
    owner: &signer,
    obj: Object<MyObject>,
    recipient: address
) {
    object::transfer(owner, obj, recipient);
}
```

## Token Standards

### Digital Asset (NFT) Standard

```move
use aptos_token_objects::collection;
use aptos_token_objects::token;

// Create collection
public entry fun create_collection(creator: &signer) {
    collection::create_unlimited_collection(
        creator,
        utf8(b"My Collection Description"),
        utf8(b"My Collection"),
        option::none(), // royalty
        utf8(b"https://example.com/collection"),
    );
}

// Mint token
public entry fun mint_token(creator: &signer, to: address) {
    let token_constructor_ref = token::create(
        creator,
        utf8(b"My Collection"),
        utf8(b"Token description"),
        utf8(b"Token #1"),
        option::none(), // royalty
        utf8(b"https://example.com/token/1"),
    );
    
    let transfer_ref = object::generate_transfer_ref(&token_constructor_ref);
    let linear_transfer_ref = object::generate_linear_transfer_ref(&transfer_ref);
    object::transfer_with_ref(linear_transfer_ref, to);
}
```

## Common Patterns

### Capability Pattern

```move
struct AdminCap has key, store {}

public fun init_module(deployer: &signer) {
    move_to(deployer, AdminCap {});
}

public entry fun admin_only(admin: &signer) acquires AdminCap {
    assert!(exists<AdminCap>(signer::address_of(admin)), E_NOT_ADMIN);
    // Admin-only logic
}
```

### Resource Account

```move
use aptos_framework::resource_account;

// Create resource account for deterministic addresses
public fun create_resource_account(creator: &signer): signer {
    let (resource_signer, _cap) = resource_account::create_resource_account(
        creator,
        b"seed"
    );
    resource_signer
}
```

### Events

```move
use aptos_framework::event;

#[event]
struct TransferEvent has drop, store {
    from: address,
    to: address,
    amount: u64,
}

public fun emit_transfer(from: address, to: address, amount: u64) {
    event::emit(TransferEvent { from, to, amount });
}
```

## Testing

```move
#[test]
fun test_basic() {
    let x = 1 + 1;
    assert!(x == 2, 0);
}

#[test(account = @0x123)]
fun test_with_signer(account: &signer) {
    let addr = signer::address_of(account);
    assert!(addr == @0x123, 0);
}

#[test]
#[expected_failure(abort_code = E_NOT_FOUND)]
fun test_expected_failure() {
    abort E_NOT_FOUND
}
```

## CLI Commands

```bash
# Initialize project
aptos init

# Compile
aptos move compile

# Test
aptos move test

# Publish
aptos move publish --profile mainnet

# Run function
aptos move run --function-id 'addr::module::function'
```

## Gas Optimization

- Use `inline` for small frequently-called functions
- Prefer `Table` over `vector` for large collections
- Minimize storage operations (most expensive)
- Use `SmartTable` for parallel execution
- Batch operations when possible

## TypeScript SDK

```typescript
import { Aptos, AptosConfig, Network } from "@aptos-labs/ts-sdk";

const config = new AptosConfig({ network: Network.MAINNET });
const aptos = new Aptos(config);

// Query account balance
const balance = await aptos.getAccountAPTAmount({
    accountAddress: "0x1"
});

// Submit transaction
const txn = await aptos.transaction.build.simple({
    sender: account.accountAddress,
    data: {
        function: "0x1::coin::transfer",
        typeArguments: ["0x1::aptos_coin::AptosCoin"],
        functionArguments: [recipientAddress, amount],
    },
});

const result = await aptos.signAndSubmitTransaction({
    signer: account,
    transaction: txn,
});
```

## Resources

- **Docs:** https://aptos.dev
- **Move Book:** https://move-book.com
- **Framework:** https://github.com/aptos-labs/aptos-core/tree/main/aptos-move/framework
- **SDK:** https://github.com/aptos-labs/aptos-ts-sdk
