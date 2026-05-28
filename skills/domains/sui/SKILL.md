---
name: sui-knowledge
description: Answer questions about Sui blockchain ecosystem, concepts, tokenomics, validators, staking, and general knowledge. Use when users ask "what is Sui", "how does Sui work", "Sui vs other chains", or any Sui-related questions that aren't specifically about Move programming.
version: 1.0.0
metadata:
  author: EasonClawdbot1
  tags: sui, blockchain, web3, knowledge, ecosystem
---

# Sui Knowledge Base

Expert knowledge about Sui blockchain ecosystem. Use this skill to answer questions about Sui concepts, architecture, tokenomics, and ecosystem.

## When to Use This Skill

Activate when users ask about:
- What is Sui? How does it work?
- Sui vs Ethereum/Solana/other chains
- SUI token, tokenomics, staking
- Validators, consensus, transactions
- Sui ecosystem, projects, wallets
- Object model, ownership concepts
- Performance, TPS, finality

**For Move programming questions → use `sui-move` skill instead**

## Setup References

```bash
cd {baseDir}
chmod +x setup.sh && ./setup.sh
```

This clones:
- Sui official documentation
- Sui whitepaper and technical docs

## Quick Search

```bash
# Search Sui docs
rg -i "keyword" {baseDir}/references/sui-docs/ --type md -C 2

# Search for specific concepts
rg -i "object|ownership|transfer" {baseDir}/references/ --type md
```

## Core Concepts

### What is Sui?

Sui is a Layer 1 blockchain designed for high throughput and low latency. Key innovations:

1. **Object-Centric Model**: Unlike account-based chains, Sui treats everything as objects with unique IDs
2. **Parallel Execution**: Independent transactions execute in parallel without global ordering
3. **Move Language**: Safe, resource-oriented smart contract language
4. **Mysticeti Consensus**: Fast finality (~390ms) for shared objects

### Object Model

```
┌─────────────────────────────────────────┐
│              Object Types               │
├─────────────────────────────────────────┤
│ Owned Objects    → Single owner address │
│ Shared Objects   → Multiple can access  │
│ Immutable Objects→ Frozen, read-only    │
│ Wrapped Objects  → Nested in another    │
└─────────────────────────────────────────┘
```

- Every object has a unique `ObjectID` (32 bytes)
- Objects have `version` that increments on mutation
- Owned object transactions don't need consensus (fast path)

### Transaction Types

| Type | Consensus | Speed | Use Case |
|------|-----------|-------|----------|
| Owned Object | No (fast path) | ~200ms | Transfers, simple ops |
| Shared Object | Yes (Mysticeti) | ~390ms | DEX, auctions, games |

### SUI Token

- **Ticker**: SUI
- **Total Supply**: 10 billion SUI
- **Uses**: Gas fees, staking, governance
- **Smallest Unit**: MIST (1 SUI = 10^9 MIST)

### Gas Model

- Gas price in MIST per computation unit
- Storage rebates: Get gas back when deleting objects
- Sponsored transactions: Third party pays gas

### Validators & Staking

- Delegated Proof of Stake (DPoS)
- ~100+ active validators
- Stake SUI to validators to earn rewards
- Epoch: ~24 hours

### Consensus: Mysticeti

- DAG-based consensus protocol
- Sub-second finality for shared objects
- Replaces Narwhal/Bullshark (used previously)

## Sui vs Other Chains

| Feature | Sui | Ethereum | Solana |
|---------|-----|----------|--------|
| Model | Object-centric | Account-based | Account-based |
| Language | Move | Solidity | Rust |
| TPS | 100k+ | ~15 | ~65k |
| Finality | <1s | ~12min | ~400ms |
| Parallel Exec | Yes (objects) | Limited | Yes |

## Ecosystem

### Wallets
- Sui Wallet (official)
- Suiet
- Ethos
- Martian

### DEXs
- Cetus
- Turbos
- DeepBook (order book)

### NFT Marketplaces
- BlueMove
- Clutchy
- Hyperspace

### Developer Tools
- Sui CLI
- Sui Explorer
- Move Analyzer (VSCode)

## Common Questions

### "Is Sui EVM compatible?"
No. Sui uses Move, not EVM. However, bridges exist to transfer assets from EVM chains.

### "How fast is Sui?"
- Owned object txs: ~200ms
- Shared object txs: ~390ms
- Theoretical TPS: 100,000+

### "How do I stake SUI?"
1. Open Sui Wallet
2. Go to Staking tab
3. Choose a validator
4. Enter amount and confirm

### "What's the difference between Sui Move and Aptos Move?"
- Sui uses object-centric storage
- Different standard library
- Sui has native object primitives
- Some syntax differences in Move 2024

## Answering Workflow

1. **Identify the question type**:
   - General knowledge → Answer from this skill
   - Move programming → Refer to sui-move skill
   - Specific API/code → Search references

2. **Search if needed**:
   ```bash
   rg -i "question keywords" {baseDir}/references/
   ```

3. **Provide clear answer** with:
   - Direct answer first
   - Supporting details
   - Links to official docs if relevant

## Official Resources

- Website: https://sui.io
- Docs: https://docs.sui.io
- GitHub: https://github.com/MystenLabs/sui
- Discord: https://discord.gg/sui
- Twitter: @SuiNetwork
