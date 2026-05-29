---
name: aptos-token-standards
description: Expert on Aptos token standards including fungible tokens (Coin, Fungible Asset), non-fungible tokens (Digital Asset standard, Token V1/V2), collections, metadata, minting, burning, and transfer patterns. Triggers on keywords token, nft, fungible asset, coin, digital asset, collection, mint, burn, metadata, royalty
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

# Aptos Token Standards Expert

## Purpose

Provide expert guidance on Aptos token standards, including fungible tokens (Coin and Fungible Asset frameworks), non-fungible tokens (Digital Asset standard, Token V1/V2), collections, metadata management, minting, burning, and transfer patterns.

## When to Use

Auto-invoke when users mention:
- **Fungible Tokens** - coin, fungible asset, FA, token standard, currency
- **NFTs** - non-fungible token, digital asset, collection, NFT standard
- **Operations** - mint, burn, transfer, freeze, metadata
- **Standards** - Token V1, Token V2, Digital Asset, Coin framework
- **Collections** - collection creation, NFT collections, series
- **Metadata** - token URI, properties, attributes, royalties

## Token Framework Overview

### Aptos Token Frameworks

```
1. Coin Framework (0x1::coin)
   - Original fungible token standard
   - Simple, battle-tested
   - Used for APT and most tokens
   - Limited customization

2. Fungible Asset Framework (0x1::fungible_asset)
   - New fungible token standard
   - More flexible than Coin
   - Object-based architecture
   - Advanced features (pause, freeze, etc.)

3. Token V1 (0x3::token)
   - Original NFT standard (deprecated)
   - Simple but limited
   - Being phased out

4. Token V2 / Digital Asset (0x4::aptos_token, 0x4::token)
   - Current NFT standard
   - Object-based
   - Flexible, composable
   - Recommended for new projects
```

## Process

When a user asks about tokens:

### 1. Identify Token Type

```
Fungible or Non-Fungible?
- Fungible: Use Coin or Fungible Asset
- Non-fungible: Use Digital Asset (Token V2)

Which standard to use?
- New projects: Fungible Asset / Digital Asset
- Existing integrations: Coin / Token V1 (if needed)
- Advanced features: Fungible Asset / Digital Asset
```

### 2. Determine Use Case

```
Common scenarios:
- Creating a new coin/token
- Minting NFTs in a collection
- Managing token metadata
- Implementing transfers/burns
- Setting up royalties
- Creating token utilities (staking, etc.)
- Multi-token management
```

### 3. Provide Implementation Guidance

Structure your response:
- **Standard choice** - which framework to use and why
- **Code example** - complete working implementation
- **Key concepts** - important patterns and structures
- **Best practices** - security and design recommendations
- **Common pitfalls** - what to avoid
- **References** - link to relevant docs

## Fungible Tokens: Coin Framework

### Creating a Coin

```move
module my_addr::my_coin {
    use std::string;
    use aptos_framework::coin;

    struct MyCoin {}

    fun init_module(sender: &signer) {
        let (burn_cap, freeze_cap, mint_cap) = coin::initialize<MyCoin>(
            sender,
            string::utf8(b"My Coin"),
            string::utf8(b"MYC"),
            8, // decimals
            true, // monitor_supply
        );

        // Store capabilities
        move_to(sender, Capabilities {
            burn_cap,
            freeze_cap,
            mint_cap,
        });
    }

    struct Capabilities has key {
        burn_cap: coin::BurnCapability<MyCoin>,
        freeze_cap: coin::FreezeCapability<MyCoin>,
        mint_cap: coin::MintCapability<MyCoin>,
    }
}
```

### Minting Coins

```move
public entry fun mint(
    admin: &signer,
    recipient: address,
    amount: u64
) acquires Capabilities {
    let caps = borrow_global<Capabilities>(@my_addr);
    let coins = coin::mint(amount, &caps.mint_cap);
    coin::deposit(recipient, coins);
}
```

### Burning Coins

```move
public entry fun burn(
    account: &signer,
    amount: u64
) acquires Capabilities {
    let caps = borrow_global<Capabilities>(@my_addr);
    let coins = coin::withdraw<MyCoin>(account, amount);
    coin::burn(coins, &caps.burn_cap);
}
```

### Coin Operations

```move
// Transfer coins
public entry fun transfer(
    from: &signer,
    to: address,
    amount: u64
) {
    coin::transfer<MyCoin>(from, to, amount);
}

// Get balance
public fun balance(account: address): u64 {
    coin::balance<MyCoin>(account)
}

// Register to receive coins
public entry fun register(account: &signer) {
    coin::register<MyCoin>(account);
}
```

## Fungible Tokens: Fungible Asset Framework

### Creating a Fungible Asset

```move
module my_addr::my_fa {
    use aptos_framework::fungible_asset::{Self, MintRef, BurnRef, TransferRef};
    use aptos_framework::object::{Self, Object};
    use aptos_framework::primary_fungible_store;
    use std::string;
    use std::option;

    struct MyFA {}

    struct Refs has key {
        mint_ref: MintRef,
        burn_ref: BurnRef,
        transfer_ref: TransferRef,
    }

    fun init_module(admin: &signer) {
        let constructor_ref = &object::create_named_object(admin, b"MY_FA");

        primary_fungible_store::create_primary_store_enabled_fungible_asset(
            constructor_ref,
            option::none(), // max_supply
            string::utf8(b"My Fungible Asset"),
            string::utf8(b"MFA"),
            8, // decimals
            string::utf8(b"https://myfa.com/icon.png"),
            string::utf8(b"https://myfa.com"),
        );

        let mint_ref = fungible_asset::generate_mint_ref(constructor_ref);
        let burn_ref = fungible_asset::generate_burn_ref(constructor_ref);
        let transfer_ref = fungible_asset::generate_transfer_ref(constructor_ref);

        move_to(admin, Refs { mint_ref, burn_ref, transfer_ref });
    }
}
```

### Fungible Asset Operations

```move
public entry fun mint(
    admin: &signer,
    recipient: address,
    amount: u64
) acquires Refs {
    let refs = borrow_global<Refs>(@my_addr);
    let fa = fungible_asset::mint(&refs.mint_ref, amount);
    primary_fungible_store::deposit(recipient, fa);
}

public entry fun burn(
    admin: &signer,
    holder: address,
    amount: u64
) acquires Refs {
    let refs = borrow_global<Refs>(@my_addr);
    let fa = primary_fungible_store::withdraw(holder, amount);
    fungible_asset::burn(&refs.burn_ref, fa);
}

// Freeze/unfreeze account
public entry fun freeze_account(
    admin: &signer,
    account: address
) acquires Refs {
    let refs = borrow_global<Refs>(@my_addr);
    fungible_asset::set_frozen_flag(&refs.transfer_ref, account, true);
}
```

## Non-Fungible Tokens: Digital Asset (Token V2)

### Creating a Collection

```move
module my_addr::my_nft {
    use aptos_token_objects::collection;
    use std::string::{Self, String};
    use std::option;

    public entry fun create_collection(creator: &signer) {
        let description = string::utf8(b"My NFT Collection");
        let name = string::utf8(b"My NFTs");
        let uri = string::utf8(b"https://mynft.com/collection");

        collection::create_unlimited_collection(
            creator,
            description,
            name,
            option::none(), // royalty
            uri,
        );
    }

    // Or with fixed supply
    public entry fun create_fixed_collection(
        creator: &signer,
        max_supply: u64
    ) {
        collection::create_fixed_collection(
            creator,
            string::utf8(b"Description"),
            max_supply,
            string::utf8(b"Collection Name"),
            option::none(),
            string::utf8(b"https://uri.com"),
        );
    }
}
```

### Minting NFTs

```move
use aptos_token_objects::token;

public entry fun mint_nft(
    creator: &signer,
    collection_name: String,
    description: String,
    name: String,
    uri: String,
) {
    token::create_named_token(
        creator,
        collection_name,
        description,
        name,
        option::none(), // royalty
        uri,
    );
}

// Mint to specific recipient
public entry fun mint_to(
    creator: &signer,
    recipient: address,
    collection_name: String,
    token_name: String,
) {
    let constructor_ref = token::create_named_token(
        creator,
        collection_name,
        string::utf8(b"Description"),
        token_name,
        option::none(),
        string::utf8(b"https://uri.com"),
    );

    // Transfer to recipient
    let transfer_ref = object::generate_transfer_ref(&constructor_ref);
    let linear_transfer_ref = object::generate_linear_transfer_ref(&transfer_ref);
    object::transfer_with_ref(linear_transfer_ref, recipient);
}
```

### NFT with Properties (Metadata)

```move
use aptos_token_objects::property_map;

public entry fun mint_with_properties(
    creator: &signer,
    collection: String,
    name: String,
) {
    let constructor_ref = token::create_named_token(
        creator,
        collection,
        string::utf8(b"Description"),
        name,
        option::none(),
        string::utf8(b"https://uri.com"),
    );

    // Add properties
    let property_mutator_ref = property_map::generate_mutator_ref(&constructor_ref);

    property_map::add_typed(
        &property_mutator_ref,
        string::utf8(b"strength"),
        100u64
    );

    property_map::add_typed(
        &property_mutator_ref,
        string::utf8(b"rarity"),
        string::utf8(b"legendary")
    );

    // Store mutator ref if properties need to change later
    // move_to(creator, PropertyMutatorRef { property_mutator_ref });
}
```

### Reading NFT Properties

```move
public fun get_nft_property(
    token_address: address,
    property_name: String
): u64 {
    let property_map = property_map::borrow(token_address);
    property_map::read_u64(property_map, &property_name)
}
```

### NFT Transfers

```move
use aptos_framework::object;

// Standard transfer (if transferable)
public entry fun transfer_nft(
    owner: &signer,
    token_address: address,
    recipient: address
) {
    object::transfer(owner, object::address_to_object<token::Token>(token_address), recipient);
}

// For soul-bound tokens (non-transferable)
public entry fun make_soul_bound(creator: &signer, constructor_ref: &ConstructorRef) {
    let transfer_ref = object::generate_transfer_ref(constructor_ref);
    object::disable_ungated_transfer(&transfer_ref);
    // Don't store transfer_ref - token becomes non-transferable
}
```

### Burning NFTs

```move
public entry fun burn_nft(
    owner: &signer,
    token_address: address
) {
    let token_object = object::address_to_object<token::Token>(token_address);
    token::burn(owner, token_object);
}
```

## Royalties

### Setting Royalties on Collection

```move
use aptos_token_objects::royalty;

public entry fun create_collection_with_royalty(
    creator: &signer,
    royalty_numerator: u64,
    royalty_denominator: u64,
    payee_address: address
) {
    let royalty = royalty::create(
        royalty_numerator,
        royalty_denominator,
        payee_address
    );

    collection::create_unlimited_collection(
        creator,
        string::utf8(b"Description"),
        string::utf8(b"Name"),
        option::some(royalty), // 👈 royalty here
        string::utf8(b"https://uri.com"),
    );
}
```

### Reading Royalty Info

```move
public fun get_royalty_info(collection_addr: address): (u64, u64, address) {
    let collection_obj = object::address_to_object<collection::Collection>(collection_addr);
    let royalty = royalty::get(collection_obj);

    (
        royalty::numerator(&royalty),
        royalty::denominator(&royalty),
        royalty::payee_address(&royalty)
    )
}
```

## Advanced Patterns

### Conditional Minting (Allowlist)

```move
struct Allowlist has key {
    addresses: vector<address>
}

public entry fun mint_if_allowed(
    minter: &signer,
    collection: String,
    name: String
) acquires Allowlist {
    let allowlist = borrow_global<Allowlist>(@my_addr);
    let minter_addr = signer::address_of(minter);

    assert!(
        vector::contains(&allowlist.addresses, &minter_addr),
        ERROR_NOT_ALLOWED
    );

    token::create_named_token(/* ... */);
}
```

### Evolving NFTs (Mutable Properties)

```move
struct EvolutionRefs has key {
    mutator_refs: SimpleMap<address, PropertyMutatorRef>
}

public entry fun evolve_nft(
    token_addr: address,
    new_level: u64
) acquires EvolutionRefs {
    let refs = borrow_global<EvolutionRefs>(@my_addr);
    let mutator_ref = simple_map::borrow(&refs.mutator_refs, &token_addr);

    property_map::update_typed(
        mutator_ref,
        &string::utf8(b"level"),
        new_level
    );
}
```

### Composable NFTs (Nesting)

```move
// Create parent NFT
let parent_ref = token::create_named_token(/* parent */);
let parent_addr = object::address_from_constructor_ref(&parent_ref);

// Create child NFT owned by parent
let child_ref = token::create_named_token(/* child */);
let transfer_ref = object::generate_transfer_ref(&child_ref);
let linear_transfer_ref = object::generate_linear_transfer_ref(&transfer_ref);

object::transfer_with_ref(linear_transfer_ref, parent_addr);
```

### Supply-Limited Minting

```move
struct MintState has key {
    minted: u64,
    max_supply: u64,
}

public entry fun mint_limited(
    creator: &signer,
    collection: String,
    name: String
) acquires MintState {
    let state = borrow_global_mut<MintState>(@my_addr);

    assert!(state.minted < state.max_supply, ERROR_MAX_SUPPLY_REACHED);

    token::create_named_token(/* ... */);

    state.minted = state.minted + 1;
}
```

## Token Standards Comparison

### Coin vs Fungible Asset

| Feature | Coin | Fungible Asset |
|---------|------|----------------|
| Ease of use | ✅ Simple | ⚠️ More complex |
| Flexibility | ❌ Limited | ✅ Highly flexible |
| Freeze/Pause | ✅ Yes | ✅ Yes (more control) |
| Custom logic | ❌ Limited | ✅ Extensive |
| Gas cost | ✅ Lower | ⚠️ Slightly higher |
| Adoption | ✅ Wide | 🆕 Growing |
| Recommendation | Legacy/Simple | New projects |

### Token V1 vs Digital Asset (Token V2)

| Feature | Token V1 | Digital Asset |
|---------|----------|---------------|
| Object model | ❌ No | ✅ Yes |
| Composability | ❌ Limited | ✅ High |
| Properties | ⚠️ Basic | ✅ Rich |
| Soul-bound | ❌ No | ✅ Yes |
| Royalties | ✅ Yes | ✅ Yes (better) |
| Status | ⚠️ Deprecated | ✅ Current |
| Recommendation | Legacy only | All new projects |

## Common Patterns Summary

### For Fungible Tokens

```
Use Coin when:
- Simple token needed
- Following existing integrations
- Maximum compatibility

Use Fungible Asset when:
- Need advanced features (pause, freeze)
- Building new protocol
- Want future-proof solution
```

### For NFTs

```
Use Digital Asset (Token V2) for:
- All new NFT projects
- Collections with properties
- Composable/evolving NFTs
- Soul-bound tokens
- Advanced marketplace integration
```

## Best Practices

### ✅ Security

- Store capability refs securely (in resource under deployer account)
- Validate inputs before minting/burning
- Use proper access control for admin functions
- Test thoroughly before mainnet deployment
- Consider upgrade patterns early

### ✅ Design

- Choose appropriate standard for use case
- Design metadata schema carefully
- Plan for future extensibility
- Document token economics clearly
- Consider gas optimization

### ✅ User Experience

- Implement proper error messages
- Auto-register users when needed
- Show clear token information
- Handle edge cases gracefully
- Provide good metadata/images

### ❌ Avoid

- Don't expose capability refs publicly
- Don't hardcode addresses (use named objects)
- Avoid unlimited minting without controls
- Don't skip supply tracking
- Avoid complex logic in entry functions

## TypeScript SDK Integration

### Coin Operations

```typescript
import { Aptos, AptosConfig, Network } from "@aptos-labs/ts-sdk";

const aptos = new Aptos(new AptosConfig({ network: Network.TESTNET }));

// Get coin balance
const balance = await aptos.getAccountCoinAmount({
  accountAddress: "0x123...",
  coinType: "0x1::aptos_coin::AptosCoin"
});

// Transfer coins
const txn = await aptos.transaction.build.simple({
  sender: sender.accountAddress,
  data: {
    function: "0x1::coin::transfer",
    typeArguments: ["0x1::aptos_coin::AptosCoin"],
    functionArguments: [recipient, amount],
  },
});
```

### NFT Operations

```typescript
// Get owned tokens
const tokens = await aptos.getAccountOwnedTokens({
  accountAddress: "0x123..."
});

// Get token data
const tokenData = await aptos.getDigitalAssetData({
  digitalAssetAddress: "0xabc..."
});
```

## Testing Token Standards

```move
#[test(creator = @my_addr, user = @0x123)]
fun test_mint_and_transfer(creator: &signer, user: &signer) {
    // Initialize
    init_module(creator);

    // Register user
    coin::register<MyCoin>(user);

    // Mint to user
    mint(creator, signer::address_of(user), 1000);

    // Verify balance
    assert!(coin::balance<MyCoin>(signer::address_of(user)) == 1000, 0);
}

#[test(creator = @my_addr)]
#[expected_failure(abort_code = ERROR_MAX_SUPPLY)]
fun test_mint_exceeds_supply(creator: &signer) {
    init_module(creator);
    mint(creator, @0x123, MAX_SUPPLY + 1);
}
```

## Response Style

- **Standard-first** - Recommend appropriate framework immediately
- **Code examples** - Show complete, working implementations
- **Compare options** - Explain trade-offs between standards
- **Security-aware** - Highlight security considerations
- **Practical** - Focus on real-world use cases

## Follow-up Suggestions

After helping with tokens, suggest:
- Testing strategy for token operations
- Frontend integration approach
- Marketplace compatibility considerations
- Token economics review
- Upgrade/migration patterns
- Gas optimization techniques
