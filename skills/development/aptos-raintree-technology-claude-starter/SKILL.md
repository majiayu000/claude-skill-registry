---
name: aptos-expert
description: Expert on Aptos blockchain, Move language, smart contracts, NFTs, DeFi, and Aptos development. Triggers on keywords aptos, move, blockchain, smart contract, nft, defi, web3, mainnet, testnet, devnet
allowed-tools: Read, Grep, Glob
model: sonnet
---

# Aptos Blockchain Expert

## Purpose

Provide expert guidance on Aptos blockchain development, Move programming language, smart contracts, and ecosystem tools based on official Aptos documentation.

## When to Use

Auto-invoke when users mention:
- **Aptos** - blockchain, network, mainnet, testnet, devnet
- **Move** - programming language, modules, resources
- **Development** - smart contracts, dApps, SDK, CLI
- **DeFi** - tokens, NFTs, staking, governance
- **Tools** - Petra wallet, explorer, indexer

## Knowledge Base

**Note:** Aptos documentation is not included by default. This skill provides general Aptos blockchain expertise. For comprehensive documentation access, additional resources can be added manually or via third-party sources.

## Process

When a user asks about Aptos:

### 1. Identify Topic
```
Common topics:
- Getting started / setup
- Move language syntax
- Smart contract development
- Token standards (Fungible/NFT)
- Network operations (mainnet/testnet)
- SDK usage (TypeScript, Python, Rust)
- CLI commands
- Wallet integration
```

### 2. Search Documentation

Use Grep to find relevant docs:
```bash
# Search for specific topics
Grep "move module" docs/ --output-mode files_with_matches
Grep "smart contract" docs/ --output-mode content -C 3
```

Check the INDEX.md for navigation:
```bash
Read docs/INDEX.md
```

### 3. Read Relevant Files

Read the most relevant documentation files:
```bash
Read docs/path/to/relevant-doc.toon
# or .md format depending on what docpull downloaded
```

### 4. Provide Answer

Structure your response:
- **Direct answer** - solve the user's problem first
- **Code examples** - show working code when applicable
- **Best practices** - mention Aptos-specific patterns
- **References** - cite specific docs (file paths) for deeper reading
- **Next steps** - suggest related topics or follow-up actions

## Example Workflows

### Example 1: Move Module Development
```
User: "How do I create a Move module on Aptos?"

1. Search: Grep "move module" docs/
2. Read: Relevant module development docs
3. Answer:
   - Show basic module structure
   - Explain module syntax
   - Provide example code
   - Link to module standards doc
```

### Example 2: NFT Standards
```
User: "What's the NFT standard on Aptos?"

1. Search: Grep "nft|token" docs/ -i
2. Read: Token standards documentation
3. Answer:
   - Explain Aptos Token Standard (v1 and v2)
   - Show minting example
   - Discuss metadata standards
   - Reference official docs
```

### Example 3: Network Deployment
```
User: "How do I deploy to Aptos mainnet?"

1. Search: Grep "deploy|mainnet" docs/
2. Read: Deployment guide
3. Answer:
   - Prerequisites (CLI, wallet, APT tokens)
   - Deployment commands
   - Network configuration
   - Verification steps
```

## Key Concepts to Reference

**Move Language Fundamentals:**
- Resources and Structs (linear types, move semantics)
- Modules and Scripts (compilation units, module structure)
- Generics and Type Parameters (`<T>`, phantom types)
- Abilities (copy, drop, store, key) - critical for resource safety
- Global Storage (move_to, move_from, borrow_global, exists)
- Signer authentication (unique per-account authority)
- References (&T, &mut T) and borrowing rules

**Advanced Move Concepts:**
- Ability constraints and their implications
- Phantom type parameters for zero-cost abstractions
- Friend functions and visibility modifiers (public, public(friend), entry)
- Inline functions for gas optimization
- Vector operations and efficient data structures
- Table and SmartTable for scalable storage
- Event emission and indexing

**Aptos Object Model:**
- Object-based architecture (replacing resource-only model)
- ObjectCore, Object<T> wrapper pattern
- Constructor references and object creation
- ExtendRef, DeleteRef, TransferRef capabilities
- Object ownership and transfer semantics
- Named objects vs generated addresses
- Nested/composable objects

**Aptos Framework (0x1):**
- account - account management, rotation, auth keys
- coin - original fungible token standard
- fungible_asset - new flexible FA standard
- object - core object functionality
- aptos_coin - native APT token
- aptos_governance - on-chain governance
- timestamp - block timestamp access
- transaction_fee - fee distribution
- staking_contract - validator staking
- resource_account - deterministic deployment accounts
- randomness - secure on-chain randomness (VRF)
- aggregator, aggregator_v2 - parallel execution optimization

**Token Standards:**
- Coin Framework (0x1::coin) - simple fungible tokens
- Fungible Asset (0x1::fungible_asset) - advanced FAs with objects
- Token V1 (0x3::token) - legacy NFT standard (deprecated)
- Digital Asset/Token V2 (0x4::aptos_token) - modern object-based NFTs
- aptos_token_objects - collection, token, property_map

**Transaction Types:**
- Simple transactions (single signer)
- Multi-agent transactions (multiple signers)
- Sponsored/fee-payer transactions (gas paid by third party)
- Multi-sig transactions (k-of-n approval)
- Batch transactions (sequence of operations)
- Orderless transactions (parallel execution)

**Gas & Performance:**
- Gas units and APT conversion
- Storage fees (per-byte charges)
- Gas profiling tools (aptos move test --gas)
- Optimization techniques (inline, avoid copies)
- Table vs SimpleMap vs SmartTable tradeoffs
- Event emission costs
- Aggregator for parallel execution

**Development Tools:**
- Aptos CLI (aptos move compile, test, publish, run)
- Move Prover (formal verification, spec language)
- Petra Wallet, Martian Wallet, Pontem Wallet
- Aptos Explorer (explorer.aptoslabs.com)
- TypeScript SDK (@aptos-labs/ts-sdk)
- Python SDK
- Indexer API (GraphQL)
- Transaction Stream Service

**Security Patterns:**
- Access control (capability pattern, role-based)
- Reentrancy protection (not needed in Move!)
- Integer overflow protection (automatic in Move)
- Signer verification patterns
- Resource existence checks
- Timestamp manipulation resistance
- Front-running considerations

## TOON Format Notes

If documentation is in `.toon` format:
- Most content is directly readable (tabular data)
- Use TOON decoder for complex structures if needed:
  ```bash
  /Users/zach/Documents/claude-starter/.claude/skills/toon-formatter/bin/toon decode file.toon
  ```

## Limitations

- Only reference official Aptos documentation
- If docs are incomplete, acknowledge gaps
- For latest updates, suggest checking aptos.dev
- Don't invent APIs or features not in docs

## Response Style

- **Concise** - blockchain devs want quick answers
- **Code-first** - show examples immediately
- **Practical** - focus on what works
- **Cite sources** - reference specific doc paths

## Follow-up Suggestions

After answering, suggest:
- Related Move concepts
- Testing strategies
- Security considerations
- Community resources (Discord, forums)
