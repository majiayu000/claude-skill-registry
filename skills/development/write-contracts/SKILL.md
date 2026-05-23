---
name: write-contracts
description:
  "Generates secure Aptos Move V2 smart contracts with Object model, Digital Asset integration, security patterns, and
  storage type guidance. Includes comprehensive storage decision framework for optimal data structure selection.
  Triggers on: 'write contract', 'create NFT collection', 'build marketplace', 'implement minting', 'generate Move
  module', 'create token contract', 'build DAO', 'implement staking'. Ask storage questions when: 'store', 'track',
  'registry', 'mapping', 'list', 'collection'."
license: MIT
metadata:
  author: aptos-labs
  version: "1.0"
  category: move
  tags: ["smart-contracts", "move", "nft", "defi", "objects"]
  priority: critical
---

# Write Contracts Skill

## Core Rules

### Digital Assets (NFTs) ⭐ CRITICAL

1. **ALWAYS use Digital Asset (DA) standard** for ALL NFT-related contracts (collections, marketplaces, minting)
2. **ALWAYS import** `aptos_token_objects::collection` and `aptos_token_objects::token` modules
3. **ALWAYS use** `Object<AptosToken>` for NFT references (NOT generic `Object<T>`)
4. **NEVER use legacy TokenV1** standard or `aptos_token::token` module (deprecated)
5. See `../../../patterns/move/DIGITAL_ASSETS.md` for complete NFT patterns

### Object Model

6. **ALWAYS use** `Object<T>` for all object references (NEVER raw addresses)
7. **Generate all refs** (TransferRef, DeleteRef) in constructor before ConstructorRef destroyed
8. **Return** `Object<T>` from constructors (NEVER return ConstructorRef)
9. **Verify ownership** with `object::owner(obj) == signer::address_of(user)`
10. **Use** `object::generate_signer(&constructor_ref)` for object signers
11. **Use named objects** for singletons: `object::create_named_object(creator, seed)`

### Security

12. **ALWAYS verify signer authority** in entry functions:
    `assert!(signer::address_of(user) == expected, E_UNAUTHORIZED)`
13. **ALWAYS validate inputs**: non-zero amounts, address validation, string length checks
14. **NEVER expose** `&mut` references in public functions
15. **NEVER skip** signer verification in entry functions

### Modern Syntax

16. **Use inline functions** and lambdas for iteration
17. **Use receiver-style** method calls: `obj.is_owner(user)` (define first param as `self`)
18. **Use vector indexing**: `vector[index]` instead of `vector::borrow()`
19. **Use direct named addresses**: `@marketplace_addr` (NOT helper functions)

### Required Patterns

20. **Use init_module** for contract initialization on deployment
21. **Emit events** for ALL significant activities (create, transfer, update, delete)
22. **Define clear error constants** with descriptive names (E_NOT_OWNER, E_INSUFFICIENT_BALANCE)

### Testability

23. **Add accessor functions** for struct fields - tests in separate modules cannot access struct fields directly
24. **Use `#[view]` annotation** for read-only accessor functions
25. **Return tuples** from accessors for multi-field access: `(seller, price, timestamp)`
26. **Place `#[view]` BEFORE doc comments** - `/// comment` before `#[view]` causes compiler warnings. Write `#[view]`
    first, then `///`

## Quick Workflow

1. **Create module structure** → Define structs, events, constants, init_module
2. **Implement object creation** → Use proper constructor pattern with all refs generated upfront
3. **Add access control** → Verify ownership and validate all inputs
4. **Security check** → Use `security-audit` skill before deployment

## Key Example: Object Creation Pattern

```move
struct MyObject has key {
    name: String,
    transfer_ref: object::TransferRef,
    delete_ref: object::DeleteRef,
}

// Error constants
const E_NOT_OWNER: u64 = 1;
const E_EMPTY_STRING: u64 = 2;
const E_NAME_TOO_LONG: u64 = 3;

// Configuration constants
const MAX_NAME_LENGTH: u64 = 100;

/// Create object with proper pattern
public fun create_my_object(creator: &signer, name: String): Object<MyObject> {
    // 1. Create object
    let constructor_ref = object::create_object(signer::address_of(creator));

    // 2. Generate ALL refs you'll need BEFORE constructor_ref is destroyed
    let transfer_ref = object::generate_transfer_ref(&constructor_ref);
    let delete_ref = object::generate_delete_ref(&constructor_ref);

    // 3. Get object signer
    let object_signer = object::generate_signer(&constructor_ref);

    // 4. Store data in object
    move_to(&object_signer, MyObject {
        name,
        transfer_ref,
        delete_ref,
    });

    // 5. Return typed object reference (ConstructorRef automatically destroyed)
    object::object_from_constructor_ref<MyObject>(&constructor_ref)
}

/// Update with ownership verification
public entry fun update_object(
    owner: &signer,
    obj: Object<MyObject>,
    new_name: String
) acquires MyObject {
    // ✅ ALWAYS: Verify ownership
    assert!(object::owner(obj) == signer::address_of(owner), E_NOT_OWNER);

    // ✅ ALWAYS: Validate inputs
    assert!(string::length(&new_name) > 0, E_EMPTY_STRING);
    assert!(string::length(&new_name) <= MAX_NAME_LENGTH, E_NAME_TOO_LONG);

    // Safe to proceed
    let obj_data = borrow_global_mut<MyObject>(object::object_address(&obj));
    obj_data.name = new_name;
}
```

## Key Example: Accessor Functions for Testing

```move
struct ListingInfo has store, drop, copy {
    seller: address,
    price: u64,
    listed_at: u64,
}

/// Accessor function - tests cannot access struct fields directly
/// Use tuple returns for multiple fields
#[view]
public fun get_listing_details(nft_addr: address): (address, u64, u64) acquires Listings {
    let listings = borrow_global<Listings>(get_marketplace_address());
    assert!(table::contains(&listings.items, nft_addr), E_NOT_LISTED);
    let listing = table::borrow(&listings.items, nft_addr);
    (listing.seller, listing.price, listing.listed_at)
}

/// Single-field accessor when only one value needed
#[view]
public fun get_staked_amount(user_addr: address): u64 acquires Stakes {
    let stakes = borrow_global<Stakes>(get_vault_address());
    if (table_with_length::contains(&stakes.items, user_addr)) {
        table_with_length::borrow(&stakes.items, user_addr).amount
    } else {
        0
    }
}
```

## Module Structure Template

```move
module my_addr::my_module {
    // ============ Imports ============
    use std::signer;
    use std::string::String;
    use aptos_framework::object::{Self, Object};
    use aptos_framework::event;

    // ============ Events ============
    #[event]
    struct ItemCreated has drop, store {
        item: address,
        creator: address,
    }

    // ============ Structs ============
    // Define your data structures

    // ============ Constants ============
    const E_NOT_OWNER: u64 = 1;
    const E_UNAUTHORIZED: u64 = 2;

    // ============ Init Module ============
    fun init_module(deployer: &signer) {
        // Initialize global state, registries, etc.
    }

    // ============ Public Entry Functions ============
    // User-facing functions

    // ============ Public Functions ============
    // Composable functions

    // ============ Private Functions ============
    // Internal helpers
}
```

## Storage Type Selection

⚠️ **When user mentions storage** ("store", "track", "registry", "mapping", "list", "collection"):

### 1. Ask 2-3 Questions (see `references/storage-decision-tree.md`)

- **Access pattern?** (sequential vs key-value vs both)
- **Expected size?** (small vs large vs unknown)
- **Need `.length()`?** (conditional)

### 2. Recommend from Patterns (`references/storage-patterns.md`)

| Pattern          | Recommended Storage                  |
| ---------------- | ------------------------------------ |
| User registry    | `Table<address, UserInfo>`           |
| Staking records  | `Table<address, StakeInfo>`          |
| Leaderboard      | `BigOrderedMap<u64, address>`        |
| Transaction log  | `SmartVector<TxRecord>` or `Vector`  |
| Whitelist (<100) | `Vector<address>`                    |
| Voting records   | `TableWithLength<address, bool>`     |
| Config (<50)     | `OrderedMap<String, Value>`          |
| DAO proposals    | `BigOrderedMap<u64, Proposal>`       |
| Asset collection | `Vector<Object<T>>` or `SmartVector` |

### 3. Include Brief Gas Context

**Example recommendations:**

- "For staking, I recommend `Table<address, StakeInfo>` because you'll have unbounded users with concurrent operations
  (separate slots enable parallel access)"
- "For leaderboard, I recommend `BigOrderedMap<u64, address>` because you need sorted iteration (O(log n), use
  `allocate_spare_slots` for production)"

### Storage Types Available

- **Vector** - Small sequential (<100 items)
- **SmartVector** - Large sequential (100+ items)
- **Table** - Unordered key-value lookups
- **TableWithLength** - Table with count tracking
- **OrderedMap** - Small sorted maps (<100 items)
- **BigOrderedMap** - Large sorted maps (100+ items)

⚠️ **NEVER use SmartTable** (deprecated, use BigOrderedMap)

**Details:** See `references/` for decision tree, type comparisons, and gas optimization.

## Anti-patterns

1. ❌ **Never use legacy TokenV1** standard or import `aptos_token::token`
2. ❌ **Never use resource accounts** (use named objects instead)
3. ❌ **Never return ConstructorRef** from public functions
4. ❌ **Never skip signer verification** in entry functions
5. ❌ **Never skip input validation** (amounts, addresses, strings)
6. ❌ **Never deploy without 100% test coverage**
7. ❌ **Never create helper functions** that just return named addresses
8. ❌ **Never skip event emission** for significant activities
9. ❌ **Never use old syntax** when V2 syntax is available
10. ❌ **Never skip init_module** for contracts that need initialization
11. ❌ **Never hardcode real private keys** or secrets in code — use `@my_addr` named addresses and `"0x..."`
    placeholders
12. ❌ **Never read `.env` or `~/.aptos/config.yaml`** — these contain private keys

## Edge Cases to Handle

| Scenario            | Check                                                   | Error Code         |
| ------------------- | ------------------------------------------------------- | ------------------ |
| Zero amounts        | `assert!(amount > 0, E_ZERO_AMOUNT)`                    | E_ZERO_AMOUNT      |
| Excessive amounts   | `assert!(amount <= MAX, E_AMOUNT_TOO_HIGH)`             | E_AMOUNT_TOO_HIGH  |
| Empty vectors       | `assert!(vector::length(&v) > 0, E_EMPTY_VECTOR)`       | E_EMPTY_VECTOR     |
| Empty strings       | `assert!(string::length(&s) > 0, E_EMPTY_STRING)`       | E_EMPTY_STRING     |
| Strings too long    | `assert!(string::length(&s) <= MAX, E_STRING_TOO_LONG)` | E_STRING_TOO_LONG  |
| Zero address        | `assert!(addr != @0x0, E_ZERO_ADDRESS)`                 | E_ZERO_ADDRESS     |
| Overflow            | `assert!(a <= MAX_U64 - b, E_OVERFLOW)`                 | E_OVERFLOW         |
| Underflow           | `assert!(a >= b, E_UNDERFLOW)`                          | E_UNDERFLOW        |
| Division by zero    | `assert!(divisor > 0, E_DIVISION_BY_ZERO)`              | E_DIVISION_BY_ZERO |
| Unauthorized access | `assert!(signer == expected, E_UNAUTHORIZED)`           | E_UNAUTHORIZED     |
| Not object owner    | `assert!(object::owner(obj) == user, E_NOT_OWNER)`      | E_NOT_OWNER        |

## References

**Detailed Patterns (references/ folder):**

- `references/storage-decision-tree.md` - ⭐ Storage type selection framework (ask when storage mentioned)
- `references/storage-patterns.md` - ⭐ Use-case patterns and smart defaults
- `references/storage-types.md` - Detailed comparison of all 6 storage types
- `references/storage-gas-optimization.md` - Gas optimization strategies for storage
- `references/object-patterns.md` - Named objects, collections, nested objects
- `references/access-control.md` - RBAC and permission systems
- `references/safe-arithmetic.md` - Overflow/underflow prevention
- `references/initialization.md` - init_module patterns and registry creation
- `references/events.md` - Event emission patterns
- `references/v2-syntax.md` - Modern Move V2 features (method calls, indexing, lambdas)
- `references/complete-example.md` - Full annotated NFT collection contract

**Pattern Documentation (patterns/ folder):**

- `../../../patterns/move/DIGITAL_ASSETS.md` - Digital Asset (NFT) standard - CRITICAL for NFTs
- `../../../patterns/move/OBJECTS.md` - Comprehensive object model guide
- `../../../patterns/move/SECURITY.md` - Security checklist and patterns
- `../../../patterns/move/MOVE_V2_SYNTAX.md` - Modern syntax examples

**Official Documentation:**

- Digital Asset Standard: https://aptos.dev/build/smart-contracts/digital-asset
- Object Model: https://aptos.dev/build/smart-contracts/object
- Security Guidelines: https://aptos.dev/build/smart-contracts/move-security-guidelines

**Related Skills:**

- `search-aptos-examples` - Find similar examples in aptos-core (optional)
- `generate-tests` - Write tests for contracts (use AFTER writing contracts)
- `security-audit` - Audit contracts before deployment
