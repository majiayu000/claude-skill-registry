---
name: aptos-object-model
description: Expert on Aptos Object Model - ObjectCore, Object<T> wrapper, constructor references, ExtendRef/DeleteRef/TransferRef capabilities, object ownership, named vs generated objects, composability, and migration from resource-only patterns. Triggers on keywords object model, objectcore, constructorref, extendref, deleteref, transferref, named object, object ownership, composable object
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

# Aptos Object Model Expert

## Purpose

Provide expert guidance on the Aptos Object Model - a powerful abstraction that enables composable, transferable, and flexible on-chain assets. The Object Model is the foundation for modern Aptos development including Token V2 (Digital Assets), Fungible Assets, and custom composable resources.

## When to Use

Auto-invoke when users mention:
- **Object Model** - objects, ObjectCore, Object<T>, object-based design
- **Object Creation** - ConstructorRef, named objects, object generation
- **Object Capabilities** - ExtendRef, DeleteRef, TransferRef, LinearTransferRef
- **Object Patterns** - composability, nesting, soul-bound, ownership
- **Migration** - moving from resource-only to object-based architecture
- **Standards** - Digital Assets (NFTs), Fungible Assets built on objects

## Core Concepts

### What is the Aptos Object Model?

The Object Model is Aptos's object-oriented programming abstraction that:

1. **Wraps resources** - Any resource can become an "object"
2. **Enables transfer** - Objects can be transferred between accounts
3. **Provides composability** - Objects can own other objects
4. **Manages lifecycle** - Creation, extension, deletion via refs
5. **Separates ownership** - Owner address ≠ object address

### Key Difference from Traditional Resources

```move
// Traditional Resource (can't be transferred directly)
struct MyResource has key {
    value: u64
}
// Lives at account address, can't move to another account

// Object-wrapped Resource (transferable)
struct MyResource has key {
    value: u64
}
// Lives at object address, object itself can transfer between accounts
```

## Object Architecture

### ObjectCore - The Foundation

Every object contains an `ObjectCore` at its address:

```move
struct ObjectCore has key {
    guid_creation_num: u64,      // For generating unique IDs
    owner: address,              // Who owns this object
    allow_ungated_transfer: bool, // Can anyone transfer it?
    transfer_events: EventHandle<TransferEvent>,
}
```

**Key Points:**
- `ObjectCore` is automatically created during object creation
- Object's address ≠ owner's address (objects live at their own address)
- Owner can be an account OR another object (composition!)
- Transfer permissions controlled via `allow_ungated_transfer`

### Object<T> - The Type Wrapper

```move
struct Object<phantom T> has copy, drop, store {
    inner: address  // The object's address
}
```

**Important:**
- `Object<T>` is a **typed reference** to an object
- It's NOT the object itself, just a pointer
- Has `copy + drop + store` (can be copied, stored anywhere)
- Type parameter `T` indicates what resource is at that address
- Phantom type parameter (zero runtime cost)

### Type Hierarchy Example

```move
// An NFT is an Object wrapping a Token resource
Object<Token>

// A Fungible Asset metadata object
Object<Metadata>

// Generic object
Object<ObjectCore>  // Can reference any object
```

## Object Creation

### Method 1: Named Objects (Deterministic Address)

```move
use aptos_framework::object;

public fun create_named_object(creator: &signer) {
    let constructor_ref = object::create_named_object(
        creator,
        b"MY_UNIQUE_SEED"  // Seed for deterministic address
    );

    // Object address is deterministic: hash(creator_address, seed)
    let object_signer = object::generate_signer(&constructor_ref);
    let object_addr = signer::address_of(&object_signer);

    // Move resources to object address
    move_to(&object_signer, MyResource { value: 100 });
}
```

**Named Object Features:**
- Deterministic address: `hash(creator_address, seed)`
- Same creator + seed = same address (idempotent)
- Useful for singletons, registries, well-known objects
- Can't create duplicate with same creator + seed

### Method 2: Generated Objects (Random Address)

```move
public fun create_generated_object(creator: &signer) {
    let constructor_ref = object::create_object(creator);

    // Object address is generated (non-deterministic)
    let object_signer = object::generate_signer(&constructor_ref);

    move_to(&object_signer, MyResource { value: 100 });
}
```

**Generated Object Features:**
- Non-deterministic address (GUID-based)
- Each call creates new unique object
- Useful for collections (NFTs, tokens, etc.)

### Method 3: Object from Account

```move
public entry fun create_object_from_account(caller: &signer) {
    // Convert account into an object
    let constructor_ref = object::create_object_from_account(caller);
    // Now the account itself becomes an object
}
```

### Method 4: Sticky Object (Cannot Delete)

```move
public fun create_sticky_object(creator: &signer) {
    let constructor_ref = object::create_sticky_object(creator);
    // No DeleteRef can be generated - object is permanent
}
```

## Object References and Capabilities

### ConstructorRef - The Master Key

```move
struct ConstructorRef {
    self: address,
    can_delete: bool
}
```

Only available during object creation. Used to generate all other refs:

```move
public fun create_with_refs(creator: &signer) {
    let constructor_ref = object::create_object(creator);

    // Generate various capabilities
    let extend_ref = object::generate_extend_ref(&constructor_ref);
    let transfer_ref = object::generate_transfer_ref(&constructor_ref);
    let delete_ref = object::generate_delete_ref(&constructor_ref);
    let mutator_ref = property_map::generate_mutator_ref(&constructor_ref);

    // Store refs for later use
    let object_signer = object::generate_signer(&constructor_ref);
    move_to(&object_signer, Refs {
        extend_ref,
        transfer_ref,
        delete_ref,
        mutator_ref,
    });
}

struct Refs has key {
    extend_ref: ExtendRef,
    transfer_ref: TransferRef,
    delete_ref: DeleteRef,
    mutator_ref: property_map::MutatorRef,
}
```

### ExtendRef - Access Object After Creation

```move
struct ExtendRef has drop, store {
    self: address
}
```

**Purpose:** Get signer of object in future transactions

```move
public fun modify_object_later(
    object_addr: address
) acquires Refs {
    let refs = borrow_global<Refs>(object_addr);

    // Generate signer from ExtendRef
    let object_signer = object::generate_signer_for_extending(&refs.extend_ref);

    // Now can modify resources at object address
    let resource = borrow_global_mut<MyResource>(object_addr);
    resource.value = resource.value + 10;
}
```

### TransferRef - Control Object Transfers

```move
struct TransferRef has drop, store {
    self: address
}
```

**Purpose:** Enable/disable transfers, force transfers

```move
// Disable ungated transfers (make soul-bound)
public fun make_soul_bound(object_addr: address) acquires Refs {
    let refs = borrow_global<Refs>(object_addr);
    object::disable_ungated_transfer(&refs.transfer_ref);
}

// Re-enable ungated transfers
public fun make_transferable(object_addr: address) acquires Refs {
    let refs = borrow_global<Refs>(object_addr);
    object::enable_ungated_transfer(&refs.transfer_ref);
}

// Force transfer (bypass ownership check)
public fun admin_transfer(
    object_addr: address,
    new_owner: address
) acquires Refs {
    let refs = borrow_global<Refs>(object_addr);
    object::transfer_with_ref(&refs.transfer_ref, new_owner);
}
```

### LinearTransferRef - One-Time Transfer

```move
struct LinearTransferRef {
    self: address,
    owner: address
}
```

**Purpose:** Transfer object exactly once (consumed on use)

```move
public fun create_and_transfer_to(
    creator: &signer,
    recipient: address
) {
    let constructor_ref = object::create_object(creator);

    // Generate linear transfer ref
    let transfer_ref = object::generate_transfer_ref(&constructor_ref);
    let linear_transfer_ref = object::generate_linear_transfer_ref(&transfer_ref);

    // Transfer to recipient (consumes linear_transfer_ref)
    object::transfer_with_ref(linear_transfer_ref, recipient);
}
```

### DeleteRef - Destroy Objects

```move
struct DeleteRef has drop, store {
    self: address
}
```

**Purpose:** Delete object and all resources at its address

```move
public fun delete_object(object_addr: address) acquires Refs, MyResource {
    // Remove all resources first
    let MyResource { value: _ } = move_from<MyResource>(object_addr);
    let Refs { delete_ref, extend_ref, transfer_ref, mutator_ref } =
        move_from<Refs>(object_addr);

    // Delete the object
    object::delete(delete_ref);
}
```

## Object Ownership and Transfer

### Reading Object Information

```move
use aptos_framework::object;

public fun get_object_info<T: key>(obj: Object<T>): (address, address, bool) {
    let object_addr = object::object_address(&obj);
    let owner_addr = object::owner(obj);
    let is_owner_account = object::is_owner(obj, owner_addr);

    (object_addr, owner_addr, is_owner_account)
}

// Check if object exists
public fun object_exists<T: key>(addr: address): bool {
    object::object_exists<T>(addr)
}
```

### User-Initiated Transfer

```move
use aptos_framework::object;

public entry fun transfer_object<T: key>(
    owner: &signer,
    object: Object<T>,
    new_owner: address
) {
    // Only works if ungated transfer is enabled
    object::transfer(owner, object, new_owner);
}
```

### Checking Transfer Permissions

```move
public fun check_transferable<T: key>(obj: Object<T>): bool {
    object::ungated_transfer_allowed(obj)
}
```

## Object Composition (Nesting)

### Child Object Pattern

```move
public fun create_parent_and_child(creator: &signer) {
    // Create parent object
    let parent_ref = object::create_named_object(creator, b"PARENT");
    let parent_signer = object::generate_signer(&parent_ref);
    let parent_addr = signer::address_of(&parent_signer);

    // Create child object OWNED BY parent
    let child_ref = object::create_object_from_object(&parent_signer);
    let child_signer = object::generate_signer(&child_ref);
    let child_addr = signer::address_of(&child_signer);

    // Transfer child to parent
    let transfer_ref = object::generate_transfer_ref(&child_ref);
    let linear_transfer_ref = object::generate_linear_transfer_ref(&transfer_ref);
    object::transfer_with_ref(linear_transfer_ref, parent_addr);

    // Now: parent owns child, creator owns parent
}
```

### Querying Nested Ownership

```move
public fun get_root_owner<T: key>(obj: Object<T>): address {
    let mut current_addr = object::object_address(&obj);

    loop {
        if (!object::is_object(current_addr)) {
            // Reached an account (not an object) - this is root owner
            return current_addr;
        };

        let owner = object::owner(object::address_to_object<ObjectCore>(current_addr));
        if (owner == current_addr) {
            return current_addr; // Self-owned
        };
        current_addr = owner;
    }
}
```

## Common Patterns

### Pattern 1: Registry / Singleton

```move
public fun get_or_create_registry(creator: &signer): address {
    let seed = b"MY_REGISTRY";
    let creator_addr = signer::address_of(creator);
    let object_addr = object::create_object_address(&creator_addr, seed);

    if (!object::object_exists<Registry>(object_addr)) {
        let constructor_ref = object::create_named_object(creator, seed);
        let object_signer = object::generate_signer(&constructor_ref);

        move_to(&object_signer, Registry {
            items: simple_map::create()
        });
    };

    object_addr
}
```

### Pattern 2: NFT with Composable Items

```move
struct NFT has key {
    name: String,
    uri: String,
}

struct EquippedItem has key {
    item_object: Object<Item>,
}

struct Item has key {
    name: String,
    power: u64,
}

public fun equip_item_to_nft(
    nft_obj: Object<NFT>,
    item_obj: Object<Item>
) acquires Refs {
    let nft_addr = object::object_address(&nft_obj);

    // Get ExtendRef to modify NFT
    let refs = borrow_global<Refs>(nft_addr);
    let nft_signer = object::generate_signer_for_extending(&refs.extend_ref);

    // Store item reference in NFT
    if (!exists<EquippedItem>(nft_addr)) {
        move_to(&nft_signer, EquippedItem { item_object: item_obj });
    };

    // Transfer item ownership to NFT object
    let item_addr = object::object_address(&item_obj);
    let item_refs = borrow_global<Refs>(item_addr);
    object::transfer_with_ref(&item_refs.transfer_ref, nft_addr);
}
```

### Pattern 3: Soul-Bound Token (SBT)

```move
public fun create_soul_bound_token(
    creator: &signer,
    recipient: address,
    name: String
) {
    let constructor_ref = token::create_named_token(
        creator,
        string::utf8(b"Soul Bound Collection"),
        string::utf8(b"Description"),
        name,
        option::none(),
        string::utf8(b"https://uri.com"),
    );

    // Disable transfers (soul-bound)
    let transfer_ref = object::generate_transfer_ref(&constructor_ref);
    object::disable_ungated_transfer(&transfer_ref);

    // Transfer to recipient (one-time transfer during creation)
    let linear_transfer_ref = object::generate_linear_transfer_ref(&transfer_ref);
    object::transfer_with_ref(linear_transfer_ref, recipient);

    // Don't store transfer_ref - now permanently non-transferable
}
```

### Pattern 4: Upgradeable Module Data

```move
struct ModuleData has key {
    version: u64,
    config: Config,
}

struct DataRefs has key {
    extend_ref: ExtendRef,
}

public fun initialize_module_data(admin: &signer) {
    let constructor_ref = object::create_named_object(admin, b"MODULE_DATA");
    let object_signer = object::generate_signer(&constructor_ref);

    move_to(&object_signer, ModuleData {
        version: 1,
        config: create_config(),
    });

    let extend_ref = object::generate_extend_ref(&constructor_ref);
    move_to(&object_signer, DataRefs { extend_ref });
}

public fun upgrade_module_data(new_config: Config) acquires DataRefs, ModuleData {
    let data_addr = object::create_object_address(&@my_module, b"MODULE_DATA");
    let refs = borrow_global<DataRefs>(data_addr);

    let object_signer = object::generate_signer_for_extending(&refs.extend_ref);
    let data = borrow_global_mut<ModuleData>(data_addr);

    data.version = data.version + 1;
    data.config = new_config;
}
```

## Migration from Resource-Only to Object Model

### Before (Resource-Only)

```move
struct OldNFT has key {
    name: String,
    uri: String,
}

// Can't transfer between accounts
// Lives at owner's address
// No composition
```

### After (Object Model)

```move
struct NewNFT has key {
    name: String,
    uri: String,
}

public fun create_nft(creator: &signer, recipient: address) {
    let constructor_ref = object::create_object(creator);
    let object_signer = object::generate_signer(&constructor_ref);

    move_to(&object_signer, NewNFT {
        name: string::utf8(b"My NFT"),
        uri: string::utf8(b"https://..."),
    });

    // Transfer to recipient
    let transfer_ref = object::generate_transfer_ref(&constructor_ref);
    let linear_ref = object::generate_linear_transfer_ref(&transfer_ref);
    object::transfer_with_ref(linear_ref, recipient);
}

// ✅ Can transfer
// ✅ Lives at own address
// ✅ Composable
```

## TypeScript SDK Integration

### Creating Objects

```typescript
import { Aptos, AptosConfig, Network } from "@aptos-labs/ts-sdk";

const aptos = new Aptos(new AptosConfig({ network: Network.TESTNET }));

// Call object creation function
const txn = await aptos.transaction.build.simple({
  sender: account.accountAddress,
  data: {
    function: "0x123::my_module::create_named_object",
    functionArguments: [],
  },
});

const response = await aptos.signAndSubmitTransaction({
  signer: account,
  transaction: txn,
});
```

### Querying Objects

```typescript
// Get object data
const objectData = await aptos.getAccountResource({
  accountAddress: "0xobject_address",
  resourceType: "0x1::object::ObjectCore"
});

console.log("Owner:", objectData.owner);
console.log("Transferable:", objectData.allow_ungated_transfer);

// Get custom resource at object address
const nftData = await aptos.getAccountResource({
  accountAddress: "0xobject_address",
  resourceType: "0x123::my_module::NFT"
});
```

### Transferring Objects

```typescript
const txn = await aptos.transaction.build.simple({
  sender: owner.accountAddress,
  data: {
    function: "0x1::object::transfer",
    typeArguments: ["0x123::my_module::NFT"],
    functionArguments: [
      objectAddress,
      recipientAddress,
    ],
  },
});
```

## Best Practices

### ✅ Do

- **Store refs at object address** - Keep ExtendRef, DeleteRef, etc. as resources at the object's own address
- **Use named objects for singletons** - Registries, module configs, well-known objects
- **Use generated objects for collections** - NFTs, tokens, user-specific objects
- **Disable ungated transfer for SBTs** - Use soul-bound pattern for credentials
- **Document object relationships** - Make ownership hierarchy clear
- **Clean up on deletion** - Remove all resources before calling object::delete()

### ❌ Avoid

- **Don't lose ConstructorRef** - Generate all needed refs during creation
- **Don't store refs elsewhere** - Store at object address, not creator address
- **Don't forget to transfer initial ownership** - Objects start owned by creator
- **Don't mix object and non-object patterns** - Pick one architecture
- **Don't delete without cleanup** - Remove resources first

## Common Errors and Solutions

### Error: "Object does not exist"

```move
// Problem: Object wasn't created or wrong address
let obj = object::address_to_object<T>(wrong_address);

// Solution: Verify object exists first
assert!(object::object_exists<T>(address), ERROR_OBJECT_NOT_FOUND);
let obj = object::address_to_object<T>(address);
```

### Error: "Ungated transfer not allowed"

```move
// Problem: Trying to transfer soul-bound object
object::transfer(owner, obj, recipient); // FAILS

// Solution: Use TransferRef for forced transfer
let refs = borrow_global<Refs>(object_addr);
object::transfer_with_ref(&refs.transfer_ref, recipient);
```

### Error: "Object already exists"

```move
// Problem: Creating named object with duplicate seed
let constructor_ref = object::create_named_object(creator, b"SEED");

// Solution: Check existence first or use different seed
let addr = object::create_object_address(&creator_addr, b"SEED");
if (!object::object_exists<ObjectCore>(addr)) {
    let constructor_ref = object::create_named_object(creator, b"SEED");
    // ...
}
```

## Security Considerations

### Access Control

```move
// Verify ownership before operations
public fun modify_only_by_owner(
    owner: &signer,
    obj: Object<MyResource>
) {
    assert!(
        object::is_owner(obj, signer::address_of(owner)),
        ERROR_NOT_OWNER
    );

    // Safe to modify
}
```

### Capability Protection

```move
// Store refs at object address (not accessible from outside)
struct Refs has key {
    extend_ref: ExtendRef,
    transfer_ref: TransferRef,
    delete_ref: DeleteRef,
}

// ✅ Good: Stored at object address
move_to(&object_signer, Refs { /* ... */ });

// ❌ Bad: Stored at creator address (could be accessed elsewhere)
// move_to(creator, Refs { /* ... */ });
```

## Documentation References

Reference official Aptos docs:
- aptos.dev/guides/objects
- aptos.dev/standards/digital-asset
- aptos.dev/standards/fungible-asset
- Aptos Framework source: 0x1::object

## Response Style

- **Concept-first** - Explain object model concepts before code
- **Pattern-driven** - Show common patterns and use cases
- **Comparison** - Compare to resource-only approach when helpful
- **Visual** - Use diagrams/structure to show object relationships
- **Security-aware** - Highlight ownership and access control

## Follow-up Suggestions

After helping with objects, suggest:
- Object composition strategies
- Ref management patterns
- Migration path from resources
- Gas optimization for object operations
- Testing object-based contracts
- Integration with Token/FA standards
