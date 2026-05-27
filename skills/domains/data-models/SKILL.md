---
name: midnight-core-concepts:data-models
description: Use when asking about UTXO vs account models, ledger tokens, shielded/unshielded tokens, nullifiers, coins, balances, or choosing between token paradigms in Midnight.
---

# Midnight Data Models

Midnight supports two distinct token paradigms: **UTXO-based ledger tokens** and **account-based contract tokens**. Choose based on privacy requirements and use case complexity.

## Quick Decision Guide

| Requirement | Use UTXO (Ledger Tokens) | Use Account (Contract Tokens) |
|-------------|--------------------------|-------------------------------|
| Privacy critical | Yes - independent, shieldable | No - balances visible |
| Parallel processing | Yes - no ordering deps | No - sequential nonce |
| Simple transfers | Yes | Overkill |
| Complex DeFi logic | Limited | Yes |
| Gaming state machines | No | Yes |
| Governance/delegation | No | Yes |

## UTXO Model (Ledger Tokens)

UTXO = Unspent Transaction Output. Each token is a discrete digital coin that must be spent entirely.

### Core Mechanics

```
Creation → Existence → Consumption → Prevention of Reuse
```

1. **Creation**: UTXO born with value, owner, cryptographic commitment
2. **Existence**: Queryable in active UTXO set
3. **Consumption**: Entire UTXO spent in transaction (change returned as new UTXO)
4. **Prevention**: Nullifier added to global set, prevents double-spend

### Nullifier Innovation

Unlike Bitcoin's spent markers, Midnight uses nullifiers:

```
nullifier = Hash(UTXO_commitment, ownerSecret)
```

**Privacy benefit**: Nullifier reveals nothing about which UTXO was spent. The nullifier can be computed without exposing the original UTXO identity.

### Shielded vs Unshielded

Each UTXO independently chooses privacy level:
- **Shielded**: Commitment hidden, value/owner private
- **Unshielded**: Value visible for regulatory compliance

```compact
// Receiving shielded tokens
receive coins: Coin[];

// Sending tokens (can be shielded or unshielded)
send value: QualifiedValue, to: Address;
```

## Account Model (Contract Tokens)

Maintain address-to-balance mappings within Compact contracts. Similar to ERC-20.

### When to Use

- Complex DeFi state machines requiring intricate interactions
- Gaming systems with stateful game logic
- Governance tokens with delegation mechanics
- Social tokens tracking relationships

### Trade-offs

| Aspect | Account Model Limitation |
|--------|-------------------------|
| Privacy | Every transaction visible forever |
| Ordering | Nonce creates sequential dependency |
| MEV | Mempool visibility enables front-running |
| Scalability | Redundant computation on every node |

## Ledger Structure

Midnight's ledger has two components:

### 1. Zswap State
- Merkle tree of coin commitments
- Free slot index
- Nullifier set
- Valid past Merkle roots

### 2. Contract Map
- Associates contract addresses with states
- Contains public and private state components

## Token Types

Token types are 256-bit collision-resistant hashes:
- **Native token**: Predefined zero value
- **Custom tokens**: Hash of contract address + domain separator

```compact
// Issue custom token from contract
// Type = Hash(contractAddress, domainSeparator)
```

## Practical Application

### Choose UTXO When:
1. Users need transaction privacy
2. High throughput required (parallel processing)
3. Simple value transfers dominate
4. Regulatory compliance via selective disclosure (viewing keys)

### Choose Account When:
1. Complex state logic required
2. Tokens interact with sophisticated contract logic
3. Privacy is secondary to functionality
4. Integration with existing DeFi patterns

## References

For detailed technical information:
- **`references/utxo-mechanics.md`** - Complete UTXO lifecycle, nullifier computation
- **`references/ledger-structure.md`** - Zswap state internals, Merkle tree details

## Examples

Working Compact patterns:
- **`examples/token-handling.compact`** - Receiving and sending tokens
