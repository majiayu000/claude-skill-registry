---
name: search-aptos-examples
description:
  "Searches aptos-core and daily-move for reference implementations before writing contracts. Triggers on: 'search
  examples', 'find example', 'check aptos-core', 'is there an example', 'reference implementation', 'how does aptos
  implement', 'similar contract', 'daily-move'."
license: MIT
metadata:
  author: aptos-labs
  version: "1.0"
  category: move
  tags: ["examples", "reference", "patterns", "aptos-core", "daily-move"]
  priority: high
---

# Search Aptos Examples Skill

## Overview

This skill helps you find relevant examples in official Aptos repositories before writing new contracts. **Always search
examples first** to follow established patterns.

**Repositories:**

- **`aptos-labs/aptos-core/aptos-move/move-examples/`** — 53+ official Move examples demonstrating best practices
- **`aptos-labs/daily-move/snippets/`** — 17 curated educational examples covering design patterns, Move 2 features,
  composable NFTs, and more

## Core Workflow

### Step 1: Identify What You're Building

Categorize your contract:

- **NFTs/Tokens**: NFT collections, digital assets, collectibles
- **Fungible Assets**: Coins, tokens, currencies
- **DeFi**: DEXs, AMMs, lending, staking
- **Governance**: DAOs, voting, proposals
- **Marketplace**: Trading, escrow, auctions
- **Gaming**: Items, characters, game logic
- **Infrastructure**: Registries, configs, utilities

### Step 2: Search Relevant Examples

**Priority Examples by Category:**

#### NFTs & Token Objects

1. **`token_objects/`** - Modern object-based tokens (V2 pattern)
2. **`mint_nft/`** - NFT minting patterns
3. **`nft_dao/`** - NFT-gated governance
4. **`collection_manager/`** - Collection management
5. **(daily-move) `composable-nfts/`** - NFTs that contain other NFTs
6. **(daily-move) `modifying-nfts/`** - Mutable NFT metadata patterns
7. **(daily-move) `parallel-nfts/`** - Concurrent NFT minting
8. **(daily-move) `liquid-nfts/`** - Fractionalized/liquid NFTs

**When to use:** Building NFT collections, digital collectibles, tokenized assets

#### Fungible Assets

1. **`fungible_asset/`** - Modern fungible token standard
2. **`coin/`** - Basic coin implementation
3. **`managed_fungible_asset/`** - Controlled fungible assets
4. **(daily-move) `fa-lockup-example/`** - FA lockup and escrow patterns
5. **(daily-move) `fractional-token/`** - Fractional token ownership
6. **(daily-move) `controlled-mint/`** - Controlled minting with access control

**When to use:** Creating tokens, currencies, reward points

#### DeFi & Trading

1. **`marketplace/`** - NFT marketplace patterns
2. **`swap/`** - Simple token swap
3. **`liquidity_pool/`** - AMM pool implementation
4. **`staking/`** - Staking mechanisms

**When to use:** Building DEXs, marketplaces, trading platforms

#### Governance & DAOs

1. **`dao/`** - DAO governance patterns
2. **`voting/`** - Voting mechanisms
3. **`multisig/`** - Multi-signature accounts

**When to use:** Building DAOs, governance systems, voting

#### Basic Patterns

1. **`hello_blockchain/`** - Module structure basics
2. **`message_board/`** - Simple state management
3. **`resource_account/`** - Resource patterns (legacy - avoid for new code)
4. **(daily-move) `error-codes/`** - Error code conventions and patterns
5. **(daily-move) `private-vs-public/`** - Function visibility and access
6. **(daily-move) `objects/`** - Object model fundamentals

**When to use:** Learning Move basics, simple contracts

#### Advanced Patterns

1. **`object_playground/`** - Object model exploration
2. **`capability/`** - Capability-based security
3. **`upgradeable/`** - Upgradeable contracts
4. **(daily-move) `design-patterns/`** - Autonomous objects and other design patterns
5. **(daily-move) `struct-capabilities/`** - Struct-based capability patterns
6. **(daily-move) `move-2/`** - Move 2 language features and idioms
7. **(daily-move) `storage/`** - Storage layout and optimization patterns
8. **(daily-move) `data-structures/`** - Heap data structure implementation

**When to use:** Complex architectures, security patterns

#### Gaming

1. **(daily-move) `lootbox/`** - Randomized loot box mechanics

**When to use:** Building games, randomized rewards, loot systems

### Step 3: Review Example Code

**What to look for:**

1. **Module Structure:**
   - How are imports organized?
   - What structs are defined?
   - How are error codes structured?

2. **Object Creation:**
   - How are objects created?
   - Which refs are generated?
   - How is ownership managed?

3. **Access Control:**
   - How is signer authority verified?
   - How is object ownership checked?
   - What roles/permissions exist?

4. **Operations:**
   - How are transfers handled?
   - How are updates secured?
   - What validations are performed?

5. **Testing:**
   - What test patterns are used?
   - How is coverage achieved?

### Step 4: Adapt Patterns to Your Use Case

**Don't copy blindly - adapt:**

1. **Understand the pattern:** Why is it structured this way?
2. **Identify core concepts:** What security checks are critical?
3. **Adapt to your needs:** Modify for your specific requirements
4. **Maintain security:** Keep all security checks intact
5. **Test thoroughly:** Ensure 100% coverage

## Example Discovery Table

| Building          | Search For                          | Source     | Key Files                                    |
| ----------------- | ----------------------------------- | ---------- | -------------------------------------------- |
| NFT Collection    | `token_objects`, `mint_nft`         | aptos-core | `token_objects/sources/token.move`           |
| Fungible Token    | `fungible_asset`                    | aptos-core | `fungible_asset/sources/fungible_asset.move` |
| Marketplace       | `marketplace`                       | aptos-core | `marketplace/sources/marketplace.move`       |
| DAO               | `dao`, `voting`                     | aptos-core | `dao/sources/dao.move`                       |
| Token Swap        | `swap`, `liquidity_pool`            | aptos-core | `swap/sources/swap.move`                     |
| Staking           | `staking`                           | aptos-core | `staking/sources/staking.move`               |
| Simple Contract   | `hello_blockchain`, `message_board` | aptos-core | `hello_blockchain/sources/hello.move`        |
| Object Patterns   | `object_playground`                 | aptos-core | `object_playground/sources/playground.move`  |
| Composable NFTs   | `composable-nfts`                   | daily-move | `snippets/composable-nfts/`                  |
| FA Lockup/Escrow  | `fa-lockup-example`                 | daily-move | `snippets/fa-lockup-example/`                |
| Design Patterns   | `design-patterns`                   | daily-move | `snippets/design-patterns/`                  |
| Move 2 Features   | `move-2`                            | daily-move | `snippets/move-2/`                           |
| Data Structures   | `data-structures`                   | daily-move | `snippets/data-structures/`                  |
| Storage Patterns  | `storage`                           | daily-move | `snippets/storage/`                          |
| Loot Box Patterns | `lootbox`                           | daily-move | `snippets/lootbox/`                          |

## How to Access Examples

### Option 1: GitHub Web Interface

```
https://github.com/aptos-labs/aptos-core/tree/main/aptos-move/move-examples
```

Browse online and read source files directly.

### Option 2: Clone Repository (Recommended)

```bash
# Clone Aptos core
git clone https://github.com/aptos-labs/aptos-core.git

# Navigate to examples
cd aptos-core/aptos-move/move-examples

# List all examples
ls -la

# View specific example
cd token_objects
cat sources/token.move
```

### Option 3: daily-move Repository

**Browse online:**

```
https://github.com/aptos-labs/daily-move/tree/main/snippets
```

**Clone locally:**

```bash
git clone https://github.com/aptos-labs/daily-move.git
cd daily-move/snippets
ls -la
```

### Option 4: Search Aptos Documentation

```
https://aptos.dev/build/smart-contracts
```

Many examples are documented with explanations.

## Common Patterns from Examples

### Pattern 1: Object Creation (from token_objects)

```move
// From: token_objects/sources/token.move
public entry fun create_token(
    creator: &signer,
    collection_name: String,
    description: String,
    name: String,
    uri: String,
) {
    let constructor_ref = token::create_named_token(
        creator,
        collection_name,
        description,
        name,
        option::none(),
        uri,
    );
    // ... additional setup
}
```

**Takeaway:** Use named tokens for collections, create_object for unique items.

### Pattern 2: Access Control (from dao)

```move
// From: dao/sources/dao.move
public entry fun execute_proposal(
    proposer: &signer,
    proposal_id: u64
) acquires DAO, Proposal {
    let dao = borrow_global_mut<DAO>(@dao_addr);
    let proposal = vector::borrow_mut(&mut dao.proposals, proposal_id);

    // Verify proposal passed
    assert!(proposal.votes_for > proposal.votes_against, E_PROPOSAL_NOT_PASSED);

    // Execute actions
    // ...
}
```

**Takeaway:** Verify state conditions before executing critical operations.

### Pattern 3: Transfer Control (from fungible_asset)

```move
// From: fungible_asset/sources/fungible_asset.move
public fun transfer<T: key>(
    from: &signer,
    to: address,
    amount: u64
) acquires FungibleStore {
    // Verify sender has sufficient balance
    let from_store = borrow_global_mut<FungibleStore<T>>(signer::address_of(from));
    assert!(from_store.balance >= amount, E_INSUFFICIENT_BALANCE);

    // Deduct from sender
    from_store.balance = from_store.balance - amount;

    // Add to recipient
    let to_store = borrow_global_mut<FungibleStore<T>>(to);
    to_store.balance = to_store.balance + amount;
}
```

**Takeaway:** Check-effects-interactions pattern (verify, deduct, add).

## ALWAYS Rules

- ✅ ALWAYS search examples before writing new contracts
- ✅ ALWAYS check both aptos-core (canonical) and daily-move (educational) repositories
- ✅ ALWAYS understand patterns before copying
- ✅ ALWAYS adapt patterns to your use case
- ✅ ALWAYS maintain security checks from examples
- ✅ ALWAYS reference which example you adapted from
- ✅ ALWAYS test adapted code thoroughly

## NEVER Rules

- ❌ NEVER copy code without understanding it
- ❌ NEVER skip security checks from examples
- ❌ NEVER use deprecated patterns (resource accounts, address-based)
- ❌ NEVER assume examples are always up-to-date (verify against docs)
- ❌ NEVER mix V1 and V2 patterns
- ❌ NEVER include real private keys or credentials when adapting examples — use `"0x..."` placeholders

## Search Checklist

Before writing contract code:

- [ ] Identified category (NFT, DeFi, DAO, etc.)
- [ ] Found 2-3 relevant examples in aptos-core
- [ ] Checked daily-move snippets for educational examples
- [ ] Reviewed module structure
- [ ] Identified security patterns
- [ ] Understood object creation patterns
- [ ] Noted access control mechanisms
- [ ] Checked test patterns
- [ ] Ready to adapt to my use case

## Example Adaptation Workflow

### Step-by-Step: Building NFT Collection

1. **Search:** Find `token_objects` example
2. **Review Structure:**

   ```
   token_objects/
   ├── sources/
   │   ├── collection.move  # Collection management
   │   ├── token.move       # Token operations
   │   └── property_map.move # Metadata handling
   └── tests/
       └── token_tests.move
   ```

3. **Identify Key Patterns:**
   - Collection creation with `create_collection`
   - Token minting with `create_named_token`
   - Metadata storage using `PropertyMap`
   - Transfer control with `TransferRef`

4. **Adapt to Your Needs:**
   - Keep object creation pattern
   - Keep security checks
   - Add your custom fields
   - Add your business logic
   - Write comprehensive tests

5. **Reference in Code:**
   ```move
   // Adapted from: aptos-core/move-examples/token_objects
   module my_addr::custom_nft {
       // ... your implementation
   }
   ```

## References

**Official Examples:**

- aptos-core: https://github.com/aptos-labs/aptos-core/tree/main/aptos-move/move-examples
- daily-move: https://github.com/aptos-labs/daily-move/tree/main/snippets
- Documentation: https://aptos.dev/build/smart-contracts

**Related Skills:**

- `write-contracts` - Apply patterns after searching
- `security-audit` - Verify security of adapted code
- `generate-tests` - Test adapted patterns

---

**Remember:** Search examples first. Understand patterns. Adapt securely. Test thoroughly.
