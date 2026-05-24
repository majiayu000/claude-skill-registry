---
name: aptos-move-language
description: Expert on Move programming language - abilities (copy/drop/store/key), generics, phantom types, references, global storage operations, signer pattern, visibility modifiers, friend functions, inline optimization, and advanced type system. Triggers on keywords move language, abilities, generics, phantom type, borrow global, signer, friend, inline, type parameter
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

# Move Language Expert

## Purpose

Provide deep expertise on the Move programming language, focusing on its unique type system, abilities, generics, resource safety, and Aptos-specific features. Move is designed for safe digital asset programming with linear types and formal verification support.

## When to Use

Auto-invoke when users mention:
- **Abilities** - copy, drop, store, key, ability constraints
- **Generics** - type parameters, phantom types, constraints
- **References** - borrowing, &T, &mut T, borrow_global
- **Global Storage** - move_to, move_from, exists, borrow_global_mut
- **Signer** - authentication, signer pattern, access control
- **Visibility** - public, public(friend), entry, private
- **Advanced** - inline, friend functions, spec blocks

## Move Language Fundamentals

### Type System Overview

Move is a **statically typed, compiled language** with:
- **Linear types** (resources can't be copied or dropped arbitrarily)
- **Generics** with ability constraints
- **No null/undefined** - explicit Option<T>
- **No dynamic dispatch** - all calls resolved at compile time
- **Memory safety** without garbage collection

### Primitive Types

```move
// Integers
let x: u8 = 255;         // 0 to 255
let y: u16 = 65535;      // 0 to 65,535
let z: u32 = 4294967295; // 0 to 4,294,967,295
let w: u64 = 18446744073709551615; // 0 to 2^64-1
let v: u128 = 340282366920938463463374607431768211455; // 0 to 2^128-1
let t: u256 = 115792089237316195423570985008687907853269984665640564039457584007913129639935; // 0 to 2^256-1

// Boolean
let flag: bool = true;

// Address
let addr: address = @0x1;
let named: address = @aptos_framework;

// Vectors
let nums: vector<u64> = vector[1, 2, 3];
let empty: vector<address> = vector::empty();
```

### No Implicit Conversions

```move
let x: u8 = 10;
let y: u64 = 20;

// ❌ Error: type mismatch
// let z = x + y;

// ✅ Correct: explicit casting
let z = (x as u64) + y;
```

## Abilities - Move's Type Superpowers

### The Four Abilities

```move
struct Resource has key, store {
    value: u64
}
// key:   Can be stored in global storage as a top-level resource
// store: Can be stored inside other structs
// copy:  Can be copied (duplicated)
// drop:  Can be dropped/discarded
```

### Ability Semantics

| Ability | Meaning | Example Use Case |
|---------|---------|------------------|
| `copy` | Type can be copied by value | Primitives, small configs |
| `drop` | Type can be discarded | References, temporary data |
| `store` | Can be stored in structs/global storage | Most data types |
| `key` | Can be top-level resource in global storage | Account resources, NFTs |

### Ability Constraints

```move
// No abilities - can't copy, drop, store, or use as resource
struct Capability {}

// Only store - can be inside structs, but not global storage
struct InnerData has store {
    value: u64
}

// store + key - can be global resource
struct Account has store, key {
    balance: u64,
    inner: InnerData,  // ✅ InnerData has store
}

// copy + drop + store - behaves like primitive
struct Point has copy, drop, store {
    x: u64,
    y: u64,
}
```

### Critical Rules

**Rule 1:** Fields must have compatible abilities
```move
// ❌ ERROR: InnerData doesn't have 'key'
struct Account has key {
    data: InnerData  // InnerData needs 'store' at minimum
}

// ✅ CORRECT
struct Account has key {
    data: InnerData  // InnerData has 'store'
}
```

**Rule 2:** Structs without `drop` must be explicitly handled
```move
struct NoDrop has store, key {
    value: u64
}

fun use_no_drop(nd: NoDrop) {
    // ❌ ERROR: Can't drop NoDrop
    // Function ends and nd is dropped implicitly
}

fun use_no_drop_correct(nd: NoDrop) {
    // ✅ Must explicitly destructure or store
    let NoDrop { value: _ } = nd;  // Unpack and drop fields
}
```

**Rule 3:** `copy` requires all fields to have `copy`
```move
struct NotCopyable has store {
    x: u64
}

// ❌ ERROR: Can't have copy because NotCopyable doesn't
struct Container has copy {
    inner: NotCopyable
}

// ✅ CORRECT
struct Container has store {
    inner: NotCopyable
}
```

## Generics and Type Parameters

### Basic Generics

```move
struct Box<T> has store {
    value: T
}

struct Pair<T1, T2> has store {
    first: T1,
    second: T2,
}

public fun create_box<T: store>(value: T): Box<T> {
    Box { value }
}
```

### Ability Constraints on Type Parameters

```move
// T must have 'store' ability
public fun store_in_box<T: store>(value: T): Box<T> {
    Box { value }
}

// T must have 'copy + drop'
public fun duplicate<T: copy + drop>(value: T): (T, T) {
    (value, copy value)
}

// T must have all abilities
public fun full_featured<T: copy + drop + store + key>(value: T) {
    // Can do anything with T
}

// No constraints (very limited - can only pass around)
public fun unconstrained<T>(value: T): T {
    value  // Can't copy, can't drop, can't store
}
```

### Phantom Type Parameters

Phantom types don't appear in struct fields but affect type safety:

```move
struct Coin<phantom CoinType> has store {
    value: u64  // CoinType doesn't appear here!
}

struct BTC {}
struct ETH {}

// These are different types!
let btc: Coin<BTC> = Coin { value: 100 };
let eth: Coin<ETH> = Coin { value: 50 };

// ❌ ERROR: Type mismatch
// let mixed = btc + eth;
```

**Why Phantom Types?**
- Zero runtime overhead (erased at compile time)
- Type-level guarantees (can't mix BTC and ETH)
- Ability inheritance doesn't require CoinType to have abilities

```move
// Even if SomeCoin doesn't have 'store', Coin<SomeCoin> can have it
struct SomeCoin {}  // No abilities!

struct Coin<phantom CoinType> has store {
    value: u64
}

// ✅ Works! Phantom type doesn't affect abilities
let coin: Coin<SomeCoin> = Coin { value: 100 };
```

### Multiple Type Parameters

```move
struct Pool<phantom X, phantom Y> has key {
    reserve_x: u64,
    reserve_y: u64,
    lp_supply: u64,
}

public fun create_pool<X, Y>(account: &signer) {
    move_to(account, Pool<X, Y> {
        reserve_x: 0,
        reserve_y: 0,
        lp_supply: 0,
    });
}

// Pool<BTC, ETH> ≠ Pool<ETH, BTC>
```

## References and Borrowing

### Immutable References (&T)

```move
fun read_value(x: &u64): u64 {
    *x  // Dereference to read
}

let val = 42;
let ref = &val;
let copy = *ref;  // copy is 42, val is still 42
```

### Mutable References (&mut T)

```move
fun increment(x: &mut u64) {
    *x = *x + 1;
}

let mut val = 42;
increment(&mut val);
// val is now 43
```

### Reference Rules

1. **Can't have mutable + immutable refs simultaneously**
```move
let mut x = 10;
let r1 = &x;
let r2 = &mut x;  // ❌ ERROR: Can't have both
```

2. **Only one mutable reference at a time**
```move
let mut x = 10;
let r1 = &mut x;
let r2 = &mut x;  // ❌ ERROR: x already borrowed mutably
```

3. **References can't outlive their values**
```move
fun get_ref(): &u64 {
    let x = 42;
    &x  // ❌ ERROR: Can't return ref to local variable
}
```

### Reference Copying for `copy` Types

```move
fun copy_from_ref(x: &u64): u64 {
    *x  // ✅ u64 has copy, so this works
}

struct NoCopy has store {}

fun copy_from_ref_no_copy(x: &NoCopy): NoCopy {
    *x  // ❌ ERROR: NoCopy doesn't have copy ability
}
```

## Global Storage Operations

### The Five Global Storage Functions

```move
// 1. move_to<T> - Store resource at signer's address
public fun initialize(account: &signer) {
    move_to(account, MyResource { value: 0 });
}

// 2. move_from<T> - Remove and return resource
public fun destroy(account: &signer): MyResource {
    move_from<MyResource>(signer::address_of(account))
}

// 3. borrow_global<T> - Immutable borrow
public fun read_value(addr: address): u64 acquires MyResource {
    let resource = borrow_global<MyResource>(addr);
    resource.value
}

// 4. borrow_global_mut<T> - Mutable borrow
public fun update_value(addr: address, new_val: u64) acquires MyResource {
    let resource = borrow_global_mut<MyResource>(addr);
    resource.value = new_val;
}

// 5. exists<T> - Check if resource exists
public fun has_resource(addr: address): bool {
    exists<MyResource>(addr)
}
```

### The `acquires` Annotation

**Critical:** Functions that use `borrow_global` or `borrow_global_mut` must declare `acquires`:

```move
struct Balance has key {
    coins: u64
}

// ✅ Correct
public fun get_balance(addr: address): u64 acquires Balance {
    borrow_global<Balance>(addr).coins
}

// ❌ ERROR: Missing 'acquires Balance'
public fun get_balance_wrong(addr: address): u64 {
    borrow_global<Balance>(addr).coins
}

// Multiple acquires
public fun transfer(from: address, to: address) acquires Balance {
    let from_balance = borrow_global_mut<Balance>(from);
    let to_balance = borrow_global_mut<Balance>(to);
    // ...
}
```

### Resource Existence Patterns

```move
// Pattern 1: Ensure resource exists
public fun ensure_initialized(account: &signer) {
    let addr = signer::address_of(account);
    if (!exists<MyResource>(addr)) {
        move_to(account, MyResource { value: 0 });
    }
}

// Pattern 2: Get or create
public fun get_or_create(account: &signer): &mut MyResource acquires MyResource {
    let addr = signer::address_of(account);
    if (!exists<MyResource>(addr)) {
        move_to(account, MyResource { value: 0 });
    };
    borrow_global_mut<MyResource>(addr)
}

// Pattern 3: Assert exists
public fun must_exist(addr: address) acquires MyResource {
    assert!(exists<MyResource>(addr), ERROR_NOT_INITIALIZED);
    let resource = borrow_global<MyResource>(addr);
    // ...
}
```

## Signer - Authentication Primitive

### What is Signer?

`signer` is Move's authentication primitive - represents authority to act on behalf of an account.

```move
// ✅ Only the signer can authorize operations on their account
public entry fun initialize(account: &signer) {
    // 'account' proves the caller owns this address
    move_to(account, MyResource { value: 0 });
}

// ❌ Can't fake a signer - runtime provides it
public fun fake_signer(addr: address) {
    // No way to create signer from address!
}
```

### Signer Operations

```move
use std::signer;

public fun get_address(account: &signer): address {
    signer::address_of(account)
}

// Common pattern: get address for storage lookup
public fun update_resource(account: &signer, val: u64) acquires MyResource {
    let addr = signer::address_of(account);
    let resource = borrow_global_mut<MyResource>(addr);
    resource.value = val;
}
```

### Access Control with Signer

```move
const ERROR_UNAUTHORIZED: u64 = 1;

public entry fun admin_only(admin: &signer) {
    assert!(signer::address_of(admin) == @admin_address, ERROR_UNAUTHORIZED);
    // Only @admin_address can call this
}

public entry fun owner_only(owner: &signer, resource_addr: address) acquires Owner {
    let owner_addr = signer::address_of(owner);
    let owner_resource = borrow_global<Owner>(resource_addr);
    assert!(owner_resource.owner == owner_addr, ERROR_UNAUTHORIZED);
    // Only the owner can call this
}
```

## Visibility Modifiers

### Function Visibility

```move
module my_module {
    // Private (default) - only callable within module
    fun private_function() { }

    // Public - callable from anywhere, but not as entry point
    public fun public_function() { }

    // Public(friend) - only callable from this module + friend modules
    public(friend) fun friend_function() { }

    // Entry - callable as transaction entry point (public entry)
    public entry fun entry_function(account: &signer) { }

    // Entry (module-local) - entry point but not callable from other modules
    entry fun local_entry(account: &signer) { }
}
```

### Friend Functions

```move
module admin {
    friend user_module;  // Declare friend

    public(friend) fun admin_function() {
        // Only callable from admin module or user_module
    }
}

module user_module {
    use admin::admin_function;

    public fun user_function() {
        admin_function();  // ✅ Allowed (we're a friend)
    }
}

module other_module {
    use admin::admin_function;

    public fun other_function() {
        admin_function();  // ❌ ERROR: Not a friend
    }
}
```

### Entry Functions

Entry functions can be called directly as transaction entry points:

```move
// ✅ Valid entry function signatures
public entry fun simple() { }
public entry fun with_signer(account: &signer) { }
public entry fun with_args(account: &signer, amount: u64, recipient: address) { }

// ❌ Invalid - entry functions can't return values
public entry fun returns_value(): u64 { 0 }

// ❌ Invalid - entry functions can't have reference parameters (except &signer)
public entry fun ref_param(x: &u64) { }
```

## Advanced Features

### Inline Functions

Mark functions for inlining to save gas:

```move
inline fun add(a: u64, b: u64): u64 {
    a + b
}

public fun calculate(): u64 {
    add(5, 10)  // Inlined: becomes 5 + 10 directly
}
```

**When to use `inline`:**
- Small functions called frequently
- Wrappers around simple operations
- Gas-critical paths

### Constant Values

```move
const MAX_SUPPLY: u64 = 1_000_000;
const ERROR_INSUFFICIENT_BALANCE: u64 = 1;
const MODULE_NAME: vector<u8> = b"MyModule";

public fun check_supply(amount: u64) {
    assert!(amount <= MAX_SUPPLY, ERROR_INSUFFICIENT_BALANCE);
}
```

### Module Initialization

```move
fun init_module(deployer: &signer) {
    // Called exactly once when module is published
    move_to(deployer, ModuleConfig {
        admin: signer::address_of(deployer),
        version: 1,
    });
}
```

### Struct Unpacking

```move
struct Point has copy, drop {
    x: u64,
    y: u64,
}

// Unpack all fields
let Point { x, y } = point;

// Unpack some fields, ignore others
let Point { x, y: _ } = point;

// Unpack and rename
let Point { x: x_coord, y: y_coord } = point;
```

### Vector Operations

```move
use std::vector;

let mut v = vector::empty<u64>();
vector::push_back(&mut v, 10);
vector::push_back(&mut v, 20);

let len = vector::length(&v);
let first = vector::borrow(&v, 0);
let mut last = vector::borrow_mut(&mut v, 1);
*last = 30;

let popped = vector::pop_back(&mut v);

vector::append(&mut v, vector[40, 50]);

// Iteration
let i = 0;
while (i < vector::length(&v)) {
    let elem = vector::borrow(&v, i);
    // Use elem
    i = i + 1;
}
```

## Common Patterns

### Pattern 1: Capability Pattern

```move
struct AdminCap has key, store {}

public fun initialize_admin(account: &signer) {
    move_to(account, AdminCap {});
}

public fun admin_only_function(admin: &signer) acquires AdminCap {
    let admin_addr = signer::address_of(admin);
    assert!(exists<AdminCap>(admin_addr), ERROR_NO_ADMIN_CAP);
    // Admin has proven they have AdminCap
}

// Transfer admin capability
public fun transfer_admin(admin: &signer, new_admin: address) acquires AdminCap {
    let cap = move_from<AdminCap>(signer::address_of(admin));
    // In practice, you'd need new_admin's signer
    // This is simplified for demonstration
}
```

### Pattern 2: Witness Pattern

```move
struct MyModule has drop {}  // Witness type

struct Config<phantom T> has key {
    value: u64
}

// Only callable once - witness can only be created in init_module
fun init_module(account: &signer) {
    initialize(account, MyModule {});
}

public fun initialize<T: drop>(account: &signer, _witness: T) {
    move_to(account, Config<T> { value: 0 });
}
```

### Pattern 3: Hot Potato Pattern

```move
// No abilities - can't copy, drop, or store
struct Receipt {
    amount: u64
}

public fun buy(): Receipt {
    Receipt { amount: 100 }
}

public fun redeem(receipt: Receipt) {
    let Receipt { amount } = receipt;  // Must unpack
    // Process redemption
}

// Caller MUST call both buy() and redeem()
// Can't drop Receipt, so must be consumed
```

## Type System Best Practices

### ✅ Do

- **Use abilities explicitly** - Think about copy/drop/store/key
- **Leverage phantom types** - Zero-cost type safety
- **Constrain generics** - Add ability constraints as needed
- **Use references** - Avoid unnecessary copies
- **Check exists before borrow** - Prevent runtime errors
- **Mark admin functions** - Use signer for access control

### ❌ Avoid

- **Over-constraining generics** - Don't require abilities you don't use
- **Ignoring ability requirements** - Compiler errors indicate design issues
- **Returning references to locals** - Lifetime violation
- **Missing acquires** - Always annotate global storage access
- **Copying large structs** - Use references when possible

## Common Errors

### Error: "Field requires ability 'store'"

```move
// ❌ Problem
struct Container has key {
    inner: Inner  // Inner needs 'store'
}

struct Inner {  // Missing 'store'
    value: u64
}

// ✅ Solution
struct Inner has store {
    value: u64
}
```

### Error: "Missing acquires annotation"

```move
// ❌ Problem
public fun get_value(addr: address): u64 {
    borrow_global<Resource>(addr).value
}

// ✅ Solution
public fun get_value(addr: address): u64 acquires Resource {
    borrow_global<Resource>(addr).value
}
```

### Error: "Type parameter T requires constraint"

```move
// ❌ Problem
public fun store<T>(value: T) {
    // Can't do anything with T
}

// ✅ Solution
public fun store<T: store>(value: T) {
    // Now T can be stored
}
```

## Testing Move Code

```move
#[test]
fun test_abilities() {
    let point = Point { x: 10, y: 20 };
    let copy = point;  // ✅ Has copy
    let Point { x, y } = point;  // ✅ Has drop
}

#[test(account = @0x123)]
fun test_signer(account: &signer) {
    let addr = signer::address_of(account);
    assert!(addr == @0x123, 0);
}

#[test]
#[expected_failure(abort_code = ERROR_INVALID)]
fun test_failure() {
    assert!(false, ERROR_INVALID);
}
```

## Response Style

- **Type-first** - Explain type implications before code
- **Ability-aware** - Always discuss ability constraints
- **Safety-focused** - Highlight Move's safety guarantees
- **Pattern-driven** - Show idiomatic Move patterns
- **Error-preventing** - Explain common mistakes upfront

## Follow-up Suggestions

After helping with Move language, suggest:
- Ability design for custom types
- Generic function optimization
- Move Prover specifications
- Gas optimization techniques
- Testing strategies for complex types
- Migration from other smart contract languages
